import streamlit as st
import sqlite3
import pandas as pd

DB_FILE = "food_sharing.db"

def get_connection():
    return sqlite3.connect(DB_FILE, check_same_thread=False)

def run_query(query, params=None):
    conn = get_connection()
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df

def execute_query(query, params=None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, params or [])
    conn.commit()
    cursor.close()
    conn.close()

st.title("Food Sharing-Analytics and Operations")

menu = ["Queries", "Contacts", "CRUD"]
choice = st.sidebar.selectbox("Menu", menu)

#15 SQL Queries
if choice == "Queries":
    st.header("Analytics Queries")

    query_options = [
        "Food wastage by type",
        "Food wastage by location",
        "Food wastage by expiry date",
        "Most active providers",
        "Most active receivers",
        "Claims by status",
        "Claims over time",
        "Available food by type",
        "Available food by location",
        "Expired vs Non-expired food",
        "Top cities with food donations",
        "Receivers by city",
        "Average quantity per listing",
        "Meal type distribution",
        "Food type distribution"
    ]

    query_choice = st.selectbox("Select a query", query_options)

    if query_choice == "Food wastage by type":
        query = """
            SELECT food_type, SUM(quantity) AS total_wasted
            FROM Food_Listings
            WHERE expiry_date < DATE('now')
            GROUP BY food_type
            ORDER BY total_wasted DESC;
        """
        st.dataframe(run_query(query))

    elif query_choice == "Food wastage by location":
        query = """
            SELECT location, SUM(quantity) AS total_wasted
            FROM Food_Listings
            WHERE expiry_date < DATE('now')
            GROUP BY location
            ORDER BY total_wasted DESC;
        """
        st.dataframe(run_query(query))

    elif query_choice == "Food wastage by expiry date":
        query = """
            SELECT expiry_date, SUM(quantity) AS total_wasted
            FROM Food_Listings
            WHERE expiry_date < DATE('now')
            GROUP BY expiry_date
            ORDER BY expiry_date;
        """
        st.dataframe(run_query(query))

    elif query_choice == "Most active providers":
        query = """
            SELECT p.name, COUNT(f.food_id) AS total_listings
            FROM Providers p
            JOIN Food_Listings f ON p.provider_id = f.provider_id
            GROUP BY p.name
            ORDER BY total_listings DESC;
        """
        st.dataframe(run_query(query))

    elif query_choice == "Most active receivers":
        query = """
            SELECT r.name, COUNT(c.claim_id) AS total_claims
            FROM Receivers r
            JOIN Claims c ON r.receiver_id = c.receiver_id
            GROUP BY r.name
            ORDER BY total_claims DESC;
        """
        st.dataframe(run_query(query))

    elif query_choice == "Claims by status":
        query = "SELECT status, COUNT(*) AS total FROM Claims GROUP BY status;"
        st.dataframe(run_query(query))

    elif query_choice == "Claims over time":
        query = "SELECT DATE(timestamp) AS date, COUNT(*) AS total_claims FROM Claims GROUP BY DATE(timestamp);"
        st.dataframe(run_query(query))

    elif query_choice == "Available food by type":
        query = """
            SELECT food_type, SUM(quantity) AS available
            FROM Food_Listings
            WHERE expiry_date >= DATE('now')
            GROUP BY food_type;
        """
        st.dataframe(run_query(query))

    elif query_choice == "Available food by location":
        query = """
            SELECT location, SUM(quantity) AS available
            FROM Food_Listings
            WHERE expiry_date >= DATE('now')
            GROUP BY location;
        """
        st.dataframe(run_query(query))

    elif query_choice == "Expired vs Non-expired food":
        query = """
            SELECT 
              SUM(CASE WHEN expiry_date < DATE('now') THEN quantity ELSE 0 END) AS expired,
              SUM(CASE WHEN expiry_date >= DATE('now') THEN quantity ELSE 0 END) AS non_expired
            FROM Food_Listings;
        """
        st.dataframe(run_query(query))

    elif query_choice == "Top cities with food donations":
        query = """
            SELECT city, COUNT(f.food_id) AS donations
            FROM Providers p
            JOIN Food_Listings f ON p.provider_id = f.provider_id
            GROUP BY city
            ORDER BY donations DESC;
        """
        st.dataframe(run_query(query))

    elif query_choice == "Receivers by city":
        query = "SELECT city, COUNT(*) AS total_receivers FROM Receivers GROUP BY city;"
        st.dataframe(run_query(query))

    elif query_choice == "Average quantity per listing":
        query = "SELECT AVG(quantity) AS avg_quantity FROM Food_Listings;"
        st.dataframe(run_query(query))

    elif query_choice == "Meal type distribution":
        query = "SELECT meal_type, COUNT(*) AS total FROM Food_Listings GROUP BY meal_type;"
        st.dataframe(run_query(query))

    elif query_choice == "Food type distribution":
        query = "SELECT food_type, COUNT(*) AS total FROM Food_Listings GROUP BY food_type;"
        st.dataframe(run_query(query))

# Contacts
elif choice == "Contacts":
    st.header("Contact Information")

    tab = st.radio("View Contacts of", ["Providers", "Receivers"])

    if tab == "Providers":
        query = "SELECT name, contact, city FROM Providers;"
        st.dataframe(run_query(query))
    else:
        query = "SELECT name, contact, city FROM Receivers;"
        st.dataframe(run_query(query))

