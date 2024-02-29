import streamlit as st
import pandas as pd
import pickle
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, func, text
from sqlalchemy.orm import sessionmaker
import matplotlib.pyplot as plt
from tomlkit import boolean


# Set page configuration
st.set_page_config(
    page_title="IPL Dashboard",
    page_icon="🏏",
    layout="wide",
)
st.title('🏏IPL Dashboard🏏')


db_params = {
    'host': 'localhost',
    'database': 'IPL_analysis',
    'user': 'postgres',
    'password': 'Ropa',
}

engine = create_engine(f"postgresql+psycopg2://{db_params['user']}:{db_params['password']}@{db_params['host']}/{db_params['database']}")


Base = declarative_base()

class Deliveries(Base):
    __tablename__ = 'deliveries'

    id = Column(Integer, primary_key=True)
    match_id = Column(Integer, ForeignKey('matches.match_id'))
    overs = Column(Integer)
    ballnumber = Column(Integer)
    batter = Column(String)
    bowler = Column(String)
    nonstriker = Column(String)
    extratype = Column(String)
    batsmanrun = Column(Integer)
    extrasrun = Column(Integer)
    totalrun = Column(Integer)
    nonboundary = Column(Integer)
    battingteamid = Column(Integer)
    isWicketdelivery=Column(Integer, server_default=text('0'))
    playerout=Column(String)
    fieldersinvolved=Column(String)
    kind=Column(String)

class Match(Base):
    __tablename__ = 'matches'

    match_id = Column(Integer, primary_key=True)
    season = Column(Integer)
    matchnumber = Column(Integer)
    venueid = Column(Integer, ForeignKey('venues.venueid'))
    tosswinner = Column(String)
    tossdecision = Column(String)
    winningteam = Column(String)
    wonby = Column(String)
    margin = Column(String)
    playerofthematch = Column(String)
    umpire1id = Column(Integer, ForeignKey('umpires.umpireid'))
    umpire2id = Column(Integer, ForeignKey('umpires.umpireid'))

    # Define relationships
    deliveries = relationship('Deliveries', backref='match')

class Team(Base):
    __tablename__ = 'teams'

    teamid = Column(Integer, primary_key=True)
    teamname = Column(String)

class Umpire(Base):
    __tablename__ = 'umpires'

    umpireid = Column(Integer, primary_key=True)
    umpirename = Column(String)

class Venue(Base):
    __tablename__ = 'venues'

    venueid = Column(Integer, primary_key=True)
    venuename = Column(String)
    city=Column(String)


Session = sessionmaker(bind=engine)
session = Session()

def load_player_details(player):
    st.subheader(player)

def imp_info_of_batsman(player_name):
   
    query = text(
        f"""
        SELECT matchid, SUM(batsmanrun) AS "100S"
        FROM deliveries
        WHERE batter = :player_name
        GROUP BY matchid
        HAVING SUM(batsmanrun) BETWEEN 100 AND 199
        """
    )
    df9 = pd.read_sql(query, engine, params={"player_name": player_name})
    
    if df9.empty:
        st.markdown("- <span style='color:red; font-weight:bold;'>NO 100s</span>", unsafe_allow_html=True)
    else:
        st.markdown(
            f"- <span style='color:blue'>STADIUM WISE CENTURY RECORDS OF {player_name}  ", 
            unsafe_allow_html=True
        )
        df10 = df9.groupby('venues')['100S'].count().reset_index()
        df10.rename(columns={'100S': 'NUMBER OF 100s'}, inplace=True)

        def highlight_rows(row):
            background_color = 'green' if row['NUMBER OF 100s'] >= 3 else 'yellow'
            return ['background-color: {}'.format(background_color)] * len(row)

        st.dataframe(df10.style.apply(highlight_rows, axis=1))

    def imp_info_of_batsman_50s(session, player_name):
    # Query to get the total runs scored by the player in each match
       total_runs_query = (
        session.query(Deliveries.match_id, func.sum(Deliveries.batsmanrun).label('50S'))
        .filter(Deliveries.batter == player_name)
        .group_by(Deliveries.match_id)
        .having(func.sum(Deliveries.batsmanrun).between(50, 99))
        .subquery()
    )

    # Join the total_runs_query with the Venue table to get the venue information
       query = (
        session.query(total_runs_query.c.match_id, Venue.venues, total_runs_query.c['50S'])
        .join(Venue, total_runs_query.c.match_id == Venue.match_id)
        .all()
    )

    # Convert the result to a DataFrame for display
       df_50s = pd.DataFrame(query, columns=['match_id', 'VENUE', '50S'])

       if df_50s.empty:
        st.markdown("- <span style='color:red; font-weight:bold;'>NO 50s</span>", unsafe_allow_html=True)
       else:
        st.markdown(
            f"- <span style='color:blue'>STADIUM WISE HALF CENTURY RECORDS OF {player_name}</span>",
            unsafe_allow_html=True
        )

        df_50s_highlighted = df_50s.style.apply(highlight_rows, axis=1)
        st.dataframe(df_50s_highlighted)

