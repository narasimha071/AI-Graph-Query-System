import streamlit as st
from dotenv import load_dotenv
from neo4j import GraphDatabase
from groq import Groq
import os
import pandas as pd
from pyvis.network import Network
import streamlit.components.v1 as components
import re

# 🔹 Load ENV
load_dotenv()

# 🔹 Neo4j
driver = GraphDatabase.driver(
    "bolt://localhost:7687",
    auth=("neo4j", "Raju@2003")
)

# 🔹 Groq
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# =========================================================
# FLOW TRACING (NEW)
# =========================================================
def detect_flow_query(user_input):
    match = re.search(r"\b(\d{5,})\b", user_input)

    if "trace" in user_input.lower() and match:
        doc_id = match.group(1)

        return f"""
        MATCH (o:SalesOrder {{id: '{doc_id}'}})
        OPTIONAL MATCH (o)-[:DELIVERED_AS]->(d)
        OPTIONAL MATCH (d)-[:BILLED_AS]->(i)
        OPTIONAL MATCH (c:Customer)-[:PLACED]->(o)
        RETURN o,d,i,c
        """
    return None

# =========================================================
# LOGGING
# =========================================================
def log_query(user_input, cypher):
    print("\n USER:", user_input)
    print("CYPHER:", cypher)

# =========================================================
# VALIDATION + OPTIMIZATION
# =========================================================
def validate_and_optimize_query(query):
    forbidden = ["DELETE", "DETACH", "CREATE", "MERGE", "DROP"]

    if any(word in query.upper() for word in forbidden):
        raise ValueError("Unsafe query blocked")

    query = query.strip().rstrip(";")

    if "LIMIT" not in query.upper():
        query += " LIMIT 50"

    return query

# =========================================================
# SCHEMA
# =========================================================
def get_schema():
    with driver.session() as session:
        result = session.run("CALL db.schema.visualization()")
        return str([r.data() for r in result])

# =========================================================
# NL → CYPHER
# =========================================================
def nl_to_cypher(question):
    schema = get_schema()

    prompt = f"""
    You are an expert Neo4j Cypher generator.

    Graph Schema:
    {schema}

    Rules:
    - Use only schema provided
    - Always use property "id"
    - IDs are STRINGS
    - Use OPTIONAL MATCH where needed
    - No semicolons

    Return ONLY Cypher query.

    Question: {question}
    """

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": prompt}]
    )

    query = response.choices[0].message.content.strip()
    return query.replace("```", "").strip()

# =========================================================
# AUTO-CORRECTION
# =========================================================
def fix_cypher_query(question, bad_query, error_msg):
    schema = get_schema()

    prompt = f"""
    You are an expert Neo4j Cypher debugger.

    Graph Schema:
    {schema}

    Question: {question}
    Bad Query: {bad_query}
    Error: {error_msg}

    Fix the query and return only Cypher.
    """

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip().replace("```", "")

# =========================================================
# CHAT MEMORY
# =========================================================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# =========================================================
# AI ANSWER
# =========================================================
def generate_answer(question, data):
    history = st.session_state.chat_history[-3:]

    prompt = f"""
    You are a business analyst.

    Conversation History:
    {history}

    Question: {question}
    Data: {data}

    Give a short answer.
    """

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": prompt}]
    )

    answer = response.choices[0].message.content.strip()

    st.session_state.chat_history.append({
        "question": question,
        "answer": answer
    })

    return answer

# =========================================================
# GRAPH CHECK
# =========================================================
def is_graph_data(records):
    for r in records:
        for v in r.values():
            if hasattr(v, "labels") or hasattr(v, "start_node") or hasattr(v, "nodes"):
                return True
    return False

