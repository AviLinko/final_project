import numpy as np

def quaternion_from_vectors(vec1, vec2):
    vec1 = vec1 / np.linalg.norm(vec1)
    vec2 = vec2 / np.linalg.norm(vec2)
    w = np.sqrt(np.dot(vec1, vec1) * np.dot(vec2, vec2)) + np.dot(vec1, vec2)
    xyz = np.cross(vec1, vec2)
    return np.array([w, xyz[0], xyz[1], xyz[2]])