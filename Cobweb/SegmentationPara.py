# 使用 jieba 并行断词
# 并行感觉跟没并行差不多……
import os
import sys
import unicodedata
import logging
import jieba
import multiprocessing

def worker(qi: multiprocessing.Queue, qo: multiprocessing.Queue):
    with open("stopwords.txt", "r", encoding="utf-8") as fs:
        stopWords = set((l.strip() for l in fs));
    while True:
        line = None
        try:
            line = qi.get(True, 5)
        except multiprocessing.queues.Empty:
            return
        result = (w for w in jieba.lcut(line.strip()) if w not in stopWords)
        qo.put(" ".join(result))

def main():
    logging.basicConfig(format='[%(asctime)s]%(levelname)s: %(message)s', level=logging.INFO)
    stopWords = None
    if len(sys.argv) < 3:
        print("用法")
        print("    Segmentation.py 输入文件名 输出文件名")
        return
    counter = 0
    qi = multiprocessing.Queue(100)
    qo = multiprocessing.Queue(100)
    processes = [multiprocessing.Process(target=worker, args=(qi, qo)) for i in range(0, 8)]
    for p in processes: p.start()
    with open(sys.argv[1], "r", encoding="utf-8") as input, \
        open(sys.argv[2], "w", encoding="utf-8") as output:
        logging.info("开始。")
        while True:
            line = input.readline()
            if line:
                qi.put(line.strip())
            else:
                for p in processes:
                    logging.info("等待结束：{0}".format(p))
                    p.join()
            while True:
                try:
                    result = qo.get(False);
                    output.write(result + "\n")
                    counter += 1
                    if counter % 100000 == 0:
                        logging.info("已处理：{0}行。".format(counter))
                except multiprocessing.queues.Empty:
                    break
            if not line: break
    qi.close()
    qo.close()

if __name__ == "__main__":
    main()