# CRUD 
elif choice == "CRUD":
    st.header("CRUD Operations")

    crud_table = st.selectbox("Select Table", ["Providers", "Receivers", "Food_Listings", "Claims"])
    crud_action = st.radio("Action", ["Add", "Update", "Delete"])

    if crud_table == "Providers":
        if crud_action == "Add":
            with st.form("add_provider"):
                pid = st.text_input("Provider ID")
                name = st.text_input("Name")
                ptype = st.text_input("Type")
                city = st.text_input("City")
                contact = st.text_input("Contact")
                submitted = st.form_submit_button("Add Provider")
                if submitted:
                    execute_query("INSERT INTO Providers (provider_id, name, provider_type, city, contact) VALUES (?,?,?,?,?)",
                                  (pid, name, ptype, city, contact))
                    st.success("Provider added successfully")

        elif crud_action == "Update":
            with st.form("update_provider"):
                pid = st.text_input("Provider ID to Update")
                name = st.text_input("New Name")
                submitted = st.form_submit_button("Update")
                if submitted:
                    execute_query("UPDATE Providers SET name=? WHERE provider_id=?", (name, pid))
                    st.success("Provider updated successfully")

        elif crud_action == "Delete":
            pid = st.text_input("Provider ID to Delete")
            if st.button("Delete"):
                execute_query("DELETE FROM Providers WHERE provider_id=?", (pid,))
                st.success("Provider deleted successfully")

    if crud_table == "Receivers":
        if crud_action == "Add":
            with st.form("add_receiver"):
                rid = st.text_input("Receiver ID")
                name = st.text_input("Name")
                rtype = st.text_input("Type")
                city = st.text_input("City")
                contact = st.text_input("Contact")
                submitted = st.form_submit_button("Add Receiver")
                if submitted:
                    execute_query("INSERT INTO Receivers (receiver_id, name, type, city, contact) VALUES (?,?,?,?,?)",
                                  (rid, name, rtype, city, contact))
                    st.success("Receiver added successfully")

        elif crud_action == "Update":
            with st.form("update_receiver"):
                rid = st.text_input("Receiver ID to Update")
                name = st.text_input("New Name")
                submitted = st.form_submit_button("Update")
                if submitted:
                    execute_query("UPDATE Receivers SET name=? WHERE receiver_id=?", (name, rid))
                    st.success("Receiver updated successfully")

        elif crud_action == "Delete":
            rid = st.text_input("Receiver ID to Delete")
            if st.button("Delete"):
                execute_query("DELETE FROM Receivers WHERE receiver_id=?", (rid,))
                st.success("Receiver deleted successfully")

    if crud_table == "Food_Listings":
        if crud_action == "Add":
            with st.form("add_food"):
                fid = st.text_input("Food ID")
                name = st.text_input("Food Name")
                qty = st.number_input("Quantity", min_value=1)
                expiry = st.date_input("Expiry Date")
                pid = st.text_input("Provider ID")
                ftype = st.text_input("Food Type")
                mtype = st.text_input("Meal Type")
                loc = st.text_input("Location")
                submitted = st.form_submit_button("Add Food")
                if submitted:
                    execute_query("INSERT INTO Food_Listings (food_id, food_name, quantity, expiry_date, provider_id, food_type, meal_type, location) VALUES (?,?,?,?,?,?,?,?)",
                                  (fid, name, qty, expiry, pid, ftype, mtype, loc))
                    st.success("Food listing added successfully")

        elif crud_action == "Update":
            with st.form("update_food"):
                fid = st.text_input("Food ID to Update")
                qty = st.number_input("New Quantity", min_value=1)
                submitted = st.form_submit_button("Update")
                if submitted:
                    execute_query("UPDATE Food_Listings SET quantity=? WHERE food_id=?", (qty, fid))
                    st.success("Food listing updated successfully")

        elif crud_action == "Delete":
            fid = st.text_input("Food ID to Delete")
            if st.button("Delete"):
                execute_query("DELETE FROM Food_Listings WHERE food_id=?", (fid,))
                st.success("Food listing deleted successfully")

    if crud_table == "Claims":
        if crud_action == "Add":
            with st.form("add_claim"):
                cid = st.text_input("Claim ID")
                fid = st.text_input("Food ID")
                rid = st.text_input("Receiver ID")
                status = st.text_input("Status")
                ts = st.text_input("Timestamp (YYYY-MM-DD HH:MM:SS)")
                submitted = st.form_submit_button("Add Claim")
                if submitted:
                    execute_query("INSERT INTO Claims (claim_id, food_id, receiver_id, status, timestamp) VALUES (?,?,?,?,?)",
                                  (cid, fid, rid, status, ts))
                    st.success("Claim added successfully")

        elif crud_action == "Update":
            with st.form("update_claim"):
                cid = st.text_input("Claim ID to Update")
                status = st.text_input("New Status")
                submitted = st.form_submit_button("Update")
                if submitted:
                    execute_query("UPDATE Claims SET status=? WHERE claim_id=?", (status, cid))
                    st.success("Claim updated successfully")

        elif crud_action == "Delete":
            cid = st.text_input("Claim ID to Delete")
            if st.button("Delete"):
                execute_query("DELETE FROM Claims WHERE claim_id=?", (cid,))
                st.success("Claim deleted successfully")
