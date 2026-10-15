# Architettura

## Principio

Applicazione **statica e autonoma**: nessun backend, nessuna dipendenza da servizi esterni a
runtime, nessuna chiamata di rete durante l'uso. L'intera applicazione — codice, stili e dati
clinici — è contenuta in `index.html`, che può essere aperto anche senza server.

Questa scelta ha tre conseguenze volute: l'app funziona in reparto senza connessione, non esiste un
canale attraverso cui possano uscire dati, e la distribuzione si riduce a servire un file statico.

## I due volti dei contenuti

I contenuti clinici esistono in due forme, che devono restare allineate:

| | `data/*.json` | `index.html` |
|---|---|---|
| Ruolo | fonte revisionabile | applicazione eseguibile |
| Uso | revisione clinica, diff di Git, controllo qualità | consultazione, pubblicazione |
| Formato | un file JSON per entità | oggetto `DATA` incorporato nello script |

**`data/` è la forma su cui si fa la revisione clinica**: una modifica a una controindicazione
produce una diff leggibile riga per riga, che è esattamente ciò che serve per validare o contestare
un contenuto. `index.html` è il prodotto consultabile.

### Stato del generatore

> [!WARNING]
> Lo script che generava `index.html` a partire da `data/` (`build_app2.py`) **non fa parte del
> repository**: è stato perduto in un reset dell'ambiente di sviluppo. I dati e l'applicazione sono
> integri e allineati, ma **al momento non esiste una pipeline automatica** che rigeneri l'HTML dai
> JSON.

Finché il generatore non viene ricostruito, valgono queste regole operative:

- **modifiche di contenuto**: vanno fatte sul JSON in `data/` **e** riportate nell'oggetto `DATA`
  incorporato in `index.html`, altrimenti le due forme divergono;
- **modifiche di interfaccia**: si applicano a `index.html` con script di sostituzione mirata
  (è il metodo con cui sono state realizzate le ultime rifiniture), validando sempre con
  `node --check` sullo script estratto;
- **controllo di allineamento**: `tools/extract_data.py` estrae `DATA` dall'HTML e lo confronta con
  `data/`, segnalando le divergenze.

Ricostruire il generatore è il primo intervento tecnico consigliato: renderebbe `data/` l'unica
fonte di verità e l'HTML un artefatto riproducibile.

## Struttura dei dati

### `data/drugs/<id>.json`
```
meta          id, stato editoriale, versione, fonti citate, note e limiti dichiarati
name          generico, INN, nomi commerciali italiani
identity      codici ATC, formulazioni, vie, stato di commercializzazione
quickSummary  che cos'è, usi principali, rischi principali, monitoraggio essenziale
clinical      indicazioni autorizzate vs da linee guida, controindicazioni assolute e relative,
              avvertenze, effetti avversi, sovradosaggio, antidoti, popolazioni speciali
deep          spiegazione semplice/clinica/molecolare, bersaglio, farmacodinamica,
              farmacocinetica (emivita compilata su tutte le schede popolate), bibliografia
```

`clinical.specialPopulations` usa chiavi fisse (`renal`, `hepatic`, `elderly`, `pregnancy`,
`breastfeeding`, `lowBodyWeight`, `obesity`, `transplant`): **sono i campi su cui lavora la
Simulazione**, ed è la ragione per cui quella funzione non deve indovinare nulla.

### Altre cartelle
- `data/classes/<id>.json` — meccanismo, bersaglio, effetti di classe, controindicazioni condivise,
  monitoraggio, note su classe vs singola molecola, `memberDrugIds`.
- `data/dosing/<farmaco>__<chiave>__<via>.json` — uno schema per indicazione e via. Il blocco
  `approvalEvidence` ha tutti i valori a `false`: **nessuna posologia è verificata su RCP ufficiale**.
- `data/interactions/<farmaco>.json` — voci con `severity` (`contraindicated`, `major`, `moderate`,
  `minor`), `agent`, `effect`, `management`.
- `data/regulatory/<farmaco>.json` — classe di rimborsabilità, regime di fornitura, piano
  terapeutico, legge 648/96, restrizioni prescrittive.
- `data/recommendations/<patologia>.json` — raccomandazioni della Mappa terapeutica, raggruppate
  per tema: testo, classe (`cor`: I, IIa, IIb, III o `null`), livello di evidenza (`loe`), molecole
  selezionabili (`drugIds`), nota e fonte facoltative. Lo slug coincide con quello della patologia.
- `data/rules/combination-rules.json` — regole di associazione: ciascuna ha una gravità, un elenco
  `all` di condizioni (`classes`, `drugs` o `pathologies`) che devono essere soddisfatte da entità
  distinte, un messaggio, la gestione e la fonte.

