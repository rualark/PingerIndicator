# PingerIndicator

Ubuntu indicator applet for monitoring connection to host (Gtk-based).

# Features

- Pings host two times per second (configurable) no matter how long it takes host to reply (does not flood if host replies fast and does not hang if host does not reply for a long time). As a result, PingerIndicator stays responsive even in slow networks.
- Color of indicator changes based on current ping round trip time. Black dot flashes every time ping is received.
- Dot color changes to white during first minute (configurable) after disconnection was detected.
- Detects disconnection after 3 ping timeouts (configurable) and take action (e.g. reconnect VPN)
- Customizable ping timeout and delay
- Writes log of connection and disconnection events and can open it from applet menu

<img src=https://i.imgur.com/8CyK7XH.png align=top width=30> Last ping round trip time was below 100 ms (configurable)

<img src=https://i.imgur.com/wvyKZQi.png align=top width=30> Last ping round trip time was below 200 ms (configurable)

<img src=https://i.imgur.com/TO4BdU3.png align=top width=30> Last ping round trip time was below 350 ms (configurable)

<img src=https://i.imgur.com/dSU0463.png align=top width=30> Last ping round trip time was below 500 ms (configurable)

<img src=https://i.imgur.com/sWazN2B.png align=top width=30> Last ping round trip time was above 500 ms or timed out (configurable)

# Operating system support

Ubuntu.

# Installation on Ubuntu

1. Download
2. Edit config.py
3. Edit disconnect_action monitor.py
4. Add to autostart or run
