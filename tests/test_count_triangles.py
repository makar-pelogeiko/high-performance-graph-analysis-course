import pytest
import pygraphblas as gb
from project.triangleCount import get_triang_amount


@pytest.mark.parametrize(
    "I, J, V, size, expected",
    [
        ([1], [1], [True], 4, [0, 0, 0, 0]),
        ([0, 0, 1, 1, 2, 2], [1, 2, 1, 2, 1, 2], [True] * 6, 3, [2, 4, 4]),
        ([0, 1, 1, 2, 2, 0], [1, 0, 2, 1, 0, 2], [True] * 6, 4, [1, 1, 1, 0]),
    ],
)
def test_get_triang_amount(I, J, V, size, expected):
    matrix_graph = gb.Matrix.from_lists(I, J, V, nrows=size, ncols=size)
    answer = get_triang_amount(matrix_graph)
    assert answer == expected
