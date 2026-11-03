# ⚡ InsightEngine Enterprise — Unstructured-to-Structured AI Pipeline

[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-red.svg)](https://streamlit.io/)
[![Google Gemini API](https://img.shields.io/badge/Google_Gemini_API-3.6--flash-orange.svg)](https://ai.google.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**InsightEngine Enterprise** is a commercial-grade, multi-tenant ready AI processing pipeline designed to convert raw, messy meeting transcripts, executive notes, and unstructured business text into decision-ready Markdown reports.

Engineered with strict zero-hallucination constraints, multi-language output capabilities, multi-schema report templates, and real-time operational telemetry for enterprise IT management.

---

## 🔥 Enterprise Features & Commercial Value

* **🎯 Multi-Schema Intelligence Extraction**: Switch seamlessly between *Executive Briefing*, *Technical & Infrastructure Review*, and *Product Strategy* templates.
* **🌐 Native Multi-Language Output**: Process input in any language and deliver structured reports in English, Traditional Chinese, Japanese, or Spanish.
* **🛡️ Zero-Hallucination Guardrails**: Enforces strict system instructions to guarantee zero data fabrication, preserving factual accuracy for high-stakes business decisions.
* **⚡ Production-Grade Telemetry**: Displays token payload size, processing latency, and execution HTTP status codes for enterprise cost tracking.
* **📁 Multi-Format Data Input**: Supports direct text streaming as well as `.txt` and `.md` file upload processing.
* **📦 Complete DevContainer & Docker Readiness**: Pre-configured with `.devcontainer` settings for zero-setup cloud deployment (GitHub Codespaces & VS Code Remote Containers).

---

## 🏗 System Architecture & Workflow

```
┌────────────────────────────────────────────────────────┐
│  Input Source: Raw Text / Document Upload (.txt/.md)  │
└──────────────────────────┬─────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────┐
│  InsightEngine Controls (Schema Prompt + Temperature) │
└──────────────────────────┬─────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────┐
│  Google Gemini Engine (gemini-3.6-flash Model)         │
└──────────────────────────┬─────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────┐
│  Structured Markdown & Operational Telemetry Metrics    │
│  ├── Executive Summary                                 │
│  ├── Critical Pain Points & Operational Risks          │
│  └── Action Items Table (Owner, Deadline, Priority)    │
└────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start Guide

### 1. Prerequisites
- Python 3.11+
- Google Gemini API Key

### 2. Installation
```bash
git clone https://github.com/your-username/insightengine-enterprise.git
cd insightengine-enterprise

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. API Key Setup
Create a `.streamlit/secrets.toml` file:
```toml
GEMINI_API_KEY = "your_enterprise_gemini_api_key"
```
Or export as environment variable:
```bash
export GEMINI_API_KEY="your_enterprise_gemini_api_key"
```

### 4. Launch Application
```bash
streamlit run app.py
```

---

## 📄 License
This project is licensed under the MIT License.