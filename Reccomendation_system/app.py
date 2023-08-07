from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans

# Assuming you have installed Flask and other required libraries
app = Flask(__name__)

# Sample product data for demonstration (you should replace this with data from your database)
data = [
    {"ProductName": "Product A", "ProductPrice": 50.0, "Offers": 10, "ProductRating": 4.5},
    {"ProductName": "Product B", "ProductPrice": 30.0, "Offers": 20, "ProductRating": 3.8},
    {"ProductName": "Product c", "ProductPrice": 20.0, "Offers": 5 , "ProductRating": 3.5}
    # Add more products here...
]
df = pd.DataFrame(data)

# 4. Model Training (K-means Clustering)
# Prepare the data for K-means clustering
# Use all available numerical attributes for clustering
X = df.select_dtypes(include=[np.number])

# Apply K-means clustering to classify products into three categories
num_clusters = 3
kmeans_model = KMeans(n_clusters=num_clusters, random_state=42)
df['Cluster'] = kmeans_model.fit_predict(X)

# 5. Product Classification Endpoint
@app.route('/classify_product', methods=['POST'])
def classify_product():
    # Get product data from the request (Assuming JSON format)
    data = request.get_json()

    # Convert the product data into a DataFrame
    df = pd.DataFrame(data)

    # Prepare the data for K-means clustering
    # Use all available numerical attributes for clustering
    X = df.select_dtypes(include=[np.number])

    # Use the trained model to predict the cluster (category) for the product
    cluster = kmeans_model.predict(X)

    # Return the predicted cluster as the response (Assuming JSON format)
    response = {'category': cluster[0]}
    return jsonify(response)

if __name__ == '__main__':
    # Run the Flask app (debug=True for development)
    app.run(host='0.0.0.0', port=5000, debug=True)
