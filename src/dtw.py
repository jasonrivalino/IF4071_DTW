import numpy as np
from scipy.spatial.distance import cdist

# Dynamic Time Warping (DTW) function to calculate similarity between two feature sets
def dtw(x, y, dist_func='euclidean'):
    cost = cdist(x, y, metric=dist_func)
    # Create a cumulative cost matrix
    acc_cost = np.zeros_like(cost)
    acc_cost[0, 0] = cost[0, 0]

    # Initialize the edges
    for i in range(1, acc_cost.shape[0]):
        acc_cost[i, 0] = cost[i, 0] + acc_cost[i - 1, 0]
    for j in range(1, acc_cost.shape[1]):
        acc_cost[0, j] = cost[0, j] + acc_cost[0, j - 1]

    # Populate the cumulative cost matrix
    for i in range(1, acc_cost.shape[0]):
        for j in range(1, acc_cost.shape[1]):
            acc_cost[i, j] = cost[i, j] + min(acc_cost[i - 1, j],
                                              acc_cost[i, j - 1],
                                              acc_cost[i - 1, j - 1])
    
    return acc_cost[-1, -1]  # Return the final cost (similarity score)