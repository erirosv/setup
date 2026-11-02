# Installera Linux (postmarketOS) på Lenovo Tab 4 10 Plus (TB-X704F) via USB-kabel

> **Läs detta först**
> - Den här guiden installerar **postmarketOS**, en Linuxdistribution för mobiler och plattor som bygger på Alpine Linux.
> - Porten för TB-X704F är **experimentell och saknar underhållare**. Den använder Lenovos gamla Android-kernel (Linux 3.18). Räkna med att saker som grafikacceleration, wifi, ljud, kamera och batterihantering kan sakna funktion eller fungera dåligt.
> - **All data på plattan raderas** när bootloadern låses upp.
> - Du gör detta på egen risk. I värsta fall startar plattan inte. Det går nästan alltid att återställa Android (se avsnitt 9), men det finns inga garantier.

---

## Innehåll

1. Vad du behöver
2. Förbered plattan (Android)
3. Förbered datorn
4. Lås upp bootloadern
5. (Valfritt men rekommenderat) Installera TWRP
6. Installera och konfigurera pmbootstrap
7. Bygg postmarketOS
8. Flasha postmarketOS till plattan
9. Återställa Android om något går fel
10. Felsökning

---

## 1. Vad du behöver

| Sak | Kommentar |
|---|---|
| Lenovo Tab 4 10 Plus **TB-X704F** | Wifi-modellen. Kontrollera modellnumret under *Inställningar → Om surfplattan*. |
| USB-kabel som klarar data | Inte en kabel som bara laddar. Använd gärna originalkabeln. |
| Dator med **Linux** | Krävs för pmbootstrap. WSL på Windows **fungerar inte**. Har du Windows kan du använda VirtualBox med Ubuntu eller starta Ubuntu från ett USB-minne (live-läge). |
| Internetuppkoppling | pmbootstrap laddar ned paket under bygget. |
| Laddad platta | Minst 60 % batteri. |
| Minst ca 10 GB ledigt diskutrymme på datorn | För byggmiljön. |

---

## 2. Förbered plattan (Android)

1. **Säkerhetskopiera** bilder, filer och annat du vill behålla.
2. Gå till **Inställningar → Om surfplattan** (eller *Om enheten*) och tryck **7 gånger** på **Versionsnummer**. Nu är *Utvecklaralternativ* aktiverade.
3. Gå till **Inställningar → System → Utvecklaralternativ** (platsen kan variera) och slå på:
   - **OEM-upplåsning** (*OEM unlocking*)
   - **USB-felsökning** (*USB debugging*)
4. Anslut plattan till datorn med USB-kabeln. När frågan *Tillåta USB-felsökning?* visas på plattan, kryssa i *Tillåt alltid från den här datorn* och tryck **OK**.

---

## 3. Förbered datorn

Instruktionerna nedan gäller Ubuntu/Debian. Andra distributioner har motsvarande paket.

### 3.1 Installera adb och fastboot

```bash
sudo apt update
sudo apt install android-sdk-platform-tools git python3
```

(På vissa versioner heter paketen `adb` och `fastboot`: `sudo apt install adb fastboot`.)

### 3.2 Kontrollera kontakten med plattan

```bash
adb devices
```

Plattans serienummer ska visas med statusen `device`. Om det står `unauthorized` har du inte godkänt datorn på plattan (steg 2.4).

> Om `fastboot` senare inte hittar plattan, eller ger `no permissions`, kan du prova att köra kommandot med `sudo` eller installera udev-reglerna med `sudo apt install android-sdk-platform-tools-common`.

---

## 4. Lås upp bootloadern

> ⚠️ **Det här steget raderar all data på plattan.**

1. Starta om plattan till bootloader-/fastboot-läge:

   ```bash
   adb reboot bootloader
   ```

   Om det inte fungerar: stäng av plattan och håll **Volym ned + Power** tills fastboot-skärmen visas.

2. Kontrollera att datorn ser plattan:

   ```bash
   fastboot devices
   ```

3. Lås upp:

   ```bash
   fastboot oem unlock-go
   ```

   (På Lenovo-plattor av den här generationen är det `oem unlock-go` som gäller. Vanliga `fastboot flashing unlock` ger ofta felet *"Need wipe userdata. Do 'fastboot oem unlock-go'"*.)

