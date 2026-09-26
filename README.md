# 🏛️ CivicHelp AI — Government Schemes & Public Services Navigator

CivicHelp AI is an **evidence-grounded RAG and Agentic AI platform** designed to help citizens discover government schemes, understand eligibility requirements, identify required documents, and navigate public services across **Andhra Pradesh and Telangana**.

The system combines **Hybrid RAG, LangChain, LangGraph, BM25, dense embeddings, Cross-Encoder reranking, deterministic eligibility rules, and LLM-based response generation** to provide reliable, source-backed answers from official government information.

---

## 🚀 Key Features

### 🔎 1. Government Scheme Discovery
Find relevant government schemes based on:

- State
- Category
- User query
- Scheme-related keywords

Currently supports categories such as:

- 🎓 Education
- 🌾 Agriculture
- ❤️ Health
- 🤝 Welfare
- 🏛️ Government Services

---

### ✅ 2. Eligibility Checking

CivicHelp AI uses a **deterministic eligibility engine** for supported schemes.

For example:

> "I am 72 years old and live in Telangana. Am I eligible for Vay Vandana?"

The system extracts the user's profile and evaluates the applicable eligibility rules.

This approach avoids relying entirely on an LLM for rule-based eligibility decisions.

---

### 📄 3. Document Requirements

The system retrieves official information about documents required for government services and schemes.

For example:

> "What documents are required for Telangana ePASS?"

The system retrieves relevant government source documents and generates an evidence-backed response.

---

### 🧭 4. Application Guidance

CivicHelp AI can help users understand:

- Where to apply
- Application procedures
- Required documents
- Registration information
- Relevant government portals

---

### 🧠 5. Hybrid RAG Retrieval

The retrieval system combines:

**BM25 keyword retrieval**

+

**Dense vector retrieval**

↓

**Reciprocal Rank Fusion (RRF)**

↓

**Cross-Encoder Reranking**

↓

**Evidence Selection**

This helps improve retrieval quality for both keyword-heavy and semantic queries.

---

### 🔗 6. Source-Backed Responses

Responses are generated using retrieved evidence from government sources.

The system maintains metadata such as:

- Document ID
- Government authority
- State
- District
- Category
- Language
- Source type
- URL
- Published date
- Effective date
- Status
- Version

This enables the system to provide traceable citations.

---

### 🛡️ 7. Evidence Validation

Before generating the final answer, retrieved evidence is validated.

The validation layer checks:

- Query relevance
- Evidence quality
- Document relevance
- Important concept overlap
- Primary/supporting source relationships
- Citation availability

Unsupported responses are not treated as verified answers.

---

## 🏗️ System Architecture

```text
                         ┌─────────────────┐
                         │      User       │
                         └────────┬────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │   FastAPI API   │
                         └────────┬────────┘
                                  │
                                  ▼
                    ┌──────────────────────────┐
                    │   Query Understanding   │
                    └────────────┬─────────────┘
                                 │
                                 ▼
                       ┌──────────────────┐
                       │   Query Router   │
                       └────────┬─────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │   Query Planner  │
                       └────────┬─────────┘
                                │
                  ┌─────────────┴─────────────┐
                  │                           │
                  ▼                           ▼
        ┌──────────────────┐        ┌────────────────────┐
        │ Scheme Discovery │        │ Normal RAG Query   │
        └────────┬─────────┘        └─────────┬──────────┘
                 │                            │
                 │                            ▼
                 │                  ┌────────────────────┐
                 │                  │ Hybrid Retrieval   │
                 │                  │                    │
                 │                  │ BM25 + Dense       │
                 │                  └─────────┬──────────┘
                 │                            │
                 │                            ▼
                 │                  ┌────────────────────┐
                 │                  │ RRF Fusion         │
                 │                  └─────────┬──────────┘
                 │                            │
                 │                            ▼
                 │                  ┌────────────────────┐
                 │                  │ Cross Encoder      │
                 │                  │ Reranking          │
                 │                  └─────────┬──────────┘
                 │                            │
                 └─────────────┬──────────────┘
                               │
                               ▼
                    ┌────────────────────────┐
                    │ Evidence Validation   │
                    └────────────┬───────────┘
                                 │
                                 ▼
                    ┌────────────────────────┐
                    │ Eligibility Engine     │
                    │ Deterministic Rules    │
                    └────────────┬───────────┘
                                 │
                                 ▼
                    ┌────────────────────────┐
                    │   LLM Answer Generator │
                    └────────────┬───────────┘
                                 │
                                 ▼
                    ┌────────────────────────┐
                    │ Citation Builder       │
                    └────────────┬───────────┘
                                 │
                                 ▼
                         ┌───────────────┐
                         │ Final Answer  │
                         └───────────────┘
