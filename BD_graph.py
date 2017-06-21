#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sqlite3
import graphviz as gv
from collections import OrderedDict
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
import ngram

conn = sqlite3.connect('test3.db')

c = conn.cursor()

# Create table
c.execute("drop table if exists denotat")
c.execute("drop table if exists direction")
c.execute("drop table if exists communications")

c.execute("""CREATE TABLE  denotat
	( 
	id_denotat int PRIMARY_KEY,
	name_denotat text 
	)
	""") 

c.execute("""CREATE TABLE  direction
	( 
	id_direct int PRIMARY_KEY,
	name_direction text 
	)
	""")

c.execute("""CREATE TABLE  communications 
	( 
	id_comm int PRIMARY KEY, 
	den1 int, 
	den2 int, 
	den3 int, 
	den4 int, 
	den5 int, 
	den6 int, 
	den7 int,  
	direct_comm int,
	direct_type real, 
	FOREIGN KEY(den1) REFERENCES denotat(id_denotat), 
	FOREIGN KEY(den2) REFERENCES denotat(id_denotat), 
	FOREIGN KEY(direct_comm) REFERENCES direction(id_direct) 
	)
	""")

#Insert a row of data

c.execute("INSERT INTO denotat(id_denotat, name_denotat) VALUES (10,'Жидкий кристалл (ЖК) (Смесь МВВА + ХХ)')")
c.execute("INSERT INTO denotat(id_denotat, name_denotat) VALUES (20,'Капля ЖК' )")
c.execute("INSERT INTO denotat(id_denotat, name_denotat) VALUES (30,'Состояние' )")
c.execute("INSERT INTO denotat(id_denotat, name_denotat) VALUES (40,'Стеклянная пластинка' ) ")
c.execute("INSERT INTO denotat(id_denotat, name_denotat) VALUES (50, 'Молекулярные слои') ")
c.execute("INSERT INTO denotat(id_denotat, name_denotat) VALUES (60, 'Рифление') ")
c.execute("INSERT INTO denotat(id_denotat, name_denotat) VALUES (70, 'Нижний слой') ")
c.execute("INSERT INTO denotat(id_denotat, name_denotat) VALUES (80, 'Верхний слой') ")
c.execute("INSERT INTO denotat(id_denotat, name_denotat) VALUES (90, 'Регистрирующий прибор') ")
c.execute("INSERT INTO denotat(id_denotat, name_denotat) VALUES (100, 'Самописец') ")
c.execute("INSERT INTO denotat(id_denotat, name_denotat) VALUES (110, 'Анализатор') ")
c.execute("INSERT INTO denotat(id_denotat, name_denotat) VALUES (120, 'Микроскоп') ")
c.execute("INSERT INTO denotat(id_denotat, name_denotat) VALUES (130, 'Фотоэлемент') ")
c.execute("INSERT INTO denotat(id_denotat, name_denotat) VALUES (140, 'Интенсивность света') ")
c.execute("INSERT INTO denotat(id_denotat, name_denotat) VALUES (150, 'Источник поляризованного света') ")
c.execute("INSERT INTO denotat(id_denotat, name_denotat) VALUES (160, 'Поляризованный свет') ")
c.execute("INSERT INTO denotat(id_denotat, name_denotat) VALUES (170, 'Генератор') ")
c.execute("INSERT INTO denotat(id_denotat, name_denotat) VALUES (180, 'Электромагнит') ")
c.execute("INSERT INTO denotat(id_denotat, name_denotat) VALUES (190, 'Магнитное поле') ")
c.execute("INSERT INTO denotat(id_denotat, name_denotat) VALUES (200, 'Индукция 0≤B≤10кГс') ")
c.execute("INSERT INTO denotat(id_denotat, name_denotat) VALUES (210, 'Направление B') ")
c.execute("INSERT INTO denotat(id_denotat, name_denotat) VALUES (220, 'Скорость изменения (dB/dt)') ")
c.execute("INSERT INTO denotat(id_denotat, name_denotat) VALUES (230, 'Критическое значение') ")
c.execute("INSERT INTO denotat(id_denotat, name_denotat) VALUES (240, 'Величина скорости изменения') ")
c.execute("INSERT INTO denotat(id_denotat, name_denotat) VALUES (250, 'Направление изменения') ")
c.execute("INSERT INTO denotat(id_denotat, name_denotat) VALUES (260, 'Убыль dB/dt < 0') ")
c.execute("INSERT INTO denotat(id_denotat, name_denotat) VALUES (270, 'Возрастание dB/dt > 0') ")
c.execute("INSERT INTO denotat(id_denotat, name_denotat) VALUES (280, '25+600 Гс/с') ")
c.execute("INSERT INTO denotat(id_denotat, name_denotat) VALUES (290, 'Закрепленный директор') ")
c.execute("INSERT INTO denotat(id_denotat, name_denotat) VALUES (300, 'Свободный директор') ")
c.execute("INSERT INTO denotat(id_denotat, name_denotat) VALUES (310, 'На определенный угол α') ")
c.execute("INSERT INTO denotat(id_denotat, name_denotat) VALUES (320, 'Параллельно магнитного полю') ")
c.execute("INSERT INTO denotat(id_denotat, name_denotat) VALUES (330, 'Переход нематик-холестик') ")
c.execute("INSERT INTO denotat(id_denotat, name_denotat) VALUES (340, 'Переход холестик-нематик') ")
c.execute("INSERT INTO denotat(id_denotat, name_denotat) VALUES (350, 'Холестерик') ")
c.execute("INSERT INTO denotat(id_denotat, name_denotat) VALUES (360, 'Нематик') ")
c.execute("INSERT INTO denotat(id_denotat, name_denotat) VALUES (370, 'Спиральная структруа') ")
c.execute("INSERT INTO denotat(id_denotat, name_denotat) VALUES (380, 'Шаг спирали') ")
c.execute("INSERT INTO denotat(id_denotat, name_denotat) VALUES (390, 'Направление плоскости поляризации') ")
c.execute("INSERT INTO denotat(id_denotat, name_denotat) VALUES (400, 'График I=I(B)') ")
c.execute("INSERT INTO denotat(id_denotat, name_denotat) VALUES (410, 'График ϴ=ϴ(t)') ")
c.execute("INSERT INTO denotat(id_denotat, name_denotat) VALUES (420, 'График I=I(t)') ")
c.execute("INSERT INTO denotat(id_denotat, name_denotat) VALUES (430, 'Релаксация') ")
c.execute("INSERT INTO denotat(id_denotat, name_denotat) VALUES (440, 'Поверхностное натяжение') ")
c.execute("INSERT INTO denotat(id_denotat, name_denotat) VALUES (450, 'Упругие свойства холестической спирали') ")
c.execute("INSERT INTO denotat(id_denotat, name_denotat) VALUES (460, 'Представлен в виде') ")
c.execute("INSERT INTO denotat(id_denotat, name_denotat) VALUES (470, 'Состоит') ")
c.execute("INSERT INTO denotat(id_denotat, name_denotat) VALUES (480, 'Характеризуется') ")
c.execute("INSERT INTO denotat(id_denotat, name_denotat) VALUES (490, 'Находится на') ")
c.execute("INSERT INTO denotat(id_denotat, name_denotat) VALUES (500, 'Состоит из') ")
c.execute("INSERT INTO denotat(id_denotat, name_denotat) VALUES (510, 'Может быть') ")
c.execute("INSERT INTO denotat(id_denotat, name_denotat) VALUES (520, 'Можеть иметь') ")
c.execute("INSERT INTO denotat(id_denotat, name_denotat) VALUES (530, 'Имеет') ")
c.execute("INSERT INTO denotat(id_denotat, name_denotat) VALUES (540, 'Помещается') ")
c.execute("INSERT INTO denotat(id_denotat, name_denotat) VALUES (550, 'В зависимости1') ")
c.execute("INSERT INTO denotat(id_denotat, name_denotat) VALUES (551, 'В зависимости2') ")
c.execute("INSERT INTO denotat(id_denotat, name_denotat) VALUES (552, 'В зависимости3') ")
c.execute("INSERT INTO denotat(id_denotat, name_denotat) VALUES (553, 'В зависимости4') ")
c.execute("INSERT INTO denotat(id_denotat, name_denotat) VALUES (554, 'В зависимости5') ")
c.execute("INSERT INTO denotat(id_denotat, name_denotat) VALUES (560, 'Или') ")
c.execute("INSERT INTO denotat(id_denotat, name_denotat) VALUES (570, 'Излучает') ")
c.execute("INSERT INTO denotat(id_denotat, name_denotat) VALUES (580, 'Проходит') ")
c.execute("INSERT INTO denotat(id_denotat, name_denotat) VALUES (590, 'Записывает') ")
c.execute("INSERT INTO denotat(id_denotat, name_denotat) VALUES (600, 'Обусловлен') ")
c.execute("INSERT INTO denotat(id_denotat, name_denotat) VALUES (610, 'Объясняется') ")
c.execute("INSERT INTO denotat(id_denotat, name_denotat) VALUES (620, 'Влияет на') ")
c.execute("INSERT INTO denotat(id_denotat, name_denotat) VALUES (630, 'Регистрирует') ")
c.execute("INSERT INTO denotat(id_denotat, name_denotat) VALUES (640, 'Изменяет') ")
c.execute("INSERT INTO denotat(id_denotat, name_denotat) VALUES (650, 'Описан на') ")
c.execute("INSERT INTO denotat(id_denotat, name_denotat) VALUES (660, 'Имеет значение') ")
c.execute("INSERT INTO denotat(id_denotat, name_denotat) VALUES (670, 'Зависит от') ")
c.execute("INSERT INTO denotat(id_denotat, name_denotat) VALUES (680, 'Питает') ")
c.execute("INSERT INTO denotat(id_denotat, name_denotat) VALUES (690, 'Создает') ")
c.execute("INSERT INTO denotat(id_denotat, name_denotat) VALUES (710, 'Совпадает с') ")
c.execute("INSERT INTO denotat(id_denotat, name_denotat) VALUES (720, 'α=α(B)') ")
c.execute("INSERT INTO denotat(id_denotat, name_denotat) VALUES (730, 'α≠α(B)') ")
c.execute("INSERT INTO denotat(id_denotat, name_denotat) VALUES (740, 'h=∞') ")
c.execute("INSERT INTO denotat(id_denotat, name_denotat) VALUES (750, 'h>2.5мм') ")
c.execute("INSERT INTO denotat(id_denotat, name_denotat) VALUES (760, 'h=2.5мм') ")
c.execute("INSERT INTO denotat(id_denotat, name_denotat) VALUES (770, 'Направлен вдоль') ")
c.execute("INSERT INTO denotat(id_denotat, name_denotat) VALUES (780, 'Вращается')")
 
 
c.execute("INSERT INTO direction(id_direct, name_direction) values(0,'Вниз')")
c.execute("INSERT INTO direction(id_direct, name_direction) values(1,'Вверх')")
c.execute("INSERT INTO direction(id_direct, name_direction) values(3,'В обе стороны')")
	
	
c.execute("INSERT INTO communications(id_comm, den1, den2, den3, den4, den5, den6, den7, direct_comm, direct_type) VALUES(10, 10,   460, 20,  0, 0, 0, 0, 0, 1) ")
c.execute("INSERT INTO communications(id_comm, den1, den2, den3, den4, den5, den6, den7, direct_comm, direct_type) VALUES(20, 20,   480, 30,  0, 0,	 0, 0,  0, 1) ")
c.execute("INSERT INTO communications(id_comm, den1, den2, den3, den4, den5, den6, den7, direct_comm, direct_type) VALUES(80, 20,   490, 40,  0, 0,	 0, 0,  0, 1) ")
c.execute("INSERT INTO communications(id_comm, den1, den2, den3, den4, den5, den6, den7, direct_comm, direct_type) VALUES(90, 20,   500, 50,  0, 0,	 0, 0,  0, 1) ")