4. Plattan raderas och startar om. Den visar nu en varning om att enheten är upplåst vid varje start. Det är normalt.

5. Kontrollera att upplåsningen gick igenom: gå tillbaka till fastboot (`adb reboot bootloader` kräver att du aktiverar USB-felsökning igen efter återställningen, alternativt Volym ned + Power) och kör:

   ```bash
   fastboot getvar unlocked
   ```

   Svaret ska vara `unlocked: yes`.

---

## 5. (Valfritt men rekommenderat) Installera TWRP

TWRP är en recovery-miljö med officiellt stöd för TB-X704F. Du behöver den inte för att installera postmarketOS via USB, men den är bra att ha för att **göra en fullständig säkerhetskopia av Android** innan du skriver över systemet.

1. Ladda ner senaste `twrp-*-X704F.img` från TWRP:s officiella sida för *Lenovo Tab4 10 Plus* (twrp.me → Lenovo → Lenovo Tab4 10 Plus).
2. Med plattan i fastboot-läge:

   ```bash
   fastboot flash recovery twrp-X.X.X-X-X704F.img
   ```

3. Starta direkt in i TWRP **utan att starta Android först** (annars kan Android skriva tillbaka sin egen recovery): håll **Volym upp + Power** från avstängt läge, eller:

   ```bash
   fastboot boot twrp-X.X.X-X-X704F.img
   ```

4. I TWRP: välj **Backup**, markera *Boot*, *System* och *Data*, och spara till SD-kort. Kopiera sedan säkerhetskopian till datorn.

---

## 6. Installera och konfigurera pmbootstrap

pmbootstrap är postmarketOS officiella verktyg för att bygga och flasha systemet.

### 6.1 Installera

Det enklaste sättet är att köra den senaste versionen direkt från git:

```bash
git clone https://gitlab.postmarketos.org/postmarketOS/pmbootstrap.git
mkdir -p ~/.local/bin
ln -s "$PWD/pmbootstrap/pmbootstrap.py" ~/.local/bin/pmbootstrap
```

Kontrollera att `~/.local/bin` finns i din `PATH` (logga ut och in igen vid behov) och testa:

```bash
pmbootstrap --version
```

Alternativt finns pmbootstrap som paket i många distributioner (`sudo apt install pmbootstrap`), men versionen kan vara äldre.

### 6.2 Initiera

```bash
pmbootstrap init
```

Du får ett antal frågor. Rekommenderade svar:

| Fråga | Svar |
|---|---|
| Work path | Standardvärdet går bra (tryck Enter). |
| Channel | `edge` (porten finns bara i utvecklingsgrenen). |
| Vendor | `lenovo` |
| Device codename | `tb-x704f` |
| User interface | Se nedan. |
| Username | Valfritt användarnamn. |
| Övriga frågor | Standardvärdena fungerar oftast. |

**Om enheten inte syns i listan:** porten ligger i en kategori som inte alltid visas som standard (till exempel *testing*). pmbootstrap frågar då oftast om du vill visa även sådana enheter. Svara ja. Om porten tagits bort helt ur postmarketOS går guiden inte att följa längre. Kontrollera i så fall postmarketOS-wikin.

**Val av gränssnitt:**

- `phosh` eller `plasma-mobile`: fullständiga pekgränssnitt, men kräver fungerande grafikacceleration. Med den här gamla kerneln blir de troligen mycket långsamma eller startar inte.
- `sxmo-de-sway`: lättare gränssnitt som är mer realistiskt på en downstream-port.
- `console`: bara textterminal. Bra för att först testa att systemet alls startar.

**Tips:** Börja med `console` eller `sxmo-de-sway`. Fungerar det kan du bygga om med ett annat gränssnitt senare.

### 6.3 Kontrollera inställningarna

```bash
pmbootstrap status
```

---

## 7. Bygg postmarketOS

```bash
pmbootstrap install
```

