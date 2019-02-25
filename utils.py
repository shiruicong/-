# coding = utf-8

import xml.etree.ElementTree as et
import re
import os
import pickle
from string import punctuation
from nltk import WordNetLemmatizer
from nltk.corpus import stopwords
import shutil

def load_data(data_path):
    '''
    以行的形式读取文件, utf-8格式

    Args:
        data_path str 数据路径
    Returns:
        cont list 数据
    '''
    with open(data_path, 'r', encoding = 'utf-8') as f:
        cont = f.read()
    return cont

def load_data_lines(data_path):
    '''
    以行的形式读取文件, utf-8格式

    Args:
        data_path str 数据路径
    Returns:
        cont list 数据
    '''
    with open(data_path, 'r', encoding = 'utf-8') as f:
        cont = f.readlines()
    return cont


def load_data_lines_v2(data_path):
    '''
    以行的形式读取文件, utf-8格式, 去除空行

    Args:
        data_path str 数据路径
    Returns:
        cont list 数据
    '''
    with open(data_path, 'r', encoding = 'utf-8') as f:
        cont = f.readlines()
        for i in range(len(cont)-1, -1, -1):
            # 删除文件中的空行
            if cont[i] == '\n' :
                cont.pop(i)
    return cont

def load_data_lines_bin(data_path):
    '''
    以行的形式读取文件, utf-8格式

    Args:
        data_path str 数据路径
    Returns:
        cont list 数据
    '''
    with open(data_path, 'rb') as f:
        cont = f.readlines()
    return cont

def save_data(data_path, data):
    '''
    以行的形式存储数据, utf-8

    Args:
        data_path str 存储路径
        data list 存储数据
    '''
    with open(data_path, 'w', encoding = 'utf-8') as f:
        f.write(data)

def save_data_lines(data_path, data):
    '''
    以行的形式存储数据, utf-8

    Args:
        data_path str 存储路径
        data list 存储数据
    '''
    with open(data_path, 'w', encoding = 'utf-8') as f:
        f.writelines(data)

def save_data_lines_bin(data_path, data):
    '''
    以行的形式存储数据, utf-8

    Args:
        data_path str 存储路径
        data list 存储数据
    '''
    with open(data_path, 'wb') as f:
        f.writelines(data)

def save_data_dict(data_path, data):
    '''
    存储字典, utf-8

    Args:
        data_path str 存储路径
        data dict 存储数据
    '''
    with open(data_path, 'a+', encoding = 'utf-8') as f:
        doc_id = data['doc_id']
        if len(data['brief_title']) == 0:
            brief_title = ''
        else:
            brief_title = data['brief_title'][0]
        if len(data['brief_summary']) == 0:
            brief_summary = ''
        else:
            brief_summary = data['brief_summary'][0]
            brief_summary_list = brief_summary.split('\n')
            brief_summary = clean(brief_summary_list)
            brief_summary = brief_summary.strip(' ')
        if len(data['detailed_description']) == 0:
            detailed_description = ''
        else:
            detailed_description = data['detailed_description'][0]
            detailed_description_list = detailed_description.split('\n')
            detailed_description = clean(detailed_description_list)
            detailed_description = detailed_description.strip(' ')
        f.write('doc_id:' + doc_id[0] + '\n' + 'brief_title:' + brief_title + '\n' + 'brief_summary:' + brief_summary 
            + '\n' +'detailed_description:' + detailed_description + '\n' + '\n')
        
def pickle_load(data_path):
    '''
    pickle载入数据

    Args:
        data_path str 数据路径
    Returns:
        cont dict 读取内容
    '''
    with open(data_path, 'rb') as f:
        cont = pickle.load(f)
    return cont

def pickle_dump(data_path, data):
    '''
    pickle存储数据
    '''
    with open(data_path, 'wb') as f:
        pickle.dump(data, f)

