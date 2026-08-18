# Razer Orochi V2 battery on Linux

This guide covers installing **OpenRazer + Polychromatic** on **Ubuntu** and **Arch Linux / CachyOS**.

OpenRazer is an open-source Linux driver/daemon for Razer peripherals. Polychromatic is a graphical frontend for OpenRazer. Polychromatic itself requires OpenRazer to communicate with the mouse.

> **Important:** There are multiple Orochi V2 revisions. The original Orochi V2 (RZ01-0373) is supported by OpenRazer, while the newer **Orochi V2 (2026), model RZ01-0569 / USB ID 1532:00e0**, currently has an open OpenRazer support request. If your mouse is the 2026 model, these instructions may install correctly but the mouse may not be detected yet.

Official references:
- OpenRazer: https://openrazer.github.io/
- OpenRazer GitHub: https://github.com/openrazer/openrazer
- Polychromatic: https://polychromatic.app/
- Polychromatic GitHub: https://github.com/polychromatic/polychromatic

---

## 1. Check which Orochi V2 you have

Before installing anything, connect the mouse/dongle and run:

```bash
lsusb | grep 1532
```

For the original Orochi V2, you may see a USB ID associated with the supported model.

You can also identify the exact product/model number from the label on the mouse or its packaging.

If you see:

```text
1532:00e0
```

you have the **2026 Orochi V2 (RZ01-0569)**. OpenRazer currently has an open device-support issue for this revision.

---

# Ubuntu

## 2. Install OpenRazer

OpenRazer recommends its stable PPA for Ubuntu when you want the latest released driver/device support.

```bash
sudo add-apt-repository ppa:openrazer/stable
sudo apt update
sudo apt install openrazer-meta
```

Add your user to the `plugdev` group:

```bash
sudo gpasswd -a $USER plugdev
```

Then install Polychromatic:

```bash
sudo add-apt-repository ppa:polychromatic/stable
sudo apt update
sudo apt install polychromatic
```

Reboot:

```bash
sudo reboot
```

After reboot, start **Polychromatic** from your application menu.

### Ubuntu: development version

If your Orochi revision is newer than the current stable OpenRazer release, you can try the development PPA:

```bash
sudo add-apt-repository ppa:openrazer/daily
sudo apt update
sudo apt install openrazer-meta
```

For Polychromatic's development version:

```bash
sudo add-apt-repository ppa:polychromatic/preview
sudo apt update
sudo apt install polychromatic
```

Only use the development versions if you need newer device support.

---

# Arch Linux / CachyOS

CachyOS is Arch-based, so the Arch instructions are the relevant ones.

## 3. Install OpenRazer

First install the required kernel headers.

For the standard CachyOS kernel, check your installed kernels:

```bash
uname -r
```

Then inspect installed kernel packages:

```bash
pacman -Q | grep -E 'linux.*headers'
```

If you use the standard Arch `linux` kernel:

```bash
sudo pacman -S linux-headers
```

OpenRazer is available in the Arch repositories:

```bash
sudo pacman -S openrazer-daemon
```

Add your user to the OpenRazer group:

```bash
sudo gpasswd -a $USER openrazer
```

Reboot:

```bash
sudo reboot
```

## 4. Install Polychromatic

If you have `yay`:

```bash
yay -S polychromatic
```

Then start it:

```bash
polychromatic
```

You can also start it from the desktop application menu.

### Manual AUR installation

If you don't use an AUR helper:

```bash
git clone https://aur.archlinux.org/polychromatic.git
cd polychromatic
makepkg -si
```

---

# 5. Check that OpenRazer is working

After reboot, check that the daemon is running:

```bash
systemctl --user status openrazer-daemon
```

You can also check whether the mouse is visible over USB:

```bash
lsusb | grep 1532
```

And check OpenRazer's device information:

```bash
python3 -m openrazer.client
```

If the device is supported, Polychromatic should normally be able to communicate with it.

---

# 6. Check the battery level

Open Polychromatic and select the Orochi V2.

Depending on the exact Orochi V2 revision and connection mode, the battery information should be available through OpenRazer.

The Orochi V2 can use:
- 2.4 GHz HyperSpeed USB receiver
- Bluetooth

For troubleshooting, test the receiver first because it makes USB device detection easier.

---

# 7. If the mouse is not detected

Run:

```bash
lsusb | grep 1532
```

If nothing appears, check that the USB receiver is connected.

If a Razer device appears but OpenRazer does not recognize it, compare its VID/PID against the OpenRazer supported-device list.

OpenRazer's troubleshooting guide recommends checking the USB PID this way.

You can also check:

```bash
sudo dmesg | grep -i razer
```

and:

```bash
journalctl --user -u openrazer-daemon
```

---

# 8. Secure Boot

OpenRazer uses a DKMS kernel driver. Because the kernel module is not necessarily signed with a key trusted by your system, **Secure Boot can prevent the driver from loading**.

If OpenRazer installs successfully but the device does not work, check:

```bash
mokutil --sb-state
```

If Secure Boot is enabled, you may need to configure module signing/MOK or disable Secure Boot.

---

# 9. If your device was added recently

OpenRazer sometimes adds support in development builds before the next stable release.

The OpenRazer troubleshooting guide recommends:

### Ubuntu

Use:

```bash
sudo add-apt-repository ppa:openrazer/daily
sudo apt update
sudo apt install openrazer-meta
```

### Arch / CachyOS

Use the development AUR packages instead of the stable packages:

```bash
yay -S openrazer-daemon-git openrazer-driver-dkms-git python-openrazer-git
```

Then reboot.

Do this only if the stable version does not support your specific device.

---

# 10. Troubleshooting commands

These are useful when asking for help:

```bash
lsusb | grep 1532
```

```bash
uname -r
```

```bash
pacman -Q | grep -E 'openrazer|polychromatic'
```

```bash
systemctl --user status openrazer-daemon
```

```bash
journalctl --user -u openrazer-daemon
```

```bash
sudo dmesg | grep -i razer
```

For Ubuntu:

```bash
apt list --installed 2>/dev/null | grep -E 'openrazer|polychromatic'
```

---

# Recommended setup for CachyOS

For a normal supported Orochi V2, I would use:

```bash
sudo pacman -S linux-headers openrazer-daemon
sudo gpasswd -a $USER openrazer
yay -S polychromatic
sudo reboot
```

Then launch:

```bash
polychromatic
```

This gives you a completely Linux-native setup without Razer Synapse.

## Sources

OpenRazer installation:
https://openrazer.github.io/

OpenRazer GitHub:
https://github.com/openrazer/openrazer

OpenRazer troubleshooting:
https://github.com/openrazer/openrazer/wiki/Troubleshooting

Polychromatic Arch installation:
https://polychromatic.app/download/arch/

Polychromatic documentation:
https://docs.polychromatic.app/

Orochi V2 2026 support issue:
https://github.com/openrazer/openrazer/issues/2856
