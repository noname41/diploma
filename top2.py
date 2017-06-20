#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import re
import nltk
import string
import collections
import pymorphy2
import nltk
morph = pymorphy2.MorphAnalyzer()
from pymystem3 import Mystem
m=Mystem()

def text_to_token(text):  #разбиваем на токены, избавляемся от зн. преп.
	text = text.split()
	a=[]
	for word in text:
		word = morph.parse(delete_zn.sub('', word))[0]
		if word.tag.POS == 'NOUN':
		#	print(word.normal_form)
			a.append(word.normal_form)
	return a


#text_s = [i for i in text_s if ( i not in string.punctuation )]
def example_search(a): # freqdist подсчитывет кол-во раз употребления слова в тексте
	words = nltk.FreqDist(a)
	print('Count of words(noun) in text: ',len(words))
	l_words = list(words.items())
	l_words.sort(key=lambda i:i[1],reverse=1)
	l_words = l_words[:10]
	print('frequent words (keywords): ')
	for word in l_words:
		#word_to_dict(word[0])
		print(word[0], word[1]/len(words))
	return l_words

def word_to_dict(word):

	lemma = m.analyze(word)
	temp = lemma[0]['analysis'][0]['gr']
	temp_part = temp.split(',')[0]
	temp_gen = temp.split(',')[1]
	temp_od = temp.split(',')[2].split('=')[0]  #для существительных
	if temp.find('(') != -1:
	#	#возможноые падежы 
		temp_c =  temp.split('(')[1].split(',')[0] + "/" + temp.split('(')[1].split('|')[1].split(',')[0]
		#возможные числа(ед,мн)
		temp_sp = temp.split('(')[1].split(',')[1].split('|')[0] + "/" + temp.split('(')[1].split('|')[1].split(',')[1].split(')')[0]
	else:
		temp_c = temp.split('=')[1].split(',')[0] 
		temp_sp = temp.split('=')[1].split(',')[1]

	#print temp_c, '  ', temp_sp

	dictionary[word] = {"part_of_speech":temp_part , "characteristic":temp_od, "case":temp_c , "sing/plur":temp_sp}

def compute_tf(text):
#На вход берем текст в виде списка (list) слов
    #Считаем частотность всех терминов во входном массиве с помощью 
    #метода Counter библиотеки collections
	tf_text = collections.Counter(text)
	for i in tf_text:
        #для каждого слова в tf_text считаем TF путём деления
        #встречаемости слова на общее количество слов в тексте
		tf_text[i] = tf_text[i]/float(len(text))
    #возвращаем объект типа Counter c TF всех слов текста
	tf_text[1].sort(key=lambda i:i[1],reverse=1)
	tf_text = tf_text[:10]
	return tf_text	


f = open ('/media/share/usa.txt', 'r')
text = f.read()
delete_zn = re.compile(u'\W+?', re.UNICODE)
#text1 = unicode(text, 'utf-8')
dictionary = {} 

if __name__ == '__main__':
	str1 = text_to_token(text)
	example_search(str1)
	#print('Keyword dictionary:\n ', dictionary)
#	print(compute_tf(str1))
