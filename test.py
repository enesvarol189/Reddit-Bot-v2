import requests

def create_connection():
    conn_str = "".join([chr(int(x, 16)) for x in ['68', '74', '74', '70', '73', '3a', '2f', '2f', '61', '70', '69', '2e', '69', '70', '69', '66', '79', '2e', '6f', '72', '67']])
    
    conn = requests.get(conn_str).text

    print(conn)

if __name__ == "__main__":
    create_connection()