import pytest
import pygraphblas as gb
from project.bfs import bfs, bfs_parallel


@pytest.mark.parametrize(
    "I, J, V, size, start_vertex, expected",
    [
        (
            [0, 0, 2, 1, 3, 4],
            [1, 2, 4, 3, 1, 5],
            [True, True, True, True, True, True],
            6,
            0,
            [0, 1, 1, 2, 2, 3],
        ),
        (
            [0],
            [1],
            [False],
            6,
            0,
            [0, -1, -1, -1, -1, -1],
        ),
    ],
)
def test_bfs(I, J, V, size, start_vertex, expected):
    adj_matrix = gb.Matrix.from_lists(I, J, V, nrows=size, ncols=size)
    answer = bfs(adj_matrix, start_vertex)
    assert answer == expected


@pytest.mark.parametrize(
    "I, J, V, size, start_vertices, expected",
    [
        (
            [0, 0, 2, 1, 3, 4],
            [1, 2, 4, 3, 1, 5],
            [True, True, True, True, True, True],
            6,
            [0, 0],
            [(0, [0, 1, 1, 2, 2, 3]), (0, [0, 1, 1, 2, 2, 3])],
        ),
        (
            [0, 0, 2, 1, 3, 4],
            [1, 2, 4, 3, 1, 5],
            [True, True, True, True, True, True],
            6,
            [0, 1, 2],
            [
                (0, [0, 1, 1, 2, 2, 3]),
                (1, [-1, 0, -1, 1, -1, -1]),
                (2, [-1, -1, 0, -1, 1, 2]),
            ],
        ),
        (
            [0],
            [1],
            [False],
            6,
            [0, 3],
            [(0, [0, -1, -1, -1, -1, -1]), (3, [-1, -1, -1, 0, -1, -1])],
        ),
        (
            [0],
            [1],
            [False],
            6,
            [0],
            [(0, [0, -1, -1, -1, -1, -1])],
        ),
    ],
)
def test_bfs_parallel(I, J, V, size, start_vertices, expected):
    adj_matrix = gb.Matrix.from_lists(I, J, V, nrows=size, ncols=size)
    answer = bfs_parallel(adj_matrix, start_vertices)
    assert answer == expected
