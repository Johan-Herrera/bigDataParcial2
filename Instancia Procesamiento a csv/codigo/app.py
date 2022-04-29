import json
import csv
import requests
from bs4 import BeautifulSoup
import urllib.parse
import boto3
from datetime import datetime
url="headlines/raw/periodico=bbc/year="+datetime.today().strftime('%Y')+"/month="+datetime.today().strftime('%m')+"/day="+datetime.today().strftime('%d')+"/noticia.html"

s3 = boto3.client('s3')

def handler(event, context):
   # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    print("La key es: "+key)
    response = s3.get_object(Bucket=bucket, Key=key)
    texto=response['Body'].read()
    soup=BeautifulSoup(texto, 'lxml')
    titulares=soup.find_all("a",class_="media__link")
    texto_csv=""
    c="'"
    for i in range(len(titulares)):
        cont=0
        titulo1=""
        categoria=""
        if "https://www.bbc" in titulares[i].get('href'):
            enlace=titulares[i].get('href')
            for k in range(len(enlace)):
                if enlace[k]=="/":
                    cont=cont+1
                if cont>=3 and cont<=4 and k>19:
                    categoria=categoria+enlace[k]
            print(enlace)
            print(categoria)
            titulo=(titulares[i].getText()).split()
        else:
            enlace="https://www.bbc.com"+titulares[i].get('href')
            for j in range(len(enlace)):
                if enlace[j]=="/":
                    cont=cont+1
                if cont>=3 and cont<=4 and j>19:
                    categoria=categoria+enlace[j]
            print(enlace)
            print(categoria)
            titulo=(titulares[i].getText()).split()
        for t in range(len(titulo)):
            titulo1=titulo1+titulo[t]+"\t"
        print(titulo1)
        if i==len(titulares)-1:
            texto_csv=texto_csv+c+titulo1+c+","+c+categoria+c+","+c+enlace+c
        else:
            texto_csv=texto_csv+c+titulo1+c+","+c+categoria+c+","+c+enlace+"\n"
    print(texto_csv)
    data=texto_csv
    s3_1 = boto3.resource('s3')
    namefile='headlines/final/periodico=bbc/'+datetime.today().strftime('year=%Y/month=%m/day=%d/noticia')+'.csv'
    s3_1object=s3_1.Object('parcial2-csv', namefile)
    s3_1object.put(Body=data)
    exit()
    return {}