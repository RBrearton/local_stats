"""
This file contains tests for the cluster module's Cluster class.
"""

# Obviously we want to test 'private' attributes.
# pylint: disable=protected-access

import numpy as np

from local_stats.cluster import Cluster


def test_init():
    """
    Classic test to blow up if attribute names change.
    """
    cluster = Cluster([])
    assert len(cluster._arr) == 0


def test_mean(simple_cluster: Cluster):
    """
    Make sure that the mean is being calculated correctly.
    """
    assert simple_cluster.mean[0] == 1
    assert simple_cluster.mean[1] == 2


def test_size(simple_cluster: Cluster):
    """
    Make sure we're calculating the size of a cluster properly.
    """
    assert simple_cluster.size == 3


def test_pixel_indices(simple_cluster: Cluster):
    """
    Make sure that the pixel indices are being returned correctly.
    """
    assert isinstance(simple_cluster.pixel_indices, tuple)
    assert (simple_cluster.pixel_indices[0] == np.array([0, 1, 2])).all()
    assert (simple_cluster.pixel_indices[1] == np.array([1, 2, 3])).all()


def test_intensity(simple_cluster: Cluster):
    """
    Make sure that we can properly calculate the area under a cluster.
    """
    test_img = np.ones((5, 5))

    assert simple_cluster.intensity(test_img) == 3
