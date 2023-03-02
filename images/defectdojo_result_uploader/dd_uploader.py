import yaml
import requests
import json
from datetime import date
from datetime import datetime as dt
import subprocess
from requests_toolbelt import MultipartEncoder
from pathlib import Path
import os
import glob

def dd_setup():
    global DD_URL
    DD_URL=os.environ['dd_url']

    global dd_username
    dd_username=os.environ['dd_username']
    
    global dd_password
    dd_password=os.environ['dd_password']

    global DD_TOKEN
    DD_TOKEN=auth()

    global DD_PRODUCT_NAME
    DD_PRODUCT_NAME=os.environ['dd_product_name']

    global DD_PROD_DESC
    DD_PROD_DESC=os.environ['dd_product_desc']
    
    global result_file
    result_file=os.listdir('/results')
    for i in result_file:
        if i.endswith('.conf'):
            result_file.remove(i)
    
    global pipeline_no
    pipeline_no = os.environ['pno']

    global DD_SCANTYPE
    DD_SCANTYPE=result_file[0]
    print(DD_SCANTYPE)

    global ENG_NAME
    ENG_NAME='Pipeline No '+pipeline_no
    print(ENG_NAME)

def auth():
    creds={
        'username' : dd_username,
        'password' : dd_password
    }
    r = requests.post(DD_URL+'/api/v2/api-token-auth/',
    data=json.dumps(creds),headers={'Content-Type': 'application/json'} )
    return r.content.decode('UTF-8').split('"')[3]

def get_prod_id():
    r=requests.get(DD_URL+'/api/v2/products', headers={'Authorization': 'Token '+DD_TOKEN})
    for i in r.json()['results']:
        if i['name']==DD_PRODUCT_NAME:
            return i['id']
    return None

def get_eng_id():
    r=requests.get(DD_URL+'/api/v2/engagements', headers={'Authorization': 'Token '+DD_TOKEN})
    for i in r.json()['results']:
        print(i)
        if i['name']==ENG_NAME:
            return i['id']
    return None


def create_prod():
    today = date.today()
    t_date=today.strftime('%Y-%m-%d')
    fields={
    'name': DD_PRODUCT_NAME,
    'product_name': DD_PRODUCT_NAME,
    'prod_type':'1',
    'description': DD_PROD_DESC
    }
    r = requests.post(DD_URL+'/api/v2/products/',
    data=json.dumps(fields),headers={'Content-Type': 'application/json',
    'Authorization': 'Token '+DD_TOKEN} )
    return r.json()['id']

def create_eng():
    today = date.today()
    t_date=today.strftime('%Y-%m-%d')
    fields={
    'name': ENG_NAME,
    'product':str(get_prod_id()),
    'engagement_type':'CI/CD',
    'target_start': str(t_date),
    'prod_type':'1',
    'target_end': str(t_date),
    'description': 'Pipeline no: ' + ENG_NAME + ' Scans'
    }
    r = requests.post(DD_URL+'/api/v2/engagements/',
    data=json.dumps(fields),headers={'Content-Type': 'application/json',
    'Authorization': 'Token '+DD_TOKEN} )


def upload_scan():
    
    mp_encoder = MultipartEncoder(
    fields={
        'scan_type': DD_SCANTYPE,
        'product_name':DD_PRODUCT_NAME,
        'engagement_name': ENG_NAME,
        'name': ENG_NAME,
        'engagement': str(get_eng_id()),
        'file':(result_file[latest], open('/results/'+result_file[latest], 'rb'), 'application/json')
        }
    )
    r = requests.post(DD_URL+'/api/v2/import-scan/',
        data=mp_encoder,headers={'Content-Type': mp_encoder.content_type,
        'Authorization': 'Token '+DD_TOKEN} )

if __name__=="__main__":
    dd_setup()
    if(get_prod_id()):
        if(get_eng_id()):
            print('Exists')
            upload_scan()
        else:
            create_eng()
            upload_scan()
    else:
        create_prod()
        create_eng()
        upload_scan()