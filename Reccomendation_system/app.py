from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import sqlite3

# Create a FastAPI instance
app = FastAPI()

# Define the database connection function
def get_product_data():
    conn = sqlite3.connect("product_database.db")  # Change this to your database path
    query = "SELECT ProductName, ProductPrice, Offers, ProductRating FROM products"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def preprocess_data(df):
    # Prepare the data for K-means clustering
    # Use all available numerical attributes for clustering
    X = df.select_dtypes(include=[np.number])

    return X

def train_unsupervised_model(X):
    # Apply K-means clustering to classify products into three categories
    num_clusters = 3
    kmeans_model = KMeans(n_clusters=num_clusters, random_state=42)
    kmeans_model.fit(X)

    return kmeans_model

@app.on_event("startup")
def startup_event():
    df = get_product_data()
    X = preprocess_data(df)
    global kmeans_model
    kmeans_model = train_unsupervised_model(X)

# Route to classify product
class ProductAttributes(BaseModel):
    ProductPrice: float
    Offers: str
    ProductRating: float

@app.post("/classify_product/")
def classify_product(product_data: ProductAttributes):
    # Prepare the data for clustering
    X_product = pd.DataFrame([product_data.dict()])

    # Remove '%' and 'off' from the 'Offers' column and convert it to float
    X_product['Offers'] = X_product['Offers'].replace(r'%\s*off', '', regex=True).astype(float)

    # Use the trained model to predict the cluster (category) for the product
    cluster = kmeans_model.predict(X_product)

    # Return the predicted cluster as the response
    return {"category": int(cluster[0])}

@app.get("/cluster_products/")
def cluster_products():
    cluster_wise_products = {}
    for cluster_id in range(kmeans_model.n_clusters):
        products_in_cluster = df[df['Cluster'] == cluster_id]['ProductName'].tolist()
        cluster_wise_products[f"Cluster {cluster_id}"] = products_in_cluster

    return cluster_wise_products

if __name__ == "__main__":
    # Run the FastAPI app using Uvicorn server
    # By default, it runs on http://127.0.0.1:8000/
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
