# ✈️ SkyPredict: Flight Price Predictor

**SkyPredict** is a machine learning-based system designed to predict domestic flight ticket prices in India using real-time scraped data and a suite of regression algorithms. This project aims to bring transparency to dynamic airfare pricing and help users make informed ticket booking decisions.

---

## Project Overview

- Collected over **65,000 flight records** using Python-based web scraping from MakeMyTrip and EaseMyTrip.
- Cleaned and preprocessed data to handle nulls, outliers, and encoded categorical variables.
- Trained and evaluated **10+ regression models** including:
  - Random Forest Regressor
  - K-Nearest Neighbors (KNN)
  - Decision Tree
  - XGBoost
  - Bagging & Extra Trees Regressor
- Achieved:
  - **R² Score**: 0.76 (Random Forest)
  - **MAPE**: 12.7%
  - **RMSE**: ~2779
- Evaluated using metrics: **R², MAE, RMSE, MAPE**
