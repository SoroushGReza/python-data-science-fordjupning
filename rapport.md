# Datavalidering av orderdata med Pydantic

Individuell fördjupning inom Python för Data Science  

## Syfte

Jag ville undersöka hur Pydantic kan användas för att kontrollera orderdata innan den används i en analys. Målet var ett litet program som läser en CSV fil, skiljer godkända rader från underkända och förklarar vad som behöver rätttas. Jag ville också förstå skillnaden mellan att omvandla ett värde till rätt datatyp och att kräva att värdet redan har rätt typ.

Min huvudsakliga frågeställning var: Hur kan en gemensam datamodell användas för att validera orderdata och ge användbara felrapporter? Jag avgränsade arbetet till fem fält, små lokala filer och ett bestämt CSV-format. Databas, webbgränssnitt och maskininlärning ingår inte.

## Området och dess relevans

Fördjupningsområdet är datavallidering med pydantic. Biblioteket kopplar ihop Pythonkodens typannoteringar med kontroller som utförs när programmet körs. Det passar uppgiften eftersom jag undersöker datamodeller, fältregler, egna validatorer och felhantering i ett fungerande flöde.

För en Data Scientist är detta relevant redan innan själva analysen börjar. Ett felaktigt antal eller pris kan påverka sammanställningar, och saknade värden kan skapa problem längre fram. Genom att ange vad inkommande data måste uppfylla blir det lättare att upptäcka problem och ge återkoppling till den som levererat datan.

## Viktiga begrepp

**Typannotering och datamodell.** En annotering som `quantity: int` beskriver den avsedda typen. Python tvingar inte automatiskt vanliga variabler att följa annoteringen. I min klass `Order`, som ärver från `BaseModel`, använder Pydantic annoteringarna för validering. Alla fem fält är obligatoriska eftersom de saknar standardvärden. [1, 2]

**Schema och validering.** När modellen definieras samlar Pydantic in typer, inställningar och validatorer och bygger ett internt schema. Vid `model_validate()` används schemat för att kontrollera indata. Valideringsarbetet utförs av `pydantic-core`. Det gör att samma regler kan återanvändas på varje rad. [3]

**Fältregel och egen validator.** `Field(gt=0)` kräver ett värde större än noll. Min egen `field_validator` tar bort omgivande blanksteg från order-ID och produktnamn och avvisar tom text. Med `mode="after"` körs funktionen efter Pydantics typvalidering. Ett `ValueError` från funktionen tas med i modellens `ValidationError`. [4, 5, 6]

**Typomvandling.** I normalt läge kan texten `"3"` bli heltalet `3`. Strikt validering av Python-indata ställer striktare krav på typerna. Detta påverkar vilka värden som accepteras, även när de ser likadana ut för en användare. [7]

**Serialisering.** Modellens värden behöver kunna sparas i ett filformat. `model_dump(mode="json")` ger JSON-kompatibla värden, där exempelvis datum och `Decimal` representeras som strängar. [10]

<!-- pagebreak -->

## Genomförande

Projektet byggdes stegvis i VS Code på Windows med Python 3.12.9 och Pydantic 2.12.5. Biblioteket installerades i en separat `.venv`, och versionen anges i `requirements.txt`. Arbetet versionshanterades med Git och GitHub. Först byggdes modellen och en liten demonstration, sedan CSV flödet och till sist jämförelsen mellan valideringslägena.

Jag använde tio syntetiska orderrader som togs fram med hjälp av ChatGPT för projektet. Datan innehåller inga verkliga kunduppgifter. Priserna avser SEK. Några rader följer reglerna och andra har avsiktliga fel, så att det finns ett förväntat resultat att jämföra körningen med.

| Fil | Ansvar |
|---|---|
| `order_model.py` | Gemensam datamodell och valideringsregler. |
| `demo_model.py` | Visar typomvandling och samlade valideringsfel. |
| `validate_orders.py` | Läser CSV, validerar rader och sparar resultat. |
| `compare_validation.py` | Jämför sex indatafall i normalt och strikt läge. |

CSV-filen läses med `csv.DictReader`, som kopplar kolumnrubriker till värden i en dictionary. Värdena läses som text. Därför använder CSV flödet normal validering. Innan raderna behandlas kontrolleras att rubrikerna motsvarar modellens fält och inte är dubblerade. [9]

