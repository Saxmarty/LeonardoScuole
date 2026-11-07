# -*- coding: utf-8 -*-
"""
CORSO ONLINE DI RUMENO - 15 MODULI (per principianti italofoni)
Leonardo Scuole - contenuti dal documento «Corso_Online_Rumeno_Completo_15_Moduli.docx».

Regole del percorso (dal documento):
  - 15 moduli, completamento progressivo: un modulo si apre quando il precedente e' superato
  - quiz finale di 5 domande, soglia 80% (4 su 5), tentativi ripetibili
  - audio rumeno registrato da madrelingua: file media/rumeno/audio/1.mp3 ... 440.mp3
    (le "voci" del frasario originale; ogni modulo indica il proprio intervallo)
  - circa 30 ore di formazione: alla fine lo studente scarica l'attestato

COME COLLEGARE I VIDEO: carica gli MP4 (YouTube non in elenco, Vimeo o Drive) e incolla
il link accanto al nome del file in VIDEO_LINK qui sotto. Finche' il link e' vuoto, il modulo
mostra "video in arrivo".

FRASARIO: le 440 voci del PDF «Primo contatto», ognuna con il suo audio madrelingua.
Le 8 frasi chiave di ogni modulo (dal documento) sono evidenziate e sono quelle del quiz.
"""
import os

INDIRIZZO_RUMENO = "Corso Rumeno"
ANNO_RUMENO = 1
MATERIA_BASE = "Lingua Rumena"
NOME_CORSO = "Corso Online di Lingua Rumena"
ORE_CORSO = 30
SOGLIA_QUIZ = 0.8  # 80%

# VERSIONE DEL CORSO
# False = BASE: rispetta integralmente il documento Word (8 frasi per modulo).
# True  = PRO: aggiunge tutte le voci del frasario del modulo e le tracce di ascolto completo.
VERSIONE_PRO = False

CARTELLA = os.path.dirname(os.path.abspath(__file__))
CARTELLA_AUDIO = os.path.join(CARTELLA, "media", "rumeno", "audio")
AUDIO_CONCLUSIONI = os.path.join(CARTELLA, "media", "rumeno", "conclusioni.m4a")
CARTELLA_TRACCE = os.path.join(CARTELLA, "media", "rumeno", "tracce")

TESTO_DOCENTE = ("Benvenuti. In questa lezione impareremo le parole più utili per la situazione di oggi. "
                 "Leggete prima la traduzione italiana, ascoltate la frase rumena e ripetetela due volte. "
                 "Poi provate a riconoscerla senza guardare il testo. L’obiettivo è comunicare, non soltanto memorizzare.")

VIDEO_INTRO = "INTRO_Rumeno_Infermieri copia.mp4"

# Spiegazione breve in cima a ogni tappa del modulo (cosa si fa e come)
GUIDA_TAPPE = {
    "video": "Guarda la video lezione fino alla fine: puoi fermarla e riguardarla quando vuoi. "
             "Alla fine il riquadro «Prossimo» ti porta alle schede.",
    "impara": "Per ogni frase leggi l'italiano, premi «Ascolta» e ripeti ad alta voce due volte. "
              "«Lento» la fa sentire rallentata. Poi passa alla frase successiva con «Successiva →».",
    "abbina": "Leggi la frase in rumeno e scegli la traduzione italiana giusta. "
              "Servono almeno 5 risposte giuste su 6: puoi ripetere con domande nuove.",
    "ascolta": "La frase parte da sola: ascoltala (anche più volte) e scegli quella che hai sentito, "
               "senza guardare il testo.",
    "quiz": "Rispondi a tutte le 5 domande e premi «Consegna il quiz». Con almeno 4 risposte giuste (80%) "
            "il modulo è superato e si apre il successivo. Puoi ripeterlo quando vuoi.",
}

# Video dentro il progetto: cartella static/rumeno/video (servita da Streamlit come /app/static/...)
# Il nome del file e' quello originale senza " copia" e "_nuova_versione" (es. Al_Bar.mp4).
CARTELLA_VIDEO = os.path.join(CARTELLA, "static", "rumeno", "video")
URL_VIDEO = "/app/static/rumeno/video/"


def nome_file_video(nome):
    return nome.replace(" copia", "").replace("_nuova_versione", "").replace(" ", "_")

# Contenuti del video di benvenuto (docente virtuale)
BENVENUTO = {
    "titolo": "Bun venit! Corso di Rumeno On Line",
    "sottotitolo": "Il tuo percorso in Romania inizia da qui",
    "obiettivo": "Comunicare fin da subito, senza imparare regole a memoria.",
    "passi": [
        ("Leggi", "il significato della frase in italiano", "«Come si sente?»"),
        ("Ascolta e ripeti", "la pronuncia autentica, ad alta voce, due volte", "«Cum vă simțiți?»"),
        ("Mettiti alla prova", "riconosci la frase solo a orecchio, senza guardare il testo", "🎧"),
    ],
    "motto": "Niente stress per gli errori: ascolta, ripeti, divertiti!",
    "chiusura": "Mult succes! Buona fortuna, futuri infermieri.",
}

# Nome file video -> link pubblico (da compilare)
VIDEO_LINK = {
    "INTRO_Rumeno_Infermieri copia.mp4": "",
    "Parole_Essenziali_nuova_versione.mp4": "",
    "Dialogare_nuova_versione.mp4": "",
    "I_Colori_nuova_versione.mp4": "",
    "I_Numeri_nuova_versione.mp4": "",
    "Riferimenti_Temporali_nuova_versione.mp4": "",
    "Taxi_nuova_versione.mp4": "",
    "Famiglia_ed_Emozioni_nuova_versione.mp4": "",
    "Al_Bar_nuova_versione.mp4": "",
    "Al_Ristorante_nuova_versione.mp4": "",
    "Dividersi_nuova_versione.mp4": "",
    "I_Trasporti_nuova_versione.mp4": "",
    "In_Hotel_nuova_versione.mp4": "",
    "Cercare_Qualcuno_nuova_versione.mp4": "",
    "Vacanza_nuova_versione.mp4": "",
    "In_caso_di_problema_nuova_versione.mp4": "",
}

