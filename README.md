# 🚀 CareerPilot Agent

> An AI-powered backend application that automates the first stages of the job application process by transforming resumes into structured data, with a production-oriented architecture designed for future end-to-end job application automation.

---

## 📌 Overview

CareerPilot Agent is a backend-first AI application built to simplify and automate job applications.

The current implementation focuses on building a reliable AI pipeline that extracts structured information from resumes using Google's Gemini models, validates the output with Pydantic, and exposes it through a clean FastAPI API.

The project is designed with scalability in mind, making it easy to extend into a complete AI Career Copilot.

---

# ✨ Current Features

### ✅ Resume Upload API

* Upload resume in PDF format
* File validation
* Temporary file management
* Automatic cleanup

### ✅ PDF Processing

* Extracts text using PyMuPDF
* Handles corrupted PDFs
* Custom exception handling

### ✅ AI Resume Parsing

* Gemini 2.5 Flash integration
* Prompt-based structured extraction
* Converts unstructured resume text into structured JSON

### ✅ AI Response Normalization

* Cleans Gemini responses
* Normalizes inconsistent field names
* Handles missing values
* Prepares data for validation

### ✅ Resume Profile Generation

Extracts:

* Personal Information
* Skills
* Education
* Experience
* Projects
* Certifications
* Languages

using strongly typed Pydantic models.

### ✅ Production-Oriented Architecture

* FastAPI
* Dependency Injection
* Layered Architecture
* Custom Exceptions
* Structured Logging
* Service-Based Design
* Type Safety
* Clean Separation of Concerns

---

# 🏗️ Project Architecture

```text
Client
    │
    ▼
FastAPI API
    │
    ▼
Resume Agent
    │
    ▼
PDF Service
    │
    ▼
Resume Parser Service
    │
    ▼
Prompt Loader
    │
    ▼
Gemini Client
    │
    ▼
Google Gemini
    │
    ▼
Resume Normalizer
    │
    ▼
Pydantic Validation
    │
    ▼
ResumeProfile
```

---

# 📁 Project Structure

```text
backend/

├── api/
│   └── resume.py
│
├── agents/
│   └── resume_agent.py
│
├── services/
│   ├── pdf_service.py
│   ├── resume_parser_service.py
│   └── resume_normalizer.py
│
├── llm/
│   ├── gemini_client.py
│   ├── prompt_loader.py
│   └── prompts/
│       └── resume_parser.md
│
├── models/
│   ├── resume.py
│   └── resume_profile.py
│
├── core/
│   ├── config.py
│   ├── exceptions.py
│   └── logger.py
│
├── temp/
│
├── main.py
│
└── requirements / pyproject.toml
```

---

# ⚙️ Tech Stack

### Backend

* Python
* FastAPI
* Uvicorn

### AI

* Google Gemini 2.5 Flash
* Prompt Engineering

### Data Validation

* Pydantic v2

### PDF Processing

* PyMuPDF

### Logging

* Loguru

### Dependency Management

* uv

---

# 🔄 Current Processing Flow

```text
Upload Resume

↓

Validate PDF

↓

Extract Text

↓

Generate AI Prompt

↓

Gemini Processing

↓

Normalize Response

↓

Validate using Pydantic

↓

Return Structured Resume Profile
```

---

# 📌 Current API

## Upload Resume

```
POST /resume
```

Accepts

* PDF Resume

Returns

```json
{
    "name": "...",
    "email": "...",
    "skills": [],
    "education": [],
    "experience": [],
    "projects": []
}
```

---

# 🎯 Design Principles

The project follows several production-oriented software engineering principles:

* Layered Architecture
* Dependency Injection
* Single Responsibility Principle (SRP)
* Separation of Concerns
* Strong Typing with Pydantic
* Reusable Services
* Structured Logging
* Custom Exception Handling
* Modular AI Integration

---

# 🚧 In Progress

The project is actively under development.

Current focus includes:

* Improving AI response accuracy
* Better skill normalization
* Enhanced project technology extraction
* Structured experience parsing
* Generic AI response parser
* Better prompt engineering
* Global exception handlers
* Request tracing and performance metrics

---

# 🗺️ Roadmap

## Phase 1 (Completed)

* Resume Upload API
* PDF Text Extraction
* AI Resume Parsing
* Structured Resume Profile
* Production Backend Foundation

---

## Phase 2 (In Progress)

* Job Description Parser
* Job Profile Generation
* AI Response Improvements
* Matching Engine
* Resume Optimization Suggestions

---

## Phase 3 (Planned)

* Browser Automation
* Automatic Job Application
* Playwright Integration
* Smart Form Filling
* Resume Upload Automation

---

## Phase 4 (Planned)

* Authentication
* User Dashboard
* Database Integration
* Resume History
* Job Tracking
* Notifications
* Analytics

---

## Phase 5 (Vision)

CareerPilot aims to evolve into a complete AI Career Copilot capable of:

* Resume Analysis
* Resume Optimization
* Job Matching
* Cover Letter Generation
* Interview Preparation
* Automated Job Applications
* Career Insights
* Personalized AI Recommendations

---

# 📖 Learning Objectives

This project is being developed to explore and implement production-oriented AI backend engineering practices, including:

* AI-powered backend development
* Large Language Model integration
* Clean Architecture
* FastAPI application design
* Production-ready API development
* Structured data validation
* AI workflow orchestration
* Scalable software architecture

---

# 📄 License

This project is intended for educational purposes, portfolio demonstration, and continued research into AI-powered career automation systems.
