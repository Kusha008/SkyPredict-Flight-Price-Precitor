from playwright.sync_api import sync_playwright
import pandas as pd
import time
import random

airline_codes = {"6E": "Indigo", "AI": "Air India", "IX": "Air India Express", "SG": "Spice Jet", "UK": "Vistara", "QP": "AkasaAir", "I5": "Air India Express"}
stops_numerics = {"Nonstop": 0, "1-stop": 1, "2+-stops": 2}
cities = ["DEL-Delhi", "BOM-Mumbai", "BLR-Bangalore", "HYD-Hyderabad", "MAA-Chennai", "CCU-Kolkata"]

def scrape_flight_data():
    # Start a Playwright session
    with sync_playwright() as p:
        flights = []
        for src_city in cities:
            for dest_city in cities:
                if src_city != dest_city:
                    browser = p.chromium.launch(headless=True)  # Set headless=True to run in the background
                    page = browser.new_page()
                    
                    # Go to the flight search results page
                    url = f"https://flight.easemytrip.com/FlightList/Index?srch={src_city}-India|{dest_city}-India|31/12/2024&px=1-0-0&cbn=0&ar=undefined&isow=true&isdm=true&lang=en-us&&IsDoubleSeat=false&CCODE=IN&curr=INR&apptype=B2C"
                    page.goto(url)
                    
                    # Wait for the page to fully load
                    page.wait_for_load_state('networkidle')  # Wait until network is idle
                    
                    # Wait for the specific flight results container to appear
                    page.wait_for_selector("div.col-md-12.col-sm-12.main-bo-lis.pad-top-bot.ng-scope", timeout=60000)  # Wait up to 60 seconds
                    
                    # Find all flight result elements
                    flight_divs = page.query_selector_all("div.col-md-12.col-sm-12.main-bo-lis.pad-top-bot.ng-scope")
                    cnt = len(flight_divs)
                    print(f"Number of flights found: {cnt}")
                    
                    if not flight_divs:
                        print(f"No flights found for {src_city} to {dest_city}.")
                        continue
                    
                    # Iterate through each flight and extract relevant details
                    for flight in flight_divs:
                        flight_dict = {}
                        flight_dict['flight_class'] = flight.query_selector('span[ng-bind="GetFltDtl(s.b[0].FL[0]).CB"]').inner_text()
                        flight_dict['airline'] = airline_codes.get(flight.query_selector('span[ng-bind="GetFltDtl(s.b[0].FL[0]).AC"]').inner_text(), "Unknown")
                        flight_dict['arrival_time'] = flight.query_selector('span[ng-bind="GetFltDtl(s.b[0].FL[s.b[0].FL.length-1]).ATM"]').inner_text()
                        flight_dict['departure_time'] = flight.query_selector('span[ng-bind="GetFltDtl(s.b[0].FL[0]).DTM"]').inner_text()
                        flight_dict['price'] = flight.query_selector('span[price]').get_attribute('price').strip()
                        flight_dict['src_city'] = flight.query_selector('span[ng-bind="GetAirportName(GetFltDtl(s.b[0].FL[0]).OG)"]').inner_text()
                        flight_dict['dest_city'] = flight.query_selector('span[ng-bind="GetAirportName(GetFltDtl(s.b[0].FL[s.b[0].FL.length-1]).DT)"]').inner_text()
                        flight_dict['duration'] = flight.query_selector('span[ng-bind="s.b[0].JyTm"]').inner_text()
                        flight_dict['stops'] = flight.query_selector('span.dura_md2').inner_text()
                        
                        flights.append(flight_dict)
                    
                    # Close the browser for the current city pair
                    browser.close()

                    # Add a random waiting time between 2 and 3 minutes
                    wait_time = random.randint(1, 60)
                    print(f"Waiting for {wait_time} seconds before the next city pair...")
                    time.sleep(wait_time)

        # Save the collected data to Excel and CSV
        df = pd.DataFrame(flights)
        df.to_excel('flights_31122024.xlsx', index=False)
        # df.to_csv('flights.csv', index=False)

# Run the scraping function
scrape_flight_data()