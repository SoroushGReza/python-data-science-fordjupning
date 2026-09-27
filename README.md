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


## Köra CSV-valideringen

Kör från projektets rot:

```powershell
.\.venv\Scripts\python.exe validate_orders.py
```

Programmet läser `data/orders.csv` och skapar:

- `outputs/valid_orders.csv`: orderrader som uppfyller valideringsreglerna.
- `outputs/validation_report.json`: sammanfattning och detaljer om fel.

Resultatfilerna skrivs om vid varje körning.


### Exempeldata

Datasetet består av tio syntetiska orderrader som togs fram med hjälp
av ChatGPT (OpenAI) för detta projekt. Uppgifterna är påhittade och representerar
inga verkliga kunder eller beställningar. Priserna avser SEK.

Filen använder UTF-8, komma som fältavskiljare och punkt som decimaltecken.
Den ska innehålla exakt dessa kolumner:

`order_id,product,quantity,unit_price,order_date`

Exempeldata innehåller både giltiga värden och avsiktliga fel:
tom produkttext, antal noll, negativt pris, ogiltigt datum,
antal med decimaler och pris med för många decimaler.

Syftet är att kontrollera om valideringen godkänner rätt rader och
identifierar de förväntade felen.

En begränsning är att detta lilla, konstruerade dataset inte täcker
all variation och alla fel som kan förekomma i verkliga orderdata.


### Förväntat resultat

- Behandlade orderrader: 10
- Godkända orderrader: 5
- Underkända orderrader: 5
- Valideringsfel: 6
- Summa för godkända orderrader: 873.10 SEK

En rad kan innehålla flera fel. Därför redovisas antalet underkända
rader och antalet valideringsfel separat.

`csv_line` i felrapporten anger postens sista fysiska rad i CSV-filen.
För exempeldata ligger varje post på en enda rad.

Saknade, oväntade eller dubblerade kolumnrubriker stoppar körningen.
Valideringsfel i enskilda orderrader samlas i felrapporten.


## Jämförelse av normal och strikt validering

Kör:

```powershell
.\.venv\Scripts\python.exe compare_validation.py
```

Programmet använder samma ordermodell och jämför sex värden för
`quantity`: `"3"`, `3`, `3.0`, `3.5`, `True` och `0`.

Övriga fält har korrekkta Python-typer för att isolera undersökningen
till antalet. Resultatet sparas i `outputs/strictness_comparison.json`.

I normalt läge accepteras exemplvis texten `"3"` och omvandlas till
heltal `3`. Strikt validering avvisar samma textvärde.

Jämförelsen visar också att det booleaska Python-värdet `True` kan
omvandlas till antalet `1` i normalt läge. Typomvandling kan därför
dölja oväntade indatatyper. Antalet `0` avvisas i båda lägena eftersom
modellen kräver ett värde större än noll.

CSV flödet använder normal validering eftersom CSV värden läses som
text. Ett alternativ är att först göra uttryckliga typomvandlingar
och därefter använda strikt vallidering.

Jämförelsen gäller Python dictionaries via `model_validate()`.
pydantics regler kan skilja sig vid direkt validering från JSON.


## Dokumentation

- [Pydantic: modeller](https://docs.pydantic.dev/latest/concepts/models/)
- [Pydantic: validatorer](https://docs.pydantic.dev/latest/concepts/validators/)
- [Pydantic: felhantering](https://docs.pydantic.dev/latest/errors/errors/)
- [Python: virtuella miljöer](https://docs.python.org/3/library/venv.html)
- [Pydantic: strikt validering](https://docs.pydantic.dev/latest/concepts/strict_mode/)