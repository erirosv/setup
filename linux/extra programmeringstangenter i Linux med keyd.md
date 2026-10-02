# HHKB – extra programmeringstangenter i Linux med keyd

Config:

```ini
[ids]
*
[main]
leftalt = layer(programming)

[programming:A]
comma = 102nd
dot = S-102nd
slash = G-102nd
7 = G-7
8 = G-8
9 = G-9
0 = G-0
```

---

Den här guiden visar hur du använder **keyd** för att lägga till tangenter som saknas eller är svåra att skriva på ett HHKB i Linux.

Fokus ligger framför allt på programmeringstecken:

| Kombination | Resultat |   |
| ----------- | -------- | - |
| `Alt + ,`   | `<`      |   |
| `Alt + .`   | `>`      |   |
| `Alt + -`   | `        | ` |

---

## 1. Installera keyd

På Arch Linux / CachyOS:

```bash
sudo pacman -S keyd
```

Kontrollera installationen:

```bash
keyd --version
```

---

## 2. Skapa keyd-konfigurationen

Skapa konfigurationsfilen:

```bash
sudo nano /etc/keyd/default.conf
```

Config:

```ini
[ids]
*
[main]
leftalt = layer(programming)

[programming:A]
comma = 102nd
dot = S-102nd
slash = G-102nd
7 = G-7
8 = G-8
9 = G-9
0 = G-0
```

---

## 3. Starta keyd

Aktivera tjänsten så att keyd startar automatiskt:

```bash
sudo systemctl enable --now keyd
```

Kontrollera status:

```bash
systemctl status keyd
```

Du bör se något liknande:

```text
Active: active (running)
```

---

## 4. Ladda om konfigurationen

När du ändrar `/etc/keyd/default.conf` kan du ladda om konfigurationen:

```bash
sudo keyd reload
```

Om `reload` inte fungerar kan du starta om tjänsten:

```bash
sudo systemctl restart keyd
```

---

## 5. Testa tangentbordet

Starta keyd:s tangentbordsmonitor:

```bash
sudo keyd monitor
```

Tryck sedan på exempelvis:

```text
Alt + ,
```

Monitoreringen visar vilka tangentkoder Linux tar emot.

Avsluta med:

```text
Ctrl + C
```

---

# 6. Testa programmeringstecknen

Öppna exempelvis en terminal och testa:

```text
Alt + ,   → <
Alt + .   → >
Alt + -   → |
```

Du kan testa med:

```bash
echo '< > |'
```

eller skriva direkt i en texteditor.

---

# 7. Om `<`, `>` eller `|` inte fungerar

Det kan bero på tangentbordslayouten.

Kontrollera vilken layout du använder:

```bash
localectl status
```

Exempel:

```text
System Locale: LANG=en_US.UTF-8
VC Keymap: us
X11 Layout: se
```

eller:

```text
System Locale: LANG=en_US.UTF-8
VC Keymap: se
X11 Layout: se
```

Om du använder svensk layout kan det vara nödvändigt att använda andra keycodes i keyd-konfigurationen.

Använd då:

```bash
sudo keyd monitor
```

och tryck på de tangenter som ska användas.

Det gör att vi kan se exakt vilka keycodes HHKB skickar till Linux.

---

# 8. Kontrollera keyd-loggar

Om keyd inte startar:

```bash
sudo systemctl status keyd
```

Visa mer detaljerade loggar:

```bash
journalctl -u keyd -b
```

Du kan även följa loggen live:

```bash
journalctl -u keyd -f
```

---

# 9. Stäng av keyd tillfälligt

Om du bara vill **stänga av keyd just nu**, men behålla installationen och konfigurationen:

```bash
sudo systemctl stop keyd
```

Kontrollera:

```bash
systemctl status keyd
```

Nu ska keyd inte längre påverka tangentbordet.

### Starta keyd igen

```bash
sudo systemctl start keyd
```

Detta är användbart om du vill jämföra HHKB:n med och utan keyd.

---

# 10. Inaktivera keyd vid uppstart

Om du inte längre vill att keyd ska starta automatiskt när CachyOS startar:

```bash
sudo systemctl disable keyd
```

