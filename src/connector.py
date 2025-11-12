import requests

def push_data_to_database(data, db_url):

    try:
        response = requests.post(db_url, json=data)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None
    
    