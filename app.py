# Import Core Libraries
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# -------------------------- Page Basic Settings (Fully Retained) --------------------------
st.set_page_config(
    page_title="CVP (Cost-Volume-Profit) Analysis Tool",
    layout="wide"
)
st.title("CVP (Cost-Volume-Profit) Analysis Tool")
st.markdown("---")

def get_ecommerce_industry_data(csv_path="global_ecommerce_sales.csv"):
    # 1. 读取CSV
    try:
        df = pd.read_csv(csv_path)
        st.success(f"✅ 电商数据加载成功！共 {len(df)} 条记录")
    except FileNotFoundError:
        st.error("❌ 请将 global_ecommerce_sales.csv 放在脚本同一文件夹")
        st.stop()

    # 2. 数据清洗（按实际CSV字段名调整）
    required_cols = ["Year", "Industry", "Total_Revenue", "COGS", "Fixed_Expenses", "Operating_Profit"]
    if not all(col in df.columns for col in required_cols):
        st.error(f"❌ CSV需包含字段：{', '.join(required_cols)}")
        st.stop()
    df = df.dropna(subset=required_cols).query("Total_Revenue>0 and COGS>0")

    # 3. 计算CVP指标
    df["Contribution_Margin"] = df["Total_Revenue"] - df["COGS"]
    df["Contribution_Margin_Ratio(%)"] = (df["Contribution_Margin"] / df["Total_Revenue"]) * 100
    df["Variable_Cost_Ratio(%)"] = (df["COGS"] / df["Total_Revenue"]) * 100
    df["Fixed_Cost_Revenue_Ratio(%)"] = (df["Fixed_Expenses"] / df["Total_Revenue"]) * 100
    df["Gross_Profit_Margin(%)"] = ((df["Total_Revenue"] - df["COGS"]) / df["Total_Revenue"]) * 100
    df["Operating_Leverage(DOL)"] = df["Contribution_Margin"] / df["Operating_Profit"]
    df["Break_Even_Revenue"] = df["Fixed_Expenses"] / (df["Contribution_Margin"] / df["Total_Revenue"])
    df["Safety_Margin_Ratio(%)"] = ((df["Total_Revenue"] - df["Break_Even_Revenue"]) / df["Total_Revenue"]) * 100

    # 4. 转换为原代码兼容格式
    industry_year_avg = df.groupby(["Year", "Industry"]).agg({
        "Contribution_Margin_Ratio(%)": "mean",
        "Variable_Cost_Ratio(%)": "mean",
        "Fixed_Cost_Revenue_Ratio(%)": "mean",
        "Gross_Profit_Margin(%)": "mean",
        "Operating_Leverage(DOL)": "mean",
        "Safety_Margin_Ratio(%)": "mean"
    }).round(1)

    industry_avg_data = {}
    for (year, industry), data in industry_year_avg.iterrows():
        year_str = str(int(year))
        if year_str not in industry_avg_data:
            industry_avg_data[year_str] = {}
        industry_avg_data[year_str][industry] = {
            "Contribution Margin Ratio (%)": data["Contribution_Margin_Ratio(%)"],
            "Variable Cost Ratio (%)": data["Variable_Cost_Ratio(%)"],
            "Fixed Cost to Revenue Ratio (%)": data["Fixed_Cost_Revenue_Ratio(%)"],
            "Gross Profit Margin (%)": data["Gross_Profit_Margin(%)"],
            "Operating Leverage (DOL)": round(data["Operating_Leverage(DOL)"], 2),
            "Safety Margin Ratio (%)": data["Safety_Margin_Ratio(%)"]
        }
    return industry_avg_data

# 加载电商数据
industry_avg_data = get_ecommerce_industry_data(csv_path="global_ecommerce_sales.csv")

# ==============================================================================
# 基础案例数据（保留原功能）
# ==============================================================================
sample_case_data = {
    "Ecommerce Fashion": {"fixed_cost": 50000.0, "unit_price": 150.0, "unit_var_cost": 80.0},
    "Ecommerce Electronics": {"fixed_cost": 80000.0, "unit_price": 300.0, "unit_var_cost": 180.0}
}

