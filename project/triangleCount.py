import pygraphblas as gb

__all__ = ["get_triang_amount"]


def get_triang_amount(matrix_graph_in: gb.Matrix):

    matrix_graph_in = matrix_graph_in.tril() + matrix_graph_in.triu().transpose()
    matrix_graph = matrix_graph_in + matrix_graph_in.transpose()

    res = matrix_graph

    for i in range(2):
        res = matrix_graph.mxm(res, cast=gb.types.INT64, accum=gb.types.INT64.PLUS)

    res = res.diag().reduce_vector()
    res /= 2

    vert_lst, triang_lst = res.to_lists()
    result = [0] * matrix_graph.nrows

    for i, vert in enumerate(vert_lst):
        result[vert] = triang_lst[i]

    return result
