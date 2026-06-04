import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# -----------------------------------
# PAGE CONFIG
# -----------------------------------
st.set_page_config(
    page_title="Fitbit Analytics Dashboard",
    page_icon="🏃",
    layout="wide"
)

# -----------------------------------
# CUSTOM CSS
# -----------------------------------
st.markdown("""
<style>
.main {
    background-color: #f5f7fa;
}

.metric-card {
    padding:15px;
    border-radius:15px;
    background:white;
    box-shadow:0px 2px 10px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

# -----------------------------------
# TITLE
# -----------------------------------
st.title("🏃 Fitbit Fitness Analytics Dashboard")
st.markdown("### Deep Health & Activity Insights")

# -----------------------------------
# SIDEBAR
# -----------------------------------
st.sidebar.header("Upload Dataset")

activity_file = st.sidebar.file_uploader(
    "Upload Daily Activity CSV",
    type=["csv"]
)

if activity_file is not None:

    df = pd.read_csv(activity_file)

    st.success("Dataset Loaded Successfully!")

    # -----------------------------------
    # DATA PREVIEW
    # -----------------------------------

    st.subheader("Dataset Preview")

    st.dataframe(df.head())

    # -----------------------------------
    # KPIs
    # -----------------------------------

    total_steps = int(df["TotalSteps"].sum())
    avg_steps = int(df["TotalSteps"].mean())
    total_calories = int(df["Calories"].sum())
    avg_calories = int(df["Calories"].mean())

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "👣 Total Steps",
        f"{total_steps:,}"
    )

    col2.metric(
        "📊 Avg Steps",
        f"{avg_steps:,}"
    )

    col3.metric(
        "🔥 Calories Burned",
        f"{total_calories:,}"
    )

    col4.metric(
        "⚡ Avg Calories",
        f"{avg_calories:,}"
    )

    st.divider()

    # -----------------------------------
    # STEPS TREND
    # -----------------------------------

    st.subheader("📈 Daily Steps Trend")

    if "ActivityDate" in df.columns:
        df["ActivityDate"] = pd.to_datetime(
            df["ActivityDate"]
        )

        fig = px.line(
            df,
            x="ActivityDate",
            y="TotalSteps",
            markers=True,
            title="Daily Steps Trend"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # -----------------------------------
    # CALORIES VS STEPS
    # -----------------------------------

    st.subheader("🔥 Calories vs Steps")

    fig2 = px.scatter(
        df,
        x="TotalSteps",
        y="Calories",
        color="VeryActiveMinutes",
        size="Calories",
        hover_data=["SedentaryMinutes"],
        title="Calories Burned vs Total Steps"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

    # -----------------------------------
    # ACTIVITY BREAKDOWN
    # -----------------------------------

    st.subheader("🏃 Activity Distribution")

    activity_cols = [
        "VeryActiveMinutes",
        "FairlyActiveMinutes",
        "LightlyActiveMinutes",
        "SedentaryMinutes"
    ]

    available_cols = [
        c for c in activity_cols if c in df.columns
    ]

    activity_sum = df[available_cols].sum()

    pie_df = pd.DataFrame({
        "Activity": activity_sum.index,
        "Minutes": activity_sum.values
    })

    fig3 = px.pie(
        pie_df,
        names="Activity",
        values="Minutes",
        hole=0.5
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

    # -----------------------------------
    # CORRELATION HEATMAP
    # -----------------------------------

    st.subheader("🧠 Correlation Heatmap")

    numeric_df = df.select_dtypes(
        include=["int64", "float64"]
    )

    corr = numeric_df.corr()

    fig4 = px.imshow(
        corr,
        text_auto=True,
        aspect="auto",
        title="Feature Correlation Matrix"
    )

    st.plotly_chart(
        fig4,
        use_container_width=True
    )

    # -----------------------------------
    # TOP ACTIVE USERS
    # -----------------------------------

    st.subheader("🏆 Top Active Users")

    top_users = (
        df.groupby("Id")["TotalSteps"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig5 = px.bar(
        top_users,
        x="Id",
        y="TotalSteps",
        title="Top 10 Active Users"
    )

    st.plotly_chart(
        fig5,
        use_container_width=True
    )

    # -----------------------------------
    # AI INSIGHTS
    # -----------------------------------

    st.subheader("🤖 AI Health Insights")

    avg_steps = df["TotalSteps"].mean()

    if avg_steps > 10000:
        st.success(
            "Users maintain an excellent activity level."
        )
    elif avg_steps > 7000:
        st.warning(
            "Users are moderately active. Improvement possible."
        )
    else:
        st.error(
            "Low activity detected. More movement recommended."
        )

    st.info(
        f"""
        Average Daily Steps: {avg_steps:.0f}

        Recommended Target:
        8,000 - 10,000 steps/day

        Focus Areas:
        • Improve consistency
        • Reduce sedentary time
        • Increase active minutes
        """
    )

else:
    st.info("Upload a Fitbit CSV file to begin analysis.")