Detta **stänger inte nödvändigtvis av en redan körande keyd-process**.

För att både stoppa den nu och förhindra att den startar vid nästa boot:

```bash
sudo systemctl disable --now keyd
```

Kontrollera:

```bash
systemctl status keyd
```

Du kan senare aktivera den igen med:

```bash
sudo systemctl enable --now keyd
```

---

# 11. Ta bort keyd helt

Om du vill ta bort keyd från systemet:

Först stoppar och inaktiverar du tjänsten:

```bash
sudo systemctl disable --now keyd
```

Ta sedan bort paketet:

```bash
sudo pacman -Rns keyd
```

Om du även vill ta bort din keyd-konfiguration:

```bash
sudo rm -rf /etc/keyd
```

### Kontrollera

```bash
systemctl status keyd
```

Det är normalt att systemet då säger att tjänsten inte finns.

---

# 12. Skillnaden mellan stoppa, inaktivera och avinstallera

| Kommando                            | Effekt                                   |
| ----------------------------------- | ---------------------------------------- |
| `sudo systemctl stop keyd`          | Stoppar keyd just nu                     |
| `sudo systemctl start keyd`         | Startar keyd igen                        |
| `sudo systemctl disable keyd`       | Hindrar keyd från att starta automatiskt |
| `sudo systemctl enable keyd`        | Låter keyd starta automatiskt igen       |
| `sudo systemctl disable --now keyd` | Stoppar keyd + hindrar autostart         |
| `sudo pacman -Rns keyd`             | Avinstallerar keyd                       |

### Rekommenderat om du bara vill stänga av det

```bash
sudo systemctl disable --now keyd
```

Det är det enklaste sättet att tillfälligt stänga av hela lösningen utan att radera konfigurationen.

---

# 13. Komplett minimal konfiguration

Den kompletta filen `/etc/keyd/default.conf` är:

```ini
[main]

M-, = <
M-. = >
M-- = |
```

---

# 14. Rekommenderad vidareutveckling för HHKB

När detta fungerar kan fler programmeringstecken läggas till.

Exempelvis:

```text
Alt + , → <
Alt + . → >
Alt + - → |

Alt + [ → {
Alt + ] → }

Alt + 8 → [
Alt + 9 → ]

Alt + / → \
Alt + ' → `
```

Det går även att skapa ett separat **programmeringslager** där exempelvis en modifierartangent används för många extra funktioner.

Exempel:

```text
          HHKB
           │
           ▼
    ┌───────────────┐
    │   keyd layer  │
    ├───────────────┤
    │ <  >  |       │
    │ [  ]  {  }    │
    │ \  `  ~       │
    │ F1-F12        │
    │ Navigation     │
    └───────────────┘
```

Det är särskilt användbart på HHKB eftersom tangentbordet har färre fysiska tangenter än ett vanligt fullstort tangentbord.

---

# 15. Snabbkommandon

### Installera

```bash
sudo pacman -S keyd
```

### Redigera konfiguration

```bash
sudo nano /etc/keyd/default.conf
```

### Starta keyd

```bash
sudo systemctl enable --now keyd
```

### Ladda om

```bash
sudo keyd reload
```

### Starta om

```bash
sudo systemctl restart keyd
```

### Stoppa

```bash
sudo systemctl stop keyd
```

### Inaktivera autostart

```bash
sudo systemctl disable keyd
```

### Stoppa + inaktivera

```bash
sudo systemctl disable --now keyd
```

### Aktivera igen

```bash
sudo systemctl enable --now keyd
```

### Kontrollera status

```bash
systemctl status keyd
```

### Se tangenttryckningar

```bash
sudo keyd monitor
```

### Se loggar

```bash
journalctl -u keyd -b
```

---

# Resultat

Efter installationen ska HHKB kunna användas som vanligt, men med de extra programmeringstangenterna:

```text
Alt + ,  → <
Alt + .  → >
Alt + -  → |
```

Det gör att du kan skriva exempelvis:

```c
if (x < 10) {
    printf("x > 5");
}
```

utan att behöva byta till ett annat tangentbord eller använda komplicerade systemgenvägar.
