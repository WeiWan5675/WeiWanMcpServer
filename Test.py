import requests


response = requests.get("https://r.jina.ai/https://www.cnblogs.com/wang_yb/p/18635441")
print(response.text)