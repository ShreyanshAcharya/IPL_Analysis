import psycopg2

def create_db_connection():
    try:
        # Replace with your database credentials
        conn = psycopg2.connect(
            dbname="database_name",
            user="username",
            password="password",
            host="host",
            port="port"
        )
        return conn
    except Exception as e:
        print(f"Database connection error: {str(e)}")
        return None

def close_db_connection(conn):
    if conn:
        conn.close()

def team_max_wins_by_venue(connection):
    try:
        cursor = connection.cursor()
        query = """
        SELECT team_name, venue, .......
        """
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result
    except Exception as e:
        print(f"Error in team_max_wins_by_venue: {str(e)}")
        return None

def runs_and_dismissals_for_match(connection, match_id):
    try:
        cursor = connection.cursor()
        query = f"""
        SELECT batsman_name, SUM(runs_scored) as total_runs, dismissal_method
        FROM match_details
        WHERE match_id = {match_id}
        GROUP BY batsman_name, dismissal_method
        """
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result
    except Exception as e:
        print(f"Error in runs_and_dismissals_for_match: {str(e)}")
        return None

def total_wickets_for_match(connection, match_id):
    try:
        cursor = connection.cursor()
        query = f"""
        SELECT SUM(wickets_taken) as total_wickets
        FROM bowler_stats
        WHERE match_id = {match_id}
        """
        cursor.execute(query)
        result = cursor.fetchone()
        cursor.close()
        return result[0] if result else 0
    except Exception as e:
        print(f"Error in total_wickets_for_match: {str(e)}")
        return 0

def top_10_batsmen_2019(connection):
    try:
        cursor = connection.cursor()
        query = """
        SELECT .......
        """
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result
    except Exception as e:
        print(f"Error in top_10_batsmen_2019: {str(e)}")
        return None

def top_10_bowlers_2019(connection):
    try:
        cursor = connection.cursor()
        query = """
        SELECT bowler_name......
        """
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result
    except Exception as e:
        print(f"Error in top_10_bowlers_2019: {str(e)}")
        return None

def toss_vs_victory(connection):
    try:
        cursor = connection.cursor()
        query = """
        SELECT toss_winner,..........
        """
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result
    except Exception as e:
        print(f"Error in toss_vs_victory: {str(e)}")
        return None

def update_data(connection) :
    try:
        cursor = connection.cursor()
        query = """
        SELECT toss_winner,..........
        """
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result
    except Exception as e:
        print(f"Error in toss_vs_victory: {str(e)}")
        return None

def delete_data(connection) :
    try:
        cursor = connection.cursor()
        query = """
        SELECT toss_winner,..........
        """
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result
    except Exception as e:
        print(f"Error in toss_vs_victory: {str(e)}")
        return None
        