# FRASARIO ORIGINALE «Primo contatto» (440 voci): numero -> (italiano, rumeno).
# Il numero e' anche il nome del file audio madrelingua: media/rumeno/audio/<numero>.mp3
FRASARIO = {
    1: ("Buongiorno", "Bună ziua"),
    2: ("Buonasera", "Bună seara"),
    3: ("Arrivederci", "La revedere"),
    4: ("A dopo", "Pe curând"),
    5: ("Sì", "Da"),
    6: ("No", "Nu"),
    7: ("Per favore!", "Vă rog!"),
    8: ("Grazie", "Mulțumesc"),
    9: ("Grazie mille", "Vă mulțumesc!"),
    10: ("Grazie per il suo aiuto", "Vă mulțumesc pentru ajutorul dumneavoastră"),
    11: ("Prego", "Cu plăcere"),
    12: ("Va bene", "De acord"),
    13: ("Quanto costa, per favore?", "Cât costă, vă rog"),
    14: ("Mi scusi!", "Pardon!"),
    15: ("Non ho capito", "Nu înțeleg"),
    16: ("Ho capito", "Am înțeles"),
    17: ("Non so", "Nu știu"),
    18: ("Vietato", "Interzis"),
    19: ("Dov'è il bagno per favore?", "Unde este toaleta, vă rog?"),
    20: ("Buon anno!", "Un an nou fericit!"),
    21: ("Buon compleanno!", "La mulți ani!"),
    22: ("Buone feste!", "Sărbători fericite!"),
    23: ("Congratulazioni!", "Felicitări!"),
    24: ("Buongiorno. Come stai?", "Bună ziua Ce mai faci?"),
    25: ("Buongiorno. Bene, grazie", "Bună ziua. Bine, mulțumesc"),
    26: ("Parli rumeno?", "Vorbești românește?"),
    27: ("No, non parlo rumeno", "Nu, nu vorbesc românește"),
    28: ("Soltanto un po'", "Puțin de tot"),
    29: ("Di dove sei?", "Din ce țară ești?"),
    30: ("Di che nazionalità sei?", "De ce naționalitate ești?"),
    31: ("Sono italiano", "Sunt italian"),
    32: ("Sono italiana", "Sunt italiancă"),
    33: ("E tu, vivi qui?", "Locuiești aici?"),
    34: ("Si, abito qui", "Da, locuiesc aici"),
    35: ("Mi chiamo Sara, e tu?", "Mă cheamă Sara. Pe tine cum te cheamă?"),
    36: ("Giuliano", "Iulian"),
    37: ("Che fai qui?", "Ce faci aici?"),
    38: ("Sono in vacanza", "Sunt în vacanță."),
    39: ("Siamo in vacanza", "Noi suntem în vacanță"),
    40: ("Sono in viaggio d'affari", "Sunt în deplasare de afaceri"),
    41: ("Lavoro qui", "Eu lucrez aici"),
    42: ("Lavoriamo qui", "Noi lucrăm aici"),
    43: ("Dove mi consigli di andare a mangiare?", "Unde putem să mâncăm?"),
    44: ("C'è un museo qui vicino?", "Este vre-un muzeu nu departe de aici?"),
    45: ("Dove posso collegarmi a internet?", "Unde mă pot conecta la internet?"),
    46: ("Vuoi imparare un po' di vocabolario?", "Vrei să înveți câteva cuvinte?"),
    47: ("Con piacere!", "Da, desigur"),
    48: ("Con piacere!", "Da, sigur că da"),
    49: ("Come si chiama?", "Cum se numește?"),
    50: ("È un tavolo", "Este o masă"),
    51: ("Un tavolo, hai capito?", "O masă, înțelegi?"),
    52: ("Non ho capito", "Nu înțeleg"),
    53: ("Puoi ripetere per favore?", "Poți să repeți, te rog?"),
    54: ("Puoi parlare più lentamente?", "N-ai putea să vorbești mai încet?"),
    55: ("Potresti scriverlo per favore?", "Te rog, n-ai putea s-o scrii?"),
    56: ("Ho capito", "Am înțeles"),
    57: ("Mi piace il colore di questo tavolo", "Îmi place culoarea acestei mese"),
    58: ("È rosso", "Este roșu"),
    59: ("È rosso", "Este roșie"),
    60: ("Blu", "Albastru"),
    61: ("Blu", "Albastră"),
    62: ("Giallo", "Galben"),
    63: ("Giallo", "Galbenă"),
    64: ("Bianco", "Alb"),
    65: ("Bianco", "Albă"),
    66: ("Nero", "Negru"),
    67: ("Nero", "Neagră"),
    68: ("Verde", "Verde"),
    69: ("Arancione", "Portocaliu"),
    70: ("Arancione", "Portocalie"),
    71: ("Viola", "Violet"),
    72: ("Viola", "Violetă"),
    73: ("Grigio", "Gri"),
    74: ("Zero", "Zero"),
    75: ("Uno", "Unu"),
    76: ("Due", "Doi"),
    77: ("Tre", "Trei"),
    78: ("Quattro", "Patru"),
    79: ("Cinque", "Cinci"),
    80: ("Sei", "Șase"),
    81: ("Sette", "Șapte"),
    82: ("Otto", "Opt"),
    83: ("Nove", "Nouă"),
    84: ("Dieci", "Zece"),
    85: ("Undici", "Unsprezece"),
    86: ("Dodici", "Doisprezece"),
    87: ("Tredici", "Treisprezece"),
    88: ("Quattordici", "Paisprezece"),
    89: ("Quindici", "Cincisprezece"),
    90: ("Sedici", "Șaisprezece"),
    91: ("Diciassette", "Șaptesprezece"),
    92: ("Diciotto", "Optsprezece"),
    93: ("Diciannove", "Nouăsprezece"),
    94: ("Venti", "Douăzeci"),
    95: ("Ventuno", "Douăzeci și unu"),
    96: ("Ventidue", "Douăzeci și doi"),
    97: ("Ventitre", "Douăzeci și trei"),
    98: ("Ventiquattro", "Douăzeci și patru"),
    99: ("Venticinque", "Douăzeci și cinci"),
    100: ("Ventisei", "Douăzeci și șase"),
    101: ("Ventisette", "Douăzeci și șapte"),
    102: ("Ventotto", "Douăzeci și opt"),
    103: ("Ventinove", "Douăzeci și nouă"),
    104: ("Trenta", "Treizeci"),
    105: ("Trentuno", "Treizeci și unu"),
    106: ("Trentadue", "Treizeci și doi"),
    107: ("Trentatre", "Treizeci și trei"),
    108: ("Trentaquattro", "Treizeci și patru"),
    109: ("Trentacinque", "Treizeci și cinci"),
    110: ("Trentasei", "Treizeci și șase"),
    111: ("Quaranta", "Patruzeci"),
    112: ("Cinquanta", "Cincizeci"),
    113: ("Sessanta", "Șaizeci"),
    114: ("Settanta", "Șaptezeci"),
    115: ("Ottanta", "Optzeci"),
    116: ("Novanta", "Nouăzeci"),
    117: ("Cento", "O sută"),
    118: ("Cento-cinque", "O sută cinci"),
    119: ("Duecento", "Două sute"),
    120: ("Trecento", "Trei sute"),
    121: ("Quattrocento", "Patru sute"),
    122: ("Mille", "O mie"),
    123: ("Millecinquecento", "O mie cinci sute"),
    124: ("Duemila", "Două mii"),
    125: ("Diecimila", "Zece mii"),
    126: ("Da quando sei qui?", "Cînd ai sosit?"),
    127: ("Da oggi", "Astăzi"),
    128: ("Da oggi", "Azi"),
    129: ("Da ieri", "Ieri"),
    130: ("Da due giorni", "Acum două zile"),
    131: ("Quanto tempo resti?", "Cât timp vei sta aici?"),
    132: ("Riparto domani", "Plec mîine"),
    133: ("Riparto dopodomani", "Plec poimîine"),
    134: ("Riparto tra tre giorni", "Plec peste trei zile"),
    135: ("Lunedì", "Luni"),
    136: ("Martedì", "Marți"),
    137: ("Mercoledì", "Miercuri"),
    138: ("Giovedì", "Joi"),
    139: ("Venerdì", "Vineri"),
    140: ("Sabato", "Sâmbătă"),
    141: ("Domenica", "Duminică"),
    142: ("Gennaio", "Ianuarie"),
    143: ("Febbraio", "Februarie"),
    144: ("Marzo", "Martie"),
    145: ("Aprile", "Aprilie"),
    146: ("Maggio", "Mai"),
    147: ("Giugno", "Iunie"),
    148: ("Luglio", "Iulie"),
    149: ("Agosto", "August"),
    150: ("Settembre", "Septembrie"),
    151: ("Ottobre", "Octombrie"),
    152: ("Novembre", "Noiembrie"),
    153: ("Dicembre", "Decembrie"),
    154: ("A che ora parti?", "La ce oră pleci?"),
    155: ("La mattina, alle otto", "Dimineața, la ora opt"),
    156: ("La mattina, alle otto e un quarto", "Dimineața, la opt și un sfert"),
    157: ("La mattina, alle otto e trenta", "Dimineața... la opt treizeci"),
    158: ("La mattina, alle otto e quarantacinque", "Dimineața... la opt patruzeci și cinci"),
    159: ("La sera, alle diciotto", "Seara... la ora optsprezece"),
    160: ("Sono in ritardo", "Am întârziat"),
    161: ("Taxi!", "Taxi!"),
    162: ("Dove vuole andare?", "Unde vreți să mergeți?"),
    163: ("Vado alla stazione", "La gară"),
    164: ("Vado all'hotel Giorno e Notte", "Merg la hotelul Zi și noapte"),
    165: ("Mi puo' portare all'aeroporto?", "Ați putea să mă duceți la aeroport?"),
    166: ("Puo' prendere i miei bagagli?", "Ați putea să-mi luați bagagele?"),
    167: ("È lontano da qui?", "Este departe de aici?"),
    168: ("È lontano da qui?", "E departe de aici?"),
    169: ("No è vicino", "Nu, este alături"),
    170: ("No è vicino", "Nu, e alături"),
    171: ("Sì è un po' più lontano", "Da, e ceva mai departe"),
    172: ("Quanto costa?", "Cât va costa?"),
    173: ("Mi porti qui per favore", "Duceți-mă acolo, vă rog."),
    174: ("A destra", "Este la dreapta"),
    175: ("A destra", "E la dreapta"),
    176: ("A sinistra", "Este la stânga"),
    177: ("A sinistra", "E la stînga"),
    178: ("Dritto", "Este drept înainte"),
    179: ("Dritto", "Este tot înainte"),
    180: ("È qui", "Este aici"),
    181: ("È qui", "E aici"),
    182: ("È di là", "Pe aici"),
    183: ("Alt!", "Stop!"),
    184: ("Faccia con comodo", "Nu vă grăbiți"),
    185: ("Mi puo' fare una ricevuta per favore?", "Ați putea să-mi pregătiți nota, vă rog"),
    186: ("Hai dei parenti qui?", "Ai rude aici?"),
    187: ("Mio padre", "Tatăl meu"),
    188: ("Mia madre", "Mama mea"),
    189: ("Mio figlio", "Fiul meu"),
    190: ("Mia figlia", "Fiica mea"),
    191: ("Un fratello", "Un frate"),
    192: ("Una sorella", "O soră"),
    193: ("Un amico", "Un prieten"),
    194: ("Un'amica", "O prietenă"),
    195: ("Il mio ragazzo", "Prietenul meu"),
    196: ("La mia ragazza", "Prietena mea"),
    197: ("Mio marito", "Soțul meu"),
    198: ("Mia moglie", "Soția mea"),
    199: ("Il tuo paese mi piace molto", "Îmi place mult țara ta"),
    200: ("Ti amo", "Te iubesc"),
    201: ("Sono felice", "Sunt fericit"),
    202: ("Sono triste", "Sunt trist"),
    203: ("Sto bene qui", "Mă simt bine aici"),
    204: ("Sento freddo", "Îmi este frig"),
    205: ("Sento caldo", "Îmi este cald"),
    206: ("È' troppo grande", "E prea mare"),
    207: ("È troppo piccolo", "E prea mic"),
    208: ("È perfetto", "E perfect"),
    209: ("Vuoi uscire stasera?", "Vrei să ieșim în seara aceasta?"),
    210: ("Vorrei uscire stasera", "Da, vreau să ieșim astă seară"),
    211: ("È una buon'idea", "E o idee bună"),
    212: ("Ho voglia di divertirmi", "Vreau să mă distrez"),
    213: ("Non è una buon'idea", "Nu e o idee bună"),
    214: ("Non ho voglia di uscire stasera", "Nu vreau să ieșim astă seară"),
    215: ("Ho voglia di riposarmi", "Vreau sămă odihnesc"),
    216: ("Vuoi fare sport?", "Vrei să faci sport?"),
    217: ("Sì, ho bisogno di sfogarmi!", "Da, am nevoie să mă defulez!"),
    218: ("Io gioco a tennis", "Eu joc tenis"),
    219: ("No grazie, sono abbastanza stanco", "Nu, mulțumesc, sunt obosit"),
    220: ("Il bar", "Barul"),
    221: ("Vuoi bere qualcosa?", "Vrei să bei ceva?"),
    222: ("Bere", "a bea"),
    223: ("Bicchiere", "un pahar"),
    224: ("Con piacere", "Cu plăcere"),
    225: ("Che cosa prendi?", "Ce iei?"),
    226: ("Che cosa c'è da bere?", "Ce este de băut?"),
    227: ("C'è dell' acqua o dei succhi di frutta", "Este apă sau suc de fructe"),
    228: ("Acqua", "apă"),
    229: ("Puo' aggiungere un po' di ghiaccio per favore?", "Ați putea să adăugați niște cuburi de gheață?"),
    230: ("Un po' di ghiaccio?", "Cuburi de gheață"),
    231: ("Una cioccolata", "Ciocolată"),
    232: ("Del latte", "Lapte"),
    233: ("Del tè", "Ceai"),
    234: ("Del caffè", "Cafea"),
    235: ("Con zucchero", "Cu zahăr"),
    236: ("Con panna", "Cu frișcă"),
    237: ("Del vino", "Vin"),
    238: ("Una birra", "Bere"),
    239: ("Un tè, per favore", "Un ceai, te rog!"),
    240: ("Una birra per favore", "O bere, te rog!"),
    241: ("Cosa vuoi bere?", "Ce vreți să beți?"),
    242: ("Due tè per favore", "Două ceaiuri, vă rog"),
    243: ("Due birre per favore", "Două beri, vă rog"),
    244: ("Niente, grazie", "Nimic, mulțumesc"),
    245: ("Alla tua", "Noroc!"),
    246: ("Salute", "Sănătate!"),
    247: ("Il conto per favore", "Nota, vă rog!"),
    248: ("Il conto per favore", "Plata, vă rog!"),
    249: ("Quanto Le devo, per favore?", "Cât vă datorez?"),
    250: ("Venti Euro", "Douăzeci de euro"),
    251: ("È per me", "Te invit"),
    252: ("Il ristorante", "Restaurantul"),
    253: ("Vuoi mangiare?", "Vrei să mănînci?"),
    254: ("Sì, ne ho voglia", "Da, vreau"),
    255: ("Mangiare", "A mânca"),
    256: ("Dove possiamo mangiare?", "Unde putem să mâncăm?"),
    257: ("Dove possiamo pranzare?", "Unde putem lua prânzul?"),
    258: ("La cena", "Cina"),
    259: ("La prima colazione", "Micul dejun"),
    260: ("Per favore!", "Vă rog!"),
    261: ("Il menu per favore!", "Meniul, vă rog!"),
    262: ("Ecco il menu!", "Poftiți meniul!"),
    263: ("Cosa preferisci? Carne o pesce?", "Ce preferi: carne sau pește?"),
    264: ("Con riso", "Cu orez"),
    265: ("Con pasta", "Cu paste făinoase"),
    266: ("Delle patate", "Cartofi"),
    267: ("Della verdura", "Legume"),
    268: ("Delle uova strapazzate - al tegamino - o alla coque", "Omletă - ochiuri - ou moale"),
    269: ("Del pane", "Pîine"),
    270: ("Del burro", "Unt"),
    271: ("Un'insalata", "O salată"),
    272: ("Un dolce", "Un desert"),
    273: ("Della frutta", "Fructe"),
    274: ("Ha un coltello per favore?", "Un cuțit, vă rog"),
    275: ("Sì, glielo porto subito", "Vi-l aduc imediat."),
    276: ("Un coltello", "Un cuțit."),
    277: ("Una forchetta", "O furculiță"),
    278: ("Un cucchiaio", "O lingură"),
    279: ("È un piatto caldo?", "Aceasta e o mâncare caldă?"),
    280: ("Sì, ed anche molto speziato!", "Da, și foarte picantă!"),
    281: ("Caldo", "Cald"),
    282: ("Freddo", "rece"),
    283: ("Speziato", "picant"),
    284: ("Prenderò il pesce!", "Voi lua pește!"),
    285: ("Prenderò il pesce!", "O să iau pește!"),
    286: ("Anch'io", "Și eu"),
    287: ("È tardi! Devo andare!", "E târziu, trebuie să plec"),
    288: ("Ci rivedremo?", "Am putea să ne revedem?"),
    289: ("Sì, certamente", "Da, cu plăcere"),
    290: ("Abito a quest'indirizzo", "Locuiesc la această adresă"),
    291: ("Hai un numero di telefono?", "Tu ai un număr de telefon?"),
    292: ("Sì, eccolo", "Da, iată-l"),
    293: ("Ho trascorso un momento piacevole con te", "Mi-a fost bine în compania ta"),
    294: ("Anch'io, mi ha fatto piacere incontrarti", "Și mie de asemenea. Îmi pare bine că te-am întâlnit"),
    295: ("Ci rivedremo presto", "Ne vom revedea curând"),
    296: ("Lo spero anch'io", "Sper și eu"),
    297: ("Arrivederci", "La revedere"),
    298: ("A domani", "Pe mâine!"),
    299: ("Ciao", "Salut!"),
    300: ("Per favore! Cerco la fermata dell'autobus", "Fiți amabil! Caut stația de autobuz"),
    301: ("Per favore! Cerco la fermata dell'autobus", "Fiți amabilă! Caut stația de autobuz"),
    302: ("Quanto costa il biglietto per La Città del Sole per favore?", "Vă rog, cât costă biletul pentru Orașul Soarelui?"),
    303: ("Dove va questo treno per favore?", "Unde merge trenul acesta?"),
    304: ("Questo treno si ferma alla Città del Sole?", "Acest tren se oprește în Orașul Soarelui?"),
    305: ("Quando parte il treno per la Città del Sole?", "Când pleacă trenul în Orașul Soarelui?"),
    306: ("Quando arriva il treno per la Città del Sole?", "Când sosește trenul în Orașul Soarelui?"),
    307: ("Un biglietto per La Città del Sole per favore", "Un bilet pentru Orașul Soarelui, vă rog!"),
    308: ("Conosce l'orario dei treni?", "Aveți orarul trenurilor?"),
    309: ("L'orario degli autobus", "Orarul aotobuzelor"),
    310: ("Qual è il treno per La Città del Sole per favore?", "Care este trenul pentru Orașul Soarelui, vă rog?"),
    311: ("È quello", "Acesta"),
    312: ("È quello", "Acela"),
    313: ("Grazie", "Mulțumesc"),
    314: ("Di niente. Buon Viaggio", "Cu plăcere. Călătorie plăcută!"),
    315: ("Il meccanico", "Atelierul de reparații"),
    316: ("La pompa di benzina", "Benzinăria"),
    317: ("Il pieno, per favore", "Plinul, vă rog"),
    318: ("Bici", "Bicicletă"),
    319: ("Il centro città", "Centrul orașului"),
    320: ("La periferia", "Periferie"),
    321: ("È una grande città", "E un oraș mare"),
    322: ("È un paese", "E un sat"),
    323: ("Una montagna", "Un munte"),
    324: ("Un lago", "Un lac"),
    325: ("La campagna", "Țară"),
    326: ("L'hotel", "Hotel"),
    327: ("Appartamento", "Apartament"),
    328: ("Benvenuti!", "Bine ai venit!"),
    329: ("Ha una camera libera?", "Aveți o cameră liberă?"),
    330: ("È una camera con bagno?", "Camera e cu bae?"),
    331: ("Preferisce due letti separati?", "Preferați cu două paturi?"),
    332: ("Desidera una camera doppia?", "Vreți o cameră dublă?"),
    333: ("Camera con vasca da bagno- con doccia- con balcone", "Cameră cu bae - cu balcon - cu duș"),
    334: ("Camera con la prima colazione", "Cameră cu micul dejun"),
    335: ("Qual è il prezzo per una notte?", "Cât costă o noapte?"),
    336: ("Prima vorrei vedere la camera, per favore!", "De la început ași vrea să văd camera, vă rog."),
    337: ("Sì, certo!", "Da, bineînțeles"),
    338: ("Grazie, la camera va benissimo.", "Mulțumesc, camera e foarte bună"),
    339: ("Va bene, posso prenotare per questa sera?", "O pot rezerva pentru această seară?"),
    340: ("La ringrazio, ma è troppo cara per me", "E prea scump pentru mine, mulțumesc"),
    341: ("Puo' prendere i miei bagagli, per favore?", "Ați putea să vă ocupați de bagajele mele?"),
    342: ("Dove si trova la mia camera, per favore?", "Unde se găsește camera mea, vă rog?"),
    343: ("È al primo piano", "Ea se găsește la primul etaj"),
    344: ("C'è un ascensore?", "Aveți un ascensor?"),
    345: ("L'ascensore è alla sua sinistra", "Ascensorul e la stânga"),
    346: ("L'ascensore è alla sua destra", "Ascensorul e la dreapta"),
    347: ("Dov'è la lavanderia?", "Unde se găsește spălătoria?"),
    348: ("È al pianterreno.", "Ea se găsește la parter"),
    349: ("Pianterreno.", "Parter"),
    350: ("Camera", "Cameră"),
    351: ("Lavanderia", "Călcatul rufelor"),
    352: ("Parrucchiere", "Frizerie"),
    353: ("Parcheggio auto", "Locuri de parcare"),
    354: ("Vediamoci nella sala conferenze?", "Ne întâlnim în sala de conferințe?"),
    355: ("La sala di riunione", "Sala de conferințe"),
    356: ("La piscina è riscaldata", "Piscina e încălzită"),
    357: ("La piscina", "O piscină"),
    358: ("Mi svegli alle sette per favore", "Treziți-mă, vă rog, la ora 7"),
    359: ("La chiave per favore", "Cheia, vă rog"),
    360: ("Il pass per favore", "Pasul, vă rog"),
    361: ("Ci sono messaggi per me?", "Este vre-un mesaj pentru mine?"),
    362: ("Sì, eccoli", "Da, iată-l"),
    363: ("No, non ha ricevuto nulla", "Nu, n-ați primit nimic"),
    364: ("Dove posso cambiare i soldi in spiccioli?", "Unde pot schimba banii?"),
    365: ("Mi puo' cambiare i soldi in spiccioli per favore?", "Ați putea să-mi schimbați banii, vă rog?"),
    366: ("Possiamo cambiarle i soldi. Quanti ne vuole cambiare?", "Da, câți bani vreți să schimbați?"),
    367: ("C'è Sara per favore?", "Sara este aici, vă rog?"),
    368: ("Sì, è qui", "Da, ea este aici"),
    369: ("È uscita", "Ea a ieșit"),
    370: ("Puo' chiamarla al cellulare", "Ați putea să-i telefonați pe telefonul portabil"),
    371: ("Sa dove posso trovarla?", "Știți unde o pot găsi?"),
    372: ("È andata al lavoro", "Ea-i la servici"),
    373: ("È a casa sua", "Ea e în camera ei"),
    374: ("C'è Giuliano per favore?", "Julien e aici, vă rog?"),
    375: ("Sì, è qui", "Da, el este aici"),
    376: ("È uscito", "el a ieșit"),
    377: ("Sa dove posso trovarlo?", "Știți unde îl pot găsi?"),
    378: ("Puo' chiamarlo al cellulare", "Ați putea să-i telefonați pe telefonul portabil"),
    379: ("È andato al lavoro", "El e la servici"),
    380: ("È a casa sua", "El e în camera lui"),
    381: ("La spiaggia", "O plajă"),
    382: ("Sa dove posso comprare un palloncino?", "Știți unde pot să cumpăr o minge?"),
    383: ("C'è un negozio da questa parte", "Este un magazin în această direcție?"),
    384: ("Un palloncino", "O minge"),
    385: ("Un binocolo", "Un binoclu"),
    386: ("Un berretto", "O caschetă"),
    387: ("Asciugamano", "Un șervet"),
    388: ("Sandali", "Niște sandale"),
    389: ("Secchiello", "O găleată"),
    390: ("Crema solare", "Cremă solară"),
    391: ("Costume da bagno maschile", "Costum de bae"),
    392: ("Occhiali da sole", "Ochelari de soare"),
    393: ("Crostaceo", "Crustacee"),
    394: ("Fare un bagno di sole", "A se bronza"),
    395: ("Assolato", "Însorit"),
    396: ("Tramonto", "Apusul soarelui"),
    397: ("Ombrellone", "Umbrelă"),
    398: ("Sole", "Soare"),
    399: ("Ombra", "Umbră"),
    400: ("Insolazione", "Insolație"),
    401: ("È pericoloso nuotare qui?", "E periculos de înotat aici?"),
    402: ("No, non è pericoloso", "Nu, nu e periculos"),
    403: ("Sì, è vietato farsi il bagno qui", "Da, e interzis de a înota aici"),
    404: ("Nuotare", "A înota"),
    405: ("Nuoto", "înot"),
    406: ("Onda", "Val"),
    407: ("Mare", "Mare"),
    408: ("Duna", "Dună"),
    409: ("Sabbia", "Nisip"),
    410: ("Quali sono le previsioni metereologiche per domani?", "Care este timpul probabil pe mâine?"),
    411: ("Il tempo sta cambiando", "Timpul se va schimba"),
    412: ("Pioverà", "Va ploua"),
    413: ("Ci sarà il sole", "Va fi soare"),
    414: ("Ci sarà molto vento", "Va fi vânt"),
    415: ("Costume da bagno", "Costum de baîe"),
    416: ("Mi può aiutare per favore?", "Mă puteți ajuta, vă rog?"),
    417: ("Mi sono perso", "M-am rătăcit"),
    418: ("Cosa desidera?", "Ce doriți?"),
    419: ("Che è successo?", "Ce s-a întâmplat?"),
    420: ("Dove posso trovare un interprete?", "Unde pot găsi un interpret?"),
    421: ("Dov'è la farmacia più vicina?", "Unde se găsește cea mai apropiată farmacie?"),
    422: ("Puo' chiamare un medico per favore?", "N-ați putea să chemați un doctor, vă rog?"),
    423: ("Che cura segue al momento?", "Ce tratament urmați în momentul de față?"),
    424: ("Un ospedale", "Un spital"),
    425: ("Una farmacia", "O farmacie"),
    426: ("Un medico", "Un doctor"),
    427: ("Servizio medico", "Serviciu medical"),
    428: ("Ho perso i documenti", "Mi-am pierdut actele"),
    429: ("Mi hanno rubato i documenti", "Mi-au furat actele"),
    430: ("Ufficio degli oggetti smarriti", "Biroul obiectelor găsite"),
    431: ("Posto di soccorso", "Postul de securitate"),
    432: ("Uscita di sicurezza", "Ieșire de serviciu"),
    433: ("La polizia", "Poliția"),
    434: ("Documenti", "Actele"),
    435: ("Soldi", "Banii"),
    436: ("Passaporto", "Pașaport"),
    437: ("Bagagli", "Bagaje"),
    438: ("No, grazie", "Nu, mulțumesc E în regulă"),
    439: ("Lasciami in pace!", "Lăsați-mă în pace!"),
    440: ("Vattene!", "Plecați!"),
}

