import mysql.connector
import csv
import os
import configparser


#  TODO Find a way to use the config to provide database connection info
#  TODO Recreate the connect func

config = configparser.ConfigParser()
config.read('/Users/jay/Documents/python_projects/bpm_swarm1/config.ini')

database = config['MYSQL']['db_database']
db_path = config['MYSQL']['db_path']
db_user = config['MYSQL']['db_user']
db_password = config['MYSQL']['db_pwd']


def create_track_db():
    """
    Creates a SQLite database for track data.

    Parameters:
    None

    Returns:
    None
    """
    conn = mysql.connector.connect(
        host="athena.eagle-mimosa.ts.net",
        user="jay",
        password="d0ghouse",
        database="bpm_swarm1"
    )
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS track_data
                 (id INTEGER AUTO_INCREMENT PRIMARY KEY
                 , title VARCHAR (100)
                 , artist VARCHAR (100)
                 , album VARCHAR (100)
                 , genre VARCHAR (50)
                 , added_date VARCHAR (50)
                 , filepath VARCHAR (200)
                 , location VARCHAR (200)
                 , schroeder_id INTEGER
                 , woodstock_id INTEGER
                 , bpm FLOAT )''')
    conn.commit()
    conn.close()
    print("Created track_data table!")


def restart():
    conn = mysql.connector.connect(
        host="athena.eagle-mimosa.ts.net",
        user="jay",
        password="d0ghouse",
        database="bpm_swarm1"
    )
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS track_data")
    c.close()


def insert_tracks(csv_file):
    """
    Inserts track data from a CSV file into the SQLite database.

    Parameters:
    csv_file (str): The path to the CSV file.

    Returns:
    None
    """
    conn = mysql.connector.connect(
        host="athena.eagle-mimosa.ts.net",
        user="jay",
        password="d0ghouse",
        database="bpm_swarm1"
    )
    c = conn.cursor()
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            c.execute("INSERT INTO track_data (title, artist, album, genre, "
                      "added_date, filepath, location, woodstock_id)VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                      (row['title'], row['artist'], row['album'], row['genre'],
                       row['added_date'], row['filepath'], row['location'], row['woodstock_id']))
    conn.commit()
    conn.close()
    print("Inserted track records in database!")


def get_id_location():
    """
    Gets the track ID and location from the SQLite database.

    Parameters:
    DATABASE (str): The path to the SQLite database.

    Returns:
    list: A list of tuples containing the track ID and location.
    """
    conn = mysql.connector.connect(
        host="athena.eagle-mimosa.ts.net",
        user="jay",
        password="d0ghouse",
        database="bpm_swarm1"
    )
    c = conn.cursor()
    c.execute("SELECT id, woodstock_id, location FROM track_data")
    results = c.fetchall()
    conn.close()
    print("Queried DB for id and location!")
    return results


def export_results(results: list, file_path: str = 'id_location.csv'):
    """
    Export the results of a query to a CSV file. 'results' is a list of tuples.
    :param results: List of tuples containing the data to be written to CSV
    :param file_path: Path to the CSV file
    :return: None
    """
    file_exists = os.path.isfile(file_path)

    with open(file_path, 'a', newline='') as csvfile:
        fieldnames = ['id', 'woodstock_id', 'location']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write the header only if the file does not exist
        if not file_exists:
            writer.writeheader()

        # Iterate over each tuple in the results list
        for element in results:
            # Convert the tuple to a dictionary
            row_dict = dict(zip(fieldnames, element))
            # Write the dictionary to the CSV
            writer.writerow(row_dict)
    print("Exported ID and Location to CSV!")