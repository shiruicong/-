# coding = utf-8

import json
import os
from nltk import FreqDist, WordNetLemmatizer
import re
from nltk.corpus import stopwords

def CleanData(raw):
    str_raw = []
    raw = re.sub(r"[^A-Za-z0-9\s]", " ", raw)
    raw = raw.split()
    wnl = WordNetLemmatizer()
    for word in set(raw):
        word = word.lower()
        word = wnl.lemmatize(word) #词形还原
        if word in stopwords.words('english'):
            continue
        if word in ['year', 'old', 'none']:
            continue
        if bool(re.search(r'\d', word)):
            continue
        str_raw.append(word)
    return " ".join(str_raw)

def CreateInvertTable_SPIMI(dic, dir, filename, clean = False, title=''):
    if title == '':
        with open(dir+filename, "r") as fr:
            raw = fr.read()
    else:
        raw = title
    if clean:
        raw = CleanData(raw)
    raw = raw.split()
    tf_dic = FreqDist(raw)
    ld = str(len(raw))
    docID = filename.replace('NCT0', '').replace('.txt', '')

    for word in set(raw):
        tf = tf_dic[word]
        if word in dic:
            dic[word].append(docID+" "+str(tf)+" "+ld)
        else:
            dic[word] = [docID+" "+str(tf)+" "+ld]
    return dic


def Create_Fulltext_Invertable(FILE, clean=False):
    dic = dict()
    filelist = os.listdir(FILE + "\\")
    N = len(filelist)
    for (i, filename) in enumerate(filelist):
        if i / 100 == 0:
            print("PRCESSING:", i / N)
        dic = CreateInvertTable_SPIMI(dic, FILE + "\\", filename, clean)
    dic = json.dumps(dic)
    if clean:
        fname  = "clinicaltrials_cleaned_txt.json"
    else:
        fname = "clinicaltrials_unclean_txt.json"
    with open(fname, "w", encoding="utf-8") as fw:
        fw.write(dic)
    print("finsh spimi")

def Create_Level_Invertable(FILE, clean=False):
    dic = dict()
    filelist = os.listdir(FILE + "\\")
    N = len(filelist)
    for (i, filename) in enumerate(filelist):
        if i / 100 == 0:
            print("PRCESSING:", i / N)
        with open(FILE + "\\" + filename, "r") as fr:
            fr.readline()  #节省时间,不进行正则匹配
            title = fr.readline()
        dic = CreateInvertTable_SPIMI(dic, FILE + "\\", filename, clean, title)
    dic = json.dumps(dic)
    if clean:
        fname = "clinicallevel_cleaned_txt.json"
    else:
        fname = "clinicallevel_unclean_txt.json"
    with open(fname, "w", encoding="utf-8") as fw:
        fw.write(dic)
    print("finsh spimi")

if __name__ == '__main__':

# print("构建全文倒排索引：")
#Create_Fulltext_Invertable("C:\\Users\\54215\\Desktop\\研究生课程\\信息检索\\作业\\clinicaltrials_txt\\000\\00000", clean=False)
#Create_Fulltext_Invertable("C:\\Users\\54215\\Desktop\\研究生课程\\信息检索\\作业\\clinicaltrials_txt\\000\\00000", clean=True)
#print("构建分层倒排索引：")
#Create_Level_Invertable("C:\\Users\\54215\\Desktop\\研究生课程\\信息检索\\作业\\clinicaltrials_txt\\000\\00000", clean=False)
#Create_Level_Invertable("C:\\Users\\54215\\Desktop\\研究生课程\\信息检索\\作业\\clinicaltrials_txt\\000\\00000", clean=True)
