# 2025.02.05

import numpy as np
from typing import Optional, Tuple

def mat_shrink(sa: np.ndarray, no_zero: bool = True) -> np.ndarray:
    """
    Shrinks a 2D NumPy array by removing columns that contain only zero values across all rows.
    Ensures the result has at least two columns unless `no_zero=True` is specified.

    Parameters:
        sa (np.ndarray): Input 2D NumPy array.
        no_zero (bool): If True, removes all-zero columns fully. If False, ensures at least two columns remain.

    Returns:
        np.ndarray: Trimmed array containing only relevant columns.
    """
    # Ensure input is a 2D NumPy array
    if not isinstance(sa, np.ndarray) or sa.ndim != 2:
        raise ValueError("ARG1: Input must be a 2D NumPy array")

    # Find the first and last columns with at least one non-zero value
    non_zero_cols = np.any(sa != 0, axis=0)
    first_nonzero_col = np.argmax(non_zero_cols)  # First column with a non-zero value
    last_nonzero_col = len(non_zero_cols) - np.argmax(non_zero_cols[::-1]) - 1  # Last column with a non-zero value

    # If no valid non-zero columns found, return all columns or at least two if no_zero=False
    if not np.any(non_zero_cols):
        return sa if no_zero else sa[:, :min(2, sa.shape[1])]

    # Ensure at least two columns remain if no_zero=False
    if not no_zero and (last_nonzero_col - first_nonzero_col + 1) < 2:
        last_nonzero_col = min(first_nonzero_col + 1, sa.shape[1] - 1)

    # Slice the array to keep only relevant columns
    return sa[:, first_nonzero_col:last_nonzero_col + 1]

def mat_hshrink_irange(sa: np.ndarray, no_zero: bool = True) -> Optional[Tuple[int, int]]:
    """
    Finds the first and last columns that contain at least one non-zero value in a 2D NumPy array.
    Ensures at least two columns remain unless `no_zero=True` is specified.

    Parameters:
        sa (np.ndarray): Input 2D NumPy array.
        no_zero (bool): If True, removes all-zero columns fully. If False, ensures at least two columns remain.

    Returns:
        Optional[Tuple[int, int]]: A tuple (first_nonzero_col, last_nonzero_col) or None if no non-zero columns exist.
    """
    if sa.size == 0 or sa.ndim != 2:
        raise ValueError("ARG1: Input must be a 2D NumPy array")

    non_zero_cols = np.any(sa != 0, axis=0)
    if not np.any(non_zero_cols):
        return (0, min(1, sa.shape[1] - 1)) if not no_zero else None

    first_nonzero_col = np.argmax(non_zero_cols)
    last_nonzero_col = len(non_zero_cols) - np.argmax(non_zero_cols[::-1]) - 1

    # Ensure at least two columns remain if no_zero=False
    if not no_zero and (last_nonzero_col - first_nonzero_col + 1) < 2:
        last_nonzero_col = min(first_nonzero_col + 1, sa.shape[1] - 1)

    return first_nonzero_col, last_nonzero_col


def mat_hmeanxy(geom: np.ndarray) -> np.ndarray:
    """
    Computes the mean of longitudes and latitudes separately for each shape.

    :param geom: A NumPy array of shape (N, K) where K must be even.
    :return: A NumPy array of shape (N, 2) containing mean longitude and latitude.
    """
    if geom.shape[1] % 2 != 0:
        raise ValueError("Number of columns must be even (pairs of Lon, Lat).")

    # Compute mean separately for even (Lon) and odd (Lat) indexed columns
    mean_lons = np.mean(geom[:, ::2], axis=1)  # Even-indexed columns (0, 2, 4, ...)
    mean_lats = np.mean(geom[:, 1::2], axis=1)  # Odd-indexed columns (1, 3, 5, ...)

    return np.column_stack([mean_lons, mean_lats])

if __name__ == "__main__":
    def nonzero_column_range_test():
        # Example matrix with zero columns at the edges
        sa = np.zeros((5, 7))
        sa[1, 2] = 5.5
        sa[2, 3] = 3.3
        sa[3, 5] = 7.7

        result = mat_hshrink_irange(sa)

        if result is not None:
            print(f"First non-zero column: {result[0]}")
            print(f"Last non-zero column: {result[1]}")
        else:
            print("No non-zero columns found.")


    nonzero_column_range_test()
