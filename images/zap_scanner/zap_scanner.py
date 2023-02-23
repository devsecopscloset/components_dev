#!/usr/bin/python3

import requests
import os
import zapv2
from pprint import pprint
import time

zap_url=os.environ['zap_url']
context_id=os.environ['context_id']
user_id=os.environ['user_id']
apiKey=os.environ['zap_api_key']
result_file_name=os.environ['result_file_name']

ascan_url = '/JSON/ascan/action/scanAsUser/'
report_url = '/OTHER/core/other/xmlreport/'
api_param = 'apikey='
context_id_param = 'contextId='
user_id_param = 'userId='
scan_id_param = 'scanId='

## Simple GET based calls
headers = {
  'Accept': 'application/json',
  'X-ZAP-API-Key': 'API_KEY'
}

# r = requests.get('http://'+zap_url+'/JSON/ascan/action/scan/scanAsUser/', params={
#     'contextId' : context_id,
#     'userId' : user_id
# }, headers = headers)
# print(r.json())

zap = zapv2.ZAPv2(apikey=apiKey, proxies={'http': zap_url, 'https': zap_url})
scan_url=zap_url+ascan_url+'?'+api_param+apiKey+'&'+context_id_param+context_id+'&'+user_id_param+user_id

scanid=zap.ascan.scan(url=scan_url,apikey=apiKey)
while int(zap.ascan.status(scanid)) < 100:
    # Loop until the scanner has finished
    print('Scan progress %: {}'.format(zap.ascan.status(scanid)))
    time.sleep(5)

print('Scan is Completed')

r = requests.get(zap_url+report_url+'?'+scan_id_param+scanid , params={}, headers=headers)

with open('/results/'+result_file_name+'.xml', 'wb') as f:
  f.write(r.content)