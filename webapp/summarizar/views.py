from django.shortcuts import render
from bs4 import BeautifulSoup as soup
from urllib.request import Request,urlopen
import heapq
import string
import re
import nltk
from nltk.corpus import stopwords
from nltk import sent_tokenize,word_tokenize
STOP_WORD=stopwords.words('english')


def get_text(link):
    req=Request(link,headers={'User-Agent':'Mozilla/5.0'})
    page=urlopen(req)
    bs4page=soup(page,'html.parser')
    element=bs4page.find_all('p')
    document=''
    for i in element:
        document+=(i.text)
    return document

def clean_text(document,lines,itype):
    if itype=='LINK':
        document=get_text(document)
    document = document.replace(r'^\s+|\s+?$','')
    document = document.replace('\n',' ')
    document = document.replace("\\",'')
    document = document.replace(",",'')
    document = document.replace('"','')
    document = re.sub(r'\[[0-9]*\]','',document)
    sentences=sent_tokenize(document)
    word_frequency={}
    document_for_word=document.lower()
    for word in word_tokenize(document_for_word):
        if word not in STOP_WORD and word not in string.punctuation:
            if word not in word_frequency.keys():
                word_frequency[word]=1
            else:
                word_frequency[word]+=1
    word_frequency
    max_frequency=max(word_frequency.values())
    for word in word_frequency.keys():
        word_frequency[word]=(word_frequency[word]/max_frequency)
    word_frequency
    sentence_score = {}
    for sent in sentences:
        for word in word_tokenize(sent):
            if word in word_frequency.keys():
                if len(sent.split(' '))<100:
                    if sent not in sentence_score.keys():
                        sentence_score[sent] = word_frequency[word]
                    else:
                        sentence_score[sent]+=word_frequency[word]
    sentence_score
    summary=heapq.nlargest(lines,sentence_score,key=sentence_score.get)
    summary=' '.join(summary)
    return summary



def index(request):
    result=""
    if request.method=='POST':
        if request.POST.get('text'):
            document=request.POST.get('text')
            result=clean_text(document,4,'TEXT')
            return render(request,'index.html',{'content':result})
        elif request.POST.get('url'):
            document=request.POST.get('url')
            result=clean_text(document,4,'LINK')
            return render(request,'index.html',{'content':result})
    return render(request,'index.html',{'content':result})