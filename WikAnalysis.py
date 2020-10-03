#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 10:38:16 2020

@author: stephencranney
"""

#Go to the specific Wikipedia portal you're interested in
#Click on "what links here" in the column to the left
#Then click 'namespace" and select article
#Then click on "500" on view, 
#Then go up to the browser and change "limit" from 500 to 2000 (or however high you need to go to get everything.)
#That's the website that you'll need to feed into beautifulsoup

websitetoscrape= 'https://en.wikipedia.org/w/index.php?title=Special:WhatLinksHere/Portal:Latter_Day_Saint_movement&namespace=0&limit=2000'

#This website doesn't have everything: https://pageviews.toolforge.org/massviews/. 

#pip install wikipedia
import pandas as pd
from bs4 import BeautifulSoup
import itertools
import requests
import re
import wikipedia
import networkx as nx
import community
from networkx.algorithms.community import k_clique_communities
from networkx.algorithms.community import greedy_modularity_communities


r = requests.get(websitetoscrape)
soup = BeautifulSoup(r.text, 'html.parser')

LINKS=[]
LINKS2=[]
numberofviews=[]
    
pattern = re.compile('(?<=wiki/)(.*)')

numberofviews=[]
###############Create list of items. 

for link in soup.find_all('a'): # find_all('a', {'href': True}):
    url = link.get('href')
    try:
        url2= 'https://en.wikipedia.org'+url
        pattern = re.compile('(?<=wiki/)(.*)')
        urltemp=pattern.findall(url2)
    except TypeError: 
        url= 'empty'
        url2= 'empty'
    LINKS.append(url)
    LINKS2.append(url2)

DF3= pd.DataFrame(columns = ['title', 'website'])
DF3['title']=LINKS 
DF3['website']=LINKS2
DF3.title=DF3.title.astype(str)
DF3.website=DF3.website.astype(str)

DF3['title2']= DF3['title'].str.contains(r'(^Special.*)')
DF3['title4']= DF3['title'].str.contains(r'(^None.*)')
DF3['title5']= DF3['title'].str.contains(r'(:.*)')   
DF3['title6']= DF3['title'].str.contains(r'(#.*)')  
DF3['title7']= DF3['title'].str.contains(r'(^empty.*)')
DF3['website2']= DF3['website'].str.contains(r'(.*index.*)')

DF3=DF3[DF3['title2']==False]
DF3=DF3[DF3['title4']==False]
DF3=DF3[DF3['title5']==False]
DF3=DF3[DF3['title6']==False]
DF3=DF3[DF3['website2']==False]
DF3=DF3[DF3['title7']==False]
websitelist= DF3['website'].tolist()
websitelist=list(set(websitelist))

listofwebsites=[]
    
#Now iterate through each page and get list. 
numberofviews=[]
title=[]

for i in websitelist:
    pattern = re.compile('(?<=wiki/)(.*)')
    urltemp=pattern.findall(i)
    try:
        infourl= 'https://en.wikipedia.org/w/index.php?title=' + urltemp[0] + '&action=info'
        r_temp = requests.get(infourl)
        soup_temp = BeautifulSoup(r_temp.text, 'html.parser')
        mydivs = soup_temp.find('div', attrs={"class":"mw-pvi-month"})
        Numberofviews=mydivs.text
        
        mydivs2 = soup_temp.find('tr', attrs={"id":"mw-pageinfo-display-title"})
        title2=mydivs2.text
        pattern = re.compile('(?<=Display title)(.*)')
        Title=pattern.findall(title2)
    except:
        Numberofviews='Error'
        Title= "Error"
    numberofviews.append(Numberofviews)
    title.append(Title)
    
DF= pd.DataFrame(columns = ['site', 'title', 'number_of_views_past_30'])
DF['site']=websitelist
DF['title']=title
DF['number_of_views_past_30']=numberofviews
DF['number_of_views_past_30']=numberofviews

DF['number_of_views_past_30']=DF['number_of_views_past_30'].str.replace(',','')
DF['number_of_views_past_30']=DF['number_of_views_past_30'].astype(int)

DF.to_csv('')  

DF= pd.read_csv('') #Read in same CSV file outputted as above in order to break up computation time  if needed. 

DF['title'] = DF['title'].str.replace("\[\'", "")
DF['title'] = DF['title'].str.replace("\'\]", "")

DF['title'] = DF['title'].str.replace('\[\"', '')
DF['title'] = DF['title'].str.replace('\"\]', '')

DF=DF[DF['title']!="Main Page"]

TITLE=DF['title'].tolist()

DF2= pd.DataFrame(columns = ['linksto', 'basepage'])

for i in TITLE:
    try:
        templinks=wikipedia.page(title=i).links
        df = pd.DataFrame()
        templinks=list(itertools.filterfalse(lambda x:x not in templinks,TITLE))
        df['linksto']=templinks
        df['basepage']=i
        DF2=DF2.append(df)
    except:
        pass

DF2.to_csv('')

DF2=pd.read_csv('')

DF2=pd.read_csv('')
DF2.columns=['Index', 'linksto', 'basepage']

#######################################Networks
#Then convert clusters from dictionary to pandas in order to report. 

G=nx.from_pandas_edgelist(DF2, source= 'basepage', target= 'linksto')
bc=nx.degree_centrality(G)

nx.draw(G, node_size=5)

partition = community.best_partition(G)





