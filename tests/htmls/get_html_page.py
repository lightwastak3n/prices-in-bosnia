import requests

url = "https://olx.ba/artikal/53070662/zemljiste-rakovica-ilidza-900m2"

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36', 'Referer': 'https://bing.com/'}
response = requests.get(url, headers=headers)
content = response.content

with open("land1.html", "wb") as f:
    f.write(content)