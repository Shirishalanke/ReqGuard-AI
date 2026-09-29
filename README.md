# 🛡️ ReqGuard-AI

### AI-Based Requirements Drift Detection System

ReqGuard-AI is an AI-powered software requirements analysis system designed to detect **semantic drift between baseline and current software requirements**.

The system uses Natural Language Processing (NLP) and sentence embeddings to compare requirement versions, calculate semantic similarity, determine a drift score, classify the level of change, and identify potentially affected software components.

## 🚀 Live Demo

Try the deployed application here:

👉 **[Open ReqGuard-AI on Streamlit](https://reqguard-ai-o4opx42uz8imgeiyp788gv.streamlit.app/)**

---

## 📌 Project Overview

Software requirements frequently change during the development lifecycle.

A small change in a requirement can potentially affect:

- Application logic
- Database design
- API implementation
- Security mechanisms
- Performance requirements
- Test cases
- Documentation
- System architecture

Traditional requirement comparison mainly depends on manually reviewing different versions of requirement documents.

ReqGuard-AI provides an automated approach by using **semantic similarity analysis** to identify meaningful differences between an original requirement and its current version.

---

## 🎯 Objectives

The main objectives of ReqGuard-AI are:

- Detect changes between baseline and current requirements
- Calculate semantic similarity using AI-based sentence embeddings
- Calculate a requirements drift score
- Classify drift into Low, Medium, and High levels
- Identify potentially affected software components
- Provide requirement traceability
- Generate downloadable drift reports
- Provide a dashboard for analyzing requirement changes

---

## ✨ Key Features

### 🔍 1. Requirement Drift Detection

Users can enter:

- Baseline Requirement
- Current Requirement

The system compares both requirements using semantic embeddings.

---

### 🤖 2. AI-Based Semantic Similarity

ReqGuard-AI uses the:

**Sentence Transformers – `all-MiniLM-L6-v2`**

model to convert requirements into numerical vector representations.

The system then calculates cosine similarity between the two requirement embeddings.

---

### 📊 3. Drift Score

The drift score is calculated using:

```text
Drift Score = 1 - Semantic Similarity
