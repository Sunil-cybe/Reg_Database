import streamlit as st
import sqlite3
from sqlite3 import Error

#checking connection with database
# Function to create a connection to the SQLite database
def create_connection():
    connection = None
    try:
        connection = sqlite3.connect('registration.db')
    except Error as e:
        st.error(f"Error: {e}")
    return connection

# Create table if not exits 
def create_table(connection):
    create_table_sql = """
        CREATE TABLE IF NOT EXISTS Registration (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Name VARCHAR(255) NOT NULL,
            Email VARCHAR(255) NOT NULL,
            DateOfBirth DATE,
            CONSTRAINT UC_Email UNIQUE (Email)
        );
    """
    try:
        cursor = connection.cursor()
        cursor.execute(create_table_sql)
    except Error as e:
        st.error(f"Error: {e}")

#Inert the record into the table
def create_record(connection, name, email, dob):
    insert_record_sql = """
        INSERT INTO Registration (Name, Email, DateOfBirth)
        VALUES (?, ?, ?);
    """
    try:
        cursor = connection.cursor()
        cursor.execute(insert_record_sql, (name, email, dob))
        connection.commit()
    except Error as e:
        st.error(f"Error: {e}")

# Dispalying the records from the table.
def read_records(connection):
    select_records_sql = "SELECT * FROM Registration;"
    try:
        cursor = connection.cursor()
        cursor.execute(select_records_sql)
        records = cursor.fetchall()
        return records
    except Error as e:
        st.error(f"Error: {e}")
        return None

# Updating the table
def update_record(connection, record_id, new_name, new_email, new_dob):
    update_record_sql = """
        UPDATE Registration
        SET Name = ?, Email = ?, DateOfBirth = ?
        WHERE ID = ?;
    """
    try:
        cursor = connection.cursor()
        cursor.execute(update_record_sql, (new_name, new_email, new_dob, record_id))
        connection.commit()
        if cursor.rowcount > 0:
            st.success("Record deleted successfully!")
        else:
            st.warning("Record not found.")
    except Error as e:
        st.error(f"Error: {e}")

# Delete the record from the table
def delete_record(connection, record_id):
    delete_record_sql = "DELETE FROM Registration WHERE ID = ?;"
    try:
        cursor = connection.cursor()
        cursor.execute(delete_record_sql, (record_id,))
        connection.commit()

        if cursor.rowcount > 0:
            st.success("Record deleted successfully!")
        else:
            st.warning("Record not found.")

    except Error as e:
        st.error(f"Error: {e}")

def main():
    st.title("Registration System")

    menu_option = st.sidebar.radio("Select Operation", ["Create Record", "Update Record", "Delete Record","Read Records"])

   
    if menu_option == "Create Record":
        st.header("Create Record")
        name = st.text_input("Enter your name:")
        email = st.text_input("Enter your email:")
        dob = st.date_input("Enter your date of birth:")

        # Button to submit the form
        if st.button("Submit"):
            # Create a connection to the database
            connection = create_connection()

            if connection:
                # Create the Registration table if not exists
                create_table(connection)

                # Insert the record into the Registration table
                create_record(connection, name, email, dob)

                # Display success message
                st.success("Record created successfully!")

                # Close the connection
                connection.close()
            else:
                st.error("Unable to connect to the database.")

    elif menu_option == "Read Records":
        st.header("Read Records")
        # Display section to show values present in the database
        connection = create_connection()
        if connection:
            records = read_records(connection)
            if records:
                for record in records:
                    st.write(record)
            else:
                st.info("No records found.")
            connection.close()

    elif menu_option == "Update Record":
        st.header("Update Record")
        # Input fields for user to enter update information
        record_id = st.number_input("Enter the ID of the record to update:",value=0)
        new_name = st.text_input("Enter the new Name:")
        new_email = st.text_input("Enter the new Email:")
        new_dob = st.date_input("Enter the new Date of Birth:")

        # Button to update the record
        if st.button("Update"):
            # Create a connection to the database
            connection = create_connection()

            if connection:
                # Update the record in the Registration table
                update_record(connection, record_id, new_name, new_email, new_dob)
              
                connection.close()
            else:
                st.error("Unable to connect to the database.")

    elif menu_option == "Delete Record":
        st.header("Delete Record")
        # Input fields for user to enter delete information
        record_id_to_delete = st.number_input("Enter the ID of the record to delete:",value = 0,step = 1)

        # Button to delete the record
        if st.button("Delete"):
            # Create a connection to the database
            connection = create_connection()

            if connection:
                # Delete the record from the Registration table
                delete_record(connection, record_id_to_delete)

                # Close the connection
                connection.close()
            else:
                st.error("Unable to connect to the database.")

if __name__ == "__main__":
    main()
