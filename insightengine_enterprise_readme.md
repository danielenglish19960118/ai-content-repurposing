# ⚡ InsightEngine Enterprise — AI-Powered Unstructured-to-Structured BI SaaS

[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-red.svg)](https://streamlit.io/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109%2B-teal.svg)](https://fastapi.tiangolo.com/)
[![Pydantic v2](https://img.shields.io/badge/Pydantic-v2.5-green.svg)](https://pydantic.dev/)
[![Docker Ready](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![License: Commercial / MIT](https://img.shields.io/badge/License-Commercial-orange.svg)](https://opensource.org/licenses/MIT)

**InsightEngine Enterprise** is a production-grade, multi-tenant B2B SaaS platform engineered to transform messy meeting transcripts, engineering incident logs, and unstructured executive notes into **100% strictly validated, decision-ready executive reports** using Google Gemini and Pydantic schema enforcement.

---

## 💼 Why Enterprises & Buyers Choose InsightEngine

1. **Eliminate Manual Report Overhead**: Reduces hours of manual synthesis down to **sub-5-second automated pipelines**, saving thousands of management hours annually.
2. **Guaranteed Zero Schema Drift**: Unlike standard LLM prompts that break or hallucinate formatting, our engine enforces **Pydantic Structured Outputs** (`response_schema`), guaranteeing 100% deterministic, database-ready JSON and Markdown reports every time.
3. **Strict Data Privacy & On-Premises Security**: Designed for enterprise compliance. Deployable entirely via Docker inside your private cloud (AWS, Azure, GCP) with **Zero Data Retention (ZDR)** options.
4. **Seamless Workflow Integration**: Beyond the Streamlit web dashboard, the built-in **FastAPI REST gateway** allows instant integration with corporate Slack bots, Notion databases, or Zapier pipelines.

---

## 🏛 Clean System Architecture

```text
  [ Raw Input Sources ]       [ InsightEngine Enterprise Core SaaS ]           [ Enterprise Output ]
  • Meeting Transcripts ──►  ┌──────────────────────────────────────┐  ──►  • 100% Validated JSON Schema
  • Engineering Logs         │ api.py        (FastAPI REST Gateway) │       • Executive Markdown Report
  • Executive Notes          │ src/models.py (Pydantic Enforcement) │       • Token Cost & Latency Telemetry
                             │ src/engine.py (Google Gemini SDK)    │       • SQLite Audit Logs
                             └──────────────────────────────────────┘
```

---

## 🔥 Key Technical & Commercial Features

* **🛡️ Deterministic Schema Enforcement**: Eliminates LLM hallucinations and unexpected markdown layout shifts through strict Pydantic model validation.
* **⚡ Token Telemetry & Rate Limiting**: Built-in rate limiter and session cost calculator tracking token consumption and estimated execution costs in real time.
* **🌐 Native Multi-Language Support**: Instantly synthesize and translate raw notes into English, Traditional Chinese, Japanese, or Spanish.
* **📊 Dual-Format Export**: Export structured intelligence instantly as clean Markdown (`.md`) or parsed enterprise JSON schema (`.json`).
* **📦 Enterprise DevOps Ready**: Fully containerized with `Dockerfile`, `docker-compose.yml`, `devcontainer.json`, and automated unit test suites (`tests/`).

---

## 🚀 Quick Start Guide

### 1. Local Installation
```bash
git clone https://github.com/your-org/insightengine-enterprise.git
cd insightengine-enterprise
pip install -r requirements.txt
```

### 2. Launch Streamlit Dashboard
```bash
export GEMINI_API_KEY="your_enterprise_api_key"
streamlit run app.py
```
*(Windows Users: Double-click `run.bat` for automated setup and launch).*

### 3. Launch FastAPI REST Gateway
```bash
uvicorn api:app --host 0.0.0.0 --port 8000 --reload
```
Access interactive API docs at `http://localhost:8000/docs`.

### 4. Docker Deployment
```bash
docker-compose up --build
```

---

## 💰 Commercial Licensing & Enterprise Inquiries

InsightEngine Enterprise is available under flexible licensing terms for modern organizations and independent software vendors (ISVs):

* **Self-Hosted Annual License**: Complete source code access, Docker container rights, and priority integration support for deployment within your private cloud.
* **Managed Cloud SaaS Subscription**: Fully managed multi-tenant access with usage-based billing tiers.

For enterprise licensing inquiries, custom schema integrations, or custom AI pipeline consulting, please contact our commercial team at **enterprise@insightengine.io**.

---

## 📄 License
This project is proprietary / commercial-grade software. See [LICENSE](LICENSE) for details.