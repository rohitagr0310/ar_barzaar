import sqlite3
import csv

def update_database(csv_file, db_file, table_name, column_name, id_column):
    # Connect to the database
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    with open(csv_file, 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            record_id = row[id_column]
            new_value = row[column_name]
            # Update the specified column for the matching record ID
            cursor.execute(f"UPDATE {table_name} SET image = ? WHERE {id_column} = ?", (new_value, record_id))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

# Usage example
csv_file = 'update.csv'  # Replace with your CSV file path
db_file = 'database.db'  # Replace with your SQLite database file path
table_name = 'products'  # Replace with your table name
column_name = 'new_image'  # Replace with the column you want to update
id_column = 'productId'  # Replace with the column containing the unique IDs

update_database(csv_file, db_file, table_name, column_name, id_column)
