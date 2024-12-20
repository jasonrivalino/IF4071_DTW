import os
from scipy.spatial.distance import euclidean, cityblock, chebyshev, cosine, mahalanobis
import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from mfcc import extract_mfcc

# Function to calculate various distances
def calculate_distances(test_mfcc, template_mfccs, cov_inv=None):
    distances = {}
    for vowel, template_mfcc in template_mfccs.items():
        # Euclidean Distance
        distances[vowel] = {
            "euclidean": euclidean(test_mfcc.flatten(), template_mfcc.flatten()),
            "manhattan": cityblock(test_mfcc.flatten(), template_mfcc.flatten()),
            "cosine": cosine(test_mfcc.flatten(), template_mfcc.flatten()),
            "chebyshev": chebyshev(test_mfcc.flatten(), template_mfcc.flatten()),
        }
        if cov_inv is not None:
            distances[vowel]["mahalanobis"] = mahalanobis(
                test_mfcc.flatten(), template_mfcc.flatten(), cov_inv
            )
    return distances

# Function to train and test neural network
def train_neural_network(X, y):
    # Preprocess data
    scaler = StandardScaler()
    X = scaler.fit_transform(X)

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Neural Network
    clf = MLPClassifier(hidden_layer_sizes=(100,), max_iter=500, random_state=42)
    clf.fit(X_train, y_train)

    # Test model
    y_pred = clf.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Neural Network Accuracy: {accuracy * 100:.2f}%")

    return clf, scaler

# Main comparison function
def compare_with_all_metrics(average_templates, test_files, cov_inv=None):
    results = {}
    correct_count = 0
    total_count = 0

    for testfile in test_files:
        test_vowel = os.path.basename(testfile).split(' ')[0]
        test_mfcc = extract_mfcc(testfile)
        distances = calculate_distances(test_mfcc, average_templates, cov_inv)

        # Find the closest match based on each metric
        for metric in ["euclidean", "manhattan", "cosine", "chebyshev", "mahalanobis"]:
            sorted_distances = sorted(distances.items(), key=lambda x: x[1].get(metric, float("inf")))
            closest_vowel = sorted_distances[0][0]
            if metric not in results:
                results[metric] = []
            results[metric].append((testfile, closest_vowel, closest_vowel == test_vowel))

        total_count += 1

    # Calculate accuracy for each metric
    accuracies = {metric: sum(1 for r in results[metric] if r[2]) / total_count * 100 for metric in results}
    print("Accuracy per metric:")
    for metric, accuracy in accuracies.items():
        print(f"{metric.capitalize()} Accuracy: {accuracy:.2f}%")

    return results, accuracies
