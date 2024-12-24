import requests

zabbix_api_url = "http://52.66.246.8/zabbix/api_jsonrpc.php"
username = "Admin"
password = "zabbix"

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

    print(f"Response data is: {response_data}")  # Debugging line

    if "result" in response_data:
        return response_data.get("result")  # Return the authentication token
    else:
        raise Exception(f"Failed to authenticate. Error: {response_data.get('error')}")

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

    print(f"Response Data is: {response_data}")  # Debugging line

    if "result" in response_data:
        return response_data.get("result")
    else:
        raise Exception(f"Failed to retrieve hosts. Error: {response_data.get('error')}")

def main():
    try:
        token = authenticate(zabbix_api_url, username, password)
        print(f"Token generated: {token}")  # Debugging line

        hosts = get_hosts(zabbix_api_url, token)

        print("Host Details:")
        for host in hosts:
            print(f"Host ID: {host['hostid']}, Host: {host['host']}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