# Frasi chiave del documento (quelle dei quiz) -> numero della voce audio corrispondente
FRASE_AUDIO = {
    "Patru": 78,
    "Șase": 80,
    "Șapte": 81,
    "Opt": 82,
    "Nouă": 83,
    "Bună ziua": 1,
    "Bună seara": 2,
    "La revedere": 3,
    "Vă rog": 7,
    "Mulțumesc": 8,
    "Cu plăcere": 11,
    "Da": 5,
    "Nu": 6,
    "Din ce țară ești?": 29,
    "Sunt italian": 31,
    "Sunt italiancă": 32,
    "Vorbești românește?": 26,
    "Nu înțeleg": 52,
    "Albastru": 60,
    "Galben": 62,
    "Alb": 64,
    "Verde": 68,
    "Zero": 74,
    "Unu": 75,
    "Doi": 76,
    "Trei": 77,
    "Cinci": 79,
    "Zece": 84,
    "Douăzeci": 94,
    "O sută": 117,
    "Astăzi": 127,
    "Ieri": 129,
    "Luni": 135,
    "Marți": 136,
    "Duminică": 141,
    "Ianuarie": 142,
    "Taxi": 161,
    "La gară": 163,
    "Sunt fericit": 201,
    "Sunt trist": 202,
    "Îmi este frig": 204,
    "Îmi este cald": 205,
    "Te iubesc": 200,
    "E o idee bună": 211,
    "Vreau să mă odihnesc": 215,
    "Apă": 228,
    "Cafea": 234,
    "Ceai": 233,
    "Lapte": 232,
    "Un pahar": 223,
    "Nota, vă rog": 247,
    "Cât vă datorez?": 249,
    "Meniul, vă rog": 261,
    "Pe mâine": 298,
    "Salut": 299,
    "Hotel": 326,
    "Cameră": 350,
    "Apartament": 327,
    "Cât costă o noapte?": 335,
    "Mare": 407,
    "Soare": 398,
    "Umbră": 399,
    "Nisip": 409,
    "A înota": 404,
    "Va ploua": 412,
    "Va fi vânt": 414,
    "Pașaport": 436,
    "Mi-am pierdut actele": 428,
}

