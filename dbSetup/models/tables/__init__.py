from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    Date,
    Double,
    Float,
    ForeignKey,
    Index,
    Integer,
    SmallInteger,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, relationship


class Base(DeclarativeBase):
    pass


class People(Base):
    __tablename__ = "people"
    playerID = Column(String(9), primary_key=True, nullable=False)
    birthYear = Column(Integer, nullable=True)
    birthMonth = Column(Integer, nullable=True)
    birthDay = Column(Integer, nullable=True)
    birthCountry = Column(String(255), nullable=True)
    birthState = Column(String(255), nullable=True)
    birthCity = Column(String(255), nullable=True)
    deathYear = Column(Integer, nullable=True)
    deathMonth = Column(Integer, nullable=True)
    deathDay = Column(Integer, nullable=True)
    deathCountry = Column(String(255), nullable=True)
    deathState = Column(String(255), nullable=True)
    deathCity = Column(String(255), nullable=True)
    nameFirst = Column(String(255), nullable=True)
    nameLast = Column(String(255), nullable=True)
    nameGiven = Column(String(255), nullable=True)
    weight = Column(Integer, nullable=True)
    height = Column(Integer, nullable=True)
    bats = Column(String(255), nullable=True)
    throws = Column(String(255), nullable=True)
    debutDate = Column(Date, nullable=True)
    finalGameDate = Column(Date, nullable=True)
    nl_hof = Column(Boolean, nullable=True, default=False)

    __table_args__ = (Index("idx_nameLast", "nameLast"),)  # nameLast is MUL in the db

    # Define relationship
    allstarfull_entries = relationship("AllstarFull", back_populates="player")
    collegeplaying_player = relationship(
        "CollegePlaying", back_populates="collegeplaying_player"
    )
    managers = relationship("Manager", back_populates="people")
    awards = relationship("Awards", back_populates="player")
    awardsshare = relationship("AwardsShare", back_populates="player")
    pitching_entries = relationship("Pitching", back_populates="player")
    pitchingpost_entries = relationship("PitchingPost", back_populates="player")
    batting_entries = relationship("Batting", back_populates="player")
    battingpost_entries = relationship("BattingPost", back_populates="player")


class Manager(Base):
    __tablename__ = "managers"

    managers_ID = Column(Integer, primary_key=True, nullable=False)
    playerID = Column(String(9), ForeignKey("people.playerID"), nullable=False)
    yearID = Column(SmallInteger, nullable=False)
    teamID = Column(String(3), nullable=False)
    inSeason = Column(SmallInteger, nullable=False)
    manager_G = Column(SmallInteger, nullable=True)
    manager_W = Column(SmallInteger, nullable=True)
    manager_L = Column(SmallInteger, nullable=True)
    teamRank = Column(SmallInteger, nullable=True)
    plyrMgr = Column(String(1), nullable=True)
    half = Column(SmallInteger, nullable=True)  # Use a constraint for values 1 or 2

    __table_args__ = (
        UniqueConstraint(
            "playerID",
            "yearID",
            "teamID",
            "inSeason",
            name="uq_player_year_team_inseason",
        ),
        {"mysql_charset": "utf8mb3", "mysql_collate": "utf8mb3_general_ci"},
    )

    # Define relationship
    people = relationship("People", back_populates="managers")


class Awards(Base):
    __tablename__ = "awards"

    awards_ID = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    awardID = Column(String(255), nullable=False)
    yearID = Column(SmallInteger, nullable=False)
    playerID = Column(String(9), ForeignKey("people.playerID"), nullable=False)
    lgID = Column(String(2), nullable=False)
    tie = Column(String(1), nullable=True)
    notes = Column(String(100), nullable=True)

    # Define indexes
    __table_args__ = (
        Index("fk_awd_peo", "playerID"),
        UniqueConstraint(
            "awardID", "yearID", "playerID", "lgID", name="uq_award_year_player_lg"
        ),
    )

    # Define relationships
    player = relationship("People", back_populates="awards")


