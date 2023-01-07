import psycopg2
import random
from psycopg2 import Error
from psycopg2.extensions import (
    connection as Connection,
    cursor as Cursor
)
from config import (
    USER,
    PASSWORD,
    HOST,
    PORT,
)


class Connection:
    """Class for working to DataBase"""

    def __init__(self) -> None:
        try:
            self.connection: Connection = psycopg2.connect(
                user=USER,
                password=PASSWORD,
                host=HOST,
                port=PORT,
                database="football_matches"
            )
            print("[INFO] Connection is successful")
        except (Exception, Error) as e:
            print("{0} [ERROR] Connection to database is bad:".format(
                e
            ))

    def __new__(cls: type[any]) -> any:
        if not hasattr(cls, 'instance'):
            cls.instance = super(Connection, cls).__new__(cls)
        return cls.instance

    # func of creating tables (squad, game_score, overall_team(third table with squad.id, game_score.id))
    def create_tables(self) -> None:
        with self.connection.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS squad (
                    id SERIAL PRIMARY KEY,
                    round VARCHAR(20) NOT NULL,
                    date TEXT NOT NULL,
                    team_one VARCHAR(30) NOT NULL,
                    team_two VARCHAR(30) NOT NULL
                );
                CREATE TABLE IF NOT EXISTS game_score (
                   id SERIAL PRIMARY KEY,
                   overall VARCHAR(20) NOT NULL
                );
                CREATE TABLE IF NOT EXISTS overall_team(
                    first_id INTEGER NOT NULL REFERENCES squad(id),
                    second_id INTEGER NOT NULL REFERENCES game_score(id)
                );
                """)
        self.connection.commit()
        print("[INFO] Tables is created")

    # adding to database round matches
    def add_match(self,round):
        with self.connection.cursor() as cur:
            cur.execute(
                f"""
                INSERT INTO game_round(round) VALUES ('{round}');
                """)
        self.connection.commit()

    # adding to database score
    def add_score(self,score):
        with self.connection.cursor() as cur:
            cur.execute(
                f"""
                INSERT INTO game_score(overall) VALUES ('{score}');
                """)
        self.connection.commit() 

    # inserting to database (squad.id and game_score.id)
    def insert_overall(self,first_id,second_id):
        with self.connection.cursor() as cur:
            cur.execute(f"""
               INSERT INTO overall_team(first_id,second_id) VALUES ('{first_id}','{second_id}'); 
            """)
        self.connection.commit()
    
    # inserting to database squad (round, date and both teams)
    def insert_into_overall(self,round,date, first_team, second_team):
        with self.connection.cursor() as cur:
            cur.execute(
                f"""
                INSERT INTO squad(round, date,team_one,team_two) VALUES ('{round}','{date}','{first_team}', '{second_team}');
                """)
        self.connection.commit()

    # showing information from all tables
    def show_all_information(self) -> list[tuple]:
        with self.connection.cursor() as cur:
            cur.execute(f"""
            SELECT round, date, team_one, team_two,game_score.overall FROM squad 
            LEFT JOIN overall_team ON overall_team.first_id = squad.id
            LEFT JOIN game_score ON overall_team.second_id = game_score.id;
            """)
            team: list[tuple] = cur.fetchall()
        self.connection.commit()
        return team

    # showing score of teams 
    def show_score_information(self, score) -> list[tuple]:
        with self.connection.cursor() as cur:
            cur.execute(f"""
            SELECT round, date, team_one, team_two,game_score.overall FROM squad 
            LEFT JOIN overall_team ON overall_team.first_id = squad.id
            LEFT JOIN game_score ON overall_team.second_id = game_score.id
            WHERE game_score.overall = '{score}';
            """)
            team: list[tuple] = cur.fetchall()
        self.connection.commit()
        return team