MODULI_RUMENO = [
    {
        "ordine": 1,
        "materia": MATERIA_BASE,
        "titolo": "Modulo 1 - Saluti ed espressioni essenziali",
        "descrizione": "Salutare e usare formule di cortesia.",
        "voci": (1, 23),  # numeri dei file audio madrelingua (media/rumeno/audio/N.mp3)
        "video": ["Parole_Essenziali_nuova_versione.mp4"],
        "tracce": ["espressioni-essenziali.mp3"],  # ascolto completo (media/rumeno/tracce/)
        "frasi": [
            ("Bună ziua", "Buongiorno"),
            ("Bună seara", "Buonasera"),
            ("La revedere", "Arrivederci"),
            ("Vă rog", "Per favore"),
            ("Mulțumesc", "Grazie"),
            ("Cu plăcere", "Prego"),
            ("Da", "Sì"),
            ("Nu", "No"),
        ],
        "quiz": [
            {"domanda": "Come si dice in rumeno «Buongiorno»?",
             "opzioni": ["Bună seara", "La revedere", "Vă rog", "Bună ziua"], "corretta": 3,
             "spiegazione": "«Buongiorno» in rumeno si dice «Bună ziua»."},
            {"domanda": "Come si dice in rumeno «Per favore»?",
             "opzioni": ["Bună seara", "La revedere", "Vă rog", "Bună ziua"], "corretta": 2,
             "spiegazione": "«Per favore» in rumeno si dice «Vă rog»."},
            {"domanda": "Come si dice in rumeno «Sì»?",
             "opzioni": ["La revedere", "Da", "Bună ziua", "Bună seara"], "corretta": 1,
             "spiegazione": "«Sì» in rumeno si dice «Da»."},
            {"domanda": "Come si dice in rumeno «Buonasera»?",
             "opzioni": ["Bună seara", "Bună ziua", "La revedere", "Vă rog"], "corretta": 0,
             "spiegazione": "«Buonasera» in rumeno si dice «Bună seara»."},
            {"domanda": "Come si dice in rumeno «Grazie»?",
             "opzioni": ["Bună ziua", "Bună seara", "La revedere", "Mulțumesc"], "corretta": 3,
             "spiegazione": "«Grazie» in rumeno si dice «Mulțumesc»."},
        ],
    },
    {
        "ordine": 2,
        "materia": MATERIA_BASE,
        "titolo": "Modulo 2 - Presentarsi e conversare",
        "descrizione": "Dire nome, provenienza e attività.",
        "voci": (24, 45),  # numeri dei file audio madrelingua (media/rumeno/audio/N.mp3)
        "video": ["Dialogare_nuova_versione.mp4"],
        "tracce": ["conversazione.mp3"],  # ascolto completo (media/rumeno/tracce/)
        "frasi": [
            ("Cum te cheamă?", "Come ti chiami?"),
            ("Mă cheamă Sara", "Mi chiamo Sara"),
            ("Din ce țară ești?", "Di dove sei?"),
            ("Sunt italian", "Sono italiano"),
            ("Sunt italiancă", "Sono italiana"),
            ("Locuiesc aici", "Abito qui"),
            ("Lucrez aici", "Lavoro qui"),
            ("Vorbești românește?", "Parli rumeno?"),
        ],
        "quiz": [
            {"domanda": "Come si dice in rumeno «Come ti chiami?»?",
             "opzioni": ["Din ce țară ești?", "Sunt italian", "Cum te cheamă?", "Mă cheamă Sara"], "corretta": 2,
             "spiegazione": "«Come ti chiami?» in rumeno si dice «Cum te cheamă?»."},
            {"domanda": "Come si dice in rumeno «Sono italiano»?",
             "opzioni": ["Din ce țară ești?", "Sunt italian", "Cum te cheamă?", "Mă cheamă Sara"], "corretta": 1,
             "spiegazione": "«Sono italiano» in rumeno si dice «Sunt italian»."},
            {"domanda": "Come si dice in rumeno «Lavoro qui»?",
             "opzioni": ["Lucrez aici", "Cum te cheamă?", "Mă cheamă Sara", "Din ce țară ești?"], "corretta": 0,
             "spiegazione": "«Lavoro qui» in rumeno si dice «Lucrez aici»."},
            {"domanda": "Come si dice in rumeno «Mi chiamo Sara»?",
             "opzioni": ["Cum te cheamă?", "Din ce țară ești?", "Sunt italian", "Mă cheamă Sara"], "corretta": 3,
             "spiegazione": "«Mi chiamo Sara» in rumeno si dice «Mă cheamă Sara»."},
            {"domanda": "Come si dice in rumeno «Sono italiana»?",
             "opzioni": ["Mă cheamă Sara", "Din ce țară ești?", "Sunt italiancă", "Cum te cheamă?"], "corretta": 2,
             "spiegazione": "«Sono italiana» in rumeno si dice «Sunt italiancă»."},
        ],
    },
    {
        "ordine": 3,
        "materia": MATERIA_BASE,
        "titolo": "Modulo 3 - Imparare parole e colori",
        "descrizione": "Chiedere chiarimenti e descrivere colori.",
        "voci": (46, 73),  # numeri dei file audio madrelingua (media/rumeno/audio/N.mp3)
        "video": ["I_Colori_nuova_versione.mp4"],
        "tracce": ["imparare.mp3", "colori.mp3"],  # ascolto completo (media/rumeno/tracce/)
        "frasi": [
            ("Poți să repeți?", "Puoi ripetere?"),
            ("Vorbește mai încet", "Parla più lentamente"),
            ("Nu înțeleg", "Non capisco"),
            ("Roșu", "Rosso"),
            ("Albastru", "Blu"),
            ("Galben", "Giallo"),
            ("Alb", "Bianco"),
            ("Verde", "Verde"),
        ],
        "quiz": [
            {"domanda": "Come si dice in rumeno «Puoi ripetere?»?",
             "opzioni": ["Roșu", "Poți să repeți?", "Vorbește mai încet", "Nu înțeleg"], "corretta": 1,
             "spiegazione": "«Puoi ripetere?» in rumeno si dice «Poți să repeți?»."},
            {"domanda": "Come si dice in rumeno «Rosso»?",
             "opzioni": ["Roșu", "Poți să repeți?", "Vorbește mai încet", "Nu înțeleg"], "corretta": 0,
             "spiegazione": "«Rosso» in rumeno si dice «Roșu»."},
            {"domanda": "Come si dice in rumeno «Bianco»?",
             "opzioni": ["Poți să repeți?", "Vorbește mai încet", "Nu înțeleg", "Alb"], "corretta": 3,
             "spiegazione": "«Bianco» in rumeno si dice «Alb»."},
            {"domanda": "Come si dice in rumeno «Parla più lentamente»?",
             "opzioni": ["Nu înțeleg", "Roșu", "Vorbește mai încet", "Poți să repeți?"], "corretta": 2,
             "spiegazione": "«Parla più lentamente» in rumeno si dice «Vorbește mai încet»."},
            {"domanda": "Come si dice in rumeno «Blu»?",
             "opzioni": ["Nu înțeleg", "Albastru", "Poți să repeți?", "Vorbește mai încet"], "corretta": 1,
             "spiegazione": "«Blu» in rumeno si dice «Albastru»."},
        ],
    },
    {
        "ordine": 4,
        "materia": MATERIA_BASE,
        "titolo": "Modulo 4 - Numeri e quantità",
        "descrizione": "Leggere numeri e prezzi.",
        "voci": (74, 125),  # numeri dei file audio madrelingua (media/rumeno/audio/N.mp3)
        "video": ["I_Numeri_nuova_versione.mp4"],
        "tracce": ["numeri.mp3"],  # ascolto completo (media/rumeno/tracce/)
        "frasi": [
            ("Zero", "Zero"),
            ("Unu", "Uno"),
            ("Doi", "Due"),
            ("Trei", "Tre"),
            ("Patru", "Quattro"),
            ("Cinci", "Cinque"),
            ("Șase", "Sei"),
            ("Șapte", "Sette"),
            ("Opt", "Otto"),
            ("Nouă", "Nove"),
            ("Zece", "Dieci"),
            ("Douăzeci", "Venti"),
            ("O sută", "Cento"),
        ],
        "quiz": [
            {"domanda": "Come si dice in rumeno «Zero»?",
             "opzioni": ["Zero", "Unu", "Doi", "Trei"], "corretta": 0,
             "spiegazione": "«Zero» in rumeno si dice «Zero»."},
            {"domanda": "Come si dice in rumeno «Tre»?",
             "opzioni": ["Zero", "Unu", "Doi", "Trei"], "corretta": 3,
             "spiegazione": "«Tre» in rumeno si dice «Trei»."},
            {"domanda": "Come si dice in rumeno «Venti»?",
             "opzioni": ["Unu", "Doi", "Douăzeci", "Zero"], "corretta": 2,
             "spiegazione": "«Venti» in rumeno si dice «Douăzeci»."},
            {"domanda": "Come si dice in rumeno «Uno»?",
             "opzioni": ["Trei", "Unu", "Zero", "Doi"], "corretta": 1,
             "spiegazione": "«Uno» in rumeno si dice «Unu»."},
            {"domanda": "Come si dice in rumeno «Cinque»?",
             "opzioni": ["Cinci", "Zero", "Unu", "Doi"], "corretta": 0,
             "spiegazione": "«Cinque» in rumeno si dice «Cinci»."},
        ],
    },
    {
        "ordine": 5,
        "materia": MATERIA_BASE,
        "titolo": "Modulo 5 - Tempo, calendario e orari",
        "descrizione": "Parlare di date e orari.",
        "voci": (126, 160),  # numeri dei file audio madrelingua (media/rumeno/audio/N.mp3)
        "video": ["Riferimenti_Temporali_nuova_versione.mp4"],
        "tracce": ["punti-di-riferimento-di-tempo.mp3"],  # ascolto completo (media/rumeno/tracce/)
        "frasi": [
            ("Astăzi", "Oggi"),
            ("Ieri", "Ieri"),
            ("Mâine", "Domani"),
            ("Luni", "Lunedì"),
            ("Marți", "Martedì"),
            ("Duminică", "Domenica"),
            ("Ianuarie", "Gennaio"),
            ("La ce oră?", "A che ora?"),
        ],
        "quiz": [
            {"domanda": "Come si dice in rumeno «Oggi»?",
             "opzioni": ["Ieri", "Mâine", "Luni", "Astăzi"], "corretta": 3,
             "spiegazione": "«Oggi» in rumeno si dice «Astăzi»."},
            {"domanda": "Come si dice in rumeno «Lunedì»?",
             "opzioni": ["Ieri", "Mâine", "Luni", "Astăzi"], "corretta": 2,
             "spiegazione": "«Lunedì» in rumeno si dice «Luni»."},
            {"domanda": "Come si dice in rumeno «Gennaio»?",
             "opzioni": ["Mâine", "Ianuarie", "Astăzi", "Ieri"], "corretta": 1,
             "spiegazione": "«Gennaio» in rumeno si dice «Ianuarie»."},
            {"domanda": "Come si dice in rumeno «Ieri»?",
             "opzioni": ["Ieri", "Astăzi", "Mâine", "Luni"], "corretta": 0,
             "spiegazione": "«Ieri» in rumeno si dice «Ieri»."},
            {"domanda": "Come si dice in rumeno «Martedì»?",
             "opzioni": ["Astăzi", "Ieri", "Mâine", "Marți"], "corretta": 3,
             "spiegazione": "«Martedì» in rumeno si dice «Marți»."},
        ],
    },
    {
        "ordine": 6,
        "materia": MATERIA_BASE,
        "titolo": "Modulo 6 - Taxi e indicazioni",
        "descrizione": "Muoversi in città.",
        "voci": (161, 185),  # numeri dei file audio madrelingua (media/rumeno/audio/N.mp3)
        "video": ["Taxi_nuova_versione.mp4"],
        "tracce": ["taxi.mp3"],  # ascolto completo (media/rumeno/tracce/)
        "frasi": [
            ("Taxi", "Taxi"),
            ("La gară", "Alla stazione"),
            ("La aeroport", "All'aeroporto"),
            ("La dreapta", "A destra"),
            ("La stânga", "A sinistra"),
            ("Drept înainte", "Dritto"),
            ("Este departe?", "È lontano?"),
            ("Cât costă?", "Quanto costa?"),
        ],
        "quiz": [
            {"domanda": "Come si dice in rumeno «Taxi»?",
             "opzioni": ["La aeroport", "La dreapta", "Taxi", "La gară"], "corretta": 2,
             "spiegazione": "«Taxi» in rumeno si dice «Taxi»."},
            {"domanda": "Come si dice in rumeno «A destra»?",
             "opzioni": ["La aeroport", "La dreapta", "Taxi", "La gară"], "corretta": 1,
             "spiegazione": "«A destra» in rumeno si dice «La dreapta»."},
            {"domanda": "Come si dice in rumeno «È lontano?»?",
             "opzioni": ["Este departe?", "Taxi", "La gară", "La aeroport"], "corretta": 0,
             "spiegazione": "«È lontano?» in rumeno si dice «Este departe?»."},
            {"domanda": "Come si dice in rumeno «Alla stazione»?",
             "opzioni": ["Taxi", "La aeroport", "La dreapta", "La gară"], "corretta": 3,
             "spiegazione": "«Alla stazione» in rumeno si dice «La gară»."},
            {"domanda": "Come si dice in rumeno «A sinistra»?",
             "opzioni": ["La gară", "La aeroport", "La stânga", "Taxi"], "corretta": 2,
             "spiegazione": "«A sinistra» in rumeno si dice «La stânga»."},
        ],
    },
    {
        "ordine": 7,
        "materia": MATERIA_BASE,
        "titolo": "Modulo 7 - Famiglia e relazioni",
        "descrizione": "Nominare familiari e amici.",
        "voci": (186, 198),  # numeri dei file audio madrelingua (media/rumeno/audio/N.mp3)
        "video": ["Famiglia_ed_Emozioni_nuova_versione.mp4"],
        "tracce": ["famiglia.mp3"],  # ascolto completo (media/rumeno/tracce/)
        "frasi": [
            ("Tată", "Padre"),
            ("Mamă", "Madre"),
            ("Fiu", "Figlio"),
            ("Fiică", "Figlia"),
            ("Frate", "Fratello"),
            ("Soră", "Sorella"),
            ("Prieten", "Amico"),
            ("Prietenă", "Amica"),
        ],
        "quiz": [
            {"domanda": "Come si dice in rumeno «Padre»?",
             "opzioni": ["Fiică", "Tată", "Mamă", "Fiu"], "corretta": 1,
             "spiegazione": "«Padre» in rumeno si dice «Tată»."},
            {"domanda": "Come si dice in rumeno «Figlia»?",
             "opzioni": ["Fiică", "Tată", "Mamă", "Fiu"], "corretta": 0,
             "spiegazione": "«Figlia» in rumeno si dice «Fiică»."},
            {"domanda": "Come si dice in rumeno «Amico»?",
             "opzioni": ["Tată", "Mamă", "Fiu", "Prieten"], "corretta": 3,
             "spiegazione": "«Amico» in rumeno si dice «Prieten»."},
            {"domanda": "Come si dice in rumeno «Madre»?",
             "opzioni": ["Fiu", "Fiică", "Mamă", "Tată"], "corretta": 2,
             "spiegazione": "«Madre» in rumeno si dice «Mamă»."},
            {"domanda": "Come si dice in rumeno «Fratello»?",
             "opzioni": ["Fiu", "Frate", "Tată", "Mamă"], "corretta": 1,
             "spiegazione": "«Fratello» in rumeno si dice «Frate»."},
        ],
    },
    {
        "ordine": 8,
        "materia": MATERIA_BASE,
        "titolo": "Modulo 8 - Sentimenti e tempo libero",
        "descrizione": "Esprimere emozioni e fare inviti.",
        "voci": (199, 219),  # numeri dei file audio madrelingua (media/rumeno/audio/N.mp3)
        "video": ["Famiglia_ed_Emozioni_nuova_versione.mp4"],
        "tracce": ["sentimenti.mp3"],  # ascolto completo (media/rumeno/tracce/)
        "frasi": [
            ("Sunt fericit", "Sono felice"),
            ("Sunt trist", "Sono triste"),
            ("Îmi este frig", "Ho freddo"),
            ("Îmi este cald", "Ho caldo"),
            ("Te iubesc", "Ti amo"),
            ("Vrei să ieșim?", "Vuoi uscire?"),
            ("E o idee bună", "È una buona idea"),
            ("Vreau să mă odihnesc", "Voglio riposare"),
        ],
        "quiz": [
            {"domanda": "Come si dice in rumeno «Sono felice»?",
             "opzioni": ["Sunt fericit", "Sunt trist", "Îmi este frig", "Îmi este cald"], "corretta": 0,
             "spiegazione": "«Sono felice» in rumeno si dice «Sunt fericit»."},
            {"domanda": "Come si dice in rumeno «Ho caldo»?",
             "opzioni": ["Sunt fericit", "Sunt trist", "Îmi este frig", "Îmi este cald"], "corretta": 3,
             "spiegazione": "«Ho caldo» in rumeno si dice «Îmi este cald»."},
            {"domanda": "Come si dice in rumeno «È una buona idea»?",
             "opzioni": ["Sunt trist", "Îmi este frig", "E o idee bună", "Sunt fericit"], "corretta": 2,
             "spiegazione": "«È una buona idea» in rumeno si dice «E o idee bună»."},
            {"domanda": "Come si dice in rumeno «Sono triste»?",
             "opzioni": ["Îmi este cald", "Sunt trist", "Sunt fericit", "Îmi este frig"], "corretta": 1,
             "spiegazione": "«Sono triste» in rumeno si dice «Sunt trist»."},
            {"domanda": "Come si dice in rumeno «Ti amo»?",
             "opzioni": ["Te iubesc", "Sunt fericit", "Sunt trist", "Îmi este frig"], "corretta": 0,
             "spiegazione": "«Ti amo» in rumeno si dice «Te iubesc»."},
        ],
    },
    {
        "ordine": 9,
        "materia": MATERIA_BASE,
        "titolo": "Modulo 9 - Al bar",
        "descrizione": "Ordinare bevande e pagare.",
        "voci": (220, 251),  # numeri dei file audio madrelingua (media/rumeno/audio/N.mp3)
        "video": ["Al_Bar_nuova_versione.mp4"],
        "tracce": ["bar.mp3"],  # ascolto completo (media/rumeno/tracce/)
        "frasi": [
            ("Apă", "Acqua"),
            ("Cafea", "Caffè"),
            ("Ceai", "Tè"),
            ("Lapte", "Latte"),
            ("Zahăr", "Zucchero"),
            ("Un pahar", "Un bicchiere"),
            ("Nota, vă rog", "Il conto, per favore"),
            ("Cât vă datorez?", "Quanto devo?"),
        ],
        "quiz": [
            {"domanda": "Come si dice in rumeno «Acqua»?",
             "opzioni": ["Cafea", "Ceai", "Lapte", "Apă"], "corretta": 3,
             "spiegazione": "«Acqua» in rumeno si dice «Apă»."},
            {"domanda": "Come si dice in rumeno «Latte»?",
             "opzioni": ["Cafea", "Ceai", "Lapte", "Apă"], "corretta": 2,
             "spiegazione": "«Latte» in rumeno si dice «Lapte»."},
            {"domanda": "Come si dice in rumeno «Il conto, per favore»?",
             "opzioni": ["Ceai", "Nota, vă rog", "Apă", "Cafea"], "corretta": 1,
             "spiegazione": "«Il conto, per favore» in rumeno si dice «Nota, vă rog»."},
            {"domanda": "Come si dice in rumeno «Caffè»?",
             "opzioni": ["Cafea", "Apă", "Ceai", "Lapte"], "corretta": 0,
             "spiegazione": "«Caffè» in rumeno si dice «Cafea»."},
            {"domanda": "Come si dice in rumeno «Zucchero»?",
             "opzioni": ["Apă", "Cafea", "Ceai", "Zahăr"], "corretta": 3,
             "spiegazione": "«Zucchero» in rumeno si dice «Zahăr»."},
        ],
    },
    {
        "ordine": 10,
        "materia": MATERIA_BASE,
        "titolo": "Modulo 10 - Al ristorante",
        "descrizione": "Leggere un menu e ordinare.",
        "voci": (252, 286),  # numeri dei file audio madrelingua (media/rumeno/audio/N.mp3)
        "video": ["Al_Ristorante_nuova_versione.mp4"],
        "tracce": ["ristorante.mp3"],  # ascolto completo (media/rumeno/tracce/)
        "frasi": [
            ("Restaurant", "Ristorante"),
            ("Meniu", "Menu"),
            ("Pâine", "Pane"),
            ("Apă", "Acqua"),
            ("Pește", "Pesce"),
            ("Carne", "Carne"),
            ("Salată", "Insalata"),
            ("Meniul, vă rog", "Il menu, per favore"),
        ],
        "quiz": [
            {"domanda": "Come si dice in rumeno «Ristorante»?",
             "opzioni": ["Pâine", "Apă", "Restaurant", "Meniu"], "corretta": 2,
             "spiegazione": "«Ristorante» in rumeno si dice «Restaurant»."},
            {"domanda": "Come si dice in rumeno «Acqua»?",
             "opzioni": ["Pâine", "Apă", "Restaurant", "Meniu"], "corretta": 1,
             "spiegazione": "«Acqua» in rumeno si dice «Apă»."},
            {"domanda": "Come si dice in rumeno «Insalata»?",
             "opzioni": ["Salată", "Restaurant", "Meniu", "Pâine"], "corretta": 0,
             "spiegazione": "«Insalata» in rumeno si dice «Salată»."},
            {"domanda": "Come si dice in rumeno «Menu»?",
             "opzioni": ["Restaurant", "Pâine", "Apă", "Meniu"], "corretta": 3,
             "spiegazione": "«Menu» in rumeno si dice «Meniu»."},
            {"domanda": "Come si dice in rumeno «Pesce»?",
             "opzioni": ["Meniu", "Pâine", "Pește", "Restaurant"], "corretta": 2,
             "spiegazione": "«Pesce» in rumeno si dice «Pește»."},
        ],
    },
    {
        "ordine": 11,
        "materia": MATERIA_BASE,
        "titolo": "Modulo 11 - Commiato e trasporti",
        "descrizione": "Congedarsi e viaggiare in treno o autobus.",
        "voci": (287, 325),  # numeri dei file audio madrelingua (media/rumeno/audio/N.mp3)
        "video": ["Dividersi_nuova_versione.mp4", "I_Trasporti_nuova_versione.mp4"],
        "tracce": ["lasciarsi.mp3", "trasporto.mp3"],  # ascolto completo (media/rumeno/tracce/)
        "frasi": [
            ("Pe mâine", "A domani"),
            ("Salut", "Ciao"),
            ("Număr de telefon", "Numero di telefono"),
            ("Autobuz", "Autobus"),
            ("Tren", "Treno"),
            ("Bilet", "Biglietto"),
            ("Gară", "Stazione"),
            ("Călătorie plăcută", "Buon viaggio"),
        ],
        "quiz": [
            {"domanda": "Come si dice in rumeno «A domani»?",
             "opzioni": ["Autobuz", "Pe mâine", "Salut", "Număr de telefon"], "corretta": 1,
             "spiegazione": "«A domani» in rumeno si dice «Pe mâine»."},
            {"domanda": "Come si dice in rumeno «Autobus»?",
             "opzioni": ["Autobuz", "Pe mâine", "Salut", "Număr de telefon"], "corretta": 0,
             "spiegazione": "«Autobus» in rumeno si dice «Autobuz»."},
            {"domanda": "Come si dice in rumeno «Stazione»?",
             "opzioni": ["Pe mâine", "Salut", "Număr de telefon", "Gară"], "corretta": 3,
             "spiegazione": "«Stazione» in rumeno si dice «Gară»."},
            {"domanda": "Come si dice in rumeno «Ciao»?",
             "opzioni": ["Număr de telefon", "Autobuz", "Salut", "Pe mâine"], "corretta": 2,
             "spiegazione": "«Ciao» in rumeno si dice «Salut»."},
            {"domanda": "Come si dice in rumeno «Treno»?",
             "opzioni": ["Număr de telefon", "Tren", "Pe mâine", "Salut"], "corretta": 1,
             "spiegazione": "«Treno» in rumeno si dice «Tren»."},
        ],
    },
    {
        "ordine": 12,
        "materia": MATERIA_BASE,
        "titolo": "Modulo 12 - Hotel e alloggio",
        "descrizione": "Prenotare una camera e usare i servizi.",
        "voci": (326, 366),  # numeri dei file audio madrelingua (media/rumeno/audio/N.mp3)
        "video": ["In_Hotel_nuova_versione.mp4"],
        "tracce": ["hotel.mp3"],  # ascolto completo (media/rumeno/tracce/)
        "frasi": [
            ("Hotel", "Hotel"),
            ("Cameră", "Camera"),
            ("Apartament", "Appartamento"),
            ("O noapte", "Una notte"),
            ("Ascensor", "Ascensore"),
            ("Cheie", "Chiave"),
            ("Cameră liberă", "Camera libera"),
            ("Cât costă o noapte?", "Quanto costa una notte?"),
        ],
        "quiz": [
            {"domanda": "Come si dice in rumeno «Hotel»?",
             "opzioni": ["Hotel", "Cameră", "Apartament", "O noapte"], "corretta": 0,
             "spiegazione": "«Hotel» in rumeno si dice «Hotel»."},
            {"domanda": "Come si dice in rumeno «Una notte»?",
             "opzioni": ["Hotel", "Cameră", "Apartament", "O noapte"], "corretta": 3,
             "spiegazione": "«Una notte» in rumeno si dice «O noapte»."},
            {"domanda": "Come si dice in rumeno «Camera libera»?",
             "opzioni": ["Cameră", "Apartament", "Cameră liberă", "Hotel"], "corretta": 2,
             "spiegazione": "«Camera libera» in rumeno si dice «Cameră liberă»."},
            {"domanda": "Come si dice in rumeno «Camera»?",
             "opzioni": ["O noapte", "Cameră", "Hotel", "Apartament"], "corretta": 1,
             "spiegazione": "«Camera» in rumeno si dice «Cameră»."},
            {"domanda": "Come si dice in rumeno «Ascensore»?",
             "opzioni": ["Ascensor", "Hotel", "Cameră", "Apartament"], "corretta": 0,
             "spiegazione": "«Ascensore» in rumeno si dice «Ascensor»."},
        ],
    },
    {
        "ordine": 13,
        "materia": MATERIA_BASE,
        "titolo": "Modulo 13 - Cercare e contattare persone",
        "descrizione": "Chiedere di una persona e telefonare.",
        "voci": (367, 380),  # numeri dei file audio madrelingua (media/rumeno/audio/N.mp3)
        "video": ["Cercare_Qualcuno_nuova_versione.mp4"],
        "tracce": ["cercare-qualcuno.mp3"],  # ascolto completo (media/rumeno/tracce/)
        "frasi": [
            ("Este aici", "È qui"),
            ("A ieșit", "È uscita"),
            ("Este la serviciu", "È al lavoro"),
            ("Acasă", "A casa"),
            ("Telefon", "Telefono"),
            ("Telefon mobil", "Cellulare"),
            ("Unde o pot găsi?", "Dove posso trovarla?"),
            ("Puteți să o sunați?", "Può chiamarla?"),
        ],
        "quiz": [
            {"domanda": "Come si dice in rumeno «È qui»?",
             "opzioni": ["A ieșit", "Este la serviciu", "Acasă", "Este aici"], "corretta": 3,
             "spiegazione": "«È qui» in rumeno si dice «Este aici»."},
            {"domanda": "Come si dice in rumeno «A casa»?",
             "opzioni": ["A ieșit", "Este la serviciu", "Acasă", "Este aici"], "corretta": 2,
             "spiegazione": "«A casa» in rumeno si dice «Acasă»."},
            {"domanda": "Come si dice in rumeno «Dove posso trovarla?»?",
             "opzioni": ["Este la serviciu", "Unde o pot găsi?", "Este aici", "A ieșit"], "corretta": 1,
             "spiegazione": "«Dove posso trovarla?» in rumeno si dice «Unde o pot găsi?»."},
            {"domanda": "Come si dice in rumeno «È uscita»?",
             "opzioni": ["A ieșit", "Este aici", "Este la serviciu", "Acasă"], "corretta": 0,
             "spiegazione": "«È uscita» in rumeno si dice «A ieșit»."},
            {"domanda": "Come si dice in rumeno «Telefono»?",
             "opzioni": ["Este aici", "A ieșit", "Este la serviciu", "Telefon"], "corretta": 3,
             "spiegazione": "«Telefono» in rumeno si dice «Telefon»."},
        ],
    },
    {
        "ordine": 14,
        "materia": MATERIA_BASE,
        "titolo": "Modulo 14 - Spiaggia, vacanze e meteo",
        "descrizione": "Parlare del mare e delle previsioni.",
        "voci": (381, 415),  # numeri dei file audio madrelingua (media/rumeno/audio/N.mp3)
        "video": ["Vacanza_nuova_versione.mp4"],
        "tracce": ["spiaggia.mp3"],  # ascolto completo (media/rumeno/tracce/)
        "frasi": [
            ("Plajă", "Spiaggia"),
            ("Mare", "Mare"),
            ("Soare", "Sole"),
            ("Umbră", "Ombra"),
            ("Nisip", "Sabbia"),
            ("A înota", "Nuotare"),
            ("Va ploua", "Pioverà"),
            ("Va fi vânt", "Ci sarà vento"),
        ],
        "quiz": [
            {"domanda": "Come si dice in rumeno «Spiaggia»?",
             "opzioni": ["Soare", "Umbră", "Plajă", "Mare"], "corretta": 2,
             "spiegazione": "«Spiaggia» in rumeno si dice «Plajă»."},
            {"domanda": "Come si dice in rumeno «Ombra»?",
             "opzioni": ["Soare", "Umbră", "Plajă", "Mare"], "corretta": 1,
             "spiegazione": "«Ombra» in rumeno si dice «Umbră»."},
            {"domanda": "Come si dice in rumeno «Pioverà»?",
             "opzioni": ["Va ploua", "Plajă", "Mare", "Soare"], "corretta": 0,
             "spiegazione": "«Pioverà» in rumeno si dice «Va ploua»."},
            {"domanda": "Come si dice in rumeno «Mare»?",
             "opzioni": ["Plajă", "Soare", "Umbră", "Mare"], "corretta": 3,
             "spiegazione": "«Mare» in rumeno si dice «Mare»."},
            {"domanda": "Come si dice in rumeno «Sabbia»?",
             "opzioni": ["Mare", "Soare", "Nisip", "Plajă"], "corretta": 2,
             "spiegazione": "«Sabbia» in rumeno si dice «Nisip»."},
        ],
    },
    {
        "ordine": 15,
        "materia": MATERIA_BASE,
        "titolo": "Modulo 15 - Problemi ed emergenze",
        "descrizione": "Chiedere aiuto e segnalare problemi.",
        "voci": (416, 440),  # numeri dei file audio madrelingua (media/rumeno/audio/N.mp3)
        "video": ["In_caso_di_problema_nuova_versione.mp4"],
        "tracce": ["in-caso-di-problema.mp3"],  # ascolto completo (media/rumeno/tracce/)
        "frasi": [
            ("Ajutor", "Aiuto"),
            ("Mă puteți ajuta?", "Mi può aiutare?"),
            ("Spital", "Ospedale"),
            ("Farmacie", "Farmacia"),
            ("Medic", "Medico"),
            ("Poliție", "Polizia"),
            ("Pașaport", "Passaporto"),
            ("Mi-am pierdut actele", "Ho perso i documenti"),
        ],
        "quiz": [
            {"domanda": "Come si dice in rumeno «Aiuto»?",
             "opzioni": ["Farmacie", "Ajutor", "Mă puteți ajuta?", "Spital"], "corretta": 1,
             "spiegazione": "«Aiuto» in rumeno si dice «Ajutor»."},
            {"domanda": "Come si dice in rumeno «Farmacia»?",
             "opzioni": ["Farmacie", "Ajutor", "Mă puteți ajuta?", "Spital"], "corretta": 0,
             "spiegazione": "«Farmacia» in rumeno si dice «Farmacie»."},
            {"domanda": "Come si dice in rumeno «Passaporto»?",
             "opzioni": ["Ajutor", "Mă puteți ajuta?", "Spital", "Pașaport"], "corretta": 3,
             "spiegazione": "«Passaporto» in rumeno si dice «Pașaport»."},
            {"domanda": "Come si dice in rumeno «Mi può aiutare?»?",
             "opzioni": ["Spital", "Farmacie", "Mă puteți ajuta?", "Ajutor"], "corretta": 2,
             "spiegazione": "«Mi può aiutare?» in rumeno si dice «Mă puteți ajuta?»."},
            {"domanda": "Come si dice in rumeno «Medico»?",
             "opzioni": ["Spital", "Medic", "Ajutor", "Mă puteți ajuta?"], "corretta": 1,
             "spiegazione": "«Medico» in rumeno si dice «Medic»."},
        ],
    },
]

