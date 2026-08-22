# Sunshine and Moonlight on Arch Linux and Ubuntu

A practical installation guide for using **Sunshine** as the streaming host and **Moonlight** as the streaming client on Linux.

## 1. What goes where?

- **Sunshine**: install on the computer that runs the games/applications and has the GPU doing the rendering/encoding.
- **Moonlight**: install on the computer/device where you want to receive the stream.
- You can install both on the same machine if you want that machine to act as both a host and a client.

Typical LAN setup:

```text
Gaming PC / Host
    |
    | Sunshine
    |
    +---- LAN ----> Moonlight
                      |
                  Laptop / PC / TV
```

For multiple gaming PCs, install Sunshine on each host. A single Moonlight client can then connect to the different hosts.

---

# 2. Official websites

## Sunshine

- Official website/documentation: https://docs.lizardbyte.dev/projects/sunshine/latest/
- Official GitHub: https://github.com/LizardByte/Sunshine
- Latest releases: https://github.com/LizardByte/Sunshine/releases

## Moonlight

- Official website: https://moonlight-stream.org/
- Official GitHub: https://github.com/moonlight-stream
- Moonlight PC client: https://github.com/moonlight-stream/moonlight-qt

---

# 3. Arch Linux / CachyOS

The following instructions also apply to Arch-based distributions such as CachyOS.

## 3.1 Install Sunshine

LizardByte provides an official pacman repository. The current Sunshine documentation recommends using the prebuilt package from this repository.

After configuring the LizardByte pacman repository according to the official documentation, install Sunshine with:

```bash
sudo pacman -S sunshine
```

Official instructions:

https://docs.lizardbyte.dev/projects/sunshine/latest/md_docs_2getting__started.html

### Alternative: build the package locally

You can download the PKGBUILD archive:

```bash
wget https://github.com/LizardByte/Sunshine/releases/latest/download/sunshine.pkg.tar.gz
tar -xvf sunshine.pkg.tar.gz
cd sunshine
```

For AMD GPU encoding support:

```bash
sudo pacman -S libva-mesa-driver
```

For NVIDIA GPU encoding support:

```bash
sudo pacman -S cuda
```

Then build/install:

```bash
makepkg -si
```

> Note: Sunshine's documentation states that AUR packages are third-party packages and are used at your own risk. Prefer the official LizardByte package repository when practical.

## 3.2 Start Sunshine

Start Sunshine for the current user:

```bash
systemctl --user start app-dev.lizardbyte.app.Sunshine
```

Enable it so that it starts automatically:

```bash
systemctl --user --now enable app-dev.lizardbyte.app.Sunshine
```

Check its status:

```bash
systemctl --user status app-dev.lizardbyte.app.Sunshine
```

Sunshine also provides `sunshine.service` as an alias.

## 3.3 Open the Sunshine Web UI

After starting Sunshine, open:

https://localhost:47990

Create the Sunshine username/password when prompted.

---

# 4. Install Moonlight on Arch Linux / CachyOS

Install the Qt desktop client:

```bash
sudo pacman -S moonlight-qt
```

Start it from your application menu or run:

```bash
moonlight
```

Moonlight should normally discover Sunshine hosts automatically when both devices are on the same LAN.

If the host does not appear automatically, use Moonlight's option to manually add the host's IP address.

---

# 5. Ubuntu

## 5.1 Install Sunshine

Sunshine provides distro-specific `.deb` packages.

For Ubuntu 24.04 on x86_64/amd64, download the current Ubuntu 24.04 package from the official Sunshine releases page:

https://github.com/LizardByte/Sunshine/releases/latest

The package name follows this general format:

```text
sunshine-ubuntu-24.04-amd64.deb
```

After downloading it:

```bash
cd ~/Downloads
sudo apt install ./sunshine-ubuntu-24.04-amd64.deb
```

If you have downloaded it to another directory, change the path accordingly.

If you encounter dependency problems:

```bash
sudo apt --fix-broken install
```

Then run the installation command again.

### Important

Use the package matching your Ubuntu version and CPU architecture.

For example:

```text
Ubuntu 24.04 x86_64 -> sunshine-ubuntu-24.04-amd64.deb
```

Official documentation:

https://docs.lizardbyte.dev/projects/sunshine/latest/md_docs_2getting__started.html

## 5.2 Start Sunshine

Start Sunshine:

```bash
systemctl --user start app-dev.lizardbyte.app.Sunshine
```

Enable it at login:

```bash
systemctl --user --now enable app-dev.lizardbyte.app.Sunshine
```

Check the service:

```bash
systemctl --user status app-dev.lizardbyte.app.Sunshine
```

Then open:

https://localhost:47990

---

# 6. Install Moonlight on Ubuntu

Flatpak is a convenient way to install the Moonlight Qt client.

Install Flatpak:

```bash
sudo apt update
sudo apt install flatpak
```

Add Flathub:

```bash
sudo flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
```

