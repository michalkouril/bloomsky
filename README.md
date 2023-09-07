# BloomSky Weather Camera Utilities


## SKY1 WiFi network setup

SKY1 uses cooee (listening to WiFi 2.4GHz multicast packets) for WiFi SSID/Password configuration. The packets are encrypted. See the utility in the cooee folder.

Setup:
1. Turn on SKY1 (left button)
2. When the device is running for a moment hold wifi button for 10s and release (WARNING -- this will wipe the existing WiFi SSID/Password)
3. Run the utility

Note: it may take a while (minutes) -- try restarting the device if not working.

```bash
$ python3 cooee_send.py --ssid MyWiFiNetwork --password S3cured
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
