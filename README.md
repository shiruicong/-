# 信息检索大作业

## 大作业要求

* 实现对病人病历的检索模型（20分）
* 界面程序（无具体要求，实现基本功能，建议bash纯命令行界面）
* 实验报告（10分）

## 大作业内容

* [病人病历数据库](http://www.trec-cds.org/2017.html) xml格式与txt格式前者是官方给定标准数据集格式，后者是为方便处理。官方文档是两者都可使用的，但是要以xml为准！
* 查询见[topic.xml](./topic.xml)和[extra_topics2017.pdf](./extra_topics2017.pdf) 通常做法是将disease字段作为查询，其他字段作为辅助。
* 提交结果形式：<查询ID> Q0 <> Q0 <文档ID> Q0 <> <文档排序> <文档评分> <系统ID> Q0 <>
* 评价指标——P@10 计算方法 可自己编写，也可以使用trec_eval脚本计算
* 5折交叉验证——3部分训练，1部分验证，1部分测试
* 测试结果取平均


## 实验流程

* **文档模型** ： BM25模型
* **词向量** ： 利用CBOM模型词向量
* **查询扩展** ： 利用预训练好的词向量返回原查询中的查询词的前k个相近词
* **权重** ： 原查询字段disease、gene、demographic、other字段权重依次降低，扩展词权重0.9
* **备注** ： 看代码

## 文件说明

* [main.py](./main.py) 主程序文件
* [bm25.py](./bm25.py) BM25模型
* [query.py](./query.py) 查询文件
* [word2vec.py](./word2vec.py) 训练词向量
* [data_helpers.py](./data_helpers.py) 读取数据文件
* [util.py](./util.py) 工具文件
* [SPIMI.py](./SPIMI.py) 倒排表构建文件
* [test.py](./test.py) 测试编程想法
* [clinical_trials.judgments.2017.csv](./clinical_trials.judgments.2017.csv) 标准查询结果
* [w2v.model](./) 词向量（用于查询扩展）
* [w2v.model.trainables.syn1neg.npy](./w2v.model.trainables.syn1neg.npy) 词向量辅助文件1
* [w2v.model.wv.vectors.npy](./w2v.model.wv.vectors.npy) 词向量辅助文件2
* [vocab.pkl](./w2v/vocab.pkl) 词表文件
* [trec_eval](./trec_eval_latest) trec_eval工具（用于计算准确率） 运行命令为——./trec_eval/trec_eval ./eval/qrels.txt ./eval/res.txt
* [qrels.txt](./eval/qrels.txt) 真实相关文档
* [res.txt](./eval/res.txt) 预测相关文档
* [IR界面](./IR界面) 界面 运行[interface.jar](./IR界面/IR/interface.jar) 点击start按钮，打开结果文件夹，显示相关文档内容 可选字体，背景（虽然很丑）
* [topic.xml](./topic.xml) 查询文件
# -
