
import streamlit as st
import altair as alt
from epoch_explorer.database.models.rag_history_model import RAGHistoryModel
from epoch_explorer.database.db.connection import get_connection

def show():
    st.title("📊 RAG Observability Dashboard")

    conn = get_connection()
    rag_history = RAGHistoryModel(conn)
    df = rag_history.get_metrix()

    # -------------------------
    # 🔘 Compact Mode Toggle
    # -------------------------
    compact_mode = st.toggle("🧩 Compact Mode", value=True)

    # Filters
    event_filter = st.multiselect("Event Type", df.event_type.unique())
    if event_filter:
        df = df[df.event_type.isin(event_filter)]

    # -------------------------
    # 📌 Prepare Chart Objects
    # -------------------------

    # 1️⃣ Event Distribution
    event_dist_chart = (
        alt.Chart(df)
        .mark_bar()
        .encode(x="event_type", y="count()", color="event_type")
        .properties(title="Event Type Distribution")
    )

    # 2️⃣ Accuracy Charts
    acc_df = df[df.event_type.isin(["QUERY", "SYNTHETIC_TEST"])].copy()
    acc_df["accuracy"] = acc_df["metrics"].apply(lambda m: m.get("accuracy") if m else None)
    acc_df = acc_df.dropna(subset=["accuracy"])

    accuracy_chart = (
        alt.Chart(acc_df)
        .mark_line(point=True)
        .encode(x="timestamp:T", y="accuracy:Q", color="event_type")
        .properties(title="Accuracy Over Time")
    )

    # 3️⃣ Latency
    acc_df["latency"] = acc_df["metrics"].apply(lambda m: m.get("latency") if m else None)
    latency_chart = (
        alt.Chart(acc_df)
        .mark_line(point=True)
        .encode(x="timestamp:T", y="latency:Q", color="event_type")
        .properties(title="Latency Over Time")
    )

    # 4️⃣ RL Agent Actions
    action_chart = (
        alt.Chart(df[df.action_taken.notnull()])
        .mark_bar()
        .encode(x="action_taken", y="count()", color="action_taken")
        .properties(title="RL Agent Actions")
    )

    # 5️⃣ Reward Signal
    reward_chart = (
        alt.Chart(df.dropna(subset=["reward_signal"]))
        .mark_line(point=True)
        .encode(x="timestamp:T", y="reward_signal:Q")
        .properties(title="Reward Signal Trend")
    )

    # -------------------------
    # 🧩 Render Charts
    # -------------------------
    charts = [
        event_dist_chart,
        accuracy_chart,
        latency_chart,
        action_chart,
        reward_chart,
    ]

    if compact_mode:
        st.markdown("### 🧩 Compact Mode Enabled")
        # Show charts in a 2-column grid
        for i in range(0, len(charts), 2):
            col1, col2 = st.columns(2)
            with col1:
                st.altair_chart(charts[i], use_container_width=True)
            if i + 1 < len(charts):
                with col2:
                    st.altair_chart(charts[i+1], use_container_width=True)
    else:
        st.markdown("### 📊 Standard View")
        for chart in charts:
            st.altair_chart(chart, use_container_width=True)
