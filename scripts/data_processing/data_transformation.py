from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import numpy as np

# Global variable to hold total distance traveled
total_distance = 0

def create_cassandra_session():
    # replace these with your details
    cloud_config= {
        'secure_connect_bundle': '/path/to/secure-connect-database_name.zip'
    }
    auth_provider = PlainTextAuthProvider('username', 'password')
    cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
    session = cluster.connect()
    
    return session

def close_cassandra_session(session):
    session.shutdown()

def process_data():
    session = create_cassandra_session()

    # read data from Cassandra
    rows = session.execute("SELECT * FROM drone_telemetry ORDER BY time")
    processed_rows = []

    for row in rows:
        # clean data (not much to do since our data is generated)
        clean_row = clean_data(row)

        # perform transformations (e.g., compute total distance)
        transformed_row = transform_data(clean_row)

        processed_rows.append(transformed_row)

    # write processed data back to Cassandra (or to another data store)
    for row in processed_rows:
        session.execute(
            """
            INSERT INTO processed_drone_telemetry (id, time, position, orientation, battery, velocity, total_distance)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, 
            (row['id'], row['time'], row['position'], row['orientation'], row['battery'], row['velocity'], row['total_distance'])
        )

    close_cassandra_session(session)

def clean_data(row):
    # since our data is generated, we might not need to do much cleaning
    return row

def transform_data(row):
    global total_distance
    # compute total distance from velocity data and add it to the row
    total_distance += np.linalg.norm(row['velocity'])
    row['total_distance'] = total_distance
    return row

def get_processed_data(limit=10):
    """Fetch a number of processed data records from the database"""
    session = create_cassandra_session()

    # Fetch the data from Cassandra
    rows = session.execute(f"SELECT * FROM processed_drone_telemetry LIMIT {limit}")
    processed_data = [row for row in rows]

    close_cassandra_session(session)
    return processed_data


if __name__ == "__main__":
    process_data()
