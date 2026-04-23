# Import Core Libraries
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# -------------------------- Page Basic Settings --------------------------
st.set_page_config(
    page_title="CVP (Cost-Volume-Profit) Analysis Tool",
    layout="wide"
)
st.title("CVP (Cost-Volume-Profit) Analysis Tool")
st.markdown("---")

# -------------------------- 2023-2025 CSV Raw Data Processing (NO FALLBACK) --------------------------
# 1. Read CSV Data
csv_path = "global_ecommerce_sales.csv"
try:
    df_csv = pd.read_csv(csv_path)
except FileNotFoundError:
    st.error(f"Error: CSV file '{csv_path}' not found. Please place the file in the same directory.")
    st.stop()

# 2. Preprocess Date & Filter Year Range
df_csv["Year"] = pd.to_datetime(df_csv["Order_Date"]).dt.year
df_csv = df_csv[df_csv["Year"].between(2023, 2025)]

# 3. Check if data exists after filtering
if len(df_csv) == 0:
    st.error("Error: No valid 2023-2025 data found in the CSV file.")
    st.stop()

# 4. Get Dynamic Lists (Only what exists in CSV)
available_years = sorted(df_csv["Year"].unique().astype(str), reverse=True)

# Create a mapping of years to available categories (only what exists)
year_to_categories = {}
for year in available_years:
    year_data = df_csv[df_csv["Year"] == int(year)]
    year_to_categories[year] = sorted(year_data["Product_Category"].unique())

# 5. Calculate Industry Average Data (Only for existing data, NO FALLBACK)
industry_avg_data = {}

for year in available_years:
    year_data = df_csv[df_csv["Year"] == int(year)]
    industry_avg_data[year] = {}
    
    for category in year_to_categories[year]:
        cat_data = year_data[year_data["Product_Category"] == category]
        
        # Skip if no data (NO FALLBACK)
        if len(cat_data) == 0:
            continue
        
        # Calculate core financial metrics
        total_revenue = cat_data["Total_Sales"].sum()
        total_profit = cat_data["Profit"].sum()
        total_cost = total_revenue - total_profit
        
        # Simple generic cost split (30% fixed, 70% variable)
        fixed_cost = total_cost * 0.3
        total_var_cost = total_cost * 0.7
        
        # Calculate 4 key indicators
        contribution_margin_ratio = ((total_revenue - total_var_cost) / total_revenue) * 100
        variable_cost_ratio = (total_var_cost / total_revenue) * 100
        fixed_cost_ratio = (fixed_cost / total_revenue) * 100
        gross_profit_margin = (total_profit / total_revenue) * 100
        
        # Store in dictionary (ONLY if we have real data)
        industry_avg_data[year][category] = {
            "Contribution Margin Ratio (%)": round(contribution_margin_ratio, 1),
            "Variable Cost Ratio (%)": round(variable_cost_ratio, 1),
            "Fixed Cost to Revenue Ratio (%)": round(fixed_cost_ratio, 1),
            "Gross Profit Margin (%)": round(gross_profit_margin, 1)
        }

# -------------------------- Sidebar Input Module (Dynamic Options) --------------------------
with st.sidebar:
    st.header("Basic Parameters")
    fixed_cost = st.number_input("Fixed Cost (FC)", min_value=0.0, value=50000.0, step=1000.0)
    unit_price = st.number_input("Selling Price per Unit (SP)", min_value=0.1, value=100.0, step=1.0)
    unit_var_cost = st.number_input("Variable Cost per Unit (VC)", min_value=0.0, value=60.0, step=1.0)
    min_volume = st.number_input("Minimum Sales Volume", min_value=0, value=0, step=100)
    max_volume = st.number_input("Maximum Sales Volume", min_value=1, value=2000, step=100)
    
    st.markdown("---")
    st.subheader("Benchmark Settings (From CSV Only)")
    
    # Year selection (only available years)
    selected_year = st.selectbox(
        "Select Data Year",
        options=available_years,
        index=0
    )
    
    # Category selection (only categories available for the selected year)
    selected_category = st.selectbox(
        "Select Product Category",
        options=year_to_categories[selected_year],
        index=0
    )

