# Come contribuire

Grazie dell'interesse. Questo progetto ha una particolarità che ne condiziona ogni regola: i suoi
contenuti possono influenzare decisioni terapeutiche. Le regole che seguono servono a questo.

## La regola non negoziabile

> **Meglio un campo vuoto che un campo inventato.**

Ogni campo clinico deve derivare da una fonte citata nella scheda stessa: RCP, documento
regolatorio o linea guida. Se la fonte non copre un dato, il campo resta vuoto. Non si completa
per analogia con altre molecole della stessa classe, per quanto la deduzione sembri sicura.

Non sono accettati contributi clinici senza fonte, nemmeno quando l'informazione è di dominio
comune.

## Segnalare un errore clinico

È il contributo più utile. Apri una *issue* con il modello **«Segnalazione clinica»**: servono la
scheda interessata, il campo, il testo attuale, la formulazione corretta e **la fonte**. Se
l'errore riguarda una dose, una controindicazione o un'interazione, scrivi `URGENTE` nel titolo.

## Proporre una modifica

1. apri una *issue* prima di lavorare su modifiche estese, per evitare doppioni;
2. modifica il JSON in `data/` **e** l'oggetto `DATA` dentro `index.html` — finché il generatore
   non è ricostruito le due forme vanno tenute allineate a mano
   (vedi [docs/ARCHITETTURA.md](docs/ARCHITETTURA.md));
3. esegui i controlli:
   ```bash
   python3 tools/validate_data.py     # contenuti
   python3 tools/extract_data.py      # allineamento app ↔ data/
   ```
4. se hai toccato il JavaScript, validalo (`node --check` sullo script estratto);
5. apri la *pull request* compilando il modello.

## Regole di redazione dei contenuti

- **Distinguere autorizzato da raccomandato.** Le indicazioni da RCP vanno in
  `authorisedIndications`, quelle da linee guida in `guidelineIndications`. L'uso off-label va
  dichiarato esplicitamente nel testo.
- **Citare la fonte con precisione**: RCP con nome commerciale e data, linea guida con anno e
  sezione o numero di tabella.
- **Non riprodurre verbatim** porzioni estese di RCP o linee guida: si sintetizza e si parafrasa,
  citando. È una questione di diritto d'autore oltre che di leggibilità.
- **Verificare la versione della linea guida** prima di aggiornare un percorso: durante la stesura
  sono emersi documenti più recenti di quelli attesi.
- **Dichiarare l'incertezza.** Dove l'evidenza è discordante va riportata come tale.
- **Italiano**, virgola decimale, unità come nell'RCP.
- Lo stato editoriale di una scheda modificata resta `source-review`: solo il curatore clinico può
  portarlo a `clinician-approved` (vedi [docs/REVISIONE-CLINICA.md](docs/REVISIONE-CLINICA.md)).

## Contributi tecnici

Interfaccia e strumenti sono benvenuti. Due vincoli architetturali:

- **nessuna dipendenza a runtime**: niente framework, CDN o chiamate di rete durante l'uso;
- **nessuna raccolta di dati**: nessun tracciamento, nessuna persistenza dei valori inseriti.

## Che cosa non verrà accettato

- contenuti clinici senza fonte, o con fonte generica («da letteratura»);
- funzioni che generano dosi o raccomandazioni terapeutiche in modo automatico: lo strumento
  seleziona e mostra ciò che le fonti dicono, non decide;
- integrazioni che inviano dati a servizi esterni;
- pubblicità, analisi del traffico, profilazione.
