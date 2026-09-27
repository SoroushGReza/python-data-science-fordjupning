# Datavalidering av orderdata med Pydantic

Individuell fördjupningsuppgift inom Python för Data Science.

## Syfte

Syftet är att undersöka hur Pydantic kan användas för att kontrollera
orderrdata innan den används i en analys. Fördjupningen fokuserar på
typannoteringar, datamodeller, valideringsregler och felhantering.

Följande frågor undersöks:

- Hur definieras datatyper och valideringsregler i en Pydantic-modell?
- När är automatisk typomvandling användbar, och när passar strikt
  validering bättre?
- Hur kan fel rapporteras så att det framgår vilken rad och vilket
  fält som behöver rättas?

## Planerad funktion

Programmet ska läsa orderdata från en CSV-fil och kontrollera varje
rad mot en gemensam datamodell.

Godkända rader ska sparas separat. Rader som inte uppfyller reglerna
ska redovisas i en felrapport med information om orsaken.

## Koppling till Data Science

Datakvalitet påverkar tillförlitligheten i analyser och modeller.
Ett valideringssteg kan upptäcka exempelvis saknade värden, felaktiga
datatyper och otillåtna värden innan datan används vidare.

## Avgränsning

Projektet använder små, lokala CSV filer med en bestämt kolumnstruktur.
Exempeldata skapas för demonstrationen och innehåller inga verkliga
kunduppgifter.

Projektet omfattar inte databas, webbgränssnitt, externa API:er eller
maskininlärning. Validerringen kontrollerar definerade regler och kan
inte garantera att uppgifternaa stämmer i verkligheten.

## Teknik och installation

- Python 3.10 eller senare
- Pydantic 2.12.5
- Pythons standardbibliotek

Kör följande i projektets rot på Windows med PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Projektstatus

Projektet är under utveckling. Körinstruktioner för programmet,
exempeldata och sparade resultat läggs till under arbetets gång.


## Köra datamodellens demonstration

Kör från projektets rot:

```powershell
.\.venv\Scripts\python.exe demo_model.py
```

Demonstrationen använder två påhittade orderrader.

Den första visar hur textvärden omvandlas till heltal, Decimal och
datum, samt hur omgivande blanksteg tas bort från textfält.

Den andra visar fyra valideringsfel: ett tomt produktnamn, antal noll,
ett negativt pris och ett ogiltigt datum. Felen fångas och presenteras
med fältnamn och felorsak.

Datamodellen finns i `order_model.py`. Demonstrationen finns i
`demo_model.py`.


## Dokumentation

- [Pydantic: modeller](https://docs.pydantic.dev/latest/concepts/models/)
- [Pydantic: validatorer](https://docs.pydantic.dev/latest/concepts/validators/)
- [Pydantic: felhantering](https://docs.pydantic.dev/latest/errors/errors/)
- [Python: virtuella miljöer](https://docs.python.org/3/library/venv.html)