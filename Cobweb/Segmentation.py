# 按照字符断词
import sys
import unicodedata

stopWords = set("的 了 和 是 就 都 而 及 与 着 或".split())

def main():
    if len(sys.argv) < 3:
        print("用法")
        print("    Segmentation.py 输入文件名 输出文件名")
        return
    with open(sys.argv[1], "r", encoding="utf-8") as input, \
        open(sys.argv[2], "w", encoding="utf-8") as output:
        while True:
            line = input.readline()
            if not line: break
            
            output.write(" ".join(c for c in line if c not in stopWords).strip())
            output.write("\n")

main()