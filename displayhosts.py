import streamlit as st
import requests
import pandas as pd

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

    if "result" in response_data:
        return response_data.get("result")
    else:
        raise Exception(f"Failed to retrieve hosts. Error: {response_data.get('error')}")

def main():
    try:
        token = authenticate(zabbix_api_url, username, password)
        hosts = get_hosts(zabbix_api_url, token)

        # Convert host details to a DataFrame
        host_data = [{"Host ID": host['hostid'], "Host": host['host']} for host in hosts]
        df = pd.DataFrame(host_data)

        # Display the DataFrame in Streamlit
        st.write("Host Details:")
        st.dataframe(df)

        # Provide a download button for the CSV
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name="host_details.csv",
            mime="text/csv"
        )
    except Exception as e:
        st.error(f"Error: {e}")

if __name__ == "__main__":
    main()
