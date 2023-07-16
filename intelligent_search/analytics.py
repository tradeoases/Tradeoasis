import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity


def generate_cosine_similarity_matrix(embeddings):
    similarity_matrix = cosine_similarity(embeddings)
    return similarity_matrix


def plot_cosine_similarity_matrix(similarity_matrix):
    plt.imshow(similarity_matrix, cmap='hot', interpolation='nearest')
    plt.colorbar()
    plt.title("Cosine Similarity Matrix")
    plt.show()


def plot_search_results_distribution(search_results):
    result_counts = {result: search_results.count(result) for result in search_results}
    result_labels = list(result_counts.keys())
    result_values = list(result_counts.values())

    plt.bar(result_labels, result_values)
    plt.title("Search Results Distribution")
    plt.xlabel("Search Result")
    plt.ylabel("Frequency")
    plt.xticks(rotation=45)
    plt.show()


def plot_search_results_distribution_with_threshold(search_results, threshold):
    result_counts = {result: search_results.count(result) for result in search_results}
    result_labels = list(result_counts.keys())
    result_values = list(result_counts.values())

    plt.bar(result_labels, result_values)
    plt.title("Search Results Distribution")
    plt.xlabel("Search Result")
    plt.ylabel("Frequency")
    plt.xticks(rotation=45)
    plt.axhline(y=threshold, color='r', linestyle='-')
    plt.show()


# analyse the search results
def analyse_search_results(search_results):
    # Plot the distribution of search results
    plot_search_results_distribution(search_results)

    # Calculate the percentage of each search result
    result_counts = {result: search_results.count(result) for result in search_results}
    total_results = len(search_results)
    result_percentages = {result: result_counts[result] / total_results * 100 for result in result_counts.keys()}
    print(result_percentages)

    # Plot the distribution of search results with a threshold
    plot_search_results_distribution_with_threshold(search_results, 10)

    # Calculate the percentage of each search result with a threshold
    threshold = 10
    total_results_above_threshold = sum(
        [result_counts[result] for result in result_counts.keys() if result_counts[result] > threshold])
    result_percentages_above_threshold = {result: result_counts[result] / total_results_above_threshold * 100 for result
                                          in result_counts.keys() if result_counts[result] > threshold}
    print(result_percentages_above_threshold)

# usage of this file
# # Perform analytics and generate graphs
# embeddings = search_algorithm.index
#
# # Generate and plot the cosine similarity matrix
# similarity_matrix = generate_cosine_similarity_matrix(embeddings)
# plot_cosine_similarity_matrix(similarity_matrix)
#
# # Plot the search results distribution
# plot_search_results_distribution(search_results)
#
# # Calculate the percentage of each search result
# search_results_percentage = [search_results.count(result) / len(search_results) * 100 for result in search_results]
# print(search_results_percentage)
#
# # Perform other analytics tasks...
# analyse_search_results(search_results)
