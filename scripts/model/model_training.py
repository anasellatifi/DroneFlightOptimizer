from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import pandas as pd
from sklearn.externals import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error

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

def load_data():
    session = create_cassandra_session()

    # read processed data from Cassandra
    rows = session.execute("SELECT * FROM processed_drone_telemetry ORDER BY time")
    data = pd.DataFrame(list(rows))

    close_cassandra_session(session)

    return data

def prepare_data(data):
    # separate features and target
    X = data[['position', 'orientation', 'velocity', 'total_distance']]
    y = data['battery']

    # split data into training set and test set
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    return X_train, X_test, y_train, y_test


def train(X_train, y_train):
    # create and train the model
    model = GradientBoostingRegressor(random_state=42)
    model.fit(X_train, y_train)

    return model

def evaluate(model, X_test, y_test):
    # make predictions on the test set
    predictions = model.predict(X_test)

    # compute MAE
    mae = mean_absolute_error(y_test, predictions)

    return mae

def train_model():
    data = load_data()
    X_train, X_test, y_train, y_test = prepare_data(data)

    model = train(X_train, y_train)

    # Save the trained model
    joblib.dump(model, 'trained_model.pkl')
    
    mae = evaluate(model, X_test, y_test)

    print(f"Mean Absolute Error: {mae}")