ICONE_MODULI = {1: "👋", 2: "🗣️", 3: "🎨", 4: "🔢", 5: "📅", 6: "🚕", 7: "👨‍👩‍👧", 8: "😊", 9: "☕", 10: "🍽️", 11: "🚆", 12: "🏨", 13: "📞", 14: "🏖️", 15: "🆘"}

EMOJI = {
    "Patru": "4️⃣",
    "Șase": "6️⃣",
    "Șapte": "7️⃣",
    "Opt": "8️⃣",
    "Nouă": "9️⃣",
    "Bună ziua": "🌞",
    "Bună seara": "🌆",
    "La revedere": "🙋",
    "Vă rog": "🙏",
    "Mulțumesc": "🙏",
    "Cu plăcere": "😊",
    "Da": "👍",
    "Nu": "👎",
    "Cum te cheamă?": "❓",
    "Mă cheamă Sara": "🙋‍♀️",
    "Din ce țară ești?": "🌍",
    "Sunt italian": "🇮🇹",
    "Sunt italiancă": "🇮🇹",
    "Locuiesc aici": "🏠",
    "Lucrez aici": "💼",
    "Vorbești românește?": "💬",
    "Poți să repeți?": "🔁",
    "Vorbește mai încet": "🐢",
    "Nu înțeleg": "🤷",
    "Roșu": "🟥",
    "Albastru": "🟦",
    "Galben": "🟨",
    "Alb": "⬜",
    "Verde": "🟩",
    "Zero": "0️⃣",
    "Unu": "1️⃣",
    "Doi": "2️⃣",
    "Trei": "3️⃣",
    "Cinci": "5️⃣",
    "Zece": "🔟",
    "Douăzeci": "2️⃣0️⃣",
    "O sută": "💯",
    "Astăzi": "📍",
    "Ieri": "⏪",
    "Mâine": "⏩",
    "Luni": "📅",
    "Marți": "📅",
    "Duminică": "🎉",
    "Ianuarie": "❄️",
    "La ce oră?": "⏰",
    "Taxi": "🚕",
    "La gară": "🚉",
    "La aeroport": "✈️",
    "La dreapta": "➡️",
    "La stânga": "⬅️",
    "Drept înainte": "⬆️",
    "Este departe?": "📏",
    "Cât costă?": "💶",
    "Tată": "👨",
    "Mamă": "👩",
    "Fiu": "👦",
    "Fiică": "👧",
    "Frate": "🧑",
    "Soră": "👩‍🦰",
    "Prieten": "🤝",
    "Prietenă": "🤝",
    "Sunt fericit": "😄",
    "Sunt trist": "😢",
    "Îmi este frig": "🥶",
    "Îmi este cald": "🥵",
    "Te iubesc": "❤️",
    "Vrei să ieșim?": "🎟️",
    "E o idee bună": "💡",
    "Vreau să mă odihnesc": "😴",
    "Apă": "💧",
    "Cafea": "☕",
    "Ceai": "🍵",
    "Lapte": "🥛",
    "Zahăr": "🍬",
    "Un pahar": "🥃",
    "Nota, vă rog": "🧾",
    "Cât vă datorez?": "💳",
    "Restaurant": "🍽️",
    "Meniu": "📋",
    "Pâine": "🍞",
    "Pește": "🐟",
    "Carne": "🥩",
    "Salată": "🥗",
    "Meniul, vă rog": "📋",
    "Pe mâine": "👋",
    "Salut": "👋",
    "Număr de telefon": "📱",
    "Autobuz": "🚌",
    "Tren": "🚆",
    "Bilet": "🎫",
    "Gară": "🚉",
    "Călătorie plăcută": "🧳",
    "Hotel": "🏨",
    "Cameră": "🛏️",
    "Apartament": "🏢",
    "O noapte": "🌙",
    "Ascensor": "🛗",
    "Cheie": "🔑",
    "Cameră liberă": "✅",
    "Cât costă o noapte?": "💶",
    "Este aici": "📍",
    "A ieșit": "🚪",
    "Este la serviciu": "💼",
    "Acasă": "🏠",
    "Telefon": "☎️",
    "Telefon mobil": "📱",
    "Unde o pot găsi?": "🔎",
    "Puteți să o sunați?": "📞",
    "Plajă": "🏖️",
    "Mare": "🌊",
    "Soare": "☀️",
    "Umbră": "⛱️",
    "Nisip": "🏝️",
    "A înota": "🏊",
    "Va ploua": "🌧️",
    "Va fi vânt": "💨",
    "Ajutor": "🆘",
    "Mă puteți ajuta?": "🙋",
    "Spital": "🏥",
    "Farmacie": "💊",
    "Medic": "🩺",
    "Poliție": "👮",
    "Pașaport": "🛂",
    "Mi-am pierdut actele": "📄",
}


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


