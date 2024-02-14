import psycopg2

def create_db_connection():
    try:
        # Replace with your database credentials
        conn = psycopg2.connect(
            dbname="your_database_name",
            user="your_username",
            password="your_password",
            host="your_host",
            port="your_port"
        )
        return conn
    except Exception as e:
        print(f"Database connection error: {str(e)}")
        return None

def close_db_connection(conn):
    if conn:
        conn.close()

if __name__ == "__main__":
    # Test the database connection
    connection = create_db_connection()
    if connection:
        print("Database connection successful!")
        close_db_connection(connection)