class AwardsShare(Base):
    __tablename__ = "awardsshare"

    awardsshare_ID = Column(
        Integer, primary_key=True, nullable=False, autoincrement=True
    )
    awardID = Column(String(255), nullable=False)
    yearID = Column(SmallInteger, nullable=False)
    playerID = Column(String(9), ForeignKey("people.playerID"), nullable=False)
    lgID = Column(String(2), nullable=False)
    pointsWon = Column(Double, nullable=True)
    pointsMax = Column(SmallInteger, nullable=True)
    votesFirst = Column(Double, nullable=True)

    # Define indexes
    __table_args__ = (
        Index("fk_awdshr_peo", "playerID"),
        UniqueConstraint(
            "awardID", "yearID", "playerID", "lgID", name="uq_award_year_player_lg"
        ),
    )

    # Define relationships
    player = relationship("People", back_populates="awardsshare")


class Batting(Base):
    __tablename__ = "batting"
    batting_ID = Column(Integer, primary_key=True, nullable=False)
    playerID = Column(String(9), ForeignKey("people.playerID"), nullable=False)
    yearID = Column(SmallInteger, nullable=False)
    teamID = Column(String(3), nullable=False)
    stint = Column(SmallInteger, nullable=False)
    b_G = Column(SmallInteger, nullable=True)
    b_AB = Column(SmallInteger, nullable=True)
    b_R = Column(SmallInteger, nullable=True)
    b_H = Column(SmallInteger, nullable=True)
    b_2B = Column(SmallInteger, nullable=True)
    b_3B = Column(SmallInteger, nullable=True)
    b_HR = Column(SmallInteger, nullable=True)
    b_RBI = Column(SmallInteger, nullable=True)
    b_SB = Column(SmallInteger, nullable=True)
    b_CS = Column(SmallInteger, nullable=True)
    b_BB = Column(SmallInteger, nullable=True)
    b_SO = Column(SmallInteger, nullable=True)
    b_IBB = Column(SmallInteger, nullable=True)
    b_HBP = Column(SmallInteger, nullable=True)
    b_SH = Column(SmallInteger, nullable=True)
    b_SF = Column(SmallInteger, nullable=True)
    b_GIDP = Column(SmallInteger, nullable=True)

    # Indexes
    __table_args__ = (
        Index("k_bat_team", "teamID"),  # Index for teamID
        Index(
            "batting_playerID_yearID_teamID", "playerID", "yearID", "teamID"
        ),  # Composite index
        UniqueConstraint(
            "playerID", "yearID", "teamID", "stint", name="uq_player_year_team_stint"
        ),
    )

    # Define relationships
    player = relationship("People", back_populates="batting_entries")


class BattingPost(Base):
    __tablename__ = "battingpost"
    battingpost_ID = Column(Integer, primary_key=True, nullable=False)
    playerID = Column(String(9), ForeignKey("people.playerID"), nullable=False)
    yearId = Column(SmallInteger, nullable=False)
    teamID = Column(String(3), nullable=False)
    round = Column(String(10), nullable=False)
    b_G = Column(SmallInteger, nullable=True)
    b_AB = Column(SmallInteger, nullable=True)
    b_R = Column(SmallInteger, nullable=True)
    b_H = Column(SmallInteger, nullable=True)
    b_2B = Column(SmallInteger, nullable=True)
    b_3B = Column(SmallInteger, nullable=True)
    b_HR = Column(SmallInteger, nullable=True)
    b_RBI = Column(SmallInteger, nullable=True)
    b_SB = Column(SmallInteger, nullable=True)
    b_CS = Column(SmallInteger, nullable=True)
    b_BB = Column(SmallInteger, nullable=True)
    b_SO = Column(SmallInteger, nullable=True)
    b_IBB = Column(SmallInteger, nullable=True)
    b_HBP = Column(SmallInteger, nullable=True)
    b_SH = Column(SmallInteger, nullable=True)
    b_SF = Column(SmallInteger, nullable=True)
    b_GIDP = Column(SmallInteger, nullable=True)

    # Indexes
    __table_args__ = (
        Index("k_bp_team", "teamID"),  # Index for teamID
        Index(
            "battingpost_playerID_yearID_teamID", "playerID", "yearId", "teamID"
        ),  # Composite index
        UniqueConstraint(
            "playerID", "yearId", "teamID", "round", name="uq_player_year_team_round"
        ),
    )

    # Relationships
    player = relationship("People", back_populates="battingpost_entries")


