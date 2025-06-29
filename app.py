# app.py

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Gamification in Education", layout="wide")
st.title("🎮 Gamification in Education - Survey Dashboard")

# Load the Excel file
@st.cache_data
def load_data():
    df = pd.read_excel("SurveyResponses.xlsx")
    return df

df = load_data()

# Overview
st.subheader("📊 Survey Overview")
st.write("Total Responses:", df.shape[0])
st.dataframe(df.head())

# Sidebar filters
st.sidebar.header("🔍 Filter Responses")
selected_col = st.sidebar.selectbox("Select a column to filter", df.columns)

if df[selected_col].dtype == 'object':
    unique_vals = df[selected_col].dropna().unique()
    selected_vals = st.sidebar.multiselect(f"Choose values in '{selected_col}'", unique_vals)
    if selected_vals:
        df = df[df[selected_col].isin(selected_vals)]
else:
    min_val = float(df[selected_col].min())
    max_val = float(df[selected_col].max())
    range_vals = st.sidebar.slider(f"Select range for '{selected_col}'", min_val, max_val, (min_val, max_val))
    df = df[(df[selected_col] >= range_vals[0]) & (df[selected_col] <= range_vals[1])]

st.subheader("📌 Filtered Data")
st.write(f"Rows after filtering: {df.shape[0]}")
st.dataframe(df)

# Visualization
st.subheader("📈 Auto Visualizer")

col_to_plot = st.selectbox("Select a column to visualize", df.columns)

if df[col_to_plot].dtype == 'object':
    plot_data = df[col_to_plot].value_counts().head(10)
    st.bar_chart(plot_data)
else:
    st.line_chart(df[col_to_plot])

# Correlation (if numeric)
numeric_df = df.select_dtypes(include='number')
if numeric_df.shape[1] >= 2:
    st.subheader("📉 Correlation Heatmap")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(numeric_df.corr(), annot=True, cmap="coolwarm", ax=ax)
    st.pyplot(fig)

# Download button
csv = df.to_csv(index=False).encode('utf-8')
st.download_button("⬇️ Download Filtered Data", csv, "filtered_survey.csv", "text/csv")

st.markdown("---")
st.caption("Developed by Aiman Khan | GitHub: [itsaimankhan](https://github.com/itsaimankhan)")
