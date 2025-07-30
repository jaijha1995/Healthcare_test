import psycopg2
import tkinter as tk
from tkinter import messagebox

def migrate_data():
    source_postgres_hostname = source_postgres_host_entry.get()
    source_postgres_username = source_postgres_user_entry.get()
    source_postgres_password = source_postgres_password_entry.get()
    source_postgres_database_name = source_postgres_db_entry.get()

    target_postgres_hostname = target_postgres_host_entry.get()
    target_postgres_username = target_postgres_user_entry.get()
    target_postgres_password = target_postgres_password_entry.get()
    target_postgres_database_name = target_postgres_db_entry.get()

    try:
        # Connect to source PostgreSQL database
        source_postgres_connection = psycopg2.connect(
            dbname=source_postgres_database_name,
            user=source_postgres_username,
            password=source_postgres_password,
            host=source_postgres_hostname
        )
        source_postgres_cursor = source_postgres_connection.cursor()
        
        table_name = table_name_entry.get()
        source_postgres_cursor.execute("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = %s", (table_name,))
        postgres_table_schema = source_postgres_cursor.fetchall()

        # Connect to target PostgreSQL database
        target_postgres_connection = psycopg2.connect(
            dbname=target_postgres_database_name,
            user=target_postgres_username,
            password=target_postgres_password,
            host=target_postgres_hostname
        )
        target_postgres_cursor = target_postgres_connection.cursor()

        target_create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ("
        for column in postgres_table_schema:
            column_name = column[0]
            column_type = column[1]
            target_create_table_query += f"{column_name} {column_type}, "
        target_create_table_query = target_create_table_query[:-2]
        target_create_table_query += ")"
        target_postgres_cursor.execute(target_create_table_query)

        source_postgres_cursor.execute(f"SELECT * FROM {table_name}")
        source_postgres_rows = source_postgres_cursor.fetchall()

        target_insert_query = f"INSERT INTO {table_name} VALUES ({', '.join(['%s']*len(postgres_table_schema))})"
        for row in source_postgres_rows:
            target_postgres_cursor.execute(target_insert_query, row)

        target_postgres_connection.commit()

        messagebox.showinfo("Success", "Data inserted into target PostgreSQL database")

    except psycopg2.Error as e:
        messagebox.showerror("Error", f"Error connecting to PostgreSQL database: {e}")

    finally:
        if 'source_postgres_connection' in locals():
            source_postgres_cursor.close()
            source_postgres_connection.close()

        if 'target_postgres_connection' in locals():
            target_postgres_cursor.close()
            target_postgres_connection.close()

root = tk.Tk()
root.title("PostgreSQL to PostgreSQL Migration")

# Source PostgreSQL Server Credentials
source_postgres_host_label = tk.Label(root, text="Source PostgreSQL Host:")
source_postgres_host_label.grid(row=0, column=0)
source_postgres_host_entry = tk.Entry(root)
source_postgres_host_entry.grid(row=0, column=1)

source_postgres_user_label = tk.Label(root, text="Source PostgreSQL User:")
source_postgres_user_label.grid(row=1, column=0)
source_postgres_user_entry = tk.Entry(root)
source_postgres_user_entry.grid(row=1, column=1)

source_postgres_password_label = tk.Label(root, text="Source PostgreSQL Password:")
source_postgres_password_label.grid(row=2, column=0)
source_postgres_password_entry = tk.Entry(root, show="*")
source_postgres_password_entry.grid(row=2, column=1)

source_postgres_db_label = tk.Label(root, text="Source PostgreSQL Database:")
source_postgres_db_label.grid(row=3, column=0)
source_postgres_db_entry = tk.Entry(root)
source_postgres_db_entry.grid(row=3, column=1)

# Target PostgreSQL Server Credentials
target_postgres_host_label = tk.Label(root, text="Target PostgreSQL Host:")
target_postgres_host_label.grid(row=4, column=0)
target_postgres_host_entry = tk.Entry(root)
target_postgres_host_entry.grid(row=4, column=1)

target_postgres_user_label = tk.Label(root, text="Target PostgreSQL User:")
target_postgres_user_label.grid(row=5, column=0)
target_postgres_user_entry = tk.Entry(root)
target_postgres_user_entry.grid(row=5, column=1)

target_postgres_password_label = tk.Label(root, text="Target PostgreSQL Password:")
target_postgres_password_label.grid(row=6, column=0)
target_postgres_password_entry = tk.Entry(root, show="*")
target_postgres_password_entry.grid(row=6, column=1)

target_postgres_db_label = tk.Label(root, text="Target PostgreSQL Database:")
target_postgres_db_label.grid(row=7, column=0)
target_postgres_db_entry = tk.Entry(root)
target_postgres_db_entry.grid(row=7, column=1)

# Table Name
table_name_label = tk.Label(root, text="Table Name:")
table_name_label.grid(row=8, column=0)
table_name_entry = tk.Entry(root)
table_name_entry.grid(row=8, column=1)

# Button to initiate migration
migrate_button = tk.Button(root, text="Migrate Data", command=migrate_data)
migrate_button.grid(row=9, columnspan=2)

root.mainloop()