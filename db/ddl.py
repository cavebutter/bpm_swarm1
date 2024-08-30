import mysql.connector
from loguru import logger
import sys

def create_artists_table():
    """
    Creates an artists table in the MySQL database. Should only be called once
    at the beginning of the program.
    Returns:

    """
    try:
        conn = mysql.connector.connect(
        host="athena.eagle-mimosa.ts.net",
        user="jay",
        password="d0ghouse",
        database="bpm_swarm1"
    )
        logger.debug("Connected to MySQL server")
    except Exception as e:
        logger.error(f"There was an error connecting to MySQL server: {e}")
        sys.exit()
    c = conn.cursor()
    c.execute('''DROP TABLE IF EXISTS artists''')
    c.execute('''CREATE TABLE IF NOT EXISTS artists(
    id INTEGER PRIMARY KEY AUTO_INCREMENT
    , artist VARCHAR(255) NOT NULL
    , last_fm_id VARCHAR(255)
    , discogs_id VARCHAR(255)
    , musicbrainz_id VARCHAR(255)
    )''')
    conn.commit()
    conn.close()
    logger.info("Created artists table")


def create_track_data_table():

    try:
        conn = mysql.connector.connect(
            host="athena.eagle-mimosa.ts.net",
            user="jay",
            password="d0ghouse",
            database="bpm_swarm1"
        )
        logger.info("Connected to MySQL server")
    except Exception as e:
        logger.error(f"There was an error connecting to MySQL server: {e}")
        sys.exit()
    c = conn.cursor()
    c.execute('''DROP TABLE IF EXISTS track_data''')
    c.execute('''
    CREATE TABLE IF NOT EXISTS track_data(
    id INTEGER PRIMARY KEY AUTO_INCREMENT
    , title VARCHAR (1000) NOT NULL
    , artist VARCHAR (1000) NOT NULL
    , album VARCHAR (1000) NOT NULL
    , added_date VARCHAR
    , location VARCHAR (1000)
    , location VARCHAR (1000)
    , bpm INTEGER
    , genre VARCHAR (1000)
    , artist_id INTEGER
    , FOREIGN KEY (artist_id) REFERENCES artists(id) ON DELETE CASCADE
    
    ''')
    c.execute('''CREATE INDEX ix_loc ON track_data (location)''')
    c.execute('''CREATE INDEX ix_fileath on track_data (filepath)''')
    c.execute('''CREATE INDEX ix_bpm on track_data (bpm)''')
    conn.commit()
    conn.close()
    logger.info("Created track_data table")


def create_history_table():
    try:
        conn = mysql.connector.connect(
            host="athena.eagle-mimosa.ts.net",
            user="jay",
            password="d0ghouse",
            database="bpm_swarm1"
        )
        logger.info("Connected to MySQL server")
    except Exception as e:
        logger.error(f"There was an error connecting to MySQL server: {e}")
        sys.exit()
    c = conn.cursor()
    c.execute('''DROP TABLE IF EXISTS history''')
    c.execute('''
    CREATE TABLE IF NOT EXISTS history(
    id INTEGER PRIMARY KEY AUTO_INCREMENT
    , date VARCHAR
    , records INTEGER''')
    conn.commit()
    conn.close()
    logger.info("Created history table")


def create_tags_table():
    try:
        conn = mysql.connector.connect(
            host="athena.eagle-mimosa.ts.net",
            user="jay",
            password="d0ghouse",
            database="bpm_swarm1"
        )
        logger.info("Connected to MySQL server")
    except Exception as e:
        logger.error(f"There was an error connecting to MySQL server: {e}")
        sys.exit()
    c = conn.cursor()
    c.execute('''DROP TABLE IF EXISTS tags''')
    c.execute('''
    CREATE TABLE IF NOT EXISTS tags(
    id INTEGER PRIMARY KEY AUTO_INCREMENT
    , tag VARCHAR
    , artist_id INTEGER
    , FOREIGN KEY (artist_id) REFERENCES artists(id) ON DELETE CASCADE''')