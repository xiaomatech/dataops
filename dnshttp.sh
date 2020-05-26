#!/usr/bin/env bash

echo -ne '''
[Unit]
Description=A dnshttp for dnsmasq
After=network.target dnsmasq.target

[Service]
Type=simple
ExecStart=/usr/bin/python /opt/dnshttp.py
TimeoutStopSec=180
Restart=yes

[Install]
WantedBy=multi-user.target
''' > /usr/lib/systemd/system/dnshttp.service

systemctl enable dnshttp
systemctl start dnshttp