"""
Tests for k-modes clustering algorithm
"""

import pickle
import unittest

import numpy as np
from sklearn.utils.testing import assert_equal

from kmodes.kmodes import KModes
from kmodes.util.dissim import ng_dissim


SOYBEAN = np.array([
    [4, 0, 2, 1, 1, 1, 0, 1, 0, 2, 1, 1, 0, 2, 2, 0, 0, 0, 1, 0, 3, 1, 1, 1, 0, 0, 0, 0,
     4, 0, 0, 0, 0, 0, 0, 'D1'],
    [5, 0, 2, 1, 0, 3, 1, 1, 1, 2, 1, 1, 0, 2, 2, 0, 0, 0, 1, 1, 3, 0, 1, 1, 0, 0, 0, 0,
     4, 0, 0, 0, 0, 0, 0, 'D1'],
    [3, 0, 2, 1, 0, 2, 0, 2, 1, 1, 1, 1, 0, 2, 2, 0, 0, 0, 1, 0, 3, 0, 1, 1, 0, 0, 0, 0,
     4, 0, 0, 0, 0, 0, 0, 'D1'],
    [6, 0, 2, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 2, 2, 0, 0, 0, 1, 1, 3, 1, 1, 1, 0, 0, 0, 0,
     4, 0, 0, 0, 0, 0, 0, 'D1'],
    [4, 0, 2, 1, 0, 3, 0, 2, 0, 2, 1, 1, 0, 2, 2, 0, 0, 0, 1, 0, 3, 1, 1, 1, 0, 0, 0, 0,
     4, 0, 0, 0, 0, 0, 0, 'D1'],
    [5, 0, 2, 1, 0, 2, 0, 1, 1, 0, 1, 1, 0, 2, 2, 0, 0, 0, 1, 1, 3, 1, 1, 1, 0, 0, 0, 0,
     4, 0, 0, 0, 0, 0, 0, 'D1'],
    [3, 0, 2, 1, 0, 2, 1, 1, 0, 1, 1, 1, 0, 2, 2, 0, 0, 0, 1, 1, 3, 0, 1, 1, 0, 0, 0, 0,
     4, 0, 0, 0, 0, 0, 0, 'D1'],
    [3, 0, 2, 1, 0, 1, 0, 2, 1, 2, 1, 1, 0, 2, 2, 0, 0, 0, 1, 0, 3, 0, 1, 1, 0, 0, 0, 0,
     4, 0, 0, 0, 0, 0, 0, 'D1'],
    [6, 0, 2, 1, 0, 3, 0, 1, 1, 1, 1, 1, 0, 2, 2, 0, 0, 0, 1, 0, 3, 1, 1, 1, 0, 0, 0, 0,
     4, 0, 0, 0, 0, 0, 0, 'D1'],
    [6, 0, 2, 1, 0, 1, 0, 1, 0, 2, 1, 1, 0, 2, 2, 0, 0, 0, 1, 0, 3, 1, 1, 1, 0, 0, 0, 0,
     4, 0, 0, 0, 0, 0, 0, 'D1'],
    [6, 0, 0, 2, 1, 0, 2, 1, 0, 0, 1, 1, 0, 2, 2, 0, 0, 0, 1, 1, 0, 3, 0, 0, 0, 2, 1, 0,
     4, 0, 0, 0, 0, 0, 0, 'D2'],
    [4, 0, 0, 1, 0, 2, 3, 1, 1, 1, 1, 1, 0, 2, 2, 0, 0, 0, 1, 0, 0, 3, 0, 0, 0, 2, 1, 0,
     4, 0, 0, 0, 0, 0, 0, 'D2'],
    [5, 0, 0, 2, 0, 3, 2, 1, 0, 2, 1, 1, 0, 2, 2, 0, 0, 0, 1, 0, 0, 3, 0, 0, 0, 2, 1, 0,
     4, 0, 0, 0, 0, 0, 0, 'D2'],
    [6, 0, 0, 1, 1, 3, 3, 1, 1, 0, 1, 1, 0, 2, 2, 0, 0, 0, 1, 0, 0, 3, 0, 0, 0, 2, 1, 0,
     4, 0, 0, 0, 0, 0, 0, 'D2'],
    [3, 0, 0, 2, 1, 0, 2, 1, 0, 1, 1, 1, 0, 2, 2, 0, 0, 0, 1, 0, 0, 3, 0, 0, 0, 2, 1, 0,
     4, 0, 0, 0, 0, 0, 0, 'D2'],
    [4, 0, 0, 1, 1, 1, 3, 1, 1, 1, 1, 1, 0, 2, 2, 0, 0, 0, 1, 1, 0, 3, 0, 0, 0, 2, 1, 0,
     4, 0, 0, 0, 0, 0, 0, 'D2'],
    [3, 0, 0, 1, 0, 1, 2, 1, 0, 0, 1, 1, 0, 2, 2, 0, 0, 0, 1, 0, 0, 3, 0, 0, 0, 2, 1, 0,
     4, 0, 0, 0, 0, 0, 0, 'D2'],
    [5, 0, 0, 2, 1, 2, 2, 1, 0, 2, 1, 1, 0, 2, 2, 0, 0, 0, 1, 1, 0, 3, 0, 0, 0, 2, 1, 0,
     4, 0, 0, 0, 0, 0, 0, 'D2'],
    [6, 0, 0, 2, 0, 1, 3, 1, 1, 0, 1, 1, 0, 2, 2, 0, 0, 0, 1, 0, 0, 3, 0, 0, 0, 2, 1, 0,
     4, 0, 0, 0, 0, 0, 0, 'D2'],
    [5, 0, 0, 2, 1, 3, 3, 1, 1, 2, 1, 1, 0, 2, 2, 0, 0, 0, 1, 0, 0, 3, 0, 0, 0, 2, 1, 0,
     4, 0, 0, 0, 0, 0, 0, 'D2'],
    [0, 1, 2, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 2, 2, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 3,
     4, 0, 0, 0, 0, 0, 0, 'D3'],
    [2, 1, 2, 0, 0, 3, 1, 2, 0, 1, 1, 0, 0, 2, 2, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 3,
     4, 0, 0, 0, 0, 0, 0, 'D3'],
    [2, 1, 2, 0, 0, 2, 1, 1, 0, 2, 1, 0, 0, 2, 2, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 3,
     4, 0, 0, 0, 0, 0, 0, 'D3'],
    [0, 1, 2, 0, 0, 0, 1, 1, 1, 2, 1, 0, 0, 2, 2, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 3,
     4, 0, 0, 0, 0, 0, 0, 'D3'],
    [0, 1, 2, 0, 0, 2, 1, 1, 1, 1, 1, 0, 0, 2, 2, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 3,
     4, 0, 0, 0, 0, 0, 0, 'D3'],
    [4, 0, 2, 0, 1, 0, 1, 2, 0, 2, 1, 1, 0, 2, 2, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 3,
     4, 0, 0, 0, 0, 0, 0, 'D3'],
    [2, 1, 2, 0, 0, 3, 1, 2, 0, 2, 1, 0, 0, 2, 2, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 3,
     4, 0, 0, 0, 0, 0, 0, 'D3'],
    [0, 1, 2, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 2, 2, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 3,
     4, 0, 0, 0, 0, 0, 1, 'D3'],
    [3, 0, 2, 0, 1, 3, 1, 2, 0, 1, 1, 0, 0, 2, 2, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 3,
     4, 0, 0, 0, 0, 0, 0, 'D3'],
    [0, 1, 2, 0, 0, 1, 1, 2, 1, 2, 1, 0, 0, 2, 2, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 3,
     4, 0, 0, 0, 0, 0, 0, 'D3'],
    [2, 1, 2, 1, 1, 3, 1, 2, 1, 2, 1, 1, 0, 2, 2, 0, 0, 0, 1, 0, 2, 2, 0, 1, 0, 0, 0, 3,
     4, 0, 0, 0, 0, 0, 1, 'D4'],
    [0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 2, 2, 0, 0, 0, 1, 0, 1, 2, 0, 0, 0, 0, 0, 3,
     4, 0, 0, 0, 0, 0, 1, 'D4'],
    [3, 1, 2, 0, 0, 1, 1, 2, 1, 0, 1, 1, 0, 2, 2, 0, 0, 0, 1, 0, 2, 2, 0, 0, 0, 0, 0, 3,
     4, 0, 0, 0, 0, 0, 1, 'D4'],
    [2, 1, 2, 1, 1, 1, 1, 2, 0, 2, 1, 1, 0, 2, 2, 0, 0, 0, 1, 0, 1, 2, 0, 1, 0, 0, 0, 3,
     4, 0, 0, 0, 0, 0, 1, 'D4'],
    [1, 1, 2, 0, 0, 3, 1, 1, 1, 2, 1, 1, 0, 2, 2, 0, 0, 0, 1, 0, 2, 2, 0, 0, 0, 0, 0, 3,
     4, 0, 0, 0, 0, 0, 1, 'D4'],
    [1, 1, 2, 1, 0, 0, 1, 2, 1, 1, 1, 1, 0, 2, 2, 0, 0, 0, 1, 0, 2, 2, 0, 0, 0, 0, 0, 3,
     4, 0, 0, 0, 0, 0, 1, 'D4'],
    [0, 1, 2, 1, 0, 3, 1, 1, 0, 0, 1, 1, 0, 2, 2, 0, 0, 0, 1, 0, 1, 2, 0, 0, 0, 0, 0, 3,
     4, 0, 0, 0, 0, 0, 1, 'D4'],
    [2, 1, 2, 0, 0, 1, 1, 2, 0, 0, 1, 1, 0, 2, 2, 0, 0, 0, 1, 0, 1, 2, 0, 0, 0, 0, 0, 3,
     4, 0, 0, 0, 0, 0, 1, 'D4'],
    [3, 1, 2, 0, 0, 2, 1, 2, 1, 1, 1, 1, 0, 2, 2, 0, 0, 0, 1, 0, 2, 2, 0, 0, 0, 0, 0, 3,
     4, 0, 0, 0, 0, 0, 1, 'D4'],
    [3, 1, 1, 0, 0, 2, 1, 2, 1, 2, 1, 1, 0, 2, 2, 0, 0, 0, 1, 0, 2, 2, 0, 0, 0, 0, 0, 3,
     4, 0, 0, 0, 0, 0, 1, 'D4'],
    [0, 1, 2, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 2, 2, 0, 0, 0, 1, 0, 1, 2, 0, 1, 0, 0, 0, 3,
     4, 0, 0, 0, 0, 0, 1, 'D4'],
    [1, 1, 2, 1, 1, 3, 1, 2, 0, 1, 1, 1, 0, 2, 2, 0, 0, 0, 1, 1, 1, 2, 0, 1, 0, 0, 0, 3,
     4, 0, 0, 0, 0, 0, 1, 'D4'],
    [1, 1, 2, 0, 0, 0, 1, 2, 1, 0, 1, 1, 0, 2, 2, 0, 0, 0, 1, 0, 2, 2, 0, 0, 0, 0, 0, 3,
     4, 0, 0, 0, 0, 0, 1, 'D4'],
    [1, 1, 2, 1, 1, 2, 3, 1, 1, 1, 1, 1, 0, 2, 2, 0, 0, 0, 1, 0, 2, 2, 0, 1, 0, 0, 0, 3,
     4, 0, 0, 0, 0, 0, 1, 'D4'],
    [2, 1, 1, 0, 0, 3, 1, 2, 0, 2, 1, 1, 0, 2, 2, 0, 0, 0, 1, 0, 1, 2, 0, 0, 0, 0, 0, 3,
     4, 0, 0, 0, 0, 0, 1, 'D4'],
    [0, 1, 1, 1, 1, 2, 1, 2, 1, 0, 1, 1, 0, 2, 2, 0, 0, 0, 1, 1, 2, 2, 0, 1, 0, 0, 0, 3,
     4, 0, 0, 0, 0, 0, 1, 'D4'],
    [0, 1, 2, 1, 0, 3, 1, 1, 0, 2, 1, 1, 0, 2, 2, 0, 0, 0, 1, 0, 1, 2, 0, 0, 0, 0, 0, 3,
     4, 0, 0, 0, 0, 0, 1, 'D4'],
])
# Drop target column
SOYBEAN = SOYBEAN[:, :35]

