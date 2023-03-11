# Create ssh alias for remote connections

## Create ssh key
create ssh key:
```ssh-keygen -t rsa```

copy ssh id to server:
```ssh-copy-id user@ip```

## Create alias
open terminal of choise and goto this directory:
```cd ~/.ssh```

If there are no file in the .ssh directory called this will create it:
```nano config```

this text below is for each alias you want
```
Host (alias_name)
HostName (ip_for_server)
User (user_on_remote_server)
```