def lezione(modulo):
    """Testo della lezione (docente virtuale + obiettivo + come si studia)."""
    v1, v2 = modulo["voci"]
    return (f"**Obiettivo del modulo:** {modulo['descrizione']}\n\n"
            f"> 🎙️ *{TESTO_DOCENTE}*\n\n"
            f"**Come si studia questo modulo**\n"
            f"1. Guarda la video lezione.\n"
            f"2. Leggi l'italiano, ascolta il rumeno e ripeti due volte.\n"
            f"3. Riconosci le frasi senza guardare il testo.\n"
            f"4. Fai gli esercizi «Abbina» e «Ascolta».\n"
            f"5. Supera il quiz finale con almeno l'80% (4 risposte su 5). Puoi ripeterlo quando vuoi.")


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
            "Video": link_video(m),
        }
        for m in sorted(MODULI_RUMENO, key=lambda x: x["ordine"])
    ]


def link_video(modulo):
    """Primo link video esterno del modulo ("" se non c'e')."""
    for nome in modulo.get("video", []):
        if VIDEO_LINK.get(nome):
            return VIDEO_LINK[nome]
    return ""


def sorgente_video(nome):
    """{"tipo": "locale"|"link", "url": ...} oppure None se il video non c'e' ancora.
    Il file nel progetto ha la precedenza: solo li' si puo' bloccare l'avanzamento veloce."""
    file = nome_file_video(nome)
    if os.path.exists(os.path.join(CARTELLA_VIDEO, file)):
        return {"tipo": "locale", "url": URL_VIDEO + file}
    if VIDEO_LINK.get(nome):
        return {"tipo": "link", "url": VIDEO_LINK[nome]}
    return None


