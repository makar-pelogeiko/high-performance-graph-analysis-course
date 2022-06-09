import pygraphblas as gb
import numpy as np
from pygraphblas import INT64

__all__ = ["m_get_short_ways", "s_get_short_ways"]


def m_get_short_ways(matrix_graph: gb.Matrix, start_verts):
    no_way = -1

    fronts = gb.Matrix.sparse(
        matrix_graph.type, nrows=len(start_verts), ncols=matrix_graph.ncols
    )

    for i, j in enumerate(start_verts):
        fronts.assign_scalar(0, i, j)

    old_fronts = np.copy(fronts)

    for n in range(matrix_graph.nrows - 1):

        fronts.mxm(
            matrix_graph,
            semiring=matrix_graph.type.min_plus,
            out=fronts,
            accum=matrix_graph.type.min,
        )

        if np.array_equal(old_fronts, fronts):
            break

        old_fronts = np.copy(fronts)

    result = []
    for i, j in enumerate(start_verts):
        temp_step = [no_way] * matrix_graph.nrows
        fronts[i].to_lists()
        vert_lst, dist_lst = fronts[i].to_lists()
        for k, vert in enumerate(vert_lst):
            temp_step[vert] = dist_lst[k]

        result.append((j, temp_step))

    return result


def s_get_short_ways(matrix_graph: gb.Matrix, start_vert: int):
    result = m_get_short_ways(matrix_graph, [start_vert])
    return result[0][1]