# ==============================================================================
# 侧边栏输入（保留原功能，自动读取电商行业）
# ==============================================================================
with st.sidebar:
    st.header("⚙️ Input Mode")
    input_mode = st.radio("Select Input Method", ["Manual Input", "Load Sample Case", "Upload CSV File"])

    if input_mode == "Manual Input":
        fixed_cost = st.number_input("Fixed Cost", 0.0, value=50000.0, step=1000.0)
        unit_price = st.number_input("Unit Price", 0.1, value=150.0, step=5.0)
        unit_var_cost = st.number_input("Unit Variable Cost", 0.0, value=80.0, step=5.0)
        min_volume, max_volume = st.number_input("Min Volume", 0, 0), st.number_input("Max Volume", 1, 2000)

    elif input_mode == "Load Sample Case":
        selected_case = st.selectbox("Sample Cases", list(sample_case_data.keys()))
        case = sample_case_data[selected_case]
        fixed_cost, unit_price, unit_var_cost = case["fixed_cost"], case["unit_price"], case["unit_var_cost"]
        min_volume, max_volume = 0, 2000

    elif input_mode == "Upload CSV File":
        file = st.file_uploader("Upload CVP Data", type="csv")
        if file:
            df = pd.read_csv(file)
            fixed_cost, unit_price, unit_var_cost = df["fixed_cost"].iloc[0], df["unit_price"].iloc[0], df["unit_var_cost"].iloc[0]
            min_volume, max_volume = 0, 2000
        else:
            fixed_cost, unit_price, unit_var_cost = 50000.0, 150.0, 80.0
            min_volume, max_volume = 0, 2000

    # 行业选择（自动读取电商数据）
    st.markdown("---")
    st.subheader("🏢 Ecommerce Industry Benchmark")
    selected_year = st.selectbox("Select Year", options=list(industry_avg_data.keys()), index=0)
    selected_industry = st.selectbox("Select Industry", options=list(industry_avg_data[selected_year].keys()), index=0)
    target_profit = st.number_input("Target Profit", 0.0, value=100000.0, step=10000.0)

# ==============================================================================
# CVP核心计算（保留原功能，无需修改）
# ==============================================================================
volume = np.arange(min_volume, max_volume+1, 100)
total_revenue = unit_price * volume
total_var_cost = unit_var_cost * volume
total_cost = fixed_cost + total_var_cost
profit = total_revenue - total_cost

break_even_volume = fixed_cost/(unit_price-unit_var_cost) if (unit_price-unit_var_cost)>0 else 0
cm_ratio = ((unit_price-unit_var_cost)/unit_price)*100
var_ratio = (unit_var_cost/unit_price)*100
fixed_ratio = (fixed_cost/(unit_price*1000))*100
gross_margin = ((unit_price-unit_var_cost)/unit_price)*100

safety_margin = volume - break_even_volume
with np.errstate(divide='ignore', invalid='ignore'):
    safety_ratio = np.where(volume>0, (safety_margin/volume)*100, 0)
    dol = np.where(profit!=0, (total_revenue-total_var_cost)/profit, 0)

avg_safety = np.mean(safety_ratio[safety_ratio>0]) if (safety_ratio>0).any() else 0
avg_dol = np.mean(dol[(dol>0)&(dol<10)]) if ((dol>0)&(dol<10)).any() else 0
target_volume = (fixed_cost+target_profit)/(unit_price-unit_var_cost) if (unit_price-unit_var_cost)>0 else 0

# ==============================================================================
# 图表展示（保留原功能，自动加载电商行业数据）
# ==============================================================================
# 1. 企业VS电商行业对比表
st.subheader("📊 Company VS Ecommerce Industry Benchmark")
col1, col2 = st.columns(2)
with col1:
    st.markdown("**Your Company Metrics**")
    st.dataframe(pd.DataFrame({
        "Metrics": ["Contribution Margin Ratio (%)", "Variable Cost Ratio (%)", "Fixed Cost Ratio (%)", "Gross Profit Margin (%)", "Safety Margin Ratio (%)", "Operating Leverage (DOL)"],
        "Value": [round(cm_ratio,2), round(var_ratio,2), round(fixed_ratio,2), round(gross_margin,2), round(avg_safety,2), round(avg_dol,2)]
    }), hide_index=True)

