import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

st.title("Loan Repayments Calculator")

st.write("### Input Data")

# Initialize session state
if 'loan_amt' not in st.session_state:
    st.session_state.loan_amt = 500000
if 'down_pay' not in st.session_state:
    st.session_state.down_pay = 100000
if 'int_rate' not in st.session_state:
    st.session_state.int_rate = 6.5
if 'loan_trm' not in st.session_state:
    st.session_state.loan_trm = 360

# Loan Amount
col1, col2 = st.columns(2)
loan_slider = col1.slider("Loan Amount (₹)", 20000, 10000000, st.session_state.loan_amt, step=5000)
loan_input = col1.number_input("Loan Amount (text input)", value=st.session_state.loan_amt, step=5000, min_value=20000, max_value=10000000)

# Update session state from whichever changed
if loan_slider != st.session_state.loan_amt:
    st.session_state.loan_amt = loan_slider
    st.rerun()
if loan_input != st.session_state.loan_amt:
    st.session_state.loan_amt = loan_input
    st.rerun()

Loan_amount = st.session_state.loan_amt

# Down Payment
down_slider = col2.slider("Down Payment (₹)", 0, Loan_amount, min(st.session_state.down_pay, Loan_amount), step=5000)
down_input = col2.number_input("Down Payment (text input)", value=min(st.session_state.down_pay, Loan_amount), step=1000, min_value=0, max_value=Loan_amount)

if down_slider != st.session_state.down_pay:
    st.session_state.down_pay = down_slider
    st.rerun()
if down_input != st.session_state.down_pay:
    st.session_state.down_pay = down_input
    st.rerun()

down_payment = st.session_state.down_pay

# Interest Rate
col3, col4 = st.columns(2)
rate_slider = col3.slider("Interest Rate (%)", 0.0, 15.0, st.session_state.int_rate, step=0.1)
rate_input = col3.number_input("Interest Rate (text input)", value=st.session_state.int_rate, step=0.01, min_value=0.0, max_value=15.0)

if rate_slider != st.session_state.int_rate:
    st.session_state.int_rate = rate_slider
    st.rerun()
if rate_input != st.session_state.int_rate:
    st.session_state.int_rate = rate_input
    st.rerun()

interest_rate = st.session_state.int_rate

# Loan Term
term_slider = col4.slider("Loan Term (months)", 1, 360, st.session_state.loan_trm, step=1)
term_input = col4.number_input("Loan Term (text input)", value=st.session_state.loan_trm, step=1, min_value=1, max_value=360)

if term_slider != st.session_state.loan_trm:
    st.session_state.loan_trm = term_slider
    st.rerun()
if term_input != st.session_state.loan_trm:
    st.session_state.loan_trm = term_input
    st.rerun()

loan_term = st.session_state.loan_trm

# Calculate loan amount
loan_amount = Loan_amount - down_payment