c.execute("INSERT INTO communications(id_comm, den1, den2, den3, den4, den5, den6, den7, direct_comm, direct_type) VALUES(30, 30,   510, 550, 200, 360, 350, 0,  0, 1) ")
c.execute("INSERT INTO communications(id_comm, den1, den2, den3, den4, den5, den6, den7, direct_comm, direct_type) VALUES(40, 30,   520, 551, 250, 330, 340, 0,  0, 1) ") 

c.execute("INSERT INTO communications(id_comm, den1, den2, den3, den4, den5, den6, den7, direct_comm, direct_type) VALUES(50, 40,   530, 60,  0, 	 0, 0, 0,  0, 1) ")
c.execute("INSERT INTO communications(id_comm, den1, den2, den3, den4, den5, den6, den7, direct_comm, direct_type) VALUES(60, 40,	540, 190, 0, 	 0, 0, 0,  0, 1) ")

c.execute("INSERT INTO communications(id_comm, den1, den2, den3, den4, den5, den6, den7, direct_comm, direct_type) VALUES(70, 50,   660, 70,  80, 0, 0, 0,  0, 1) ")

c.execute("INSERT INTO communications(id_comm, den1, den2, den3, den4, den5, den6, den7, direct_comm, direct_type) VALUES(290, 70,  530, 290, 0, 	 0, 0, 0,  0, 1) ")

