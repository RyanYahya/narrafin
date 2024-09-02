import streamlit as st
import pandas as pd

# Set page config
st.set_page_config(page_title="Narra Financial Insights", layout="wide", initial_sidebar_state="expanded")

# Custom CSS for styling
st.markdown("""
<style>
    .main {
        background-color: var(--background-color);
        font-family: 'Inter', sans-serif;
    }
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    h1, h2, h3 {
        color: var(--text-color);
        font-weight: 600;
    }
    .metric-card {
        background-color: var(--secondary-background-color);
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        padding: 1rem;
        text-align: center;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .metric-label {
        font-size: 0.875rem;
        color: var(--text-color);
        margin-bottom: 0.5rem;
    }
    .metric-value {
        font-size: 1.25rem;
        font-weight: 600;
        color: var(--text-color);
        margin: 0;
    }
    .metric-sar {
        font-size: 0.75rem;
        color: var(--secondary-text-color);
        margin-top: 0.25rem;
    }
    /* Light mode */
    [data-theme="light"] {
        --background-color: #ffffff;
        --secondary-background-color: #f7fafc;
        --text-color: #1a202c;
        --secondary-text-color: #718096;
    }
    /* Dark mode */
    [data-theme="dark"] {
        --background-color: #1a202c;
        --secondary-background-color: #2d3748;
        --text-color: #f7fafc;
        --secondary-text-color: #a0aec0;
    }
    /* Responsive design */
    @media (max-width: 768px) {
        .metric-card {
            margin-bottom: 1rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Helper functions
def convert_to_sar(amount):
    return amount * 3.75

def format_currency(amount, currency='USD'):
    return f"${amount:,.2f}" if currency == 'USD' else f"SAR {amount:,.2f}"

# Sidebar for inputs
with st.sidebar:
    st.image("Logo-01.png", width=100)  # Adjust the width as needed
    st.title("Financial Parameters")
    
    st.subheader("Timeline")
    months = st.slider("Projection Period (Months)", 1, 60, 12)
    
    st.subheader("Revenue")
    total_customers = st.number_input("Total Available Customers", min_value=0, value=1, step=1)
    target_percentage = st.slider("Target Market Share (%)", 0.0, 100.0, 100.0, 1.0)
    price_per_customer = st.number_input("Price per Customer (USD)", min_value=0.0, value=39.99, step=0.01)
    
    st.subheader("Expenses")
    num_employees = st.number_input("Number of Employees", min_value=0, value=1, step=1)
    avg_salary = st.number_input("Average Monthly Salary (USD)", min_value=0.0, value=1000.0, step=1.0)
    llm_cost_per_user = st.number_input("LLM Cost per User per Month (USD)", min_value=0.0, value=1.0, step=0.01)
    fixed_expenses = st.number_input("Fixed Monthly Expenses (USD)", min_value=0.0, value=100.0, step=1.0)
    
    st.subheader("Taxes")
    tax_rate = st.slider("Estimated Tax Rate (%)", 0.0, 50.0, 20.0, 0.5)
    apple_tax_rate = st.slider("App Store Fee (%)", 0.0, 30.0, 30.0, 0.5)

# Main dashboard
st.title("Narra Financial Insights")

# Calculations
market_size = int(total_customers * (target_percentage / 100))
projected_revenue = market_size * price_per_customer * months
total_employee_costs = num_employees * avg_salary * months
total_llm_cost = llm_cost_per_user * market_size * months
total_fixed_expenses = fixed_expenses * months
total_expenses = total_employee_costs + total_llm_cost + total_fixed_expenses
estimated_tax = max(0, (projected_revenue - total_expenses) * (tax_rate / 100))
apple_tax = projected_revenue * (apple_tax_rate / 100)
profit = projected_revenue - total_expenses - estimated_tax - apple_tax
break_even_point = total_expenses / (price_per_customer * market_size) if market_size > 0 else float('inf')
revenue_per_employee = projected_revenue / num_employees if num_employees > 0 else 0

# Key Metrics
st.subheader("Key Financial Metrics")
col1, col2, col3 = st.columns(3)
metrics = [
    ("Projected Revenue", projected_revenue),
    ("Total Expenses", total_expenses),
    ("Profit", profit)
]

for i, (label, value) in enumerate(metrics):
    with [col1, col2, col3][i]:
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-label">{label}</p>
            <p class="metric-value">{format_currency(value)}</p>
            <p class="metric-sar">SAR {format_currency(convert_to_sar(value), 'SAR')}</p>
        </div>
        """, unsafe_allow_html=True)