Varje rad skickas till `Order.model_validate()`. Vid ett `ValidationError` sparas radnummer, order-ID, fältnamn, meddelande och feltyp. Behandlingen fortsätter med nästa rad. Fel på filens kolumnstruktur stoppar däremot körningen, eftersom hela filen då avviker från det förväntade formatet.

Jag valde `Decimal` för priset eftersom decimalvärden från text kan representeras exakt, exempelvis `49.90`. Priset måste vara ändligt, minst noll och får inte kräva fler än två decimaler. Nollpris tillåts i denna demo, medan antalet måste vara större än noll. Det är regler för den valda tillämpningen, inte regler som passar alla slags orderdata. [8]

Godkända orderrader sparas med modellens normaliserade värden. Felrapporten byggs av utvalda feluppgifter som kan skrivas till JSON. Det gör rapporten enklare att läsa än ett fullständigt undantagsobjekt. Typomvandling och export hålls också isär i koden.

## Resultat

CSV-demonstrationen ger följande resultat med den medföljande filen:

| Mått | Resultat |
|---|---:|
| Behandlade orderrader | 10 |
| Godkända orderrader | 5 |
| Underkända orderrader | 5 |
| Valideringsfel | 6 |
| Summa för godkända orderrader | 873.10 SEK |

Resultaten sparas i `outputs/valid_orders.csv` och `outputs/validation_report.json`. Order `ORD-1010` har både ett antal med decimaler och ett pris med för många decimaler. Därför blir det sex fel på fem underkända rader. Produktnamnet `Suddgummi` får sina omgivande blanksteg borttagna i den godkända utdatafilen.

<!-- pagebreak -->

### Resultat från jämförelsen av valideringslägen

Jämförelsen använder samma ordermodell. Pris och datum har redan rätt Python-typer, så att bara antalet varierar. Det gör det tydligt vad som orsakar skillnaden mellan lägena. Följande resultat sparas i `outputs/strictness_comparison.json`:

| Indata | Python-typ | Normalt läge | Strikt läge |
|---|---|---|---|
| `"3"` | `str` | Godkänd som `3` | Underkänd |
| `3` | `int` | Godkänd som `3` | Godkänd som `3` |
| `3.0` | `float` | Godkänd som `3` | Underkänd |
| `3.5` | `float` | Underkänd | Underkänd |
| `True` | `bool` | Godkänd som `1` | Underkänd |
| `0` | `int` | Underkänd | Underkänd |

Resultatet visar att typomvandling både kan vara användbar och dölja en oväntad indatatyp. Att `"3"` blir `3` passar CSV-importen. Att det booleska Python-värdet `True` blir antalet `1` är lättare att missa. Detta gäller ett faktiskt booleskt värde i jämförelsen; det är inte samma indata som texten `"True"` i en CSV-fil.

Värdet `0` avvvisas i båda lägena eftersom fältregeln fortfarande gäller. Strikt validering ersätter alltså inte reglerna för tillåtna värden. Jämförelsen gäller `model_validate()` med Python-dictionaries. Vid direkt JSON-validering har Pydantic andra regler för vissa typer, exempelvis datum. [7]

## Begränsningar och möjliga förbättringar

Den tydligaste begränsningen är att valideringen bara kontrollerar de regler jag har definierat. Ett pris kan ha rätt typ och ändå vara fel för produkten. Ett datum kan vara giltigt men höra till fel beställning. Modellen kontrollerar dessutom varje rad separat och upptäcker inte dubblerade order-ID:n.

Datasetet är litet och konstruerat för demonstrationen. Det visar hur de valda fallen hanteras, men räcker inte för att bedöma tillförlitlighet på verkliga orderflöden. Godkända rader och felinformation samlas i minnet, och jag har inte undersökt prestanda för stora filer. Filformat och sökvägar är också avgränsade till projektets upplägg.

Ett naturligt nästa steg är automatiserade tester för fler gränsfall, till exempel saknade kolumner, tomma filer och oväntade datatyper. Därefter skulle jag kunna lägga till kontroller mellan rader. För större filer skulle resultaten kunna skrivas löpande för att minska minnesbehovet.

Ett alternativ till normal vallidering är uttrycklig parsning följd av strikt validering. Det ger mer direkt kontroll över accepterade format, men kräver också mer egen kod och felhantering. Vanliga Pythonfunktioner med villkor och undantag är ett annat alternativ för en liten lösning. Jag valde Pydantic för att samla återanvändbara regler i modellen.

