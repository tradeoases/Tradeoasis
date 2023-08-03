import pandas as pd
import numpy as np
import tensorflow as tf

# Load the saved model
model = tf.keras.models.load_model("fraud_detection_model")

# Function to create mock data with both fraudulent and non-fraudulent transactions
def create_mock_data(num_samples, fraud_ratio=0.1):
    num_fraudulent = int(num_samples * fraud_ratio)
    num_non_fraudulent = num_samples - num_fraudulent

    # Generate random data for non-fraudulent transactions (class 0)
    non_fraudulent_data = np.random.randn(num_non_fraudulent, 30)
    non_fraudulent_labels = np.zeros(num_non_fraudulent)

    # Generate random data for fraudulent transactions (class 1)
    fraudulent_data = np.random.randn(num_fraudulent, 30)
    fraudulent_labels = np.ones(num_fraudulent)

    # Combine both non-fraudulent and fraudulent data
    data = np.vstack((non_fraudulent_data, fraudulent_data))
    labels = np.concatenate((non_fraudulent_labels, fraudulent_labels))

    # Shuffle the data and create a DataFrame
    combined_data = np.c_[data, labels]
    np.random.shuffle(combined_data)

    return pd.DataFrame(combined_data, columns=[f"Feature_{i+1}" for i in range(30)] + ["Class"])

# Mock data for testing (100 samples with 10% fraudulent transactions)
num_samples = 100
fraud_ratio = 0.1
mock_data = create_mock_data(num_samples, fraud_ratio)

# Separate features and labels
features = mock_data.drop("Class", axis=1)
labels = mock_data["Class"]

# Normalize the features
features = tf.keras.utils.normalize(features, axis=1)

# Make predictions on the mock data
predictions = model.predict(features)
predictions = np.round(predictions)  # Round the predictions to 0 or 1

# Display the predictions
print("Predictions:")
for i, pred in enumerate(predictions):
    if pred == 0:
        print(f"Sample {i + 1}: Non-Fraudulent Transaction")
    else:
        print(f"Sample {i + 1}: Fraudulent Transaction")
