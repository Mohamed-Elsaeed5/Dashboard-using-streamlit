import pandas as pd
import streamlit as st
import plotly.express as px

# Load the data
df = pd.read_excel('2009.xlsx')

# Set page config
st.set_page_config(page_title="Sales Dashboard", layout="wide")
st.title("📊 Sales Data Dashboard (2009.xlsx)")

# --- Sidebar ---
st.sidebar.title("📂 Dashboard Filters")
st.sidebar.image('filter.png')
st.sidebar.title("📂 This will filter bar chart")

# Filter for bar chart (categorical)
filter_column = st.sidebar.selectbox(
    "Group Profit By (Bar Chart):",
    options=['Product Category', 'Product Sub-Category', 'Region']
)
st.sidebar.title("📂 This will filter scatter plot")
   
# Filter for scatter plot (numerical only)
numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
scatter_xaxis = st.sidebar.selectbox(
    "X-Axis for Scatter Plot (Numeric):",
    options=numeric_cols
)

# --- Display Dataset Preview ---
st.write("Dataset Shape:", df.shape)
st.dataframe(df.head())

# --- Pie Chart: Orders by Ship Mode ---
st.subheader("Pie Chart: Order Distribution by Ship Mode")
ship_counts = df['Ship Mode'].value_counts().reset_index()
ship_counts.columns = ['Ship Mode', 'Count']
fig_pie = px.pie(ship_counts, names='Ship Mode', values='Count', title="Orders by Ship Mode")
st.plotly_chart(fig_pie, use_container_width=True)

# --- Bar Chart: Total Profit by selected filter ---
st.subheader(f"Bar Chart: Total Profit by {filter_column}")
if filter_column in df.columns:
    grouped_profit = df.groupby(filter_column)['Profit'].sum().reset_index().sort_values(by='Profit', ascending=False)
    fig_bar = px.bar(grouped_profit, x=filter_column, y='Profit', text='Profit',
                     title=f"Total Profit by {filter_column}")
    fig_bar.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig_bar.update_layout(yaxis=dict(visible=False))
    st.plotly_chart(fig_bar, use_container_width=True)
else:
    st.warning(f"{filter_column} not found in data.")

# --- Scatter Plot: [Selected Numeric Column] vs Profit ---
st.subheader(f"Scatter Plot: {scatter_xaxis} vs Profit")
fig_scatter = px.scatter(
    df,
    x=scatter_xaxis,
    y='Profit',
    color='Product Category',
    title=f"{scatter_xaxis} vs Profit"
)
fig_scatter.update_layout(
    xaxis_title=scatter_xaxis,
    yaxis_title="Profit"
)
st.plotly_chart(fig_scatter, use_container_width=True)
