# 🎯 Executive AI Strategy Dashboard

> **CEO-Track Portfolio Project** | Board-Level Intelligence Platform

[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32-red)](https://streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🏢 Business Problem

C-suite leaders waste 40% of their time aggregating data from siloed systems. This dashboard eliminates that problem by unifying revenue, churn, product engagement, and people metrics into a single real-time board-level view powered by AI.

## 🎯 Decision This Enables

Leadership can answer "Should we reallocate Q3 budget from acquisition to retention?" in under 60 seconds — not 3 days.

## 📈 Measurable Impact

- Time to executive insight: 3-5 days → under 60 seconds
- Data sources unified: 4 manual → 8 automated
- Decision cycle time: Weekly → Real-time
- CFO/CEO prep time saved: ~7 hrs/week

## 🏗️ Architecture

Data Layer → AI/ML Layer → Presentation Layer
- Stripe, Salesforce, Mixpanel, Workday HR, PostgreSQL
- GPT-4 Insights, Anomaly Detection, Forecast Models
- Streamlit UI, Plotly Charts, PDF Export, Slack Alerts

## 🚀 Features

### Revenue Intelligence
- MRR/ARR tracking with AI-generated trend narratives
- Cohort revenue analysis with expansion/contraction breakdown
- Forecasting with confidence intervals (Prophet + GPT-4)
- NRR, GRR, and net new ARR waterfall charts

### Churn & Retention Analytics
- Real-time churn probability scores per account
- Early warning system: accounts at risk flagged 30-60 days early
- Retention driver analysis with SHAP explainability

### Product Usage Metrics
- DAU/MAU with stickiness ratio
- Feature adoption heatmaps
- Power user segmentation

### People & Org Health
- Headcount growth vs. revenue efficiency ratio
- Attrition risk heatmap by department
- Hiring velocity vs. plan

### AI Executive Briefing
- GPT-4 generates a 3-sentence board summary every morning
- Anomaly detection with context
- Prescriptive recommendations with confidence levels

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| Frontend | Streamlit 1.32 |
| Charts | Plotly Express + Altair |
| AI Layer | OpenAI GPT-4o, LangChain |
| ML Models | scikit-learn, Prophet, XGBoost |
| Database | PostgreSQL + Redis |
| Pipeline | Apache Airflow |
| Deployment | Docker + AWS ECS |

## 📁 Project Structure

```
executive-ai-strategy-dashboard/
├── app/
│   ├── main.py
│   ├── pages/
│   │   ├── 01_revenue.py
│   │   ├── 02_churn.py
│   │   ├── 03_product.py
│   │   ├── 04_people.py
│   │   └── 05_ai_briefing.py
│   ├── components/
│   │   ├── kpi_cards.py
│   │   ├── charts.py
│   │   └── ai_narratives.py
│   └── utils/
│       ├── data_connectors.py
│       ├── ml_models.py
│       └── cache.py
├── models/
│   ├── churn_predictor.py
│   ├── revenue_forecast.py
│   └── anomaly_detector.py
├── pipelines/
│   └── dags/
│       ├── revenue_pipeline.py
│       ├── churn_pipeline.py
│       └── people_pipeline.py
├── tests/
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
├── requirements.txt
└── .env.example
```

## ⚡ Quick Start

```bash
git clone https://github.com/shobharanip/executive-ai-strategy-dashboard
cd executive-ai-strategy-dashboard
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
streamlit run app/main.py
```

## 🔧 Environment Variables

```env
OPENAI_API_KEY=sk-...
STRIPE_API_KEY=sk_live_...
SALESFORCE_URL=https://yourorg.salesforce.com
POSTGRES_URL=postgresql://user:pass@localhost:5432/exec_db
REDIS_URL=redis://localhost:6379
```

## 🤖 AI Briefing Sample

> **Morning Brief — June 14, 2026**
> MRR grew 3.2% WoW to $4.2M, driven by 12 new enterprise logos, but churn risk is elevated in the SMB segment with 23 accounts showing declining usage. Recommend scheduling a QBR blitz for accounts with health score < 40.

## 🧪 Testing

```bash
pytest tests/ -v --cov=app --cov-report=html
```

## 📄 License

MIT License

## 👤 Author

**Shobha Rani P** | AI Strategy & Executive Analytics
[GitHub](https://github.com/shobharanip) | [LinkedIn](https://linkedin.com/in/shobharanip)

*Part of the CEO-Track AI Portfolio*
