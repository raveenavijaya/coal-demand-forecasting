
import os
import pandas as pd
import numpy as np
import pulp

project_path = '/content/drive/MyDrive/coal_demand_forecasting/'
os.chdir(project_path)

# 1. Load the CSV file into a DataFrame called `df`
df = pd.read_csv('data/synthetic_coal_data.csv')

# 2. Clean the column names of the DataFrame by stripping any leading or trailing whitespace
df.columns = df.columns.str.strip()

# 3. Convert the 'Date' column to datetime objects
df['Date'] = pd.to_datetime(df['Date'])

# 4. Sort the DataFrame `df` by the 'Date' column in ascending order
df = df.sort_values(by='Date')

# 5. Filter the DataFrame `df` to include only rows where the 'Date' is in the year 2025.
df_2025 = df[df['Date'].dt.year == 2025].copy()

# 6. Set the 'Date' column as the index of the DataFrame `df_2025`
df_2025 = df_2025.set_index('Date')

# Weekly aggregation
weekly_data_2025 = df_2025.resample('W').agg(
    weekly_demand=('daily_requirement', 'sum'),
    weekly_avg_daily_demand=('daily_requirement', 'mean'),
    domestic_price=('domestic_coal_price_index', 'mean'),
    import_price=('international_coal_price_index', 'mean')
)

# Reset index to make 'Date' a regular column
df_weekly = weekly_data_2025.reset_index()

# Define constants
initial_stock = 900000
normative_stock_days = 23

# Calculate 'minimum_stock'
df_weekly['minimum_stock'] = normative_stock_days * df_weekly['weekly_avg_daily_demand']

# Create 'initial_stock_level' column
df_weekly['initial_stock_level'] = 0.0 # Initialize all to 0.0, first week will be updated
df_weekly.loc[0, 'initial_stock_level'] = initial_stock

# Create 'ending_stock_level' column and initialize with zeros
df_weekly['ending_stock_level'] = 0.0

# Calculate 'maximum_stock'
df_weekly['maximum_stock'] = 45 * df_weekly['weekly_avg_daily_demand']

# Calculate 'holding_cost'
df_weekly['holding_cost'] = 0.02 * df_weekly['domestic_price']

# Create the linear programming problem instance
prob_enhanced = pulp.LpProblem("Enhanced_Coal_Procurement_Optimization", pulp.LpMinimize)

# Get the number of weeks
num_weeks = len(df_weekly)

# Define decision variables
domestic_procurement_vars_enhanced = pulp.LpVariable.dicts("domestic_procurement_enhanced", range(num_weeks), lowBound=0)
import_procurement_vars_enhanced = pulp.LpVariable.dicts("import_procurement_enhanced", range(num_weeks), lowBound=0)
stock_vars_enhanced = pulp.LpVariable.dicts("stock_enhanced", range(num_weeks), lowBound=0)

# Set the objective function (Minimize total procurement and holding costs)
prob_enhanced += pulp.lpSum([
    (domestic_procurement_vars_enhanced[w] * df_weekly['domestic_price'][w]) +
    (import_procurement_vars_enhanced[w] * df_weekly['import_price'][w]) +
    (stock_vars_enhanced[w] * df_weekly['holding_cost'][w])
    for w in range(num_weeks)
]), "Total Procurement and Holding Cost"

# Add constraints for each week
for w in range(num_weeks):
    # Stock Balance Constraint
    if w == 0:
        prob_enhanced += stock_vars_enhanced[w] == initial_stock + domestic_procurement_vars_enhanced[w] + import_procurement_vars_enhanced[w] - df_weekly['weekly_demand'][w], f"Stock_Balance_Week_Enhanced_{w}"
    else:
        prob_enhanced += stock_vars_enhanced[w] == stock_vars_enhanced[w-1] + domestic_procurement_vars_enhanced[w] + import_procurement_vars_enhanced[w] - df_weekly['weekly_demand'][w], f"Stock_Balance_Week_Enhanced_{w}"

    # Minimum Stock Constraint
    prob_enhanced += stock_vars_enhanced[w] >= df_weekly['minimum_stock'][w], f"Minimum_Stock_Week_Enhanced_{w}"

    # Maximum Stock Constraint
    if w == 0:
        effective_max_stock_w0 = max(df_weekly['maximum_stock'][w], initial_stock - df_weekly['weekly_demand'][w])
        prob_enhanced += stock_vars_enhanced[w] <= effective_max_stock_w0, f"Maximum_Stock_Week_Enhanced_{w}"
    else:
        prob_enhanced += stock_vars_enhanced[w] <= df_weekly['maximum_stock'][w], f"Maximum_Stock_Week_Enhanced_{w}"

    # Import Quantity Limit Constraint (Import <= 40% of total procurement)
    prob_enhanced += import_procurement_vars_enhanced[w] <= 0.4 * (domestic_procurement_vars_enhanced[w] + import_procurement_vars_enhanced[w]), f"Import_Limit_Week_Enhanced_{w}"

# Solve the optimization problem
prob_enhanced.solve()

print(f"Enhanced Optimization Status: {pulp.LpStatus[prob_enhanced.status]}")

# Extract optimization results
enhanced_optimization_results = []

for w in range(num_weeks):
    domestic_procurement = domestic_procurement_vars_enhanced[w].varValue
    import_procurement = import_procurement_vars_enhanced[w].varValue
    ending_stock = stock_vars_enhanced[w].varValue
    current_date = df_weekly['Date'][w]

    enhanced_optimization_results.append({
        'Date': current_date,
        'Domestic Procurement': domestic_procurement,
        'Import Procurement': import_procurement,
        'Ending Stock': ending_stock
    })

enhanced_optimization_results_df = pd.DataFrame(enhanced_optimization_results)

total_enhanced_cost = pulp.value(prob_enhanced.objective)
print(f"Total Enhanced Procurement and Holding Cost: {total_enhanced_cost:,.2f}")
print("
First 5 rows of enhanced_optimization_results_df:")
print(enhanced_optimization_results_df.head())

# Optional: Save results to CSV or visualize
# enhanced_optimization_results_df.to_csv('enhanced_optimization_results.csv', index=False)
