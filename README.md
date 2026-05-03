# Citi Bike Daily Demand Prediction — STAT GR5243 Project 4

End-to-end machine learning pipeline that predicts **daily station-level Citi Bike trip demand** in New York City using trip records, daily weather, and station context features.

## Final Result

| Model | MAE | RMSE | R² |
|---|---:|---:|---:|
| **Tuned Random Forest** (final) | **19.75** | **28.13** | **0.289** |
| Random Forest | 21.23 | 29.70 | 0.207 |
| Gradient Boosting | 24.70 | 32.71 | 0.038 |
| Ridge Regression | 25.85 | 35.78 | −0.151 |

Top predictors: previous-day demand (`lag_1_trip_count`), mean temperature, max wind speed, precipitation, and same-weekday-last-week demand (`lag_7_trip_count`).

## Repository Structure

```
5243Project4/
├── Raw Data/                                 # Raw Citi Bike monthly trip files (samples)
├── Data Acquisition and Preprocessing/
│   ├── data_acquisition_cleaning.ipynb       # Trip + weather + station merge & cleaning
│   └── citibike_station_day_clean.csv        # One row per station per day (analytic table)
├── Data Analysis/
│   ├── 5243_project4_analysis.py             # EDA script
│   └── *.png                                 # EDA figures (trends, distributions, weather, top stations, correlation)
├── Project 4 Modeling.ipynb                  # Clustering + feature engineering + supervised models + evaluation
├── REPORT.tex                                # Final written report (LaTeX)
└── README.md
```

## Data Sources

- **Citi Bike trip records** — monthly CSVs from <https://citibikenyc.com/system-data> (2–4 months covering weekdays and weekends).
- **Daily weather** — temperature, precipitation, wind from the Open-Meteo API for NYC.
- **Station context** — station IDs, lat/lon, and neighborhood proximity flags (park, pier, plaza, square) derived from station metadata.

## Pipeline (run order)

1. **Acquire & clean**: `Data Acquisition and Preprocessing/data_acquisition_cleaning.ipynb`
   → produces `citibike_station_day_clean.csv`.
2. **EDA**: `python "Data Analysis/5243_project4_analysis.py"`
   → writes figures and summary CSVs into `Data Analysis/eda_outputs/`.
3. **Modeling**: open `Project 4 Modeling.ipynb` and run all cells
   → station clustering (K-Means, k=4), feature engineering (calendar, weather, lag-1/lag-7, log target, station cluster, neighborhood flags), supervised models (Ridge, Random Forest, Gradient Boosting, tuned Random Forest with `GridSearchCV`), and evaluation (MAE / RMSE / R², predicted vs. actual, residuals, error by demand quartile, feature importance).

## Environment

Python 3.10+ with:

```
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

## How to Reproduce

```bash
git clone <this-repo-url>
cd 5243Project4

# 1. (Optional) re-run cleaning if you re-download raw trip files
jupyter notebook "Data Acquisition and Preprocessing/data_acquisition_cleaning.ipynb"

# 2. EDA figures
cd "Data Analysis" && python 5243_project4_analysis.py && cd ..

# 3. Modeling + evaluation
jupyter notebook "Project 4 Modeling.ipynb"

# 4. Build the report
pdflatex REPORT.tex
```

## Modeling Choices (Summary)

- **Target**: `log(1 + daily_trip_count)` — stabilizes the right-skewed demand distribution.
- **Split**: time-based — most recent 20% of dates held out (no future leakage).
- **Lag features per station**: `lag_1_trip_count`, `lag_7_trip_count`.
- **Weather binaries**: `has_precipitation`, `heavy_precipitation` (top-decile), `high_wind` (top-decile).
- **Cyclical calendar**: `dow_sin`, `dow_cos`.
- **Excluded as leakage**: same-day rider/bike-type shares (used only at the station-aggregate level for clustering).
- **Final model**: Tuned Random Forest (`n_estimators=300`, `max_depth=None`, `min_samples_leaf=3`).

## Team Contributions

- **Helena Li (yl6029)** — Data acquisition and cleaning; produced the final aggregated `citibike_station_day_clean.csv`.
- **Wentao Zhong (wz2753)** — Exploratory data analysis in Python; generated all EDA figures and summary tables in `Data Analysis/`.
- **Kevin Ma (km4189)** — Clustering (K-Means + PCA), feature engineering, supervised models (Ridge / Random Forest / Gradient Boosting / tuned RF), and in-notebook model evaluation.
- **Ketaki Dabade (kvd2112)** — Final report (`REPORT.tex`), README and repo organization, evaluation interpretation, and presentation slides.

## Deliverables

- Final report: [`REPORT.tex`](./REPORT.tex)
- Code: notebooks + EDA script in this repo
- Data: raw samples in `Raw Data/`, cleaned analytic table in `Data Acquisition and Preprocessing/`