c.execute("INSERT INTO communications(id_comm, den1, den2, den3, den4, den5, den6, den7, direct_comm, direct_type) VALUES(300, 80,  530, 300, 0, 	 0, 0, 0,  0, 1) ")

c.execute("INSERT INTO communications(id_comm, den1, den2, den3, den4, den5, den6, den7, direct_comm, direct_type) VALUES(170, 90,  470, 100, 0, 	 0, 0, 0,  0, 1) ")
c.execute("INSERT INTO communications(id_comm, den1, den2, den3, den4, den5, den6, den7, direct_comm, direct_type) VALUES(180, 90,  470, 110, 120, 130, 0, 0,  0, 0.5) ")

c.execute("INSERT INTO communications(id_comm, den1, den2, den3, den4, den5, den6, den7, direct_comm, direct_type) VALUES(190, 100, 590, 400, 410, 420, 0, 0,  0, 1) ")


c.execute("INSERT INTO communications(id_comm, den1, den2, den3, den4, den5, den6, den7, direct_comm, direct_type) VALUES(160, 140, 630, 90,  0, 	 0, 0, 0,  0, 1) ")
c.execute("INSERT INTO communications(id_comm, den1, den2, den3, den4, den5, den6, den7, direct_comm, direct_type) VALUES(130, 150, 570, 160, 0, 	 0, 0, 0,  0, 0.5) ")
c.execute("INSERT INTO communications(id_comm, den1, den2, den3, den4, den5, den6, den7, direct_comm, direct_type) VALUES(140, 160, 580, 110, 120, 130, 0, 0, 0, 0.5) ")
c.execute("INSERT INTO communications(id_comm, den1, den2, den3, den4, den5, den6, den7, direct_comm, direct_type) VALUES(150, 160, 580, 20,  0, 	 0, 0, 0,  0, 1) ")
c.execute("INSERT INTO communications(id_comm, den1, den2, den3, den4, den5, den6, den7, direct_comm, direct_type) VALUES(120, 160, 480, 390, 140,  0, 0, 0,  0, 1) ")

