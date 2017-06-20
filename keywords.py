#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import pymorphy2
morph = pymorphy2.MorphAnalyzer()
import nltk
from nltk.collocations import *
from collections import defaultdict
from nltk.corpus import stopwords
from bs4 import BeautifulSoup
import urllib3
import requests



def alloc_colloc(text):
	bigram_measures = nltk.collocations.BigramAssocMeasures()
	trigram_measures = nltk.collocations.TrigramAssocMeasures()
	delete_zn = re.compile(u'\W+?', re.UNICODE)
	text = text.split()
	a=[]
	for word in text:
		word = morph.parse(delete_zn.sub('', word))[0]
		if word.tag.POS in ('NOUN', 'ADJF', 'ADJS', 'VERB','INFN'):
				a.append(word.normal_form)
	text = a

	
	finder = BigramCollocationFinder.from_words(text)
	finder.apply_freq_filter(1)
	#finder.apply_word_filter(lambda w: len(w) < 3 or w.lower() in stop_words) 
	#f = finder.nbest(bigram_measures.pmi, 25)

	lik = finder.score_ngrams(bigram_measures.likelihood_ratio)
	pm = finder.score_ngrams(bigram_measures.pmi)
	sq = finder.score_ngrams(bigram_measures.dice) #chi_sq
	stt = finder.score_ngrams(bigram_measures.student_t)

	#f = open ('/media/share/results.txt', 'w')
	list_of_colloc = []
	
	print('-------------')
	print('-------------')
	print('Метрика likelyhood:')
	for col in lik[1:50]:
		print(col[0],'       ',col[1])
	
	print('-------------')
	print('Метрика pmi:')
	for col in pm[1:50]:
		list_of_colloc.append(col[0])
		print(col[0],'       ',col[1])

	print('-------------')
	print('Метрика dice:')
	for col in sq[1:50]:
		print(col[0],'       ',col[1])

	print('-------------')
	print('Метрика student_t:')
	for col in stt[1:50]:
		print(col[0],'       ',col[1])
	
	return list_of_colloc


def search_meanword(query):
	print('-----------')
	print('-----------')
	list_dict= ['Википедия','Большой Энциклопедический словарь', 'Большая советская энциклопедия','Фразеологический словарь русского литературного языка']
	link=''
	query.lower()
	query.replace (" ", "+")
	r = requests.get('http://dic.academic.ru/searchall.php?SWord='+query+'&from=xx&to=ru&did=&stype=0')
	soup = BeautifulSoup(r.text ,"html.parser")
	q=bool(0)
	i=1
	for items in soup.find_all('ul', attrs={'class' : 'terms-list'}):#, attrs={'li' : 'r'}):
		for it in items.find_all('li'):
			if it.p.strong.a.text.find(query) != -1: 
				link = it.a['href']
				print(it.p.text)
				#print(it.p.text)
				print(it.find('p',attrs={'class':'src'}).text + '\n')
				q=bool(1)

	meaning_str = ''
	if link != '':
		r1 = requests.get(link)
		soup1 = BeautifulSoup(r1.text,'html.parser')
		for items in soup1.find_all('div', attrs={'class' : 'content'}):
			temp = items.find('dd',attrs={'class':'descript'})
			for p in temp.find_all('p'):
				i+=1
				if i in range(2,8):
					print(p.text + '\n')
					meaning_str+=p.text + '\n'
					
	else:
		print('Словарных статей не найдено')
	return meaning_str




stop_words = stopwords.words('russian')
f = open ('/media/share/ref1.txt', 'r')
text = f.read()
collocs = []
meaning = {}
collocs = alloc_colloc(text)
#for col in collocs:
#	col = col[0]+' '+col[1]	
	#meaning[col] = {'Словарная статья':(search_meanword(col))}
#print(meaning)

# словарные статьи - находим коллоки, записываем в словарь и дальше в графвиз	