## Koppling till yrkesrollen

Jag ser främst användning vid import av data från filer eller andra system. En Data Scientist eller analytiker kan använda ett sådant kontrollsteg för att upptäcka struktur- och värdefel innan sammanställningar och modeller byggs. Felrapporten kan ge underlag för dialog med dataleverantören. Vilka rader som får användas vidare behöver dock avgöras utifrån verksamhetens krav; ett tekniskt godkännande räcker inte som kvalitetsgaranti.

<!-- pagebreak -->

## Källor

Resultaten i rapporten avser projektets demonstrationer med Pydantic 2.12.5.

1. Python Software Foundation. **typing - Support for type hints.**
   https://docs.python.org/3/library/typing.html

2. Pydantic. **Models.**
   https://docs.pydantic.dev/latest/concepts/models/

3. Pydantic. **Architecture.**
   https://docs.pydantic.dev/latest/internals/architecture/

4. Pydantic. **Fields.**
   https://docs.pydantic.dev/latest/concepts/fields/

5. Pydantic. **Validators.**
   https://docs.pydantic.dev/latest/concepts/validators/

6. Pydantic. **Error Handling.**
   https://docs.pydantic.dev/latest/errors/errors/

7. Pydantic. **Strict Mode.**
   https://docs.pydantic.dev/latest/concepts/strict_mode/

8. Python Software Foundation. **decimal - Decimal fixed-point and floating-point arithmetic.**
   https://docs.python.org/3/library/decimal.html

9. Python Software Foundation. **csv - CSV File Reading and Writing.**
   https://docs.python.org/3/library/csv.html

10. Pydantic. **Serialization.**
    https://docs.pydantic.dev/latest/concepts/serialization/

**AI-stöd:** ChatGPT har använts som stöd för syntetiska exempeldata och formulering av dokumentation och rapport. Exempeldata kommer inte från en extern databas. Jag ansvarar för det som lämnas in och för att kunna förklara koden och de tekniska valen.

<!-- pagebreak -->

## Självreflektion

### 1. Vad lärde jag mig som jag inte kunde innan?

Det viktigaste för mig var att förstå skillnaden mellan att ange en datatyp och att faktiskt kontrollera ett värde när programmet körs. Jag fick också en tydligare bild av vad Pydantic gör med indata.

### 2. Vad var svårast att förstå eller genomföra?

Jag tyckte att skillnaden mellan normal och strikt validering krävde mest eftertanke. Först kan strikt läge verka som det självklara valet, men då uppstår frågan hur text från en CSV fil ska bli tal och datum. Jämförelsen hjälpte mig att förstå varför valet beror på hur datan kommer in och vilka omvandlingar jag vill tillåta.

### 3. Vilket tekniskt val är jag mest nöjd med och varför?

Jag är mest nöjd med att samma `Order`-modell används i både CSV flödet och demonstrationerna. Reglerna behöver då finnas på ett ställe, vilket gör koden lättare att följa och ändra. Jag tycker också att uppdelningen mellan underkända rader och enskilda fel gör resultatet tydligare.

### 4. Vad hade jag gjort annorlunda om jag började om?

Jag hade skrivit ner förväntat resultat för varje exempelrad tidigare. Då hade kopplingen mellan regel, indata och utfall blivit tydligare redan från början. Jag hade också velat lägga till några automatiserade tester tidigare, så att jag enklare kunde kontrollera att en ändring inte påverkar andra fall.

### 5. Vad är ett naturligt nästa steg?

Jag skulle börja med fler testfall och en kontroll för dubblerade order-ID:n. Efter det skulle jag vilja prova en större, anonymiserad datamängd för att se vilka situationer mina konstruerade exempel inte fångar.

### 6. Vilket betyg bedömer jag att arbetet motsvarar?

Min egen bedömning är VG. Det bygger framför allt på jämförelsen av vallideringslägen och resonemanget om vilka konsekvenser de tekniska valen får.

### 7. Hur kopplar jag bedömningen till kriterierna?

Jag bedömer att underlaget för G finns genom ett avgränsat område, fungerande kod, exempeldata, körinstruktioner, källor och sparade resultat. För VG lyfter jag fram återanvändningen av modellen, motiveringen av `Decimal` och vallideringsläge samt de pedagogiska exemplen som visar oväntad typomvandling. Jag diskuterar också begränsningar och alternativ.