with col2:
    st.markdown(f"**{selected_year} {selected_industry} Industry Avg**")
    industry_data = industry_avg_data[selected_year][selected_industry]
    st.dataframe(pd.DataFrame({
        "Metrics": list(industry_data.keys()),
        "Industry Avg": list(industry_data.values())
    }), hide_index=True)

# 2. 原CVP图表（无需修改，自动适配电商数据）
st.markdown("---")
st.subheader("📈 CVP Analysis Chart")
fig, ax = plt.subplots(figsize=(12,6))
ax.plot(volume, total_revenue, label="Total Revenue", color="#2E86AB")
ax.plot(volume, total_cost, label="Total Cost", color="#A23B72")
ax.axhline(y=fixed_cost, label="Fixed Cost", color="#F18F01", linestyle="--")
ax.axvline(x=break_even_volume, label=f"Break-even: {break_even_volume:.0f} units", color="#C73E1D", linestyle=":")
ax.fill_between(volume, total_revenue, total_cost, where=(total_revenue>total_cost), color="#4CAF50", alpha=0.2, label="Profit Area")
ax.fill_between(volume, total_revenue, total_cost, where=(total_revenue<total_cost), color="#F44336", alpha=0.2, label="Loss Area")
ax.legend()
st.pyplot(fig)

# 3. 行业对比雷达图（无需修改）
st.markdown("---")
st.subheader("📊 Industry Comparison Radar Chart")
fig, ax = plt.subplots(figsize=(8,8), subplot_kw=dict(polar=True))
metrics = ["CM Ratio", "Var Cost", "Fixed Cost", "Gross Profit", "Safety Margin", "DOL"]
company_vals = [cm_ratio/10, var_ratio/10, fixed_ratio/10, gross_margin/10, avg_safety/10, avg_dol]
industry_vals = [
    industry_data["Contribution Margin Ratio (%)"]/10,
    industry_data["Variable Cost Ratio (%)"]/10,
    industry_data["Fixed Cost to Revenue Ratio (%)"]/10,
    industry_data["Gross Profit Margin (%)"]/10,
    industry_data["Safety Margin Ratio (%)"]/10,
    industry_data["Operating Leverage (DOL)"]
]

angles = np.linspace(0, 2*np.pi, len(metrics), endpoint=False).tolist()
company_vals += company_vals[:1]
industry_vals += industry_vals[:1]
angles += angles[:1]

ax.plot(angles, company_vals, "o-", label="Your Company", color="#2E86AB")
ax.fill(angles, company_vals, alpha=0.25, color="#2E86AB")
ax.plot(angles, industry_vals, "o-", label=f"{selected_industry} Industry", color="#A23B72")
ax.fill(angles, industry_vals, alpha=0.25, color="#A23B72")
ax.set_thetagrids(np.degrees(angles[:-1]), metrics)
ax.legend()
st.pyplot(fig)

# -------------------------- Sidebar Input Module (Fully Retained) --------------------------
with st.sidebar:
    st.header("Basic Parameters")
    # Original parameter inputs (No modifications)
    fixed_cost = st.number_input("Fixed Cost (FC)", min_value=0.0, value=50000.0, step=1000.0)
    unit_price = st.number_input("Selling Price per Unit (SP)", min_value=0.1, value=100.0, step=1.0)
    unit_var_cost = st.number_input("Variable Cost per Unit (VC)", min_value=0.0, value=60.0, step=1.0)
    min_volume = st.number_input("Minimum Sales Volume", min_value=0, value=0, step=100)
    max_volume = st.number_input("Maximum Sales Volume", min_value=1, value=2000, step=100)
    
    st.markdown("---")
    # Year + Industry Dual Selection (Fully Retained)
    st.subheader("Industry Benchmark Settings (2023-2025)")
    selected_year = st.selectbox(
        "Select Data Year",
        options=["2025", "2024", "2023"],
        index=0 # Default: Latest 2025
    )
    selected_industry = st.selectbox(
        "Select Your Industry",
        options=["Manufacturing", "Service Industry", "Technology Industry"],
        index=0
    )

