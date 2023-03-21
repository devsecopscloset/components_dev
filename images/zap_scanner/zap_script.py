import requests
import json
import os

ZAP_SOURCE=os.environ['zap_url']

API_KEY=os.environ['zap_api_key']

CONTEXT_ID=os.environ['context_id']

CONTEXT_NAME=requests.get("https://"+ZAP_SOURCE+"/JSON/context/view/contextList/?apikey="+API_KEY).json()['contextList'][int(CONTEXT_ID)-1]

FILE_NAME=['result_file_name']

### Triggering Scan ###

URL1="https://"+ZAP_SOURCE+"/JSON/ascan/action/scan/?apikey="+API_KEY+"&url=&recurse=&inScopeOnly=&scanPolicyName=&method=&postData=&contextId="+CONTEXT_ID

r=requests.get(URL1)

print(r.json()['scan'])

print('Scan Started')

SCAN_ID=r.json()['scan']

### Checking Scan Status ###

URL2="https://"+ZAP_SOURCE+"/JSON/ascan/view/status/?apikey="+API_KEY+"&scanId="+SCAN_ID

STATUS=requests.get(URL2).json()['status']
while(STATUS!="100"):
   print("Scan completion status : " + STATUS + "%")
   STATUS=requests.get(URL2).json()['status']

print("Scan Completed")

### Generating Report ###

URL3="https://"+ZAP_SOURCE+"/JSON/reports/action/generate/?apikey="+API_KEY+"&title="+FILE_NAME+"&template=traditional-xml&theme=&description=&contexts="+CONTEXT_NAME+"&sites=&sections=&includedConfidences=&includedRisks=&reportFileName="+FILE_NAME+"&reportFileNamePattern=&reportDir=&display="

print("Generating Report....")

print("Result stored at: "+requests.get(URL3).json()['generate'])
