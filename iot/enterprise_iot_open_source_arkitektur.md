# Förslag: Open source enterprise-IoT-plattform

## 1. Mål

Bygga en självhostad, open source IoT-plattform för enterprise-bruk utan
att ersätta den befintliga **ChirpStack-installationen**. Plattformen
ska komplettera ChirpStack med bland annat:

-   Central enhets- och tillgångshantering
-   Dashboards och visualisering
-   Historik och datalagring
-   Regler, larm och automationer
-   Användare, roller och SSO
-   API:er och integrationer
-   Övervakning, backup och driftsäkerhet

Detta är ett förslag till arkitektur som behöver verifieras och testas
mot verksamhetens krav innan produktionssättning.

## 2. Föreslagen arkitektur

``` text
LoRaWAN-sensorer och gateways
             |
             v
       ChirpStack v4
  (befintlig installation)
             |
             v
     MQTT / meddelandeflöde
             |
       +-----+----------------+
       |                      |
       v                      v
   OpenRemote              Node-RED
   IoT-gränssnitt          Automationer
   och tillgångar          och integrationer
       |                      |
       +----------+-----------+
                  |
          API:er och externa system

Kompletterande infrastruktur:
- PostgreSQL: beständig lagring för plattformen
- Keycloak/IAM: identitet och SSO, efter verifiering av integrationsstödet
- Prometheus + Grafana: teknisk övervakning
- Nginx eller Traefik: HTTPS och reverse proxy
- Docker Compose eller Kubernetes: driftsättning, beroende på krav
```

### Ansvarsområden

-   **ChirpStack:** LoRaWAN-nätverksserver, gateways, enhetsanslutning
    och uplink-/downlink-hantering.
-   **MQTT:** Transport av händelser och sensordata mellan komponenter.
-   **OpenRemote:** Föreslagen huvudplattform för tillgångsmodell,
    enhetsrelaterade vyer, dashboards, regler och användargränssnitt.
-   **Node-RED:** Flödesbaserad automation, datatransformation och
    integrationer med API:er och andra system.
-   **PostgreSQL:** Databas för de komponenter som använder PostgreSQL.
    Verifiera behovet av separat tidsserielagring utifrån datamängd och
    historikkrav.
-   **Keycloak/IAM:** Central identitet och SSO om integrationen med
    valda komponenter uppfyller kraven.
-   **Prometheus + Grafana:** Övervakning av tjänster, resurser och
    teknisk hälsa.
-   **Nginx/Traefik:** TLS-terminering och publicering av
    webbgränssnitt/API:er.

Komponenterna ska inte antas dela databas eller autentisering
automatiskt; varje integration behöver konfigureras och verifieras.

## 3. Kandidater till huvudplattform

### Först att utvärdera: OpenRemote

Passar som första kandidat när målet är en relativt färdig, självhostad
IoT-plattform med tillgångshantering, användargränssnitt, dashboards och
regler.

-   Webbplats: <https://openremote.io/>
-   Källkod: <https://github.com/openremote/core>
-   Licens: AGPL-3.0 enligt projektets publicerade licens. Granska
    villkoren för den tänkta användningen och distributionen.

Verifiera särskilt MQTT-integrationen med ChirpStack, SSO,
multi-tenancy, behörighetsisolering och hög tillgänglighet.

### Alternativ: Eclipse Kapua

Värt att utvärdera om tyngdpunkten ligger på anslutningshantering,
gateway-administration, datarouting och API-integrationer.

-   Projekt: <https://projects.eclipse.org/projects/iot.kapua>

Kontrollera projektets aktuella status, version, licens och hur väl det
täcker behovet av färdiga dashboards och tillgångshantering.

### Alternativ: Magistrala

Intressant för en API-orienterad IoT-backend eller om organisationen
vill bygga mer av den egna applikationen.

-   Webbplats: <https://magistrala.absmach.eu/>

Kontrollera aktuell release, licens, mognad, driftkrav och hur mycket
egen utveckling som krävs.

**Rekommendation:** Börja med en proof of concept (PoC) av OpenRemote.
Jämför med Kapua eller Magistrala om PoC:n inte klarar kraven.

## 4. Automation: Home Assistant, Node-RED eller Flowable?

### Node-RED --- generell IoT-automation

Rekommenderas som första automationskomponent för MQTT-händelser och
integrationer.

Exempel: - Skapa larm om temperatur överstiger en gräns under en bestämd
tid. - Upptäck sensorer som inte har rapporterat inom en timeout. -
Omvandla payloads och skicka data vidare till API:er. - Skicka notiser
eller anropa externa system.

