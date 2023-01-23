from django.shortcuts import render,redirect,HttpResponseRedirect,reverse
import psycopg2
import pandas as pd
from sqlalchemy import create_engine
import json 
from bs4 import BeautifulSoup
import requests
import re
import string

# def index(request):
#     return (request,'search_database/search.html')
def search(request):
    try:
        connection = psycopg2.connect(user="postgres",
                                    password="Bhadra123",
                                    host="127.0.0.1",
                                    port="5433",
                                    database="postgresql")
    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)
        # connection = psycopg2.connect(user="postgres",
        #                               password="Bhadra123",
        #                               host="127.0.0.1",
        #                               port="5432",
        #                               database="django-database")
    data1 = pd.read_sql("select * from search",connection)
    columns = data1.columns
    #print(columns)
    data1.columns = map(str.upper, data1.columns)
    data1.columns = [c.replace('_', ' ') for c in data1]
    col = data1.columns
    if request.method=="POST":
            answer =  request.POST.getlist("name")
            coulumns = request.POST.getlist('texts')
            fruits = request.POST.getlist('fruits')
            col_names = request.POST.getlist('col-name')
            # print(fruits)
            # print(col_names)
            # print(coulumns)

            # print(col_names)
            # print(fruits)
            # print('|'.join(filter(None, coulumns)))  
            d = coulumns[0]
            s =  "||' '||"
            answer = s.join(filter(None, col_names))
            #print(answer)     
            pd.set_option('display.expand_frame_repr', False)
            if len(answer) >0 and len(coulumns) != len(col_names):
                #print('kk')
                data1 = pd.read_sql("SELECT * FROM search WHERE to_tsvector({})@@to_tsquery('{}')".format(answer,d),connection)
                pd.set_option('display.expand_frame_repr', False)
            elif len(coulumns)>0 and len(answer)<=1 and len(coulumns) != len(col_names):
                #print('kl')
                data1 = data1[data1.apply(lambda row: row.astype(str).str.contains('|'.join(filter(None, coulumns)), case=False).any(), axis=1)]
            elif len(coulumns) == len(col_names):
                #print('jai')
                dfs = []
                for i in range(len(coulumns)):
                    df = pd.read_sql("SELECT * FROM search WHERE {} ~ '{}';".format(col_names[i],coulumns[i]),connection);
                    pd.set_option('display.expand_frame_repr', False);
                    dfs.append(df)
                data1 = pd.concat(dfs, axis=0, ignore_index=True)

            #print(data1)
            # elif len(coulumns)>0 and len(answer)>=1:
            #     data1.loc[data1['DRUG'].str.contains('entinostat.') | data1['DRUG'].str.contains('Cisplatin.')]

            data = data1.to_json()
            request.session['data'] = data   
            return redirect("/table/")
        
    return render(request,'search_database/search.html',{'columns':columns,'col':col})
    
def table(request):    
    data = request.session['data'] 
    data = pd.DataFrame(eval(data))
    columns = ['index', 'target_s_or_mechanism_of_action', 'COMBINATION', 'CANCER_TYPE', 'STR_LINK (SMILES)']
    columns = [x.upper() for x in columns]
    columns = [c.replace('_', ' ') for c in columns]
    # data2 = data.copy()
    data.columns = map(str.lower, data.columns)
    data.columns = [c.replace(' ', '_') for c in data]
    # print(data['index'])
    # print(d)
    #columns = data.columns[0:7]
    json_records = data.to_json(orient ='records') 

    d = [] 

    d = json.loads(json_records) 

    #print(d)
    # index = data['INDEX']
    # status = data['STATUS']
    # paper_number = data['PAPER NUMBER']
    # pmid = data['PMID']
    # drug = data['DRUG']
    # drug_id = data['DRUG ID']
    # target_s_or_mechanism_of_action = data['TARGET S OR MECHANISM OF ACTION']
    

    
   # print(columns)
    # columns = data.columns[0:7] 
    # ['index', 'status', 'paper_number', 'pmid', 'drug', 'drug_id',
    #    'target_s_or_mechanism_of_action']
    # #data = data1.to_html()
    context = {'columns':columns,'d':d}

    # print(data1)
    return render(request,'search_database/search2.html',context)

def page(request,pk):
    try:
        connection = psycopg2.connect(user="postgres",
                                    password="Bhadra123",
                                    host="127.0.0.1",
                                    port="5433",
                                    database="postgresql")
    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)

    get = str(pk)
    print(get)
    data1 = pd.read_sql("SELECT * FROM search WHERE index LIKE '{}' ".format(get),connection)
    pd.set_option('display.expand_frame_repr', False)
    #print(data1)
    for i in data1['drug_id'].values:
        print(i)
        x = i.split("(")
        print(x[0])
        x = str(x[0])
        x=x.replace(" ", "")
    for i in data1['kegg_drug_id'].values:
        if i != 'Data Not Available':
            print(i)
            y = i
    print(y)
    url = "https://go.drugbank.com/drugs/"+str(x)
    u = url
    url3 = 'https://www.genome.jp/entry/'+str(y)
    url2 = "https://www.genome.jp/kegg-bin/simcomp_list?id="+str(y)
    u2 = url3
    req2 = requests.get(url2)
    req = requests.get(url)
    text = []
    soup2 = BeautifulSoup(req2.text, "html.parser")
    page = requests.get(url2)
    if (page.status_code == 200):
        html_text = BeautifulSoup(page.text, "html.parser")
    data= html_text.find_all('pre')[0].get_text()
    lines  = [x.split(';') for x in re.split('\n\xa0', data) if x != ' \r']
    kegg = []
    for i in lines:
        for j in i[0:]:
            kegg.append(j.translate({ord(c): None for c in string.whitespace}))
    
    score = []
    entry = []
    for i in kegg[1:]:
        er = i.split('.')
        entry.append(er[0][:-1])
        score.append(er[0][-1]+"."+er[1])

    df = pd.DataFrame(list(zip(entry, score)),
               columns =['entry', 'score'])
    json_records = df.to_json(orient ='records')
    di = json.loads(json_records)



    url2 ='https://www.genome.jp/Fig/drug/'+str(y)+'.gif'
    soup = BeautifulSoup(req.text, "html.parser")
    for data in soup.find_all("p"):
        summary= data.get_text()
        break
    url = 'https://go.drugbank.com/structures/'+str(x)+'/image.svg/'
    print(url)
    #'summary':summary,'x':x,'url':url
    context={'data1':data1,'x':get,'url':url,'summary':summary,'url2':url2,'di':di,'u':u,'u2':u2}

    return render(request,'search_database/page.html',context)