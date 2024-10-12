import duckdb
import os

dir1 = 'Fitabase Data 3.12.16-4.11.16'
dir2 = 'Fitabase Data 4.12.16-5.12.16'

with duckdb.connect('fitbit.ddb') as conn:
    def load_csv_to_duckdb(directory):
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.csv'):
                    file_path = os.path.join(root, file)
                    table_name = os.path.splitext(file)[0]
                    print(f"Loading {file_path} into table '{table_name}'")

                    table_exists_query = f"""
                        SELECT COUNT(*)
                        FROM information_schema.tables
                        WHERE table_name = '{table_name}'
                    """
                    table_exists = conn.execute(table_exists_query).fetchone()[0]

                    if table_exists:
                        query = f"""
                            INSERT INTO {table_name} 
                            SELECT * FROM read_csv_auto('{file_path}')
                        """
                    else:
                        query = f"""
                            CREATE TABLE {table_name} AS
                            SELECT * FROM read_csv_auto('{file_path}')
                        """
                    
                    try:
                        conn.execute(query)
                    except Exception as e:
                        print(f"Error loading {file_path}: {e}")

    load_csv_to_duckdb(dir1)
    load_csv_to_duckdb(dir2)

    tables_query = "SHOW TABLES"
    tables = conn.execute(tables_query).fetchall()

    print("\nDatabase contains the following tables:\n")
    for table in tables:
        table_name = table[0]
        column_query = f"DESCRIBE {table_name}"
        row_count_query = f"SELECT COUNT(*) FROM {table_name}"

        columns = conn.execute(column_query).fetchall()
        row_count = conn.execute(row_count_query).fetchone()[0]

        print(f"Table: {table_name}")
        print(f"  Total Rows: {row_count}")
        print("  Columns:")
        for col in columns:
            print(f"    {col[0]} ({col[1]})")
