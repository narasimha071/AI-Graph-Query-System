# LLM Prompt Logs

## 1. Natural Language → Cypher

### Strategy

Used schema-aware prompting to generate accurate Cypher queries.

### Input

"Which customer is most active?"

### Generated Query

MATCH (c:Customer)
OPTIONAL MATCH (c)-[:PLACED]->(o:SalesOrder)
WITH c, count(o) AS orders
OPTIONAL MATCH (c)-[:MADE_PAYMENT]->(p:Payment)
WITH c, orders, count(p) AS payments
RETURN c.id, (orders + payments) AS activity
ORDER BY activity DESC

---

## 2. Auto-Correction

### Problem

LLM generated invalid queries (aggregation issues)

### Solution

Used second prompt with:

* Schema
* Error message
* Bad query

### Result

Query fixed automatically

---

## 3. Answer Generation

### Strategy

LLM acts as business analyst

### Output Example

"Customer X is the most active based on orders and payments"

---

## 4. Guardrails

Restricted queries using keywords:

* order
* customer
* invoice
* payment
* product

Irrelevant queries are rejected.
