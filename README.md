# Flight Optimizer - Drone Flight Optimization using Machine Learning

Flight Optimizer is a project that simulates drone flights and optimizes flight paths. It utilizes a combination of AirSim, Apache Cassandra, Apache Airflow, TensorFlow, and Flask to simulate, collect, process, and model flight data, and then apply those models to optimize flight paths.

## Overview

Flight Optimizer operates in several steps:

1. **Drone Simulation**: Simulates drone flights using AirSim, generating telemetry data which includes position, orientation, and battery level.

2. **Data Collection**: Collects the simulated telemetry data and stores it in a Cassandra database.

3. **Data Processing**: Processes the raw telemetry data, calculating velocity and total distance traveled.

4. **Model Training**: Trains a TensorFlow model to predict flight duration based on the processed telemetry data.

5. **Scoring Service**: Provides a Flask app that uses the trained model to score new flight paths, predicting their flight duration.

6. **Flight Optimization**: Optimizes flight paths based on the scores from the scoring service, minimizing flight duration and battery usage.

The entire pipeline is orchestrated using Apache Airflow.

## Setup and Usage

Instructions for setting up and running each part of the project are located in the respective directories. Please refer to them for detailed information.

## Contributing

Contributions are welcome. Please submit a pull request with any enhancements, fixes, or features.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
