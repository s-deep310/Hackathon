import streamlit as st
import altair as alt
import pandas as pd
from epoch_explorer.database.models.document_metadata_model import DocumentMetadataModel
from epoch_explorer.database.db.connection import get_connection
import json

def show():
    st.title("📄 Document Metadata Dashboard")

    # -------------------------
    # 🔘 Compact Mode Toggle
    # -------------------------
    compact_mode = st.toggle("🧩 Compact Mode", value=True)

    # Load data
    conn = get_connection()
    doc_model = DocumentMetadataModel(conn)
    df = doc_model.get_all_documents()

    # --- Filters ---
    st.subheader("Filters")
    rbac_filter = st.multiselect(
        "RBAC Namespace",
        df.rbac_namespace.unique(),
        df.rbac_namespace.unique()
    )
    chunk_filter = st.multiselect(
        "Chunk Strategy",
        df.chunk_strategy.unique(),
        df.chunk_strategy.unique()
    )

    if rbac_filter:
        df = df[df.rbac_namespace.isin(rbac_filter)]
    if chunk_filter:
        df = df[df.chunk_strategy.isin(chunk_filter)]

    # -------------------------
    # 📌 Prepare Chart Objects
    # -------------------------

    # 1️⃣ Document Count by RBAC Namespace
    chart_rbac = (
        alt.Chart(df)
        .mark_bar()
        .encode(
            x="rbac_namespace:N",
            y="count():Q",
            color="rbac_namespace:N",
            tooltip=["rbac_namespace", "count()"]
        )
        .properties(title="Document Count by RBAC Namespace")
    )

    # 2️⃣ Chunking Strategy Distribution
    chart_chunk = (
        alt.Chart(df)
        .mark_bar()
        .encode(
            x="chunk_strategy:N",
            y="count():Q",
            color="chunk_strategy:N",
            tooltip=["chunk_strategy", "count()"]
        )
        .properties(title="Chunking Strategy Distribution")
    )

    # 3️⃣ Chunk Size vs Overlap
    chunk_chart = (
        alt.Chart(df)
        .mark_circle(size=100)
        .encode(
            x="chunk_size_char:Q",
            y="overlap_char:Q",
            color="chunk_strategy:N",
            tooltip=["title", "chunk_size_char", "overlap_char", "chunk_strategy"]
        )
        .properties(title="Chunk Size vs Overlap")
    )

    # Put charts in list for compact mode
    charts = [chart_rbac, chart_chunk, chunk_chart]

    # -------------------------
    # 🧩 Render Charts
    # -------------------------
    if compact_mode:
        st.markdown("### 🧩 Compact Mode Enabled")

        # Display charts in 2-column grid
        for i in range(0, len(charts), 2):
            col1, col2 = st.columns(2)
            with col1:
                st.altair_chart(charts[i], use_container_width=True)
            if i + 1 < len(charts):
                with col2:
                    st.altair_chart(charts[i + 1], use_container_width=True)

    else:
        st.markdown("### 📊 Standard View")
        for chart in charts:
            st.altair_chart(chart, use_container_width=True)

    # -------------------------
    # 🕒 Recently Ingested Documents
    # -------------------------
    st.subheader("🕒 Recently Ingested Documents")
    recent_df = df.sort_values("last_ingested", ascending=False).head(10)
    st.table(
        recent_df[["doc_id", "title", "author", "source", "last_ingested"]]
    )

    # -------------------------
    # 📝 Metadata JSON Viewer
    # -------------------------
    st.subheader("📝 Metadata JSON Insights")

    if len(df) > 0:
        selected_doc = st.selectbox("Select Document", df.title)
        metadata_json_str = df[df.title == selected_doc]["metadata_json"].values[0]

        if metadata_json_str:
            try:
                metadata = json.loads(metadata_json_str)
                st.json(metadata)
            except Exception as e:
                st.warning(f"Invalid JSON: {e}")
        else:
            st.info("No metadata available for this document.")
    else:
        st.info("No records available.")
