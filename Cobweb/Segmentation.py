# 使用 jieba 断词
import os
import sys
import unicodedata
import logging
import jieba

def main():
    logging.basicConfig(format='[%(asctime)s]%(levelname)s: %(message)s', level=logging.INFO)
    stopWords = None
    if len(sys.argv) < 3:
        print("用法")
        print("    Segmentation.py 输入文件名 输出文件名")
        return
    with open("stopwords.txt", "r", encoding="utf-8") as fs:
        stopWords = set((l.strip() for l in fs));
    counter = 0
    with open(sys.argv[1], "r", encoding="utf-8") as input, \
        open(sys.argv[2], "w", encoding="utf-8") as output:
        logging.info("开始。")
        while True:
            if counter % 100000 == 0:
                logging.info("已处理：{0}行。".format(counter))
            counter += 1
            line = input.readline()
            if not line: break
            result = (w for w in jieba.cut(line.strip()) if w not in stopWords)
            output.write(" ".join(result))
            output.write(" ")

if __name__ == "__main__":
    main()