SOYBEAN2 = np.array([
    [4, 0, 2, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 2, 2, 0, 0, 0, 1, 0, 3, 0, 1, 1, 0, 0, 0, 0,
     4, 0, 0, 0, 0, 0, 0, 'D1'],
    [7, 0, 0, 2, 1, 0, 2, 1, 0, 0, 1, 1, 0, 2, 2, 0, 0, 0, 1, 1, 0, 3, 0, 0, 0, 2, 1, 0,
     4, 0, 0, 0, 0, 0, 0, 'D2'],
    [0, 1, 2, 0, 0, 1, 1, 1, 1, 2, 1, 0, 0, 2, 2, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 3,
     4, 0, 0, 0, 0, 0, 0, 'D3'],
    [2, 1, 2, 1, 1, 3, 1, 2, 1, 1, 1, 1, 0, 2, 2, 0, 0, 0, 1, 1, 1, 2, 0, 1, 0, 0, 0, 3,
     4, 0, 0, 0, 0, 0, 1, 'D4'],
])
# Drop target column
SOYBEAN2 = SOYBEAN2[:, :35]


def assert_cluster_splits_equal(array1, array2):

    def find_splits(x):
        return np.where(np.hstack((np.array([1]), np.diff(x))))[0]

    np.testing.assert_array_equal(find_splits(array1), find_splits(array2))


