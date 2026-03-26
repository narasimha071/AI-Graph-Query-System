# AI-Powered Graph Query System

## Overview

In real-world business systems, data is often fragmented across multiple tables such as orders, deliveries, invoices, and payments. This makes it difficult to trace relationships and understand end-to-end workflows.

This project addresses this challenge by transforming structured business data into a **graph-based model** and enabling users to interact with it using **natural language queries**.

The system integrates a **Graph Database (Neo4j)** with a **Large Language Model (LLM)** to dynamically generate Cypher queries, execute them, and return **data-backed insights** along with visual representations.

---

## Problem Statement

* Business data requires complex joins across multiple tables
* Non-technical users cannot write SQL/Cypher queries
* Tracing end-to-end workflows is difficult

---

## Solution

This system enables:

* Natural language querying
* Automatic Cypher generation
* Graph-based visualization
* AI-generated business insights
* End-to-end flow tracing

---

## Dataset

The dataset represents an **Order-to-Cash (O2C) lifecycle**:

Customer → Sales Order → Delivery → Invoice → Payment

### 🔹 Entities:

* Customers
* Sales Orders
* Products
* Deliveries
* Invoices
* Payments

### 🔹 Purpose:

* Understand business workflows
* Detect incomplete transactions
* Analyze relationships

---

## Architecture

```
User Query (Natural Language)
        ↓
LLM (NL → Cypher Translation)
        ↓
Validation + Guardrails Layer
        ↓
Neo4j Graph Database
        ↓
Structured Data (Graph/Table)
        ↓
LLM (Answer Generation)
        ↓
UI (Streamlit + PyVis Visualization)
```

---

## Data Model

### 🔹 Nodes

* Customer
* SalesOrder
* Product
* Delivery
* Invoice
* Payment

### 🔹 Relationships

* Customer → PLACED → SalesOrder
* SalesOrder → HAS_PRODUCT → Product
* SalesOrder → DELIVERED_AS → Delivery
* Delivery → BILLED_AS → Invoice
* Customer → MADE_PAYMENT → Payment

---

## Key Features

* Natural language → Cypher conversion
* Auto query correction (self-healing system)
* Hybrid output (Graph + Table)
* AI-generated answers grounded in data
* Schema-aware prompting
* Chat memory (context retention)
* Domain guardrails
* KPI metrics

---

##  Advanced Features

### 1️⃣ Flow Tracing

* Tracks complete lifecycle of a business entity
* Example:

  * Customer → Order → Delivery → Invoice

### 2️⃣ Node Highlighting

* Relevant nodes are highlighted in graph
* Improves interpretability

### 3️⃣ Auto-Correction Layer

* Detects and fixes Cypher query errors
* Retries execution automatically

---

##  Example Queries

### 🔹 Analytical

* Which customer is most active?
* What is total number of orders?

### 🔹 Graph Queries

* Trace order 740556
* Show full lifecycle of a sales order

### 🔹 Edge Cases

* Show orders without delivery
* Show customers with no payments

---

## Guardrails

The system restricts queries strictly to dataset-related topics.

Example:
❌"Tell me about cricket"
✔ Returns:

> This system is designed to answer questions related to the dataset only.

---

## ⚙️ Tech Stack

| Component     | Technology |
| ------------- | ---------- |
| Frontend      | Streamlit  |
| Backend       | Python     |
| Database      | Neo4j      |
| LLM API       | Groq       |
| Visualization | PyVis      |

---

## Setup Instructions

### 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/AI-Graph-Query-System.git
cd AI-Graph-Query-System
```

---

### 2️⃣ Install Dependencies

```bash
pip install -r src/requirements.txt
```

---

### 3️⃣ Configure Environment

Create `.env` file:

```
GROQ_API_KEY=your_api_key
```

---

### 4️⃣ Start Neo4j

* Run Neo4j locally at:

```
bolt://localhost:7687
```

---

### 5️⃣ Load Dataset

```bash
python src/neo4j_loader.py
```

---

### 6️⃣ Run Application

```bash
streamlit run src/app.py
```

---

## Project Structure

```
AI-Graph-Query-System/
│
├── src/
│   ├── app.py
│   ├── Neo4j_loader.py
│   ├── requirements.txt
│
├── sap-order-to-cash-dataset/
├── screenshots/
│
├── sessions/
│   ├── llm_prompt_logs.md
│   ├── development_journey.md
│
├── README.md
├── .gitignore
```

---

## LLM Usage

The LLM is used for:

* Natural language → Cypher conversion
* Query debugging (auto-fix)
* AI answer generation

---

## AI Coding Sessions

All AI interaction logs are included in `/sessions` folder.

These demonstrate:

* Prompt design
* Debugging workflow
* Iteration process

---
## Evaluation Highlights

* Strong graph modeling of business workflow
* Effective LLM integration with schema awareness
* Robust guardrails implementation
* Advanced features like flow tracing & highlighting
* Clean and modular architecture

---
## Future Enhancements

* Semantic search
* Graph clustering
* AWS deployment
* Advanced dashboards

---
## Conclusion

This project demonstrates how **Graph Databases + LLMs** can be combined to build an intelligent, explainable, and interactive data exploration system.

It enables users to seamlessly explore complex business relationships using simple natural language queries.

