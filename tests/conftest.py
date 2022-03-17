"""
The pytest conftest file for fixtures.
"""


from PIL import Image
from pytest import fixture
import numpy as np

from local_stats.cluster import Cluster


@fixture
def raw_image_array() -> np.ndarray:
    """
    Returns numpy array representing a raw image.
    """
    return np.array(Image.open("resources/pixis-20.tiff"))


@fixture
def simple_cluster() -> Cluster:
    """
    Returns a simple cluster with a few simple pixel values that it's easy to
    do test maths with.
    """
    pixel_coords = np.zeros((3, 2))
    pixels_x, pixels_y = np.arange(3), np.arange(1, 4)
    pixel_coords[:, 0], pixel_coords[:, 1] = pixels_x, pixels_y
    return Cluster(pixel_coords)
