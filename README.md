JulianaNFC
==========

JulianaNFC is a binding between libnfc and a websocket interface, exposed is an enpoint running at localhost:5000

# API
When connected to this service you will get new NFC tags in json format on the "nfc_read" channel, a UID (tag), a ATQA and a SAK value are supplied all in hexadecimal format.

```
    --> {"args": [{"atqa": "ab:cd", "sak": "ef", "uid": "ab:cd:ef:ab:cd:ef:ab"}], "name": "nfc_read"}
```
