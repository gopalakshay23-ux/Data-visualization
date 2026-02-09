import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# -----------------------------
# Streamlit Page Config
# -----------------------------
st.set_page_config(layout="wide", page_title="BAJAJFINSV Dashboard")
sns.set_style("whitegrid")

st.title("📊 BAJAJFINSV Stock Dashboard")

# -----------------------------
# Load Dataset
# -----------------------------
df = pd.read_csv(r"C:\Users\vgane\Downloads\BAJAJFINSV.csv")  # Update path if needed

# -----------------------------
# Data Cleaning / Feature Engineering
# -----------------------------
df = df.dropna(subset=['Close','Turnover'])
df['Date'] = pd.to_datetime(df['Date'])
df['year'] = df['Date'].dt.year
df['month'] = df['Date'].dt.month
df['Month_Name'] = df['Date'].dt.strftime('%B')
df['Daily_Return_%'] = ((df['Close'] - df['Prev Close']) / df['Prev Close']) * 100
df['Profit (Close - Open)'] = df['Close'] - df['Open']
df['Volume Range'] = pd.qcut(df['Volume'], q=3, labels=['Low','Medium','High'])
df = df[df['Turnover'] > 0]

month_order = [
    "January","February","March","April","May","June",
    "July","August","September","October","November","December"
]

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("Filters")

# Year Dropdown (single select)
selected_year = st.sidebar.selectbox(
    "Select Year:",
    options=sorted(df['year'].unique()),  # all years in dataset
    index=0  # default to first year
)

# Month Dropdown (multi-select)
selected_months = st.sidebar.multiselect(
    "Select Month(s):",
    options=month_order,  # all months
    default=month_order  # by default, all months selected
)

# Apply filters
df_filtered = df[(df['year'] == selected_year) & (df['Month_Name'].isin(selected_months))]


# -----------------------------
# Tabs for Plots
# -----------------------------
tab1, tab2, tab3, tab4 = st.tabs(["Trend", "Distribution", "Correlations", "Monthly Analysis"])

# -----------------------------
# TAB 1: Trend Plots
# -----------------------------
with tab1:
    st.subheader("Monthly Turnover Trend")
    monthly_sales = df_filtered.set_index('Date').resample('M')['Turnover'].sum()
    fig1, ax1 = plt.subplots(figsize=(10,5))
    ax1.plot(monthly_sales.index, monthly_sales.values, marker='o', color='dodgerblue')
    ax1.set_title("Monthly Turnover Trend")
    ax1.set_xlabel("Date")
    ax1.set_ylabel("Turnover")
    st.pyplot(fig1)

    st.subheader("Daily Return % Over Time")
    fig4, ax4 = plt.subplots(figsize=(10,5))
    ax4.plot(df_filtered['Date'], df_filtered['Daily_Return_%'], color='orange')
    ax4.axhline(0, color='red', linestyle='--')
    ax4.set_title("Daily Return %")
    ax4.set_xlabel("Date")
    ax4.set_ylabel("Daily Return %")
    st.pyplot(fig4)

# -----------------------------
# TAB 2: Distribution Plots
# -----------------------------
with tab2:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Yearly Turnover Distribution (Log Scale)")
        fig2, ax2 = plt.subplots(figsize=(6,5))
        sns.boxplot(x='year', y=np.log10(df_filtered['Turnover']), data=df_filtered, ax=ax2, palette="Set2")
        ax2.set_title("Yearly Turnover (Log Scale)")
        st.pyplot(fig2)

        st.subheader("Prev Close vs Close Scatter")
        fig3, ax3 = plt.subplots(figsize=(6,5))
        sns.scatterplot(x='Prev Close', y='Close', data=df_filtered, alpha=0.5, ax=ax3, color='green')
        ax3.set_title("Prev Close vs Close")
        st.pyplot(fig3)

    with col2:
        st.subheader("Histogram of Open Prices")
        fig7, ax7 = plt.subplots(figsize=(6,5))
        ax7.hist(df_filtered['Open'], bins=50, color='purple', alpha=0.7)
        ax7.set_title("Open Price Distribution")
        st.pyplot(fig7)

        st.subheader("Pie Charts: Year & Volume Range")
        fig5, axes = plt.subplots(1,2, figsize=(10,5))
        year_counts = df_filtered['year'].value_counts().sort_index()
        axes[0].pie(year_counts, labels=year_counts.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette("pastel"))
        axes[0].set_title("Year Distribution")
        volume_counts = df_filtered['Volume Range'].value_counts()
        axes[1].pie(volume_counts, labels=volume_counts.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette("pastel"))
        axes[1].set_title("Volume Range")
        st.pyplot(fig5)

# -----------------------------
# TAB 3: Correlations
# -----------------------------
with tab3:
    st.subheader("Correlation Heatmap")
    fig6, ax6 = plt.subplots(figsize=(8,5))
    sns.heatmap(df_filtered[['Open','High','Last','Close']].corr(), annot=True, cmap='coolwarm', ax=ax6)
    ax6.set_title("Correlation Heatmap")
    st.pyplot(fig6)

# -----------------------------
# TAB 4: Monthly Analysis
# -----------------------------
with tab4:
    st.subheader("Total Turnover by Month")
    fig8, ax8 = plt.subplots(figsize=(10,5))
    sns.barplot(data=df_filtered, x='Month_Name', y='Turnover', estimator=sum, order=month_order, errorbar=None, palette="Set2", ax=ax8)
    ax8.set_title("Total Turnover by Month")
    ax8.set_xlabel("Month")
    ax8.set_ylabel("Total Turnover")
    plt.xticks(rotation=45)
    st.pyplot(fig8)
