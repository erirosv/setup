# Disable password for SUDO

```sudo visudo```

Change: ```%sudo ALL=(ALL:ALL) ALL``` TO ```%sudo ALL=(ALL:ALL) NOPASSWD:ALL```