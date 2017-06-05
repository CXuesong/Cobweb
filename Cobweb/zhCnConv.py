import logging
import sys
from multiprocessing import Pool

# http://gerry.lamost.org/blog/?p=603
# 最大正向匹配
def conv(string,dic):
    i = 0
    while i < len(string):
        for j in range(len(string) - i, 0, -1):
            if string[i:][:j] in dic:
                t = dic[string[i:][:j]]
                string = string[:i] + t + string[i:][j:]
                i += len(t) - 1
                break
        i += 1
    return string

# 生成转换字典
def mdic():    
    dic = dict()
    name = []
    with open('ZhConversion.php','r', encoding="utf-8") as table:
        for line in table:
            line = line.strip()
            if len(line) == 0: continue
            if line[0] == "]":
                name.append(dic)
                dic = dict()
            if line[0] == "'":
                word = line.split("'")
                dic[word[1]] = word[3]
    name[2].update(name[0]) # 简繁通用转换规则(zh2Hant)加上台湾区域用法(zh2TW)
    name[3].update(name[0]) # 简繁通用转换规则(zh2Hant)加上香港区域用法(zh2HK)
    name[4].update(name[1]) # 繁简通用转换规则(zh2Hans)加上大陆区域用法(zh2CN)
    return name[2],name[3],name[4]

(dic_TW,dic_HK,dic_CN) = mdic()

def worker(input: str):
    return conv(input, dic_CN)

def main(sourcePath: str, destPath: str):
    logging.basicConfig(format='[%(asctime)s]%(levelname)s: %(message)s', level=logging.INFO)
    counter = 0
    pool = Pool()
    with open(sourcePath, "r", encoding="utf-8") as input, \
        open(destPath, "w", encoding="utf-8") as output:
        for line in pool.imap(worker, input, 100000):
            if counter % 100000 == 0:
                logging.info("已处理：{0}行。".format(counter))
            counter += 1
            output.write(line)

if __name__=="__main__":
    if len(sys.argv) < 3:
        print("用法")
        print("    zhCnConv.py 输入文件名 输出文件名")
    main(sys.argv[1], sys.argv[2])
