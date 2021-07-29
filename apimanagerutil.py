import requests
import sys
import json



def main():
    
    operation_type = sys.argv[1]
    username = sys.argv[2]
    password = sys.argv[3]
    api_name = sys.argv[4]
    group_id = sys.argv[5]
    env = sys.argv[6]
    version_overwrite = sys.argv[7]
    major_version_overwrite = sys.argv[8]


    access_token = autheticate_with_anypoint_platform(username,password)
    
    #exchange_api_version, exchange_api_version_group = fetch_exchange_details(access_token, group_id, api_name)
    exchange_api_version = '1.0.1'
    exchange_api_version_group = 'v1'
    apis = fetch_apimanager_details(access_token, group_id, env, api_name)
    #print(apis)
    updateFlag = True
    apiId = 0
    needToUpdate = True

    if version_overwrite == 'NORMAL':
        if apis != []:
            for item in apis:
                if item['productVersion'] == exchange_api_version_group and item['assetVersion'] > exchange_api_version:
                    #print('Higher version found in API manager, Not updating')
                    updateFlag = False
                    break
                else:
                    apiId = item['id']
        else: 
            #print("New API")
            needToUpdate = False

        if apiId == 0:
            #print('Major version update')
            needToUpdate = False
    
    message = {'api_id': apiId, 'updateVersion': needToUpdate}
    print(message)
    return 0



    


def fetch_apimanager_details(access_token, group_id, env, api_name):

    url_apimanager = "https://anypoint.mulesoft.com/apimanager/api/v1/organizations/" + group_id \
            + "/environments/" + env \
            + "/apis?ascending=false&limit=20&offset=0&sort=createdDate" + "&assetId=" + api_name
    
    headers={"authorization": "Bearer "+ access_token}
    #print(headers)
    response = requests.get(url_apimanager,headers = headers)
    #with open('/Users/mainul.islam/Documents/personal/tools/python/api-details-apimanager.json') as f:
        #data = json.load(f)
    
    if response.status_code != 200:
        #print(response.status_code)
        raise Exception('Error during data fetch from API manager')
    
    data = response.json()

    if data['total'] > 0:
        assets = data['assets']
        return assets[0]['apis']
    else:
        return []

def fetch_exchange_details(access_token, group_id, api_name):
    
    url_exchange = "https://anypoint.mulesoft.com/exchange/api/v2/assets/" + group_id + "/" + api_name
    
    with open('api-details-exchange.json') as f:
        data = json.load(f)

    api_version = data['version']
    api_version_group = data['versionGroup']
    
    return api_version, api_version_group



def autheticate_with_anypoint_platform(user, password):
    #print(user + " " + password)

    url_login = "https://anypoint.mulesoft.com/accounts/login"
    message = {'username':user,'password':password}
    headers={"Accept": "application/json"}

    #response = requests.post(url_login,headers = headers,data = message)
    #access_token = response.json()['access_token']
    #print(access_token)

    return "0dd542aa-5103-4932-85d6-4b2aaa0203a5"


main()