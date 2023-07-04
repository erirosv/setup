# Disable SSH password for connection

## Create file
Create file ```authorized_keys``` if it is **NOT** existing in ```~/.ssh```. On the client add public key in the file.

## Editing the config
```sudo vi /etc/shh/sshd_config```

Locate the ```PasswordAuthentication``` change to ```no```. Disable comment if needed. Do also change ```PubkeyAuthentication``` to  ```yes```. Disable comment if needed.

Save the file...

Run the following to restart SSH:

```sudo systemctl restart ssh``` 

```sudo systemctl restart ssh.service```

```sudo systemctl restart sshd.service```

## Extra
In some cases linux can give the problem with the login. 
- ```cd /etc/ssh/sshd_config.d````
- ```ls -l````
- remove the file and run the restart commands above and it should work...