c.execute("INSERT INTO communications(id_comm, den1, den2, den3, den4, den5, den6, den7, direct_comm, direct_type) VALUES(340, 170, 680, 180, 0, 	 0, 0, 0,  0, 1) ")
c.execute("INSERT INTO communications(id_comm, den1, den2, den3, den4, den5, den6, den7, direct_comm, direct_type) VALUES(350, 180, 690, 190, 0, 	 0, 0, 0,  0, 1) ")
c.execute("INSERT INTO communications(id_comm, den1, den2, den3, den4, den5, den6, den7, direct_comm, direct_type) VALUES(360, 190, 480, 220, 200, 210, 0, 0,  0, 1) ")
c.execute("INSERT INTO communications(id_comm, den1, den2, den3, den4, den5, den6, den7, direct_comm, direct_type) VALUES(370, 200, 530, 230, 0, 	 0, 0, 0,  0, 1) ")
c.execute("INSERT INTO communications(id_comm, den1, den2, den3, den4, den5, den6, den7, direct_comm, direct_type) VALUES(380, 210, 710, 60,  0, 	 0, 0, 0,  0, 1) ")
c.execute("INSERT INTO communications(id_comm, den1, den2, den3, den4, den5, den6, den7, direct_comm, direct_type) VALUES(390, 220, 480, 240, 250, 0, 0, 0,  0, 1) ")
c.execute("INSERT INTO communications(id_comm, den1, den2, den3, den4, den5, den6, den7, direct_comm, direct_type) VALUES(400, 240, 660, 280, 0, 	 0, 0, 0,  0, 1) ")
c.execute("INSERT INTO communications(id_comm, den1, den2, den3, den4, den5, den6, den7, direct_comm, direct_type) VALUES(410, 250, 660, 552, 170, 260, 270, 0,  0, 1)")
c.execute("INSERT INTO communications(id_comm, den1, den2, den3, den4, den5, den6, den7, direct_comm, direct_type) VALUES(100, 350, 640, 390, 0,  0, 0, 0,  0, 1) ")
c.execute("INSERT INTO communications(id_comm, den1, den2, den3, den4, den5, den6, den7, direct_comm, direct_type) VALUES(110, 350, 640, 140, 0,  0, 0, 0,  0, 0.5) ")