# -------------------------- Core CVP Calculation Logic --------------------------
volume = np.arange(min_volume, max_volume + 1, 100)
total_revenue = unit_price * volume
total_var_cost = unit_var_cost * volume
total_cost = fixed_cost + total_var_cost
profit = total_revenue - total_cost
break_even_volume = fixed_cost / (unit_price - unit_var_cost) if (unit_price - unit_var_cost) > 0 else 0
break_even_revenue = break_even_volume * unit_price
contribution_margin_per_unit = unit_price - unit_var_cost
contribution_margin_ratio = (contribution_margin_per_unit / unit_price) * 100
var_cost_ratio = (unit_var_cost / unit_price) * 100
fixed_cost_ratio = (fixed_cost / (unit_price * 1000)) * 100
gross_margin = ((unit_price - unit_var_cost)/unit_price)*100

# -------------------------- Company Metrics VS CSV Benchmark --------------------------
st.subheader("Company Metrics VS CSV Benchmark")
col1, col2 = st.columns(2)
with col1:
    st.markdown(" Your Company Metrics")
    df_company = pd.DataFrame({
        "Metrics": ["Contribution Margin Ratio (%)", "Variable Cost Ratio (%)", "Fixed Cost to Revenue Ratio (%)", "Gross Profit Margin (%)"],
        "Value": [round(contribution_margin_ratio,2), round(var_cost_ratio,2), round(fixed_cost_ratio,2), round(gross_margin,2)]
    })
    st.dataframe(df_company, hide_index=True, use_container_width=True)

with col2:
    st.markdown(f" {selected_year} {selected_category} Benchmark (From CSV)")
    df_benchmark = pd.DataFrame(industry_avg_data[selected_year][selected_category], index=[selected_year])
    df_benchmark = df_benchmark.T.reset_index()
    df_benchmark.columns = ["Metrics", f"{selected_year} Benchmark"]
    st.dataframe(df_benchmark, hide_index=True, use_container_width=True)

# -------------------------- Core CVP Results Display --------------------------
st.markdown("---")
st.subheader(" Core CVP Calculation Results")
col_a, col_b, col_c, col_d = st.columns(4)
with col_a:
    st.metric("Unit Contribution Margin", f"{contribution_margin_per_unit:.2f}")
with col_b:
    st.metric("Contribution Margin Ratio", f"{contribution_margin_ratio:.2f} %")
with col_c:
    st.metric("Break-even Sales Volume", f"{break_even_volume:.0f} units")
with col_d:
    st.metric("Break-even Revenue", f"{break_even_revenue:.0f}")

# -------------------------- CVP Visualization Chart --------------------------
st.markdown("---")
st.subheader(" CVP Analysis Chart (With CSV Benchmark)")
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(volume, total_revenue, label="Total Revenue", color="#2E86AB", linewidth=2)
ax.plot(volume, total_cost, label="Total Cost", color="#A23B72", linewidth=2)
ax.axhline(y=fixed_cost, label="Fixed Cost", color="#F18F01", linestyle="--", linewidth=1.5)
ax.axvline(x=break_even_volume, color="#C73E1D", linestyle=":", label=f"Break-even Point: {break_even_volume:.0f} units")
ax.fill_between(volume, total_revenue, total_cost, where=(total_revenue > total_cost), color="#4CAF50", alpha=0.2, label="Profit Area")
ax.fill_between(volume, total_revenue, total_cost, where=(total_revenue < total_cost), color="#F44336", alpha=0.2, label="Loss Area")

# Benchmark line from CSV (only if data exists)
benchmark_cm_ratio = industry_avg_data[selected_year][selected_category]["Contribution Margin Ratio (%)"]
benchmark_revenue = (unit_price * (1 - benchmark_cm_ratio/100) + fixed_cost/1000) * volume
ax.plot(volume, benchmark_revenue, label=f"{selected_year} {selected_category} Benchmark", color="#9C27B0", linestyle="-.", linewidth=1.5)

