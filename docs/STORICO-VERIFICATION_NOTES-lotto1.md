# VERIFICATION_NOTES — Lotto 1

Mappatura campo -> fonte e conflitti/decisioni. Verifica: 18/07/2026. Revisore clinico/regolatorio: NON ancora eseguita.

## Regola applicata
Ogni campo clinico deriva da una RCP/PI recuperata o da una fonte regolatoria/linea guida citata nel record.
Dove la fonte non copriva un campo, il valore e' null e la lacuna e' in MISSING.md. Nessun campo e' "approved".

## Note per farmaco (campo -> fonte)
- **apixaban**: indicazioni/posologia/controindicazioni/PK -> SmPC Eliquis (emc). ATC dalla SmPC. Regolatorio (Nota 97, abrogazione scheda 09/07/2026) -> AIFA.
- **acenocoumarol**: indicazione, controindicazioni, CYP2C9/2C19/3A4, gravidanza -> RCP Sintrom. Target INR FA -> ESC 2024. ATC -> WHO (flag).
- **aspirin**: indicazioni cardio, controindicazioni, gravidanza (3 trim >100 mg) -> RCP Cardioaspirin. Meccanismo COX-1 -> RCP. Regime RR -> scheda codifa.
- **clopidogrel**: posologia 75 mg + carico 300 mg, CYP2C19, PTT/emofilia acquisita, ictus <7 gg -> RCP Plavix + PI EMA. Indicazioni verbatim: standard EMA (flag).
- **dabigatran**: 150/110 mg, CrCl, idarucizumab, HIT-non applicabile, >=80 anni -> RCP Pradaxa. Nota 97 -> AIFA.
- **edoxaban**: 60/30 mg, criteri riduzione (CrCl 15-50, peso <=60 kg, P-gp), ESRD non racc., assenza antidoto -> RCP Lixiana. Nota 97 -> AIFA.
- **enoxaparin**: 1 mg = 100 UI, indicazioni, CrCl 15-30, controindicazioni HIT/IM, protamina -> RCP Clexane + NII AIFA 2017. Dose NSTEMI 1 mg/kg q12h -> RCP (pharmamedix).
- **prasugrel**: indicazione ACS+PCI, carico 60/mant. 10, 5 mg se <60 kg o >=75, CI ictus/TIA/Child C -> RCP Efient/generici.
- **rivaroxaban**: FANV 20/15 mg, TVP/EP schema, dose 2,5 mg vascolare, con il cibo, CrCl -> RCP Xarelto + Registro CE. Antidoto non nominato (flag).
- **ticagrelor**: ACS 180->90 mg x2, post-IM 60 mg x2, dispnea, ENT-1/adenosina, CABG >=96 h -> RCP Brilique. PT+PHT -> Det. AIFA 22/05/2017 (medisoc).
- **unfractionated-heparin**: meccanismo anti-IIa/anti-Xa, aPTT, controindicazioni, HIT (<100.000/mm3), protamina, no IM -> RCP Eparina Sodica. Nomogramma numerico assente (flag).
- **warfarin**: indicazioni (TVP/EP, FA, protesi, post-IM), CYP2C9/VKORC1, enantiomeri S/R, gravidanza (embriopatia), fitomenadione -> RCP Coumadin. Target INR FA -> ESC 2024.

## Conflitti / decisioni
1. **Andexanet alfa (anti-Xa reversal)**: non nominato nelle SmPC recuperate di apixaban/rivaroxaban/edoxaban -> antidoteDrugIds lasciato vuoto (non inventato). Da aggiungere quando reperita la sezione 4.9 aggiornata.
2. **Nota 97 - abrogazione scheda 09/07/2026**: evento successivo al training; recepito SOLO dalla fonte AIFA citata. therapeuticPlan impostato a false per i DOAC/VKA in FANV di conseguenza.
3. **Preferenza DOAC vs VKA (ESC 2024)**: espressa come raccomandazione di CLASSE, non attribuita alla singola molecola.
4. **Fonti "portale" vs RCP ufficiale**: codifa/torrinomedica/mediately riproducono la RCP AIFA; usate come proxy. Il revisore deve validare sulla RCP/EPAR ufficiale (flag in ogni record).
5. **ATC VKA (acenocumarolo B01AA07, warfarin B01AA03)**: da classificazione WHO, non dallo snippet -> flag.