class CareerWarLeaders(Base):
    __tablename__ = "careerwarleaders"
    careerwarleaders_ID = Column(Integer, primary_key=True, nullable=False)
    playerID = Column(String(9), ForeignKey("people.playerID"), nullable=False)
    war = Column(Double, nullable=False)

    __table_args__ = (
        Index(
            "careerwarleaders_playerID_war",
            "playerID",
            "war",
        ),  # Composite index
    )

class SeasonWarLeaders(Base):
    __tablename__ = "seasonwarleaders"
    seasonwarleaders_ID = Column(Integer, primary_key=True, nullable=False)
    playerID = Column(String(9), ForeignKey("people.playerID"), nullable=False)
    war = Column(Double, nullable=False)
    yearID = Column(SmallInteger, nullable=False)

    __table_args__ = (
        Index(
            "seasonwarleaders_playerID_war",
            "playerID",
            "war",
        ),  # Composite index
    )


class Draft(Base):
    __tablename__ = "draft"
    draft_ID = Column(Integer, primary_key=True, nullable=False)
    playerID = Column(String(9), ForeignKey("people.playerID"), nullable=False)
    yearID = Column(SmallInteger, nullable=False)
    teamID = Column(String(3), nullable=False)

    __table_args__ = (
        Index("k_draft_team", "teamID"),  # Index for teamID
        Index(
            "draft_playerID_yearID_teamID", "playerID", "yearID", "teamID"
        ),  # Composite index
    )


class HallofFame(Base):
    __tablename__ = "halloffame"
    halloffame_ID = Column(Integer, primary_key=True, nullable=False)
    playerID = Column(String(9), ForeignKey("people.playerID"), nullable=False)
    yearID = Column(SmallInteger, nullable=False)
    votedBy = Column(String(64), nullable=False)
    ballots = Column(SmallInteger, nullable=True)
    needed = Column(SmallInteger, nullable=True)
    votes = Column(SmallInteger, nullable=True)
    inducted = Column(String(1), nullable=True)
    category = Column(String(20), nullable=True)
    note = Column(String(255), nullable=True)


class NoHitters(Base):
    __tablename__ = "nohitters"
    nohitters_ID = Column(Integer, primary_key=True, nullable=False)
    playerID = Column(String(9), ForeignKey("people.playerID"), nullable=False)
    yearID = Column(SmallInteger, nullable=False)
    teamID = Column(String(3), nullable=False)
    date = Column(String(9), nullable=False)
    type = Column(String(1), nullable=False)

    __table_args__ = (
        Index("k_nohitters_team", "teamID"),  # Index for teamID
        Index(
            "nohitters_playerID_yearID_teamID_date_type",
            "playerID",
            "yearID",
            "teamID",
            "date",
            "type",
        ),  # Composite index
    )


class Leagues(Base):
    __tablename__ = "leagues"
    lgID = Column(String(2), primary_key=True, nullable=False)
    league_name = Column(String(50), nullable=False)
    league_active = Column(String(1), nullable=False)

    # Define relationship
    allstarfull_entries = relationship(
        "AllstarFull", foreign_keys="[AllstarFull.lgID]", back_populates="league"
    )
    teams_entries = relationship(
        "Teams", foreign_keys="[Teams.lgID]", back_populates="league"
    )
    league_seriespost_winner = relationship(
        "SeriesPost",
        foreign_keys="[SeriesPost.lgIDwinner]",
        back_populates="winner_league",
    )
    league_seriespost_loser = relationship(
        "SeriesPost",
        foreign_keys="[SeriesPost.lgIDloser]",
        back_populates="loser_league",
    )


