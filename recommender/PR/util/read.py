import os


def get_graph_from_data(input_file):
    if not os.path.exists(input_file):
        return {}

    graph = {}
    linenum = 0
    score_thr = 4.0
    fp = open(input_file,'r', encoding='UTF-8')

    for line in fp:
        if linenum == 0:
            linenum += 1
            continue
        item = line.strip().split(',')
        if len(item) < 3:
            continue
        userid,itemid,ratings = item[0], "item_" + item[1], float(item[2])

        if ratings < score_thr:
            continue
        
        if userid not in graph:
            graph[userid] = {}
        graph[userid][itemid] = 1

        if itemid not in graph:
            graph[itemid] = {}
        graph[itemid][userid] = 1
    
    fp.close()
    return graph


if __name__ == "__main__":
    print(get_graph_from_data(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))) + "\\recommender\\data\\log.txt"))

    graph = get_graph_from_data(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))) + "\\recommender\\data\\ml-latest-small\\ratings.csv");

    print(graph["1"])