c.execute("INSERT INTO communications(id_comm, den1, den2, den3, den4, den5, den6, den7, direct_comm, direct_type) VALUES(200, 410, 600, 430, 0, 	 0, 0, 0,  0, 1) ")
c.execute("INSERT INTO communications(id_comm, den1, den2, den3, den4, den5, den6, den7, direct_comm, direct_type) VALUES(210, 430, 610, 440, 450, 0, 0, 0,  0, 1) ")
c.execute("INSERT INTO communications(id_comm, den1, den2, den3, den4, den5, den6, den7, direct_comm, direct_type) VALUES(220, 390, 620, 140, 0, 	 0, 0, 0,  0, 1) ")

c.execute("INSERT INTO communications(id_comm, den1, den2, den3, den4, den5, den6, den7, direct_comm, direct_type) VALUES(230, 350, 530, 370, 0, 	 0, 0, 0,  0, 1) ")
c.execute("INSERT INTO communications(id_comm, den1, den2, den3, den4, den5, den6, den7, direct_comm, direct_type) VALUES(240, 370, 480, 380, 0, 	 0, 0, 0,  0, 1) ")
c.execute("INSERT INTO communications(id_comm, den1, den2, den3, den4, den5, den6, den7, direct_comm, direct_type) VALUES(250, 380, 510, 553, 200, 740, 750, 760,  0, 1) ") 
c.execute("INSERT INTO communications(id_comm, den1, den2, den3, den4, den5, den6, den7, direct_comm, direct_type) VALUES(260, 360, 480, 740, 0, 	 0, 0, 0,  0, 1) ")
c.execute("INSERT INTO communications(id_comm, den1, den2, den3, den4, den5, den6, den7, direct_comm, direct_type) VALUES(270, 330, 650, 400, 410, 420, 0, 0,  0, 1) ")
c.execute("INSERT INTO communications(id_comm, den1, den2, den3, den4, den5, den6, den7, direct_comm, direct_type) VALUES(280, 330, 670, 240, 0, 	 0, 0, 0,  0, 1) ")

