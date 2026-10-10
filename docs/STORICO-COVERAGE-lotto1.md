# COVERAGE — Lotto 1 (stato di completamento)

Aggiornato: 18/07/2026. Legenda: [x] presente e validato JSON · (parziale) = presente con lacune note in MISSING.md

## Farmaci (drugs/) — 12/12
[x] acenocoumarol  [x] apixaban  [x] aspirin (parziale: solo dose antiaggregante)
[x] clopidogrel  [x] dabigatran  [x] edoxaban  [x] enoxaparin
[x] prasugrel  [x] rivaroxaban  [x] ticagrelor  [x] unfractionated-heparin  [x] warfarin

## Regulatory (regulatory/) — 12/12
[x] uno per ciascun farmaco (editorialStatus = regulatory-review)

## Dosing (dosing/) — 19 file (scenari multipli per i farmaci multi-indicazione)
[x] apixaban (FANV) · acenocoumarol (tromboembolismo) · aspirin (prev. secondaria) ·
    clopidogrel (SCA) · dabigatran (FANV) · edoxaban (FANV) · enoxaparin (NSTEMI) ·
    prasugrel (SCA-PCI) · rivaroxaban (FANV) · ticagrelor (SCA) · UFH (anticoag. EV) · warfarin (anticoag. orale)
    Aggiunti: apixaban (TEV) · enoxaparina (STEMI, TVP/EP, profilassi) · rivaroxaban (TEV, dose vascolare 2,5 mg) · ticagrelor (60 mg post-IM).

## Classi (classes/) — 7/7 (con meccanismi d'azione)
[x] vitamin-k-antagonists  [x] factor-xa-inhibitors  [x] direct-thrombin-inhibitors
[x] low-molecular-weight-heparins  [x] unfractionated-heparins
[x] antiplatelets-cox-inhibitors  [x] p2y12-inhibitors

## Interazioni (interactions/) — 12/12
[x] una scheda per farmaco: sintesi delle interazioni principali dalle sez. 4.5 delle RCP (revisione 4.5 completa pendente).

## Log
[x] SOURCES_LOG.md  [x] MISSING.md  [x] VERIFICATION_NOTES.md  [x] COVERAGE.md

## NON incluso (fuori dal Lotto 1)
- interactions/ (interazioni farmacologiche) e pathologies/ (macro-aree cliniche)
- record "reversal agents" (idarucizumab, protamina, fitomenadione, andexanet alfa)
- verifica AIC/classe/regime per confezione su banca dati AIFA
- revisione clinica e regolatoria umana (obbligatoria prima di qualsiasi uso)
