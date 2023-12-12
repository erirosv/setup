# Git

## Kapitel 1: En Introduktion till Git

### Vad är Git?

Git är ett distribuerat versionshanteringssystem som används för att spåra ändringar i källkoden under utvecklingsprocessen. Det skapades av Linus Torvalds år 2005 och har sedan dess blivit standard inom många utvecklingsprojekt.

### Varför använda Git?
Git erbjuder flera fördelar, inklusive:
- **Versionskontroll:** Git sparar och hanterar alla ändringar i koden, vilket möjliggör enkel återgång till tidigare versioner om något går fel.
- **Distribuerad utveckling:** Git tillåter flera utvecklare att arbeta parallellt på olika delar av projektet, vilket ökar effektiviteten.
- **Branching och merging:** Utvecklare kan skapa separata grenar (branches) för att experimentera med nya funktioner eller fixa buggar utan att påverka huvudkoden. Dessa grenar kan sedan enkelt slås samman (merged) när de är klara.  

### Grundläggande Git-kommandon

Här är några grundläggande Git-kommandon för att komma igång:

```markdown 
git init: Initialiserar ett nytt Git-repositorium i den aktuella katalogen.
git clone [URL]: Klonar ett befintligt Git-repositorium från en given URL.
git add [fil]: Lägger till en fil i den så kallade "staging area" för att förbereda för en commit.
git commit -m "Meddelande": Sparar ändringarna i koden med ett beskrivande meddelande.
git pull: Hämtar och integrerar ändringar från ett fjärrrepositorium till det lokala.
git push: Skickar ändringar från det lokala repositoriet till det fjärranlagda repositoriet.
git branch: Visar befintliga grenar och den aktuella grenen.
git merge [gren]: Slår samman ändringar från en specifik gren till den aktuella grenen.
```
Detta är bara några grundläggande kommandon. Nästa kapitel kommer att utforska GitLab, en plattform som bygger på Git för att underlätta samarbete och projektadministration.