c.execute("INSERT INTO communications(id_comm, den1, den2, den3, den4, den5, den6, den7, direct_comm, direct_type) VALUES(310, 290, 770, 60,  0, 	 0, 0, 0,  0, 1) ")
c.execute("INSERT INTO communications(id_comm, den1, den2, den3, den4, den5, den6, den7, direct_comm, direct_type) VALUES(320, 300, 780, 554, 200, 310, 320, 0,  0, 1) ")
c.execute("INSERT INTO communications(id_comm, den1, den2, den3, den4, den5, den6, den7, direct_comm, direct_type) VALUES(330, 310, 560, 720, 730, 0, 0, 0,  0, 1) ")



den_d={}
com_d={}
graph=()

# Save (commit) the changes
conn.commit()
for row in c.execute('SELECT * FROM communications'):
	com_d[row[0]]={"den1" : row[1], "den2" : row[2], "den3" : row[3], "den4" : row[4], "den5" : row[5], "den6" : row[6], "den7" : row[7],  'direct_type' : row[9]}
	#print(com_d[row[0]])

for row in c.execute('SELECT * FROM denotat'):
	den_d[row[0]]={"den" : row[1]}
	#print(den_d[row[0]])


g2 = gv.Digraph(format='png')
count=1
d1=den_d.copy()
#print(den_d.items())


for a in d1:
	if a not in range(460,720,10) and a not in (770,780):
		#print(den_d[a]["den"]) #добавляем вершину shape box
		g2.node(den_d[a]["den"], shape = 'box')
		del den_d[a]
	else: 
		if a in (550, 551, 552, 553, 554):
			#for i in (1,2,3,4,5):
			g2.node(den_d[a]["den"], shape='diamond')
			del den_d[a]
			#count+=1
		#print(den_d[a]["den"]) # лейблы для ребра rроме "в зависимости от", все подписи для дуг, а взт - даймонд 

#print(com_d)
#for k in sorted(den_d.keys()):
	#print(k, ':', den_d[k])

count=0
for a in com_d:
	#если в вершине 4 нет 550, но есть вершина 5(непустая) и/или 6, то просто две связи, иначе в зависимости от и тд как в граф.пайы
	#print(com_d[a]["den4"])
	a1=com_d[a]["den1"]
	a2=com_d[a]["den2"]
	a3=com_d[a]["den3"]
	a4=com_d[a]["den4"]
	a5=com_d[a]["den5"]
	a6=com_d[a]["den6"]
	a7=com_d[a]["den7"]
	a9=com_d[a]["direct_type"]
	stl='solid'
	#print(a1)
	if a9 == 0.5: stl='dotted'
	if a3 not in (550, 551, 552, 505, 554):				#a2 always comm
		if a5 != 0:
			#print(a1 , '  ' , a2 , '  ' , a3)
			g2.edge(d1[a1]["den"], d1[a3]["den"], label = den_d[a2]["den"] , style = stl )
			g2.edge(d1[a1]["den"], d1[a4]["den"], label = den_d[a2]["den"] , style = stl )
			g2.edge(d1[a1]["den"], d1[a5]["den"], label = den_d[a2]["den"] , style = stl )
		else:
			if a4 !=0:
				g2.edge(d1[a1]["den"], d1[a3]["den"],  label = den_d[a2]["den"] , style = stl )
				g2.edge(d1[a1]["den"], d1[a4]["den"],  label = den_d[a2]["den"] , style = stl )
			else:
				if a3 != 0:
					g2.edge(d1[a1]["den"], d1[a3]["den"], label = den_d[a2]["den"] , style = stl )
	else:
		count+=1
		temp = d1[a3]["den"] + str(count)
		#print(temp)
		if a7 != 0:
			g2.edge(d1[a1]["den"], temp , style = stl )
			g2.edge(temp, d1[a4]["den"])
			g2.edge(temp, d1[a5]["den"],  label = den_d[a2]["den"] , style = stl )
			g2.edge(temp, d1[a6]["den"],  label = den_d[a2]["den"] , style = stl )
			g2.edge(temp, d1[a7]["den"],  label = den_d[a2]["den"] , style = stl )
		else:
			if a6 !=0:
				g2.edge(d1[a1]["den"], temp , style = stl )
				g2.edge(temp, d1[a4]["den"])
				#print(den_d[a2]["den"] )
				g2.edge(temp, d1[a5]["den"], label = den_d[a2]["den"] , style = stl )
				g2.edge(temp, d1[a6]["den"], label = den_d[a2]["den"] , style = stl )
		