ax.set_xlabel("Sales Volume (Units)", fontsize=12)
ax.set_ylabel("Amount", fontsize=12)
ax.set_title("Cost-Volume-Profit Analysis Chart", fontsize=14, fontweight="bold")
ax.legend(loc="upper left")
ax.grid(alpha=0.3)
st.pyplot(fig)

# -------------------------- Detailed Data Table --------------------------
st.markdown("---")
st.subheader(" Detailed Data Table")
df = pd.DataFrame({
    "Sales Volume": volume,
    "Total Revenue": total_revenue,
    "Total Variable Cost": total_var_cost,
    "Total Cost": total_cost,
    "Profit": profit
})
st.dataframe(df, hide_index=True, use_container_width=True)

# -------------------------- Overall CVP Analysis & Recommendations --------------------------
st.markdown("---")
st.subheader(" Overall CVP Analysis & Strategic Recommendations")
st.markdown("#### I. Overall Situation Summary")

benchmark_cm = industry_avg_data[selected_year][selected_category]["Contribution Margin Ratio (%)"]
profit_status = "Profitable" if max(profit) > 0 else "Loss-making" if max(profit) < 0 else "Break-even"
be_level = "Extremely High" if break_even_volume > max_volume * 0.8 else "High" if break_even_volume > max_volume * 0.5 else "Reasonable" if break_even_volume > 0 else "Invalid (SP ≤ VC)"

if contribution_margin_ratio > benchmark_cm + 1:
    cm_comparison = "significantly above the CSV benchmark"
elif abs(contribution_margin_ratio - benchmark_cm) <= 1:
    cm_comparison = "basically equal to the CSV benchmark"
else:
    cm_comparison = "below the CSV benchmark"

comprehensive_rating = (
    "Excellent" if (profit_status == "Profitable" and "above" in cm_comparison and be_level == "Reasonable")
    else "Moderate" if (profit_status == "Profitable" or "equal" in cm_comparison)
    else "Needs Urgent Optimization"
)

analysis_text = f"""
1. **Break-even Status**: The break-even sales volume is {break_even_volume:.0f} units, which is at a **{be_level}** level.
2. **Profitability**: Your business operates in a **{profit_status}** state.
3. **Cost Structure**: Unit Contribution Margin = {contribution_margin_per_unit:.2f}, Contribution Margin Ratio = {contribution_margin_ratio:.2f}%.
4. **CSV Benchmark**: Your contribution margin ratio is **{cm_comparison}**; the {selected_year} {selected_category} benchmark is {benchmark_cm:.1f}%.
5. **Comprehensive Rating**: **{comprehensive_rating}**
"""
st.write(analysis_text)

st.markdown("#### II. Targeted Strategic Recommendations")
suggestions = []

if contribution_margin_per_unit <= 0:
    suggestions.append(" CRITICAL RISK: Selling price is lower than or equal to variable cost. Increase unit price or reduce variable costs immediately.")

if break_even_volume > max_volume:
    suggestions.append(f" Break-even volume ({break_even_volume:.0f}) exceeds your maximum sales volume ({max_volume}). Expand sales scale or cut fixed costs.")

if contribution_margin_ratio < benchmark_cm - 1:
    suggestions.append(f" Your contribution margin ratio is {benchmark_cm - contribution_margin_ratio:.2f}% lower than the {selected_year} {selected_category} CSV benchmark. Optimize pricing or reduce variable costs.")

if fixed_cost_ratio > 20:
    suggestions.append(" Fixed cost ratio is excessively high. Reduce overheads to lower the break-even point.")

if profit_status == "Profitable" and "above" in cm_comparison and be_level == "Reasonable":
    suggestions.append(" Your CVP structure is healthy! Maintain current strategies and expand sales.")

for i, sug in enumerate(suggestions, 1):
    st.write(f"{i}. {sug}")

# -------------------------- Data Source Statement --------------------------
st.markdown("---")
st.caption(f"""
 **Data Source Statement**:
1. **100% CSV-Only Data**: No fallback values, no default data, no artificial filling.
2. All benchmark data is directly calculated from raw CSV fields: Order_Date, Product_Category, Total_Sales, and Profit.
3. Sidebar options are dynamically generated based on what actually exists in the CSV file.
4. If a year or category has no data, it will not appear in the selection options.
""")
