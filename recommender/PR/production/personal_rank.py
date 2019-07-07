import operator
import sys, os
lib_path = os.path.dirname(os.path.dirname(__file__))
sys.path.append(lib_path)
import util.read as read


def personal_rank(graph, root, alpha, iter_num, recom_num = 10):
    """
    Args:
        graph: user-item graph
        root: user who we want to recommender
        alpha: prob to walk
        iter_num: num of iter
        recom_num: number of recommender item
    Return:
        a dict key itemid, value pr value
    """
    if root not in graph:
        return {}
    rank = {point : 0 for point in graph}
    rank[root] = 1
    recom_result={}

    for iter_index in range(iter_num):
        tmp_rank = {point : 0 for point in graph}
        for out_point, out_dict in graph.items():
            for inner_point, value in graph[out_point].items():
                tmp_rank[inner_point] += round(alpha * rank[out_point] / len(out_dict), 4)
                if inner_point == root:
                    tmp_rank[inner_point] += round(1 - alpha, 4)
        if tmp_rank == rank:
            break
        rank = tmp_rank
    right_num = 0
    for comb in sorted(rank.items(), key=operator.itemgetter(1), reverse=True):
        point, pr = comb[0], comb[1]
        if len(point.split("_")) < 2:
            continue
        if point in graph[root]:
            continue
        recom_result[point] = pr
        right_num += 1
        if right_num > recom_num:
            break
    return  recom_result

def get_user_recom():
    # user = "A"
    # alpha = 0.6
    # graph = read.get_graph_from_data(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))) + "\\recommender\\data\\log.txt")
    # print(personal_rank(graph, user, alpha, 10, 10))
    user = "1"
    alpha = 0.8
    graph = read.get_graph_from_data(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))) + "\\recommender\\data\\ml-latest-small\\ratings.csv")
    recom_result = personal_rank(graph, user, alpha, 100, 10)
    item_info = read.get_item_info(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))) + "\\recommender\\data\\ml-latest-small\\movies.csv")

    for itemid, value in graph[user].items():
        print(item_info[itemid.split("_")[1]])

    print("-"*30)

    for itemid, value in recom_result.items():
        print(item_info[itemid.split("_")[1]])
        print(value)



if __name__ == "__main__":
    get_user_recom()