# =========================================================
# GRAPH STRUCTURE + HIGHLIGHT (UPDATED)
# =========================================================
def structured_graph_output(records):
    nodes, edges = [], []
    seen = set()
    highlight_ids = set()

    for record in records:
        for value in record.values():

            if hasattr(value, "nodes"):
                for node in value.nodes:
                    node_id = node.get("id")
                    label = list(node.labels)[0]

                    highlight_ids.add(node_id)

                    if node_id not in seen:
                        nodes.append({"id": node_id, "type": label})
                        seen.add(node_id)

                for rel in value.relationships:
                    edges.append({
                        "type": rel.type,
                        "from": rel.start_node.get("id"),
                        "to": rel.end_node.get("id")
                    })

            elif hasattr(value, "labels"):
                node_id = value.get("id")
                label = list(value.labels)[0]

                highlight_ids.add(node_id)

                if node_id not in seen:
                    nodes.append({"id": node_id, "type": label})
                    seen.add(node_id)

            elif hasattr(value, "start_node"):
                edges.append({
                    "type": value.type,
                    "from": value.start_node.get("id"),
                    "to": value.end_node.get("id")
                })

    return {"nodes": nodes, "edges": edges, "highlight": highlight_ids}

# =========================================================
# KPI
# =========================================================
def show_kpis(graph_data):
    col1, col2 = st.columns(2)
    col1.metric("Total Nodes", len(graph_data["nodes"]))
    col2.metric("Total Relationships", len(graph_data["edges"]))

# =========================================================
# TABLE VIEW
# =========================================================
def show_table(graph_data):
    st.subheader("Nodes")
    st.dataframe(pd.DataFrame(graph_data["nodes"]))

    st.subheader("Relationships")
    st.dataframe(pd.DataFrame(graph_data["edges"]))

# =========================================================
# GRAPH VISUALIZATION (WITH HIGHLIGHT)
# =========================================================
def visualize_graph(graph_data):
    net = Network(height="650px", width="100%", bgcolor="#0b0f19", font_color="white")

    for node in graph_data["nodes"]:
        if node["id"] in graph_data["highlight"]:
            net.add_node(
                node["id"],
                label=node["id"],
                color="red",
                size=25
            )
        else:
            net.add_node(node["id"], label=node["id"])

    for edge in graph_data["edges"]:
        net.add_edge(edge["from"], edge["to"], label=edge["type"])

    net.save_graph("graph.html")

    with open("graph.html", "r", encoding="utf-8") as f:
        components.html(f.read(), height=650)

# =========================================================
# GUARDRAILS
# =========================================================
def is_valid_query(user_input):
    allowed = [
        "order", "delivery", "invoice", "payment",
        "customer", "product"
    ]
    return any(k in user_input.lower() for k in allowed)

# =========================================================
# UI
# =========================================================
st.set_page_config(page_title="Graph Query System", layout="wide")
st.title("Graph Query System (AI-Automated)")

user_input = st.text_input("Ask a business question")

if st.button("Ask"):

    if not user_input:
        st.warning("Enter a question")

    elif not is_valid_query(user_input):
        st.error("This system is designed to answer dataset-related questions only.")

    else:
        try:
            # FLOW FIRST
            cypher_query = detect_flow_query(user_input)

            if not cypher_query:
                cypher_query = nl_to_cypher(user_input)

            cypher_query = validate_and_optimize_query(cypher_query)

            log_query(user_input, cypher_query)

            st.subheader("Generated Cypher")
            st.code(cypher_query)

            with driver.session() as session:
                try:
                    result = session.run(cypher_query)
                    records = list(result)

                except Exception as e:
                    st.warning("Query failed. Auto-fixing...")

                    fixed_query = fix_cypher_query(user_input, cypher_query, str(e))
                    fixed_query = validate_and_optimize_query(fixed_query)

                    st.subheader("Fixed Cypher")
                    st.code(fixed_query)

                    result = session.run(fixed_query)
                    records = list(result)

            if not records:
                st.warning("No data found")

            else:
                if not is_graph_data(records):
                    df = pd.DataFrame([r.data() for r in records])

                    st.subheader("Table Result")
                    st.dataframe(df)

                    st.subheader("AI Answer")
                    st.write(generate_answer(user_input, df.to_dict()))

                else:
                    graph_data = structured_graph_output(records)

                    st.subheader("KPIs")
                    show_kpis(graph_data)

                    st.subheader("Graph View")
                    visualize_graph(graph_data)

                    st.subheader("AI Answer")
                    st.write(generate_answer(user_input, graph_data["nodes"][:20]))

        except Exception as e:
            st.error(f"Error: {str(e)}")