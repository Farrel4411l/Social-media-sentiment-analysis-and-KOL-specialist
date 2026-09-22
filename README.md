<!-- 
Author: Muhammad Farrel Haidar
Project: AI PR & KOL Specialist DSS
Date: 2026-09-22
-->

# AI PR & KOL Specialist: A Decision Support System for Digital Marketing

## Abstract / Overview
The AI PR & KOL Specialist is an advanced Decision Support System (DSS) designed to optimize digital marketing campaigns and Key Opinion Leader (KOL) management. By integrating Natural Language Processing (NLP), Retrieval-Augmented Generation (RAG), and Machine Learning (ML), this system automates the creation of highly persuasive, data-driven KOL Briefs and fair budget estimations.

## System Architecture
The system architecture comprises four core modules:
1. **NLP Sentiment Engine**: Extracts public sentiment and identifies audience "pain points" from raw text data.
2. **RAG Psychology Knowledge Base**: Embeds and retrieves marketing psychology literature, persuasion frameworks (e.g., AIDA, PAS, Cialdini's principles), and industry-standard templates.
3. **Strategist SLM Generator**: A Small Language Model (SLM) integrated with prompt engineering that synthesizes sentiment context and psychological frameworks to generate comprehensive KOL Briefs (Objective, Angle, Persona, Storyline).
4. **Budget Predictor ML**: A predictive regression model (utilizing Random Forest / XGBoost) to estimate fair KOL compensation based on historical metrics such as engagement rate, followers, and target reach.

## Technology Stack
- **Backend**: FastAPI (Python)
- **RAG & Orchestration**: LangChain
- **Vector Database**: ChromaDB
- **LLM/SLM**: HuggingFace Pipeline (Targeting models like Qwen2.5-7B)
- **Machine Learning**: scikit-learn, XGBoost
- **NLP**: TextBlob / HuggingFace Transformers

## Directory Structure
- `/api`: FastAPI endpoints and routing.
- `/models`: Machine learning pipelines and inference scripts (Budget Predictor & NLP).
- `/rag`: Vector database initialization, embedding logic, and RAG orchestrator.
- `/data`: Datasets, mocked documents, and serialized model artifacts.
- `/notebooks`: Jupyter notebooks for exploratory data analysis (EDA), model training, and experimentation.
