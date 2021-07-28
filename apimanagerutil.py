import requests
import sys
import json



def main():
    
    if sys.argv[1] == 'QT':
        
        #message = {'api_id': apiid}
        #print(message)    
        if sys.argv[7]:
            apiid = 123456
        else
            apiid = 786475
        print(apiid)    
        return 0

    operation_type = sys.argv[1]
    username = sys.argv[2]
    password = sys.argv[3]
    api_name = sys.argv[4]
    group_id = sys.argv[5]
    env = sys.argv[6]

    access_token = autheticate_with_anypoint_platform(username,password)
    
    exchange_api_version, exchange_api_version_group = fetch_exchange_details(access_token, group_id, api_name)

    fetch_apimanager_details(access_token, group_id, env, api_name)

    


def fetch_apimanager_details(access_token, group_id, env, api_name):

    url_apimanager = "https://anypoint.mulesoft.com/apimanager/api/v1/organizations/" + group_id \
            + "/environments/" + env \
            + "/apis?ascending=false&limit=20&offset=0&sort=createdDate" + "&assetId=" + api_name
    

    with open('/Users/mainul.islam/Documents/personal/tools/python/api-details-apimanager.json') as f:
        data = json.load(f)
    
    if data['total'] > 0:
        assets = data['assets']
        print(assets[0]['id'])
        return assets[0]['id']

def fetch_exchange_details(access_token, group_id, api_name):

    
    url_exchange = "https://anypoint.mulesoft.com/exchange/api/v2/assets/" + group_id + "/" + api_name
    
    with open('api-details-exchange.json') as f:
        data = json.load(f)

    api_version = data['version']
    api_version_group = data['versionGroup']
    
    return api_version, api_version_group



def autheticate_with_anypoint_platform(user, password):
    print(user + " " + password)

    url_login = "https://anypoint.mulesoft.com/accounts/login"
    message = {'username':user,'password':password}
    headers={"Accept": "application/json"}

    #response = requests.post(url_login,headers = headers,data = message)
    #access_token = response.json()['access_token']
    #print(access_token)

    return "4b168ed1-ca22-4d02-812f-6661ccfef714"


main()