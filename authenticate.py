import pandas as pd
import requests

zabbix_api_url = "http://52.66.246.8/zabbix/api_jsonrpc.php"
username = "Admin"
password = "zabbix"

def authenticate(url, user, password):
    """Authenticate with the Zabbix API and return the authentication token."""
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
    
    # Check for success or error in response
    if "result" in response_data:
        return response_data.get("result")  # Return the authentication token
    else:
        raise Exception(f"Failed to authenticate. Error: {response_data.get('error')}")

def main():
    token = authenticate(zabbix_api_url, username, password)
    print(f"Authentication token: {token}")

if __name__ == "__main__":
    main()
