import mysql.connector
from loguru import logger
import sys


class Database:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

    def connect(self):
        if self.connection is not None:
            return
        else:
            try:
                self.connection = mysql.connector.connect(
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    database=self.database
                )
                logger.info("Connected to MySQL server")
            except mysql.connector.Error as error:
                logger.error(f"There was an error connecting to MySQL server: {error}")
                sys.exit()

    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None
            logger.info("Connection closed")

    def drop_table(self, table_name):
        cursor = self.connection.cursor()
        cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
        self.connection.commit()
        cursor.close()
        logger.info(f"Table {table_name} dropped")

    def create_table(self, query):
        cursor = self.connection.cursor()
        cursor.execute(query)
        self.connection.commit()
        cursor.close()
        logger.info(f"Table created")

    def execute_query(self, query, params=None):
        try:
            cursor = self.connection.cursor()
            logger.debug("Executing query on MySQL server")
            cursor.execute(query, params)
            self.connection.commit()
            logger.info("Query executed successfully")
            return True
        except mysql.connector.Error as error:
            logger.error(f"There was an error executing the query: {error}")
            self.connection.rollback()
            return False
        finally:
            cursor.close()


    def execute_select_query(self, query):
        try:
            cursor = self.connection.cursor()
            logger.debug("Connected to MySQL server")
            cursor.execute(query)
            result = cursor.fetchall()
        except mysql.connector.Error as error:
            logger.error(f"There was an error executing the query: {error}")
            self.connection.rollback()
        finally:
            cursor.close()
            return result

    def create_artists_table(self, table_name="artists"):
        self.drop_table(table_name)
        artists_ddl = '''CREATE TABLE IF NOT EXISTS artists(
        id INTEGER PRIMARY KEY AUTO_INCREMENT
        , artist VARCHAR(255) NOT NULL
        , last_fm_id VARCHAR(255)
        , discogs_id VARCHAR(255)
        , musicbrainz_id VARCHAR(255)
        )'''
        self.create_table(artists_ddl)

    def create_track_data_table(self, table_name="track_data"):
        self.drop_table("track_data")
        track_data_ddl = '''
        CREATE TABLE IF NOT EXISTS track_data(
        id INTEGER PRIMARY KEY AUTO_INCREMENT
        , title VARCHAR (1000) NOT NULL
        , artist VARCHAR (1000) NOT NULL
        , album VARCHAR (1000) NOT NULL
        , added_date VARCHAR (50)
        , filepath VARCHAR (500)
        , location VARCHAR (500)
        , bpm INTEGER
        , genre VARCHAR (1000)
        , artist_id INTEGER
        , FOREIGN KEY (artist_id) REFERENCES artists(id) ON DELETE CASCADE)'''
        self.create_table(track_data_ddl)
        ix_loc ='''CREATE INDEX ix_loc ON track_data (location)'''
        ix_filepath = '''CREATE INDEX ix_fileath on track_data (filepath)'''
        ix_bpm = '''CREATE INDEX ix_bpm on track_data (bpm)'''
        self.execute_query(ix_loc)
        self.execute_query(ix_filepath)
        self.execute_query(ix_bpm)

    def create_history_table(self, table_name="history"):
        self.drop_table("history")
        history_ddl = '''
        CREATE TABLE IF NOT EXISTS history(
        id INTEGER PRIMARY KEY AUTO_INCREMENT
        , tx_date VARCHAR (255)
        , records INTEGER (6))'''
        self.create_table(history_ddl)

    def create_tags_table(self):
        self.drop_table("tags")
        tags_ddl = '''
        CREATE TABLE IF NOT EXISTS tags(
        id INTEGER PRIMARY KEY AUTO_INCREMENT
        , tag VARCHAR (1000) NOT NULL
        , artist_id INTEGER
        , FOREIGN KEY (artist_id) REFERENCES artists(id) ON DELETE CASCADE)'''
        self.create_table(tags_ddl)