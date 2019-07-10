import os

def produce_train_data(input_file, output_file):
    if not os.path.exists(input_file):
        return
    fp = open(input_file, "r", encoding='UTF-8')
    linenum = 0
    score_thr = 4
    record = {}
    for line in fp.readlines():
        if linenum == 0:
            linenum += 1
            continue
        item = line.strip().split(",")
        if len(item) < 4:
            continue
        userid,itemid,rating = item[0], item[1], float(item[2])
        if rating < score_thr:
            continue
        if userid not in record:
            record[userid] = []
        record[userid].append(itemid)
    fp.close()

    fw = open(output_file, "w+", encoding='UTF-8')
    for userid in record:
        fw.write(" ".join(record[userid]) + '\n')
    fw.close()


if __name__ == "__main__":
    root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    produce_train_data(root  + "\\recommender\\data\\ml-latest-small\\ratings.csv", root + "\\recommender\\data\\train_data.txt")
