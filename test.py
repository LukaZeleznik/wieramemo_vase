import requests
req = requests.get('https://zavezanec.zzzs.si/wps/wcm/connect/a40b6286-b84c-432c-ac26-efaeab79d447/Navodila+za+uporabo+M+obrazcev+v+PDF+obliki_i.pdf?MOD=AJPERES&CVID=meHGICR&ContentCache=NONE&CACHE=NONE')

print(req.headers['content-type'])

