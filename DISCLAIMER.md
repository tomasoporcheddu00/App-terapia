# Avvertenze d'uso

## Natura dello strumento

CardioTherapy Atlas è uno **strumento di consultazione e di supporto alla decisione**, rivolto a
professionisti sanitari. **Non è un dispositivo medico**, non è stato sottoposto a certificazione ai
sensi del Regolamento (UE) 2017/745 e non è destinato a essere impiegato come unico riferimento per
decisioni diagnostiche o terapeutiche.

## Non sostituisce le fonti ufficiali

Le informazioni contenute nell'applicazione derivano da riassunti delle caratteristiche del prodotto
(RCP), da documenti regolatori e da linee guida delle società scientifiche, **citati scheda per
scheda**. In caso di discrepanza, **prevalgono sempre**:

1. l'RCP ufficiale del medicinale, nella versione aggiornata pubblicata da AIFA o EMA;
2. le linee guida ufficiali nella loro versione integrale e aggiornata;
3. il giudizio clinico del professionista che ha in carico il paziente.

Una parte rilevante delle fonti utilizzate è costituita da **portali che riproducono l'RCP italiana**
(Torrinomedica, Codifa, Mediately, Univadis) e da sintesi delle linee guida: sono indicate come tali
nelle schede e **vanno confermate sulle fonti primarie**.

## Stato di revisione

Ogni scheda dichiara il proprio stato editoriale. Alla data di pubblicazione **12 schede su 181 sono
state validate dal curatore clinico**; le altre sono in stato *revisione fonti*, cioè derivano da
fonti citate ma **non hanno ancora ricevuto la validazione clinica**. Questa distinzione è visibile
nell'applicazione e va tenuta presente a ogni consultazione.

## Limiti specifici delle funzioni interattive

**Simulazione terapeutica.** Non genera dosi né raccomandazioni: confronta il profilo inserito con il
testo delle schede e riporta le voci che nominano le condizioni impostate, così come sono scritte
nella fonte. Ne conseguono due limiti: possono comparire voci non applicabili al singolo caso, e
possono mancare rischi reali non nominati con quei termini o non presenti nelle schede.
**L'assenza di segnalazioni non equivale a sicurezza.**

**Interazioni.** La verifica si basa sulle sezioni 4.5 sintetizzate nelle schede disponibili e non
sostituisce un database di interazioni completo. Molte segnalazioni sono a livello di classe.

**Calcolatori.** Sono deterministici e riportano la fonte della formula. Restano strumenti di
supporto: i valori vanno interpretati nel contesto clinico e confrontati con i riferimenti del
laboratorio e della singola RCP.

## Dosi e posologie

Gli schemi posologici riportano il campo `approvalEvidence` con tutti i valori a `false`: significa
che **non sono stati verificati sull'RCP ufficiale né validati clinicamente**. Vanno sempre
ricontrollati prima della prescrizione, con particolare attenzione a funzione renale ed epatica,
peso, età e interazioni.

## Trattamento dei dati

L'applicazione è interamente statica e funziona nel browser. **Non raccoglie, non salva e non
trasmette alcun dato**, compresi i valori inseriti nella sezione Simulazione e nei calcolatori, che
esistono solo per la durata della sessione e non lasciano il dispositivo. Non sono presenti sistemi
di analisi, tracciamento o pubblicità.

## Responsabilità

Il progetto è distribuito «così com'è», senza garanzie di completezza, accuratezza o adeguatezza a
uno scopo specifico. Gli autori e i contributori non rispondono di decisioni cliniche assunte sulla
base dei contenuti dell'applicazione. La responsabilità della prescrizione resta interamente del
professionista sanitario.

## Segnalazione di errori clinici

Gli errori clinici hanno priorità assoluta. Vanno segnalati aprendo una *issue* con il modello
«Segnalazione clinica», indicando la fonte corretta; se l'errore riguarda una dose, una
controindicazione o un'interazione, va segnalato come **urgente** nel titolo.
