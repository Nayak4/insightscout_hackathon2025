import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time

from config import USER_PROFILES
from data.loader import load_documents
from summarizer.summarizer import summarize_documents, aggregate_summaries, answer_on_summary


def run_dashboard():
    st.set_page_config(page_title="InsightScout AI", layout="wide")
    st.markdown("""
        <style>
        .block-container {padding-top:2rem;}
        .dashboard-card {background:#f8fafc;border-radius:16px;padding:1.5rem;margin-bottom:1.5rem;box-shadow:0 2px 8px #0001;}
        .kpi-card {background:#eef2ff;border-radius:12px;padding:1rem;text-align:center;}
        .section-title {font-size:1.2em;font-weight:600;margin-bottom:0.5em;}
        .source-table th, .source-table td {padding:8px;border-bottom:1px solid #e2e8f0;}
        .source-table th {background:#f1f5f9;}
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
    header_col1, header_col2 = st.columns([4, 1])
    with header_col1:
        st.markdown("<h2 style='margin-bottom:0;'>InsightScout AI — Dashboard</h2>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # --- Filters Row ---
    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
    filters_col1, filters_col2, filters_col3 = st.columns([2, 2, 4])
    with filters_col1:
        user_profile = st.selectbox("User Profile", list(USER_PROFILES.keys()), help="Choose your perspective")
    with filters_col2:
        topic = st.text_input("Topic", value="Reaxys")
    with filters_col3:
        sources = st.multiselect(
            "Source",
            ["Confluence", "JIRA", "Non solus", "SharePoint", ".COM", "Other"],
            default=["Confluence", "JIRA", "Non solus", "SharePoint", ".COM", "Other"],
            help="Select sources"
        )
    st.markdown('</div>', unsafe_allow_html=True)

    # --- Analyze Documents Button ---
    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
    analyze_btn = st.button("Analyze Documents", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    if "history" not in st.session_state:
        st.session_state.history = []
    if "unified_summary" not in st.session_state:
        st.session_state.unified_summary = None
    if "documents" not in st.session_state:
        st.session_state.documents = None
    if "analysis_time" not in st.session_state:
        st.session_state.analysis_time = None

    # --- Summarize only when "Analyze Documents" is clicked ---
    if analyze_btn:
        start_time = time.time()
        with st.spinner("Loading and summarizing documents..."):
            documents = load_documents()
            documents = [doc for doc in documents if doc["source"] in sources]
            st.session_state.documents = documents
            document_summaries = summarize_documents(documents)
            unified_summary = aggregate_summaries(document_summaries)
            st.session_state.unified_summary = unified_summary
        analysis_time = time.time() - start_time
        st.session_state.analysis_time = analysis_time
        st.success(f"Analysis completed in {analysis_time:.2f} seconds.")

    # --- KPI Row ---
    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Key Metrics</div>', unsafe_allow_html=True)
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    if st.session_state.documents:
        df = pd.DataFrame(st.session_state.documents)
        total_docs = len(df)
        confluence_docs = (df['source'] == 'Confluence').sum()
        jira_docs = (df['source'] == 'JIRA').sum()
        avg_doc_length = int(df['content'].apply(len).mean())
        analysis_time = st.session_state.analysis_time if st.session_state.analysis_time else 0
    else:
        total_docs = confluence_docs = jira_docs = avg_doc_length = analysis_time = 0

    with kpi1:
        st.markdown(f"<div class='kpi-card'><div>Total Docs</div><div style='font-size:1.5em'>{total_docs}</div></div>",
                    unsafe_allow_html=True)
    with kpi2:
        st.markdown(
            f"<div class='kpi-card'><div>Confluence Docs</div><div style='font-size:1.5em'>{confluence_docs}</div></div>",
            unsafe_allow_html=True)
    with kpi3:
        st.markdown(f"<div class='kpi-card'><div>JIRA Docs</div><div style='font-size:1.5em'>{jira_docs}</div></div>",
                    unsafe_allow_html=True)
    with kpi4:
        st.markdown(
            f"<div class='kpi-card'><div>Avg. Doc Length</div><div style='font-size:1.5em'>{avg_doc_length}</div></div>",
            unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # --- Charts Row ---
    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Source Mix & Analysis Time</div>', unsafe_allow_html=True)
    chart_col1, chart_col2 = st.columns([2, 2])
    with chart_col1:
        # Pie chart for source mix
        if st.session_state.documents:
            source_counts = pd.Series([doc["source"] for doc in st.session_state.documents]).value_counts()
            fig = go.Figure(data=[go.Pie(labels=source_counts.index, values=source_counts.values, hole=0.4)])
            fig.update_traces(textinfo='label+percent', marker=dict(
                colors=['#6366f1', '#EF553B', '#38bdf8', '#fbbf24', '#10b981', '#f472b6', '#a3e635', '#f59e42']))
            fig.update_layout(title="Source Document Count", showlegend=True)
            st.plotly_chart(fig, use_container_width=True)
    with chart_col2:
        # Analysis time
        st.markdown(
            f"<div class='kpi-card'><div>Analysis Time</div><div style='font-size:1.5em'>{analysis_time:.2f} sec</div></div>",
            unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # --- Query Row ---
    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
    query_col1, query_col2 = st.columns([4, 1])
    with query_col1:
        query = st.text_area("Enter your question", height=80)
    with query_col2:
        st.write(" ")
        ask_btn = st.button("Ask Question", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    if ask_btn and st.session_state.unified_summary:
        with st.spinner("Processing your query..."):
            response = answer_on_summary(query, user_profile, st.session_state.unified_summary)
        st.session_state.history.append({"query": query, "response": response})

    # --- Query/Response Table ---
    if st.session_state.history:
        st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Query & Response History</div>', unsafe_allow_html=True)
        history_table = [{"Query": h["query"], "Response": h["response"]} for h in st.session_state.history]
        st.table(history_table)
        st.markdown('</div>', unsafe_allow_html=True)

    # --- Footer ---
    st.markdown("""
        <div class="footer" style="text-align:center;color:#888;margin-top:40px;font-size:13px;">
          Built for the Elsevier Hackathon 2025.
        </div>
    """, unsafe_allow_html=True)
