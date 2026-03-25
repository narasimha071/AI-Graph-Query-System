import json
import os
from neo4j import GraphDatabase

# 🔹 Load JSONL files
def load_jsonl(folder_path):
    data = []
    for file in os.listdir(folder_path):
        if file.endswith(".jsonl"):
            with open(os.path.join(folder_path, file)) as f:
                for line in f:
                    data.append(json.loads(line))
    return data


# 🔹 Load datasets
customers = load_jsonl("sap-order-to-cash-dataset/business_partners")
orders = load_jsonl("sap-order-to-cash-dataset/sales_order_headers")
items = load_jsonl("sap-order-to-cash-dataset/sales_order_items")
delivery_items = load_jsonl("sap-order-to-cash-dataset/outbound_delivery_items")
billing_items = load_jsonl("sap-order-to-cash-dataset/billing_document_items")
payments = load_jsonl("sap-order-to-cash-dataset/payments_accounts_receivable")


print("Customers:", len(customers))
print("Orders:", len(orders))
print("Items:", len(items))
print("Delivery Items:", len(delivery_items))
print("Billing Items:", len(billing_items))
print("Payments:", len(payments))


# 🔹 Connect Neo4j
driver = GraphDatabase.driver(
    "bolt://localhost:7687",
    auth=("neo4j", "Raju@2003")
)


# 🔹 Batch Helper
def run_batch_query(query, data, batch_size=500):
    with driver.session() as session:
        for i in range(0, len(data), batch_size):
            batch = data[i:i + batch_size]
            session.run(query, batch=batch)


# 🔹 Load Graph Efficiently
def load_graph():

    # ✅ Customers
    run_batch_query("""
        UNWIND $batch AS row
        MERGE (c:Customer {id: row.businessPartner})
        SET c.name = row.businessPartnerFullName
    """, customers)

    # ✅ Orders
    run_batch_query("""
        UNWIND $batch AS row
        MERGE (o:SalesOrder {id: row.salesOrder})
        SET o.amount = toFloat(row.totalNetAmount)

        WITH o, row
        MATCH (c:Customer {id: row.soldToParty})
        MERGE (c)-[:PLACED]->(o)
    """, orders)

    # ✅ Products
    run_batch_query("""
        UNWIND $batch AS row
        MERGE (p:Product {id: row.material})

        WITH p, row
        MATCH (o:SalesOrder {id: row.salesOrder})
        MERGE (o)-[:HAS_PRODUCT]->(p)
    """, items)

    # ✅ Deliveries
    run_batch_query("""
        UNWIND $batch AS row
        WITH row
        WHERE row.deliveryDocument IS NOT NULL 
          AND row.referenceSdDocument IS NOT NULL

        MERGE (d:Delivery {id: row.deliveryDocument})

        WITH d, row
        MATCH (o:SalesOrder {id: row.referenceSdDocument})
        MERGE (o)-[:DELIVERED_AS]->(d)
    """, delivery_items)

    # ✅ Invoices
    run_batch_query("""
        UNWIND $batch AS row
        WITH row
        WHERE row.billingDocument IS NOT NULL

        MERGE (i:Invoice {id: row.billingDocument})

        WITH i, row
        MATCH (d:Delivery {id: coalesce(row.referenceSdDocument, row.referenceSDDocument)})
        MERGE (d)-[:BILLED_AS]->(i)
    """, billing_items)

    #  ✅ Payments (FIXED)
    run_batch_query("""
        UNWIND $batch AS row
        WITH row
        WHERE row.accountingDocument IS NOT NULL 
          AND row.customer IS NOT NULL

        MERGE (p:Payment {id: row.accountingDocument})
        SET 
            p.amount = toFloat(row.amountInTransactionCurrency),
            p.currency = row.transactionCurrency,
            p.date = row.postingDate

        WITH p, row
        MATCH (c:Customer {id: row.customer})
        MERGE (c)-[:MADE_PAYMENT]->(p)
    """, payments)

    print("Graph Loaded Successfully!")


# 🔹 Run
load_graph()