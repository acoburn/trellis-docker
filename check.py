import requests

if __name__ == "__main__":
    print("Starting")
    r = requests.get("http://localhost/")
    print(r.status_code)
    print(r.headers['content-type'])
