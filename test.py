import requests
req = requests.get("https://i.stack.imgur.com/1dpmw.gif")

print(req.content)
