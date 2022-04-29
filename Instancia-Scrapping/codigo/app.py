import requests
import json
from datetime import datetime
import boto3
url="https://www.bbc.com/"
r=requests.get(url)
s3 = boto3.resource('s3')

def handler(event,context):
        text = r.text
        namefile='headlines/raw/periodico=bbc/'+datetime.today().strftime('year=%Y/month=%m/day=%d/noticia')+'.html'
        s3object =s3.Object('parcial2-datos', namefile)
        s3object.put(Body=text)
        return {}