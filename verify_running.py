import argparse
import backoff
import requests

@backoff.on_exception(backoff.expo,
        requests.exceptions.RequestException,
        max_time=120)
def get_url(url):
    return requests.get(url)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check a webhost")
    parser.add_argument("--baseurl", default="http://localhost/")

    args = parser.parse_args()
    get_url(args.baseurl)
