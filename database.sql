CREATE TABLE Teams (
     TeamID serial PRIMARY KEY,
     TeamName text NOT NULL
);
CREATE TABLE Umpires (
    UmpireID serial PRIMARY KEY,
    UmpireName text NOT NULL
);
CREATE TABLE Venues (
     VenueID serial PRIMARY KEY,
     VenueName text NOT NULL,
     City text NOT NULL
 );
CREATE TABLE Matches (
    MatchID serial PRIMARY KEY,
    Season integer NOT NULL,
    MatchNumber text NOT NULL,
    VenueID integer REFERENCES Venues(VenueID),
	TossWinner integer REFERENCES Teams(TeamID),
    TossDecision text NOT NULL,
    SuperOver boolean,
	WinningTeam integer REFERENCES Teams(TeamID),
    WonBy text NOT NULL,
    Margin text,
    PlayerOfTheMatch text,
    Umpire1ID integer REFERENCES Umpires(UmpireID),
    Umpire2ID integer REFERENCES Umpires(UmpireID)
);

CREATE TABLE Deliveries (
    MatchID integer REFERENCES Matches(MatchID),
    Overs integer NOT NULL,
	BallNumber integer NOT NULL,
    Batter text NOT NULL,
    Bowler text NOT NULL,
    NonStriker text NOT NULL,
    ExtraType text,
    BatsmanRun integer NOT NULL,
    ExtrasRun integer NOT NULL,
    TotalRun integer NOT NULL,
    NonBoundary integer NOT NULL,
    IsWicketDelivery boolean NOT NULL,
    PlayerOut text,
    FieldersInvolved text,
    Kind text,
    BattingTeamID integer REFERENCES Teams(TeamID),
    PRIMARY KEY (MatchID, Overs, BallNumber,Bowler,Batter,NonStriker)
);







