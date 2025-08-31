import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib
import os

def train_model():
    """
    Trains the model and saves it to model.pkl.
    """
    # Define paths relative to the script location
    dir_path = os.path.dirname(os.path.realpath(__file__))
    data_path = os.path.join(dir_path, 'sample_data.csv')
    model_path = os.path.join(dir_path, 'model.pkl')

    # Load data
    data = pd.read_csv(data_path)

    # Feature Engineering: One-hot encode categorical variable
    data_encoded = pd.get_dummies(data, columns=['day_of_week'])

    # Define features (X) and target (y)
    # Exclude non-feature columns
    features = [col for col in data_encoded.columns if col not in ['date', 'sales']]
    target = 'sales'

    X = data_encoded[features]
    y = data_encoded[target]

    # Train model
    model = LinearRegression()
    model.fit(X, y)

    # Save model and the columns used for training
    model_payload = {
        'model': model,
        'columns': features
    }
    joblib.dump(model_payload, model_path)
    print(f"Model trained and saved as {model_path}")

if __name__ == '__main__':
    train_model()
