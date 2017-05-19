#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import nltk
import string
import collections
from pymorphy import get_morph
morph = get_morph('/media/share')
from pymystem3 import Mystem
m=Mystem()

def text_to_token(text):  #разбиваем на токены, избавляемся от зн. преп.
	text = text.split()
	a=[]
	for word in text:
		#print word
		word = word.replace(u',','').replace(u'.','').replace(u'?','').replace(u'«','').replace(u'»','').replace(';','').replace(u'!','').replace('(','').replace(')','').strip() #костыль
		#print word
		if len(word) > 2:
			info = morph.get_graminfo(word.upper())
			#if info != '':  #что выдаст если граминфо ничего не вернул

			if info[0]['class'] == (u'С'):
				#temp = info[0]['norm'].encode('utf-8')
				a.append(info[0]['norm'])#.encode('utf-8'))
				#print word , ' ' , info[0]['norm']
	return a


#text_s = [i for i in text_s if ( i not in string.punctuation )]
def example_search(a): # freqdist подсчитывет кол-во раз употребления слова в тексте
	from nltk import FreqDist
	words = FreqDist(a)
	print 'Count of words(subj) in text: ',len(words)
	l_words = list(words.items())
	l_words.sort(key=lambda i:i[1],reverse=1)
	l_words = l_words[:10]
	print 'frequent words (keywords): '
	for word in l_words:
		word_to_dict(word[0])
		print word[0].encode('utf-8') , word[1]
	return l_words

def compute_tf(text):
#На вход берем текст в виде списка (list) слов
    #Считаем частотность всех терминов во входном массиве с помощью 
    #метода Counter библиотеки collections
	tf_text = collections.Counter(text)
	for i in tf_text:
        #для каждого слова в tf_text считаем TF путём деления
        #встречаемости слова на общее количество слов в тексте
		tf_text[i] = tf_text[i]/float(len(text))
		#print i, ' ',tf_text[i]
    #возвращаем объект типа Counter c TF всех слов текста
	   # tf_text.sort(key=lambda i:i[1],reverse=1)
	#tf_text.most_common()
	tf_list = list(tf_text.items())
 	tf_list.sort(key=lambda i:i[1], reverse=True)
 	tf_list = tf_list[:10]
	for i in tf_list:
		print i[0], ' ', i[1]
	return tf_list

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
	

f = open ('/media/share/text.txt', 'r')
text = f.read()
text1 = unicode(text, 'utf-8')

dictionary = {} 

if __name__ == '__main__':
	str = text_to_token(text1)
	#print str
	print '-----------------------способ 1---------------------'
	example_search(str)
	#print '-----------------------способ 2---------------------'
	#compute_tf(str)
	print 'Keyword dictionary:\n ', dictionary#.unicode('utf-8')