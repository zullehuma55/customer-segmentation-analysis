import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(layout="wide", initial_sidebar_state="expanded")

st.title("📊 Customer Segmentation Dashboard")

st.caption(
    "This dashboard presents the results of customer segmentation using the Mall Customers dataset."
)

df = pd.read_csv("data/Mall_Customers_Segmented.csv")

# 🔥 SIDEBAR

# Gender Filter
st.sidebar.header("Filter Options")

# Define options
gender_options = ["All"] + sorted(df["Gender"].unique())
    
#Create the multiselect widget
selected_gender = st.sidebar.selectbox("Select Gender", gender_options)

# Age Filter
age_range = st.sidebar.slider(
        "Select Age Range",
        int(df["Age"].min()),
        int(df["Age"].max()),
        (int(df["Age"].min()), int(df["Age"].max()))
    )

# Income Filter
income_range = st.sidebar.slider(
        "Select income Range",
        int(df["Annual Income (k$)"].min()),
        int(df["Annual Income (k$)"].max()),
        (int(df["Annual Income (k$)"].min()), int(df["Annual Income (k$)"].max()))
    )

# Sepnding Score Filter
spending_range = st.sidebar.slider(
        "Select spending Range",
        int(df["Spending Score (1-100)"].min()),
        int(df["Spending Score (1-100)"].max()),
        (int(df["Spending Score (1-100)"].min()), int(df["Spending Score (1-100)"].max()))    )
    
segment_options = ["All"] + sorted(df["Segment"].unique())
segment_chosen = st.sidebar.selectbox("Customer Segment",segment_options)


# 🔥 FILTER LOGIC
filtered_df = df[
     (df["Gender"].isin(["Male","Female"]) if selected_gender =="All" else df["Gender"]==selected_gender) &
        (df["Age"] >= age_range[0]) &
        (df["Age"] <= age_range[1]) &
        (df["Annual Income (k$)"] >= income_range[0]) &
        (df["Annual Income (k$)"] <= income_range[1])&
        (df["Spending Score (1-100)"] >= spending_range[0]) &
        (df["Spending Score (1-100)"] <= spending_range[1])&
        (df["Segment"] if segment_chosen == "All" else df["Segment"] == segment_chosen)
]

# 🔥 KPI SECTION

st.markdown("""
<style>
/* KPI Card Styling */
[data-testid="stMetric"] {
    background-color: #f8f9fa;
    border: 1px solid #e6e6e6;
    padding: 18px;
    border-radius: 12px;
    text-align: center;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}

[data-testid="stMetricLabel"] {
    font-size: 18px;
    font-weight: 600;
}

[data-testid="stMetricValue"] {
    font-size: 32px;
    font-weight: bold;
    color: #1f77b4;
}
</style>
""", unsafe_allow_html=True)

st.markdown("## 📌 Key Insights")
col1, col2, col3 = st.columns(3)

col1.metric("Total Customers", len(filtered_df))
    #col2.metric("Average Annual Income", round(filtered_df["Annual Income (k$)"].mean(), 1))
col2.metric("Average Annual Income", f"{filtered_df['Annual Income (k$)'].mean():.1f} k$")

col3.metric("Avg Spending Score", round(filtered_df["Spending Score (1-100)"].mean(), 1))

# 🔥 CHART SECTION (side by side)
st.markdown("## 📊 Visual Analysis")

col1, col2 = st.columns(2)

with col1:
        st.subheader("Age Distribution")
        #age_counts = filtered_df["Age"].value_counts().sort_index()
        #st.bar_chart(age_counts)

        bins = [0, 20, 30, 40, 50, 60, 100]
        labels = ["0-20", "20-30", "30-40", "40-50", "50-60", "60+"]

        filtered_df["Age Group"] = pd.cut(filtered_df["Age"], bins=bins, labels=labels)
        age_group_counts = filtered_df["Age Group"].value_counts().sort_index()
        st.bar_chart(age_group_counts)

with col2:
        segment_colors = {
    "High Value Customers": "#00CC96",      # Bright Green
    "Mid Value Customers": "#636EFA",       # Bright Blue
    "Potential Customers": "#FFA15A",       # Orange
    "Impulse Buyers": "#EF553B",            # Red
    "Low Value Customers": "#AB63FA"        # Purple
}



with col2:
    st.subheader("Income vs Spending")

    scatter_data = filtered_df[
        ["Annual Income (k$)", "Spending Score (1-100)"]
    ]

    st.scatter_chart(
        filtered_df,
        x="Annual Income (k$)",
        y="Spending Score (1-100)",
        color="Segment",
        legend=None,
        use_container_width=True
    )
    
# 🔥 DATA SECTION
st.markdown("## 📄 Data Preview")
st.dataframe(filtered_df)

# 🔥 DOWNLOAD BUTTON
csv = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button(
        "Download Results",
        data=csv,
        file_name="customer_segmentation_results.csv",
        mime="text/csv"
    )
