# AI-Powered Graph Query System

## Overview

In real-world business systems, data is often fragmented across multiple tables such as orders, deliveries, invoices, and payments. This makes it difficult to trace relationships and understand end-to-end workflows.

This project solves that problem by converting structured business data into a **graph-based model** and enabling users to interact with it using **natural language queries**.

The system integrates a **Graph Database (Neo4j)** with a **Large Language Model (LLM)** to dynamically generate queries and return **data-backed answers**, along with visual insights.

---

## Key Features

* 🔗 Graph-based data modeling using Neo4j
* 💬 Natural language query interface
* 🔄 Automatic conversion of queries (NL → Cypher)
* 📊 Hybrid output (Graph visualization + Table results)
* 🧠 AI-generated answers grounded in data
* 🔁 Auto-correction layer for fixing query errors
* 🧾 Schema-aware query generation
* 💬 Multi-turn conversation (chat memory)
* 🔐 Guardrails for domain-restricted queries
* 📈 KPI metrics and tabular insights

---

## 🏗️ Architecture

```
User Query (Natural Language)
        ↓
LLM (NL → Cypher Translation)
        ↓
Validation + Optimization Layer
        ↓
Neo4j Graph Database
        ↓
Structured Data (Nodes / Table)
        ↓
LLM (Answer Generation)
        ↓
UI (Streamlit + Graph Visualization)
```

---

## 📊 Data Model

The dataset is transformed into a graph consisting of:

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

## Functional Requirements Implemented

### 1️⃣ Graph Construction

* Data is modeled as nodes and relationships in Neo4j
* Supports multi-entity business flows

### 2️⃣ Graph Visualization

* Interactive graph using PyVis
* Displays entity connections and relationships

### 3️⃣ Conversational Query Interface

* Accepts natural language questions
* Converts queries dynamically into Cypher
* Executes queries and returns accurate results

---

## Advanced Features

### 🔥 Auto-Correction Layer (Self-Healing System)

* Detects Cypher query errors
* Automatically fixes queries using LLM
* Retries execution without user intervention

### 🔍 Hybrid Query Handling

* Graph queries → Visual graph output
* Analytical queries → Table format

### 🧾 Schema-Aware Prompting

* Dynamically fetches schema from Neo4j
* Improves accuracy of generated queries

### 💬 Chat Memory

* Maintains context across multiple queries

### 📊 KPI Dashboard

* Displays key metrics like:

  * Total nodes
  * Total relationships

---

## Example Queries

### 🔹 Analytical Queries

* What is the total number of orders?
* Which customer made the most payments?
* What is the average number of products per order?

### 🔹 Graph Queries

* Trace the lifecycle of order "740509"
* Show all products in an order
* Show full flow from customer to invoice

### 🔹 Edge Case Queries

* Show orders without delivery
* Show customers with no payments
* Identify incomplete transactions

---

## Guardrails

The system restricts queries strictly to dataset-related topics.

Example response:

> "This system is designed to answer questions related to the dataset only."

---

## 🛠️ Tech Stack

| Component     | Technology |
| ------------- | ---------- |
| Frontend      | Streamlit  |
| Backend       | Python     |
| Database      | Neo4j      |
| LLM           | Groq API   |
| Visualization | PyVis      |

---

## Installation

```bash
git clone https://github.com/your-username/AI-Graph-Query-System.git
cd AI-Graph-Query-System
pip install -r requirements.txt
```

---

## Run the Application

```bash
streamlit run app.py
```

---

## Environment Variables

Create a `.env` file in the root directory:

```
GROQ_API_KEY=your_api_key_here
```

---

## Project Structure

```
AI-Graph-Query-System/
│
├── app.py
├── Neo4j_loader.py
├── requirements.txt
├── dataset/
├── screenshots/
```
---

## Evaluation Highlights

* Clean and modular architecture
* Strong graph data modeling
* Effective LLM integration and prompting
* Robust error handling with auto-correction
* Domain-specific guardrails

---

## 🚀 Future Enhancements

* Query confidence scoring
* Advanced analytics dashboard
* Graph clustering and community detection
* Cloud deployment (AWS / Streamlit Cloud)

---

## 🙌 Conclusion

This project demonstrates how **Graph Databases + LLMs** can be combined to build an intelligent, explainable, and interactive data exploration system.

It enables users to seamlessly explore complex business relationships using simple natural language queries.

---
