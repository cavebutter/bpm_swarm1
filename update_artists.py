from loguru import logger
import mysql.connector
import sys
import db.db_functions
import db.update_db

def configure_logging():
    logger.remove()
    logger.add(sys.stderr, level="DEBUG")
    logger.add('run.log', level="DEBUG")

if __name__ == "__main__":
    configure_logging()
    # db.db_functions.create_artists_table()
    # db.db_functions.populate_artists_table()
    # db.db_functions.add_artist_id_column()
    db.db_functions.populate_artist_id_column()