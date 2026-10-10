# MISSING — Lotto 1 (lacune e verifiche da completare)

Principio guida rispettato: "meglio un campo vuoto che un campo inventato". Ogni farmaco ha
editorialStatus = source-review (i regulatory = regulatory-review): NESSUN contenuto e'
"approved". Sotto, le lacune trasversali e quelle specifiche.

## Trasversali (tutti i farmaci)
- **AIC per confezione**: non inseriti (nessun codice AIC verificato sulla banca dati AIFA). Da recuperare per ogni confezione su https://www.aifa.gov.it (banca dati farmaci) o AIC lookup.
- **Classe di rimborsabilita' e regime di fornitura per confezione**: inseriti a livello indicativo (es. classe A, RR) dove desumibile; da confermare puntualmente su AIFA per ogni confezione/indicazione.
- **Indicazioni autorizzate (sez. 4.1) verbatim**: per i farmaci centralizzati il testo e' standard UE ma va confrontato con la RCP integrale ufficiale (spesso ho usato portali che riproducono la RCP).
- **classIds / linkedMacroAreaIds / indication id nei file dosing**: usano slug proposti (es. "atrial-fibrillation", "nvaf-stroke-prevention"); da riconciliare con il vocabolario controllato del progetto (pathologies/ e tassonomia classi).
- **Schema dei file /classes/**: non era definito nei template forniti. Ho proposto una struttura (mechanismSummary, molecularTarget, memberDrugIds, ecc.): da validare/riscrivere secondo lo schema ufficiale.
- **Cartelle /interactions/ e /pathologies/**: non popolate in questo lotto (non richieste per il Lotto 1). Le interazioni sono numerose (soprattutto VKA, DOAC via CYP3A4/P-gp, P2Y12) e meritano file dedicati.
- **evidenceIds / recommendationIds**: lasciati vuoti; i trial cardine sono citati in bibliography come stringhe, non come record collegati.
- **Tutti i file dosing**: primarySourceVerified = false (verificata la RCP, NON il paper del trial). clinicalReviewDone = false ovunque.

## Specifiche per farmaco
- **acenocoumarol / warfarin**: ATC (B01AA07 / B01AA03) da classificazione WHO; dose e' INR-guidata (nessuna dose fissa nella RCP). Target INR per protesi valvolari meccaniche NON specificato (dipende da tipo/posizione: da linee guida valvole). Emivita acenocumarolo non estratta.
- **aspirin**: monografia limitata alla dose antiaggregante; alcune controindicazioni troncate nello snippet (grave insufficienza cardiaca, metotressato >=15 mg/sett): confermare su RCP integrale. Dose di carico in SCA e schemi DAPT da linee guida (non da RCP).
- **clopidogrel**: dose di carico 600 mg in alcuni contesti PCI = da linee guida (RCP riporta 300 mg). Indicazioni 4.1 verbatim da confermare. Stato PT storico da verificare.
- **dabigatran**: soglie posologiche fini (eta' 75-80, verapamil, gastrite) verificate su fonte spagnola/torrinomedica: confermare su RCP IT integrale. TVP/EP: fase parenterale iniziale.
- **edoxaban**: assenza di antidoto specifico confermata. CrCl elevata: possibile minore efficacia (avvertenza importante) inserita.
- **enoxaparin**: creato solo il dosing NSTEMI. Mancano i file dosing per STEMI (bolo EV 30 mg + 1 mg/kg; anziani >=75 senza bolo, 0,75 mg/kg q12h), trattamento TVP/EP (1,5 mg/kg/die o 1 mg/kg q12h) e profilassi (20/40 mg/die). Elenco AIC delle molte confezioni assente.
- **prasugrel**: therapeuticPlan = null (non determinato); verificare eventuale PT/registro AIFA per P2Y12 nelle SCA.
- **rivaroxaban**: creato solo il dosing FANV. Mancano dosing per TVP/EP (15 mg x2 3 sett -> 20 mg), dose vascolare 2,5 mg x2 con ASA (SCA/CAD/PAD), profilassi 10 mg. Antidoto (andexanet alfa) non nominato nella fonte: antidoteDrugIds lasciato vuoto. Materiale educazionale/patient card: stato da verificare.
- **ticagrelor**: controindicazioni 4.3 = standard Brilique, da confermare sul testo integrale. PT + PHT confermati da fonte (Det. AIFA 22/05/2017): verificare aggiornamenti. Manca il file dosing 60 mg (post-IM prolungato).
- **unfractionated-heparin**: nomogramma posologico peso-basato (bolo + infusione, valori numerici) NON inserito: da RCP/protocollo locale/linee guida. Classe/regime (uso ospedaliero) da confermare. Esiste anche eparina calcica (SC) non trattata.

## Antidoti (record collegati da creare in un lotto "reversal agents")
Citati come antidoteDrugIds: **idarucizumab** (dabigatran), **protamine** (enoxaparina, UFH),
**phytomenadione**/vitamina K1 (warfarin, acenocumarolo). Per apixaban/rivaroxaban/edoxaban
l'agente anti-Xa (andexanet alfa) NON e' stato inserito perche' non nominato nelle fonti recuperate.

## Aggiornamento 18/07/2026 — ampliamento contenuti
- Aggiunti 7 nuovi file dosing (apixaban TEV; enoxaparina STEMI/TVP-EP/profilassi; rivaroxaban TEV/vascolare; ticagrelor 60 mg) dalle stesse RCP gia' citate.
- Creata cartella interactions/ con 12 schede: sono una SINTESI delle interazioni principali coerente con PK/controindicazioni gia' documentate. La revisione COMPLETA della sezione 4.5 (tutti i singoli farmaci, quantificazione) resta DA FARE su ogni RCP integrale.
- I calcolatori dell'app (Cockcroft-Gault, CHA2DS2-VA, HAS-BLED, QTc) sono strumenti deterministici con fonte citata e casi di test; non sostituiscono il giudizio clinico.