class CollegePlaying(Base):
    __tablename__ = "collegeplaying"
    collegeplaying_ID = Column(
        Integer, primary_key=True, nullable=False, autoincrement=True
    )
    playerID = Column(String(9), ForeignKey("people.playerID"), nullable=False)
    schoolID = Column(String(15), ForeignKey("schools.schoolId"), nullable=True)
    yearID = Column(SmallInteger, nullable=True)

    # Define relationships
    collegeplaying_player = relationship(
        "People", back_populates="collegeplaying_player"
    )
    collegeplaying_school = relationship(
        "Schools", back_populates="collegeplaying_school"
    )

    # Define the MUL (Index) fields
    # this speeds up data retrieval by these columns
    __table_args__ = (
        Index("idx_schoolID", "schoolID"),
        Index("idx_playerID", "playerID"),
        UniqueConstraint(
            "playerID", "schoolID", "yearID", name="uq_player_school_year"
        ),
    )


class Teams(Base):
    __tablename__ = "teams"
    teams_ID = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    teamID = Column(String(3), nullable=False)
    yearID = Column(SmallInteger, nullable=False)
    lgID = Column(String(2), ForeignKey("leagues.lgID"), nullable=True)
    divID = Column(String(1), ForeignKey("divisions.divID"), nullable=True)
    franchID = Column(String(3), nullable=True)
    team_name = Column(String(50), nullable=True)
    team_rank = Column(SmallInteger, nullable=True)
    team_G = Column(SmallInteger, nullable=True)
    team_G_home = Column(SmallInteger, nullable=True)
    team_W = Column(SmallInteger, nullable=True)
    team_L = Column(SmallInteger, nullable=True)
    DivWin = Column(String(1), nullable=True)
    WCWin = Column(String(1), nullable=True)
    LgWin = Column(String(1), nullable=True)
    WSWin = Column(String(1), nullable=True)
    team_R = Column(SmallInteger, nullable=True)
    team_AB = Column(SmallInteger, nullable=True)
    team_H = Column(SmallInteger, nullable=True)
    team_2B = Column(SmallInteger, nullable=True)
    team_3B = Column(SmallInteger, nullable=True)
    team_HR = Column(SmallInteger, nullable=True)
    team_BB = Column(SmallInteger, nullable=True)
    team_SO = Column(SmallInteger, nullable=True)
    team_SB = Column(SmallInteger, nullable=True)
    team_CS = Column(SmallInteger, nullable=True)
    team_HBP = Column(SmallInteger, nullable=True)
    team_SF = Column(SmallInteger, nullable=True)
    team_RA = Column(SmallInteger, nullable=True)
    team_ER = Column(SmallInteger, nullable=True)
    team_ERA = Column(Double, nullable=True)
    team_CG = Column(SmallInteger, nullable=True)
    team_SHO = Column(SmallInteger, nullable=True)
    team_SV = Column(SmallInteger, nullable=True)
    team_IPouts = Column(Integer, nullable=True)
    team_HA = Column(SmallInteger, nullable=True)
    team_HRA = Column(SmallInteger, nullable=True)
    team_BBA = Column(SmallInteger, nullable=True)
    team_SOA = Column(SmallInteger, nullable=True)
    team_E = Column(SmallInteger, nullable=True)
    team_DP = Column(SmallInteger, nullable=True)
    team_FP = Column(Double, nullable=True)
    park_name = Column(String(50), nullable=True)
    team_attendance = Column(Integer, nullable=True)
    team_BPF = Column(SmallInteger, nullable=True)
    team_PPF = Column(SmallInteger, nullable=True)
    team_projW = Column(SmallInteger, nullable=True)
    team_projL = Column(SmallInteger, nullable=True)

    # Define the MUL (Index) fields
    __table_args__ = (
        Index("idx_teamID", "teamID"),
        Index("idx_lgID", "lgID"),
        Index("idx_franchID", "franchID"),
        UniqueConstraint(
            "teamID",
            "yearID",
            name="uq_teams",
        ),
    )

    # Define relationships
    league = relationship(
        "Leagues", foreign_keys=[lgID], back_populates="teams_entries"
    )
    seriespost_winner = relationship(
        "SeriesPost",
        foreign_keys="[SeriesPost.teamIDwinner]",
        back_populates="winner",
    )
    seriespost_loser = relationship(
        "SeriesPost",
        foreign_keys="[SeriesPost.teamIDloser]",
        back_populates="loser",
    )


