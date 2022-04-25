This is primarily to ease running Bluetooth Client Manager Service on an unsupport operating system with systemd.

Create a service file:

```sh
sudo nano /lib/systemd/system/px-user-identity.service
```

With the following content:

```
[Unit]
Description=PantherX User Identity Service
After=multi-user.target

[Service]
Type=idle
ExecStart=px-user-identity-service
WorkingDirectory=/root
User=root

[Install]
WantedBy=multi-user.target
```

Enable and start the service:

```sh
sudo systemctl daemon-reload
sudo systemctl enable px-user-identity.service
sudo systemctl start px-user-identity.service
```

Status:

```sh
sudo systemctl status px-user-identity.service
```
