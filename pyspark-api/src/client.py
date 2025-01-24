import requests
import json


def get_stream(url):
    s = requests.Session()

    with s.get(url, headers=None, stream=True) as resp:
        for line in resp.iter_lines():
            if line:
                print(json.loads(line))


url = "http://localhost:4444/preview"
get_stream(url)
