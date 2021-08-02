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
    
    file_flag = sys.argv[8]

    file_api_version = ''
    
    
    

    if operation_type == 'GETID': # Getting API from api manager
        access_token = autheticate_with_anypoint_platform(username,password)
        version_overwrite = sys.argv[7]

        new_api_version = ''
        exchange_api_version, exchange_api_version_group = fetch_exchange_details(access_token, group_id, api_name)

        ##### Compare file version with exchange version (if application)
        if file_flag:
            with open(sys.argv[9]) as f:
                file_data = json.load(f)

            file_api_version = file_data['apiSpecVersion']
            if file_api_version > exchange_api_version:
                ##### Compare file version with exchange version (if application)
                raise Exception('Working version cannot be greater that Exchange version')
            else:
                new_api_version = file_api_version
        
        else:
            new_api_version = exchange_api_version

        apis = fetch_apimanager_details(access_token, group_id, env, api_name,exchange_api_version_group)
        apiId = 0
        needToUpdate = True

        if version_overwrite == 'NORMAL':
            if apis != []:
                apiId = apis[0]['id']
                if apis[0]['assetVersion'] == new_api_version or apis[0]['assetVersion'] > new_api_version:
                    ##### Working API and API manager have same resource version, no need to update
                    ##### OR Working API version is lower than API manager version, no need to update
                    needToUpdate = False
            else: 
                ##### Major version update
                apiId = add_api_manager(access_token, group_id, env, api_name, new_api_version)
                needToUpdate = False

            
        
        elif version_overwrite == 'ALWAYS':
            # Creating new API instance if exchange version is different from API manager
            apiFoundFlag = False
            if apis != []:
                for item in apis:
                    if item['assetVersion'] == new_api_version:
                        ##### Exchange and API manager have same resource version, no need to update
                        apiId = item['id']
                        apiFoundFlag = True
                        break
            elif apis == [] or apiFoundFlag != True:
                apiId = add_api_manager(access_token, group_id, env, api_name, new_api_version)
            
            needToUpdate = False

        message = {'api_id': apiId, 'updateVersion': needToUpdate, 'exchageVersion':new_api_version, 'access_token': access_token}
    
    elif operation_type == 'UPDATEVERSION':
        apiId = sys.argv[7]
        newVersion = sys.argv[8]
        access_token = sys.argv[9]
        message = update_api_manager_version(access_token, group_id, env, apiId, newVersion)

    print(message)
    return 0


def add_api_manager(access_token, group_id, env, api_name, api_version):
    url_insert_apimanager = "https://anypoint.mulesoft.com/apimanager/api/v1/organizations/" + group_id \
            + "/environments/" + env + "/apis"
    headers={"authorization": "Bearer "+ access_token, 'Content-Type': 'application/json'}

    message = {"endpoint": {"deploymentType": "CH", "isCloudHub": None,"muleVersion4OrAbove": True,"proxyUri": None,"referencesUserDomain": None,"responseTimeout": None,"type": "raml","uri": None}, "providerId": None,"instanceLabel": None,"spec": {"assetId": api_name,"groupId": group_id,"version": api_version}}
    response = requests.post(url_insert_apimanager,headers = headers,data = json.dumps(message))


    if response.status_code > 399:
        raise Exception("Could not create API instance in API manager")

    data = response.json()
    return data['id']


def update_api_manager_version(access_token, group_id, env, api_id, new_version):    
    
    url_update_apimanager = "https://anypoint.mulesoft.com/apimanager/api/v1/organizations/" + group_id \
            + "/environments/" + env + "/apis/" + api_id
    headers={"authorization": "Bearer "+ access_token, 'Content-Type': 'application/json'}
    message = {"assetVersion": new_version}
    response = requests.patch(url_update_apimanager,headers = headers,data = json.dumps(message))

    if response.status_code != 200:
        #return 'ERROR Updating API manager'
        raise Exception('ERROR Updating API manager')
    else:
        return 'API manager Update SUCCESS'





def fetch_apimanager_details(access_token, group_id, env, api_name, major_version):

    url_apimanager = "https://anypoint.mulesoft.com/apimanager/api/v1/organizations/" + group_id \
            + "/environments/" + env \
            + "/apis?ascending=false&limit=20&offset=0&sort=createdDate" + "&assetId=" + api_name + "&productVersion=" + major_version
    
    headers={"authorization": "Bearer "+ access_token}
    #print(headers)
    response = requests.get(url_apimanager,headers = headers)
    
    
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
    headers={"authorization": "Bearer "+ access_token}
    response = requests.get(url_exchange,headers = headers)
    
    if response.status_code == 404:
        #print(response.status_code)
        raise Exception('Resource was not found in exchange')
    
    elif response.status_code != 200:
        #print(response.status_code)
        raise Exception('Error during data fetch from Exchange')

    data = response.json()
    api_version = data['version']
    api_version_group = data['versionGroup']
    
    return api_version, api_version_group



def autheticate_with_anypoint_platform(user, password):
    #print(user + " " + password)

    url_login = "https://anypoint.mulesoft.com/accounts/login"
    message = {'username':user,'password':password}
    headers = {"Accept": "application/json", "Content-Type": "application/json"}

    response = requests.post(url_login,headers = headers,data = json.dumps(message))
    print(response.status_code)

    if response.status_code > 399:
        #print(response.status_code)
        raise Exception('Error during Access token fetch')

    access_token = response.json()['access_token']
    #print(access_token)

    return access_token


main()