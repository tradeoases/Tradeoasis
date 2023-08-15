import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score

# Load the dataset of anonymized credit card transactions from Cloud Academy
df = pd.read_csv("https://clouda-labs-assets.s3-us-west-2.amazonaws.com/fraud-detection/creditcard.csv.zip")

# Split the dataset into features (X) and labels (y)
X = df.drop("Class", axis=1)
y = df["Class"]

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Normalize the features
X_train = tf.keras.utils.normalize(X_train, axis=1)
X_test = tf.keras.utils.normalize(X_test, axis=1)

# Build a custom fraud detection model
model = tf.keras.Sequential([
    tf.keras.layers.Dense(64, activation="relu", input_shape=(X_train.shape[1],)),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(32, activation="relu"),
    tf.keras.layers.Dense(1, activation="sigmoid")
])

# Compile the model with binary crossentropy loss and Adam optimizer
model.compile(loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"])

# Train the model for 10 epochs with a batch size of 32
model.fit(X_train, y_train, epochs=10, batch_size=32)

# Evaluate the model on the test set and print the results
y_pred = model.predict(X_test)
y_pred = np.round(y_pred)  # Round the predictions to 0 or 1
cm = confusion_matrix(y_test, y_pred)  # Compute the confusion matrix
acc = accuracy_score(y_test, y_pred)  # Compute the accuracy score
prec = precision_score(y_test, y_pred)  # Compute the precision score
rec = recall_score(y_test, y_pred)  # Compute the recall score

print("Confusion matrix:\n", cm)
print("Accuracy: {:.2f}%".format(acc * 100))
print("Precision: {:.2f}%".format(prec * 100))
print("Recall: {:.2f}%".format(rec * 100))

# Save the trained model
model.save("fraud_detection_model")
