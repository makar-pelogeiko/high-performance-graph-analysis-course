import pygraphblas as gb

__all__ = ["bfs", "bfs_parallel"]


def bfs(matrix_graph: gb.Matrix, start_vert: int):

    visited = gb.Vector.sparse(gb.types.BOOL, matrix_graph.nrows)
    result = gb.Vector.dense(gb.types.INT64, matrix_graph.nrows, fill=-1)
    curr_front = gb.Vector.sparse(gb.types.BOOL, matrix_graph.nrows)

    result[start_vert] = 0
    visited[start_vert] = True
    curr_front[start_vert] = True
    step = 0
    prev_nnz = -1

    while prev_nnz != visited.nvals:
        step += 1
        prev_nnz = visited.nvals

        curr_front.vxm(
            matrix_graph, mask=visited, out=curr_front, desc=gb.descriptor.RC
        )

        visited.eadd(
            curr_front, curr_front.type.lxor_monoid, out=visited, desc=gb.descriptor.R
        )
        result.assign_scalar(step, mask=curr_front)

    return list(result.vals)


def bfs_parallel(matrix_graph: gb.Matrix, start_vert_lst):

    visited = gb.Matrix.sparse(
        gb.types.BOOL, nrows=len(start_vert_lst), ncols=matrix_graph.ncols
    )
    result_matrix = gb.Matrix.dense(
        gb.types.INT64, nrows=len(start_vert_lst), ncols=matrix_graph.ncols, fill=-1
    )
    curr_front = gb.Matrix.sparse(
        gb.types.BOOL, nrows=len(start_vert_lst), ncols=matrix_graph.ncols
    )

    for i, j in enumerate(start_vert_lst):
        visited.assign_scalar(True, i, j)
        result_matrix.assign_scalar(0, i, j)
        curr_front.assign_scalar(True, i, j)

    prev_nnz = -1
    step = 0

    while prev_nnz != visited.nvals:
        prev_nnz = visited.nvals
        step += 1

        curr_front.mxm(
            matrix_graph, mask=visited, out=curr_front, desc=gb.descriptor.RC
        )

        visited.eadd(
            curr_front, curr_front.type.lxor_monoid, out=visited, desc=gb.descriptor.R
        )
        result_matrix.assign_scalar(step, mask=curr_front)

    result = list()
    for i, vert in enumerate(start_vert_lst):
        result.append((vert, list(result_matrix[i].vals)))

    return result
