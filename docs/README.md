
# Coal Demand Forecasting and Procurement Optimization

## Project Overview
This project simulates a thermal power plant coal demand system, focusing on forecasting future coal demand and optimizing procurement strategies to minimize costs while ensuring sufficient stock levels.

## Dataset Description
- **Period**: 2021–2025
- **Target**: Daily coal demand
- **Generation**: Synthetic data is generated for a single thermal power plant to simulate real-world conditions.

## Forecasting Models
The project explores several time series forecasting models to predict daily coal demand:
- **Seasonal Naive Baseline**: A simple baseline model that forecasts the next period's value as the value from the same period in the previous cycle.
- **SARIMA (Seasonal Autoregressive Integrated Moving Average)**: A statistical model used for analyzing and forecasting time series data, taking into account seasonality.
- **SARIMAX (Seasonal Autoregressive Integrated Moving Average with Exogenous Regressors)**: An extension of SARIMA that includes the effect of exogenous (external) variables, such as macroeconomic indicators, to improve forecasting accuracy.

## Procurement Optimization
The core objective of the procurement strategy is to **minimize procurement cost** while consistently maintaining **minimum stock levels** to ensure uninterrupted power generation.
- **Methodology**: Linear Programming is employed to solve the optimization problem.
- **Planning**: Weekly procurement planning is conducted, incorporating stock constraints to manage inventory efficiently.

## Project Folder Structure
```
coal_demand_forecasting/
├── docs/
│   └── README.md
├── data/
│   ├── raw/
│   ├── processed/
├── notebooks/
│   ├── 01_data_generation.ipynb
│   ├── 02_eda.ipynb
│   ├── 03_forecasting_models.ipynb
│   ├── 04_procurement_optimization.ipynb
├── scripts/
│   ├── generate_synthetic_data.py
│   ├── train_models.py
│   ├── run_optimization.py
├── src/
│   ├── data_processing.py
│   ├── models.py
│   ├── optimization.py
├── requirements.txt
├── config.py
```

## How to Run the Project
1.  **Clone the repository**:
    ```bash
    git clone <repository_url>
    cd coal_demand_forecasting
    ```
2.  **Set up the environment**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Generate Synthetic Data**:
    Run the notebook `notebooks/01_data_generation.ipynb` or execute the script `scripts/generate_synthetic_data.py`.
4.  **Perform EDA and Train Models**:
    Follow the steps in `notebooks/02_eda.ipynb` and `notebooks/03_forecasting_models.ipynb` to understand the data and train the demand forecasting models.
5.  **Run Procurement Optimization**:
    Execute `notebooks/04_procurement_optimization.ipynb` or `scripts/run_optimization.py` to perform the weekly procurement planning.

