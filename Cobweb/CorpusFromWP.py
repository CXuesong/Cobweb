from gensim.corpora import WikiCorpus
import localconfig
from datetime import datetime
import logging

def main():
    logging.basicConfig(format='[%(asctime)s]%(levelname)s: %(message)s', level=logging.INFO)
    wiki = WikiCorpus(localconfig.WpDumpDir, dictionary={})
    counter = 0
    logging.info("开始处理。")
    with open("zhwp.txt", "w", encoding="utf-8") as output:
        for text in wiki.get_texts():
            counter += 1
            for segment in text:
                segmentStr = segment.decode(encoding="utf-8")
                # 此处暂不断词，后期需要进行字形转换。
                output.write(segmentStr)
                output.write("\n")
            if counter % 10000 == 0 :
                logging.info("已经处理%d篇文章。" % counter)

if __name__ == "__main__":
    main()