class AllstarFull(Base):
    __tablename__ = "allstarfull"
    allstarfull_ID = Column(Integer, primary_key=True, nullable=False)
    playerID = Column(String(9), ForeignKey("people.playerID"), nullable=False)
    lgID = Column(String(2), ForeignKey("leagues.lgID"), nullable=False)
    teamID = Column(String(3), nullable=False)
    yearID = Column(SmallInteger, nullable=False)
    gameID = Column(String(12))
    GP = Column(SmallInteger)
    startingPos = Column(SmallInteger)

    __table_args__ = (
        UniqueConstraint(
            "playerID",
            "lgID",
            "teamID",
            "yearID",
            name="uq_allstarfull",
        ),
    )

    # Define relationships
    league = relationship("Leagues", back_populates="allstarfull_entries")
    player = relationship("People", back_populates="allstarfull_entries")


class Schools(Base):
    __tablename__ = "schools"
    schoolId = Column(String(15), primary_key=True, nullable=False)
    # none of the following column values are ever null, AND it doesnt make sense to allow them to be null
    school_name = Column(String(255), nullable=False)
    school_city = Column(String(55), nullable=False)
    school_state = Column(String(55), nullable=False)
    school_country = Column(String(55), nullable=False)

    # Define relationships
    collegeplaying_school = relationship(
        "CollegePlaying", back_populates="collegeplaying_school"
    )


class SeriesPost(Base):
    __tablename__ = "seriespost"
    seriespost_ID = Column(Integer, primary_key=True, nullable=False)
    teamIDwinner = Column(String(3), ForeignKey("teams.teamID"), nullable=False)
    lgIDwinner = Column(String(3), ForeignKey("leagues.lgID"), nullable=False)
    teamIDloser = Column(String(3), ForeignKey("teams.teamID"), nullable=False)
    lgIDloser = Column(String(3), ForeignKey("leagues.lgID"), nullable=False)
    yearID = Column(SmallInteger, nullable=False)
    round = Column(String(5), nullable=False)
    wins = Column(SmallInteger, nullable=True)
    losses = Column(SmallInteger, nullable=True)
    ties = Column(SmallInteger, nullable=True)

    __table_args__ = (
        UniqueConstraint(
            "teamIDwinner",
            "lgIDwinner",
            "teamIDloser",
            "lgIDloser",
            "yearID",
            "round",
            name="uq_seriespost",
        ),
    )

    winner = relationship(
        "Teams", foreign_keys=[teamIDwinner], back_populates="seriespost_winner"
    )
    loser = relationship(
        "Teams", foreign_keys=[teamIDloser], back_populates="seriespost_loser"
    )
    winner_league = relationship(
        "Leagues", foreign_keys=[lgIDwinner], back_populates="league_seriespost_winner"
    )
    loser_league = relationship(
        "Leagues", foreign_keys=[lgIDloser], back_populates="league_seriespost_loser"
    )


