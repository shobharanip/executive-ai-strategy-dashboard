"""
Executive AI Strategy Dashboard - Main Application
CEO-Track Portfolio Project
"""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime
import openai
from dotenv import load_dotenv
import os

load_dotenv()

st.set_page_config(
    page_title="Executive AI Strategy Dashboard",
    page_icon="🎯",
    layout="wide"
)


def generate_sample_data():
    np.random.seed(42)
    dates = pd.date_range(end=datetime.now(), periods=90, freq="D")
    revenue_data = pd.DataFrame({
        "date": dates,
        "mrr": np.cumsum(np.random.normal(50000, 10000, 90)) + 3500000,
    })
    churn_data = pd.DataFrame({
        "account": ["Account_" + str(i).zfill(3) for i in range(100)],
        "churn_score": np.random.beta(2, 5, 100),
        "arr": np.random.lognormal(10, 1, 100),
        "health_score": np.random.randint(0, 100, 100),
        "days_since_login": np.random.randint(0, 90, 100),
    })
    return revenue_data, churn_data


def get_ai_briefing(revenue_data, api_key):
    """Generate AI-powered executive briefing via GPT-4."""
    latest_mrr = revenue_data["mrr"].iloc[-1]
    prev_mrr = revenue_data["mrr"].iloc[-8]
    mrr_growth = ((latest_mrr - prev_mrr) / prev_mrr) * 100
    if api_key and api_key != "demo":
        try:
            client = openai.OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are an AI executive assistant."},
                    {"role": "user", "content": "Generate a 3-sentence board brief with this data: " +
                     "MRR growth: " + str(round(mrr_growth, 1)) + "%, 23 accounts at churn risk, DAU/MAU: 0.42"}
                ],
                max_tokens=200
            )
            return response.choices[0].message.content
        except Exception as e:
            pass
    return ("MRR grew " + str(round(mrr_growth, 1)) + "% WoW to $" + str(round(latest_mrr/1e6, 2)) + "M, "
            "driven by enterprise expansion, but 23 SMB accounts show declining usage with at-risk ARR of $1.2M. "
            "Recommend QBR blitz for health score < 40 accounts before end of quarter.")


