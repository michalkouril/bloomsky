# BloomSky Weather Camera Utilities


## SKY1 WiFi network setup

SKY1 uses cooee (listening to WiFi 2.4GHz multicast packets) for WiFi SSID/Password configuration. The packets are encrypted. See the utility in the cooee folder.

```bash
python3 cooee_send.py --ssid MyWiFiNetwork --password S3cured
retrying... elapsed 3s
retrying... elapsed 5s
retrying... elapsed 8s
retrying... elapsed 10s
Received discovery response from 10.100.1.89 device ID 94A1A2712345 (SKY1)
Sending restart command... 
```

## SKY2 WiFi network setup

SKY2 uses bluetooth to configure WiFi SSID/Password. See the browser based bluetooth setup (Chrome) in bluetooth folder.

## FAQ

1. SKY1 vs. SKY2

* SKY1 has two sensor windows next two the camera. SKY2 does not.
* SKY2 has bluetooth for WiFi setup. SKY1 does not.
