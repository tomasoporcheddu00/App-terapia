## Che cosa cambia

<!-- Descrizione sintetica. Se la modifica tocca contenuti clinici, indica quali schede. -->

## Tipo

- [ ] Contenuto clinico (schede, percorsi, interazioni, posologie)
- [ ] Revisione clinica (passaggio a `clinician-approved`)
- [ ] Interfaccia o funzionalità
- [ ] Documentazione
- [ ] Strumenti o automazione

## Controlli

- [ ] `python3 tools/validate_data.py` non riporta errori
- [ ] `python3 tools/extract_data.py` conferma l'allineamento fra `index.html` e `data/`
- [ ] Se ho toccato i contenuti, ho aggiornato **sia** `data/` **sia** l'oggetto `DATA` in `index.html`
- [ ] Se ho toccato il JavaScript, ho validato con `node --check`

## Fonti

<!-- Obbligatorie per ogni modifica clinica: RCP con versione, linea guida con anno e sezione. -->

## Dichiarazione

- [ ] Non ho inserito alcun campo clinico privo di fonte citata
- [ ] Non ho riprodotto verbatim porzioni estese di RCP o linee guida
