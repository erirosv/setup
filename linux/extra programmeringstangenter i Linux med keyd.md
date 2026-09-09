# HHKB – extra programmeringstangenter i Linux med keyd

Den här guiden visar hur du använder **keyd** för att lägga till tangenter som saknas eller är svåra att skriva på ett HHKB i Linux.

Fokus ligger framför allt på programmeringstecken:

| Kombination | Resultat |
|---|---|
| `Alt + ,` | `<` |
| `Alt + .` | `>` |
| `Alt + -` | `|` |

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

Lägg in:

```ini
[main]

M-, = <
M-. = >
M-- = |
```

### Vad betyder `M-`?

`M-` betyder **Meta**, vilket normalt motsvarar `Alt`.

Exempel:

```ini
M-, = <
```

betyder:

```text
Alt + , → <
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

# 9. Komplett minimal konfiguration

Den kompletta filen `/etc/keyd/default.conf` är:

```ini
[main]

M-, = <
M-. = >
M-- = |
```

---

# 10. Rekommenderad vidareutveckling för HHKB

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

## Snabbkommandon

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

## Resultat

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