class TestKModes(unittest.TestCase):

    def test_pickle(self):
        obj = KModes()
        s = pickle.dumps(obj)
        assert_equal(type(pickle.loads(s)), obj.__class__)

    def test_kmodes_huang_soybean(self):
        kmodes_huang = KModes(n_clusters=4, n_init=2, init='Huang', verbose=2,
                              random_state=42)
        result = kmodes_huang.fit_predict(SOYBEAN)
        expected = np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0,
                             0, 0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2,
                             2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2])
        assert_cluster_splits_equal(result, expected)
        self.assertTrue(result.dtype == np.dtype(np.uint16))

    def test_kmodes_huang_soybean_parallel(self):
        kmodes_huang = KModes(n_clusters=4, n_init=4, init='Huang', verbose=2,
                              random_state=42, n_jobs=4)
        result = kmodes_huang.fit_predict(SOYBEAN)
        expected = np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0,
                             0, 0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2,
                             2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2])
        assert_cluster_splits_equal(result, expected)
        self.assertTrue(result.dtype == np.dtype(np.uint16))

    def test_kmodes_cao_soybean(self):
        kmodes_cao = KModes(n_clusters=4, init='Cao', verbose=2)
        result = kmodes_cao.fit_predict(SOYBEAN)
        expected = np.array([2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1,
                             1, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0,
                             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        assert_cluster_splits_equal(result, expected)
        self.assertTrue(result.dtype == np.dtype(np.uint16))

    def test_kmodes_predict_soybean(self):
        kmodes_cao = KModes(n_clusters=4, init='Cao', verbose=2)
        kmodes_cao = kmodes_cao.fit(SOYBEAN)
        result = kmodes_cao.predict(SOYBEAN2)
        expected = np.array([2, 1, 3, 0])
        assert_cluster_splits_equal(result, expected)
        self.assertTrue(result.dtype == np.dtype(np.uint16))

    def test_kmodes_predict_unfitted(self):
        kmodes_cao = KModes(n_clusters=4, init='Cao', verbose=2)
        with self.assertRaises(AssertionError):
            kmodes_cao.predict(SOYBEAN)
        with self.assertRaises(AttributeError):
            kmodes_cao.cluster_centroids_

    def test_kmodes_random_soybean(self):
        kmodes_random = KModes(n_clusters=4, init='random', verbose=2,
                               random_state=42)
        result = kmodes_random.fit(SOYBEAN)
        self.assertIsInstance(result, KModes)

    def test_kmodes_init_soybean(self):
        init_vals = np.array(
            [[0, 1, 2, 1, 0, 3, 1, 1, 0, 2, 1, 1, 0, 2, 2, 0, 0, 0, 1, 0, 1, 2,
              0, 0, 0, 0, 0, 3, 4, 0, 0, 0, 0, 0, 1],
             [4, 0, 0, 1, 1, 1, 3, 1, 1, 1, 1, 1, 0, 2, 2, 0, 0, 0, 1, 1, 0, 3,
              0, 0, 0, 2, 1, 0, 4, 0, 0, 0, 0, 0, 0],
             [3, 0, 2, 1, 0, 2, 0, 2, 1, 1, 1, 1, 0, 2, 2, 0, 0, 0, 1, 0, 3, 0,
              1, 1, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0],
             [3, 0, 2, 0, 1, 3, 1, 2, 0, 1, 1, 0, 0, 2, 2, 0, 0, 0, 1, 1, 1, 1,
              0, 1, 1, 0, 0, 3, 4, 0, 0, 0, 0, 0, 0]])
        kmodes_init = KModes(n_clusters=4, init=init_vals, verbose=2)
        result = kmodes_init.fit_predict(SOYBEAN)
        expected = np.array([2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1,
                             1, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0,
                             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        assert_cluster_splits_equal(result, expected)

        # 5 initial centroids, 4 n_clusters
        init_vals = np.array(
            [[0, 1],
             [4, 0],
             [4, 0],
             [3, 0],
             [3, 0]])
        kmodes_init = KModes(n_clusters=4, init=init_vals, verbose=2)
        with self.assertRaises(AssertionError):
            kmodes_init.fit(SOYBEAN)

        # wrong number of attributes
        init_vals = np.array(
            [0, 1, 2, 3])
        kmodes_init = KModes(n_clusters=4, init=init_vals, verbose=2)
        with self.assertRaises(AssertionError):
            kmodes_init.fit(SOYBEAN)

    def test_kmodes_empty_init_cluster_soybean(self):
        # Check if the clustering does not crash in case of an empty cluster.
        init_vals = np.array(
            [[0, 1, 2, 1, 0, 3, 1, 1, 0, 2, 1, 1, 0, 2, 2, 0, 0, 0, 1, 0, 1, 2,
              0, 0, 0, 0, 0, 3, 4, 0, 0, 0, 0, 0, 1],
             [4, 0, 0, 1, 1, 1, 3, 1, 1, 1, 1, 1, 0, 2, 2, 0, 0, 0, 1, 1, 0, 3,
              0, 0, 0, 2, 1, 0, 4, 0, 0, 0, 0, 0, 0],
             [3, 0, 2, 1, 0, 2, 0, 2, 1, 1, 1, 1, 0, 2, 2, 0, 0, 0, 1, 0, 3, 0,
              1, 1, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0],
             [3, 0, 2, 0, 1, 3, 1, 2, 0, 1, 1, 0, 0, 2, 2, 0, 0, 0, 1, 1, 1, 1,
              0, 1, 1, 0, 0, 3, 4, 0, 0, 0, 0, 0, 0]])
        kmodes_init = KModes(n_clusters=4, init=init_vals, verbose=2)
        result = kmodes_init.fit(SOYBEAN)
        self.assertIsInstance(result, KModes)

    def test_kmodes_empty_init_cluster_edge_case(self):
        # Edge case from: https://github.com/nicodv/kmodes/issues/106,
        # due to negative values in all-integer data.
        init_vals = np.array([
            [14, 0, 16, 0, -1, -1, 158, 115],
            [2, 0, 3, 3, 127, 105, 295, 197],
            [10, 2, 12, 3, 136, 20, 77, 42],
            [2, 0, 3, 4, 127, 55, 150, 63],
            [1, 0, 21, 5, 39, -1, 124, 90],
            [17, 2, 12, 3, 22, 175, 242, 164],
            [5, 1, 7, -1, -1, -1, 69, 38],
            [3, 3, 6, -1, -1, -1, 267, 175],
            [1, 0, 21, 4, 71, -1, 276, 196],
            [11, 2, 12, 5, -1, -1, 209, 148],
            [2, 0, 3, 5, 127, 105, 375, 263],
            [2, 0, 3, 4, 28, 105, 16, 8],
            [13, 2, 12, -1, -1, -1, 263, 187],
            [6, 2, 6, 4, 21, 20, 370, 256],
            [10, 2, 12, 3, 136, 137, 59, 31]
        ])
        data = np.hstack((init_vals, init_vals))
        kmodes_init = KModes(n_clusters=15, init='Huang', verbose=2)
        kmodes_init.fit_predict(data)
        kmodes_init.cluster_centroids_

    def test_kmodes_unknowninit_soybean(self):
        with self.assertRaises(NotImplementedError):
            KModes(n_clusters=4, init='nonsense', verbose=2).fit(SOYBEAN)

    def test_kmodes_nunique_nclusters(self):
        data = np.array([
            [0, 1],
            [0, 1],
            [0, 1],
            [0, 2],
            [0, 2],
            [0, 2]
        ])
        kmodes_cao = KModes(n_clusters=6, init='Cao', verbose=2,
                            random_state=42)
        result = kmodes_cao.fit_predict(data, categorical=[1])
        expected = np.array([0, 0, 0, 1, 1, 1])
        assert_cluster_splits_equal(result, expected)
        np.testing.assert_array_equal(kmodes_cao.cluster_centroids_,
                                      np.array([[0, 2],
                                                [0, 1]]))

    def test_kmodes_huang_soybean_ng(self):
        kmodes_huang = KModes(n_clusters=4, n_init=2, init='Huang', verbose=2,
                              cat_dissim=ng_dissim, random_state=42)
        result = kmodes_huang.fit_predict(SOYBEAN)
        expected = np.array([3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0,
                             0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2,
                             2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2])
        assert_cluster_splits_equal(result, expected)
        self.assertTrue(result.dtype == np.dtype(np.uint16))

    def test_kmodes_cao_soybean_ng(self):
        kmodes_cao = KModes(n_clusters=4, init='Cao', verbose=2,
                            cat_dissim=ng_dissim)
        result = kmodes_cao.fit_predict(SOYBEAN)
        expected = np.array([2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1,
                             1, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0,
                             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        assert_cluster_splits_equal(result, expected)
        self.assertTrue(result.dtype == np.dtype(np.uint16))

    def test_kmodes_predict_soybean_ng(self):
        kmodes_cao = KModes(n_clusters=4, init='Cao', verbose=2,
                            cat_dissim=ng_dissim)
        kmodes_cao = kmodes_cao.fit(SOYBEAN)
        result = kmodes_cao.predict(SOYBEAN2)
        expected = np.array([2, 1, 3, 0])
        assert_cluster_splits_equal(result, expected)
        self.assertTrue(result.dtype == np.dtype(np.uint16))

    def test_kmodes_nunique_nclusters_ng(self):
        data = np.array([
            [0, 1],
            [0, 1],
            [0, 1],
            [0, 2],
            [0, 2],
            [0, 2]
        ])
        kmodes_cao = KModes(n_clusters=6, init='Cao', verbose=2,
                            cat_dissim=ng_dissim, random_state=42)
        result = kmodes_cao.fit_predict(data, categorical=[1])
        expected = np.array([0, 0, 0, 1, 1, 1])
        assert_cluster_splits_equal(result, expected)
        np.testing.assert_array_equal(kmodes_cao.cluster_centroids_,
                                      np.array([[0, 2],
                                                [0, 1]]))

    def test_kmodes_ninit(self):
        kmodes = KModes(n_init=10, init='Huang')
        self.assertEqual(kmodes.n_init, 10)
        kmodes = KModes(n_init=10)
        self.assertEqual(kmodes.n_init, 1)
        kmodes = KModes(n_init=10, init=np.array([1, 1]))
        self.assertEqual(kmodes.n_init, 1)
