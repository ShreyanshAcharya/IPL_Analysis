import streamlit as st
import db  # Import the database connection functions from db.py

# Import data analysis functions from queries.py
from queries import team_max_wins_by_venue, top_10_batsmen_2019, top_10_bowlers_2019

def user_dashboard():
    st.title("IPL Data Analysis Dashboard - User")

    st.sidebar.title("Menu")

    # Buttons for data analysis queries
    analysis_query = st.sidebar.radio("Select Analysis Query", ['team_max_wins_by_venue", "top_10_batsmen_2019", "top_10_bowlers_2019',"Batsman's Most Frequent Dismissal", "Best Batsman per Match",
                                                              "Top Bowlers as Batsmen", "Allrounders in a Match"])


    # Set a background image
    st.markdown(
        """
        <style>
        .reportview-container {
            background: url('https://example.com/your-background-image.jpg');
            background-size: cover;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Play background audio
    audio_file = open("background_audio.mp3", "rb")
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format="audio/mp3")

    st.sidebar.title("Menu")

    # Buttons for data analysis queries
    analysis_query = st.sidebar.radio("Select Analysis Query", ["Team's Most Wins by Venue", "Top 10 Batsmen in 2019", "Top 10 Bowlers in 2019"])

    if analysis_query == "Team's Most Wins by Venue":
        display_team_max_wins_by_venue()
    elif analysis_query == "Top 10 Batsmen in 2019":
        display_top_10_batsmen_2019()
    elif analysis_query == "Top 10 Bowlers in 2019":
        display_top_10_bowlers_2019()

def display_team_max_wins_by_venue():
    st.subheader("Team's Most Wins by Venue")
    
    # Call the data analysis function from queries.py to get results
    connection = db.create_db_connection()
    if connection:
        team_stadium_max_wins = team_max_wins_by_venue(connection)
        connection.close()
        # Display the results
        st.write("Results:")
        st.write(team_stadium_max_wins)
    else:
        st.error("Unable to connect to the database. Please try again later.")

def display_top_10_batsmen_2019():
    st.subheader("Top 10 Batsmen in 2019")
    
    # Call the data analysis function from queries.py to get results
    connection = db.create_db_connection()
    if connection:
        top_batsmen_2019 = top_10_batsmen_2019(connection)
        connection.close()
        # Display the results
        st.write("Results:")
        st.write(top_batsmen_2019)
    else:
        st.error("Unable to connect to the database. Please try again later.")

def display_top_10_bowlers_2019():
    st.subheader("Top 10 Bowlers in 2019")
    
    # Call the data analysis function from queries.py to get results
    connection = db.create_db_connection()
    if connection:
        top_bowlers_2019 = top_10_bowlers_2019(connection)
        connection.close()
        # Display the results
        st.write("Results:")
        st.write(top_bowlers_2019)
    else:
        st.error("Unable to connect to the database. Please try again later.")

def main():
    user_dashboard()

if __name__ == "__main__":
    main()
