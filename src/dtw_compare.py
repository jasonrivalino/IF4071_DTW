from fastdtw import fastdtw
from scipy.spatial.distance import euclidean, cityblock, chebyshev, cosine, mahalanobis

# Dynamic Time Warping (DTW) function with various distance metrics as a metric parameter

# DTW implementation using the fastdtw library
def dtw_library_euclidean(x, y):
    distance, _ = fastdtw(x, y, dist=euclidean)
    return distance

# DTW implementation using the fastdtw library with Manhattan distance
def dtw_library_manhattan(x, y):
    distance, _ = fastdtw(x, y, dist=cityblock)
    return distance

# DTW implementation using the fastdtw library with Chebyshev distance
def dtw_library_chebyshev(x, y):
    distance, _ = fastdtw(x, y, dist=chebyshev)
    return distance

# DTW implementation using the fastdtw library with Cosine distance
def dtw_library_cosine(x, y):
    distance, _ = fastdtw(x, y, dist=cosine)
    return distance

# DTW implementation using the fastdtw library with Mahalanobis distance
def mahalanobis_distance(u, v, cov_inv):
    return mahalanobis(u, v, cov_inv)

def dtw_library_mahalanobis(x, y, cov_inv):
    def custom_mahalanobis(u, v):
        return mahalanobis_distance(u, v, cov_inv)

    distance, _ = fastdtw(x, y, dist=custom_mahalanobis)
    return distance