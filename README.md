# CardioTherapy Atlas

**Assistente farmacologico-terapeutico cardiovascolare, evidence-based, per professionisti sanitari.**
Applicazione web statica, installabile e utilizzabile offline: nessun backend, nessun account, nessun dato paziente.

**App online:** <https://tomasoporcheddu00.github.io/App-terapia/>

> [!WARNING]
> **Strumento di supporto alla decisione, non un dispositivo medico.** Non sostituisce il giudizio
> clinico, il riassunto delle caratteristiche del prodotto (RCP) né le linee guida ufficiali.
> La maggior parte delle schede è in stato *revisione fonti* e **attende la validazione clinica**.
> Leggere [DISCLAIMER.md](DISCLAIMER.md) prima dell'uso.

---

## Cosa contiene

| Contenuto | Quantità |
|---|---|
| Schede-farmaco con fonte citata | **181** (12 validate dal curatore clinico) |
| Pagine di classe con meccanismo d'azione | **75** |
| Percorsi in *Terapia per patologia* | **80** (72 protocolli a step + 8 disionie) |
| Schemi posologici | **228** |
| Schede di interazioni (sez. 4.5) | **180** |
| Record regolatori italiani | **181** |

### Le undici sezioni

- **Farmaci** — monografie: indicazioni autorizzate e da linee guida, controindicazioni,
  avvertenze, effetti avversi, sovradosaggio e antidoto, popolazioni speciali, farmacocinetica
  (compresa l'emivita, completata su tutte le schede), posologie e regime prescrittivo italiano.
- **Terapia per patologia** — 80 percorsi terapeutici a step con le raccomandazioni delle linee
  guida citate: cardiopatia ischemica, scompenso, aritmie, ipertensione, disionie, malattie
  strutturali, tromboembolismo, prevenzione, circolo polmonare, popolazioni speciali.
- **Mappa terapeutica** — si selezionano le patologie del paziente e per ognuna si apre una mappa
  concettuale delle terapie raccomandate, con **classe di raccomandazione e livello di evidenza**
  (26 patologie, 264 raccomandazioni; scompenso aggiornato alla ESC 2026, embolia polmonare con AHA/ACC 2026); le voci spuntate formano un riepilogo testuale e l'app
  segnala incongruenze e associazioni rischiose (49 regole farmaco-farmaco e farmaco-patologia,
  doppioni di classe, interazioni, controindicazioni delle schede).
- **Simulazione** — profilo del paziente → voci pertinenti delle schede (vedi sotto).
- **Confronto** — fino a sei farmaci affiancati per colonne su attributi omogenei.
- **Interazioni** — «pinboard»: si aggiungono i farmaci del paziente e l'app confronta ogni coppia.
- **Calcolatori** — Cockcroft-Gault, CHA₂DS₂-VA, HAS-BLED, QTc: deterministici e con fonte citata.
- **UTIC** — 15 farmaci in infusione (vasopressori, inotropi, vasodilatatori, antiaritmici, eparina,
  furosemide) con preparazione di esempio modificabile, conversione dose ↔ mL/h sul peso, tabella
  delle velocità, boli, accesso venoso e avvertenze; calcolatore libero per qualsiasi preparazione.
- **Rene e fegato** — soglie strutturate di funzione renale (CrCl Cockcroft-Gault o eGFR CKD-EPI
  2021, secondo la RCP di ciascun farmaco) e di funzione epatica (Child-Pugh, con calcolatore) per
  35 farmaci: gliflozine, anticoagulanti orali e parenterali, antiaggreganti, farmaci dello scompenso,
  antiaritmici, ipolipemizzanti, metformina. Tabella immediata «controindicato / non raccomandato /
  adeguare la dose» per i valori del paziente; le stesse soglie compaiono nella scheda del farmaco,
  nella Simulazione e negli avvisi della Mappa.
- **Classi** — meccanismo, effetti di classe, controindicazioni condivise, monitoraggio.
- **Info** — metodo, copertura e limiti dichiarati.

---

## La regola che governa tutto il progetto

> **Meglio un campo vuoto che un campo inventato.**

Ogni campo clinico deriva da una RCP o da una linea guida **citata nella scheda stessa**. Dove la
fonte non copre un dato, il campo resta «non disponibile» invece di essere completato per analogia.
Da questa regola discendono alcune scelte visibili nell'app:

- le **indicazioni autorizzate** (da RCP italiana) sono separate da quelle **da linee guida**, e
  l'impiego off-label è dichiarato — per esempio la colchicina nella pericardite;
- dove una molecola non è disponibile in Italia la scheda lo dice e resta volutamente parziale
  (aficamten, approvato in UE nel febbraio 2026, ne è l'esempio);
- dove l'evidenza è discordante viene riportata come tale: la scheda sul rischio infiammatorio
  residuo espone sia COLCOT e LoDoCo2 sia il risultato neutro di CLEAR SYNERGY;
- dove l'emivita numerica non è il parametro clinicamente utile (antidoti, siRNA, proteine di
  fusione) è riportato il profilo farmacocinetico-farmacodinamico onesto invece di un numero.

---

## La sezione Simulazione

Si inserisce il profilo del paziente — sesso, età, peso, creatinina (con clearance calcolata in
tempo reale secondo Cockcroft-Gault), potassiemia, frazione d'eiezione, grado di epatopatia e le
condizioni cliniche rilevanti — e la terapia che si sta considerando.

**Che cosa fa:** confronta il profilo con il testo delle schede e riporta **verbatim** le voci
pertinenti — i paragrafi sulle popolazioni speciali e le controindicazioni o avvertenze che
nominano le condizioni impostate — indicando per ciascuna la fonte. Mostra inoltre le interazioni
fra i farmaci scelti e converte le infusioni da mcg/kg/min a mL/h sul peso inserito.

**Che cosa NON fa:** non genera dosi, non produce raccomandazioni, non decide. Seleziona e mostra
ciò che le fonti già dicono.

**I due limiti, dichiarati anche dentro l'app:** possono comparire voci non applicabili al singolo
caso, e possono mancare rischi reali non nominati con quei termini o non presenti nelle schede.
**L'assenza di segnalazioni non equivale a sicurezza.**

Nessun dato del paziente viene salvato o trasmesso: tutto resta nel browser.

---

## Uso

### Online
Pubblicato con GitHub Pages: il workflow in `.github/workflows/pages.yml` valida i contenuti e
pubblica il ramo principale. Il repository si pubblica così com'è, senza file da modificare:
guida passo passo in [docs/PUBBLICAZIONE.md](docs/PUBBLICAZIONE.md).

L'app **non contatta alcun servizio esterno**: anche i caratteri tipografici sono ospitati nel
repository, per cui funziona offline e non trasmette l'indirizzo IP di chi la consulta a terzi.

### Offline / installazione
L'app è una PWA: dal browser è possibile installarla («Aggiungi a schermata Home» o
«Installa applicazione») e da quel momento funziona **senza connessione**, service worker incluso.

