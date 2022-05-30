import pygraphblas as gb
from pygraphblas import INT64

__all__ = ["m_get_short_ways", "s_get_short_ways"]


def m_get_short_ways(matrix_graph: gb.Matrix, start_verts):
    no_way = -1

    fronts = gb.Matrix.sparse(
        matrix_graph.type, nrows=len(start_verts), ncols=matrix_graph.ncols
    )
    visited = gb.Matrix.sparse(
        gb.types.BOOL, nrows=len(start_verts), ncols=matrix_graph.ncols
    )

    for i, j in enumerate(start_verts):
        fronts.assign_scalar(0, i, j)
        visited.assign_scalar(True, i, j)

    prev_nnz = -1
    while prev_nnz != visited.nvals:
        prev_nnz = visited.nvals

        fronts.mxm(
            matrix_graph,
            semiring=matrix_graph.type.min_plus,
            out=fronts,
            accum=matrix_graph.type.min,
        )

        visited.eadd(
            fronts, visited.type.lxor_monoid, out=visited, desc=gb.descriptor.R
        )

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
