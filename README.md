# Citi Bike Daily Demand Prediction: STAT GR5243 Project 4

End-to-end machine learning pipeline that predicts **daily station-level Citi Bike trip demand** in New York City using Citi Bike trip records, daily weather conditions, and station-level context features.

This project follows a complete data science workflow: data acquisition, cleaning, aggregation, exploratory data analysis, feature engineering, unsupervised learning, supervised modeling, model evaluation, and communication through both a written report and an interactive dashboard.

## Live Dashboard

The final interactive Shiny dashboard is available here:

[Citi Bike Demand Dashboard](https://helenaliyz.shinyapps.io/citibike-dashboard/)

The dashboard presents the project in an interactive format across five tabs. It includes data overview, demand patterns, weather relationships, station-level exploration, and a live demand predictor that allows users to input station and weather conditions to generate predicted Citi Bike demand.

## Final Result

| Model | MAE | RMSE | R² |
|---|---:|---:|---:|
| **Tuned Random Forest** (final) | **19.75** | **28.13** | **0.289** |
| Random Forest | 21.23 | 29.70 | 0.207 |
| Gradient Boosting | 24.70 | 32.71 | 0.038 |
| Ridge Regression | 25.85 | 35.78 | −0.151 |

The **tuned Random Forest** was selected as the final model because it achieved the best overall predictive performance and handled nonlinear relationships between demand, weather, lagged demand, calendar variables, and station context more effectively than the linear baseline.

Top predictors included previous-day demand (`lag_1_trip_count`), mean temperature, max wind speed, precipitation, and same-weekday-last-week demand (`lag_7_trip_count`). These results suggest that Citi Bike demand is strongly shaped by recent usage patterns and short-term weather conditions.

## Repository Structure

```text
5243Project4/
├── Raw Data/                                 # Random samples from raw Citi Bike monthly trip files
├── Data Acquisition and Preprocessing/
│   ├── data_acquisition_cleaning.ipynb       # Web scraping, trip cleaning, Open-Meteo API integration, station-day aggregation
│   └── citibike_station_day_clean.csv        # Final analytic CSV, one row per station per day
├── Data Analysis/
│   ├── 5243_project4_analysis.py             # EDA script
│   └── eda_outputs/                          # EDA figures and summary outputs
├── Project 4 Modeling.ipynb                  # Feature engineering, clustering, supervised models, tuning, and evaluation
├── 5243Project4_Report.pdf                   # Final written project report
└── README.md
```

## Data Sources

* **Citi Bike trip records**: monthly trip data from [Citi Bike System Data](https://citibikenyc.com/system-data). These files contain individual trip records, including ride start time, end time, start station, end station, station coordinates, and rider-related fields.
* **Daily weather data**: temperature, precipitation, and wind variables collected from the Open-Meteo API for New York City.
* **Station context features**: station IDs, latitude, longitude, and location-based text features derived from station metadata, including whether station names contain terms such as park, pier, plaza, or square.

The full monthly Citi Bike files are large, so the repository stores sampled raw data rather than full raw files. For each monthly zip file, the data acquisition pipeline randomly samples 100,000 rows. At roughly 250 bytes per row, each sampled CSV is about 25 MB. This keeps each raw sample well below GitHub's 50 MB recommended file size and below the 100 MB hard limit, while still preserving enough trip-level data to document the raw data structure and support reproducibility.

The final modeling dataset is aggregated to the **station-day level**, where each row represents one Citi Bike station on one calendar date. This structure allows the project to predict daily demand at the station level instead of only modeling total citywide demand.

## Pipeline Overview

### 1. Data Acquisition and Cleaning

The project begins by collecting raw Citi Bike monthly trip files and combining them with daily weather data from the Open-Meteo API. The cleaning process standardizes station IDs, parses dates, removes invalid or incomplete records, checks missing values, and aggregates raw trip-level records into a station-day analytic table.

Main output:

```text
Data Acquisition and Preprocessing/citibike_station_day_clean.csv
```

This final CSV contains station-level daily demand, weather variables, station coordinates, calendar variables, and station context features.

### 2. Exploratory Data Analysis

The EDA script investigates the structure of the cleaned data and identifies major demand patterns. The analysis includes:

* daily trip demand trends;
* demand distribution across stations;
* high-demand and low-demand station comparisons;
* weather-demand relationships;
* weekday and weekend patterns;
* correlation analysis among numeric features.

These visualizations help guide later modeling decisions by showing that demand is unevenly distributed across stations and is related to both recent usage history and weather conditions.

Run:

```bash
python "Data Analysis/5243_project4_analysis.py"
```

Outputs are saved in:

```text
Data Analysis/eda_outputs/
```

### 3. Feature Engineering and Preprocessing

The modeling notebook creates features designed to improve predictive performance and prevent data leakage. Key features include:

* `lag_1_trip_count`: previous-day station demand;
* `lag_7_trip_count`: same-weekday-last-week station demand;
* weather variables such as temperature, precipitation, and wind speed;
* binary weather indicators such as `has_precipitation`, `heavy_precipitation`, and `high_wind`;
* cyclical weekday features: `dow_sin` and `dow_cos`;
* station-level context features based on station names;
* station clusters from unsupervised learning.

The target variable is:

```python
log(1 + daily_trip_count)
```

This transformation reduces the effect of extreme high-demand station-days and makes the target distribution more stable for modeling.

### 4. Unsupervised Learning

K-Means clustering is applied to station-level characteristics to identify groups of stations with similar usage and contextual patterns. PCA is used to support visualization and interpretation of the clusters.

The cluster labels are then used as additional features in the supervised models. This connects the unsupervised learning stage to the predictive modeling stage by allowing the models to account for hidden station structure.

### 5. Supervised Modeling and Evaluation

The project compares multiple supervised regression models:

* Ridge Regression;
* Random Forest;
* Gradient Boosting;
* Tuned Random Forest with `GridSearchCV`.

A time-based train-test split is used, where the most recent 20% of dates are held out for testing. This avoids future leakage and better reflects the real forecasting setting, where future demand must be predicted from past data.

Models are evaluated using:

* MAE;
* RMSE;
* R²;
* predicted vs. actual plots;
* residual analysis;
* error by demand quartile;
* feature importance.

The tuned Random Forest is selected as the final model because it has the lowest MAE and RMSE and performs best across different levels of station demand.

## Pipeline Run Order

1. **Acquire and clean data**

```bash
jupyter notebook "Data Acquisition and Preprocessing/data_acquisition_cleaning.ipynb"
```

This produces:

```text
Data Acquisition and Preprocessing/citibike_station_day_clean.csv
```

2. **Run EDA**

```bash
cd "Data Analysis"
python 5243_project4_analysis.py
cd ..
```

This produces EDA figures and summary files in:

```text
Data Analysis/eda_outputs/
```

3. **Run modeling and evaluation**

```bash
jupyter notebook "Project 4 Modeling.ipynb"
```

This notebook runs clustering, feature engineering, model training, hyperparameter tuning, model comparison, and final evaluation.

4. **View the dashboard**

Open the deployed Shiny dashboard:

[https://helenaliyz.shinyapps.io/citibike-dashboard/](https://helenaliyz.shinyapps.io/citibike-dashboard/)

## Environment

Python 3.10+ with:

```text
pandas
numpy
matplotlib
scikit-learn
jupyter
```

Install:

```bash
pip install pandas numpy matplotlib scikit-learn jupyter
```

The interactive dashboard was developed and deployed separately using Shiny.

## How to Reproduce

```bash
git clone <this-repo-url>
cd 5243Project4

# 1. Re-run cleaning if raw trip files are available
jupyter notebook "Data Acquisition and Preprocessing/data_acquisition_cleaning.ipynb"

# 2. Generate EDA figures
cd "Data Analysis" && python 5243_project4_analysis.py && cd ..

# 3. Run modeling and evaluation
jupyter notebook "Project 4 Modeling.ipynb"
```

The cleaned analytic dataset is already included in the repository, so users can also start directly from the EDA or modeling stage without re-downloading the raw Citi Bike data.

## Modeling Choices Summary

* **Predictive question**: Can we predict daily Citi Bike trip demand at the station level using weather, calendar, station context, and recent demand history?
* **Target**: `log(1 + daily_trip_count)` to reduce skewness in station-day demand.
* **Train-test split**: time-based split with the most recent 20% of dates held out for testing.
* **Lag features**: `lag_1_trip_count` and `lag_7_trip_count` capture short-term and weekly demand patterns.
* **Weather features**: temperature, precipitation, wind speed, and binary weather indicators.
* **Calendar features**: weekday encoded using cyclical sine and cosine transformations.
* **Station structure**: K-Means clustering captures differences across station types and usage patterns.
* **Leakage prevention**: same-day rider and bike-type shares are not used as direct supervised predictors because they would not be available before the day’s demand occurs.
* **Final model**: Tuned Random Forest with `n_estimators=300`, `max_depth=None`, and `min_samples_leaf=3`.

## Team Contributions

* **Helena Li (yl6029)**: Built the complete data acquisition and preprocessing pipeline, including the web scraper, Open-Meteo API integration, cleaning, aggregation, and the final analytic CSV. She developed and deployed the full interactive Shiny dashboard across all five sections, and wrote and revised the full project report and repository README.
* **Wentao Zhong (wz2753)**: Conducted exploratory data analysis in Python, generated EDA figures and summary tables in `Data Analysis/`, and supported interpretation of demand patterns, weather relationships, and station-level trends.
* **Kevin Ma (km4189)**: Developed the modeling notebook, including K-Means clustering, PCA visualization, feature engineering, supervised regression models, hyperparameter tuning, and model evaluation.
* **Ketaki Dabade (kvd2112)**: Wrote the final written report, repository organization and README, evaluation interpretation, and presentation slides.

## Deliverables

* Final report: [`5243Project4_Report.pdf`](./5243Project4_Report.pdf)
* Interactive dashboard: [Citi Bike Demand Dashboard](https://helenaliyz.shinyapps.io/citibike-dashboard/)
* Code: notebooks and EDA script in this repository
* Data: sampled raw trip files in `Raw Data/`, cleaned analytic table in `Data Acquisition and Preprocessing/`
* Modeling notebook: [`Project 4 Modeling.ipynb`](./Project%204%20Modeling.ipynb)

## Project Summary

This project shows that Citi Bike demand can be predicted more effectively when recent station-level usage patterns are combined with weather, calendar, and station context features. The final tuned Random Forest model performs better than the linear and untuned baseline models, suggesting that demand is driven by nonlinear interactions between past demand, local station characteristics, and daily weather conditions.

The deployed dashboard extends the analysis beyond a static report by allowing users to explore the data interactively and test demand predictions under different conditions.