st.divider()
# Tax and Fee Metrics
st.subheader("Tax and Fee Metrics")
col1, col2 = st.columns(2)
tax_fee_metrics = [
    ("Estimated Tax", estimated_tax),
    ("App Store Fee", apple_tax)
]

for i, (label, value) in enumerate(tax_fee_metrics):
    with [col1, col2][i]:
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-label">{label}</p>
            <p class="metric-value">{format_currency(value)}</p>
            <p class="metric-sar">SAR {format_currency(convert_to_sar(value), 'SAR')}</p>
        </div>
        """, unsafe_allow_html=True)
st.divider()
# Expenses Breakdown
st.subheader("Expenses Breakdown")
col1, col2, col3 = st.columns(3)
expense_metrics = [
    ("Employee Costs", total_employee_costs),
    ("LLM Costs", total_llm_cost),
    ("Fixed Expenses", total_fixed_expenses)
]
st.divider()
for i, (label, value) in enumerate(expense_metrics):
    with [col1, col2, col3][i]:
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-label">{label}</p>
            <p class="metric-value">{format_currency(value)}</p>
            <p class="metric-sar">SAR {format_currency(convert_to_sar(value), 'SAR')}</p>
        </div>
        """, unsafe_allow_html=True)

# Export Report
st.subheader("Export Financial Report")

report = f"""
Narra Financial Analysis Report

Timeline: {months} months
Currency: USD

Revenue Projection: {format_currency(projected_revenue)}
Total Expenses: {format_currency(total_expenses)}
Profit: {format_currency(profit)}

Expenses Breakdown:
- Employee Costs: {format_currency(total_employee_costs)}
- LLM Costs: {format_currency(total_llm_cost)}
- Fixed Expenses: {format_currency(total_fixed_expenses)}

Break-Even Point: {break_even_point:.2f} months
Revenue Per Employee: {format_currency(revenue_per_employee)}

Estimated Tax: {format_currency(estimated_tax)}
App Store Fee: {format_currency(apple_tax)}
"""

st.download_button(
    label="Download Financial Report",
    data=report,
    file_name="narra_financial_report.txt",
    mime="text/plain"
)

# Prepare data for CSV export
metrics_data = {
    "Metric": ["Market Size", "Target Market Share (%)", "Projected Revenue", "Total Expenses", "Profit", "Estimated Tax", "App Store Fee", "Employee Costs", "LLM Costs", "Fixed Expenses"],
    "Value (USD)": [market_size, target_percentage, projected_revenue, total_expenses, profit, estimated_tax, apple_tax, total_employee_costs, total_llm_cost, total_fixed_expenses],
    "Value (SAR)": ["N/A", "N/A", convert_to_sar(projected_revenue), convert_to_sar(total_expenses), convert_to_sar(profit), convert_to_sar(estimated_tax), convert_to_sar(apple_tax), convert_to_sar(total_employee_costs), convert_to_sar(total_llm_cost), convert_to_sar(total_fixed_expenses)]
}

metrics_df = pd.DataFrame(metrics_data)

# Export CSV button
st.download_button(
    label="Download Metrics as CSV",
    data=metrics_df.to_csv(index=False),
    file_name="narra_financial_metrics.csv",
    mime="text/csv"
)