def generate_data():
    import setup_path 
    import airsim
    import time
    from cassandra.cluster import Cluster
    from cassandra import ConsistencyLevel
    from cassandra.query import SimpleStatement
    import json
    import random
    import logging

    # setting up logging
    logging.basicConfig(filename='drone_simulator.log', level=logging.INFO)

    # connect to the AirSim simulator 
    client = airsim.MultirotorClient()
    client.confirmConnection()
    client.enableApiControl(True)
    client.armDisarm(True)

    # connect to Cassandra cluster
    cluster = Cluster(['127.0.0.1'])  # replace with your Cassandra node IP
    session = cluster.connect()

    # create keyspace and table if they don't exist
    session.execute("""
        CREATE KEYSPACE IF NOT EXISTS drone_data 
        WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 1 };
    """)
    session.execute("""
        CREATE TABLE IF NOT EXISTS drone_data.telemetry (
            timestamp timestamp,
            drone_id text,
            latitude double,
            longitude double,
            altitude double,
            speed map<text, double>,
            orientation map<text, double>,
            battery_level double,
            environment map<text, double>,
            PRIMARY KEY (drone_id, timestamp)
        );
    """)
    session.set_keyspace('drone_data')

    # takeoff
    client.takeoffAsync().join()

    # List of drone IDs (expand or modify based on your simulation)
    drones = ["drone_001", "drone_002", "drone_003"]

    while True:
        for drone in drones:
            try:
                # get state of the drone
                drone_state = client.getMultirotorState()

                # get current position, orientation, speed and timestamp
                pos = drone_state.kinematics_estimated.position
                orient = drone_state.kinematics_estimated.orientation
                speed = drone_state.kinematics_estimated.linear_velocity
                timestamp = drone_state.timestamp

                # get battery level
                battery_level = client.getBatteryInfo().remaining_capacity

                # get current weather conditions (in real implementation, you might connect to a weather API here)
                weather_conditions = {"temperature": 20, "humidity": 50, "wind_speed": 5, "precipitation": 0}

                # prepare data
                data = {
                    "timestamp": timestamp,
                    "drone_id": drone,
                    "latitude": pos.x_val,
                    "longitude": pos.y_val,
                    "altitude": pos.z_val,
                    "speed": {"x_val": speed.x_val, "y_val": speed.y_val, "z_val": speed.z_val},
                    "orientation": {"pitch": orient.x_val, "roll": orient.y_val, "yaw": orient.z_val},
                    "battery_level": battery_level,
                    "environment": weather_conditions
                }

                # send data to Cassandra
                query = SimpleStatement(
                    """
                    INSERT INTO telemetry (timestamp, drone_id, latitude, longitude, altitude, speed, orientation, battery_level, environment)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    consistency_level=ConsistencyLevel.LOCAL_ONE
                )
                session.execute(query, (data['timestamp'], data['drone_id'], data['latitude'], data['longitude'], data['altitude'],
                                        data['speed'], data['orientation'], data['battery_level'], data['environment']))
                logging.info(f'Data for {drone} sent to Cassandra')
                
                # move drone to a new random location
                client.moveToPositionAsync(pos.x_val + random.randint(-10, 10), pos.y_val + random.randint(-10, 10), pos.z_val, 5).join()
            except Exception as e:
                logging.error(f'Error occurred: {e}')
            finally:
                # add delay between data collection
                time.sleep(5)

    # Close Cassandra connection
    cluster.shutdown()
