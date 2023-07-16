import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer


class IntelligentSearch:
    def __init__(self, documents):
        self.documents = documents
        self.model = None
        self.index = None

    def preprocess_documents(self):
        # Perform any necessary preprocessing on the documents, such as cleaning or tokenization
        self.documents = [document.lower() for document in self.documents]

    def build_index(self):
        # Build an index using advanced AI-powered algorithms such as sentence embeddings
        self.model = SentenceTransformer('xlm-roberta-base')
        embeddings = self.model.encode(self.documents)
        self.index = np.array(embeddings)

    def search(self, query, top_k=5):
        # Search for documents based on the query using the built index
        query_embedding = self.model.encode([query])[0]
        similarity_scores = cosine_similarity([query_embedding], self.index)[0]
        sorted_indices = np.argsort(similarity_scores)[::-1][:top_k]

        results = []
        for idx in sorted_indices:
            results.append(self.documents[idx])

        return results


# Example usage:
documents = [
    "Product A is a cutting-edge B2B solution for businesses in the technology sector. It offers seamless integration with existing systems, advanced security features, and real-time collaboration tools.",
    "Our flagship product, Product B, is a comprehensive B2B platform designed to streamline operations. It includes modules for inventory management, order processing, and supplier relationship management.",
    "Product C is an innovative B2B marketplace that connects buyers and suppliers. It provides a user-friendly interface, personalized recommendations, and secure payment options.",
    "With Product D, businesses can optimize their B2B marketing strategies. It offers advanced analytics, lead generation tools, and marketing automation capabilities.",
    "Product E is a powerful B2B CRM (Customer Relationship Management) software. It enables businesses to manage customer interactions, track sales, and enhance customer satisfaction.",
    "Product F is a cloud-based B2B collaboration tool. It facilitates seamless communication, file sharing, and project management among business partners.",
    "Product G is an AI-powered B2B chatbot that automates customer support. It provides instant responses, 24/7 availability, and intelligent routing of inquiries.",
    "Product H, businesses can streamline B2B logistics and supply chain management. It offers features such as real-time tracking, inventory optimization, and route planning.",
    "Product I is a B2B e-commerce platform tailored for wholesale businesses. It includes features like bulk ordering, pricing tiers, and integration with ERP systems.",
    "Product J is a B2B payment gateway that enables secure and efficient transactions. It supports multiple payment methods, fraud detection, and customizable payment workflows.",
    "Product L is a B2B sales enablement platform. It equips sales teams with tools for content"
]

search_algorithm = IntelligentSearch(documents)
search_algorithm.preprocess_documents()
search_algorithm.build_index()

query = "tools for content"

search_results = search_algorithm.search(query)
print("Search Results:")
for result in search_results:
    print(result)