g2.render('img/denotat')
# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()

edge_count = 0;
node_count = 0;
for a in com_d:
	if com_d[a]["den4"] == 0 : edge_count+=1
	else:
		if com_d[a]["den5"] == 0 : edge_count+=2
		else:
			if com_d[a]["den6"] == 0 : edge_count+=4
			else:
				if com_d[a]["den7"] == 0 : edge_count+=5

node_count = len(range(10,460,10)) + len(range(720,770,10)) +5
#print('количество вершин: ', node_count, '  ', 'количество ребер: ', edge_count)

list_sm = [i for i in range(10,460,10)]#
list_sm.extend([i for i in range(720,770,10)])
list_sm.extend([i for i in range(550,555,1)])

list_sm1 = sorted(list_sm)

list_smm=[]
for c in range(len(list_sm1)):
	a = list_sm1[c]

	list_smm.append([])
	if a not in (550, 551, 552, 553, 554):
		for b in com_d:		
			if com_d[b]["den1"] == a:
				if com_d[b]["den3"] in (550, 551, 552, 553, 554):
				
					list_smm[c].append(list_sm1.index(com_d[b]["den3"]))
						
				else:
					if com_d[b]["den4"] == 0:
						
						list_smm[c].append(list_sm1.index(com_d[b]["den3"]))
				
					else:
						if com_d[b]["den5"] == 0:
						
							list_smm[c].append(list_sm1.index(com_d[b]["den3"]))
							list_smm[c].append(list_sm1.index(com_d[b]["den4"]))
							
						else:
							if com_d[b]["den6"] == 0:
							
								list_smm[c].append(list_sm1.index(com_d[b]["den3"]))
								list_smm[c].append(list_sm1.index(com_d[b]["den4"]))
								list_smm[c].append(list_sm1.index(com_d[b]["den5"]))
								
								
	else:
		for b in com_d:
			if com_d[b]["den3"] == a:
				if com_d[b]["den7"] == 0:
			
					list_smm[c].append(list_sm1.index(com_d[b]["den4"]))
					list_smm[c].append(list_sm1.index(com_d[b]["den5"]))
					list_smm[c].append(list_sm1.index(com_d[b]["den6"]))
			
				else:
					
					list_smm[c].append(list_sm1.index(com_d[b]["den4"]))
					list_smm[c].append(list_sm1.index(com_d[b]["den5"]))
					list_smm[c].append(list_sm1.index(com_d[b]["den6"]))
					list_smm[c].append(list_sm1.index(com_d[b]["den7"]))
#list_smm - список смежности 0 - [,,,] , 1- [,,,] ...
#матрица смежности
matrix = [[0] * len(list_smm) for i in range(len(list_smm))]
for j in range(len(list_smm)) : 
	for i in list_smm[j]:  
		matrix[j][i] =matrix[i][j]= 1		


def alloc_colloc(text):
	bigram_measures = nltk.collocations.BigramAssocMeasures()
	trigram_measures = nltk.collocations.TrigramAssocMeasures()
	delete_zn = re.compile(u'\W+?', re.UNICODE)
	text = text.split()
	a=[]
	for word in text:
		word = morph.parse(delete_zn.sub('', word))[0]
		#if word.tag.POS in ('NOUN', 'ADJF', 'ADJS', 'VERB','INFN'):
		a.append(word.normal_form)
	text = a

	
	finder = BigramCollocationFinder.from_words(text)
	finder.apply_freq_filter(1)
	#finder.apply_word_filter(lambda w: len(w) < 3 or w.lower() in stop_words) 
	#f = finder.nbest(bigram_measures.pmi, 25)

	lik = finder.score_ngrams(bigram_measures.likelihood_ratio)
