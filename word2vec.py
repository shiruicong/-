# coding = utf-8

from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence
from utils import *
import collections


def build_vocab(data_path, vocab_path, w2id_path, id2w_path, min_cnt = 3):
    '''
    构建字典

    Args:
        data_path str 数据路径
        vocab_path str 词典路径
        min_cnt int 低频词阈值
    '''
    word_counter = collections.Counter()
    sentences = load_data_lines(data_path)
    for sent in sentences:
        word_counter.update(sent)
    vocabulary_inv = ['<UNK>'] + [x[0] for x in word_counter.most_common() if x[1] >= min_cnt]
    w2id = {x : i for i, x in enumerate(vocabulary_inv)}
    id2w = {i : x for i, x in enumerate(vocabulary_inv)}
    pickle_dump(vocab_path, vocabulary_inv)
    pickle_dump(w2id_path, w2id)
    pickle_dump(id2w_path, id2w)

def word_embedding(data_path, model_path, size = 128, window = 10, min_cnt = 3):
    '''
    读取语料，训练词向量，并存储模型

    Args:
        data_path str 语料路径
        model_path str 模型存储路径
        size int 词向量温度
        window int word2vec的窗口大小
        min_cnt int 最小词频
    '''
    model = Word2Vec(LineSentence(data_path), size = size, window = window, min_count = min_cnt)
    model.save(model_path)

def load_model(model_path):
    '''
    读取模型

    Args:
        model_path str 载入模型
    '''
    print("载入词向量")
    model = Word2Vec.load(model_path)
    print("载入词向量完毕")
    return model

if __name__ == '__main__':
    data_path = '../data/test/corpus.txt'
    model_path = '../data/w2v_corpus.model'
    vocab_path = './vocab_corpus.pkl'
    w2id_path = './w2id_corpus.pkl'
    id2w_path = './id2w_corpus.pkl'
    word_embedding(data_path, model_path)
    build_vocab(data_path, vocab_path, w2id_path, id2w_path)