def main():
    st.title("🎯 Executive AI Strategy Dashboard")
    st.caption("Board Intelligence Platform | " + datetime.now().strftime("%B %d, %Y %H:%M"))
    
    # Sidebar config
    with st.sidebar:
        st.header("⚙️ Configuration")
        api_key = st.text_input("OpenAI API Key", type="password", value=os.getenv("OPENAI_API_KEY", ""))
        st.divider()
        st.markdown("### 📊 Dashboard Info")
        st.markdown("**Version:** 1.0.0")
        st.markdown("**Data Refresh:** Real-time")
        st.markdown("**AI Model:** GPT-4o")
    
    revenue_data, churn_data = generate_sample_data()
    
    # AI Briefing
    with st.expander("🤖 AI Executive Morning Brief", expanded=True):
        with st.spinner("Generating AI briefing..."):
            briefing = get_ai_briefing(revenue_data, api_key)
        st.info(briefing)
    
    st.divider()
    
    # Top KPIs
    st.subheader("📊 Board-Level KPIs")
    c1, c2, c3, c4, c5 = st.columns(5)
    current_mrr = revenue_data["mrr"].iloc[-1]
    prev_mrr = revenue_data["mrr"].iloc[-8]
    mrr_delta = ((current_mrr - prev_mrr) / prev_mrr) * 100
    c1.metric("ARR", "$" + str(round(current_mrr*12/1e6, 1)) + "M", str(round(mrr_delta, 1)) + "% WoW")
    c2.metric("NRR", "118%", "+3pp QoQ")
    c3.metric("Gross Churn", "1.8%/mo", "-0.2pp")
    c4.metric("Headcount", "342", "+12 QoQ")
    c5.metric("eNPS", "42", "+5 pts")
    
    st.divider()
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "💰 Revenue Intelligence",
        "🔄 Churn & Retention",
        "🛠️ Product Analytics",
        "👥 People & Org"
    ])
    
    with tab1:
        st.subheader("Revenue Trend")
        fig = px.area(revenue_data, x="date", y="mrr",
                      title="Monthly Recurring Revenue (90-day trend)",
                      template="plotly_dark")
        fig.update_traces(line_color="#00d4aa", fillcolor="rgba(0,212,170,0.2)")
        st.plotly_chart(fig, use_container_width=True)
        
        c1, c2 = st.columns(2)
        with c1:
            waterfall = go.Figure(go.Waterfall(
                orientation="v",
                measure=["absolute", "relative", "relative", "relative", "total"],
                x=["Opening ARR", "New Biz", "Expansion", "Churn", "Closing ARR"],
                y=[45000000, 2200000, 1800000, -850000, 0],
                decreasing={"marker": {"color": "#ff6b6b"}},
                increasing={"marker": {"color": "#00d4aa"}},
                totals={"marker": {"color": "#4ecdc4"}}
            ))
            waterfall.update_layout(title="ARR Waterfall Q2 2026", template="plotly_dark", height=350)
            st.plotly_chart(waterfall, use_container_width=True)
        with c2:
            seg_df = pd.DataFrame({
                "Segment": ["Enterprise", "Mid-Market", "SMB"],
                "ARR ($M)": [28, 12, 8],
                "YoY Growth %": [18, 12, -3]
            })
            fig_seg = px.bar(seg_df, x="Segment", y="ARR ($M)",
                             color="YoY Growth %", color_continuous_scale="RdYlGn",
                             title="ARR by Segment",
                             template="plotly_dark", height=350)
            st.plotly_chart(fig_seg, use_container_width=True)
    
    with tab2:
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Monthly Churn", "1.8%", "-0.2pp", delta_color="inverse")
        c2.metric("At-Risk Accounts", "23", "+5 WoW", delta_color="inverse")
        c3.metric("At-Risk ARR", "$1.2M", "+$180K", delta_color="inverse")
        c4.metric("Avg Health Score", "72/100", "+3 pts")
        fig_churn = px.scatter(
            churn_data, x="days_since_login", y="churn_score",
            size="arr", color="health_score",
            color_continuous_scale="RdYlGn",
            title="Account Churn Risk Map (bubble = ARR value)",
            template="plotly_dark", height=450
        )
        fig_churn.add_hline(y=0.6, line_dash="dash", line_color="red",
                             annotation_text="High Risk Threshold")
        st.plotly_chart(fig_churn, use_container_width=True)
        at_risk = churn_data[churn_data["churn_score"] > 0.6].sort_values("arr", ascending=False)
        st.subheader("🚨 High-Risk Accounts Requiring Immediate Action")
        st.dataframe(at_risk.head(10), use_container_width=True)
    
    with tab3:
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("DAU", "8,432", "+234")
        c2.metric("MAU", "24,891", "+1,203")
        c3.metric("Stickiness (DAU/MAU)", "33.9%", "+1.2pp")
        c4.metric("Time to Value", "4.2 days", "-0.8 days")
        features = ["Dashboard", "Reports", "API", "Integrations", "AI", "Export"]
        segments = ["Enterprise", "Mid-Market", "SMB", "Trial"]
        adoption = np.random.randint(20, 100, (4, 6))
        import altair as alt
        fig_heat = px.imshow(adoption, x=features, y=segments,
                             title="Feature Adoption Heatmap by Segment (%)",
                             color_continuous_scale="RdYlGn",
                             template="plotly_dark", height=350)
        st.plotly_chart(fig_heat, use_container_width=True)
    
    with tab4:
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Headcount", "342", "+12 QoQ")
        c2.metric("Attrition Rate", "11.2%", "+1.8pp", delta_color="inverse")
        c3.metric("eNPS", "42", "+5 QoQ")
        c4.metric("Revenue/Employee", "$132K", "+8%")
        dept_df = pd.DataFrame({
            "Department": ["Engineering", "Sales", "Customer Success", "Marketing", "Product", "G&A"],
            "Attrition Risk": [35, 72, 58, 42, 28, 22],
            "Headcount": [98, 65, 72, 38, 31, 38]
        })
        fig_people = px.bar(dept_df, x="Department", y="Attrition Risk",
                             color="Attrition Risk", color_continuous_scale="RdYlGn_r",
                             title="Attrition Risk Score by Department",
                             text="Headcount", template="plotly_dark", height=400)
        fig_people.add_hline(y=60, line_dash="dash", line_color="orange")
        st.plotly_chart(fig_people, use_container_width=True)


if __name__ == "__main__":
    main()