Install Moonlight:

```bash
flatpak install flathub com.moonlight_stream.Moonlight
```

Run it:

```bash
flatpak run com.moonlight_stream.Moonlight
```

You can also launch Moonlight from the Ubuntu application menu after installation.

---

# 7. Pair Moonlight with Sunshine

Make sure the two machines are connected to the same LAN.

1. Start Sunshine on the host.
2. Start Moonlight on the client.
3. Moonlight should display the Sunshine host.
4. Select the host.
5. Moonlight will show a PIN.
6. Open the Sunshine web interface:

```text
https://<HOST-IP>:47990
```

7. Enter the PIN in Sunshine.
8. The devices are now paired.
9. Select the host in Moonlight and launch an application/game.

To find the host's IP address on Linux:

```bash
ip addr
```

A simpler command is:

```bash
hostname -I
```

Example:

```text
192.168.1.50
```

Then the Sunshine Web UI would be:

```text
https://192.168.1.50:47990
```

---

# 8. Recommended LAN setup

For the best streaming experience:

```text
                 Router / Switch
                       |
              Ethernet connection
                       |
                 Gaming PC
                 Sunshine
                       |
                 LAN / Wi-Fi
                       |
                  Laptop
                 Moonlight
```

Ideally, connect the Sunshine host using Ethernet.

The Moonlight client can use Wi-Fi, but Ethernet is preferable if available.

For high-quality 1440p/4K streaming, a wired gigabit connection is strongly recommended.

---

# 9. Multiple Sunshine hosts

You can run Sunshine on several machines:

```text
                     LAN
                      |
       +--------------+--------------+
       |              |              |
       v              v              v
   Gaming PC       Server PC       Other PC
   Sunshine       Sunshine        Sunshine
       |              |              |
       +--------------+--------------+
                      |
                      v
                  Moonlight
                   Client
```

For example:

- Windows gaming PC -> Sunshine
- Arch/CachyOS gaming PC -> Sunshine
- Ubuntu gaming PC -> Sunshine
- Laptop -> Moonlight
- Another desktop -> Moonlight

Moonlight can be used to select which Sunshine host you want to connect to.

---

# 10. GPU considerations

Sunshine uses the GPU's hardware video encoding capabilities.

### AMD

On Arch Linux, the official Sunshine documentation lists:

```bash
sudo pacman -S libva-mesa-driver
```

as an optional dependency for AMD GPU encoding.

### NVIDIA

The official Sunshine documentation lists:

```bash
sudo pacman -S cuda
```

for NVIDIA GPU encoding support.

### Intel

Intel GPUs use Intel's hardware video encoding stack. Make sure the appropriate Intel graphics/media drivers are installed for your distribution.

---

# 11. Useful Sunshine commands

Start:

```bash
systemctl --user start app-dev.lizardbyte.app.Sunshine
```

Enable at login:

```bash
systemctl --user --now enable app-dev.lizardbyte.app.Sunshine
```

Stop:

```bash
systemctl --user stop app-dev.lizardbyte.app.Sunshine
```

Restart:

```bash
systemctl --user restart app-dev.lizardbyte.app.Sunshine
```

Check status:

```bash
systemctl --user status app-dev.lizardbyte.app.Sunshine
```

---

# 12. Uninstall

## Arch Linux / CachyOS

```bash
sudo pacman -R sunshine
```

Moonlight:

```bash
sudo pacman -R moonlight-qt
```

## Ubuntu

Sunshine:

```bash
sudo apt remove sunshine
```

Moonlight installed with Flatpak:

```bash
flatpak uninstall com.moonlight_stream.Moonlight
```

---

# 13. Quick installation summary

## Arch Linux / CachyOS

### Sunshine

```bash
sudo pacman -S sunshine
sudo pacman -S libva-mesa-driver
systemctl --user --now enable app-dev.lizardbyte.app.Sunshine
```

### Moonlight

```bash
sudo pacman -S moonlight-qt
```

---

## Ubuntu 24.04

### Sunshine

Download the appropriate `.deb` from:

https://github.com/LizardByte/Sunshine/releases/latest

Then:

```bash
cd ~/Downloads
sudo apt install ./sunshine-ubuntu-24.04-amd64.deb
systemctl --user --now enable app-dev.lizardbyte.app.Sunshine
```

### Moonlight

```bash
sudo apt update
sudo apt install flatpak
sudo flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
flatpak install flathub com.moonlight_stream.Moonlight
```

---

# 14. Official documentation

Sunshine documentation:

https://docs.lizardbyte.dev/projects/sunshine/latest/

Sunshine GitHub:

https://github.com/LizardByte/Sunshine

Sunshine releases:

https://github.com/LizardByte/Sunshine/releases

Moonlight website:

https://moonlight-stream.org/

Moonlight GitHub:

https://github.com/moonlight-stream

Moonlight Qt:

https://github.com/moonlight-stream/moonlight-qt