def video_modulo(modulo):
    """Lista di (nome_file, link) dei video del modulo."""
    return [(nome, sorgente_video(nome)) for nome in modulo.get("video", [])]


def file_voce(numero):
    """Percorso dell'audio madrelingua n. «numero», None se il file non c'e'."""
    percorso = os.path.join(CARTELLA_AUDIO, f"{int(numero)}.mp3")
    return percorso if os.path.exists(percorso) else None


def voci_modulo(modulo):
    """Numeri delle voci audio madrelingua del modulo che esistono davvero."""
    v1, v2 = modulo["voci"]
    return [n for n in range(v1, v2 + 1) if file_voce(n)]


def tracce_modulo(modulo):
    """Percorsi delle tracce di ascolto completo del modulo che esistono davvero."""
    if not VERSIONE_PRO:
        return []
    percorsi = [os.path.join(CARTELLA_TRACCE, nome) for nome in modulo.get("tracce", [])]
    return [p for p in percorsi if os.path.exists(p)]


def elementi(modulo):
    """Schede da imparare: le 8 frasi del documento (versione PRO: anche le altre voci del frasario).
    Ogni scheda: {ro, pron, it, emoji, tipo, audio, voce}."""
    icona = ICONE_MODULI.get(modulo["ordine"], "💬")
    schede, usate = [], set()
    for ro, it in modulo["frasi"]:
        n = (modulo.get("audio_frasi") or {}).get(ro) or FRASE_AUDIO.get(ro)
        if n:
            usate.add(n)
        schede.append({"ro": ro, "pron": "", "it": it, "emoji": EMOJI.get(ro, icona), "tipo": "⭐ Frase del modulo",
                        "audio": file_voce(n) if n else None, "voce": n})
    if not VERSIONE_PRO:
        return schede
    v1, v2 = modulo["voci"]
    for n in range(v1, v2 + 1):
        if n in usate or n not in FRASARIO:
            continue
        it, ro = FRASARIO[n]
        schede.append({"ro": ro, "pron": "", "it": it, "emoji": EMOJI.get(ro, icona), "tipo": f"Voce {n} del frasario",
                        "audio": file_voce(n), "voce": n})
    return schede


