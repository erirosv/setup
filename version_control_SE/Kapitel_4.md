## Kapitel 4: Länka GitLab Repository till Azure DevOps

Att länka ditt GitLab-repositorium till Azure DevOps möjliggör integrerad hantering av projekt, hantering av arbetsuppgifter, och implementering av CI/CD (Continuous Integration/Continuous Deployment) genom Azure DevOps tjänster. Här är en steg-för-steg guide för att genomföra detta:

### Steg 1: Skapa ett Projekt i Azure DevOps

1. Gå till Azure DevOps-webbplatsen och logga in med ditt konto.
2. Skapa ett nytt projekt genom att klicka på "New Project" och följ instruktionerna för att ange projektnamn och inställningar.

### Steg 2: Skapa ett GitLab Personal Access Token

1. Logga in på GitLab och gå till "Settings" -> "Access Tokens".
2. Skapa ett nytt personligt access token med behörighet att läsa repositories.
3. Kopiera tokenet eftersom det kommer att användas senare för autentisering.

### Steg 3: Skapa en Service Connection i Azure DevOps

1. Inne i ditt Azure DevOps-projekt, gå till "Project Settings" -> "Service connections" -> "New service connection" -> "GitLab".
2. Ange GitLab-webbadressen och det tidigare skapade personal access token.
3. Klicka på "Verify and save" för att bekräfta anslutningen.

### Steg 4: Skapa en YAML-fil för CI/CD

I ditt GitLab-repositorium, skapa en fil med namnet .gitlab-ci.yml i roten.
Konfigurera YAML-filen med steg för att bygga, testa och distribuera din kod. 

Exempelvis:
```yaml
stages:
  - build
  - test
  - deploy

build_job:
  stage: build
  script:
    - echo "Building the project"

test_job:
  stage: test
  script:
    - echo "Running tests"

deploy_job:
  stage: deploy
  script:
    - echo "Deploying to production"
```

### Steg 5: Aktivera GitLab CI/CD-pipelinen

1. När du gör en push till ditt GitLab-repositorium, kommer GitLab att automatiskt upptäcka .gitlab-ci.yml och starta CI/CD-pipelinen.
2. Du kan övervaka pipelinen och dess steg direkt från GitLab-gränssnittet.

Genom att följa dessa steg skapar du en sömlös integration mellan ditt GitLab-repositorium och Azure DevOps för att hantera projektfaser och automatisera din CI/CD-process. Detta underlättar en effektiv och strukturerad utvecklingscykel.



