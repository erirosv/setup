# Miniconda on Linux via SSH and terminal

```conda config --set auto_activate_base false```

## Export
Go into environment. 
```conda env export > <env_name>.yaml```

```conda create --f <env_name>.yaml -n <new_name>```