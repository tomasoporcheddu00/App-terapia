# Pubblicare su GitHub Pages

Repository: <https://github.com/tomasoporcheddu00/App-terapia>
Indirizzo del sito: <https://tomasoporcheddu00.github.io/App-terapia/>

Il materiale è pronto così com'è: **nessun file da modificare** prima della pubblicazione.

## Prima di pubblicare: tre decisioni

1. **Pubblico o privato.** Con un account gratuito GitHub Pages funziona **solo su repository
   pubblici**. Pubblicando ora, 169 schede su 181 risultano ancora in *revisione fonti*: README e
   `DISCLAIMER.md` lo dichiarano in modo evidente, ma la scelta se pubblicare subito o dopo la
   revisione clinica è tua.
2. **Licenza dei contenuti.** Vedi [LICENSE-CONTENUTI.md](../LICENSE-CONTENUTI.md). Finché la
   revisione non è completa la scelta prudente è «tutti i diritti riservati».
3. **Indicizzazione nei motori di ricerca.** Di default il sito è indicizzabile. Se preferisci che
   non compaia nelle ricerche finché le schede non sono validate, aggiungi nell'`<head>` di
   `index.html`: `<meta name="robots" content="noindex">`.

Nel `CITATION.cff` compare il tuo nome come autore: toglilo se preferisci pubblicare in forma anonima.

> **File nascosti.** Il materiale contiene due elementi il cui nome inizia con un punto:
> la cartella `.github` (validazione e pubblicazione automatica) e il file `.nojekyll`.
> Su Mac il Finder non li mostra: premi **Cmd + Maiusc + .** (punto) per vederli prima di
> copiare. Su Windows sono visibili normalmente.

---

## Strada A — GitHub Desktop (consigliata, nessun comando)

Il caricamento dal sito di GitHub accetta **al massimo 100 file per volta** e il materiale ne
contiene oltre 900 (la cartella `data/`): per questo la strada più comoda è GitHub Desktop.

1. Installa **GitHub Desktop** (<https://desktop.github.com>) e accedi con il tuo account.
2. **File → Clone repository…** → scegli `tomasoporcheddu00/App-terapia` → **Clone**.
   Si crea sul computer la cartella `App-terapia`.
3. Estrai lo ZIP e copia **tutto il contenuto** della cartella estratta (file nascosti compresi,
   vedi sopra) dentro `App-terapia`. Se il repository conteneva già un `README.md`, sostituiscilo.
4. In GitHub Desktop compaiono i file nuovi: in basso a sinistra scrivi `CardioTherapy Atlas 1.0`
   → **Commit to main** → **Push origin**.
5. Vai alla sezione **Attivare Pages** qui sotto.

Se il ramo principale del repository non si chiama `main` (lo vedi in alto in GitHub Desktop),
cambia `branches: [main]` nel file `.github/workflows/pages.yml` con il nome corretto.

## Strada B — riga di comando

```bash
git clone https://github.com/tomasoporcheddu00/App-terapia.git
cp -R cardiotherapy-atlas/. App-terapia/     # il "/." copia anche i file nascosti
cd App-terapia
python3 tools/validate_data.py && python3 tools/extract_data.py
git add -A
git commit -m "CardioTherapy Atlas 1.0"
git push origin main
```

## Strada C — solo dal browser (senza installare nulla)

Per avere il sito online subito, senza la cartella `data/` (non serve al funzionamento: i dati
sono già dentro `index.html`; è la copia leggibile per la revisione, da aggiungere più avanti con
la strada A o B).

1. Estrai `App-terapia-caricamento-browser.zip`: ottieni la cartella `App-terapia-sito`
   (meno di 100 file).
2. Su github.com apri il repository → **Add file → Upload files** → trascina nella pagina
   **il contenuto** della cartella (cartelle `assets`, `docs`, `tools` comprese) → **Commit changes**.
3. **Add file → Create new file** → nome `.nojekyll` (con il punto iniziale), contenuto vuoto →
   **Commit changes**.
4. **Settings → Pages → Source: Deploy from a branch → main → / (root) → Save**.

Con questa strada non c'è la validazione automatica prima della pubblicazione: quando aggiungerai
`data/` e `.github/` con la strada A o B, passa a **Source: GitHub Actions**.

---

## Attivare Pages

Nel repository su github.com: **Settings → Pages → Build and deployment → Source:
GitHub Actions**.

Poi **Actions → Pubblicazione su GitHub Pages → Run workflow** (oppure fai un qualunque nuovo
commit). Il primo avvio parte già al caricamento ma fallisce se Pages non era ancora attivato: in
quel caso basta rilanciarlo.

Il workflow prima **valida i contenuti clinici e la sintassi JavaScript**, poi pubblica: se la
validazione fallisce il sito resta alla versione precedente. È voluto: su contenuti clinici è
meglio non pubblicare che pubblicare rotto. Dopo 1-2 minuti il sito è online; l'indirizzo compare
in **Settings → Pages**.

### Alternativa senza Actions

Se preferisci non usare le Actions: **Source: Deploy from a branch → main → / (root) → Save**.
Il sito funziona allo stesso modo (il file `.nojekyll` è già presente), ma **perdi la validazione
automatica** prima della pubblicazione: ricordati di eseguire gli strumenti in locale.

---

## Verificare il sito pubblicato

- l'app si apre e le otto sezioni rispondono;
- una scheda qualunque si apre, così come Simulazione e Interazioni;
- **installazione**: su computer compare l'icona di installazione nella barra degli indirizzi; su
  Android «Installa app» nel menu; su iPhone da Safari **Condividi → Aggiungi a schermata Home**;
- **offline**: dopo la prima apertura, disattiva la rete e ricarica: l'app deve funzionare,
  caratteri compresi (sono ospitati nel repository, non su servizi esterni).

## Aggiornare dopo una modifica

```bash
python3 tools/validate_data.py && python3 tools/extract_data.py
git add -A && git commit -m "revisione clinica: <scheda> → clinician-approved" && git push
```

Con GitHub Desktop: modifica i file, scrivi il messaggio, **Commit to main**, **Push origin**.

La pubblicazione riparte da sola. Per far comparire subito l'aggiornamento a chi ha installato
l'app, incrementa `CACHE_NAME` in `sw.js` (es. da `v2` a `v3`): comparirà l'avviso «È disponibile
una versione aggiornata».

## Provare in locale prima di pubblicare

```bash
cd App-terapia
python3 -m http.server 8080
# apri http://localhost:8080
```

Aprendo `index.html` con doppio clic l'app funziona, ma non si installa e non va offline: il
service worker richiede `http://` o `https://`.

## Rifiniture facoltative sul repository

- **About** (ingranaggio in alto a destra): descrizione, link al sito, argomenti `cardiology`,
  `pharmacology`, `clinical-decision-support`, `pwa`, `italian`.
- **Etichette** per le segnalazioni: `clinica`, `da-verificare`, `urgente`, `revisione-clinica`, `bug`.
- **Protezione del ramo** `main` se lavorerai con altri: richiedi che il workflow di validazione
  passi prima di accettare modifiche.

## Nota sulla dimensione

`index.html` pesa circa 2,5 MB perché contiene tutti i dati clinici: nessun problema per Git o
Pages, ma GitHub non ne mostra l'anteprima nel browser dei file. Le modifiche leggibili riga per
riga si vedono in `data/`, la forma pensata per la revisione.