# Function to highlight rows based on the count of 50s
def highlight_rows(row):
    background_color = 'green' if row['50S'] >= 10 else 'yellow'
    return ['background-color: {}'.format(background_color)] * len(row)



def imp_info_of_bowler(player_name):
  
    query = text(
        f"""
        SELECT bowler
        FROM deliveries
        WHERE bowler = :player_name  
        GROUP BY  bowler
        
        """
    )
    df_pcap = pd.read_sql(query, engine, params={"player_name": player_name})

    if not df_pcap.empty:
        st.markdown(
            f"- <span style='color:purple; font-weight:bold;'>Pcap cap holder details of {player_name}</span>",
            unsafe_allow_html=True
        )

        def highlight_player(row):
            if row['bowler'] == player_name:
                return ['background-color:purple'] * len(row)
            else:
                return [''] * len(row)

        styled_df = df_pcap.style.apply(highlight_player, axis=1)
        st.dataframe(styled_df)

    # Stadium-wise at least 3 wickets taken
    st.markdown(
        f"- <span style='color:green; font-weight:bold;'>Stadium wise at least 3 wickets taken by {player_name}</span>",
        unsafe_allow_html=True
    )
    
    st.write(" ")
    st.write(" ")
    
    # Best 5 records against batsman
    st.markdown(
        f"- <span style='color:green; font-weight:bold;'>{player_name} best 5 records against batsman </span>",
        unsafe_allow_html=True
    )
   
    query_records = text(
        f"""
        SELECT batter, SUM(batsmanrun) AS "Batter_run"
        FROM deliveries
        WHERE bowler = :player_name
        GROUP BY batter
        ORDER BY "Batter_run" DESC 
        LIMIT 5
        """
    )
    df_records = pd.read_sql(query_records, engine, params={"player_name": player_name})

    background_color = 'yellow'
    # Function to apply background color to the DataFrame cells
    def apply_background_color(row):
        return [f'background-color: {background_color}' for _ in row]

    # Apply styling to the DataFrame
    styled_df = df_records.style.apply(apply_background_color, axis=1)

    # Convert Styler object to HTML
    styled_html = styled_df.to_html(classes=['styled-table'], escape=False, index=False)

    # Display the DataFrame with the background color applied
    st.markdown(styled_html, unsafe_allow_html=True)

def query_max_wins_venue(team):
    # Implement the query for finding the stadium where the team has won the maximum number of matches
    query = text(f"""SELECT
        t.teamname AS team,
        v.venuename AS stadium,
        COUNT(*) AS wins
    FROM
        matches m
    JOIN
        teams t ON m.winningteam = t.teamid
    JOIN
        venues v ON m.venueid = v.venueid
    WHERE
        t.teamname = :team
    GROUP BY
        t.teamname, v.venuename
    ORDER BY
        t.teamname, COUNT(*) DESC
    """)
    result = engine.execute(query, team=team)
    data = result.fetchall()


    # Create a DataFrame from the query result
    df = pd.DataFrame(data, columns=['Team', 'Venue', 'Wins'])
    print(df)
    # Plot a bar chart
    st.set_option('deprecation.showPyplotGlobalUse', False)
    plt.figure(figsize=(12, 8))  # Increase the figure size
    plt.bar(df['Venue'], df['Wins'])
    
    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45, ha='right')  # Use plt.xticks instead of ax.xticks

    plt.title(f'Max Wins Venue for {team}')
    plt.xlabel('Venue')
    plt.ylabel('Number of Wins')
    st.pyplot()

