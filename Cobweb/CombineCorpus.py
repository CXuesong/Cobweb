import sys

BUFFER_SIZE = 1024*1024*16

def main(destPath:str, sourcePaths: list):
    with open(destPath, "w", encoding="utf-8") as output:
        for sp in sourcePaths:
            print(sp)
            with open(sp, "r", encoding="utf-8") as input:
                while True:
                    block = input.read(BUFFER_SIZE)
                    if not block: break
                    block = block.replace("\n", " ")
                    output.write(block)
            output.write(" ")

if __name__=="__main__":
    if len(sys.argv) < 4:
        print("用法")
        print("    CombineCorpus.py 目标文件名 文件名1 文件名2 … 文件名n")
    else:
        main(sys.argv[1], sys.argv[2:])
