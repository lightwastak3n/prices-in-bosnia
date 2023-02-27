import requests

url = "https://olx.ba/artikal/51868032/kuca-sa-dvoristem-laktasi"

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36', 'Referer': 'https://bing.com/'}
response = requests.get(url, headers=headers)
content = response.content

with open("house1.html", "wb") as f:
    f.write(content)