def query_runs_by_batsman(match_id):
    query = text(f"""SELECT
        batter AS batsman,
        SUM(batsmanrun) AS total_runs,
        MAX(kind) AS dismissalmethod
    FROM
        deliveries
    WHERE
        matchid = :match_id
    GROUP BY
        batter, kind
    """)
    result = engine.execute(query, match_id=match_id)
    data = result.fetchall()

    # Create a DataFrame from the query result
    df = pd.DataFrame(data, columns=['Batsman', 'Total Runs', 'Dismissal Method'])
    
    # Display the DataFrame in Streamlit
    st.write(df)

# Plot a bar chart
    st.set_option('deprecation.showPyplotGlobalUse', False)
    plt.figure(figsize=(10, 6))
    plt.bar(df['Batsman'], df['Total Runs'])
    plt.title(f'Total Runs by Batsman in Match {match_id}')
    plt.xlabel('Batsman')
    plt.ylabel('Total Runs')
    plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better visibility
    st.pyplot()

# Function to query total wickets taken by all bowlers in a match
def query_wickets_in_match(match_id):
    query = text(f"""SELECT
        bowler,
        COUNT(*) AS total_wickets
    FROM
        deliveries
    WHERE
        matchid = :match_id
        AND iswicketdelivery = true
    GROUP BY
        bowler
    """)
    result = engine.execute(query, match_id=match_id)
    data = result.fetchall()

    # Create a DataFrame from the query result
    df = pd.DataFrame(data, columns=['Bowler', 'Total Wickets'])
    
    # Display the DataFrame in Streamlit
    st.write(df)

    # Visualize the data using a bar chart
    st.set_option('deprecation.showPyplotGlobalUse', False)
    plt.figure(figsize=(10, 6))
    plt.bar(df['Bowler'], df['Total Wickets'])
    plt.title(f'Total Wickets by Bowlers in Match {match_id}')
    plt.xlabel('Bowler')
    plt.ylabel('Total Wickets')
    plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better visibility
    st.pyplot()

def query_top_bowlers_by_season(selected_season):
    query = text(f"""SELECT
        bowler,
        COUNT(*) AS total_wickets
    FROM
        deliveries d
    JOIN
        matches m ON d.matchid = m.matchid
    WHERE
        m.season = :selected_season
        AND d.iswicketdelivery = true
    GROUP BY
        bowler
    ORDER BY
        total_wickets DESC
    LIMIT 10
    """)
    result = engine.execute(query, selected_season=selected_season)
    data = result.fetchall()
    return data
def display_top_bowlers_info(top_bowlers_data):
    # Create a DataFrame from the query result
    df = pd.DataFrame(top_bowlers_data, columns=['Bowler', 'Total Wickets'])
    
    # Display the DataFrame in Streamlit
    st.write(df)

    # Visualize the data using a bar chart
    st.set_option('deprecation.showPyplotGlobalUse', False)
    plt.figure(figsize=(10, 6))
    plt.bar(df['Bowler'], df['Total Wickets'])
    plt.title(f'Top 10 Bowlers in {selected_season}')
    plt.xlabel('Bowler')
    plt.ylabel('Total Wickets')
    plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better visibility
    st.pyplot()
  
def query_top_batters_by_season(selected_season):
    query = text(f"""SELECT
        batter AS Batsman,
        SUM(totalrun) AS TotalRuns
    FROM
        deliveries d
    JOIN
        matches m ON d.matchid = m.matchid
    WHERE
        m.season = :selected_season
    GROUP BY
        batter
    ORDER BY
        TotalRuns DESC
    LIMIT
        10;
    """)
    result = engine.execute(query, selected_season=selected_season)
    data = result.fetchall()
    return data

def display_top_batters_info(top_batters_data):
    # Create a DataFrame from the query result
    df = pd.DataFrame(top_batters_data, columns=['Batsman', 'Total Runs'])
    
    # Display the DataFrame in Streamlit
    st.write(df)

    # Visualize the data using a bar chart
    st.set_option('deprecation.showPyplotGlobalUse', False)
    plt.figure(figsize=(10, 6))
    plt.bar(df['Batsman'], df['Total Runs'])
    plt.title(f'Top 10 Batsmen in {selected_season}')
    plt.xlabel('Batsman')
    plt.ylabel('Total Runs')
    plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better visibility
    st.pyplot()
