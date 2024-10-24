# wifi-qr-generator
A REST api to generate wifi QR as png image.

## How to install requirements

```
pip3 install -r requirements.txt
```

## how to start the API

```
python3 ./qr_rest.py
```

## How to access API using curl

```
curl -X POST http://127.0.0.1:5000/generate_qr \                                           
-H "Content-Type: application/json" \
-d '{"ssid": "YourWiFiSSID", "password": "YourWiFiPassword", "description": "Your WiFi Network"}' --output wifi_qr_code.png
```
