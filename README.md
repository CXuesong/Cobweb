# Cobweb

>   A  feeble attempt on BOP 2017 PRELIM.

BOP 2017资格赛观光存储库。

关于规则和数据集下载，请参阅：[资格赛规则](https://studentclub.msra.cn/bop2017/rules/qualification)。

## 工作流程

1.  下载中文维基百科的文章转储

2.  使用`CorpusFromWP.py`将转储转换为语料库

3.  使用`zhCnConv.py`进行字形和常见地区词转换

    需要提前下载MediaWiki源代码，并将`ZhConversion.php`复制到工作路径

4.  使用`Segmentation.py`对语料库中的文本进行断词

5.  将训练集和测试集中的数据进行预处理

    1.  去除所有的脚注标号和“编辑”链接（显然，训练集来自于维基百科）
    2.  将所有的标点符号替换为空格
    3.  将所有的阿拉伯数字替换为“#”

6.  使用`CombineCorpus.py`合并维基百科语料库和5中得到的语料库，将所有的换行符替换为空格

    考虑到Word2Vec训练时会剔除出现频次较低的词汇，所以合并时考虑将5中的语料库重复加入两次

7.  使用`Word2VecTrain.py`在合并之后的语料库上对Word2Vec进行训练

8.  使用`Word2VecBuilder.py`将预处理之后的训练集和测试集Q/A转换为向量

9.  使用`XGB.py`进行排名模型训练和预测

## 开发集测试结果

MRR约为0.6313。