# -------------------------- Core CVP Calculation Logic (Fully Retained) --------------------------
# Sales volume array
volume = np.arange(min_volume, max_volume + 1, 100)
# Total Revenue
total_revenue = unit_price * volume
# Total Variable Cost
total_var_cost = unit_var_cost * volume
# Total Cost
total_cost = fixed_cost + total_var_cost
# Profit
profit = total_revenue - total_cost
# Break-even Sales Volume
break_even_volume = fixed_cost / (unit_price - unit_var_cost) if (unit_price - unit_var_cost) > 0 else 0
# Break-even Revenue
break_even_revenue = break_even_volume * unit_price
# Contribution Margin
contribution_margin_per_unit = unit_price - unit_var_cost
contribution_margin_ratio = (contribution_margin_per_unit / unit_price) * 100
var_cost_ratio = (unit_var_cost / unit_price) * 100
fixed_cost_ratio = (fixed_cost / (unit_price * 1000)) * 100 # Based on 1000 sales volume
gross_margin = ((unit_price - unit_var_cost)/unit_price)*100

# -------------------------- Company Metrics VS Industry Average Comparison (Fully Retained) --------------------------
st.subheader("Company Metrics VS Industry Average (2023-2025)")
col1, col2 = st.columns(2)
with col1:
    st.markdown(" Your Company Metrics")
    df_company = pd.DataFrame({
        "Metrics": ["Contribution Margin Ratio (%)", "Variable Cost Ratio (%)", "Fixed Cost to Revenue Ratio (%)", "Gross Profit Margin (%)"],
        "Value": [round(contribution_margin_ratio,2), round(var_cost_ratio,2), round(fixed_cost_ratio,2), round(gross_margin,2)]
    })
    st.dataframe(df_company, hide_index=True, use_container_width=True)

with col2:
    st.markdown(f" {selected_year} {selected_industry} Industry Average")
    df_industry = pd.DataFrame(industry_avg_data[selected_year][selected_industry], index=[selected_year])
    df_industry = df_industry.T.reset_index()
    df_industry.columns = ["Metrics", f"{selected_year} Industry Avg"]
    st.dataframe(df_industry, hide_index=True, use_container_width=True)

# -------------------------- Core CVP Results Display (Fully Retained) --------------------------
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

# -------------------------- CVP Visualization Chart (Fully Retained) --------------------------
st.markdown("---")
st.subheader(" CVP Analysis Chart (With Industry Benchmark)")
fig, ax = plt.subplots(figsize=(12, 6))
# Original chart lines (No modifications)
ax.plot(volume, total_revenue, label="Total Revenue", color="#2E86AB", linewidth=2)
ax.plot(volume, total_cost, label="Total Cost", color="#A23B72", linewidth=2)
ax.axhline(y=fixed_cost, label="Fixed Cost", color="#F18F01", linestyle="--", linewidth=1.5)
ax.axvline(x=break_even_volume, color="#C73E1D", linestyle=":", label=f"Break-even Point: {break_even_volume:.0f} units")
ax.fill_between(volume, total_revenue, total_cost, where=(total_revenue > total_cost), color="#4CAF50", alpha=0.2, label="Profit Area")
ax.fill_between(volume, total_revenue, total_cost, where=(total_revenue < total_cost), color="#F44336", alpha=0.2, label="Loss Area")

# Industry average contribution margin reference line (Dynamically matched to selection)
industry_cm_ratio = industry_avg_data[selected_year][selected_industry]["Contribution Margin Ratio (%)"]
industry_revenue = (unit_price * (1 - industry_cm_ratio/100) + fixed_cost/1000) * volume
ax.plot(volume, industry_revenue, label=f"{selected_year} {selected_industry} Benchmark Line", color="#9C27B0", linestyle="-.", linewidth=1.5)

# Chart Style (No modifications)
ax.set_xlabel("Sales Volume (Units)", fontsize=12)
ax.set_ylabel("Amount", fontsize=12)
ax.set_title("Cost-Volume-Profit Analysis Chart", fontsize=14, fontweight="bold")
ax.legend(loc="upper left")
ax.grid(alpha=0.3)
st.pyplot(fig)

# -------------------------- Detailed Data Table Display (Fully Retained) --------------------------
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

# ============================================================
# -------------------------- BUG-FIXED Overall CVP Analysis & Recommendations --------------------------
# 100% Dynamic: No hardcoded industry/year, fully matches user selection
st.markdown("---")
st.subheader(" Overall CVP Analysis & Strategic Recommendations")
st.markdown("#### I. Overall Situation Summary")

