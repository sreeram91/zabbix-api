import streamlit as st
import requests
import pandas as pd

#zabbix api url and credentials
zabbix_api_url = "http://65.2.153.81/zabbix/api_jsonrpc.php"
username = "Admin"
password = "zabbix"

#function to authenticate and retrive the token
def authenticate(url, user, password):
    payload = {
        "jsonrpc": "2.0",
        "method": "user.login",
        "params": {
            "username": user,
            "password": password
        },
        "id": 1
    }
    response = requests.post(url, json=payload)
    response_data = response.json()

    if "result" in response_data:
        return response_data.get("result")  # Return the authentication token
    else:
        raise Exception(f"Failed to authenticate. Error: {response_data.get('error')}")
    
#function to fetch hosts from zabbix
def get_hosts(url, token):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json-rpc"
    }
    payload = {
        "jsonrpc": "2.0",
        "method": "host.get",
        "params": {
            "output": [
                "hostid",
                "host"
            ],
            "selectInterfaces": ["interfaceid", "ip"]
        },
        "id": 2
    }

    response = requests.post(url, json=payload, headers=headers)
    response_data = response.json()

    #rint(f"Response Data is: {response_data}")  # Debugging line

    if "result" in response_data:
        return response_data.get("result")
    else:
        raise Exception(f"Failed to retrieve hosts. Error: {response_data.get('error')}")

#fucntion to fetch items for the hosts
def get_items(url, token, hostid):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json-rpc"
    }
    
    payload = {
        "jsonrpc": "2.0",
        "method": "item.get",
        "params": {
            "output": "extend",
            "hostids": hostid,
            "with_triggers": True,
            "search": {
                "key_": "system.cpu.util"
            },
            "sortfield": "name"
        },
        "id": 1
    }
    response = requests.post(url, json=payload, headers=headers)
    response_data = response.json()

   #print(f'Response data is: {response_data}') #Debugging line
    
    if 'result' in response_data:
        return response_data.get('result')
    else:
        raise Exception(f"Failed to retrieve items: {response_data.get('error')}")

#main app function
def main():
    try:
        #authenticate and get the token
        token = authenticate(zabbix_api_url, username, password)
        
        #get hosts
        hosts = get_hosts(zabbix_api_url, token)

        #create a list to store data for display
        all_data = []

        #loop through each host to get its items
        for host in hosts:
            hostid = host['hostid']
            hostname = host['host']

            items = get_items(zabbix_api_url, token, hostid)

            #append the host-item data to the all_data list
            for item in items:
                itemid = item['itemid']
                type = item['type']
                all_data.append([hostid, hostname, itemid, type])

        #create a dataframe from the data
        df = pd.DataFrame(all_data, columns=["Host ID", "Host", "Item ID", "Type"])


        st.write("Host and Item Details:")
        st.dataframe(df)
    
    except Exception as e:
        st.error(f"Error: {e}")
 
if __name__ == '__main__':
    main()
