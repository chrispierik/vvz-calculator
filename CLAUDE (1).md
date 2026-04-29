# CLAUDE.md — Verzuimpremie Calculator
## verzekerverzuim.nl

---

## Doel van dit project

Bouw een verzuimpremie-calculator voor verzekerverzuim.nl. De calculator stelt MKB-ondernemers met 10–50 medewerkers in staat om in minder dan 2 minuten een schatting te krijgen van hun potentiële besparing op hun verzuimverzekering — zonder dat ze hun polis hoeven te uploaden.

De calculator is de ingang van een marketingcampagne gericht op bedrijven die **al** een verzuimverzekering hebben maar waarschijnlijk te veel betalen. De tone of voice is fris, direct en zonder jargon.

---

## De drie inputvelden

De calculator stelt precies drie vragen. Niet meer, niet minder.

### 1. Branche
Een dropdown met de volgende opties:

| Branche | Gemiddeld premie% | Marktbeste premie% |
|---|---|---|
| Bouw & installatie | 4.8% | 3.1% |
| Zorg & welzijn | 5.9% | 4.0% |
| Transport & logistiek | 5.2% | 3.6% |
| Horeca & catering | 5.5% | 3.8% |
| Groothandel & retail | 4.1% | 2.9% |
| Zakelijke dienstverlening | 2.8% | 1.9% |
| Productie & industrie | 4.6% | 3.2% |
| ICT & technologie | 2.2% | 1.5% |

> Deze percentages zijn illustratieve benchmarks. Vervang met actuele marktdata uit de eigen offertedata van verzekerverzuim.nl zodra beschikbaar.

### 2. Loonsom
- Invoer: slider of numeriek invoerveld
- Eenheid: totale bruto jaarloonsom in euro's
- Minimumwaarde: € 200.000
- Maximumwaarde: € 5.000.000
- Standaardwaarde: € 800.000
- Stap: € 50.000

### 3. Aantal medewerkers
- Invoer: slider of numeriek invoerveld
- Minimumwaarde: 5
- Maximumwaarde: 100
- Standaardwaarde: 20
- Stap: 1

---

## Berekening

De output wordt volledig automatisch berekend op basis van de drie inputs. Geen verdere invoer nodig.

```
huidigePremie    = loonsom × (gemiddeldPremiePercentage / 100)
marktbestePremie = loonsom × (marktbestePremiePercentage / 100)
geschatBesparing = huidigePremie - marktbestePremie
besparingPct     = (geschatBesparing / huidigePremie) × 100
```

---

## Output — wat de gebruiker ziet na invullen

Toon de volgende drie metrics prominent:

1. **Geschatte jaarlijkse besparing** — in euro's, groot en centraal
2. **Huidig gemiddeld premiepercentage** in hun branche
3. **Marktbeste premiepercentage** via verzekerverzuim.nl

Daaronder direct de call to action (zie hieronder).

### Verzuimscore A–E (optioneel uitbreidbaar)
Genereer automatisch een score op basis van de branche:
- Marktbeste prijs → A
- 0–10% boven marktbeste → B
- 10–20% erboven → C
- 20–35% erboven → D
- 35%+ erboven → E

De score visualiseert waar de ondernemer staat zonder dat hij zijn eigen premie hoeft te weten.

---

## Call to action

Na het tonen van de besparing:

> **"Vraag gratis offertes aan bij 6 verzekeraars — binnen 24 uur in je inbox."**

Verzamel:
- Naam
- Bedrijfsnaam
- E-mailadres
- Telefoonnummer (optioneel)

Stuur na invullen automatisch het verzuimrapport naar het opgegeven e-mailadres.

---

## Design

### Visuele stijl
- Donkere achtergrond (`#0a0a0a` of vergelijkbaar)
- Primaire accentkleur: blauw (`#378ADD`)
- Tekst: wit op donker
- Lettertype: modern sans-serif (Inter, DM Sans of Geist)
- Afgeronde hoeken, voldoende witruimte
- Progressiebalk bovenaan die stap 1 t/m 3 aangeeft

### Toon van de teksten
- Direct en zonder verzekeringsvaaktaal
- Geen angstmarketing — de ondernemer heeft het al geregeld, dit is een optimalisatie
- Voorbeeldtekst stap 1: *"Wat betaal jij eigenlijk te veel?"*
- Subkop: *"Beantwoord 3 vragen. Wij schatten je besparing — op basis van gemiddelden uit onze database van 6 verzekeraars."*

### Responsiviteit
- Volledig mobielvriendelijk
- Sliders werken op touch
- Resultaatpagina leesbaar op klein scherm

---

## Tech stack (aanbevolen)

- **Framework:** React (Vite) of Next.js
- **Styling:** Tailwind CSS
- **Formulierverwerking:** React Hook Form of native state
- **E-mailintegratie:** koppel aan bestaand CRM of gebruik Resend / Mailchimp API
- **Hosting:** Vercel of Netlify

---

## Wat dit project niet doet

- Vraagt **niet** om een bestaande polis of polisnummer
- Geeft **geen** bindende offerte — het is een schatting op basis van branchegemiddelden
- Vereist **geen** account of login om de berekening te zien
- Gebruikt **geen** cookies of tracking zonder toestemming (AVG-proof)

---

## Disclaimertekst (verplicht tonen onder resultaat)

> *"Deze berekening is een schatting op basis van gemiddelde marktdata per branche. De werkelijke besparing wordt duidelijk na een officiële offerteaanvraag. Aan deze berekening kunnen geen rechten worden ontleend."*

---

## Contactpersoon / eigenaar

Project: verzekerverzuim.nl  
Onderdeel van: du Gardijn Verzekeringen  
Doel: leadgeneratie via marketingcampagne "Je verzuimverzekering is geregeld. De premie waarschijnlijk niet."