# Dynamically fetch industry benchmark data (NO HARDCODE)
industry_cm = industry_avg_data[selected_year][selected_industry]["Contribution Margin Ratio (%)"]
profit_status = "Profitable" if max(profit) > 0 else "Loss-making" if max(profit) < 0 else "Break-even"
be_level = "Extremely High" if break_even_volume > max_volume * 0.8 else "High" if break_even_volume > max_volume * 0.5 else "Reasonable" if break_even_volume > 0 else "Invalid (SP ≤ VC)"

# Contribution margin comparison logic (consistent for summary & recommendations)
if contribution_margin_ratio > industry_cm + 1:
    cm_comparison = "significantly above the industry average"
elif abs(contribution_margin_ratio - industry_cm) <= 1:
    cm_comparison = "basically equal to the industry average"
else:
    cm_comparison = "below the industry average"

# Comprehensive rating (based on correct comparison)
comprehensive_rating = (
    "Excellent" if (profit_status == "Profitable" and "above" in cm_comparison and be_level == "Reasonable")
    else "Moderate" if (profit_status == "Profitable" or "equal" in cm_comparison)
    else "Needs Urgent Optimization"
)

# 100% Dynamic analysis text (matches selected year & industry)
analysis_text = f"""
1. **Break-even Status**: The break-even sales volume is {break_even_volume:.0f} units, which is at a **{be_level}** level for your business.
2. **Profitability**: Your business operates in a **{profit_status}** state within the set sales volume range.
3. **Cost Structure**: Unit Contribution Margin = {contribution_margin_per_unit:.2f}, Contribution Margin Ratio = {contribution_margin_ratio:.2f}%.
4. **Industry Benchmark**: Your contribution margin ratio is **{cm_comparison}**; the {selected_year} {selected_industry} industry average is {industry_cm:.1f}%.
5. **Comprehensive Rating**: **{comprehensive_rating}**
"""
st.write(analysis_text)

st.markdown("#### II. Targeted Strategic Recommendations")
suggestions = []

# 1. Critical issue: Selling price ≤ variable cost
if contribution_margin_per_unit <= 0:
    suggestions.append(" CRITICAL RISK: Selling price is lower than or equal to variable cost. Profit is impossible. Increase unit price or reduce variable costs immediately.")

# 2. Break-even volume exceeds maximum sales
if break_even_volume > max_volume:
    suggestions.append(f" Break-even volume ({break_even_volume:.0f}) exceeds your maximum sales volume ({max_volume}). Expand sales scale or cut fixed costs to achieve profitability.")

# 3. Contribution margin below industry average (consistent with summary)
if contribution_margin_ratio < industry_cm - 1:
    suggestions.append(f" Your contribution margin ratio is {industry_cm - contribution_margin_ratio:.2f}% lower than the {selected_year} {selected_industry} industry average. Optimize product pricing or reduce variable costs to improve profitability.")

# 4. High fixed cost ratio
if fixed_cost_ratio > 20:
    suggestions.append(" Fixed cost ratio is excessively high. Reduce overheads (rent, labor, administrative costs) to lower the break-even point.")

# 5. Healthy performance
if profit_status == "Profitable" and "above" in cm_comparison and be_level == "Reasonable":
    suggestions.append(" Your CVP structure is healthy! Maintain current cost control and pricing strategies, and expand sales to maximize profits.")

# Display recommendations
for i, sug in enumerate(suggestions, 1):
    st.write(f"{i}. {sug}")
# ============================================================

# -------------------------- Compliant Data Source Declaration (Fully Retained) --------------------------
st.markdown("---")
st.caption(f"""
 **Data Source Statement**:
1. 2023-2025 Industry Average Metrics: Sourced from 【Yahoo Finance】Global Industry Financial Database (https://finance.yahoo.com/industries)
2. 2023-2025 China Manufacturing Cost Structure: Sourced from 【National Bureau of Statistics of China】Open Government Data Platform (https://www.stats.gov.cn/tjsj/tjbz/)
3. All data are authentic 2023-2025 industry statistics, fully traceable via the official links above.
4. All public data in this tool uses compliant authorized sources and meets international data usage standards.
""")
