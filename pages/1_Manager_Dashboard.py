import streamlit as st
import sqlite3
import pandas as pd
from collections import Counter
import plotly.express as px

st.set_page_config(
    page_title="Manager Dashboard",
    layout="wide"
)

st.title("Manager Dashboard")

# =========================
# DATABASE
# =========================

conn = sqlite3.connect("fieldintel.db")

df = pd.read_sql_query(
    "SELECT * FROM visits",
    conn
)

if df.empty:
    st.warning("No data available.")
    st.stop()


# =========================
# KPI CARDS
# =========================

c1, c2, c3 = st.columns(3)

c1.metric(
    "Total Visits",
    len(df)
)

c2.metric(
    "Locations",
    df["location"].nunique()
)

c3.metric(
    "Programs",
    df["program_area"].nunique()
)

st.divider()

# =========================
# VISITS BY PROGRAM
# =========================

st.subheader("Visits by Program")

program_counts = (
    df["program_area"]
    .value_counts()
    .reset_index()
)

program_counts.columns = [
    "Program",
    "Count"
]

fig1 = px.bar(
    program_counts,
    x="Program",
    y="Count",
    title="Visits by Program Area"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

# =========================
# VISITS BY LOCATION
# =========================

st.subheader("Visits by Location")

location_counts = (
    df["location"]
    .value_counts()
    .reset_index()
)

location_counts.columns = [
    "Location",
    "Count"
]

fig2 = px.bar(
    location_counts,
    x="Location",
    y="Count",
    title="Visits by Location"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# =========================
# RECURRING ISSUES
# =========================

st.subheader("Top Recurring Issues")

all_tags = []

if "tags" in df.columns:

    for tags in df["tags"]:

        if pd.notna(tags) and str(tags).strip():

            tag_list = [
                tag.strip().title()
                for tag in str(tags).split(",")
            ]

            all_tags.extend(tag_list)

if len(all_tags) > 0:

    issue_counts = Counter(all_tags)

    issue_df = pd.DataFrame(
        issue_counts.items(),
        columns=[
            "Issue",
            "Count"
        ]
    )

    issue_df = issue_df.sort_values(
        by="Count",
        ascending=False
    )

    st.dataframe(
        issue_df,
        use_container_width=True
    )

    fig3 = px.bar(
        issue_df,
        x="Issue",
        y="Count",
        title="Recurring Issues Across All Visits"
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

else:

    st.warning(
        "No tags found. Create a few new visits and verify tags are being saved."
    )

st.divider()

# =========================
# GEOGRAPHY INSIGHTS
# =========================

st.subheader("Geography Insights")

selected_location = st.selectbox(
    "Select Location",
    sorted(
        df["location"]
        .dropna()
        .unique()
    )
)

location_df = df[
    df["location"] == selected_location
]

location_tags = []

if "tags" in location_df.columns:

    for tags in location_df["tags"]:

        if pd.notna(tags) and str(tags).strip():

            location_tags.extend(
                [
                    tag.strip()
                    for tag in str(tags).split(",")
                ]
            )

if len(location_tags) > 0:

    location_issues = Counter(
        location_tags
    )

    geo_df = pd.DataFrame(
        location_issues.items(),
        columns=[
            "Issue",
            "Count"
        ]
    )

    geo_df = geo_df.sort_values(
        by="Count",
        ascending=False
    )

    st.write(
        f"Top issues reported in {selected_location}"
    )

    st.dataframe(
        geo_df,
        use_container_width=True
    )

else:

    st.info(
        f"No issue tags available for {selected_location}"
    )

st.divider()

# =========================
# PROGRAM INSIGHTS
# =========================

st.subheader("Program Insights")

selected_program = st.selectbox(
    "Select Program",
    sorted(
        df["program_area"]
        .dropna()
        .unique()
    )
)

program_df = df[
    df["program_area"] == selected_program
]

program_tags = []

if "tags" in program_df.columns:

    for tags in program_df["tags"]:

        if pd.notna(tags) and str(tags).strip():

            program_tags.extend(
                [
                    tag.strip()
                    for tag in str(tags).split(",")
                ]
            )

if len(program_tags) > 0:

    program_issues = Counter(
        program_tags
    )

    prog_df = pd.DataFrame(
        program_issues.items(),
        columns=[
            "Issue",
            "Count"
        ]
    )

    prog_df = prog_df.sort_values(
        by="Count",
        ascending=False
    )

    st.write(
        f"Top issues for {selected_program}"
    )

    st.dataframe(
        prog_df,
        use_container_width=True
    )

else:

    st.info(
        f"No issue tags available for {selected_program}"
    )

st.divider()

# =========================
# SENTIMENT OVERVIEW
# =========================

if "sentiment" in df.columns:

    st.subheader("Community Sentiment Overview")

    sentiment_counts = (
        df["sentiment"]
        .value_counts()
        .reset_index()
    )

    sentiment_counts.columns = [
        "Sentiment",
        "Count"
    ]

    fig4 = px.pie(
        sentiment_counts,
        names="Sentiment",
        values="Count"
    )

    st.plotly_chart(
        fig4,
        use_container_width=True
    )

# =========================
# RECENT REPORTS
# =========================

st.subheader("Recent Reports")

show_cols = [
    "location",
    "visit_date",
    "program_area",
    "sentiment",
    "key_findings"
]

existing_cols = [
    c for c in show_cols
    if c in df.columns
]

st.dataframe(
    df[existing_cols],
    use_container_width=True
)