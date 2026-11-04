# -*- coding: utf-8 -*-
"""
CORSO DI LINGUA RUMENA - LIVELLO A1 (per studenti italiani)
Leonardo Scuole - contenuti delle lezioni, vocaboli, frasi utili e quiz.

Ogni modulo e' identificato dal titolo (= colonna "Argomento" del catalogo).
Leo.py usa questo file per:
  - aggiungere i moduli al catalogo se non sono ancora presenti nel foglio Google
  - mostrare lezione, vocaboli e frasi quando lo studente apre il modulo
  - far funzionare il pulsante "Avvia Test / Quiz"

Guida alla pronuncia usata nelle colonne "Pronuncia":
  - si legge come in italiano; la sillaba in MAIUSCOLO e' quella accentata
  - "ə" = vocale neutra del rumeno "ă" (una "e" debole, come nell'inglese "the")
  - "î"  = vocale del rumeno "â/î" (si pronuncia con la bocca da "i" ma la lingua indietro)
  - "k"  = c dura (come in "casa"); "ts" = z di "zio"; "sc" = sc di "scena"
"""

INDIRIZZO_RUMENO = "Corso Rumeno"
ANNO_RUMENO = 1
MATERIA_BASE = "Lingua Rumena - Base"
MATERIA_GRAMMATICA = "Grammatica Rumena"