class Pitching(Base):
    __tablename__ = "pitching"
    pitching_ID = Column(Integer, primary_key=True, nullable=False)
    playerID = Column(String(9), ForeignKey("people.playerID"), nullable=False)
    yearID = Column(SmallInteger, nullable=False)
    teamID = Column(String(3), ForeignKey("teams.teamID"), nullable=False)
    stint = Column(SmallInteger, nullable=False)
    p_W = Column(SmallInteger, nullable=True)
    p_L = Column(SmallInteger, nullable=True)
    p_G = Column(SmallInteger, nullable=True)
    p_GS = Column(SmallInteger, nullable=True)
    p_CG = Column(SmallInteger, nullable=True)
    p_SHO = Column(SmallInteger, nullable=True)
    p_SV = Column(SmallInteger, nullable=True)
    p_IPouts = Column(Integer, nullable=True)
    p_H = Column(SmallInteger, nullable=True)
    p_ER = Column(SmallInteger, nullable=True)
    p_HR = Column(SmallInteger, nullable=True)
    p_BB = Column(SmallInteger, nullable=True)
    p_SO = Column(SmallInteger, nullable=True)
    p_BAOpp = Column(Double, nullable=True)
    p_ERA = Column(Double, nullable=True)
    p_IBB = Column(SmallInteger, nullable=True)
    p_WP = Column(SmallInteger, nullable=True)
    p_HBP = Column(SmallInteger, nullable=True)
    p_BK = Column(SmallInteger, nullable=True)
    p_BFP = Column(SmallInteger, nullable=True)
    p_GF = Column(SmallInteger, nullable=True)
    p_R = Column(SmallInteger, nullable=True)
    p_SH = Column(SmallInteger, nullable=True)
    p_SF = Column(SmallInteger, nullable=True)
    p_GIDP = Column(SmallInteger, nullable=True)

    # Define the MUL (Index) fields
    # this speeds up data retrieval by these columns
    __table_args__ = (
        Index("idx_teamID", "teamID"),
        Index("idx_playerID_yearID_teamID", "playerID", "yearID", "teamID"),
        UniqueConstraint(
            "playerID", "yearID", "teamID", "stint", name="uq_player_year_team_stint"
        ),
    )

    player = relationship("People", back_populates="pitching_entries")


class PitchingPost(Base):
    __tablename__ = "pitchingpost"
    pitchingpost_ID = Column(Integer, primary_key=True, nullable=False)
    playerID = Column(String(9), ForeignKey("people.playerID"), nullable=False)
    yearID = Column(SmallInteger, nullable=False)
    teamID = Column(String(3), ForeignKey("teams.teamID"), nullable=False)
    round = Column(String(10), nullable=False)
    p_W = Column(SmallInteger, nullable=True)
    p_L = Column(SmallInteger, nullable=True)
    p_G = Column(SmallInteger, nullable=True)
    p_GS = Column(SmallInteger, nullable=True)
    p_CG = Column(SmallInteger, nullable=True)
    p_SHO = Column(SmallInteger, nullable=True)
    p_SV = Column(SmallInteger, nullable=True)
    p_IPouts = Column(Integer, nullable=True)
    p_H = Column(SmallInteger, nullable=True)
    p_ER = Column(SmallInteger, nullable=True)
    p_HR = Column(SmallInteger, nullable=True)
    p_BB = Column(SmallInteger, nullable=True)
    p_SO = Column(SmallInteger, nullable=True)
    p_BAOpp = Column(Double, nullable=True)
    p_ERA = Column(Double, nullable=True)
    p_IBB = Column(SmallInteger, nullable=True)
    p_WP = Column(SmallInteger, nullable=True)
    p_HBP = Column(SmallInteger, nullable=True)
    p_BK = Column(SmallInteger, nullable=True)
    p_BFP = Column(SmallInteger, nullable=True)
    p_GF = Column(SmallInteger, nullable=True)
    p_R = Column(SmallInteger, nullable=True)
    p_SH = Column(SmallInteger, nullable=True)
    p_SF = Column(SmallInteger, nullable=True)
    p_GIDP = Column(SmallInteger, nullable=True)

    # Define the MUL (Index) fields
    # this speeds up data retrieval by these columns
    __table_args__ = (
        Index("idx_teamID", "teamID"),
        Index("idx_playerID_yearID_teamID", "playerID", "yearID", "teamID"),
        UniqueConstraint(
            "playerID", "yearID", "teamID", "round", name="uq_player_year_team_round"
        ),
    )

    player = relationship("People", back_populates="pitchingpost_entries")