def query_toss_and_victory():
    query = text("""
        SELECT
            tosswinner AS Team,
            COUNT(*) AS TotalMatches,
            SUM(CASE WHEN winningteam = tosswinner THEN 1 ELSE 0 END) AS MatchesWon
        FROM
            matches
        WHERE
            tosswinner IS NOT NULL
            AND winningteam IS NOT NULL
        GROUP BY
            tosswinner
    """)
    result = engine.execute(query)
    data = result.fetchall()
    return data

team_id_name_mapping = {
    
    1:"Rajasthan Royals",
    2:"Royal Challengers Bangalore",
    3:"Sunrisers Hyderabad",
    4:"Delhi Capitals",
    5:"Chennai Super Kings",
    6:"Gujarat Titans",
    7:"Lucknow Super Giants",
    8:"Kolkata Knight Riders",
    9:"Punjab Kings",
    10:"Mumbai Indians",
    11:"Rising Pune Supergiant",
    12:"Gujarat Lions",
    13:"Pune Warriors",
    14:"Deccan Chargers",
    15:"Kochi Tuskers Kerala"
    }

def visualize_toss_and_victory(data):
    # Create a DataFrame from the query result
    df = pd.DataFrame(data, columns=['Team', 'Toss Wins', 'Match Wins'])


    # Visualize the data using a bar chart
    fig, ax = plt.subplots(figsize=(10, 6))
    df.plot(kind='bar', x='Team', y=['Toss Wins', 'Match Wins'], ax=ax, color=['magenta', 'lightgreen'])
    ax.set_title('Toss Wins vs. Match Wins')
    ax.set_xlabel('Team')
    ax.set_ylabel('Count')
    ax.legend(["Toss Wins", "Match Wins"])
    st.pyplot(fig)


def query_top_batsmen_by_year_and_match(selected_year, selected_match_id):
    query = text(f"""
        SELECT batter AS Batsman, SUM(totalrun) AS TotalRuns
        FROM deliveries d
        JOIN matches m ON d.matchid = m.matchid
        WHERE m.season = :selected_year AND m.matchid = :selected_match_id
        GROUP BY batter
        ORDER BY TotalRuns DESC
        LIMIT 10
    """)
    result = engine.execute(query, selected_year=selected_year, selected_match_id=selected_match_id)
    return result.fetchall()

# Function to display the top 10 batsmen and visualize the data
def display_top_batsmen_by_year_and_match(top_batsmen_data):
    # Convert the list of tuples to a DataFrame
    top_batsmen_df = pd.DataFrame(top_batsmen_data, columns=['Batsman', 'TotalRuns'])

    # Display the top 10 batsmen
    st.table(top_batsmen_df)

    # Visualize the data using a bar chart
    st.set_option('deprecation.showPyplotGlobalUse', False)
    plt.figure(figsize=(10, 6))
    plt.bar(top_batsmen_df['Batsman'], top_batsmen_df['TotalRuns'])
    plt.title(f'Top 10 Batsmen')
    plt.xlabel('Batsman')
    plt.ylabel('Total Runs')
    plt.xticks(rotation=45, ha='right')
    st.pyplot()

def query_top_bowlers_as_batsmen(selected_year):
    query = text(f"""
        SELECT d.bowler, SUM(d.batsmanrun) AS total_runs
        FROM deliveries d
        JOIN matches m ON d.matchid = m.matchid
        WHERE m.season = :selected_year AND d.bowler IS NOT NULL
        GROUP BY d.bowler
        ORDER BY total_runs DESC
        LIMIT 5
    """)
    result = engine.execute(query, selected_year=selected_year)
    return result.fetchall()

# Function to display the top 5 bowlers with highest runs scored as batsmen and visualize the data
def display_top_bowlers_as_batsmen(top_bowlers_data):
    # Display the top 5 bowlers
    st.table(top_bowlers_data)

    # Visualize the data using a bar chart
    plt.figure(figsize=(10, 6))
    plt.bar(top_bowlers_data['Bowler'], top_bowlers_data['TotalRuns'])
    plt.title(f'Top 5 Bowlers with Highest Runs Scored as Batsmen')
    plt.xlabel('Bowler')
    plt.ylabel('Total Runs')
    st.pyplot()