def frasi_chiave(modulo):
    """Solo le 8 frasi chiave (servono agli esercizi brevi)."""
    return [s for s in elementi(modulo) if s["tipo"].startswith("⭐")]


def testo_da_leggere(ro):
    """Testo per la sintesi vocale."""
    return ro.replace("→", ",").replace(" / ", ", ")


# ----------------------------------------------------------------------
# PERSONALIZZAZIONI DAL PANNELLO DI CONTROLLO
# Il pannello salva un dizionario (config) che viene applicato sopra i contenuti predefiniti.
# ----------------------------------------------------------------------
import copy as _copy

_BASE_MODULI = _copy.deepcopy(MODULI_RUMENO)
_BASE_TESTI = {"NOME_CORSO": NOME_CORSO, "ORE_CORSO": ORE_CORSO, "TESTO_DOCENTE": TESTO_DOCENTE,
               "BENVENUTO": _copy.deepcopy(BENVENUTO), "GUIDA_TAPPE": _copy.deepcopy(GUIDA_TAPPE)}


def testi_predefiniti():
    b = _BASE_TESTI["BENVENUTO"]
    return {"nome_corso": _BASE_TESTI["NOME_CORSO"], "ore": _BASE_TESTI["ORE_CORSO"],
            "testo_docente": _BASE_TESTI["TESTO_DOCENTE"], "titolo_menu": "Lingua Rumena",
            "benvenuto_titolo": b["titolo"], "benvenuto_sottotitolo": b["sottotitolo"],
            "obiettivo": b["obiettivo"], "motto": b["motto"], "chiusura": b["chiusura"],
            **{f"guida_{k}": v for k, v in _BASE_TESTI["GUIDA_TAPPE"].items()}}


def modulo_predefinito(ordine):
    return next(m for m in _BASE_MODULI if m["ordine"] == ordine)


def applica_personalizzazioni(cfg):
    """Rimette i contenuti predefiniti e ci applica sopra la config del pannello."""
    global NOME_CORSO, ORE_CORSO, TESTO_DOCENTE, TITOLO_MENU, _INDICE
    cfg = cfg or {}
    testi = {**testi_predefiniti(), **{k: v for k, v in (cfg.get("testi") or {}).items() if v not in (None, "")}}
    NOME_CORSO = testi["nome_corso"]
    try:
        ORE_CORSO = int(testi["ore"])
    except Exception:
        ORE_CORSO = _BASE_TESTI["ORE_CORSO"]
    TESTO_DOCENTE = testi["testo_docente"]
    TITOLO_MENU = testi["titolo_menu"]
    BENVENUTO.clear()
    BENVENUTO.update(_copy.deepcopy(_BASE_TESTI["BENVENUTO"]))
    BENVENUTO.update({"titolo": testi["benvenuto_titolo"], "sottotitolo": testi["benvenuto_sottotitolo"],
                      "obiettivo": testi["obiettivo"], "motto": testi["motto"], "chiusura": testi["chiusura"]})
    GUIDA_TAPPE.clear()
    GUIDA_TAPPE.update({k: testi[f"guida_{k}"] for k in _BASE_TESTI["GUIDA_TAPPE"]})
    MODULI_RUMENO[:] = _copy.deepcopy(_BASE_MODULI)
    for m in MODULI_RUMENO:
        mod = (cfg.get("moduli") or {}).get(str(m["ordine"])) or {}
        if mod.get("nome"):
            m["nome"] = mod["nome"]          # il "titolo" resta fisso: serve a riconoscere i moduli superati
        if mod.get("descrizione"):
            m["descrizione"] = mod["descrizione"]
        if mod.get("frasi"):
            m["frasi"] = [(f[0], f[1]) for f in mod["frasi"] if f and f[0] and f[1]]
            m["audio_frasi"] = {f[0]: int(f[2]) for f in mod["frasi"] if f and f[0] and len(f) > 2 and str(f[2]).strip().isdigit()}
        if mod.get("quiz"):
            m["quiz"] = [{"domanda": q["domanda"], "opzioni": q["opzioni"], "corretta": int(q["corretta"]),
                          "spiegazione": f"Risposta giusta: «{q['opzioni'][int(q['corretta'])]}»."}
                         for q in mod["quiz"] if q.get("domanda") and len(q.get("opzioni", [])) == 4]
    _INDICE = {_norm(m["titolo"]): m for m in MODULI_RUMENO}


TITOLO_MENU = "Lingua Rumena"
