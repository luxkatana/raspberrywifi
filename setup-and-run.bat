python -m pip install -r requirements.txt
python -m pip install waitress
waitress-serve --listen=0.0.0.0:9090 main:app