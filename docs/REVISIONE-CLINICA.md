# Revisione clinica

Il progetto è completo sul piano dei contenuti: 181 schede popolate, 75 pagine di classe, 80
percorsi terapeutici. **Non è completo sul piano della validazione**: 12 schede su 181 sono state
approvate dal curatore clinico. Questo documento descrive come chiudere quel divario.

## Gli stati editoriali

| Stato | Significato |
|---|---|
| `placeholder` | Voce presente in elenco, contenuto non compilato |
| `source-review` | Compilata da fonti citate, **in attesa di validazione clinica** |
| `clinician-approved` | Contenuto verificato e approvato dal curatore clinico |

Lo stato è dichiarato in `meta.editorialStatus` di ogni file ed è visibile nell'applicazione. Non
esiste uno stato intermedio: una scheda o è stata riletta da un clinico oppure no.

## Chi approva

L'approvazione è un atto clinico e spetta al **curatore clinico del progetto**, che se ne assume la
responsabilità. Non può essere delegata a chi ha compilato la scheda né automatizzata.

## Che cosa verificare, in ordine di rischio

L'ordine non è casuale: riflette il danno potenziale di un errore.

1. **Posologie** — è il campo più pericoloso. Ogni schema in `data/dosing/` va confrontato con
   l'RCP ufficiale; alla verifica si aggiornano i flag in `approvalEvidence`. Attenzione
   particolare ai farmaci a indice terapeutico stretto (digossina, amiodarone, colchicina,
   teofillina, aminoglicosidi, vancomicina) e agli aggiustamenti per funzione renale.
2. **Controindicazioni assolute** — una controindicazione mancante è un errore silenzioso: non
   produce un avviso sbagliato, produce l'assenza di un avviso.
3. **Interazioni** — verificare che gravità e gestione corrispondano alla sezione 4.5, e che il
   campo `agent` sia formulato in modo che il motore lo riconosca (vedi sotto).
4. **Indicazioni** — controllare che la separazione fra autorizzate e da linee guida sia corretta,
   e che l'off-label sia dichiarato dove esiste.
5. **Popolazioni speciali** — sono i campi su cui lavora la Simulazione: un errore qui si propaga.
6. **Regolatorio** — classe di rimborsabilità, regime di fornitura, piano terapeutico, nota AIFA.
   È la parte che invecchia più in fretta.
7. **Farmacocinetica e testo descrittivo** — importanti ma a rischio clinico inferiore.

## Ordine consigliato dei lotti

Conviene procedere per classi omogenee e partire da ciò che si usa quotidianamente, perché la
revisione è più rapida e il beneficio immediato:

1. antitrombotici (già approvati: sono i 12 esistenti) — usarli come riferimento di stile;
2. scompenso: ARNI, betabloccanti, MRA, SGLT2-inibitori, diuretici;
3. antiaritmici e farmaci dell'urgenza (UTIC), dove l'errore ha le conseguenze più rapide;
4. antipertensivi e ipolipemizzanti;
5. classi specialistiche: ipertensione polmonare, amiloidosi e cardiomiopatia ipertrofica,
   antibiotici per l'endocardite;
6. percorsi in *Terapia per patologia*, verificando le raccomandazioni contro le linee guida citate.

## Procedura per una scheda

1. aprire il file in `data/drugs/<id>.json` accanto all'RCP ufficiale;
2. verificare i campi nell'ordine di rischio sopra;
3. correggere ciò che serve **citando la fonte** in `meta.sources`;
4. se la scheda è corretta e completa, portare `meta.editorialStatus` a `clinician-approved` e
   valorizzare `clinicalReviewer` e `clinicalReviewDate`;
5. riportare le stesse modifiche nell'oggetto `DATA` dentro `index.html` (finché il generatore non
   è ricostruito — vedi [ARCHITETTURA.md](ARCHITETTURA.md));
6. eseguire `python3 tools/validate_data.py`;
7. un commit per scheda o per lotto omogeneo, con messaggio del tipo
   `revisione clinica: bisoprololo → clinician-approved`.

## Regole da non violare

- **Meglio un campo vuoto che un campo inventato.** Se la fonte non copre un dato, il campo resta
  vuoto: non si completa per analogia con molecole della stessa classe.
- **Nessuna dose senza fonte.** Vale anche per le dosi «ovvie».
- **Distinguere autorizzato da raccomandato.** Un'indicazione da linee guida non diventa
  autorizzata perché è pratica diffusa.
- **Dichiarare l'incertezza.** Dove l'evidenza è discordante va riportata come tale, non risolta
  scegliendo il lato che piace di più.
- **Verificare la versione della linea guida** prima di aggiornare un percorso: durante la stesura
  sono emersi documenti più recenti di quelli attesi (valvulopatie 2025, miocardite e pericardite
  2025, dislipidemie 2025, embolia polmonare AHA/ACC 2026).

## Nota sul campo `agent` delle interazioni

Il motore confronta il testo di `agent` con i nomi del farmaco e con i sinonimi di classe. Se una
voce nomina un farmaco in modo troppo generico l'interazione non viene rilevata. È il motivo per cui
la voce del ceftriaxone è stata riscritta come «Soluzioni endovenose contenenti calcio (calcio
gluconato, calcio cloruro)»: senza i nomi espliciti la coppia non compariva. Quando si aggiunge o si
corregge un'interazione, verificarne il funzionamento nella sezione Interazioni dell'app.