Webbplats: <https://nodered.org/>

För produktion behöver Node-RED-flöden versionshanteras och driftas med
plan för behörigheter, backup, återställning och eventuell redundans.

### Home Assistant --- fastighetsautomation

Lämpligt om lösningen också ska styra eller samordna byggnads- och
fastighetsfunktioner med många färdiga integrationer.

-   Visuell automation och scheman
-   MQTT-integration
-   Notiser och styrning av kompatibla system

Webbplats: <https://www.home-assistant.io/>

Home Assistant bör ses som ett komplement för fastighetsautomation, inte
automatiskt som central enterprise-backend för hela IoT-plattformen.

### Flowable --- verksamhetsprocesser

Relevant när automation kräver godkännanden, eskaleringar eller
processer där människor deltar.

Webbplats: <https://www.flowable.com/open-source>

För vanlig MQTT-baserad sensorlogik är Node-RED normalt enklare att
börja med.

## 5. Enterprise-krav att verifiera

### Identitet och behörighet

-   SSO mot Keycloak, Active Directory eller befintlig
    identitetsleverantör
-   Rollbaserad åtkomst (RBAC)
-   Multi-tenancy om flera organisationer/förvaltningar ska dela
    plattformen
-   Testad isolering mellan organisationers enheter, data, larm och
    API:er
-   Revisionsloggar för relevanta administrativa åtgärder

### Säkerhet

-   TLS för webb, API och MQTT där det är tillämpligt
-   Säker hantering och rotation av hemligheter och enhetsnycklar
-   Minsta möjliga behörighet mellan tjänster
-   Uppdaterings- och sårbarhetshantering
-   Backup och testad återläsning

### Driftsäkerhet och skalning

-   Hälsokontroller och larm för tjänster
-   Resurs- och kapacitetsmätning
-   Loggning och spårbarhet
-   Definierade RPO/RTO för backup och återställning
-   Testad uppgradering och rollback
-   Hög tillgänglighet där verksamhetskraven motiverar det

### Data och integration

-   Dokumenterade MQTT-topics och payloadformat
-   Tydlig mappning från ChirpStack-enheter till tillgångar och attribut
-   Policy för datalagring, retention och historik
-   API-dokumentation och integrationstester
-   Tydlig skillnad mellan enhetens anslutningsstatus och tiden sedan
    senaste mätvärde

## 6. Föreslagen införandeplan

1.  **Kravlista:** Definiera antal enheter, meddelandefrekvens,
    användare, organisationer, retention, larm och tillgänglighetskrav.
2.  **PoC:** Installera OpenRemote i en testmiljö och anslut ChirpStack
    via MQTT.
3.  **Datamodell:** Mappa enheter, sensortyper, metadata, attribut och
    tidsstämplar.
4.  **Automation:** Lägg till Node-RED och implementera ett par
    representativa regler.
5.  **Identitet:** Testa SSO, roller och isolering mellan
    användare/organisationer.
6.  **Drift:** Sätt upp TLS, övervakning, backup, loggning och
    dokumenterade uppgraderingar.
7.  **Belastningstest:** Testa förväntad och högre meddelandebelastning
    samt återhämtning efter fel.
8.  **Produktionsbeslut:** Bekräfta licenser, säkerhetskrav,
    supportmodell och driftsansvar innan lansering.

## 7. Öppna beslut

Följande behöver beslutas för att kunna färdigställa arkitekturen:

-   Ska flera separata organisationer/förvaltningar dela plattformen?
-   Krävs SSO via Keycloak eller Active Directory?
-   Hur många enheter och meddelanden per minut förväntas?
-   Hur länge ska rådata och aggregerad historik sparas?
-   Krävs hög tillgänglighet, och vilka RPO/RTO gäller?
-   Ska plattformen endast övervaka sensorer eller även styra
    utrustning?
-   Ska driften ske med Docker Compose eller Kubernetes?
-   Vilka licensvillkor är acceptabla för verksamheten?

## Sammanfattning

Behåll **ChirpStack** som LoRaWAN-lager. Utvärdera **OpenRemote** som
huvudplattform, använd **Node-RED** för generell automation och
komplettera med PostgreSQL, identitet/SSO, övervakning och TLS. Lägg
till **Home Assistant** om fastighetsautomation är ett separat behov.
Verifiera integrationsstöd, licenser, multi-tenancy och driftsäkerhet i
en PoC innan produktionssättning.
