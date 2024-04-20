import requests


def send_ntfy(msg: str, title: str, tags: list):
    all_tags = ",".join(tags)
    headers = {"Title": f"{title}", "Tags": f"{all_tags}"}
    url = "https://ntfy.sh/VSNyDS35BgEi"
    requests.post(url=url, data=msg, headers=headers)