def xml_parse(data_path, query_dict, flag = 1):
    '''
    xml文件解析

    Args:
        data_path str xml文件路径
    Returns:
        query_dict dict 查询字典
    '''
    tree = et.parse(data_path)
    if flag == 1:
        root = tree.getroot()
        for value in root.iter('topic'):
            query_dict['disease'].append(value[0].text)
            query_dict['gene'].append(value[1].text)
            query_dict['demographic'].append(value[2].text)
            query_dict['other'].append(value[3].text)
    else:
        query_dict['brief_title'] = tree.find('brief_title').text
        query_dict['brief_summary'] = tree.find('brief_summary').find('textblock').text
        try:
            query_dict['detailed_description'] = tree.find('detailed_description').find('textblock').text
        except AttributeError:
            pass
    return query_dict

def cut_file(src_path, des_path):
    '''
    剪切文件

    Args:
        src_path str 原数据路径
        des_path str 目标数据路径
    '''
    if not os.path.isdir(des_path):
        os.mkdir(des_path)
    for root, _, files in os.walk(src_path):
        for target_file in files:
            if os.path.isfile(os.path.join(des_path, target_file)):
                os.remove(os.path.join(des_path, target_file))
            os.rename(os.path.join(root, target_file), os.path.join(des_path, target_file))

def clean_data(query_list):
    '''
    对查询进行词干还原与去停用词

    Args:
        query_list list 原始的查询
    Returns:
        query_clean_list list 词干还原和去停用词之后的查询
    '''
    # 导入词性还原与停用词
    wnl = WordNetLemmatizer()
    sw = stopwords.words('english')
    # 扩展后的查询
    query_clean_list = []
    for query in query_list:
        query = query.lower()
        query = wnl.lemmatize(query)
        if query not in sw:
            query_clean_list.append(query)
    return query_clean_list

def clean(data):
    '''
    清理数据
    Args:
        data list 待清理的数据
    Returns
        cont str 清除完毕的数据
    '''
    cont = ''
    for sent in data:
        sent = sent.strip(' ')
        cont += sent + ' '
    return cont

def eval_res(res, eval_path):
    '''
    将查询结果写入文件

    Args:
        res tuple 查询结果
        res_path str 结果存储文件
    '''
    result = ''
    for query_id, query_res in enumerate(res):
        i = 1
        doc_id_list, doc_score_list = query_res
        for j in range(len(doc_id_list)):
            result += (str(query_id + 1) + " Q0 " + str(doc_id_list[j]) + " " + str(i) + " " + str(doc_score_list[j]) + " myrun\n")
            i += 1
    save_data(eval_path, result)

def preprocess(cont):
    '''
    对文档内容进行预处理，用于map函数

    Args:
        cont str 未预处理的文档内容中的一行
    Returns:
        cont str 预处理之后的文档内容中的一行
    '''
    cont = re.sub(r'[{%s}]+'%punctuation, '', cont)
    return cont

def get_doc(doc_id, res_file_path, doc_path):
    '''
    根据doc_id，获取对应的文本内容（目前是摘要），并存储

    Args:
        doc_id int 文档id
        res_file_path str 文档存储路径
    '''
    # 相关文档的返回内容
    query_dict = {'brief_title' : [], 'brief_summary' : [], 'detailed_description' : []}
    doc_id += '.xml'
    query_dict = xml_parse(os.path.join(doc_path, doc_id), query_dict, 0)
    query_dict['doc_id'] = [doc_id]
    save_data_dict(res_file_path, query_dict)

def get_doc_cont(res, res_path, doc_path):
    '''
    返回相关文档的内容，并存储

    Args:
        res tuple 查询结果
        res_path str 存储路径
    '''
    if os.path.exists(res_path):
        shutil.rmtree(res_path)
    os.makedirs(res_path)
    for quert_id, query_res in enumerate(res):
        doc_id_list, _ = query_res
        for doc_id in doc_id_list:
            get_doc(doc_id, os.path.join(res_path, str(quert_id + 1) + '.txt'), doc_path)