#	pm = finder.score_ngrams(bigram_measures.pmi)
#	sq = finder.score_ngrams(bigram_measures.dice) #chi_sq
#	stt = finder.score_ngrams(bigram_measures.student_t)

	#f = open ('/media/share/results.txt', 'w')
	list_of_colloc = []
	
	#print('-------------')
	#print('-------------')
	#print('Метрика likelyhood:')
	for col in lik[1:50]:
		list_of_colloc.append(col[0])
			#print(col[0],'       ',col[1])
	return list_of_colloc

def search_meanword(query):
	#print('-----------')
	#print('-----------')
	list_dict= ['Википедия','Большой Энциклопедический словарь', 'Большая советская энциклопедия','Фразеологический словарь русского литературного языка']
	link=''
	query.lower()
	query.replace (" ", "+")

	r = requests.get('http://dic.academic.ru/searchall.php?SWord='+query+'&from=xx&to=ru&did=&stype=')
	soup = BeautifulSoup(r.text ,"html.parser")
	q1=bool(0)
	i=1
	for items in soup.find_all('ul', attrs={'class' : 'terms-list'}):#, attrs={'li' : 'r'}):
		for it in items.find_all('li'):
			if it.p.strong.a.text.find(query) != -1: 
				link = it.a['href']
				#print(it.p.text)
				#print(it.find('p',attrs={'class':'src'}).text + '\n')
				q1=bool(1)
	return link

def get_meanword(link):	
	meaning_str = -2
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
	return meaning_str



visited = [False for i in range(len(list_smm))] #массив для хранения информации о пройденных и не пройденных вершинах
path=[]

word='Молекулярные слои'
#word1='Величина скорости изменения'

def dfs(v):
	#print(word)
	q=False
	path.append(v+1)
	visited[v] = True
	for vertex in list_smm[v]:  #задаю слово - ищет его в дереве, сохраняет путь до него
		if word == d1[list_sm1[vertex]]["den"] or d1[list_sm1[vertex]]["den"].find(word) != -1 :
			q=True
		if not visited[vertex] and not q:
			#print(path)
			dfs(vertex)
	return q	

#word=''
strr=[]
referat=[]
stop_words = stopwords.words('russian')
f = open ('/media/share/ref3.txt', 'r')
text = f.read()
collocs = []
meaning = {}

collocs = alloc_colloc(text)

for col in collocs:
	col = col[0]+' '+col[1]	
	if search_meanword(col) != '':
		meaning[col] = 1
	else:
		meaning[col] = -1
		#print(col)
		col1 = col.split()

		if len(col1) > 1:
			if col1[0] != '':
				a=col1[0]
				if search_meanword(a) != '':
				#	meaning[a] = 1
					meaning[col] = 0

			if col1[1] != '':	
				b=col1[1]
				if search_meanword(b) != '':
				#	meaning[b] = 1 
					meaning[col] = 0
		else:
			if search_meanword(col1[0]) != '':
				#print(search_meanword(col1[0]))
				meaning[col] = 0

m1=sorted(meaning.items(),key=lambda x:x[1],reverse=True) ## получается много 0-взвешенных коллокаций из-за поиска по каждому слову
														  ## определяются словарными статьями глаголы, числительные и тд

### Поиск коллокаций в графе - не работает.
for mean in m1:
	word=str(mean[0]).capitalize()		
	if dfs(list_sm1.index(10)):
		referat.append(mean[0])
	else:
		word1 = str(word).split()
		if len(word1) > 1:
			if word1[0] != '':
				word = word1[0].capitalize()
				if dfs(list_sm1.index(10)):
					referat.append(mean[0])

			if word1[1] != '':	
				word = word1[1].capitalize()
				if dfs(list_sm1.index(10)):
					referat.append(mean[0])
		else:
			word = str(word1)[0].capitalize()
			if dfs(list_sm1.index(10)):
				referat.append(mean[0])
print(referat)
