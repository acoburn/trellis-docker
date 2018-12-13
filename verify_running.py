import requests
import backoff

@backoff.on_exception(backoff.expo,
        requests.exceptions.RequestException,
        max_time=120)
def get_url(url):
    return requests.get(url)

if __name__ == "__main__":
    get_url("http://localhost/")
    get_url("http://localhost:8080/")
