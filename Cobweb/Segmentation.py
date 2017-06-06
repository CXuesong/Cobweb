# 使用 jieba 断词
import os
import sys
import unicodedata
import logging
import jieba

DISABLE_STOP_WORDS = True

def main():
    logging.basicConfig(format='[%(asctime)s]%(levelname)s: %(message)s', level=logging.INFO)
    stopWords = {}
    if len(sys.argv) < 3:
        print("用法")
        print("    Segmentation.py 输入文件名 输出文件名")
        return
    if not DISABLE_STOP_WORDS:
        with open("stopwords.txt", "r", encoding="utf-8") as fs:
            stopWords = set((l.strip() for l in fs));
    def tokenFilter(tokens):
        for t in tokens:
            t = t.strip()
            if not t: continue
            if t in stopWords: continue
            yield t
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
            result = tokenFilter(jieba.cut(line.strip()))
            output.write(" ".join(result))
            output.write("\n")

if __name__ == "__main__":
    main()