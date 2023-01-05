import numpy as np

def quat_from_vectors(vec1, vec2):
    """
    Returns the quaternion that rotates vector `vec1` to vector `vec2`.
    """
    # Normalize input vectors
    vec1 = vec1 / np.linalg.norm(vec1)
    vec2 = vec2 / np.linalg.norm(vec2)
    
    # Calculate rotation axis
    axis = np.cross(vec1, vec2)
    axis_norm = np.linalg.norm(axis)
    if axis_norm < 1e-10:
        # Vectors are already aligned, return identity quaternion
        return np.array([1, 0, 0, 0])
    axis = axis / axis_norm
    
    # Calculate rotation angle
    angle = np.arccos(np.dot(vec1, vec2))
    
    # Calculate quaternion
    s = np.sin(angle / 2)
    q = np.concatenate(([np.cos(angle / 2)], axis * s))
    
    return q

def rotate_vector(vec, quat):
    """
    Rotates a 3D vector `vec` using the quaternion `quat`.
    """
    # Convert vector to quaternion with w = 0
    vec_quat = np.concatenate((vec, [0]))
    
    # Rotate vector
    rotated_quat = quat_mult(quat, quat_mult(vec_quat, quat_conj(quat)))
    
    # Return rotated vector
    return rotated_quat[:3]

def quat_mult(q1, q2):
    """
    Multiplies quaternion `q1` by quaternion `q2`.
    """
    w1, x1, y1, z1 = q1
    w2, x2, y2, z2 = q2
    w = w1*w2 - x1*x2 - y1*y2 - z1*z2
    x = w1*x2 + x1*w2 + y1*z2 - z1*y2
    y = w1*y2 - x1*z2 + y1*w2 + z1*x2
    z = w1*z2 + x1*y2 - y1*x2 + z1*w2
    return np.array([w, x, y, z])

def quat_conj(q):
    """
    Returns the conjugate of quaternion `q`.
    """
    w, x, y, z = q
    return np.array([w, -x, -y, -z])