class Appearances(Base):
    __tablename__ = "appearances"
    appearances_ID = Column(Integer, primary_key=True, nullable=False)
    playerID = Column(String(9), ForeignKey("people.playerID"), nullable=False)
    yearID = Column(SmallInteger, nullable=False)
    teamID = Column(String(3), ForeignKey("teams.teamID"), nullable=False)
    G_all = Column(SmallInteger, nullable=True)
    GS = Column(SmallInteger, nullable=True)
    G_batting = Column(SmallInteger, nullable=True)
    G_defense = Column(SmallInteger, nullable=True)
    G_p = Column(SmallInteger, nullable=True)
    G_c = Column(SmallInteger, nullable=True)
    G_1b = Column(SmallInteger, nullable=True)
    G_2b = Column(SmallInteger, nullable=True)
    G_3b = Column(SmallInteger, nullable=True)
    G_ss = Column(SmallInteger, nullable=True)
    G_lf = Column(SmallInteger, nullable=True)
    G_cf = Column(SmallInteger, nullable=True)
    G_rf = Column(SmallInteger, nullable=True)
    G_of = Column(SmallInteger, nullable=True)
    G_dh = Column(SmallInteger, nullable=True)
    G_ph = Column(SmallInteger, nullable=True)
    G_pr = Column(SmallInteger, nullable=True)

    # Define the MUL (Index) fields
    # this speeds up data retrieval by these columns
    __table_args__ = (
        Index("idx_teamID", "teamID"),
        Index(
            "idx_playerID_yearID",
            "playerID",
            "yearID",
        ),
        UniqueConstraint("playerID", "yearID", "teamID", name="uq_player_year_team"),
    )


class Fielding(Base):
    __tablename__ = "fielding"
    fielding_ID = Column(Integer, primary_key=True, nullable=False)
    playerID = Column(String(9), ForeignKey("people.playerID"), nullable=False)
    yearID = Column(SmallInteger, nullable=False)
    teamID = Column(String(3), ForeignKey("teams.teamID"), nullable=False)
    stint = Column(SmallInteger, nullable=False)
    position = Column(String(2), nullable=True)
    f_G = Column(SmallInteger, nullable=True)
    f_GS = Column(SmallInteger, nullable=True)
    f_InnOuts = Column(SmallInteger, nullable=True)
    f_PO = Column(SmallInteger, nullable=True)
    f_A = Column(SmallInteger, nullable=True)
    f_E = Column(SmallInteger, nullable=True)
    f_DP = Column(SmallInteger, nullable=True)
    f_PB = Column(SmallInteger, nullable=True)
    f_WP = Column(SmallInteger, nullable=True)
    f_SB = Column(SmallInteger, nullable=True)
    f_CS = Column(SmallInteger, nullable=True)
    f_ZR = Column(Float, nullable=True)

    # Define the MUL (Index) fields
    # this speeds up data retrieval by these columns
    __table_args__ = (
        Index("idx_teamID", "teamID"),
        Index("idx_playerID_yearID_teamID", "playerID", "yearID", "teamID"),
        UniqueConstraint(
            "playerID",
            "yearID",
            "teamID",
            "stint",
            "position",
            name="uq_player_team_year_stint_position",
        ),
    )

class FieldingPost(Base):
    __tablename__ = "fieldingpost"
    fieldingpost_ID = Column(Integer, primary_key=True, nullable=False)
    playerID = Column(String(9), ForeignKey("people.playerID"), nullable=False)
    yearID = Column(SmallInteger, nullable=False)
    teamID = Column(String(3), ForeignKey("teams.teamID"), nullable=False)
    round = Column(String(10), nullable=False)
    position = Column(String(2), nullable=True)
    f_G = Column(SmallInteger, nullable=True)
    f_GS = Column(SmallInteger, nullable=True)
    f_InnOuts = Column(SmallInteger, nullable=True)
    f_PO = Column(SmallInteger, nullable=True)
    f_A = Column(SmallInteger, nullable=True)
    f_E = Column(SmallInteger, nullable=True)
    f_DP = Column(SmallInteger, nullable=True)
    f_TP = Column(SmallInteger, nullable=True)
    f_PB = Column(SmallInteger, nullable=True)

    # SB and CS are in the CSV but not in our database -Icko

    # Define the MUL (Index) fields
    # this speeds up data retrieval by these columns
    __table_args__ = (
        Index("idx_teamID", "teamID"),
        Index("idx_playerID_yearID_teamID", "playerID", "yearID", "teamID"),
        UniqueConstraint(
            "playerID",
            "yearID",
            "teamID",
            "round",
            "position",
            name="uq_player_team_year_round_position",
        ),
    )