- Du får välja ett lösenord för användaren. Det behövs för att logga in.
- Första bygget tar tid (från tiotals minuter till över en timme) beroende på dator och uppkoppling.
- Vill du ha diskkryptering lägger du till `--fde`, men det rekommenderas inte på en experimentell port eftersom det försvårar felsökningen.

Om bygget avbryts med fel: se avsnitt 10.

---

## 8. Flasha postmarketOS till plattan

1. Sätt plattan i fastboot-läge (stäng av, håll **Volym ned + Power**) och anslut den.
2. Kontrollera:

   ```bash
   fastboot devices
   ```

3. Flasha rotfilsystemet:

   ```bash
   pmbootstrap flasher flash_rootfs
   ```

   Om du får ett felmeddelande om att `system`-partitionen är för liten, flasha istället till den större `userdata`-partitionen:

   ```bash
   pmbootstrap flasher flash_rootfs --partition userdata
   ```

4. Flasha kerneln:

   ```bash
   pmbootstrap flasher flash_kernel
   ```

5. Starta om:

   ```bash
   fastboot reboot
   ```

6. Plattan ska nu starta postmarketOS. Första starten kan ta en stund.

### Komma åt plattan via USB efter installationen

postmarketOS skapar ett nätverk över USB-kabeln. Från datorn kan du logga in med SSH (om SSH valdes vid `pmbootstrap init`):

```bash
ssh användarnamn@172.16.42.1
```

Det är mycket användbart om skärmen är svart eller gränssnittet inte startar.

---

## 9. Återställa Android om något går fel

### Med TWRP-säkerhetskopia (avsnitt 5)

1. Starta TWRP (Volym upp + Power).
2. Välj **Restore** och välj din säkerhetskopia.

### Med Lenovos officiella verktyg

Lenovo har ett Windows-program, **Lenovo Software Fix** (tidigare *Rescue and Smart Assistant*, LMSA), som laddar ned och installerar originalfirmware för din modell. Ladda ned det från Lenovos officiella supportsida och välj *Rescue*. Det fungerar oftast även på en platta som inte startar, så länge den kan nå fastboot-läge.

> Hämta firmware och drivrutiner bara från Lenovos egna webbplatser (`lenovo.com`). Det finns många tredjepartssidor som ger sken av att vara officiella.

---

## 10. Felsökning

| Problem | Möjlig lösning |
|---|---|
| `fastboot devices` visar inget | Byt USB-kabel eller USB-port (använd gärna en USB 2.0-port direkt på datorn, inte via hubb). Prova `sudo fastboot devices`. |
| `FAILED (remote: 'Need wipe userdata...')` | Använd `fastboot oem unlock-go` (avsnitt 4). |
| OEM-upplåsning är gråmarkerad i Android | Anslut plattan till internet en stund och starta om. På vissa enheter blir alternativet tillgängligt först då. |
| Enheten saknas i `pmbootstrap init` | Se kommentaren i avsnitt 6.2. Porten kan ha flyttats eller tagits bort. |
| Bygget misslyckas | Kör `pmbootstrap pull` och försök igen. Läs loggen med `pmbootstrap log`. Eftersom porten saknar underhållare kan det krävas egna rättelser. Fråga i så fall i postmarketOS chatt (Matrix) eller på deras GitLab. |
| Plattan fastnar på Lenovo-logon | Starta om till fastboot (Volym ned + Power) och prova med gränssnittet `console`. Om det inte heller fungerar stöds porten troligen inte längre av aktuell postmarketOS. Återställ Android enligt avsnitt 9. |
| Svart skärm men plattan verkar igång | Prova SSH-inloggning via USB (avsnitt 8). |
| Gränssnittet är mycket segt | Förväntat med den gamla kerneln. Byt till ett lättare gränssnitt (`sxmo-de-sway` eller `console`). |

---

## Länkar

- postmarketOS wiki: <https://wiki.postmarketos.org>
- pmbootstrap-dokumentation: <https://docs.postmarketos.org/pmbootstrap/>
- postmarketOS paketinformation för plattan: <https://pkgs.postmarketos.org/package/master/postmarketos/aarch64/device-lenovo-tb-x704f>
- TWRP: <https://twrp.me>
- Lenovo support (TAB4 10 Plus): <https://pcsupport.lenovo.com>
