# Changelog

Il formato segue [Keep a Changelog](https://keepachangelog.com/it/1.1.0/).

## [1.2.0] — 2026-10-10

### Aggiunto
- **UTIC — farmaci in infusione e diluizioni** (nuova sezione): noradrenalina, adrenalina, dopamina,
  dobutamina, milrinone, levosimendan, nitroglicerina, isosorbide dinitrato, nitroprussiato,
  amiodarone, esmololo, landiololo, isoprenalina, eparina non frazionata, furosemide. Per ognuno:
  preparazione di esempio (quantità e volume modificabili) con concentrazione risultante,
  conversione dose → mL/h e mL/h → dose sul peso del paziente, tabella delle velocità, intervallo di
  dose dalle fonti citate (con evidenza delle dosi fuori intervallo), bolo, accesso venoso, avvertenze.
- **Calcolatore libero** per qualsiasi preparazione (mg o UI; mcg/kg/min, mcg/min, mg/h, UI/kg/h,
  UI/h), con caso di test.
- `data/infusions/` (15 preparazioni), incorporate da `tools/embed_data.py` e controllate da
  `validate_data.py` (unità, coerenza mg/UI, intervalli) ed `extract_data.py`.

### Modificato
- Service worker: cache `v4`.

## [1.1.0] — 2026-10-10

### Aggiunto
- **Mappa terapeutica** (nuova sezione): si selezionano le patologie del paziente e per ciascuna si
  apre una mappa concettuale espandibile delle terapie raccomandate, con classe di raccomandazione
  (I, IIa, IIb, III) e livello di evidenza (A, B, C) delle linee guida ESC citate. Le voci spuntate
  (con scelta della molecola) formano un riepilogo testuale copiabile e stampabile.
- **Avvisi su incongruenze e associazioni rischiose**: voci di classe III selezionate, 49 regole
  farmaco-farmaco e farmaco-patologia con fonte (es. ACE-i + ARNI, diltiazem/verapamil nell'HFrEF,
  bloccanti del nodo AV nella FA pre-eccitata, triplice antitrombotica, farmaci in gravidanza),
  doppioni di classe, interazioni delle sezioni 4.5 e controindicazioni delle schede che nominano le
  patologie scelte. Le associazioni raccomandate dalla stessa linea guida restano come note di
  monitoraggio.
- `data/recommendations/` (25 patologie, 250 raccomandazioni) e `data/rules/` (49 regole), in stato
  `source-review`: dove la classe non è certa la voce è marcata «classe non indicata».
- `tools/embed_data.py`: incorpora in `index.html` le due nuove cartelle; `validate_data.py` ed
  `extract_data.py` controllano anche questi dati. Le patologie senza classi mostrano nella mappa
  gli step del percorso e i farmaci collegati.

### Modificato
- Service worker: cache `v3`.

## [1.0.1] — 2026-09-28

Preparazione alla pubblicazione su GitHub Pages.

### Corretto
- **Schede di atorvastatina, pitavastatina e rosuvastatina non si aprivano**: il campo dei
  trasportatori era testo invece di elenco e il codice andava in errore. Il rendering ora accetta
  entrambi i formati (`asList()`), esteso a tutti i campi dello stesso tipo — compresi quelli
  usati dall'indice di ricerca, dove un errore avrebbe bloccato la ricerca dell'intera app.
  Verificato: 181 schede su 181 si aprono.

### Modificato
- **Caratteri tipografici ospitati nel repository** al posto di Google Fonts: l'app non contatta
  più alcun servizio esterno, funziona completamente offline e non comunica a terzi l'indirizzo IP
  di chi la consulta. Il service worker (cache `v2`) li mette in cache fin dalla prima visita.
- Rimossi i segnaposto `OWNER/REPO`: il repository si pubblica senza modifiche manuali.
- Guida di pubblicazione riscritta, con il percorso tramite GitHub Desktop (il caricamento dal
  browser è limitato a 100 file per volta).

### Aggiunto
- `404.html` che riporta all'atlante da qualunque indirizzo errato.

## [1.0.0] — 2026-08-04

Prima versione completa: contenuti clinici conclusi, in attesa di revisione clinica.

### Aggiunto
- **Simulazione terapeutica**: profilo del paziente (età, peso, creatinina con clearance
  Cockcroft-Gault calcolata in tempo reale, potassiemia, frazione d'eiezione, epatopatia e
  condizioni cliniche) da cui l'app estrae le voci pertinenti delle schede, riportate verbatim con
  la fonte, più le interazioni fra i farmaci scelti e il convertitore di infusione mcg/kg/min → mL/h.
- **Funzionamento offline**: manifest, service worker, icone; installabile come PWA.
- **Terapia per patologia completa**: 80 percorsi (72 protocolli a step + 8 disionie), nessuno vuoto.
- Schede-farmaco: 181 popolate su 186, fra cui antinfiammatori e immunomodulanti, terapie
  dell'amiloidosi e della cardiomiopatia ipertrofica, GLP-1 agonisti e antidiabetici,
  antibiotici per l'endocardite.
- Emivita compilata su tutte le schede popolate, con fonte citata; dove il valore numerico non è
  il parametro clinicamente rilevante è riportato il profilo farmacocinetico-farmacodinamico.
- Strumenti `tools/validate_data.py` e `tools/extract_data.py`; workflow di validazione e
  pubblicazione su GitHub Pages.
- Documentazione: architettura, politica di revisione clinica, avvertenze d'uso, contribuzione.

### Modificato
- Intestazione, piè di pagina e sezione Info aggiornati allo stato reale del progetto: non
  riportano più «Lotto 1 · Antitrombotici» e distinguono correttamente le schede validate dal
  curatore clinico da quelle in revisione fonti.
- Rifiniture di interfaccia: stati di focus accessibili, transizioni, ombra della barra allo
  scorrimento, rispetto di `prefers-reduced-motion`, fogli di stile per la stampa.

### Corretto
- Simulazione: separate le espressioni per iperkaliemia e ipokaliemia. Con potassio elevato
  comparivano anche le avvertenze sull'ipokaliemia (furosemide, acetazolamide, clortalidone):
  le segnalazioni per potassio > 5,0 mmol/L sono passate da 44 a 20 schede su 181.
- Motore delle interazioni: riconoscimento delle classi aggiunte (antinfiammatori, terapie
  dell'amiloidosi, inibitori della miosina, antidiabetici, antibiotici).
- Interazione ceftriaxone–calcio: reso esplicito il nome degli agenti, altrimenti la coppia non
  veniva rilevata.
- Rimosso un riferimento pendente a una molecola non presente nell'atlante (doxazosina).

### Noto
- 169 schede su 181 sono in stato `source-review`: **attendono la validazione clinica**.
- Le posologie hanno `approvalEvidence` interamente a `false`: non verificate su RCP ufficiale.
- Lo script generatore dell'HTML non fa parte del repository (perduto in un reset dell'ambiente):
  i contenuti vanno aggiornati sia in `data/` sia nell'oggetto `DATA` di `index.html`.
- 5 schede restano placeholder: abciximab, rilonacept, dalteparina, indometacina, immunoglobuline.
