import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib

# 設定ファイルからパスをインポート
from config import DATA_PATH, MODEL_PATH

def train_model():
    """
    Reads data, trains the model, and saves it to the path specified in config.
    """
    # Load data
    data = pd.read_csv(DATA_PATH)

    # Feature Engineering: One-hot encode categorical variable
    data_encoded = pd.get_dummies(data, columns=['day_of_week'])

    # Define features (X) and target (y)
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
    joblib.dump(model_payload, MODEL_PATH)
    print(f"Model trained and saved as {MODEL_PATH}")

if __name__ == '__main__':
    train_model()