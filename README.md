# 🚀 CareerPilot AI Agent

An end-to-end AI-powered job application platform that analyzes resumes, matches them with job descriptions, and automates the job application workflow using browser automation.

---

# 📌 Overview

CareerPilot is designed to reduce the manual effort involved in job applications.

The platform combines AI resume analysis, job parsing, intelligent matching, and browser automation into a single workflow while keeping the user in control whenever manual verification is required.

---

# ✨ Current Features

## 📄 Resume Processing

- Upload PDF resumes
- Resume text extraction
- AI-powered resume parsing
- Structured resume profile generation
- Resume deduplication using SHA-256 hashing
- Resume stored with structured JSON

---

## 💼 Job Processing

- Job URL validation
- AI-powered job description parsing
- Structured job profile generation
- Job URL deduplication
- Job metadata storage
- Original application URL preserved

---

## 🤖 AI Resume Matching

- Resume vs Job semantic comparison
- Skill gap analysis
- Match score generation
- Strengths identification
- Missing skills detection
- AI-generated recommendations
- Structured match report

---

## 📂 Application Management

- Unified Application entity
- Resume + Job + Match linked together
- Application lifecycle tracking
- Application history
- Multiple applications support
- Application status management

Current Status Flow

```
Created
↓

Match Pending
↓

Ready

↓

Proceeded

↓

Completed

OR

Cancelled
```

---

## 🎨 Frontend Dashboard

Production-style responsive dashboard.

Features

- Dashboard Overview
- Application History
- Search Applications
- Filter Applications
- Sort Applications
- Match Score Display
- Application Details Drawer
- Mobile Responsive UI
- Dark Theme UI
- Resume Upload Modal
- Drag & Drop Resume Upload
- Client-side Validation
- Real-time Status Refresh

---

## ⚡ Automation Engine

Current automation pipeline

```
Proceed

↓

Background Automation

↓

Launch Chromium

↓

Open Job URL

↓

Detect Apply Button

↓

Click Apply

↓

Capture Screenshot

↓

Automation Logs

↓

Browser Cleanup
```

Implemented Components

- Browser Manager
- Browser Actions
- Apply Button Detector
- Apply Action
- Screenshot Service
- Automation Log Service
- Background Automation Execution

---

## 📝 Form Automation Foundation

Generic automation architecture for supporting multiple career portals.

Implemented

- Generic Form Detector
- Field Classifier
- Form Mapper
- Fill Engine Architecture
- Navigation Engine Architecture
- Login Detector
- CAPTCHA Detector
- Dynamic Form Scanning

---

## 🏗️ Architecture

Project follows a modular AI Agent architecture.

```
Frontend

↓

FastAPI APIs

↓

AI Agents

↓

Services

↓

Repositories

↓

PostgreSQL

↓

Automation Engine

↓

Playwright Browser
```

---

## 🔒 Production Practices

- Repository Pattern
- Dependency Injection
- Service Layer
- Agent-based Architecture
- Modular Automation Components
- Structured Logging
- Background Task Execution
- Database-backed Status Tracking
- Error Handling
- Resume & Job Deduplication
- Clean Separation of Responsibilities

---

# 🚧 In Progress

## Real-Time Automation

- Live Automation Timeline
- Server-Sent Events (SSE)
- Automation Progress Streaming
- Live Browser Status
- Live Automation Logs

---

## Human-in-the-Loop Automation

When automation requires user verification, CareerPilot pauses and requests user input instead of making assumptions.

Planned interactions include:

- Login Required
- CAPTCHA Verification
- Salary Expectations
- Visa Sponsorship
- Work Authorization
- Notice Period
- Disability Declaration
- Custom Employer Questions

Automation resumes automatically after user input.

---

## Universal Form Automation

Building a generic form engine capable of handling multiple ATS platforms.

Target Platforms

- LinkedIn
- Workday
- Greenhouse
- Lever
- SAP SuccessFactors
- Oracle Recruiting
- Taleo
- Naukri
- Company Career Portals

---

## AI Automation

Upcoming capabilities

- Multi-step form navigation
- Intelligent field mapping
- Resume upload automation
- Dynamic question understanding
- AI-powered field selection
- Automatic application submission
- Submission proof generation

---

## AutoPilot Mode (Planned)

A fully autonomous job search and application workflow.

Vision

```
Upload Resume

↓

AI searches relevant jobs

↓

Ranks opportunities

↓

Requests user approval

↓

Applies automatically

↓

Tracks application status

↓

Provides submission proof

↓

Maintains complete application history
```

---

# 🎯 Project Goal

To build a production-ready AI Job Application Agent capable of understanding resumes, analyzing jobs, automating applications across multiple career portals, and keeping users in control through a secure Human-in-the-Loop workflow.