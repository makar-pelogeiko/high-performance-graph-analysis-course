import pygraphblas as gb

__all__ = ["get_triang_amount"]


def get_triang_amount(matrix_graph_in: gb.Matrix):
    matrix_graph = matrix_graph_in
    matrix_graph.union(matrix_graph.transpose(), out=matrix_graph)

    res = matrix_graph

    res = matrix_graph.mxm(res, cast=gb.types.INT64, mask=res)

    result = []
    for i in range(res.nrows):
        result.append(sum(list(res[i].vals)))
    result = [elem // 2 for elem in result]
    return result
