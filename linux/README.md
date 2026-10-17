linux files

## Adding SSH to cahchyOS 

Check the ip-address

```bash
ip -4 -br addr
```

```bash
ip route
```

Take the ip and copy it and paste it into ths command below

Add the follow the ssh add the rule in the firewall

```bash
sudo ufw allow from 10.10.10.0/24 to any port 22 proto tcp
```

> Change the IP to the correct one