def display_top_bowlers_as_batsmen(top_bowlers_data):
    # Display the top bowlers
    st.table(top_bowlers_data)

    # Visualize the data using a bar chart
    plt.figure(figsize=(10, 6))
    plt.bar(top_bowlers_data['Player'], top_bowlers_data['AllRoundersCount'])
    plt.title('Top Bowlers as Batsmen')
    plt.xlabel('Player')
    plt.ylabel('Count')
    st.pyplot()


def query_all_rounders(match_id):
    query = text(f"""
        SELECT player, COUNT(*) as all_rounders_count
        FROM (
            SELECT player
            FROM deliveries
            WHERE matchid = :match_id AND batsman IS NOT NULL AND bowler IS NOT NULL
            GROUP BY player
            HAVING COUNT(DISTINCT CASE WHEN batsman IS NOT NULL THEN 1 END) > 0
                AND COUNT(DISTINCT CASE WHEN bowler IS NOT NULL THEN 1 END) > 0
        ) AS all_rounders
        GROUP BY player
    """)
    result = engine.execute(query, match_id=match_id)
    return result.fetchall()

def display_all_rounders(all_rounders_data):
    # Display the all-rounders
    st.table(all_rounders_data)

    # Visualize the data using a bar chart
    plt.figure(figsize=(10, 6))
    plt.bar(all_rounders_data['Player'], all_rounders_data['AllRoundersCount'])
    plt.title('All-Rounders in the Match')
    plt.xlabel('Player')
    plt.ylabel('Count')
    st.pyplot()

class Bowler(Exception):
    def __init__(self, bowler, session):
        self.player = bowler
        self.session = session

    def bowler_details(self):
        col1, col2, col3 = st.columns(3, gap='large')

        # Query for balls delivered
       # Query for balls delivered
        query_delivered = text(
            f"""
            SELECT COUNT(*) AS balls_delivered
            FROM deliveries
            WHERE bowler = :player_name
            """
        )
        balls_delivered = pd.read_sql(query_delivered, engine, params={"player_name": self.player})['balls_delivered'].iloc[0]


        with col1:
            st.markdown(
                f"- <span style='color:blue'>Balls Delivered:</span> <span style='color:green'> {balls_delivered}</span>",
                unsafe_allow_html=True
            )

        st.divider()



class Batsman(Exception):
    def __init__(self, batsman, session):
        self.player = batsman
        self.session = session

    def batsman_details(self):
        col1, col2, col3 = st.columns(3, gap='large')

        # Query for total runs
        runs = self.session.query(func.sum(Deliveries.batsmanrun)). \
            filter(Deliveries.batter == self.player).scalar()

        # Query for total 50s and 100s
        df9 = pd.read_sql(
            f"""
            SELECT season, SUM(batsmanrun) AS total_runs
            FROM deliveries
            JOIN matches ON deliveries.matchid = matches.matchid
            WHERE batter = '{self.player}'
            GROUP BY season
            """,
            self.session.bind
        )

        total_50s = df9[(df9.total_runs >= 50) & (df9.total_runs < 100)].count().loc['total_runs']
        total_100s = df9[(df9.total_runs >= 100) & (df9.total_runs < 200)].count().loc['total_runs']

        # Query for total fours and sixes
        total_fours = self.session.query(func.count()). \
            filter(Deliveries.batter == self.player, Deliveries.batsmanrun == 4).scalar()
        total_sixes = self.session.query(func.count()). \
            filter(Deliveries.batter == self.player, Deliveries.batsmanrun == 6).scalar()

        # Query for against which bowler the batsman got out most number of times
        most_out_bowler_data = self.query_most_out_against_bowler(self.player)

        with col1:
            st.markdown(
                f"- <span style='color:blue'>Total number of 4s :</span> <span style='color:green ; font-weight:bold'> "
                f"{total_fours}</span>",
                unsafe_allow_html=True)
            st.markdown(
                f"- <span style='color:blue'>Total number of 6s :</span> <span style='color:green ; font-weight:bold'> "
                f"{total_sixes}</span>",
                unsafe_allow_html=True)
            st.markdown(
                f"- <span style='color:blue'>Total number of 50s :</span> <span style='color:green ; font-weight:bold'> "
                f"{total_50s}</span>",
                unsafe_allow_html=True)
            st.markdown(
                f"- <span style='color:blue'>Total number of 100s :</span> <span style='color:green ; font-weight:bold'> "
                f"{total_100s}</span>",
                unsafe_allow_html=True)
            st.markdown(
                f"- <span style='color:blue'>Most times out against :</span> <span style='color:green ; font-weight:bold'> "
                f"{most_out_bowler_data['bowler']} ({most_out_bowler_data['num_outs']} times)</span>",
                unsafe_allow_html=True)
        st.divider()

    def query_most_out_against_bowler(self, batsman_name):
        query = text(f"""SELECT
            bowler,
            COUNT(*) AS num_outs
        FROM
            deliveries
        WHERE
            batter = :batsman_name
            AND kind IS NOT NULL
        GROUP BY
            bowler
        ORDER BY
            num_outs DESC
        LIMIT 1
        """)
        result = self.session.execute(query, {"batsman_name": batsman_name})  # Corrected line
        data = result.fetchone()
        return data
    
    
    