MODULI_RUMENO = [
    # ------------------------------------------------------------------
    {
        "ordine": 1,
        "materia": MATERIA_BASE,
        "titolo": "Modulo 1 - Alfabeto e pronuncia",
        "descrizione": "Le 31 lettere dell'alfabeto rumeno, le 5 lettere speciali (ă, â, î, ș, ț) e le regole di lettura che cambiano rispetto all'italiano.",
        "lezione": """
**Buone notizie:** il rumeno è una lingua neolatina, come l'italiano. Si scrive quasi come si pronuncia e moltissime parole ti sembreranno familiari.

L'alfabeto ha **31 lettere**: le 26 dell'alfabeto latino più 5 lettere con segni speciali.

| Lettera | Come si pronuncia | Esempio |
|---|---|---|
| **ă** | vocale neutra, una "e" debole | *mamă* (mamma) |
| **â / î** | vocale centrale, senza equivalente italiano: bocca da "i", lingua indietro | *câine* (cane), *înghețată* (gelato) |
| **ș** | come **sc** di *scena* | *șase* (sei) |
| **ț** | come **z** di *zio* | *țară* (paese) |

**â** e **î** sono lo stesso suono: **î** si usa a inizio e fine parola, **â** in mezzo.

**Regole uguali all'italiano:**
- **ce / ci** → come *cena*, *cielo*: *cireașă* (ciliegia)
- **che / chi** → come *chiesa*: *chitară* (chitarra)
- **ge / gi** → come *gelato*: *ger* (gelo)
- **ghe / ghi** → come *ghiro*: *ghid* (guida)

**Regole diverse dall'italiano:**
- **h** si pronuncia sempre, aspirata: *hartă* (mappa)
- **j** si legge come la *j* francese di *bonjour*: *jucărie* (giocattolo)
- la **-i finale** dopo consonante si sente appena: *lupi* (lupi) si dice quasi "lup'"
- l'accento non si scrive, ma cade spesso sulla penultima sillaba, come in italiano
""",
        "vocaboli": [
            ("mamă", "MA-mə", "mamma"),
            ("băiat", "bə-IAT", "ragazzo"),
            ("câine", "KÎI-ne", "cane"),
            ("înghețată", "în-ghe-TSA-tə", "gelato"),
            ("șase", "SCIA-se", "sei"),
            ("țară", "TSA-rə", "paese, nazione"),
            ("cireașă", "ci-RIA-scə", "ciliegia"),
            ("chitară", "ki-TA-rə", "chitarra"),
            ("ger", "GER (g di gelato)", "gelo"),
            ("ghid", "GHID (g di ghiro)", "guida"),
            ("hartă", "HAR-tə (h aspirata)", "mappa, cartina"),
            ("jucărie", "ju-kə-RI-e (j francese)", "giocattolo"),
        ],
        "frasi": [
            ("Cum se scrie?", "Come si scrive?"),
            ("Cum se pronunță?", "Come si pronuncia?"),
            ("Mai rar, vă rog.", "Più lentamente, per favore."),
        ],
        "quiz": [
            {"domanda": "Quante lettere ha l'alfabeto rumeno?",
             "opzioni": ["21", "26", "31", "33"], "corretta": 2,
             "spiegazione": "Sono 31: le 26 lettere latine più ă, â, î, ș, ț."},
            {"domanda": "Come si pronuncia la lettera «ș» in «șase»?",
             "opzioni": ["Come la «s» di «sole»", "Come «sc» di «scena»", "Come la «z» di «zio»", "Come la «c» di «casa»"], "corretta": 1,
             "spiegazione": "«ș» suona come «sc» di «scena»: «șase» si dice «SCIA-se»."},
            {"domanda": "Quale lettera si pronuncia come la «z» di «zio»?",
             "opzioni": ["ț", "ș", "ă", "j"], "corretta": 0,
             "spiegazione": "«ț» = «ts»: «țară» si dice «TSA-rə»."},
            {"domanda": "Come si legge «chitară»?",
             "opzioni": ["ci-TA-rə", "sci-TA-rə", "ki-TA-rə", "hi-TA-rə"], "corretta": 2,
             "spiegazione": "Come in italiano, «chi» ha la c dura: «ki-TA-rə»."},
            {"domanda": "«â» e «î» indicano...",
             "opzioni": ["due suoni diversi", "lo stesso suono", "una vocale lunga", "una lettera muta"], "corretta": 1,
             "spiegazione": "Sono lo stesso suono: «î» a inizio e fine parola, «â» all'interno."},
            {"domanda": "Nella parola «hartă» la «h»...",
             "opzioni": ["è muta come in italiano", "si pronuncia aspirata", "si legge come «k»", "si legge come «sc»"], "corretta": 1,
             "spiegazione": "In rumeno la «h» si pronuncia sempre, aspirata."},
        ],
    },
    # ------------------------------------------------------------------
    {
        "ordine": 2,
        "materia": MATERIA_BASE,
        "titolo": "Modulo 2 - Saluti e presentazioni",
        "descrizione": "Salutare in ogni momento della giornata, presentarsi, chiedere come sta qualcuno e usare la forma di cortesia.",
        "lezione": """
**Salutare.** Il saluto cambia in base al momento della giornata:
- *Bună dimineața* → buongiorno (la mattina presto)
- *Bună ziua* → buongiorno / buon pomeriggio (il saluto formale più comune)
- *Bună seara* → buonasera
- *Noapte bună* → buonanotte (quando si va a dormire)

Tra amici si dice **Salut!** o **Bună!**, e per congedarsi **Pa!**. In un contesto formale si usa **La revedere** (arrivederci).

**Tu e Lei.** Come in italiano esiste la forma di cortesia: in rumeno si usa la **seconda persona plurale** (*dumneavoastră*), come il "voi" di rispetto.
- *Te rog* → per favore (al tu)
- *Vă rog* → per favore (al Lei)

**Presentarsi:**
- *Cum te cheamă?* → Come ti chiami?
- *Mă cheamă Marco.* oppure *Mă numesc Marco.* → Mi chiamo Marco.
- *Îmi pare bine!* → Piacere!
""",
        "vocaboli": [
            ("Bună ziua", "BU-nə ZI-ua", "buongiorno (formale)"),
            ("Bună dimineața", "BU-nə di-mi-NIA-tsa", "buongiorno (mattina)"),
            ("Bună seara", "BU-nə SIA-ra", "buonasera"),
            ("Noapte bună", "NUAP-te BU-nə", "buonanotte"),
            ("Salut / Bună", "sa-LUT / BU-nə", "ciao (arrivo)"),
            ("La revedere", "la re-ve-DE-re", "arrivederci"),
            ("Pa", "PA", "ciao (congedo)"),
            ("Mulțumesc", "mul-tsu-MESK", "grazie"),
            ("Cu plăcere", "ku plə-CE-re", "prego, con piacere"),
            ("Te rog / Vă rog", "te ROG / və ROG", "per favore (tu / Lei)"),
            ("Scuzați-mă", "sku-ZA-tsi mə", "mi scusi"),
            ("Da / Nu", "DA / NU", "sì / no"),
        ],
        "frasi": [
            ("Cum te cheamă?", "Come ti chiami?"),
            ("Mă numesc Ana.", "Mi chiamo Ana."),
            ("Cum vă numiți?", "Come si chiama? (forma di cortesia)"),
            ("Ce mai faci?", "Come stai?"),
            ("Bine, mulțumesc. Și tu?", "Bene, grazie. E tu?"),
            ("De unde ești?", "Di dove sei?"),
            ("Sunt din Italia.", "Sono dall'Italia."),
            ("Sunt italian / italiancă.", "Sono italiano / italiana."),
            ("Îmi pare bine!", "Piacere!"),
            ("Nu înțeleg.", "Non capisco."),
            ("Vorbiți italiană?", "Parla italiano?"),
        ],
        "quiz": [
            {"domanda": "Come si dice «buonasera»?",
             "opzioni": ["Bună ziua", "Bună seara", "Noapte bună", "La revedere"], "corretta": 1,
             "spiegazione": "«Bună seara» = buonasera. «Noapte bună» si usa quando si va a dormire."},
            {"domanda": "Cosa significa «Mulțumesc»?",
             "opzioni": ["Prego", "Scusi", "Grazie", "Per favore"], "corretta": 2,
             "spiegazione": "«Mulțumesc» = grazie; si risponde «Cu plăcere» (prego)."},
            {"domanda": "Come chiedi a un amico «Come ti chiami?»",
             "opzioni": ["Ce mai faci?", "Cum te cheamă?", "De unde ești?", "Cum vă numiți?"], "corretta": 1,
             "spiegazione": "«Cum te cheamă?» al tu; «Cum vă numiți?» è la forma di cortesia."},
            {"domanda": "«Vă rog» è...",
             "opzioni": ["«per favore» al tu", "«per favore» in forma di cortesia", "«grazie mille»", "«mi dispiace»"], "corretta": 1,
             "spiegazione": "«Vă rog» è la forma di cortesia; al tu si dice «te rog»."},
            {"domanda": "Rispondi a «Ce mai faci?»",
             "opzioni": ["Sunt din Italia.", "Mă numesc Ana.", "Bine, mulțumesc.", "La revedere."], "corretta": 2,
             "spiegazione": "«Ce mai faci?» = come stai? → «Bine, mulțumesc» (bene, grazie)."},
            {"domanda": "Cosa significa «Îmi pare bine!»?",
             "opzioni": ["Mi dispiace!", "Piacere!", "Buon appetito!", "Benvenuto!"], "corretta": 1,
             "spiegazione": "«Îmi pare bine» si dice quando si conosce qualcuno: piacere!"},
        ],
    },
    # ------------------------------------------------------------------
    {
        "ordine": 3,
        "materia": MATERIA_BASE,
        "titolo": "Modulo 3 - Numeri, giorni e orario",
        "descrizione": "Contare da 1 a 1000, i giorni della settimana, chiedere e dire l'ora e il prezzo.",
        "lezione": """
**Numeri da 1 a 10:** *unu, doi, trei, patru, cinci, șase, șapte, opt, nouă, zece*.

**Attenzione al genere:** con i nomi femminili *unu* diventa **una** (o **o** davanti al nome) e *doi* diventa **două**.
→ *un băiat* (un ragazzo), *o fată* (una ragazza), *doi băieți*, *două fete*.

**Da 11 a 19** si aggiunge *-sprezece* ("sopra dieci"): *unsprezece* (11), *doisprezece* (12), *treisprezece* (13)...

**Le decine** si formano con *-zeci*: *douăzeci* (20), *treizeci* (30), *patruzeci* (40)...
→ 21 = *douăzeci și unu* ("venti e uno").

**100** = *o sută* · **1000** = *o mie*

**I giorni della settimana** si scrivono con l'iniziale minuscola, come in italiano: *luni, marți, miercuri, joi, vineri, sâmbătă, duminică*.

**L'orario:**
- *Cât e ceasul?* → Che ore sono?
- *Este ora trei.* → Sono le tre.
- *și jumătate* → e mezza · *și un sfert* → e un quarto · *fără un sfert* → meno un quarto
""",
        "vocaboli": [
            ("unu / una", "U-nu / U-na", "uno / una"),
            ("doi / două", "DOI / DO-uə", "due (m. / f.)"),
            ("trei, patru, cinci", "TREI, PA-tru, CINCI", "tre, quattro, cinque"),
            ("șase, șapte, opt", "SCIA-se, SCIAP-te, OPT", "sei, sette, otto"),
            ("nouă, zece", "NO-uə, ZE-ce", "nove, dieci"),
            ("douăzeci", "do-uə-ZECI", "venti"),
            ("o sută / o mie", "o SU-tə / o MI-e", "cento / mille"),
            ("luni, marți, miercuri", "LUN', MARTS', MIER-kur'", "lunedì, martedì, mercoledì"),
            ("joi, vineri", "JOI (j francese), VI-ner'", "giovedì, venerdì"),
            ("sâmbătă, duminică", "SÎM-bə-tə, du-MI-ni-kə", "sabato, domenica"),
            ("azi / mâine / ieri", "AZ' / MÎI-ne / IER'", "oggi / domani / ieri"),
            ("ora", "O-ra", "l'ora"),
        ],
        "frasi": [
            ("Cât e ceasul?", "Che ore sono?"),
            ("Este ora două și jumătate.", "Sono le due e mezza."),
            ("Este ora cinci și un sfert.", "Sono le cinque e un quarto."),
            ("Este ora șase fără un sfert.", "Sono le sei meno un quarto."),
            ("Ce zi este azi?", "Che giorno è oggi?"),
            ("Azi este luni.", "Oggi è lunedì."),
            ("Cât costă?", "Quanto costa?"),
            ("Costă zece lei.", "Costa dieci lei."),
        ],
        "quiz": [
            {"domanda": "Come si dice «sette»?",
             "opzioni": ["șase", "șapte", "opt", "nouă"], "corretta": 1,
             "spiegazione": "șase = 6, șapte = 7, opt = 8, nouă = 9."},
            {"domanda": "Quale forma è corretta per «due ragazze»?",
             "opzioni": ["doi fete", "două fete", "doua fata", "doi fată"], "corretta": 1,
             "spiegazione": "Con i nomi femminili «doi» diventa «două»: «două fete»."},
            {"domanda": "Che numero è «douăzeci și unu»?",
             "opzioni": ["12", "20", "21", "120"], "corretta": 2,
             "spiegazione": "«douăzeci» = 20, «și unu» = e uno → 21."},
            {"domanda": "Che giorno è «joi»?",
             "opzioni": ["Lunedì", "Mercoledì", "Giovedì", "Sabato"], "corretta": 2,
             "spiegazione": "joi = giovedì (somiglia al latino «Iovis dies»)."},
            {"domanda": "«Este ora șase fără un sfert» significa...",
             "opzioni": ["Sono le sei e un quarto", "Sono le sei meno un quarto", "Sono le sei e mezza", "Sono le sette"], "corretta": 1,
             "spiegazione": "«fără un sfert» = meno un quarto → 5:45."},
            {"domanda": "Come chiedi il prezzo di qualcosa?",
             "opzioni": ["Cât e ceasul?", "Ce zi este azi?", "Cât costă?", "Unde este?"], "corretta": 2,
             "spiegazione": "«Cât costă?» = quanto costa? La moneta rumena è il «leu» (plurale «lei»)."},
        ],
    },
    # ------------------------------------------------------------------
    {
        "ordine": 4,
        "materia": MATERIA_BASE,
        "titolo": "Modulo 4 - La famiglia",
        "descrizione": "I nomi dei familiari, gli aggettivi possessivi «meu / mea» e le frasi per parlare della propria famiglia.",
        "lezione": """
**Il possessivo va dopo il nome.** In rumeno si dice *"fratello-il mio"*:
- maschile: *fratele **meu*** → mio fratello
- femminile: *sora **mea*** → mia sorella
- plurale: *părinții **mei*** (i miei genitori), *surorile **mele*** (le mie sorelle)

Nota che il nome prende l'**articolo attaccato alla fine**: *frate* → *frate**le***, *soră* → *sor**a***. Lo vediamo bene nel Modulo 8.

**Avere.** Per dire quanti fratelli o figli hai si usa *am* (ho):
- *Am un frate și o soră.* → Ho un fratello e una sorella.
- *Nu am copii.* → Non ho figli.

**Tată (padre)** è maschile anche se finisce in -ă: *tatăl meu* → mio padre.
""",
        "vocaboli": [
            ("familia", "fa-MI-lia", "la famiglia"),
            ("mama / tata", "MA-ma / TA-ta", "la mamma / il papà"),
            ("părinții", "pə-RIN-tsii", "i genitori"),
            ("fratele", "FRA-te-le", "il fratello"),
            ("sora", "SO-ra", "la sorella"),
            ("fiul / fiica", "FI-ul / FI-i-ka", "il figlio / la figlia"),
            ("copilul / copiii", "ko-PI-lul / ko-PI-ii", "il bambino / i bambini (anche: figli)"),
            ("bunicul / bunica", "bu-NI-kul / bu-NI-ka", "il nonno / la nonna"),
            ("soțul / soția", "SO-tsul / so-TSI-a", "il marito / la moglie"),
            ("unchiul / mătușa", "UN-kiul / mə-TU-scia", "lo zio / la zia"),
            ("vărul / verișoara", "VƏ-rul / ve-ri-SCIUA-ra", "il cugino / la cugina"),
        ],
        "frasi": [
            ("Am un frate și o soră.", "Ho un fratello e una sorella."),
            ("Ai frați sau surori?", "Hai fratelli o sorelle?"),
            ("Am doi copii.", "Ho due figli."),
            ("Mama mea se numește Elena.", "Mia madre si chiama Elena."),
            ("Acesta este tatăl meu.", "Questo è mio padre."),
            ("Părinții mei locuiesc în Italia.", "I miei genitori vivono in Italia."),
        ],
        "quiz": [
            {"domanda": "Come si dice «mia sorella»?",
             "opzioni": ["mea sora", "sora mea", "sora meu", "meu sora"], "corretta": 1,
             "spiegazione": "Il possessivo va dopo il nome e concorda: «sora mea»."},
            {"domanda": "Cosa significa «bunica»?",
             "opzioni": ["la zia", "la cugina", "la nonna", "la moglie"], "corretta": 2,
             "spiegazione": "bunicul = il nonno, bunica = la nonna."},
            {"domanda": "Traduci: «Ho due figli».",
             "opzioni": ["Am doi copii.", "Ai doi copii.", "Sunt doi copii.", "Am două copii."], "corretta": 0,
             "spiegazione": "«Am» = ho; «copil» è maschile, quindi «doi copii»."},
            {"domanda": "«Mio padre» si dice...",
             "opzioni": ["tata mea", "tatăl meu", "meu tată", "tatăl mea"], "corretta": 1,
             "spiegazione": "«tată» è maschile: «tatăl meu»."},
            {"domanda": "Cosa significa «părinții»?",
             "opzioni": ["i parenti", "i genitori", "i fratelli", "i nonni"], "corretta": 1,
             "spiegazione": "Falso amico: «părinții» = i genitori, non «i parenti» (che si dice «rudele»)."},
            {"domanda": "Chi è «soțul»?",
             "opzioni": ["il suocero", "il fratello", "il marito", "il figlio"], "corretta": 2,
             "spiegazione": "soțul = il marito, soția = la moglie."},
        ],
    },
    # ------------------------------------------------------------------
    {
        "ordine": 5,
        "materia": MATERIA_BASE,
        "titolo": "Modulo 5 - Cibo e ristorante",
        "descrizione": "Ordinare al ristorante e al bar, i cibi di base, i piatti tipici rumeni e le frasi di cortesia a tavola.",
        "lezione": """
**Ordinare con cortesia.** La formula più usata è *Aș dori...* (vorrei...):
- *Aș dori o cafea, vă rog.* → Vorrei un caffè, per favore.
- *O masă pentru doi, vă rog.* → Un tavolo per due, per favore.
- *Nota, vă rog.* → Il conto, per favore.

**A tavola:**
- *Poftă bună!* → Buon appetito!
- *Noroc!* → Salute! (per brindare)

**Piatti tipici da conoscere:**
- **ciorbă** → zuppa dal sapore leggermente acidulo (*ciorbă de perișoare*: con polpettine)
- **sarmale** → involtini di foglie di cavolo o di vite ripieni di carne e riso
- **mămăligă** → polenta, spesso servita con *brânză* (formaggio) e *smântână* (panna acida)

**L'acqua:** *apă plată* è naturale, *apă minerală* è di solito frizzante.
""",
        "vocaboli": [
            ("pâine", "PÎI-ne", "pane"),
            ("apă plată / minerală", "A-pə PLA-tə / mi-ne-RA-lə", "acqua naturale / frizzante"),
            ("vin / bere", "VIN / BE-re", "vino / birra"),
            ("cafea / ceai", "ka-FIA / CEAI", "caffè / tè"),
            ("lapte", "LAP-te", "latte"),
            ("carne / pui", "KAR-ne / PUI", "carne / pollo"),
            ("pește", "PE-scte", "pesce"),
            ("legume / fructe", "le-GU-me / FRUK-te", "verdure / frutta"),
            ("brânză", "BRÎN-zə", "formaggio"),
            ("meniul", "me-NI-ul", "il menù"),
            ("nota", "NO-ta", "il conto"),
            ("ciorbă / sarmale / mămăligă", "CIOR-bə / sar-MA-le / mə-mə-LI-gə", "zuppa / involtini di cavolo / polenta"),
        ],
        "frasi": [
            ("O masă pentru doi, vă rog.", "Un tavolo per due, per favore."),
            ("Meniul, vă rog.", "Il menù, per favore."),
            ("Aș dori o ciorbă și o apă plată.", "Vorrei una zuppa e un'acqua naturale."),
            ("Ce recomandați?", "Cosa consiglia?"),
            ("Sunt vegetarian / vegetariană.", "Sono vegetariano / vegetariana."),
            ("Este foarte bun!", "È buonissimo!"),
            ("Poftă bună!", "Buon appetito!"),
            ("Nota, vă rog.", "Il conto, per favore."),
        ],
        "quiz": [
            {"domanda": "Come si chiede il conto?",
             "opzioni": ["Meniul, vă rog.", "Nota, vă rog.", "Poftă bună!", "Noroc!"], "corretta": 1,
             "spiegazione": "«Nota, vă rog» = il conto, per favore."},
            {"domanda": "Cosa significa «Aș dori o cafea»?",
             "opzioni": ["Ho un caffè", "Vorrei un caffè", "Non bevo caffè", "Il caffè è buono"], "corretta": 1,
             "spiegazione": "«Aș dori» = vorrei: è la formula di cortesia per ordinare."},
            {"domanda": "«Brânză» è...",
             "opzioni": ["il pane", "il burro", "il formaggio", "la birra"], "corretta": 2,
             "spiegazione": "brânză = formaggio; la birra è «bere»."},
            {"domanda": "Cosa si dice per brindare?",
             "opzioni": ["Poftă bună!", "Noroc!", "Mulțumesc!", "Pa!"], "corretta": 1,
             "spiegazione": "«Noroc!» = salute! «Poftă bună!» = buon appetito."},
            {"domanda": "Cosa sono le «sarmale»?",
             "opzioni": ["Una zuppa acidula", "Involtini di cavolo ripieni", "Un dolce al formaggio", "Una birra scura"], "corretta": 1,
             "spiegazione": "Le sarmale sono involtini di foglie di cavolo (o vite) ripieni di carne e riso."},
            {"domanda": "Vuoi acqua naturale. Cosa chiedi?",
             "opzioni": ["apă minerală", "apă plată", "lapte", "ceai"], "corretta": 1,
             "spiegazione": "«apă plată» = naturale; «apă minerală» di solito è frizzante."},
        ],
    },
    # ------------------------------------------------------------------
    {
        "ordine": 6,
        "materia": MATERIA_BASE,
        "titolo": "Modulo 6 - In città: indicazioni e trasporti",
        "descrizione": "Chiedere dove si trova un luogo, capire le indicazioni (destra, sinistra, dritto) e comprare un biglietto.",
        "lezione": """
**Chiedere dove si trova un posto:** *Unde este...?* (Dov'è...?)
- *Unde este gara?* → Dov'è la stazione?
- *Unde este o farmacie?* → Dov'è una farmacia?

**Capire la risposta:**
- *la stânga* → a sinistra · *la dreapta* → a destra
- *drept înainte* → sempre dritto
- *aproape* → vicino · *departe* → lontano
- *aici* → qui · *acolo* → lì

**Dare del Lei.** Nelle indicazioni sentirai il verbo alla forma di cortesia, che finisce in **-ți**:
*Mergeți drept înainte, apoi la dreapta.* → Vada sempre dritto, poi a destra.

**Trasporti:** *autobuzul* (l'autobus), *tramvaiul* (il tram), *metroul* (la metropolitana), *trenul* (il treno), *taxiul* (il taxi).
""",
        "vocaboli": [
            ("la stânga / la dreapta", "la STÎN-ga / la DREAP-ta", "a sinistra / a destra"),
            ("drept înainte", "DREPT î-na-IN-te", "sempre dritto"),
            ("aici / acolo", "a-ICI / a-KO-lo", "qui / lì"),
            ("aproape / departe", "a-PRUA-pe / de-PAR-te", "vicino / lontano"),
            ("gara", "GA-ra", "la stazione"),
            ("aeroportul", "a-e-ro-POR-tul", "l'aeroporto"),
            ("stația de autobuz", "STA-tsia de au-to-BUZ", "la fermata dell'autobus"),
            ("biletul", "bi-LE-tul", "il biglietto"),
            ("strada", "STRA-da", "la strada, la via"),
            ("farmacia / spitalul", "far-ma-CI-a / spi-TA-lul", "la farmacia / l'ospedale"),
            ("hotelul", "ho-TE-lul", "l'albergo"),
        ],
        "frasi": [
            ("Unde este gara?", "Dov'è la stazione?"),
            ("Este departe?", "È lontano?"),
            ("Nu, este aproape.", "No, è vicino."),
            ("Mergeți drept înainte, apoi la stânga.", "Vada dritto, poi a sinistra."),
            ("Cât costă un bilet?", "Quanto costa un biglietto?"),
            ("Un bilet până la Brașov, vă rog.", "Un biglietto per Brașov, per favore."),
            ("Opriți aici, vă rog.", "Si fermi qui, per favore. (in taxi)"),
            ("M-am rătăcit.", "Mi sono perso."),
        ],
        "quiz": [
            {"domanda": "Come chiedi «Dov'è la stazione?»",
             "opzioni": ["Cât costă gara?", "Unde este gara?", "Este gara aproape.", "Gara, vă rog."], "corretta": 1,
             "spiegazione": "«Unde este...?» = dov'è...?"},
            {"domanda": "«La dreapta» significa...",
             "opzioni": ["a sinistra", "a destra", "dritto", "indietro"], "corretta": 1,
             "spiegazione": "la dreapta = a destra; la stânga = a sinistra."},
            {"domanda": "Il contrario di «aproape» è...",
             "opzioni": ["aici", "acolo", "departe", "înainte"], "corretta": 2,
             "spiegazione": "aproape = vicino ↔ departe = lontano."},
            {"domanda": "Cosa significa «Mergeți drept înainte»?",
             "opzioni": ["Giri a destra", "Si fermi qui", "Vada sempre dritto", "Torni indietro"], "corretta": 2,
             "spiegazione": "«drept înainte» = sempre dritto; «mergeți» è la forma di cortesia di «andare»."},
            {"domanda": "«Biletul» è...",
             "opzioni": ["il biglietto", "il bagaglio", "il binario", "il conto"], "corretta": 0,
             "spiegazione": "bilet = biglietto; con l'articolo attaccato: biletul = il biglietto."},
            {"domanda": "Sei in taxi e vuoi scendere. Cosa dici?",
             "opzioni": ["Unde este taxiul?", "Opriți aici, vă rog.", "M-am rătăcit.", "Este departe?"], "corretta": 1,
             "spiegazione": "«Opriți aici, vă rog» = si fermi qui, per favore."},
        ],
    },
    # ------------------------------------------------------------------
    {
        "ordine": 7,
        "materia": MATERIA_GRAMMATICA,
        "titolo": "Modulo 7 - I verbi a fi (essere) e a avea (avere)",
        "descrizione": "La coniugazione al presente dei due verbi più importanti, la frase negativa e la domanda.",
        "lezione": """
**A fi = essere**

| Persona | Rumeno | Italiano |
|---|---|---|
| eu | **sunt** | io sono |
| tu | **ești** | tu sei |
| el / ea | **este** (o **e**) | lui / lei è |
| noi | **suntem** | noi siamo |
| voi | **sunteți** | voi siete (anche: Lei è) |
| ei / ele | **sunt** | loro sono |

**A avea = avere**

| Persona | Rumeno | Italiano |
|---|---|---|
| eu | **am** | io ho |
| tu | **ai** | tu hai |
| el / ea | **are** | lui / lei ha |
| noi | **avem** | noi abbiamo |
| voi | **aveți** | voi avete (anche: Lei ha) |
| ei / ele | **au** | loro hanno |

**Il soggetto si può omettere**, come in italiano: *Sunt student.* → (Io) sono studente.

**La negazione:** *nu* davanti al verbo → *Nu sunt obosit.* (Non sono stanco), *Nu am timp.* (Non ho tempo).

**La domanda:** basta l'intonazione → *Ești obosit?* (Sei stanco?)

⚠️ *sunt* vale sia per "io sono" sia per "loro sono": si capisce dal contesto.
""",
        "vocaboli": [
            ("a fi", "a FI", "essere"),
            ("a avea", "a a-VIA", "avere"),
            ("student / studentă", "stu-DENT / stu-DEN-tə", "studente / studentessa"),
            ("profesor / profesoară", "pro-fe-SOR / pro-fe-SUA-rə", "insegnante (m. / f.)"),
            ("obosit / obosită", "o-bo-SIT / o-bo-SI-tə", "stanco / stanca"),
            ("fericit / fericită", "fe-ri-CIT / fe-ri-CI-tə", "felice"),
            ("casă", "KA-sə", "casa"),
            ("mașină", "ma-SCI-nə", "automobile"),
            ("timp", "TIMP", "tempo"),
            ("foame / sete", "FUA-me / SE-te", "fame / sete"),
        ],
        "frasi": [
            ("Sunt student.", "Sono studente."),
            ("Ea este profesoară.", "Lei è insegnante."),
            ("Suntem din Napoli.", "Siamo di Napoli."),
            ("Ești obosit?", "Sei stanco?"),
            ("Avem o casă mică.", "Abbiamo una casa piccola."),
            ("Ei au o mașină nouă.", "Loro hanno un'auto nuova."),
            ("Mi-e foame. / Mi-e sete.", "Ho fame. / Ho sete."),
            ("Nu am timp.", "Non ho tempo."),
        ],
        "quiz": [
            {"domanda": "Completa: «Noi ___ din Italia.»",
             "opzioni": ["sunt", "ești", "suntem", "sunteți"], "corretta": 2,
             "spiegazione": "noi → suntem (noi siamo)."},
            {"domanda": "Come si dice «tu hai»?",
             "opzioni": ["ai", "am", "are", "au"], "corretta": 0,
             "spiegazione": "eu am, tu ai, el/ea are, noi avem, voi aveți, ei au."},
            {"domanda": "«Ei au o mașină» significa...",
             "opzioni": ["Lui ha un'auto", "Loro hanno un'auto", "Noi abbiamo un'auto", "Loro sono in auto"], "corretta": 1,
             "spiegazione": "«ei au» = loro hanno; «mașină» = automobile."},
            {"domanda": "Come si rende negativa «Sunt obosit»?",
             "opzioni": ["Sunt nu obosit.", "Nu sunt obosit.", "Sunt obosit nu.", "Ne sunt obosit."], "corretta": 1,
             "spiegazione": "Basta mettere «nu» davanti al verbo: «Nu sunt obosit»."},
            {"domanda": "Completa: «Ea ___ profesoară.»",
             "opzioni": ["sunt", "este", "are", "ești"], "corretta": 1,
             "spiegazione": "el/ea → este (o la forma breve «e»)."},
            {"domanda": "«Sunt» può significare...",
             "opzioni": ["solo «io sono»", "solo «loro sono»", "sia «io sono» sia «loro sono»", "«tu sei»"], "corretta": 2,
             "spiegazione": "«sunt» è la forma di eu e di ei/ele: si capisce dal contesto."},
        ],
    },
    # ------------------------------------------------------------------
    {
        "ordine": 8,
        "materia": MATERIA_GRAMMATICA,
        "titolo": "Modulo 8 - Genere dei nomi e articolo determinativo",
        "descrizione": "I tre generi del rumeno (maschile, femminile, neutro), l'articolo indeterminativo e l'articolo determinativo attaccato alla fine della parola.",
        "lezione": """
**Tre generi.** Oltre a maschile e femminile, il rumeno ha il **neutro**: si comporta come maschile al singolare e come femminile al plurale.
→ *un tren* (un treno), *două trenuri* (due treni).

**Articolo indeterminativo** (un / una), davanti al nome:
- **un** → maschile e neutro: *un băiat* (un ragazzo), *un tren* (un treno)
- **o** → femminile: *o fată* (una ragazza), *o casă* (una casa)

**Articolo determinativo** (il / la): la grande differenza con l'italiano è che **si attacca alla fine della parola**!

| Genere | Senza articolo | Con articolo | Regola |
|---|---|---|---|
| maschile | băiat | **băiatul** (il ragazzo) | + **-ul** |
| maschile in -e | frate | **fratele** (il fratello) | + **-le** |
| femminile in -ă | casă | **casa** (la casa) | -ă → **-a** |
| femminile in -ea | cafea | **cafeaua** (il caffè) | + **-ua** |
| neutro | tren | **trenul** (il treno) | + **-ul** |

**Plurale con articolo:** *băieții* (i ragazzi), *fetele* (le ragazze), *trenurile* (i treni).

💡 **Trucco:** se una parola finisce in **-ul** o **-a**, spesso ha già dentro il "il / la".
""",
        "vocaboli": [
            ("un băiat → băiatul", "un bə-IAT → bə-IA-tul", "un ragazzo → il ragazzo"),
            ("o fată → fata", "o FA-tə → FA-ta", "una ragazza → la ragazza"),
            ("un tren → trenul", "un TREN → TRE-nul", "un treno → il treno"),
            ("o casă → casa", "o KA-sə → KA-sa", "una casa → la casa"),
            ("un frate → fratele", "un FRA-te → FRA-te-le", "un fratello → il fratello"),
            ("o cafea → cafeaua", "o ka-FIA → ka-FIA-ua", "un caffè → il caffè"),
            ("un scaun → scaunul", "un SKA-un → SKA-u-nul", "una sedia → la sedia (neutro!)"),
            ("băieți → băieții", "bə-IETS' → bə-IE-tsii", "ragazzi → i ragazzi"),
            ("fete → fetele", "FE-te → FE-te-le", "ragazze → le ragazze"),
            ("trenuri → trenurile", "TRE-nur' → TRE-nu-ri-le", "treni → i treni"),
        ],
        "frasi": [
            ("Băiatul este student.", "Il ragazzo è studente."),
            ("Fata are o carte.", "La ragazza ha un libro."),
            ("Trenul este aici.", "Il treno è qui."),
            ("Cafeaua este bună.", "Il caffè è buono."),
            ("Casa este mare.", "La casa è grande."),
        ],
        "quiz": [
            {"domanda": "Come si dice «il ragazzo»?",
             "opzioni": ["ul băiat", "băiatul", "un băiat", "băiata"], "corretta": 1,
             "spiegazione": "L'articolo si attacca alla fine: băiat + -ul = băiatul."},
            {"domanda": "Qual è l'articolo indeterminativo femminile?",
             "opzioni": ["un", "o", "ul", "a"], "corretta": 1,
             "spiegazione": "«o» per il femminile (o fată), «un» per maschile e neutro."},
            {"domanda": "«Casa» in rumeno significa...",
             "opzioni": ["una casa", "la casa", "le case", "casetta"], "corretta": 1,
             "spiegazione": "casă (una casa) → casa (la casa): la -ă diventa -a."},
            {"domanda": "Quanti generi grammaticali ha il rumeno?",
             "opzioni": ["Due", "Tre", "Quattro", "Uno"], "corretta": 1,
             "spiegazione": "Maschile, femminile e neutro."},
            {"domanda": "«Il caffè» si dice...",
             "opzioni": ["cafeul", "cafea", "cafeaua", "o cafea"], "corretta": 2,
             "spiegazione": "I femminili in -ea prendono -ua: cafea → cafeaua."},
            {"domanda": "Il neutro «tren» al plurale fa «două trenuri». Perché «două»?",
             "opzioni": ["È un errore", "Il neutro al plurale si comporta come femminile", "«Tren» è femminile", "«Două» vale per tutti i plurali"], "corretta": 1,
             "spiegazione": "Il neutro è maschile al singolare (un tren) e femminile al plurale (două trenuri)."},
        ],
    },
]


# ----------------------------------------------------------------------
# FUNZIONI DI SUPPORTO USATE DA Leo.py
# ----------------------------------------------------------------------
def _norm(testo):
    return " ".join(str(testo).strip().lower().split())


_INDICE = {_norm(m["titolo"]): m for m in MODULI_RUMENO}


def trova_modulo(titolo):
    """Restituisce il modulo del corso di rumeno con questo titolo, oppure None."""
    if titolo is None:
        return None
    return _INDICE.get(_norm(titolo))


def righe_catalogo():
    """Righe nel formato del foglio catalogo (stesse colonne usate da Leo.py)."""
    return [
        {
            "Indirizzo_Studio": INDIRIZZO_RUMENO,
            "Anno": ANNO_RUMENO,
            "Materia": m["materia"],
            "Argomento": m["titolo"],
            "Descrizione": m["descrizione"],
            "Dispensa": "",
            "Video": "",
        }
        for m in sorted(MODULI_RUMENO, key=lambda x: x["ordine"])
    ]
