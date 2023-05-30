import requests

url = "https://olx.ba/artikal/51934150/audi-a3"

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36', 'Referer': 'https://bing.com/'}
response = requests.get(url, headers=headers)
content = response.content

with open("car2.html", "wb") as f:
    f.write(content)