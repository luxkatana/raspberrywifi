#/usr/bin/python3
import requests
import waitress
from main import app 
from time import sleep as wait

connected_with_wifi: bool = False
while not connected_with_wifi  :
    wait(1)
    try:
        requests.get("https://google.com")
    except: ...
    else:
        connected_with_wifi = True
print("waitress.serve")
waitress.serve(app, port=9090, host='0.0.0.0')