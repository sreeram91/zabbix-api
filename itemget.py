import requests

zabbix_api_url = "http://65.2.153.81/zabbix/api_jsonrpc.php"
username = "Admin"
password = "zabbix"

# Authentication function
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
    
# Function to get hosts
def get_hosts(url, token):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json-rpc"
    }
    payload = {
        "jsonrpc": "2.0",
        "method": "host.get",
        "params": {
            "output": ["hostid", "host"],
            "selectInterfaces": ["interfaceid", "ip"]
        },
        "id": 2
    }

    response = requests.post(url, json=payload, headers=headers)
    response_data = response.json()

    if "result" in response_data:
        return response_data.get("result")
    else:
        raise Exception(f"Failed to retrieve hosts. Error: {response_data.get('error')}")

# Function to get items for a specific host by hostid
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
                "key_": "system.cpu"
            },
            "sortfield": "name"
        },
        "id": 1
    }
    response = requests.post(url, json=payload, headers=headers)
    response_data = response.json()
    
    if 'result' in response_data:
        return response_data.get('result')
    else:
        raise Exception(f"Failed to retrieve items for host {hostid}: {response_data.get('error')}")

# Main function to execute everything
def main():
    try:
        # Step 1: Authenticate and get the token
        token = authenticate(zabbix_api_url, username, password)
        print(f'Token Generated: {token}')

        # Step 2: Get all hosts
        hosts = get_hosts(zabbix_api_url, token)

        # Step 3: Loop through each host and fetch its items
        for host in hosts:
            hostid = host['hostid']
            host_name = host['host']
            print(f"\nFetching data for host: {host_name} (hostid: {hostid})")

            # Fetch items for the current host
            items = get_items(zabbix_api_url, token, hostid)

            # Step 4: Print the items
            for item in items:
                print(f"Host ID: {hostid}, Host: {host_name}, Item ID: {item['itemid']}, Type: {item['type']}")

    except Exception as e:
        print(f'Error: {e}')

# Execute the main function
if __name__ == '__main__':
    main()
