# Ollama – Uppdatering och lagringskonfiguration på CachyOS / Arch Linux

Den här guiden beskriver hur du:
- Uppdaterar Ollama till senaste versionen.
- Konfigurerar vilken disk Ollama ska spara modeller på.
- Kontrollerar att systemd-tjänsten fungerar.
- Säkerställer att lagringsdisken monteras korrekt vid uppstart.

## 1. Kontrollera nuvarande installation

Kontrollera installerad version:

```bash
ollama --version
```

Kontrollera befintliga modeller:

```bash
ollama list
```

Kontrollera tjänstens status:

```bash
sudo systemctl status ollama
```

## 2. Uppdatera Ollama

Om Ollama installerats med den officiella installationsmetoden kan du uppdatera med:

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

Starta om tjänsten:

```bash
sudo systemctl restart ollama
```

Kontrollera att uppdateringen lyckades:

```bash
ollama --version
sudo systemctl status ollama
```

## 3. Välj lagringsplats för modeller

Ollama använder miljövariabeln `OLLAMA_MODELS` för att bestämma var modellerna ska sparas.

I detta exempel används en separat lagringsdisk monterad på `/mnt/data`.

Önskad katalog:

```text
/mnt/data/ollama/models
```

Skapa katalogen:

```bash
sudo mkdir -p /mnt/data/ollama/models
```

## 4. Konfigurera Ollama med systemd

Öppna systemd override-filen:

```bash
sudo systemctl edit ollama
```

Lägg till följande:

```ini
[Service]
Environment="OLLAMA_MODELS=/mnt/data/ollama/models"
```

Spara och stäng editorn.

Detta gör att inställningen sparas permanent och används varje gång Ollama startas.

## 5. Konfigurera behörigheter

Ollama körs som systemanvändaren `ollama`.

Ge användaren rättigheter till lagringskatalogen:

```bash
sudo chown -R ollama:ollama /mnt/data/ollama
```

## 6. Ladda om systemd och starta om Ollama

Ladda om systemd-konfigurationen:

```bash
sudo systemctl daemon-reload
```

Starta om Ollama:

```bash
sudo systemctl restart ollama
```

Kontrollera status:

```bash
sudo systemctl status ollama
```

## 7. Verifiera konfigurationen

Kontrollera att rätt miljövariabel används:

```bash
systemctl show ollama --property=Environment
```

Förväntat resultat:

```text
OLLAMA_MODELS=/mnt/data/ollama/models
```

Kontrollera även att modellerna finns tillgängliga:

```bash
ollama list
```

## 8. Kontrollera att disken monteras automatiskt

Eftersom `/mnt/data` är en separat disk är det viktigt att den monteras innan Ollama startar.

Kontrollera aktuell montering:

```bash
findmnt /mnt/data
```

Kontrollera diskens UUID och filsystem:

```bash
lsblk -f
```

Om disken inte monteras automatiskt behöver den konfigureras i `/etc/fstab`.

För att säkerställa att Ollama väntar på lagringsdisken kan du lägga till följande i samma systemd override:

```ini
[Unit]
RequiresMountsFor=/mnt/data
```

Den kompletta override-filen blir då:

```ini
[Unit]
RequiresMountsFor=/mnt/data

[Service]
Environment="OLLAMA_MODELS=/mnt/data/ollama/models"
```

Ladda därefter om och starta om:

```bash
sudo systemctl daemon-reload
sudo systemctl restart ollama
```

## 9. Flytta befintliga modeller (om nödvändigt)

Om du redan har laddat ner modeller till den gamla lagringsplatsen behöver de flyttas.

Kontrollera först var modellerna ligger och stoppa Ollama:

```bash
sudo systemctl stop ollama
```

Kopiera modellfilerna från den gamla katalogen till den nya. Exempel med standardplatsen:

```bash
sudo rsync -aHAX --info=progress2 \
/usr/share/ollama/.ollama/models/ \
/mnt/data/ollama/models/
```

**Viktigt:** Kontrollera den gamla sökvägen innan du kör kommandot. Den kan skilja sig beroende på hur Ollama installerades.

Ge därefter rättigheter:

```bash
sudo chown -R ollama:ollama /mnt/data/ollama
```

Starta Ollama igen:

```bash
sudo systemctl start ollama
```

Verifiera:

```bash
ollama list
```

Radera inte de gamla modellerna förrän du har verifierat att de nya fungerar.

## 10. Felsökning och loggar

Visa de senaste 50 loggraderna:

```bash
journalctl -u ollama -n 50 --no-pager
```

Följ loggar i realtid:

```bash
journalctl -u ollama -f
```

Kontrollera vilken adress Ollama lyssnar på:

```bash
sudo ss -lntp | grep 11434
```

Kontrollera API:

```bash
curl http://localhost:11434/api/tags
```

---

## Sammanfattning – Viktiga kommandon

| Funktion | Kommando |
|---|---|
| Uppdatera Ollama | `curl -fsSL https://ollama.com/install.sh \| sh` |
| Lista modeller | `ollama list` |
| Ändra konfiguration | `sudo systemctl edit ollama` |
| Starta om Ollama | `sudo systemctl restart ollama` |
| Kontrollera status | `sudo systemctl status ollama` |
| Kontrollera lagringsplats | `systemctl show ollama --property=Environment` |
| Visa loggar | `journalctl -u ollama -n 50 --no-pager` |

## Aktuell konfiguration

| Inställning | Värde |
|---|---|
| Operativsystem | CachyOS / Arch Linux |
| Tjänst | `ollama.service` |
| Modellkatalog | `/mnt/data/ollama/models` |
| Miljövariabel | `OLLAMA_MODELS` |
| API-port | `11434` |
| Systemanvändare | `ollama` |

**Tips:** Behåll modellerna på den separata lagringsdisken. Det gör det enklare att hantera stora AI-modeller utan att fylla systemdisken.
