import numpy as np


def rotate_list(arr, n, dir="left"):
    """
    Rotate array elements left or right by n positions.

    Args:
        arr: Input array
        n: Number of positions to rotate (wraps around if n > len (arr))
        dir: Rotation direction ('left' or 'right')

    Returns:
        Rotated array
    """
    if len(arr) == 0:
        return arr

    arr = np.array(arr)
    n = n % len(arr)

    if dir == "left":
        return np.concatenate((arr[n:], arr[:n]))
    elif dir == "right":
        return np.concatenate((arr[-n:], arr[:-n]))
    else:
        raise ValueError("Direction must be 'left' or 'right'!")
