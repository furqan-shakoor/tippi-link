import requests


def get_google():
    res = requests.get("http://www.google.com")
    print res.content


if __name__ == "__main__":
    get_google()