### In locale
```bash
git clone https://github.com/tomasoporcheddu00/App-terapia.git
cd App-terapia
python3 -m http.server 8080
# poi apri http://localhost:8080
```
Il service worker richiede `http://localhost` o HTTPS: aprendo `index.html` con doppio clic
(`file://`) l'app funziona ma non si installa.

---

## Struttura del repository

```
index.html                    applicazione completa e autonoma (dati inclusi)
manifest.webmanifest, sw.js   installazione e funzionamento offline
404.html                      reindirizzamento per indirizzi errati
assets/                       icone e caratteri tipografici (licenza SIL OFL 1.1)
data/                         contenuti clinici in JSON, versionabili e revisionabili
  drugs/ (186)  classes/ (76)  dosing/ (228)  interactions/ (180)  regulatory/ (181)
  recommendations/ (25)  rules/ (1)   ← Mappa terapeutica
  infusions/ (15)                     ← UTIC
  organ-function/ (35)                ← Rene e fegato
tools/                        validate_data.py, extract_data.py, embed_data.py
docs/                         architettura, politica dei contenuti, revisione clinica, storico
.github/                      workflow Pages, modelli di segnalazione
```

I file in `data/` sono la **fonte revisionabile** dei contenuti: sono gli stessi dati incorporati
in `index.html` e servono a rendere il lavoro clinico verificabile riga per riga tramite le diff di
Git. Vedi [docs/ARCHITETTURA.md](docs/ARCHITETTURA.md) per il rapporto fra i due.

---

## Stato editoriale

Ogni scheda dichiara il proprio stato:

| Stato | Significato | Quante |
|---|---|---|
| `clinician-approved` | Validata dal curatore clinico | 12 |
| `source-review` | Da fonti citate, **in attesa di validazione clinica** | 169 |
| `placeholder` | Presente in elenco ma non compilata | 5 |

I 5 placeholder residui sono molecole marginali per l'ambito cardiologico o non disponibili in
Europa: abciximab, rilonacept, dalteparina, indometacina, immunoglobuline endovena.

Il passo successivo del progetto non è aggiungere contenuti ma **completare la revisione clinica**:
il percorso è descritto in [docs/REVISIONE-CLINICA.md](docs/REVISIONE-CLINICA.md).

---

## Segnalare un errore clinico

Gli errori clinici hanno la priorità su tutto il resto. Aprire una *issue* con il modello
**«Segnalazione clinica»**, indicando scheda, campo, cosa risulta errato e **la fonte corretta**.
Vedi [CONTRIBUTING.md](CONTRIBUTING.md).

---

## Licenza

- **Codice** (applicazione, script, workflow): licenza MIT — vedi [LICENSE](LICENSE).
- **Contenuti clinici** (`data/`, testo delle schede e dei percorsi): vedi
  [LICENSE-CONTENUTI.md](LICENSE-CONTENUTI.md). La scelta della licenza per i contenuti **è ancora
  aperta** e richiede una decisione del curatore prima della pubblicazione.

I testi delle RCP e delle linee guida restano dei rispettivi titolari: le schede ne contengono
sintesi e parafrasi con la fonte citata, non riproduzioni integrali.
