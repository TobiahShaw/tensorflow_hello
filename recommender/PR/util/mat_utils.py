from scipy.sparse import coo_matrix
import numpy as np

def graph_to_m(graph):
    """
    graph:user-item graph
    return:
        a sparse martix M
        a list all point
        a dict point - index
    """
    vertex = graph.keys()
    total_len = len(vertex)
    address_dict = {}
    for index in range(len(vertex)):
        address_dict[vertex[index]] = index
    row = []
    col = []
    data = []
    for element_i in graph:
        weight = round(1/len(graph[element_i]), 3)
        row_index = address_dict[element_i]
        for element_j in graph[element_i]:
            col_index = address_dict[element_j]
            row.append(row_index)
            col.append(col_index)
            data.append(weight)

    row = np.array(row)
    col = np.array(col)
    data = np.array(data)

    m = coo_matrix((data, (row, col)), shape=(total_len, total_len))
    return m, vertex, address_dict