# The rest of your Streamlit code goes here
st.sidebar.title('Select One Option')
select = st.sidebar.selectbox('Statistics & Insights/More info/Win Prediction', ['Statistics & Insights',  'More info','Win Prediction' ])
if select == 'Statistics & Insights':
    option = st.sidebar.selectbox('Batsman/Bowler', ['Batsman', 'Bowler'])

    if option == 'Batsman':
        query_strikers = text("SELECT DISTINCT batter FROM deliveries")
        result = engine.execute(query_strikers)
        batsmen = result.fetchall()
        batsmen = [batsman[0] for batsman in batsmen]

        # Select box for choosing batsman
        selected_batsman = st.sidebar.selectbox('Select Batsman', sorted(batsmen))
        btn1 = st.sidebar.button('Find Details')

        # Initialize btn1_state if not present in session_state
        if "btn1_state" not in st.session_state:
            st.session_state.btn1_state = False

        if btn1 or st.session_state.btn1_state:
            st.session_state.btn1_state = True
            load_player_details(selected_batsman)

            # Pass the session to the Batsman constructor
            batsman_obj = Batsman(selected_batsman, session)  # <-- Pass the session object

            batsman_obj.batsman_details()

            st.write('Wants to know some valuable records!!')
            btn3_placeholder = st.empty()
            btn3 = btn3_placeholder.button("Show Information")

            if btn3:
                imp_info_of_batsman(batsman_obj.player)
                btn3_placeholder.empty()

    else:
        
        query_bowlers = text("SELECT DISTINCT bowler FROM deliveries")
        result = engine.execute(query_bowlers)
        bowlers = result.fetchall()
        bowlers = [bowler[0] for bowler in bowlers]

        # Select box for choosing bowler
        selected_bowler = st.sidebar.selectbox('Select Bowler', sorted(bowlers))
        btn2 = st.sidebar.button('Find Details')

        # Initialize btn2_state if not present in session_state
        if "btn2_state" not in st.session_state:
            st.session_state.btn2_state = False

        if btn2 or st.session_state.btn2_state:
            st.session_state.btn2_state = True
            load_player_details(selected_bowler)
            
            # Pass the session to the Bowler constructor
            bowler_obj = Bowler(selected_bowler, session)  # <-- Pass the session object

            bowler_obj.bowler_details()

            st.write('Wants to know some valuable records!!')
            btn4_placeholder = st.empty()
            btn4 = btn4_placeholder.button("Show Information")
            if btn4:
                imp_info_of_bowler(bowler_obj.player)
                btn4_placeholder.empty()

