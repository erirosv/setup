# Python Virtual Environment – Windows, Linux & macOS

En virtuell Python-miljö (`venv`) gör att varje projekt kan ha sina egna Python-paket utan att påverka andra projekt.

---

## Snabbguide

| Åtgärd             | Windows PowerShell             | Linux                       | macOS                       |
| ------------------ | ------------------------------ | --------------------------- | --------------------------- |
| Gå till projekt    | `cd C:\path\project`           | `cd ~/path/project`         | `cd ~/path/project`         |
| Skapa venv         | `python -m venv .venv`         | `python3 -m venv .venv`     | `python3 -m venv .venv`     |
| Aktivera           | `.\.venv\Scripts\Activate.ps1` | `source .venv/bin/activate` | `source .venv/bin/activate` |
| Kontrollera Python | `where.exe python`             | `which python`              | `which python`              |
| Installera paket   | `python -m pip install ...`    | `python -m pip install ...` | `python -m pip install ...` |
| Köra program       | `python app.py`                | `python app.py`             | `python app.py`             |
| Avsluta venv       | `deactivate`                   | `deactivate`                | `deactivate`                |

--- 

## 1. Gå till projektmappen

### Windows – PowerShell

```powershell
cd C:\Users\dummy\fun\ai-test
```

Linux

```
cd ~/fun/ai-test
```

macOS

```
cd ~/fun/ai-test
```

## 2. Skapa den virtuella miljön

### Windows

```
python -m venv .venv
```

### Linux

På många Linux-system:

```
python3 -m venv .venv
``` 

Om python pekar på Python 3 kan du även använda:

```
python -m venv .venv
```

### macOS
``` 
python3 -m venv .venv
```

Det skapar en mapp som ser ut ungefär så här:

``` 
ai-test/
├── .venv/
└── app.py
```

`.venv` innehåller den virtuella Python-miljön för projektet.

## 3. Aktivera miljön

### Windows – PowerShell

```
.\.venv\Scripts\Activate.ps1
```

Efter aktivering bör terminalen visa något i stil med:

```
(.venv) PS C:\Users\dummy\fun\ai-test>
```

Om PowerShell säger att scriptkörning är blockerad:

```
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
``` 

Kör sedan:

```
.\.venv\Scripts\Activate.ps1
```

### Windows – CMD

Om du använder vanliga Command Prompt:

```
.venv\Scripts\activate.bat
```

### Linux

```
source .venv/bin/activate
```

### macOS

``` 
source .venv/bin/activate
```

Efter aktivering bör du se något i stil med:

```
(.venv) user@computer:~/fun/ai-test$
```

## 4. Kontrollera att miljön fungerar

När .venv är aktiverad:

```
python --version
```

Kontrollera även pip:

```
python -m pip --version
```

### Windows

```
where.exe python
```

Du bör få en sökväg som pekar på `.venv`:

```
C:\Users\dummy\fun\ai-test\.venv\Scripts\python.exe
```

### Linux / macOS

```
which python
``` 

Du bör få något liknande:

```
/home/user/fun/ai-test/.venv/bin/python
```

eller på macOS:

```
/Users/user/fun/ai-test/.venv/bin/python
```

## 5. Uppdatera pip

När den virtuella miljön är aktiverad:

```
python -m pip install --upgrade pip setuptools wheel
```

Det är bra att göra detta innan du installerar projektets övriga paket.

## 6. Installera Python-paket

Exempel:

```
python -m pip install numpy pandas matplotlib scikit-learn
```

För ett AI/ML-projekt kan du exempelvis installera:

```
python -m pip install numpy pandas matplotlib scikit-learn tqdm
```

PyTorch bör installeras enligt den version och GPU-plattform som projektet använder.

7. Köra programmet

När .venv är aktiverad:

```
python app.py
```

Exempel Windows:

```
(.venv) PS C:\Users\dummy\fun\ai-test> python app.py
```

## 8. Spara installerade paket

När projektets dependencies är installerade kan du skapa en requirements.txt:

```
python -m pip freeze > requirements.txt
```

Projektet kan då se ut så här:

```
ai-test/
├── .venv/
├── data/
├── app.py
└── requirements.txt
```

### Installera dependencies på en annan dator

Efter att projektet har klonats eller kopierats:

```
python -m pip install -r requirements.txt
```

Det installerar paketen som finns i `requirements.txt`.

> Du ska normalt inte lägga `.venv` i Git. Lägg istället till `.venv/` i `.gitignore`.

## 9. Avsluta den virtuella miljön

När du är färdig:

```
deactivate
```

Terminalen går då från exempelvis:

```
(.venv) PS C:\Users\dummy\fun\ai-test>
```

till:

```
PS C:\Users\dummy\fun\ai-test>
```

## 10. Nästa gång du öppnar projektet

Du behöver inte skapa `.venv` igen.

Gå bara till projektmappen och aktivera den.

### Windows – PowerShell

```
cd C:\Users\dummy\fun\ai-test
.\.venv\Scripts\Activate.ps1
```

### Linux

```
cd ~/fun/ai-test
source .venv/bin/activate
```

### macOS

```
cd ~/fun/ai-test
source .venv/bin/activate
```

Sedan kan du köra:

```
python app.py
```
