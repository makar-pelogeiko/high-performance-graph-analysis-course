import pytest
import pygraphblas as gb
from project.shortPath import m_get_short_ways, s_get_short_ways


@pytest.mark.parametrize(
    "I, J, V, size, start_verts, expected",
    [
        (
            [0, 0, 0, 1, 1, 1, 2, 2, 2],
            [0, 1, 2, 0, 1, 2, 0, 1, 2],
            [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0],
            3,
            [0, 1, 2],
            [(0, [0.0, 1.0, 2.0]), (1, [3.0, 0.0, 5.0]), (2, [6.0, 7.0, 0.0])],
        ),
        (
            [0, 0, 0, 1, 1, 1, 2, 2, 2],
            [0, 1, 2, 0, 1, 2, 0, 1, 2],
            [0.3, 1.0, 2.0, 10000.0, 4.0, 5.0, 0.5, 7.0, 8.0],
            3,
            [0, 2],
            [(0, [0.0, 1.0, 2.0]), (2, [0.5, 1.5, 0.0])],
        ),
        (
            [0, 0, 0, 0, 0],
            [0, 1, 2, 3, 4],
            [1, 2, 3, 4, 5],
            10,
            [0, 1, 2, 3],
            [
                (0, [0, 2, 3, 4, 5, -1, -1, -1, -1, -1]),
                (1, [-1, 0, -1, -1, -1, -1, -1, -1, -1, -1]),
                (2, [-1, -1, 0, -1, -1, -1, -1, -1, -1, -1]),
                (3, [-1, -1, -1, 0, -1, -1, -1, -1, -1, -1]),
            ],
        ),
    ],
)
def test_multiple_short_ways_search(I, J, V, size, start_verts, expected):
    matrix_graph = gb.Matrix.from_lists(I, J, V, nrows=size, ncols=size)
    answer = m_get_short_ways(matrix_graph, start_verts)
    assert answer == expected


@pytest.mark.parametrize(
    "I, J, V, size, start_vert, expected",
    [
        (
            [0, 0, 0, 1, 1, 1, 2, 2, 2],
            [0, 1, 2, 0, 1, 2, 0, 1, 2],
            [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0],
            3,
            1,
            [3.0, 0.0, 5.0],
        ),
        (
            [0, 0, 0, 1, 1, 1, 2, 2, 2],
            [0, 1, 2, 0, 1, 2, 0, 1, 2],
            [0.3, 1.0, 2.0, 10000.0, 4.0, 5.0, 0.5, 7.0, 8.0],
            3,
            2,
            [0.5, 1.5, 0.0],
        ),
        (
            [0, 0, 0, 0, 0],
            [0, 1, 2, 3, 4],
            [1, 2, 3, 4, 5],
            10,
            0,
            [0, 2, 3, 4, 5, -1, -1, -1, -1, -1],
        ),
    ],
)
def test_single_short_ways_search(I, J, V, size, start_vert, expected):
    matrix_graph = gb.Matrix.from_lists(I, J, V, nrows=size, ncols=size)
    answer = s_get_short_ways(matrix_graph, start_vert)
    assert answer == expected