# Calculate monthly payment
if loan_amount > 0 and interest_rate > 0:
    monthly_rate = interest_rate / 100 / 12
    num_payments = loan_term
    monthly_payment = loan_amount * (monthly_rate * (1 + monthly_rate)**num_payments) / ((1 + monthly_rate)**num_payments - 1)
    total_payment = monthly_payment * num_payments
    total_interest = total_payment - loan_amount
    
    st.write("---")
    st.write("### Results")
    
    # Create results table with 2 rows
    results_data = {
        'Metric': ['Loan Amount', 'Monthly Payment', 'Total Payment', 'Total Interest'],
        'Value (₹)': [f'{loan_amount:,.2f}', f'{monthly_payment:,.2f}', f'{total_payment:,.2f}', f'{total_interest:,.2f}']
    }
    
    # Reshape to 2 rows x 4 columns
    row1_data = {
        'Home Value': [f'₹{Loan_amount:,.2f}'],
        'Down Payment': [f'₹{down_payment:,.2f}']
    }
    row2_data = {
        'Actual Loan Amount': [f'₹{loan_amount:,.2f}'],
        'Monthly Payment': [f'₹{monthly_payment:,.2f}']
    }
    row3_data = {
        'Total Payment': [f'₹{total_payment:,.2f}'],
        'Loan Term': [f'{loan_term} months ({loan_term // 12} years {loan_term % 12} months)']
    }
    
    df1 = pd.DataFrame(row1_data)
    df2 = pd.DataFrame(row2_data)
    df3 = pd.DataFrame(row3_data)
    
    st.dataframe(df1, use_container_width=True, hide_index=True)
    st.dataframe(df2, use_container_width=True, hide_index=True)
    st.dataframe(df3, use_container_width=True, hide_index=True)
    
    # Create pie chart for Principal vs Interest
    st.write("---")
    st.write("### Principal vs Total Interest")
    
    labels = ['Principal', 'Total Interest']
    values = [loan_amount, total_interest]
    colors = ['#4CAF50', '#FF9800']
    
    fig, ax = plt.subplots(figsize=(5, 5))
    wedges, texts, autotexts = ax.pie(values, labels=labels, colors=colors, autopct='%1.1f%%',
                                        startangle=90, textprops={'fontsize': 10})
    
    # Add value labels
    for i, (wedge, autotext) in enumerate(zip(wedges, autotexts)):
        percentage = values[i] / sum(values) * 100
        autotext.set_text(f'{percentage:.1f}%\n₹{values[i]:,.0f}')
        autotext.set_color('white')
        autotext.set_fontweight('bold')
        autotext.set_fontsize(9)
    
    ax.axis('equal')
    plt.title('Loan Breakdown: Principal vs Interest', fontsize=12, fontweight='bold')
    st.pyplot(fig)
    
    # Create amortization schedule - Payment breakdown over months
    st.write("---")
    st.markdown("<h3 style='text-align: center;'>Repayment Schedule</h3>", unsafe_allow_html=True)
    
    months = []
    principal_paid_monthly = []
    interest_paid_monthly = []
    current_principal = loan_amount
    
    for month in range(1, loan_term + 1):
        if current_principal > 0:
            interest_payment = current_principal * monthly_rate
            principal_payment = monthly_payment - interest_payment
            
            months.append(month)
            principal_paid_monthly.append(principal_payment)
            interest_paid_monthly.append(interest_payment)
            current_principal -= principal_payment
        else:
            break
    
    # Create stacked bar chart
    fig, ax = plt.subplots(figsize=(14, 5))
    
    bars1 = ax.bar(months, principal_paid_monthly, label='Principal', color='#4CAF50', edgecolor='#2E7D32', linewidth=0.5)
    bars2 = ax.bar(months, interest_paid_monthly, bottom=principal_paid_monthly, label='Interest', color='#FF9800', edgecolor='#F57C00', linewidth=0.5)
    
    # Add value labels only for every 12th month to avoid clutter
    for i, (month, principal, interest) in enumerate(zip(months, principal_paid_monthly, interest_paid_monthly)):
        if month % 12 == 0 or month == 1 or month == len(months):  # Show labels for every year + first and last month
            total = principal + interest
            if total > 0:
                ax.text(month, total, f'₹{total:,.0f}', ha='center', va='bottom', fontsize=7, fontweight='bold')
    
    ax.set_xlabel('Month', fontsize=11, fontweight='bold')
    ax.set_ylabel('Monthly Payment (₹)', fontsize=11, fontweight='bold')
    ax.set_title(f'Monthly Payment Breakdown (Principal + Interest) - Total Tenure: {loan_term} months', fontsize=12, fontweight='bold')
    ax.legend(loc='upper right')
    ax.grid(axis='y', alpha=0.3)
    
    # Format y-axis as currency
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'₹{x/100000:.1f}L' if x >= 100000 else f'₹{x:,.0f}'))
    
    # Set x-axis to show every 12 months (1 year) label
    ax.set_xticks(range(0, loan_term + 1, 12))
    ax.set_xticklabels([f'M{i}' if i > 0 else '0' for i in range(0, loan_term + 1, 12)])
    
    plt.tight_layout()
    st.pyplot(fig)
    
else:
    st.warning("Please enter valid loan parameters.")