elif select == 'Win Prediction':
    with open('pipeline (2).pkl', 'rb') as file:
        loaded_pipeline = pickle.load(file)
    col1, col2, col3 = st.columns(3)
    batting_team = ['Kolkata Knight Riders', 'Sunrisers Hyderabad',
       'Chennai Super Kings', 'Delhi Capitals', 'Mumbai Indians',
       'Gujarat Titans', 'Royal Challengers Bangalore',
       'Rajasthan Royals', 'Lucknow Super Giants', 'Punjab Kings']
    bowling_team = ['Kolkata Knight Riders', 'Sunrisers Hyderabad',
       'Chennai Super Kings', 'Delhi Capitals', 'Mumbai Indians',
       'Gujarat Titans', 'Royal Challengers Bangalore',
       'Rajasthan Royals', 'Lucknow Super Giants', 'Punjab Kings']
    venues = ['Eden Gardens, Kolkata', 'Sharjah Cricket Stadium',
       'Wankhede Stadium, Mumbai', 'Kingsmead',
       'MA Chidambaram Stadium, Chepauk, Chennai',
       'Rajiv Gandhi International Stadium, Uppal, Hyderabad',
       'Sawai Mansingh Stadium, Jaipur',
       'Dubai International Cricket Stadium',
       'Arun Jaitley Stadium, Delhi', 'M.Chinnaswamy Stadium, Bengaluru',
       'Sheikh Zayed Stadium',
       'Maharashtra Cricket Association Stadium, Pune',
       'Dr DY Patil Sports Academy, Mumbai', "St George's Park",
       'The Wanderers Stadium, Johannesburg', 'Brabourne Stadium, Mumbai',
       'Dr DY Patil Sports Academy, Navi Mumbai',
       'JSCA International Stadium Complex', 'Newlands',
       'Narendra Modi Stadium, Motera, Ahmedabad',
       'Punjab Cricket Association IS Bindra Stadium, Mohali, Chandigarh',
       'SuperSport Park', 'Zayed Cricket Stadium, Abu Dhabi',
       'Bharat Ratna Shri Atal Bihari Vajpayee Ekana Cricket Stadium, Lucknow',
       'Barsapara Cricket Stadium, Guwahati',
       'Himachal Pradesh Cricket Association Stadium, Dharamsala',
       'Barabati Stadium', 'Buffalo Park',
       'Dr. Y.S. Rajasekhara Reddy ACA-VDCA Cricket Stadium',
       'De Beers Diamond Oval']

    with col1:
        selected_batting_team = st.selectbox('Select Batting Team', batting_team)
        st.write('')
        selected_bowling_team = st.selectbox('Select Bowling Team', bowling_team)
        st.write(' ')
        selected_venue = st.selectbox('Select Venue', venues)
    with col2:
        target = st.number_input('Target', value=110)
        st.write(' ')
        runs_left = target - st.number_input('Current Score', min_value=1, max_value=300, value=50, step=1)
    with col3:
        over_completed = st.number_input('Overs Completed', min_value=1.0, max_value=120.0, value=50.0, step=0.1)
        balls_left = 120 - (int(over_completed)*6 + round((over_completed - int(over_completed))*10,1))
        st.write(' ')
        wickets_left = 10 - st.number_input('Wickets Out', min_value=0, max_value=10, value=0, step=1)

    crr = round((target-runs_left)/((120-balls_left)//6 + ((120-balls_left) % 6)/10), 2)
    rrr = round((runs_left/((balls_left//6)+((balls_left % 6)/10))), 2)
    input_df = pd.DataFrame({'batting_team': [selected_batting_team], 'bowling_team': [selected_bowling_team], 'venue': [selected_venue],
                            'target': [target], 'runs_left': [runs_left], 'balls_left': [balls_left],
                            'wickets_left': [wickets_left], 'current_run_rate': [crr], 'required_run_rate': [rrr]})
    if st.button('Predict Win Probability'):
        result = loaded_pipeline.predict_proba(input_df)[0]
        formatted_text = f"**{round(result[1] * 100, 2)}%**"
        st.markdown(f'**{selected_batting_team}**: <span style="color:green">{formatted_text}</span>', unsafe_allow_html=True)
        formatted_text = f"**{round(result[0] * 100, 2)}%**"
        st.markdown(f'**{selected_bowling_team}**: <span style="color:green">{formatted_text}</span>', unsafe_allow_html=True)
elif select == 'More info':
        more_info_option = st.sidebar.selectbox('Select More Info Option', [
            'Max Wins Venue', 'Total Runs by Batsman', 'Total Wickets in Match',
            'Top Batsmen by Season', 'Top Bowlers by Season', 'Toss and Victory',
    
        ])

        if more_info_option == 'Max Wins Venue':
            selected_team = st.sidebar.selectbox('Select Team', ["Royal Challengers Bangalore","Kochi Tuskers Kerala","Rising Pune Supergiant","Punjab Kings","Mumbai Indians",
            "Chennai Super Kings","Rajasthan Royals","Deccan Chargers","Gujarat Lions""Delhi Capitals","Sunrisers Hyderabad"
            "Gujarat Titans","Kolkata Knight Riders","Pune Warriors""teamname","Lucknow Super Giants"])
            if st.button('Show Info'):
                query_max_wins_venue(selected_team)

        elif more_info_option == 'Total Runs by Batsman':
             match_ids_query = text("SELECT DISTINCT matchid FROM deliveries")
             result = engine.execute(match_ids_query)
             match_ids = [str(match[0]) for match in result.fetchall()]

    # Dropdown for selecting match ID
             match_id_input = st.selectbox('Select Match ID', match_ids)
             if st.button('Show Info'):
               query_runs_by_batsman(match_id_input)
        elif more_info_option == 'Total Wickets in Match':
    # Fetch available match IDs from the database
            match_ids_query = text("SELECT DISTINCT matchid FROM deliveries")
            result = engine.execute(match_ids_query)
            match_ids = [str(match[0]) for match in result.fetchall()]

    # Dropdown for selecting match ID
            match_id_input = st.selectbox('Select Match ID', match_ids)
            if st.button('Show Info'):
               query_wickets_in_match(match_id_input)

   
             
        elif more_info_option == 'Top Bowlers by Season':
            selected_season = st.sidebar.selectbox('Select Season', ['2008','2009','2010', '2011','2012','2013','2014', '2015','2016', '2017','2018','2019', '2020', '2021','2022'])  # Add more seasons as needed
            if st.button('Show Info'):
                top_bowlers_data = query_top_bowlers_by_season(selected_season)
                display_top_bowlers_info(top_bowlers_data)

       
        elif more_info_option == 'Toss and Victory':
            if st.button('Show Info'):
                toss_victory_data = query_toss_and_victory()
                toss_victory_data_with_names = [(team_id_name_mapping.get(team_id, team_id), toss_wins, match_wins) for team_id, toss_wins, match_wins in toss_victory_data]
                visualize_toss_and_victory(toss_victory_data_with_names) 


        elif more_info_option == 'Top Batsmen by Season':
            years_query = text("SELECT DISTINCT season FROM matches ORDER BY season ASC")
            result_years = engine.execute(years_query)
            years = [str(year[0]) for year in result_years.fetchall()]

            # Dropdown for selecting year
            selected_year = st.sidebar.selectbox('Select Year', years)

            # Fetch available match IDs for the selected year from the database
            match_ids_query = text(f"SELECT DISTINCT matchid FROM matches WHERE season = '{selected_year}'")
            result_match_ids = engine.execute(match_ids_query)
            match_ids = [str(match[0]) for match in result_match_ids.fetchall()]

            # Dropdown for selecting match ID
            selected_match_id = st.sidebar.selectbox('Select Match ID', match_ids)

            # Button to trigger the query and visualization
            btn_show_info = st.sidebar.button('Show Top Batsmen')

            if btn_show_info:
                top_batsmen_data = query_top_batsmen_by_year_and_match(selected_year, selected_match_id)
                display_top_batsmen_by_year_and_match(top_batsmen_data)

        elif more_info_option == 'Top Bowlers as Batsmen':
    # Fetch available years from the database
            years_query = text("SELECT DISTINCT season FROM matches ORDER BY season ASC")
            result_years = engine.execute(years_query)
            years = [str(year[0]) for year in result_years.fetchall()]

            # Dropdown for selecting year
            selected_year = st.sidebar.selectbox('Select Year', years)

            # Button to trigger the query and visualization
            btn_show_info = st.sidebar.button('Show Top Bowlers as Batsmen')

            if btn_show_info:
                top_bowlers_data = query_top_bowlers_as_batsmen(selected_year)
                display_top_bowlers_as_batsmen(top_bowlers_data)
        
        elif more_info_option == 'All-Rounders in the Match':
    # Fetch available match IDs from the database
            match_ids_query = text("SELECT DISTINCT matchid FROM deliveries")
            result_match_ids = engine.execute(match_ids_query)
            match_ids = [str(match[0]) for match in result_match_ids.fetchall()]

            # Dropdown for selecting match ID
            selected_match_id = st.sidebar.selectbox('Select Match ID', match_ids)

            # Button to trigger the query and visualization
            btn_show_info = st.sidebar.button('Show All-Rounders')

            if btn_show_info:
                all_rounders_data = query_all_rounders(selected_match_id)
                display_all_rounders(all_rounders_data)

session.close()




