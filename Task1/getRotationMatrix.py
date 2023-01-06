import numpy as np
from matplotlib import pyplot as plt

def rotation_matrix_from_vectors(vec1, vec2):
   
    a, b = (vec1 / np.linalg.norm(vec1)).reshape(3), (vec2 / np.linalg.norm(vec2)).reshape(3)
    v = np.cross(a, b)
    c = np.dot(a, b)
    s = np.linalg.norm(v)
    kmat = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
    rotation_matrix = np.eye(3) + kmat + kmat.dot(kmat) * ((1 - c) / (s ** 2))
    return rotation_matrix

# Test

# vec1 = np.array([1.0,1,1])
# vec2 = vec1

# vec1 /= np.linalg.norm(vec1)
# vec2 /= np.linalg.norm(vec2)

# mat = rotation_matrix_from_vectors(vec1, vec2)
# vec1_rot = mat.dot(vec1)
# assert np.allclose(vec1_rot/np.linalg.norm(vec1_rot), vec2/np.linalg.norm(vec2))

# print(vec1_rot/np.linalg.norm(vec1_rot))
# print(vec1_rot)
# print(vec2)