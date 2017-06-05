
class QaEntry:
    def __init__(self, corresponds = None, question = None, answer = None):
        self.corresponds = corresponds
        self.question = question
        self.answer = answer
        self.questionVector = None
        self.answerVector = None

    def __str__(self):
        return "%s %s -- %s" % (self.corresponds, self.question, self.answer)

def extractEntry(entryText: str):
    items = entryText.split("\t")
    if len(items) > 2:
        return QaEntry(int(items[0]) != 0, items[1], items[2])
    else :
        return QaEntry(None, items[0], items[1])

def entriesFromFile(path: str):
    entries = []
    with open(path, "r", encoding="utf-8") as input:
        while True:
            line = input.readline()
            if not line: break
            yield extractEntry(line.strip(" "))