class Salaries(Base):
    __tablename__ = "salaries"
    salaries_ID = Column(Integer, primary_key=True, nullable=False)
    playerID = Column(String(9), ForeignKey("people.playerID"), nullable=False)
    yearId = Column(SmallInteger, nullable=False)
    teamID = Column(String(3), ForeignKey("teams.teamID"), nullable=False)
    salary = Column(Double, nullable=True)

    __table_args__ = (
        Index("key_team", "teamID"),
        Index("salaries_playerID", "playerID"),
        UniqueConstraint(
            "playerID",
            "yearId",
            "teamID",
            name="uq_salary_player_year_team"),
        {"mysql_charset": "utf8mb3", "mysql_collate": "utf8mb3_general_ci"},
    )

class HomeGames(Base):
    __tablename__ = "homegames"
    homegames_ID = Column(Integer, primary_key=True, nullable=False)
    teamID = Column(String(3), ForeignKey("teams.teamID"), nullable=False)
    parkID = Column(String, ForeignKey("parks.parkID"), nullable=False)
    yearID = Column(SmallInteger, nullable=False)
    firstGame = Column(Date, nullable=True)
    lastGame = Column(Date, nullable=True)
    games = Column(Integer, nullable=True)
    openings = Column(Integer, nullable=True)
    attendance = Column(Integer, nullable=True)

    # Define the MUL (Index) fields
    # this speeds up data retrieval by these columns
    __table_args__ = (
        Index("idx_parkID", "parkID"),
        UniqueConstraint("teamID", "parkID", "yearID", name="unq_team_park_year"),
    )


class Parks(Base):
    __tablename__ = "parks"
    parkID = Column(String, primary_key=True, nullable=False)
    park_alias = Column(String, nullable=False)
    park_name = Column(String, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    country = Column(String, nullable=False)

    __table_args__ = (
        # no rows can have the same combination of divID and lgID
        UniqueConstraint("park_name", "city", "state", "country", name="uq_entry"),
    )


class Divisions(Base):
    __tablename__ = "divisions"
    divisions_ID = Column(Integer, primary_key=True, nullable=False)
    divID = Column(String(2), nullable=False)
    lgID = Column(String(2), ForeignKey(Leagues.lgID), nullable=False)
    division_name = Column(String, nullable=False)
    division_active = Column(String(1), nullable=False)

    # Define the MUL (Index) fields
    # this speeds up data retrieval by these columns
    __table_args__ = (
        # no rows can have the same combination of divID and lgID
        UniqueConstraint("divID", "lgID", name="uq_div_lg"),
        Index("idx_lgID", "lgID"),
        Index("idx_divID", "divID"),
        # Ensure division_active is always 'Y' or 'N'
        CheckConstraint("division_active IN ('Y', 'N')", name="chk_division_active"),
    )

class WobaWeights(Base):
    __tablename__ = "wobaweights"
    wobaweights_ID = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    yearID = Column(SmallInteger, unique=True, nullable=False)
    League = Column(Float, nullable=False)
    wOBAScale = Column(Float, nullable=False)
    wBB = Column(Float, nullable=False)
    wHBP = Column(Float, nullable=False)
    w1B = Column(Float, nullable=False)
    w2B = Column(Float, nullable=False)
    w3B = Column(Float, nullable=False)
    wHR = Column(Float, nullable=False)
    runSB = Column(Float, nullable=False)
    runCS = Column(Float, nullable=False)
    R_PA = Column(Float, nullable=False)
    R_W = Column(Float, nullable=False)
    cFIP = Column(Float, nullable=False)