- `data/infusions/<id>.json` — preparazioni della sezione UTIC: farmaco, categoria, ordine,
  preparazione (`amount` in mg o UI, `volume` in mL, diluente, contenitore), dose (`unit` fra
  mcg/kg/min, mcg/min, mg/h, UI/kg/h, UI/h; `min`, `max`, `steps`, testo dell'intervallo), bolo,
  accesso, note, avvertenze e fonti.

- `data/organ-function/<farmaco>.json` — soglie renali ed epatiche: `renal.metric` (CrCl o eGFR),
  `renal.bands` (fasce contigue `from` ≤ valore < `to`, con `status`, `text`, `verified`),
  `renal.dialysis`, `hepatic.A/B/C` (Child-Pugh) e fonti con data di revisione.

- `data/regimens/<id>.json` — schemi posologici: patologie collegate, contesto, righe (farmaco,
  ruolo, dose, durata, scalo, calcolo sul peso `threshold` o `perkg`, nota, `verified`), tabella di
  scalo facoltativa e fonti.

Queste cinque cartelle si incorporano in `index.html` con `python3 tools/embed_data.py`, che riscrive
solo le chiavi `DATA.recommendations`, `DATA.rules`, `DATA.infusions`, `DATA.organ` e `DATA.regimens`.

## Come funzionano le sezioni interattive

**Interazioni** (`ixHits`, `ixPairs`). Per ogni coppia si cercano le voci della sezione 4.5 il cui
campo `agent` nomina l'altro farmaco. Il match sul **nome specifico ha priorità**; i sinonimi di
classe (mappa `IXSYN`) si usano solo se nessuna voce nomina la molecola. Serve a evitare falsi
positivi come «cangrelor + ticagrelor» che scattavano per sinonimo di classe.

**Simulazione** (`ptConds`, `ptAnalyse`). Il profilo del paziente genera un elenco di condizioni
attive, ciascuna con un'etichetta, una gravità e un'espressione regolare. Per ogni farmaco:

1. i campi `specialPopulations` corrispondenti alla condizione vengono mostrati **direttamente**
   (sono già etichettati: nessuna inferenza);
2. controindicazioni e avvertenze vengono filtrate con l'espressione regolare della condizione e
   riportate **verbatim**, con l'indicazione del campo di provenienza.

Le espressioni distinguono i casi speculari: `iperkaliemi|iperpotassiem|sali di potassio|...` per il
potassio alto e `ipokaliemi|ipopotassiem|...` per quello basso — senza questa separazione, un
paziente iperkaliemico vedeva comparire le avvertenze sull'ipokaliemia di furosemide e acetazolamide.

**Mappa terapeutica** (`mapGroups`, `mapAlerts`). Per ogni patologia scelta si usano le
raccomandazioni di `data/recommendations`; se mancano, gli step del percorso e i farmaci collegati,
senza classe. Gli avvisi nascono da cinque fonti, tutte deterministiche: voci di classe III
selezionate; regole di `data/rules`; doppioni nella stessa classe; interazioni delle sezioni 4.5
(non ripetute se una regola copre già la coppia, e declassate a nota se entrambi i farmaci sono
raccomandati per la stessa patologia); controindicazioni assolute delle schede che nominano le
patologie scelte (mappa `MAPRX`). Quando una voce offre più molecole, la scelta predefinita riusa
quella già presente nella terapia, per evitare doppioni involontari tra patologie.

**UTIC** (`utRate`, `utDoseOf`). Conversione aritmetica fra dose e velocità: con la concentrazione
C = quantità/volume, mL/h = dose·peso·60/C per mcg/kg/min, dose·60/C per mcg/min, dose/C per mg/h e
UI/h, dose·peso/C per UI/kg/h (C in mcg/mL per le unità in mcg). Le preparazioni sono esempi: i
valori inseriti dall'utente restano in memoria solo finché la pagina è aperta.

**Calcolatori.** Formule pubblicate con citazione, calcolate nel browser: Cockcroft-Gault,
CHA₂DS₂-VA, HAS-BLED, QTc.

## Interfaccia

HTML e CSS scritti a mano, senza framework. Variabili CSS in `:root` per la palette; schema chiaro
forzato (`color-scheme: light only`) perché la modalità scura del browser invertiva i colori
rendendo illeggibili le schede su alcuni dispositivi. Layout adattivo con soglia a 900 px e
attributo `data-device` sul `body`. Fogli di stile per la stampa: nascondono barra e navigazione ed
evitano che le schede si spezzino tra le pagine.

## Caratteri tipografici

Space Grotesk, IBM Plex Sans e IBM Plex Mono sono **ospitati in `assets/fonts/`** (formato woff2,
sottoinsiemi latin e latin-ext, licenza SIL Open Font License 1.1 inclusa) e dichiarati con
`@font-face` all'inizio del foglio di stile. In precedenza erano caricati da Google Fonts: era
l'unica chiamata esterna dell'app, non funzionava offline e comunicava a Google l'indirizzo IP di
ogni consultazione. I caratteri non coperti dai sottoinsiemi (per esempio ≥, →, ₂) vengono resi
dal carattere di sistema, glifo per glifo.

## Robustezza del rendering

I campi delle schede possono contenere un elenco oppure un testo libero (per esempio
`pharmacokinetics.transporters`). La funzione `asList()` accetta entrambi i formati: una scheda
non deve mai smettere di aprirsi per un campo scritto in un formato diverso da quello atteso. Il
problema si era presentato davvero su tre statine, le cui schede risultavano vuote.

## PWA e funzionamento offline

`manifest.webmanifest` descrive l'installazione; `sw.js` è un service worker con strategia
**cache-first sull'app** e aggiornamento in background. Alla prima visita l'applicazione viene messa
in cache: da quel momento funziona senza connessione. Il service worker usa percorsi relativi, così
funziona anche su una *project page* di GitHub Pages servita da una sottocartella.

La lista `CORE` di `sw.js` comprende anche i caratteri tipografici, così l'app è completa offline
fin dalla prima visita. Per forzare l'aggiornamento dopo una modifica: incrementare `CACHE_NAME`.

## Strumenti

- `tools/validate_data.py` — controlla che i JSON siano validi, che i riferimenti incrociati
  esistano, che gli stati editoriali siano coerenti e che ogni scheda popolata abbia almeno una
  fonte. Da eseguire prima di ogni commit sui contenuti.
- `tools/extract_data.py` — estrae `DATA` da `index.html` e verifica l'allineamento con `data/`.
