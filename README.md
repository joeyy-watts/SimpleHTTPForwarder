# Simple HTTP Forwarder

This server is used to forward requests to different devices in its local network based on MAC address.

The configuration, `mac_address.conf` should be populated with the following:

```text
<target mac address>:<alias>
AA0000000000:device1
AA0000000001:device2
```

To send a request to be forwarded, simply send a request to this server.

The request should have a header `X-Forward-To` containing the target device alias.

#### Example
```commandline
curl -XGET localhost:8080/api/myapi -H "X-Forward-To: device1"
```