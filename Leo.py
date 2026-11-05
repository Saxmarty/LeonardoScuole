import streamlit as st
import pandas as pd
import requests
import base64
import html
import io
import json
import random
import zlib
import os

import streamlit.components.v1 as components

try:
    import corso_rumeno
except Exception:
    corso_rumeno = None

try:
    import attestato
except Exception:
    attestato = None
from datetime import date

# 1. CONFIGURAZIONE PAGINA
st.set_page_config(
    page_title="Leonardo Scuole - Area Riservata",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# FONT UNIFORME AL SITO leonardoscuole.it (Poppins)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,400&display=swap');
html, body, .stApp, p, h1, h2, h3, h4, h5, h6, label, li, td, th, a, button, input, textarea, select, summary,
div[data-testid="stMarkdownContainer"], div[data-testid="stMarkdownContainer"] *, div[data-testid="stCaptionContainer"],
div[data-testid="stTable"] *, div[data-testid="stAlert"] *, div[data-baseweb="select"] *, div[data-testid="stTab"] * {
    font-family: 'Poppins', sans-serif !important;
}
span[data-testid="stIconMaterial"], .material-symbols-rounded, .material-icons {
    font-family: 'Material Symbols Rounded' !important;
}
</style>
""", unsafe_allow_html=True)

# CONFIGURAZIONE RISERVATA: letta dai "Secrets" di Streamlit Cloud (non sta piu' nel codice).
# Streamlit Cloud -> app -> Settings -> Secrets. In locale: file .streamlit/secrets.toml (non va su GitHub).
def _leggi_secret(chiave, obbligatorio=True):
    try:
        valore = str(st.secrets[chiave]).strip()
    except Exception:
        valore = ""
    if obbligatorio and not valore:
        st.error(f"⚙️ Configurazione mancante: imposta **{chiave}** nei Secrets dell'app su Streamlit Cloud.")
        st.stop()
    return valore

WEB_APP_URL = _leggi_secret("WEB_APP_URL")
SPREADSHEET_CATALOGO_ID = _leggi_secret("SPREADSHEET_CATALOGO_ID")
CATALOGO_GID = _leggi_secret("CATALOGO_GID")
EMAIL_ADMIN = _leggi_secret("EMAIL_ADMIN")
# Chiave condivisa con lo script Google: lo script rifiuta le richieste che non la contengono.
APPS_SCRIPT_TOKEN = _leggi_secret("APPS_SCRIPT_TOKEN")

# IMMAGINI PREDEFINITE PER MATERIE
IMMAGINI_MATERIE = {
    "Matematica": "https://images.unsplash.com/photo-1635070041078-e363dbe005cb?auto=format&fit=crop&w=600&q=80",
    "Fisica": "https://images.unsplash.com/photo-1636466497217-26a8cbeaf0aa?auto=format&fit=crop&w=600&q=80",
    "Lingua e Letteratura Italiana": "https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?auto=format&fit=crop&w=600&q=80",
    "Lingua e Cultura Latina": "https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?auto=format&fit=crop&w=600&q=80",
    "Lingua e Cultura Straniera (Inglese)": "https://images.unsplash.com/photo-1543269865-cbf427effbad?auto=format&fit=crop&w=600&q=80",
    "Storia e Geografia": "https://images.unsplash.com/photo-1461360370896-922624d12aa1?auto=format&fit=crop&w=600&q=80",
    "Storia": "https://images.unsplash.com/photo-1461360370896-922624d12aa1?auto=format&fit=crop&w=600&q=80",
    "Filosofia": "https://images.unsplash.com/photo-1507842217343-583bb7270b66?auto=format&fit=crop&w=600&q=80",
    "Scienze Naturali": "https://images.unsplash.com/photo-1532094349884-543bc11b234d?auto=format&fit=crop&w=600&q=80",
    "Disegno e Storia dell'Arte": "https://images.unsplash.com/photo-1579783900882-c0d3dad7b119?auto=format&fit=crop&w=600&q=80",
    "Educazione Civica": "https://images.unsplash.com/photo-1541872703-74c5e44368f9?auto=format&fit=crop&w=600&q=80",
    "Lingua Rumena - Base": "https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?auto=format&fit=crop&w=600&q=80",
    "Grammatica Rumena": "https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?auto=format&fit=crop&w=600&q=80"
}
IMMAGINE_DEFAULT = "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?auto=format&fit=crop&w=600&q=80"

# 2. SESSION STATE
if "autenticato" not in st.session_state:
    st.session_state.autenticato = False

if "dati_utente" not in st.session_state:
    st.session_state.dati_utente = {}

if "sezione_attiva" not in st.session_state:
    st.session_state.sezione_attiva = "Corsi"

if "open_login" not in st.session_state:
    st.session_state.open_login = False

if "open_recupero" not in st.session_state:
    st.session_state.open_recupero = False

if "quiz_aperto" not in st.session_state:
    st.session_state.quiz_aperto = None

if "esiti_quiz" not in st.session_state:
    st.session_state.esiti_quiz = {}

if "password_cambiata_successo" not in st.session_state:
    st.session_state.password_cambiata_successo = False

if "moduli_completati" not in st.session_state:
    st.session_state.moduli_completati = set()

if "risultati_quiz" not in st.session_state:
    st.session_state.risultati_quiz = {
        "Test Iniziale": 28,
        "Quiz Modulo 1": 30,
        "Verifica Intermedia": 27
    }

if "materia_selezionata_sidebar" not in st.session_state:
    st.session_state.materia_selezionata_sidebar = "Tutte le Materie"

if "materia_attiva_card" not in st.session_state:
    st.session_state.materia_attiva_card = None

if "sidebar_aperta" not in st.session_state:
    st.session_state.sidebar_aperta = False

if "moduli_aperti" not in st.session_state:
    st.session_state.moduli_aperti = {}

if "date_corso" not in st.session_state:
    st.session_state.date_corso = {}  # {"inizio": "gg/mm/aaaa", "fine": "gg/mm/aaaa"}

ATTESTATO_FIRMATARIO = _leggi_secret("ATTESTATO_FIRMATARIO", obbligatorio=False) or "Ciro Di Dato"
ATTESTATO_LUOGO = _leggi_secret("ATTESTATO_LUOGO", obbligatorio=False) or "Napoli"
# LOGO UFFICIALE (file nel progetto: non dipende piu' da ImgBB)
LOGO_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "media", "logo_leonardo_scuole.jpg")
LOGO_URL_RISERVA = "https://leonardoscuole.it/wp-content/uploads/2026/02/TV1-copia-2.jpg"
try:
    with open(LOGO_FILE, "rb") as _f:
        LOGO_BYTES = _f.read()
    LOGO_SRC = "data:image/jpeg;base64," + base64.b64encode(LOGO_BYTES).decode("ascii")
except Exception:
    LOGO_BYTES = None
    LOGO_SRC = LOGO_URL_RISERVA


# 3. FUNZIONI BACKEND
@st.cache_data(ttl=30)
def carica_catalogo_corsi():
    url = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_CATALOGO_ID}/export?format=csv&gid={CATALOGO_GID}"
    try:
        df = pd.read_csv(url)
        rinomina_colonne = {
            'Indirizzo Studio': 'Indirizzo_Studio', 'Indirizzo_Studio': 'Indirizzo_Studio',
            'Anno_Scolastico:': 'Anno', 'Anno_Scolastico': 'Anno', 'Anno Scolastico': 'Anno', 'Anno': 'Anno',
            'NOME_MATERIA': 'Materia', 'Nome_Materia': 'Materia', 'Materia': 'Materia',
            'NomeModulo': 'Argomento', 'Argomento': 'Argomento',
            'DescrizioneModulo': 'Descrizione', 'Descrizione': 'Descrizione',
            'FileDispensa': 'Dispensa', 'Dispensa': 'Dispensa',
            'VideoLezione': 'Video', 'Video': 'Video'
        }
        df = df.rename(columns=lambda c: rinomina_colonne.get(str(c).strip(), str(c).strip()))
    except Exception as e:
        st.error(f"Errore nel caricamento del catalogo: {e}")
        df = pd.DataFrame()
    return aggiungi_corso_rumeno(df)

def aggiungi_corso_rumeno(df):
    """Aggiunge al catalogo i moduli del Corso Rumeno (corso_rumeno.py) non ancora presenti nel foglio."""
    if corso_rumeno is None:
        return df
    presenti = set()
    if not df.empty and {'Indirizzo_Studio', 'Argomento'}.issubset(df.columns):
        for ind, arg in zip(df['Indirizzo_Studio'], df['Argomento']):
            presenti.add((str(ind).strip().lower(), str(arg).strip().lower()))
    nuove = [r for r in corso_rumeno.righe_catalogo()
             if (r['Indirizzo_Studio'].lower(), r['Argomento'].lower()) not in presenti]
    if not nuove:
        return df
    return pd.concat([df, pd.DataFrame(nuove)], ignore_index=True)

def chiama_script(azione, **campi):
    """Invia un'azione allo script Google (sempre con la chiave segreta). Restituisce il testo della risposta, "" se irraggiungibile."""
    payload = {"azione": azione, **campi}
    if APPS_SCRIPT_TOKEN:
        payload["token"] = APPS_SCRIPT_TOKEN
    try:
        res = requests.post(WEB_APP_URL, data=payload, timeout=20)
        if res.status_code != 200:
            st.session_state["ultimo_errore_script"] = f"HTTP {res.status_code}"
            return ""
        testo = res.text.strip()
        if testo.startswith("<"):
            st.session_state["ultimo_errore_script"] = "pagina HTML (indirizzo dello script errato o deployment non accessibile a 'Chiunque')"
            return ""
        return testo
    except Exception as e:
        st.session_state["ultimo_errore_script"] = f"connessione fallita ({type(e).__name__})"
        return ""

def verifica_credenziali(email_input, password_input, ricordami_spuntato):
    """Il controllo della password avviene dentro lo script Google: il foglio utenti puo' restare privato."""
    email_clean = email_input.strip().lower()
    password_clean = str(password_input).strip()
    testo = chiama_script("LOGIN", email=email_clean, password=password_clean)
    try:
        risposta = json.loads(testo)
    except Exception:
        if testo == "UNAUTHORIZED":
            motivo = "chiave segreta non valida (APPS_SCRIPT_TOKEN nei Secrets diverso da APP_TOKEN nello script)"
        elif testo == "ERROR":
            motivo = "errore interno dello script Google"
        elif testo == "UNKNOWN_ACTION":
            motivo = "lo script attivo è ancora la versione vecchia"
        elif testo:
            motivo = f"risposta inattesa: {testo[:60]}"
        else:
            motivo = st.session_state.pop("ultimo_errore_script", "nessuna risposta")
        st.error(f"Servizio di accesso non raggiungibile. Motivo: {motivo}")
        return False

    esito = risposta.get("esito")
    if esito == "SCADUTO":
        st.error(f"⛔ Il tuo abbonamento è scaduto il {risposta.get('data_scadenza', '')}. Contatta la segreteria per rinnovarlo.")
        return False
    if esito == "BLOCCATO":
        st.error("⛔ Troppi tentativi errati: accesso bloccato per 15 minuti.")
        return False
    if esito != "OK":
        st.error("❌ Email o password non corrette.")
        return False

    utente = risposta.get("utente", {})
    stato_utente = str(utente.get("stato", "Attivo")).strip()
    if stato_utente.lower() != "attivo":
        st.error(f"⛔ Accesso negato: Account '{stato_utente}'. Contatta la segreteria.")
        return False

    foto_url = str(utente.get("foto", "")).strip()
    st.session_state.dati_utente = {
        "id_cliente": str(utente.get("id_cliente", "1")),
        "nominativo": utente.get("nominativo", email_clean),
        "stato": stato_utente,
        "email": email_clean,
        "password": password_clean,
        "data_scadenza": str(utente.get("data_scadenza", "-")),
        "pacchetto": str(utente.get("pacchetto", "Liceo Scientifico")),
        "foto": foto_url if foto_url.lower() != "nan" else "",
        "primo_accesso": bool(utente.get("primo_accesso", False))
    }
    return True


# 3b. LEZIONI E QUIZ INTERATTIVI (Corso Rumeno)
def trova_lezione(titolo_argomento):
    if corso_rumeno is None:
        return None
    return corso_rumeno.trova_modulo(titolo_argomento)

def render_lezione(modulo):
    tab_lez, tab_frasi = st.tabs(["📖 Lezione", "💬 Frasario del modulo"])
    with tab_lez:
        st.markdown(corso_rumeno.lezione(modulo))
    with tab_frasi:
        righe = [(s["voce"] or "", s["it"], s["ro"]) for s in corso_rumeno.elementi(modulo)]
        st.dataframe(pd.DataFrame(righe, columns=["Voce", "Italiano", "Rumeno"]), use_container_width=True, hide_index=True)


def soglia_voto(modulo):
    """Voto minimo in trentesimi: 80% per il corso di rumeno."""
    if corso_rumeno is not None and corso_rumeno.trova_modulo(modulo.get("titolo")):
        return round(30 * corso_rumeno.SOGLIA_QUIZ)
    return 18


# PROGRESSI SALVATI SUL FOGLIO GOOGLE (azioni SALVA_PROGRESSI / LEGGI_PROGRESSI dello script).
# Se lo script non le conosce ancora, la piattaforma funziona lo stesso (progressi solo per la sessione).
def salva_progressi():
    dati = st.session_state.get("dati_utente", {})
    if not dati.get("email"):
        return
    pacchetto = {
        "completati": sorted(st.session_state.moduli_completati),
        "voti": {k: v for k, v in st.session_state.risultati_quiz.items() if k.startswith("Rumeno · ")},
        "date": st.session_state.date_corso,
        "tappe": {str(k): sorted(v) for k, v in st.session_state.get("ro", {}).get("fatte", {}).items()},
        "video_visti": sorted(st.session_state.get("ro", {}).get("video_visti", set())),
        "intro_vista": st.session_state.get("ro", {}).get("intro_vista", False),
    }
    chiama_script("SALVA_PROGRESSI", email=dati.get("email"), password=dati.get("password", ""),
                  progressi=json.dumps(pacchetto, ensure_ascii=False))

def carica_progressi():
    dati = st.session_state.get("dati_utente", {})
    testo = chiama_script("LEGGI_PROGRESSI", email=dati.get("email", ""), password=dati.get("password", ""))
    try:
        pacchetto = json.loads(testo) if testo else {}
        if isinstance(pacchetto, str):
            pacchetto = json.loads(pacchetto)
    except Exception:
        return
    if not isinstance(pacchetto, dict):
        return
    st.session_state.moduli_completati |= set(pacchetto.get("completati", []))
    st.session_state.risultati_quiz.update(pacchetto.get("voti", {}))
    st.session_state.date_corso.update(pacchetto.get("date", {}))
    rs = _stato_ro()
    for k, v in pacchetto.get("tappe", {}).items():
        rs["fatte"].setdefault(int(k), set()).update(v)
    rs.setdefault("video_visti", set()).update(pacchetto.get("video_visti", []))
    rs["intro_vista"] = rs.get("intro_vista") or bool(pacchetto.get("intro_vista"))

def segna_attivita_corso():
    """Registra la data di inizio del corso alla prima attività."""
    if "inizio" not in st.session_state.date_corso:
        st.session_state.date_corso["inizio"] = date.today().strftime("%d/%m/%Y")

def render_quiz(modulo, chiave):
    titolo = modulo["titolo"]
    domande = modulo["quiz"]
    soglia = soglia_voto(modulo)
    st.markdown(f"<h4 style='color:#7D001E; font-weight:800;'>📝 Quiz: {titolo}</h4>", unsafe_allow_html=True)
    st.caption(f"{len(domande)} domande · superi il modulo con almeno {soglia}/30 · puoi ripeterlo quando vuoi")

    with st.form(f"form_quiz_{chiave}"):
        risposte = []
        for n, q in enumerate(domande, start=1):
            # Ordine delle opzioni mescolato ma stabile (non cambia a ogni ricarica)
            opzioni = list(q["opzioni"])
            random.Random(zlib.crc32(q["domanda"].encode("utf-8"))).shuffle(opzioni)
            risposte.append(st.radio(f"**{n}. {q['domanda']}**", opzioni, index=None, key=f"quiz_{chiave}_{n}"))
        consegnato = st.form_submit_button("✅ Consegna il quiz", type="primary", use_container_width=True)

    if consegnato:
        if any(r is None for r in risposte):
            st.warning("⚠️ Rispondi a tutte le domande prima di consegnare.")
        else:
            corrette = [r == q["opzioni"][q["corretta"]] for q, r in zip(domande, risposte)]
            voto = round(sum(corrette) / len(domande) * 30)
            st.session_state.esiti_quiz[titolo] = {"voto": voto, "corrette": corrette, "risposte": risposte}
            chiave_voto = f"Rumeno · {titolo}"
            st.session_state.risultati_quiz[chiave_voto] = max(voto, st.session_state.risultati_quiz.get(chiave_voto, 0))
            if voto >= soglia:
                st.session_state.moduli_completati.add(titolo)
                if corso_rumeno is not None and all(m["titolo"] in st.session_state.moduli_completati for m in corso_rumeno.MODULI_RUMENO):
                    st.session_state.date_corso.setdefault("fine", date.today().strftime("%d/%m/%Y"))
            salva_progressi()

    esito = st.session_state.esiti_quiz.get(titolo)
    if esito:
        n_ok = sum(esito["corrette"])
        if esito["voto"] >= soglia:
            st.success(f"🎉 Voto: **{esito['voto']}/30** ({n_ok}/{len(domande)} risposte esatte). Modulo superato e segnato come completato!")
        else:
            st.error(f"📚 Voto: **{esito['voto']}/30** ({n_ok}/{len(domande)} risposte esatte). Ripassa la lezione e riprova.")
        with st.expander("🔍 Rivedi le risposte", expanded=esito["voto"] < soglia):
            for n, (q, ok, r) in enumerate(zip(domande, esito["corrette"], esito["risposte"]), start=1):
                icona = "✅" if ok else "❌"
                st.markdown(f"{icona} **{n}. {q['domanda']}**  \nLa tua risposta: *{r}* · Corretta: **{q['opzioni'][q['corretta']]}**  \n<span style='color:#475569;'>{q['spiegazione']}</span>", unsafe_allow_html=True)


# 3b-bis. PLAYER VIDEO DELLE LEZIONI (stile Netflix: "Prossimo" negli ultimi secondi, niente avanzamento veloce)
try:
    _player_lezione = components.declare_component(
        "player_lezione", path=os.path.join(os.path.dirname(os.path.abspath(__file__)), "componenti", "player_lezione"))
except Exception:
    _player_lezione = None

def player_lezione(url, chiave, prossimo="", visto=False, anticipo=12, auto=True, secondi_auto=8):
    """Mostra il video; restituisce l'evento nuovo ("finito" / "prossimo") oppure None."""
    if _player_lezione is None:
        st.video(url)
        return None
    valore = _player_lezione(src=url, prossimo=prossimo, libero=True, anticipo=anticipo,
                             auto=auto, secondi_auto=secondi_auto, key=chiave, default=None)
    if not isinstance(valore, dict):
        return None
    gestiti = st.session_state.setdefault("eventi_player", {})
    if gestiti.get(chiave) == valore.get("t"):
        return None
    gestiti[chiave] = valore.get("t")
    return valore.get("evento")


# 3c. CORSO DI RUMENO A TAPPE (Video -> Impara -> Abbina -> Ascolta -> Quiz finale)
TAPPE_RO = [("🎬", "Video"), ("🗣️", "Impara"), ("🎮", "Abbina"), ("🎧", "Ascolta"), ("🏁", "Quiz finale")]
T_VIDEO, T_IMPARA, T_ABBINA, T_ASCOLTA, T_QUIZ = range(5)
DOMANDE_ESERCIZIO = 6
SOGLIA_ESERCIZIO = 5  # risposte giuste su 6 (80%) per segnare la tappa come fatta

STILI_CORSO_RO = """
<style>
.ro-card { background:#ffffff; border:1.5px solid #ECECEC; border-radius:18px; overflow:hidden;
           box-shadow:0 12px 28px rgba(141,2,31,0.10); margin-bottom:14px; text-align:center; }
.ro-banda { background:linear-gradient(135deg,#8D021F 0%,#5E0015 100%); color:#ffffff; font-size:1.8rem; font-weight:800; padding:20px 18px 22px 18px; line-height:1.25; }
.ro-banda-k, .ro-it-k { color:#F3E32A; font-size:0.68rem; font-weight:700; letter-spacing:1.6px; margin-bottom:4px; }
.ro-it-k { color:#8D021F; margin-top:4px; }
.ro-tag { display:inline-block; background:#FFF8D6; color:#5E0015; border-radius:30px; padding:4px 12px; font-size:0.75rem; font-weight:600; margin:8px 4px 0 4px; }
.ro-lezione { background:#ffffff; border:1.5px solid #ECECEC; border-radius:18px; padding:20px 24px; margin-bottom:16px; box-shadow:0 8px 20px rgba(141,2,31,0.06); }
.ro-lezione-doc { background:#FFF8D6; border-left:4px solid #F3E32A; border-radius:10px; padding:12px 16px; color:#5E0015; font-size:0.92rem; margin-bottom:16px; }
.ro-lezione-k { color:#8D021F; font-weight:700; font-size:0.72rem; letter-spacing:1.5px; margin-bottom:10px; }
.ro-passi { display:grid; grid-template-columns:repeat(auto-fit,minmax(170px,1fr)); gap:10px; }
.ro-passo { display:flex; gap:10px; align-items:flex-start; background:#FCFAF5; border-radius:12px; padding:10px 12px; color:#1F2326; font-size:0.85rem; line-height:1.35; }
.ro-passo-n { flex:0 0 26px; height:26px; border-radius:50%; background:linear-gradient(135deg,#8D021F,#5E0015); color:#F3E32A; font-weight:800; font-size:0.8rem; display:flex; align-items:center; justify-content:center; }
/* pulsanti delle tappe interne: pillole come sul sito */
.st-key-ro_contenuto div[data-testid="stButton"] > button, .st-key-ro_contenuto div[data-testid="stPopover"] button,
.st-key-ro_contenuto div[data-testid="stFormSubmitButton"] > button {
    border-radius:30px !important; font-weight:600 !important; min-height:42px !important; }
.st-key-ro_contenuto div[data-testid="stButton"] > button[kind="secondary"], .st-key-ro_contenuto div[data-testid="stPopover"] button {
    background:#ffffff !important; color:#1F2326 !important; border:1.5px solid #1F2326 !important; }
.st-key-ro_contenuto div[data-testid="stButton"] > button[kind="secondary"] p { color:#1F2326 !important; }
.st-key-ro_contenuto div[data-testid="stButton"] > button[kind="secondary"]:hover { background:#F3E32A !important; border-color:#F3E32A !important; }
.st-key-ro_contenuto div[data-testid="stButton"] > button[kind="primary"], .st-key-ro_contenuto div[data-testid="stFormSubmitButton"] > button {
    background:linear-gradient(135deg,#8D021F 0%,#5E0015 100%) !important; color:#ffffff !important; border:none !important; }
.st-key-ro_contenuto div[data-testid="stButton"] > button[kind="primary"] p, .st-key-ro_contenuto div[data-testid="stFormSubmitButton"] > button p { color:#ffffff !important; }
/* elenco schede a sinistra */
div[data-testid="stVerticalBlockBorderWrapper"]:has(> div > .st-key-ro_lista), div[data-testid="stVerticalBlockBorderWrapper"]:has(> .st-key-ro_lista) {
    border:none !important; box-shadow:none !important; background:transparent !important; padding:0 !important; }
.st-key-ro_lista div[data-testid="stButton"] > button { justify-content:flex-start !important; text-align:left !important; border-radius:12px !important; min-height:38px !important; }
.st-key-ro_lista div[data-testid="stButton"] > button p { text-align:left !important; font-size:0.85rem !important; }
.st-key-ro_contenuto div[data-testid="stForm"] { background:#ffffff; border:1.5px solid #ECECEC !important; border-radius:18px; padding:18px 22px; }
.ro-emoji { font-size:6rem; line-height:1.2; padding:22px 0 6px 0; }
.ro-pron { color:#8D021F; font-size:1.05rem; font-weight:600; min-height:1.6rem; }
.ro-it { color:#626262; font-size:1.2rem; padding:6px 16px 4px 16px; }
.ro-tipo { color:#94a3b8; font-size:0.78rem; padding:4px 0 16px 0; text-transform:uppercase; letter-spacing:1px; }
.ro-nav-titolo { color:#8D021F; font-weight:900; font-size:1.2rem; margin-bottom:2px; }
.ro-materia { color:#D4AF37; font-weight:800; font-size:0.78rem; text-transform:uppercase; letter-spacing:1px; margin:14px 0 6px 0; }
.ro-titolo { color:#8D021F; font-weight:900; font-size:1.6rem; margin:0; }
.ro-sotto { color:#626262; margin:4px 0 14px 0; }
.ro-video-vuoto { background:#FFF4CC; border:2px dashed #D4AF37; border-radius:14px; padding:40px 20px;
                  text-align:center; color:#8D021F; font-weight:600; }
.att-card { background:#ffffff; border:2px solid #D4AF37; border-left:6px solid #8D021F; border-radius:14px; padding:20px 24px; margin-bottom:14px; }
.att-titolo { color:#8D021F; font-weight:800; font-size:1.25rem; margin:0 0 4px 0; }
/* STILE SITO leonardoscuole.it: riquadri bordeaux sfumati, pulsanti bianchi a pillola, accenti giallo-oro */
.ro-nav-hero, .ro-hero { background:linear-gradient(135deg,#8D021F 0%,#5E0015 100%); border-radius:18px; padding:18px 20px; color:#fff;
    box-shadow:0 12px 28px rgba(141,2,31,0.22); margin-bottom:14px; }
.ro-hero { padding:24px 28px; }
.ro-nav-hero-kicker, .ro-hero-kicker { color:#F3E32A; font-weight:700; font-size:0.72rem; letter-spacing:1.5px; }
.ro-nav-hero-tit { font-weight:800; font-size:1.35rem; color:#fff; margin:2px 0; }
.ro-hero-tit { font-weight:800; font-size:2rem; color:#fff; line-height:1.2; margin:4px 0 6px 0; }
.ro-nav-hero-sub, .ro-hero-sub { color:rgba(255,255,255,0.88); font-size:0.88rem; margin-bottom:8px; }
.ro-hero-sub { font-size:1.02rem; margin-bottom:12px; }
.ro-barra { background:rgba(255,255,255,0.18); border-radius:20px; height:8px; overflow:hidden; margin:8px 0 6px 0; }
.ro-barra > div { background:linear-gradient(90deg,#F3E32A,#F5A623); height:100%; border-radius:20px; }
.ro-pill { display:inline-block; background:rgba(255,255,255,0.14); color:#fff; border-radius:30px; padding:5px 12px;
    font-size:0.8rem; font-weight:500; margin:0 6px 6px 0; }
div[class*="st-key-ro_voce_"] { background:#ffffff; border:1.5px solid #ECECEC; border-radius:14px; padding:12px 14px 10px 14px;
    margin-bottom:10px; transition:transform .15s ease, box-shadow .15s ease; gap:0.5rem !important; }
div[class*="st-key-ro_voce_"]:hover { transform:translateY(-2px); box-shadow:0 8px 18px rgba(141,2,31,0.12); }
.ro-voce-num { color:#8D021F; font-weight:700; font-size:0.7rem; letter-spacing:1.3px; }
.ro-voce-stato { float:right; letter-spacing:0; font-weight:600; color:#2e7d32; }
.ro-voce-tit { color:#1F2326; font-weight:700; font-size:0.98rem; line-height:1.3; margin-top:2px; }
.ro-voce-desc { color:#626262; font-size:0.8rem; line-height:1.35; margin-top:2px; margin-bottom:10px; }
div[class*="st-key-ro_voce_"] div[data-testid="stMarkdownContainer"] { margin-bottom:0 !important; }
div[class*="st-key-ro_voce_"] div[data-testid="stElementContainer"] { margin-bottom:0 !important; }
.ro-voce-off { opacity:0.55; }
div[class*="st-key-ro_voce_"] div[data-testid="stButton"] > button {
    background:#ffffff !important; color:#1F2326 !important; border:1.5px solid #1F2326 !important; border-radius:30px !important;
    padding:2px 16px !important; min-height:30px !important; font-weight:600 !important; box-shadow:none !important; }
div[class*="st-key-ro_voce_"] div[data-testid="stButton"] > button p { color:inherit !important; font-size:0.8rem !important; }
div[class*="st-key-ro_voce_"] div[data-testid="stButton"] > button:hover { background:#F3E32A !important; border-color:#F3E32A !important; color:#8D021F !important; }
div[class*="st-key-ro_voce_"] div[data-testid="stButton"] > button:disabled { opacity:0.5 !important; }
.st-key-ro_tappe div[data-testid="stButton"] > button { border-radius:30px !important; font-weight:600 !important; }
.ro-oro { background:linear-gradient(135deg,#F3E32A 0%,#F5A623 100%); color:#5E0015; border-radius:14px; padding:14px 16px; margin:8px 0; }
.ro-benvenuto { background:linear-gradient(135deg,#8D021F 0%,#5E0015 100%); border-radius:20px; padding:34px 30px; text-align:center;
    color:#fff; margin-bottom:16px; box-shadow:0 12px 28px rgba(141,2,31,0.22); }
.ro-benvenuto-tit { color:#F3E32A; font-weight:900; font-size:3rem; letter-spacing:1px; line-height:1.1; }
.ro-benvenuto-sub { color:#fff; font-weight:700; font-size:1.25rem; margin-top:6px; }
.ro-benvenuto-small { color:rgba(255,255,255,0.85); font-size:0.95rem; margin-top:4px; }
</style>
"""

def _stato_ro():
    if "ro" not in st.session_state:
        st.session_state.ro = {"modulo": 1, "tappa": {}, "scheda": {}, "visti": {}, "eserc": {}, "fatte": {}}
    return st.session_state.ro

@st.cache_data(show_spinner=False, max_entries=1000)
def audio_rumeno(testo, lento=False):
    """Voce rumena sintetica (gTTS), usata solo per le frasi senza registrazione madrelingua."""
    try:
        from gtts import gTTS
        buffer = io.BytesIO()
        gTTS(testo, lang="ro", slow=lento).write_to_fp(buffer)
        return buffer.getvalue()
    except Exception:
        return None

@st.cache_data(show_spinner=False, max_entries=600)
def leggi_file_audio(percorso):
    with open(percorso, "rb") as f:
        return f.read()

def riproduci(scheda, lento=False):
    """Riproduce la scheda: registrazione madrelingua se c'e', altrimenti voce sintetica."""
    if scheda.get("audio") and not lento:
        st.audio(leggi_file_audio(scheda["audio"]), format="audio/mp3", autoplay=True)
        return
    testo = corso_rumeno.testo_da_leggere(scheda["ro"])
    dati_audio = audio_rumeno(testo, lento)
    if dati_audio:
        st.audio(dati_audio, format="audio/mp3", autoplay=True)
    else:
        components.html(
            "<script>const u=new SpeechSynthesisUtterance(" + json.dumps(testo) + ");"
            f"u.lang='ro-RO';u.rate={0.6 if lento else 0.95};"
            "speechSynthesis.cancel();speechSynthesis.speak(u);</script>",
            height=0,
        )

def _titolo_breve(modulo):
    titolo = modulo["titolo"]
    return titolo.split(" - ", 1)[1] if " - " in titolo else titolo

def tappa_aperta(ordine, i, rs, is_admin=False):
    """Tutte le tappe sono apribili (nessun blocco sull'ordine)."""
    return True

def render_percorso(ordine, rs, is_admin=False):
    tappa = rs["tappa"].get(ordine, 0)
    fatte = rs["fatte"].setdefault(ordine, set())
    larghezze = []
    for i in range(len(TAPPE_RO)):
        larghezze += [4, 1] if i < len(TAPPE_RO) - 1 else [4]
    cols = st.columns(larghezze, vertical_alignment="center")
    for i, (icona, nome) in enumerate(TAPPE_RO):
        with cols[i * 2]:
            aperta = tappa_aperta(ordine, i, rs, is_admin)
            etichetta = f"{'✅' if i in fatte else (icona if aperta else '🔒')} {nome}"
            if st.button(etichetta, key=f"ro_tappa_{ordine}_{i}", type="primary" if i == tappa else "secondary",
                         use_container_width=True, disabled=not aperta,
                         help=None if aperta else "Completa prima la tappa precedente"):
                rs["tappa"][ordine] = i
                st.rerun()
        if i < len(TAPPE_RO) - 1:
            with cols[i * 2 + 1]:
                colore = "#2e7d32" if i in fatte else "#D4AF37"
                st.markdown(f"<div style='border-top:3px dashed {colore};'></div>", unsafe_allow_html=True)

def _mostra_video(nome, sorgente, chiave, prossimo="", visto=False):
    """Video nel progetto -> player con blocco avanzamento; link esterno -> player normale.
    Restituisce l'evento del player, "assente" se il video non c'e' ancora."""
    if sorgente and sorgente["tipo"] == "locale":
        return player_lezione(sorgente["url"], chiave, prossimo=prossimo, visto=visto)
    if sorgente:
        st.video(sorgente["url"])
        return "esterno"
    st.markdown(f"<div class='ro-video-vuoto'>🎬 Video lezione in arrivo<br><span style='font-weight:400; font-size:0.85rem; color:#626262;'>{html.escape(nome)}</span></div>",
                unsafe_allow_html=True)
    return "assente"

def render_benvenuto(compatto=False):
    """Video di benvenuto del docente + il metodo in 3 passi."""
    b = corso_rumeno.BENVENUTO
    if not compatto:
        titolo, _, resto = b["titolo"].partition("! ")
        st.markdown(f"<div class='ro-benvenuto'><div class='ro-benvenuto-tit'>{html.escape(titolo.upper())}!</div>"
                    f"<div class='ro-benvenuto-sub'>{html.escape(resto)}</div>"
                    f"<div class='ro-benvenuto-small'>{html.escape(b['sottotitolo'])}</div></div>", unsafe_allow_html=True)
    rs = _stato_ro()
    primo = sorted(corso_rumeno.MODULI_RUMENO, key=lambda m: m["ordine"])[0]
    evento = _mostra_video(corso_rumeno.VIDEO_INTRO, corso_rumeno.sorgente_video(corso_rumeno.VIDEO_INTRO), "player_intro",
                           prossimo=f"Modulo 1 · {_titolo_breve(primo)}", visto=rs.get("intro_vista", False))
    if evento in ("finito", "prossimo") and not rs.get("intro_vista"):
        rs["intro_vista"] = True
        salva_progressi()
        if evento == "finito":
            st.rerun()
    if evento == "prossimo":
        rs["benvenuto"] = False
        rs["modulo"] = primo["ordine"]
        st.rerun()
    st.markdown(f"**🎯 Obiettivo:** {b['obiettivo']}")
    colonne = st.columns(len(b["passi"]))
    for i, (col, (nome, testo, esempio)) in enumerate(zip(colonne, b["passi"]), start=1):
        col.markdown(f"<div class='ro-card' style='padding:14px; text-align:left;'><div style='color:#8D021F; font-weight:800;'>{i}. {html.escape(nome)}</div>"
                     f"<div style='color:#626262; font-size:0.9rem;'>{html.escape(testo)}</div>"
                     f"<div style='color:#8D021F; font-size:0.9rem; margin-top:6px;'>{html.escape(esempio)}</div></div>", unsafe_allow_html=True)
    st.caption(f"{b['motto']} {b['chiusura']}")

def render_video(modulo, rs):
    ordine = modulo["ordine"]
    v1, v2 = modulo["voci"]
    passi = ["Guarda la video lezione", "Scorri le schede: leggi l'italiano, ascolta il rumeno e ripeti due volte",
             f"Riascolta la traccia completa del madrelingua (voci {v1}–{v2})", "Fai gli esercizi «Abbina» e «Ascolta»",
             "Supera il quiz finale con almeno l'80% (4 su 5): puoi ripeterlo quando vuoi"]
    passi_html = "".join(f"<div class='ro-passo'><span class='ro-passo-n'>{i}</span><span>{html.escape(t)}</span></div>" for i, t in enumerate(passi, 1))
    st.markdown(f"""
    <div class="ro-lezione">
        <div class="ro-lezione-doc">🎙️ <i>{html.escape(corso_rumeno.TESTO_DOCENTE)}</i></div>
        <div class="ro-lezione-k">COME SI STUDIA QUESTO MODULO</div>
        <div class="ro-passi">{passi_html}</div>
    </div>
    """, unsafe_allow_html=True)
    video = corso_rumeno.video_modulo(modulo)
    visti = rs.setdefault("video_visti", set())
    for n, (nome, sorgente) in enumerate(video):
        chiave_v = f"{ordine}:{nome}"
        if len(video) > 1:
            st.markdown(f"<h5 style='color:#8D021F; font-weight:800;'>🎬 Video {n + 1} di {len(video)}</h5>", unsafe_allow_html=True)
        prossimo = f"Video {n + 2} di {len(video)}" if n < len(video) - 1 else "Tappa Impara · le schede del modulo"
        evento = _mostra_video(nome, sorgente, f"player_{ordine}_{n}", prossimo=prossimo, visto=chiave_v in visti)
        if evento in ("assente", "esterno"):
            visti.add(chiave_v)  # video non ancora nel progetto: non si puo' controllare la visione
        elif evento in ("finito", "prossimo") and chiave_v not in visti:
            visti.add(chiave_v)
            if all(f"{ordine}:{x}" in visti for x, _ in video):
                rs["fatte"].setdefault(ordine, set()).add(T_VIDEO)
            salva_progressi()
            st.rerun()
        if evento == "prossimo" and n == len(video) - 1:
            rs["tappa"][ordine] = T_IMPARA
            st.rerun()
    tracce = corso_rumeno.tracce_modulo(modulo)
    if tracce:
        st.markdown("<h5 style='color:#8D021F; font-weight:800; margin-top:18px;'>🎧 Ascolto completo del madrelingua</h5>", unsafe_allow_html=True)
        st.caption("Tutte le frasi del modulo lette di seguito: ascolta e ripeti.")
        for t in tracce:
            st.audio(leggi_file_audio(t), format="audio/mp3")
    rs["fatte"].setdefault(ordine, set()).add(T_VIDEO)
    if st.button("🗣️ Vai alle schede →", key=f"ro_video_next_{ordine}", type="primary", use_container_width=True):
        rs["tappa"][ordine] = T_IMPARA
        st.rerun()

def render_impara(modulo, rs):
    ordine = modulo["ordine"]
    schede = corso_rumeno.elementi(modulo)
    visti = rs["visti"].setdefault(ordine, set())
    idx = min(rs["scheda"].get(ordine, 0), len(schede) - 1)
    visti.add(idx)
    n_chiave = sum(1 for s in schede if s["tipo"].startswith("⭐"))
    if all(i in visti for i in range(n_chiave)) or len(visti) == len(schede):
        rs["fatte"].setdefault(ordine, set()).add(T_IMPARA)

    col_lista, col_scheda = st.columns([1.15, 2], gap="medium")
    with col_lista:
        st.caption(f"📚 {len(visti)}/{len(schede)} schede viste · ⭐ = frase chiave del quiz")
        with st.container(height=560, border=False, key="ro_lista"):
            for i, s in enumerate(schede):
                segno = "✅" if i in visti else ("⭐" if s["tipo"].startswith("⭐") else "▫️")
                if st.button(f"{segno} {s['it']}", key=f"ro_s_{ordine}_{i}", type="primary" if i == idx else "secondary", use_container_width=True):
                    rs["scheda"][ordine] = i
                    st.rerun()

    with col_scheda:
        s = schede[idx]
        voce = "🎙️ registrazione madrelingua" if s["audio"] else "🤖 voce sintetica"
        st.markdown(f"""
        <div class="ro-card">
            <div class="ro-banda"><div class="ro-banda-k">RUMENO</div>{html.escape(s['ro'])}</div>
            <div class="ro-emoji">{s['emoji']}</div>
            <div class="ro-it-k">ITALIANO</div>
            <div class="ro-it">{html.escape(s['it'])}</div>
            <div><span class="ro-tag">{html.escape(s['tipo'])}</span><span class="ro-tag">{voce}</span><span class="ro-tag">{idx + 1} di {len(schede)}</span></div>
            <div style="height:14px"></div>
        </div>
        """, unsafe_allow_html=True)

        b1, b2, b3 = st.columns(3)
        ascolta = b1.button("▶ Ascolta", key=f"ro_play_{ordine}_{idx}", use_container_width=True)
        lento = b2.button("🐢 Lento", key=f"ro_slow_{ordine}_{idx}", use_container_width=True, help="Lettura rallentata (voce sintetica)")
        with b3.popover("🎤 Registrati", use_container_width=True):
            st.caption("Ascolta la frase, poi registra la tua voce e confrontala con l'originale.")
            if hasattr(st, "audio_input"):
                registrazione = st.audio_input("Registra la tua pronuncia", key=f"ro_mic_{ordine}_{idx}")
                if registrazione is not None:
                    st.audio(registrazione)
            else:
                st.info("Registrazione non disponibile in questa versione.")
        if ascolta or lento:
            segna_attivita_corso()
            riproduci(s, lento=lento)

        n1, n2 = st.columns(2)
        if n1.button("← Precedente", key=f"ro_prev_{ordine}", disabled=(idx == 0), use_container_width=True):
            rs["scheda"][ordine] = idx - 1
            st.rerun()
        if idx < len(schede) - 1:
            if n2.button("Successiva →", key=f"ro_next_{ordine}", type="primary", use_container_width=True):
                rs["scheda"][ordine] = idx + 1
                st.rerun()
        else:
            if n2.button("🎮 Vai all'esercizio →", key=f"ro_to_ex_{ordine}", type="primary", use_container_width=True):
                rs["tappa"][ordine] = T_ABBINA
                st.rerun()

def _domande_esercizio(modulo, tipo, seme):
    schede = corso_rumeno.elementi(modulo)
    if tipo == "ascolta":
        con_audio = [s for s in schede if s["audio"]]
        if len(con_audio) >= 4:
            schede = con_audio
    rnd = random.Random(seme)
    campo = "it" if tipo == "abbina" else "ro"
    # le frasi chiave hanno la precedenza, poi le altre voci del modulo
    chiave = [i for i, s in enumerate(schede) if s["tipo"].startswith("⭐")]
    altre_i = [i for i in range(len(schede)) if i not in chiave]
    rnd.shuffle(chiave); rnd.shuffle(altre_i)
    scelte = (chiave[:4] + altre_i)[:DOMANDE_ESERCIZIO] if len(schede) > DOMANDE_ESERCIZIO else list(range(len(schede)))
    rnd.shuffle(scelte)
    domande = []
    for i in scelte:
        giusta = schede[i][campo]
        altre = sorted({s[campo] for j, s in enumerate(schede) if j != i and s[campo] != giusta})
        opzioni = rnd.sample(altre, k=min(3, len(altre))) + [giusta]
        rnd.shuffle(opzioni)
        domande.append({"scheda": schede[i], "opzioni": opzioni, "giusta": giusta})
    return domande

def render_esercizio(modulo, rs, tipo):
    ordine = modulo["ordine"]
    indice_tappa = T_ABBINA if tipo == "abbina" else T_ASCOLTA
    stato = rs["eserc"].setdefault(f"{tipo}_{ordine}", {"seme": random.randint(1, 10**9), "n": 0, "esiti": [], "scelta": None, "auto": -1})
    domande = _domande_esercizio(modulo, tipo, stato["seme"])
    totale = len(domande)

    if tipo == "abbina":
        st.markdown("<p class='ro-sotto'>🎮 Leggi la frase in rumeno e scegli la traduzione giusta.</p>", unsafe_allow_html=True)
    else:
        st.markdown("<p class='ro-sotto'>🎧 Ascolta il madrelingua e scegli cosa hai sentito. Puoi riascoltare quante volte vuoi.</p>", unsafe_allow_html=True)

    if stato["n"] >= totale:
        giuste = sum(stato["esiti"])
        if giuste >= min(SOGLIA_ESERCIZIO, totale):
            rs["fatte"].setdefault(ordine, set()).add(indice_tappa)
            st.success(f"🎉 Ottimo! {giuste} risposte giuste su {totale}.")
        else:
            st.warning(f"📚 {giuste} risposte giuste su {totale}. Ne servono almeno {SOGLIA_ESERCIZIO}: ripassa e riprova!")
        c1, c2 = st.columns(2)
        if c1.button("🔁 Ripeti con nuove domande", key=f"ro_rip_{tipo}_{ordine}", use_container_width=True):
            rs["eserc"][f"{tipo}_{ordine}"] = {"seme": random.randint(1, 10**9), "n": 0, "esiti": [], "scelta": None, "auto": -1}
            st.rerun()
        prossima = TAPPE_RO[indice_tappa + 1]
        if c2.button(f"{prossima[0]} Vai a: {prossima[1]} →", key=f"ro_avanti_{tipo}_{ordine}", type="primary", use_container_width=True):
            rs["tappa"][ordine] = indice_tappa + 1
            st.rerun()
        return

    n = stato["n"]
    d = domande[n]
    s = d["scheda"]
    risposto = len(stato["esiti"]) > n
    st.progress(n / totale)
    st.caption(f"Domanda {n + 1} di {totale}")

    if tipo == "abbina":
        st.markdown(f"""
        <div class="ro-card">
            <div class="ro-banda">{html.escape(s['ro'])}</div>
            <div class="ro-emoji" style="font-size:4.5rem;">{s['emoji']}</div>
            <div class="ro-tipo">Cosa significa?</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        testo_svelato = html.escape(s["ro"]) if risposto else "🎧 Cosa hai sentito?"
        st.markdown(f"""
        <div class="ro-card">
            <div class="ro-banda">{testo_svelato}</div>
            <div class="ro-emoji" style="font-size:4.5rem;">{s['emoji'] if risposto else '🔊'}</div>
            <div class="ro-tipo">Ascolta e scegli</div>
        </div>
        """, unsafe_allow_html=True)

    a1, a2 = st.columns(2)
    ascolta = a1.button("▶ Ascolta", key=f"ro_ex_play_{tipo}_{ordine}_{n}", use_container_width=True)
    lento = a2.button("🐢 Lento", key=f"ro_ex_slow_{tipo}_{ordine}_{n}", use_container_width=True)
    primo_ascolto = (tipo == "ascolta" and stato["auto"] != n)
    if ascolta or lento or primo_ascolto:
        stato["auto"] = n
        riproduci(s, lento=lento)

    griglia = st.columns(2)
    for k, opzione in enumerate(d["opzioni"]):
        segno = ""
        if risposto:
            if opzione == d["giusta"]:
                segno = "✅ "
            elif opzione == stato["scelta"]:
                segno = "❌ "
        with griglia[k % 2]:
            if st.button(f"{segno}{opzione}", key=f"ro_opt_{tipo}_{ordine}_{n}_{k}", disabled=risposto, use_container_width=True):
                segna_attivita_corso()
                stato["esiti"].append(opzione == d["giusta"])
                stato["scelta"] = opzione
                st.rerun()

    if risposto:
        if stato["esiti"][n]:
            st.success(f"✅ Esatto! **{s['ro']}** = {s['it']}")
        else:
            st.error(f"❌ La risposta giusta era: **{d['giusta']}**  ·  {s['ro']} = {s['it']}")
        if st.button("Avanti →", key=f"ro_ex_next_{tipo}_{ordine}_{n}", type="primary", use_container_width=True):
            stato["n"] += 1
            stato["scelta"] = None
            st.rerun()

def modulo_sbloccato(modulo, moduli, is_admin=False):
    """Completamento progressivo: si apre quando il modulo precedente e' superato."""
    if is_admin:
        return True
    if modulo["ordine"] == moduli[0]["ordine"]:
        return True
    precedente = next((m for m in moduli if m["ordine"] == modulo["ordine"] - 1), None)
    return precedente is None or precedente["titolo"] in st.session_state.moduli_completati

def render_corso_rumeno(is_admin=False):
    rs = _stato_ro()
    st.markdown(STILI_CORSO_RO, unsafe_allow_html=True)
    moduli = sorted(corso_rumeno.MODULI_RUMENO, key=lambda m: m["ordine"])
    completati = {m["titolo"] for m in moduli if m["titolo"] in st.session_state.moduli_completati}

    col_nav, col_main = st.columns([1.25, 3.2], gap="large")
    in_benvenuto = rs.get("benvenuto", not st.session_state.moduli_completati)
    attivo = "intro" if in_benvenuto else str(rs["modulo"])
    # Evidenzia la voce aperta (stile riquadro bordeaux del sito)
    st.markdown(f"<style>.st-key-ro_voce_{attivo} {{ background:linear-gradient(135deg,#8D021F 0%,#5E0015 100%) !important; border-color:#8D021F !important; }}"
                f".st-key-ro_voce_{attivo} .ro-voce-num {{ color:#F3E32A !important; }}"
                f".st-key-ro_voce_{attivo} .ro-voce-tit, .st-key-ro_voce_{attivo} .ro-voce-desc {{ color:#ffffff !important; }}</style>",
                unsafe_allow_html=True)
    with col_nav:
        perc = int(len(completati) / len(moduli) * 100)
        st.markdown(f"""
        <div class="ro-nav-hero">
            <div class="ro-nav-hero-kicker">CORSO ONLINE</div>
            <div class="ro-nav-hero-tit">Lingua Rumena</div>
            <div class="ro-nav-hero-sub">{len(moduli)} moduli · {corso_rumeno.ORE_CORSO} ore · attestato finale</div>
            <div class="ro-barra"><div style="width:{perc}%;"></div></div>
            <div class="ro-nav-hero-sub">{len(completati)}/{len(moduli)} completati · {perc}%</div>
        </div>
        """, unsafe_allow_html=True)
        with st.container(key="ro_voce_intro"):
            st.markdown("<div class='ro-voce-num'>INTRO</div><div class='ro-voce-tit'>🎬 Benvenuto e metodo</div>"
                        "<div class='ro-voce-desc'>Il video del docente e i 3 passi per studiare.</div>", unsafe_allow_html=True)
            if st.button("Guarda →", key="ro_benvenuto"):
                rs["benvenuto"] = True
                st.rerun()
        for m in moduli:
            aperto = modulo_sbloccato(m, moduli, is_admin)
            fatto = m["titolo"] in completati
            stato = "✅ Completato" if fatto else ("" if aperto else "🔒 Bloccato")
            icona = corso_rumeno.ICONE_MODULI.get(m["ordine"], "📘")
            classe = "ro-voce-off" if not aperto else ""
            with st.container(key=f"ro_voce_{m['ordine']}"):
                st.markdown(f"<div class='{classe}'><div class='ro-voce-num'>MODULO {m['ordine']} <span class='ro-voce-stato'>{stato}</span></div>"
                            f"<div class='ro-voce-tit'>{icona} {html.escape(_titolo_breve(m))}</div>"
                            f"<div class='ro-voce-desc'>{html.escape(m['descrizione'])}</div></div>", unsafe_allow_html=True)
                etichetta = "Ripassa →" if fatto else ("Apri →" if aperto else "Bloccato")
                if st.button(etichetta, key=f"ro_mod_{m['ordine']}", disabled=not aperto):
                    rs["modulo"] = m["ordine"]
                    rs["benvenuto"] = False
                    st.rerun()
        if len(completati) == len(moduli):
            st.markdown("<div class='ro-oro'>🎓 <b>Corso completato!</b><br>Il tuo attestato è pronto.</div>", unsafe_allow_html=True)
            if st.button("🎓 Scarica l'attestato", key="ro_vai_attestati", type="primary", use_container_width=True):
                st.session_state.sezione_attiva = "Attestati"
                st.rerun()

    with col_main:
        if in_benvenuto:
            render_benvenuto()
            if st.button("▶️ Inizia dal Modulo 1", key="ro_inizia", type="primary", use_container_width=True):
                rs["benvenuto"] = False
                rs["modulo"] = 1
                st.rerun()
            return
        modulo = next((m for m in moduli if m["ordine"] == rs["modulo"]), moduli[0])
        if not modulo_sbloccato(modulo, moduli, is_admin):
            modulo = moduli[0]
            rs["modulo"] = modulo["ordine"]
        ordine = modulo["ordine"]
        icona = corso_rumeno.ICONE_MODULI.get(ordine, "📘")
        v1, v2 = modulo["voci"]
        n_schede = len(corso_rumeno.elementi(modulo))
        st.markdown(f"""
        <div class="ro-hero">
            <div class="ro-hero-kicker">MODULO {ordine} DI {len(moduli)}</div>
            <div class="ro-hero-tit">{icona} {html.escape(_titolo_breve(modulo))}</div>
            <div class="ro-hero-sub">{html.escape(modulo['descrizione'])}</div>
            <div><span class="ro-pill">💬 {n_schede} frasi</span><span class="ro-pill">🎙️ audio madrelingua</span><span class="ro-pill">📝 quiz 5 domande · 80%</span></div>
        </div>
        """, unsafe_allow_html=True)
        with st.container(key="ro_tappe"):
            render_percorso(ordine, rs, is_admin)

        contenuto = st.container(key="ro_contenuto")
        tappa = rs["tappa"].get(ordine, T_VIDEO)
        while tappa > 0 and not tappa_aperta(ordine, tappa, rs, is_admin):
            tappa -= 1
        rs["tappa"][ordine] = tappa
        with contenuto:
            if tappa == T_VIDEO:
                render_video(modulo, rs)
            elif tappa == T_IMPARA:
                render_impara(modulo, rs)
            elif tappa == T_ABBINA:
                render_esercizio(modulo, rs, "abbina")
            elif tappa == T_ASCOLTA:
                render_esercizio(modulo, rs, "ascolta")
            else:
                render_quiz(modulo, f"ro_{ordine}")
                if modulo["titolo"] in st.session_state.moduli_completati:
                    rs["fatte"].setdefault(ordine, set()).add(T_QUIZ)
                    successivo = next((m for m in moduli if m["ordine"] == ordine + 1), None)
                    if successivo and st.button(f"➡️ Passa al modulo {successivo['ordine']}: {_titolo_breve(successivo)}",
                                                key=f"ro_next_mod_{ordine}", type="primary", use_container_width=True):
                        rs["modulo"] = successivo["ordine"]
                        rs["tappa"][successivo["ordine"]] = T_VIDEO
                        st.rerun()


# 3d. AREA ATTESTATI
def scarica_logo():
    """Logo ufficiale per l'attestato: file locale, in riserva quello del sito."""
    if LOGO_BYTES:
        return LOGO_BYTES
    try:
        r = requests.get(LOGO_URL_RISERVA, timeout=10, headers={"User-Agent": "Mozilla/5.0 (LeonardoScuole)"})
        if r.status_code == 200:
            return r.content
    except Exception:
        pass
    return None

def stato_corso_rumeno():
    moduli = sorted(corso_rumeno.MODULI_RUMENO, key=lambda m: m["ordine"])
    fatti = [m for m in moduli if m["titolo"] in st.session_state.moduli_completati]
    voti = [st.session_state.risultati_quiz.get(f"Rumeno · {m['titolo']}") for m in moduli]
    voti = [v for v in voti if isinstance(v, (int, float))]
    media = round(sum(voti) / len(voti) / 30 * 100) if voti else 100
    return moduli, fatti, media

def render_area_attestati(dati, is_admin=False):
    st.markdown(STILI_CORSO_RO, unsafe_allow_html=True)
    st.markdown("<h2 style='color:#8D021F; font-weight:800; margin-top:0;'>🎓 Area Attestati</h2>", unsafe_allow_html=True)
    st.markdown("<p class='ro-sotto'>Qui trovi gli attestati dei corsi che hai completato. L'attestato si sblocca quando superi tutti i quiz di modulo.</p>",
                unsafe_allow_html=True)

    if corso_rumeno is None or attestato is None:
        st.info("Nessun attestato disponibile al momento.")
        return

    iscritto = str(dati.get("pacchetto", "")).strip().lower() == corso_rumeno.INDIRIZZO_RUMENO.lower()
    if not iscritto and not is_admin:
        st.markdown("<div class='custom-info-box'>Per il tuo percorso non sono ancora previsti attestati scaricabili.</div>", unsafe_allow_html=True)
        return

    moduli, fatti, media = stato_corso_rumeno()
    completo = len(fatti) == len(moduli)
    st.markdown(f"""
    <div class="att-card">
        <p class="att-titolo">{html.escape(corso_rumeno.NOME_CORSO)}</p>
        <p style="color:#626262; margin:0;">{len(moduli)} moduli · {corso_rumeno.ORE_CORSO} ore · quiz superati: <b>{len(fatti)}/{len(moduli)}</b></p>
    </div>
    """, unsafe_allow_html=True)
    st.progress(len(fatti) / len(moduli))

    if not completo:
        mancanti = [f"{m['ordine']}. {_titolo_breve(m)}" for m in moduli if m not in fatti]
        st.warning("🔒 L'attestato si sblocca quando completi tutti i moduli. Ti mancano: " + ", ".join(mancanti[:5]) + (" …" if len(mancanti) > 5 else ""))

    def _pdf(nome, email):
        oggi = date.today().strftime("%d/%m/%Y")
        inizio = st.session_state.date_corso.get("inizio", oggi)
        fine = st.session_state.date_corso.get("fine", oggi)
        contenuti = ", ".join(_titolo_breve(m) for m in moduli)
        return attestato.genera_attestato(
            nominativo=nome, email=email, corso=corso_rumeno.NOME_CORSO, contenuti=contenuti,
            ore=corso_rumeno.ORE_CORSO, n_moduli=len(moduli), media_quiz=media,
            data_inizio=inizio, data_fine=fine, logo_bytes=scarica_logo(),
            firmatario=ATTESTATO_FIRMATARIO, luogo=ATTESTATO_LUOGO)

    nome = str(dati.get("nominativo", "Studente")).strip()
    if completo:
        pdf, codice = _pdf(nome, dati.get("email", ""))
        st.success(f"🎉 Complimenti {nome.split()[0] if nome else ''}! Hai completato il corso. Codice attestato: **{codice}**")
        st.download_button("📄 Scarica l'attestato (PDF)", data=pdf, file_name=f"Attestato_Rumeno_{nome.replace(' ', '_')}.pdf",
                           mime="application/pdf", type="primary", use_container_width=True)
        if os.path.exists(corso_rumeno.AUDIO_CONCLUSIONI):
            st.markdown("<h5 style='color:#8D021F; font-weight:800;'>🎙️ Il saluto finale del corso</h5>", unsafe_allow_html=True)
            st.audio(leggi_file_audio(corso_rumeno.AUDIO_CONCLUSIONI), format="audio/mp4")

    if is_admin:
        with st.expander("🛠️ Anteprima attestato (solo admin)"):
            nome_prova = st.text_input("Nome e cognome da stampare", value="Mario Rossi", key="att_prova_nome")
            pdf, codice = _pdf(nome_prova, "anteprima@leonardoscuole.it")
            st.download_button("👁️ Scarica anteprima", data=pdf, file_name="Anteprima_Attestato_Rumeno.pdf",
                               mime="application/pdf", use_container_width=True, key="att_prova_btn")


# 4. DIALOG POP-UP MODALI
@st.dialog(" ", width="small")
def dialog_login():
    st.markdown("""
    <style>
    div[data-testid="stDialog"] header { display: none !important; }
    div[data-testid="stDialog"] > div {
        background-color: #7D001E !important;
        border: 3px solid #D4AF37 !important;
        border-radius: 12px !important;
        padding: 25px !important;
    }
    .modal-title-custom {
        color: #D4AF37;
        font-size: 1.4rem;
        font-weight: 800;
        margin-bottom: 15px;
        text-align: center;
        border-bottom: 2px solid #D4AF37;
        padding-bottom: 10px;
    }
    div[data-testid="stDialog"] input {
        background-color: #ffffff !important;
        border: 1px solid #D4AF37 !important;
        color: #333333 !important;
    }
    div[data-testid="stDialog"] label p { color: #ffffff !important; }
    div[data-testid="stDialog"] div[data-testid="stAlert"], div[data-testid="stDialog"] div[role="alert"] { background-color: #ffffff !important; border-radius: 8px !important; }
    div[data-testid="stDialog"] div[data-testid="stAlert"] p, div[data-testid="stDialog"] div[role="alert"] p { color: #7D001E !important; font-weight: 700 !important; }
    div[data-testid="stDialog"] .stButton > button:not([kind="tertiary"]),
    div[data-testid="stDialog"] div[data-testid="stFormSubmitButton"] > button {
        background-color: #D4AF37 !important; color: #7D001E !important; font-weight: 800 !important; width: 100% !important; border: 2px solid #D4AF37 !important; margin-top: 10px !important;
    }
    div[data-testid="stDialog"] div[data-testid="stFormSubmitButton"] > button p { color: #7D001E !important; }
    div[data-testid="stDialog"] .stButton > button:not([kind="tertiary"]):hover {
        background-color: #ffffff !important; color: #7D001E !important;
    }
    div[data-testid="stDialog"] .stButton > button[kind="tertiary"] {
        background: transparent !important; color: #D4AF37 !important; font-weight: 700 !important; text-decoration: underline !important; border: none !important; box-shadow: none !important; margin-top: 8px !important;
    }
    div[data-testid="stDialog"] .stButton > button[kind="tertiary"]:hover {
        color: #ffffff !important; background: transparent !important;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="modal-title-custom">Accedi all\'Area Riservata</div>', unsafe_allow_html=True)
    
    # RIMOZIONE CREDENZIALI DI DEFAULT
    # Modulo unico: email e password vengono lette insieme anche se riempite dal browser
    with st.form("form_login", border=False):
        email = st.text_input("Email", value="", placeholder="Email", label_visibility="collapsed", key="in_email")
        password = st.text_input("Password", value="", type="password", placeholder="Password", label_visibility="collapsed", key="in_pw")
        ricordami = st.checkbox("Ricordami", value=True, key="in_remember")
        accedi = st.form_submit_button("Accedi")

    if accedi:
        if email and password:
            if verifica_credenziali(email, password, ricordami):
                carica_progressi()
                st.session_state.autenticato = True
                st.session_state.sezione_attiva = "Corsi"
                st.session_state.open_login = False
                st.rerun()
        else:
            st.error("⚠️ Inserisci email e password.")

    if st.button("Hai dimenticato la password?", key="btn_to_rec", type="tertiary"):
        st.session_state.open_login = False
        st.session_state.open_recupero = True
        st.rerun()

@st.dialog(" ", width="small")
def dialog_recupero():
    st.markdown("""
    <style>
    div[data-testid="stDialog"] header { display: none !important; }
    div[data-testid="stDialog"] > div { background-color: #7D001E !important; border: 3px solid #D4AF37 !important; border-radius: 12px !important; padding: 25px !important; }
    .modal-title-custom { color: #D4AF37; font-size: 1.4rem; font-weight: 800; margin-bottom: 15px; text-align: center; border-bottom: 2px solid #D4AF37; padding-bottom: 10px; }
    div[data-testid="stDialog"] input { background-color: #ffffff !important; border: 1px solid #D4AF37 !important; color: #333333 !important; }
    div[data-testid="stDialog"] label p { color: #ffffff !important; }
    div[data-testid="stDialog"] div[data-testid="stAlert"], div[data-testid="stDialog"] div[role="alert"] { background-color: #ffffff !important; border-radius: 8px !important; }
    div[data-testid="stDialog"] div[data-testid="stAlert"] p, div[data-testid="stDialog"] div[role="alert"] p { color: #7D001E !important; font-weight: 700 !important; }
    div[data-testid="stDialog"] .stButton > button:not([kind="tertiary"]) { background-color: #D4AF37 !important; color: #7D001E !important; font-weight: 800 !important; width: 100% !important; border: 2px solid #D4AF37 !important; }
    div[data-testid="stDialog"] .stButton > button[kind="tertiary"] { background: transparent !important; color: #D4AF37 !important; font-weight: 700 !important; text-decoration: underline !important; border: none !important; }
    div[data-testid="stDialog"] .stButton > button[kind="tertiary"]:hover { color: #ffffff !important; }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="modal-title-custom">Recupero Password</div>', unsafe_allow_html=True)
    if st.session_state.password_cambiata_successo:
        st.success("🎉 Password cambiata con successo!")
        if st.button("Vai al Login 🔑", key="btn_go_to_login_after_success"):
            st.session_state.password_cambiata_successo = False
            st.session_state.open_recupero = False
            st.session_state.open_login = True
            st.rerun()
        return

    email_rec = st.text_input("Email recupero", placeholder="E-mail registrata", label_visibility="collapsed", key="rec_email_in")

    if st.button("Invia codice OTP via email", key="btn_send_otp_single"):
        email_pulita = email_rec.strip().lower() if email_rec else ""
        if not email_pulita:
            st.error("⚠️ Inserisci la tua email.")
        else:
            # Il codice viene generato, inviato e controllato dallo script Google
            risposta = chiama_script("RICHIEDI_OTP", email=email_pulita)
            if risposta == "SUCCESS":
                st.info("📩 Se l'email è registrata, riceverai un codice valido 10 minuti.")
            elif risposta == "TROPPE_RICHIESTE":
                st.warning("⏳ Hai richiesto troppi codici. Riprova tra un'ora.")
            else:
                st.error("❌ Servizio email non raggiungibile, riprova più tardi.")

    st.divider()
    otp_val = st.text_input("Codice OTP", placeholder="Codice OTP a 6 cifre", label_visibility="collapsed", key="rec_otp_in")
    new_p1 = st.text_input("Nuova Password", type="password", placeholder="Nuova Password", label_visibility="collapsed", key="rec_p1_in")
    new_p2 = st.text_input("Conferma Password", type="password", placeholder="Conferma Nuova Password", label_visibility="collapsed", key="rec_p2_in")

    if st.button("Aggiorna Password", key="btn_save_pw_single"):
        email_pulita = email_rec.strip().lower() if email_rec else ""
        if not email_pulita or not otp_val:
            st.error("⚠️ Inserisci email e codice OTP.")
        elif new_p1 != new_p2 or len(new_p1) < 8:
            st.error("⚠️ Le password devono coincidere ed essere lunghe almeno 8 caratteri.")
        else:
            risposta = chiama_script("RESET_PASSWORD", email=email_pulita, otp=str(otp_val).strip(), nuova_password=new_p1)
            if risposta == "SUCCESS":
                st.session_state.password_cambiata_successo = True
                st.rerun()
            elif risposta == "OTP_ERRATO":
                st.error("❌ Codice errato. Dopo 5 errori il codice non è più valido.")
            elif risposta == "OTP_SCADUTO":
                st.error("⛔ Codice scaduto o non valido per questa email. Richiedine uno nuovo.")
            else:
                st.error("❌ Aggiornamento non riuscito, riprova.")

    if st.button("← Torna al Login", key="btn_back_log", type="tertiary"):
        st.session_state.open_recupero = False
        st.session_state.open_login = True
        st.rerun()

if not st.session_state.autenticato:
    if st.session_state.open_login:
        dialog_login()
    if st.session_state.open_recupero:
        dialog_recupero()

# 5. LANDING PAGE / AREA RISERVATA
if not st.session_state.autenticato:
    stili_landing = """
    <style>
    header[data-testid="stHeader"] { display: none !important; }
    section[data-testid="stSidebar"] { display: none !important; }
    .main .block-container, div[data-testid="stMainBlockContainer"] { padding: 0rem !important; margin: 0rem !important; max-width: 100% !important; }
    .stApp { background-image: url('https://i.ibb.co/zTR3Yqwb/Gemini-Generated-Image-tpzaywtpzaywtpza.png') !important; background-size: cover !important; background-position: center top !important; }
    .st-key-header_bar_landing { background-color: #7D001E !important; border-top: 4px solid #D4AF37 !important; border-bottom: 4px solid #D4AF37 !important; padding: 8px 25px !important; margin: 0 !important; width: 100% !important; }
    .st-key-header_bar_landing .stButton > button { background-color: #D4AF37 !important; color: #7D001E !important; font-weight: 800 !important; border-radius: 6px !important; border: none !important; padding: 8px 28px !important; }
    </style>
    """
    st.markdown(stili_landing, unsafe_allow_html=True)

    with st.container(key="header_bar_landing"):
        col1, col2 = st.columns([8, 2])
        with col1:
            st.image(LOGO_BYTES or LOGO_URL_RISERVA, width=240)
        with col2:
            if st.button("Accedi 🔑", key="btn_main_accedi"):
                st.session_state.open_login = True
                st.rerun()

else:
    LARGHEZZA_MENU = 280  # px
    padding_sx_contenuto = f"{LARGHEZZA_MENU + 30}px" if st.session_state.sidebar_aperta else "2.8rem"

    stili_area_riservata = f"""
    <style>
    /* SFONDO CALDO GLOBALE */
    [data-testid="stAppViewContainer"], .stApp {{
        background: linear-gradient(135deg, #fdfbf7 0%, #f0ede6 100%) !important;
        background-color: #fcfaf5 !important;
    }}
    
    section[data-testid="stSidebar"] {{ display: none !important; }}
    div[data-testid="stSidebarCollapsedControl"], [data-testid="collapsedControl"] {{ display: none !important; }}

    header[data-testid="stHeader"] {{ position: fixed !important; top: 0 !important; left: 0 !important; width: 100% !important; background-color: #7D001E !important; border-bottom: 3px solid #D4AF37 !important; height: 65px !important; z-index: 999900 !important; }}
    .st-key-header_custom_bar {{ position: fixed !important; top: 0 !important; left: 0 !important; width: 100% !important; height: 65px !important; z-index: 999950 !important; padding: 0 25px !important; background-color: #7D001E !important; border-bottom: 3px solid #D4AF37 !important; display: flex !important; align-items: center !important; justify-content: center !important; }}

    .main .block-container, div[data-testid="stMainBlockContainer"] {{
        padding-top: 6.5rem !important;
        padding-left: {padding_sx_contenuto} !important;
        padding-right: 2.8rem !important;
        padding-bottom: 120px !important;
        max-width: 100% !important;
        transition: padding-left 0.2s ease-in-out !important;
    }}

    /* PANNELLO MENU CUSTOM LATERALE */
    .st-key-menu_custom_panel {{
        position: fixed !important; top: 0 !important; left: 0 !important; width: {LARGHEZZA_MENU}px !important;
        height: 100vh !important; z-index: 9999999 !important;
        background: linear-gradient(180deg, #7D001E 0%, #5c0016 100%) !important;
        box-shadow: 4px 0 15px rgba(0, 0, 0, 0.3) !important;
        overflow-y: auto !important; display: flex !important; flex-direction: column !important;
        padding: 22px 18px 16px 18px !important; text-align: center !important;
    }}
    .st-key-menu_custom_panel * {{ color: #ffffff !important; }}
    .st-key-menu_custom_panel > div {{ display: flex !important; flex-direction: column !important; flex: 1 1 auto !important; width: 100% !important; }}
    .st-key-menu_custom_panel div[data-testid="stButton"] {{ width: 100% !important; }}

    .menu-logo-box {{
        text-align: center !important; margin: 40px auto 20px auto !important; width: 100% !important;
        display: flex !important; justify-content: center !important; padding-bottom: 16px !important;
        border-bottom: 1px solid rgba(212, 175, 55, 0.35) !important;
    }}

    .st-key-menu_custom_panel button, .st-key-menu_custom_panel div[data-testid="stFormSubmitButton"] > button {{
        background-color: rgba(212, 175, 55, 0.12) !important; color: #F3DFA0 !important; font-weight: 700 !important;
        font-size: 0.93rem !important; border-radius: 4px !important; border: none !important; width: 100% !important;
        text-align: center !important; padding: 11px 10px !important; transition: all 0.2s ease-in-out !important;
        margin: 0 auto 8px auto !important; display: block !important;
    }}
    .st-key-menu_custom_panel button p {{ color: #F3DFA0 !important; transition: color 0.2s ease-in-out !important; }}
    .st-key-menu_custom_panel button:hover {{ background-color: #D4AF37 !important; color: #7D001E !important; }}
    .st-key-menu_custom_panel button:hover p {{ color: #7D001E !important; }}

    .st-key-menu_custom_panel div[data-testid="stExpander"] {{
        background-color: rgba(255, 255, 255, 0.06) !important; border: 1px solid transparent !important;
        border-radius: 4px !important; margin-bottom: 12px !important; text-align: center !important; width: 100% !important;
    }}
    .st-key-menu_custom_panel div[data-testid="stExpander"]:hover {{ border-color: #D4AF37 !important; }}
    .st-key-menu_custom_panel div[data-testid="stExpander"] summary {{ padding: 4px 6px !important; }}
    .st-key-menu_custom_panel div[data-testid="stExpander"] summary:hover {{ background-color: #D4AF37 !important; }}
    .st-key-menu_custom_panel div[data-testid="stExpander"] summary:hover div p {{ color: #7D001E !important; }}
    .st-key-menu_custom_panel div[data-testid="stExpander"] summary div p {{ color: #D4AF37 !important; font-weight: 800 !important; text-align: center !important; }}

    .st-key-menu_custom_panel div[role="radiogroup"] {{ width: 100% !important; align-items: flex-start !important; }}
    .st-key-menu_custom_panel div[data-testid="stRadio"] label:hover p {{ color: #D4AF37 !important; transition: color 0.2s ease; }}

    /* Pulsante Toggle Quadrato ORO */
    .st-key-toggle_menu_btn div[data-testid="stButton"] > button {{
        width: 45px !important; height: 45px !important; min-width: 45px !important; max-width: 45px !important;
        min-height: 45px !important; max-height: 45px !important; aspect-ratio: 1 / 1 !important; flex-shrink: 0 !important;
        position: fixed !important; top: 10px !important; left: 10px !important; z-index: 99999999999 !important;
        background-color: #D4AF37 !important; color: #7D001E !important; border: 2px solid #D4AF37 !important; border-radius: 8px !important;
        font-weight: 900 !important; font-size: 20px !important; padding: 0 !important; display: flex !important; align-items: center !important; 
        justify-content: center !important; box-shadow: 0 4px 10px rgba(0,0,0,0.3) !important;
    }}
    .st-key-toggle_menu_btn div[data-testid="stButton"] > button p {{ color: #7D001E !important; margin:0 !important; }}
    .st-key-toggle_menu_btn div[data-testid="stButton"] > button:hover {{ background-color: #ffffff !important; color: #7D001E !important; }}

    /* SCHEDE MATERIE */
    .materia-card-img-container {{ 
        background-color: #ffffff; border: 2px solid #D4AF37 !important; border-radius: 16px; 
        overflow: hidden; box-shadow: 0 10px 30px rgba(125, 0, 30, 0.08) !important; 
        transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275), box-shadow 0.3s ease !important; 
        margin-bottom: 25px; display: flex; flex-direction: column;
    }}
    .materia-card-img-container:hover {{ transform: translateY(-8px); box-shadow: 0 15px 40px rgba(125, 0, 30, 0.15) !important; border-color: #D4AF37 !important; }}
    .materia-banner-img {{ width: 100%; height: 160px; object-fit: cover; margin: 0; padding: 0; border-bottom: 1px solid rgba(212, 175, 55, 0.15); }}
    .materia-card-body {{ padding: 20px; display: flex; flex-direction: column; flex-grow: 1; }}
    .materia-card-title {{ color: #7D001E; font-size: 1.25rem; font-weight: 800; margin-bottom: 6px; }}

    /* CORNICI DEI MODULI FISARMONICA (BORDO ORO SOLIDO) */
    div[data-testid="stVerticalBlockBorderWrapper"] {{
        background-color: #ffffff !important;
        border: 2px solid #D4AF37 !important;
        border-left: 6px solid #7D001E !important;
        border-radius: 12px !important;
        padding: 10px 15px !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05) !important;
        margin-bottom: 18px !important;
        transition: all 0.3s ease !important;
    }}
    div[data-testid="stVerticalBlockBorderWrapper"]:hover {{
        border-color: #D4AF37 !important;
        box-shadow: 0 10px 25px rgba(125, 0, 30, 0.1) !important;
    }}
    
    /* SFONDO ROSA/AMARANTO ANTICO SE LA SCHEDA E' APERTA */
    div[data-testid="stVerticalBlockBorderWrapper"]:has(.is-open-card) {{
        background-color: #fbeef0 !important; 
        border: 2px solid #D4AF37 !important;
        border-left: 8px solid #7D001E !important;
        box-shadow: 0 15px 40px rgba(125, 0, 30, 0.15) !important;
        transform: scale(1.01) !important;
        z-index: 10 !important;
    }}

    .argomento-num {{ width: 36px; height: 36px; border-radius: 50%; background-color: #7D001E; color: #D4AF37; font-weight: 800; font-size: 1rem; display: flex; align-items: center; justify-content: center; flex-shrink: 0; box-shadow: 0 2px 5px rgba(0,0,0,0.1);}}
    .argomento-num.completed {{ background-color: #2e7d32; color: #ffffff; }}
    .card-badge {{ display: inline-block; padding: 3px 8px; border-radius: 12px; font-size: 0.75rem; font-weight: 700; margin-left: 10px; }}
    .badge-anno {{ background-color: rgba(212, 175, 55, 0.15); color: #7D001E; border: 1px solid #D4AF37; }}

    .custom-info-box {{
        background-color: rgba(212, 175, 55, 0.08);
        border-left: 4px solid #D4AF37;
        padding: 12px 16px;
        border-radius: 4px;
        color: #7D001E;
        font-size: 0.95rem;
        font-weight: 500;
        margin-bottom: 15px;
    }}
    .custom-caption {{ font-size: 0.85rem; color: #94a3b8; font-style: italic; }}

    /* FORZATURA BOTTONI */
    div.stButton > button[kind="primary"] {{
        background-color: #7D001E !important;
        color: #D4AF37 !important;
        font-weight: 800 !important;
        border-radius: 8px !important;
        border: 2px solid #7D001E !important;
        width: 100% !important;
        box-shadow: 0 4px 10px rgba(125, 0, 30, 0.3) !important;
    }}
    div.stButton > button[kind="primary"] p, div.stButton > button[kind="primary"] div {{ color: #D4AF37 !important; font-size: 1.05rem !important; margin: 0 !important; }}
    div.stButton > button[kind="primary"]:hover {{ background-color: #D4AF37 !important; border-color: #D4AF37 !important; box-shadow: 0 6px 15px rgba(212, 175, 55, 0.4) !important; }}
    div.stButton > button[kind="primary"]:hover p, div.stButton > button[kind="primary"]:hover div {{ color: #7D001E !important; }}

    div.stButton > button[kind="secondary"] {{
        background-color: #ffffff !important; color: #7D001E !important; font-weight: 800 !important;
        border-radius: 8px !important; border: 2px solid #D4AF37 !important; width: 100% !important;
        box-shadow: 0 4px 6px rgba(212, 175, 55, 0.1) !important;
    }}
    div.stButton > button[kind="secondary"] p, div.stButton > button[kind="secondary"] div {{ color: #7D001E !important; margin: 0 !important; }}
    div.stButton > button[kind="secondary"]:hover {{ background-color: #D4AF37 !important; border-color: #D4AF37 !important; }}
    div.stButton > button[kind="secondary"]:hover p, div.stButton > button[kind="secondary"]:hover div {{ color: #ffffff !important; }}

    div.stButton > button[kind="tertiary"] {{
        background-color: transparent !important; color: #D4AF37 !important; font-weight: 700 !important;
        border-radius: 20px !important; border: 1.5px solid #D4AF37 !important; width: 100% !important;
        padding: 4px 10px !important; min-height: 0 !important;
    }}
    div.stButton > button[kind="tertiary"] p, div.stButton > button[kind="tertiary"] div {{ color: #D4AF37 !important; margin: 0 !important; }}
    div.stButton > button[kind="tertiary"]:hover {{ background-color: #D4AF37 !important; border-color: #D4AF37 !important; }}
    div.stButton > button[kind="tertiary"]:hover p, div.stButton > button[kind="tertiary"]:hover div {{ color: #ffffff !important; }}

    a.btn-dispensa-pdf {{ display: inline-block; background-color: #ffffff !important; color: #7D001E !important; font-weight: 800 !important; padding: 8px 14px !important; border-radius: 8px !important; border: 2px solid #D4AF37 !important; text-decoration: none !important; text-align: center !important; width: 100% !important; box-sizing: border-box !important; transition: all 0.3s ease !important; box-shadow: 0 4px 6px rgba(212, 175, 55, 0.1) !important; }}
    a.btn-dispensa-pdf:hover {{ background-color: #D4AF37 !important; color: #ffffff !important; box-shadow: 0 6px 12px rgba(212, 175, 55, 0.3) !important;}}

    .global-footer-bar {{
        position: fixed; left: 0; bottom: 0; width: 100%;
        background: linear-gradient(90deg, #7D001E 0%, #4a0011 100%); color: #ffffff;
        text-align: center; padding: 12px 20px; font-size: 0.85rem; font-weight: 500;
        z-index: 999980; box-shadow: 0px -4px 15px rgba(0,0,0,0.2);
        display: flex; justify-content: center; align-items: center; gap: 15px;
    }}
    .global-footer-bar a {{ color: #D4AF37 !important; text-decoration: none; font-weight: 800; }}
    .global-footer-bar a:hover {{ text-decoration: underline; color: #ffffff !important; }}
    </style>
    """
    st.markdown(stili_area_riservata, unsafe_allow_html=True)

    # Footer globale
    st.markdown("""
    <div class="global-footer-bar">
        <span>🎓 <b>Leonardo Scuole</b> - Eccellenza Didattica</span> | 
        <span>Contattaci: segreteria@leonardoscuole.it</span> |
        <a href="https://www.leonardoscuole.it" target="_blank">Visita il nostro sito ufficiale</a>
    </div>
    """, unsafe_allow_html=True)

    # Toggle Menu
    with st.container(key="toggle_menu_btn"):
        if st.button("☰", key="btn_toggle_menu"):
            st.session_state.sidebar_aperta = not st.session_state.sidebar_aperta
            st.rerun()

    dati = st.session_state.dati_utente
    is_admin = (dati.get('email').strip().lower() == EMAIL_ADMIN.strip().lower())
    df_catalogo_base = carica_catalogo_corsi()

    # Header
    nome_solo = dati.get('nominativo', 'Studente').split()[0]
    with st.container(key="header_custom_bar"):
        st.markdown(
            f"<div style='text-align:center; color:#ffffff; font-size:1.35rem; font-weight:800; line-height:65px;'>"
            f"<span style='color:#D4AF37;'>{nome_solo}</span>, benvenuto in <span style='color:#D4AF37;'>Leonardo Scuole</span>"
            f"</div>",
            unsafe_allow_html=True
        )

    # PRIMO ACCESSO: la password temporanea ricevuta via email va cambiata prima di entrare
    if dati.get("primo_accesso"):
        _, col_centro, _ = st.columns([1, 1.4, 1])
        with col_centro:
            with st.container(border=True):
                st.markdown("<h3 style='color:#7D001E; font-weight:800; margin-top:0;'>🔐 Scegli la tua password</h3>", unsafe_allow_html=True)
                st.markdown("<p style='color:#475569;'>È il tuo primo accesso: per proteggere il tuo account sostituisci la password temporanea che hai ricevuto via email.</p>", unsafe_allow_html=True)
                with st.form("form_primo_accesso"):
                    pa_nuova = st.text_input("Nuova password (almeno 8 caratteri)", type="password", key="pa_nuova")
                    pa_conf = st.text_input("Conferma nuova password", type="password", key="pa_conf")
                    pa_invia = st.form_submit_button("💾 Salva e continua", type="primary", use_container_width=True)
                if pa_invia:
                    if pa_nuova != pa_conf or len(pa_nuova.strip()) < 8:
                        st.error("⚠️ Le password devono coincidere ed essere lunghe almeno 8 caratteri.")
                    elif pa_nuova.strip() == str(dati.get("password", "")).strip():
                        st.error("⚠️ La nuova password deve essere diversa da quella temporanea.")
                    else:
                        risposta = chiama_script("CAMBIA_PASSWORD", email=dati.get("email"),
                                                 password_attuale=dati.get("password", ""), nuova_password=pa_nuova)
                        if risposta == "SUCCESS":
                            st.session_state.dati_utente["password"] = pa_nuova.strip()
                            st.session_state.dati_utente["primo_accesso"] = False
                            st.rerun()
                        else:
                            st.error("❌ Salvataggio non riuscito, riprova tra poco.")
                if st.button("🚪 Esci", key="pa_esci", type="tertiary"):
                    st.session_state.autenticato = False
                    st.session_state.dati_utente = {}
                    st.rerun()
        st.stop()

    # Menu Custom
    if st.session_state.sidebar_aperta:
        with st.container(key="menu_custom_panel"):
            st.markdown(f"""
            <div class="menu-logo-box">
                <img src="{LOGO_SRC}" style="width: 160px; margin: 0 auto; display: block;">
            </div>
            """, unsafe_allow_html=True)

            foto_st = dati.get("foto", "")
            if not foto_st or not (foto_st.startswith("data:image") or foto_st.startswith("http")):
                foto_st = "https://cdn-icons-png.flaticon.com/512/3135/3135715.png"

            with st.expander("👤 Profilo & Andamento", expanded=False):
                st.markdown(f"""
                <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center; margin-bottom:12px;">
                    <img src="{foto_st}" style="width:45px; height:45px; border-radius:50%; border:2px solid #D4AF37; object-fit:cover; margin-bottom:6px;">
                    <div>
                        <h5 style="margin:0; font-weight:800; color:#ffffff;">{dati.get('nominativo', 'Studente')}</h5>
                        <p style="font-size:0.8rem; color:#D4AF37; margin:0;">{dati.get('pacchetto', 'Corso Standard')}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                totale_moduli = len(df_catalogo_base[df_catalogo_base['Indirizzo_Studio'] == dati.get('pacchetto')]) if not df_catalogo_base.empty else 10
                completati_cnt = len(st.session_state.moduli_completati)
                percentuale = min(int((completati_cnt / max(totale_moduli, 1)) * 100), 100)
                st.progress(percentuale / 100)
                st.caption(f"📊 Completati: {completati_cnt}/{totale_moduli} ({percentuale}%)")

                st.write("")

                if st.button("👤 Mio Profilo", key="sb_btn_prof", use_container_width=True):
                    st.session_state.sezione_attiva = "Profilo"
                    st.session_state.materia_attiva_card = None
                    st.rerun()

                if is_admin:
                    if st.button("🛠️ Pannello Admin", key="sb_btn_admin", use_container_width=True):
                        st.session_state.sezione_attiva = "Admin"
                        st.session_state.materia_attiva_card = None
                        st.rerun()
                    if st.button("🎓 Vista Studente", key="sb_btn_corsi", use_container_width=True):
                        st.session_state.sezione_attiva = "Corsi"
                        st.session_state.materia_attiva_card = None
                        st.rerun()
                else:
                    if st.button("🎓 Corsi e Didattica", key="sb_btn_corsi", use_container_width=True):
                        st.session_state.sezione_attiva = "Corsi"
                        st.session_state.materia_attiva_card = None
                        st.rerun()

            with st.expander("🎓 Area Attestati", expanded=False):
                st.caption("Scarica l'attestato dei corsi che hai completato.")
                if st.button("🎓 I miei attestati", key="sb_btn_attestati", use_container_width=True):
                    st.session_state.sezione_attiva = "Attestati"
                    st.session_state.materia_attiva_card = None
                    st.rerun()

            with st.expander("📚 Materie del Corso", expanded=False):
                if not df_catalogo_base.empty:
                    df_corso_user = df_catalogo_base[df_catalogo_base['Indirizzo_Studio'] == dati.get('pacchetto')]
                    materie_list = sorted([str(m).strip() for m in df_corso_user['Materia'].dropna().unique() if str(m).strip()])
                else:
                    materie_list = []
                scelta_mat_sb = st.radio("Filtra per materia:", ["Tutte le Materie"] + materie_list, key="radio_materia_sidebar")
                st.session_state.materia_selezionata_sidebar = scelta_mat_sb

            with st.expander("🚪 Account & Sessione", expanded=False):
                if st.button("🚪 Esci", key="sb_btn_logout", use_container_width=True):
                    st.session_state.autenticato = False
                    st.session_state.dati_utente = {}
                    st.session_state.sezione_attiva = "Corsi"
                    st.session_state.materia_attiva_card = None
                    st.rerun()

            st.markdown('<div class="menu-footer-signature">Piattaforma realizzata da SG Managements</div>', unsafe_allow_html=True)

    # CONTENUTO PRINCIPALE
    if st.session_state.sezione_attiva == "Attestati":
        render_area_attestati(dati, is_admin)

    elif st.session_state.sezione_attiva == "Profilo":
        nome_studente = dati.get('nominativo', 'Profilo Utente')
        st.markdown(f'<div class="profile-header-title">👤 Profilo & Valutazioni: {nome_studente}</div>', unsafe_allow_html=True)
        col_foto, col_dati, col_pw = st.columns([1, 1.1, 1.1])

        with col_foto:
            st.markdown("<h3 style='color: #7D001E !important; font-weight: 800;'>Foto Profilo</h3>", unsafe_allow_html=True)
            foto_link = dati.get("foto", "")
            if foto_link and (foto_link.startswith("data:image") or foto_link.startswith("http")):
                st.markdown(f'<img src="{foto_link}" class="profile-img">', unsafe_allow_html=True)
            else:
                st.markdown('<img src="https://cdn-icons-png.flaticon.com/512/3135/3135715.png" class="profile-img">', unsafe_allow_html=True)

            uploaded_file = st.file_uploader("Carica una nuova foto", type=["png", "jpg", "jpeg"], key="upload_profile_pic")
            if uploaded_file is not None:
                bytes_data = uploaded_file.getvalue()
                encoded = base64.b64encode(bytes_data).decode()
                base64_src = f"data:{uploaded_file.type};base64,{encoded}"
                if st.button("Salva Foto", key="btn_save_photo"):
                    risposta = chiama_script("AGGIORNA_FOTO", email=dati.get("email"), password=dati.get("password", ""), foto=base64_src)
                    if risposta == "SUCCESS":
                        st.session_state.dati_utente["foto"] = base64_src
                        st.rerun()
                    elif risposta == "FOTO_TROPPO_GRANDE":
                        st.error("⚠️ Immagine troppo grande: usa una foto più piccola (circa 30 KB).")
                    else:
                        st.error("❌ Salvataggio della foto non riuscito, riprova.")

        with col_dati:
            st.markdown("<h3 style='color: #7D001E !important; font-weight: 800;'>Dati Account</h3>", unsafe_allow_html=True)
            st.markdown(f"<p style='color: #7D001E !important;'><b>ID Cliente:</b> {dati.get('id_cliente')}</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='color: #7D001E !important;'><b>Nominativo:</b> {dati.get('nominativo')}</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='color: #7D001E !important;'><b>Email:</b> {dati.get('email')}</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='color: #7D001E !important;'><b>Pacchetto Acquistato:</b> {dati.get('pacchetto')}</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='color: #7D001E !important;'><b>Data Scadenza:</b> {dati.get('data_scadenza')}</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='color: #7D001E !important;'><b>Stato Account:</b> 🟢 {dati.get('stato')}</p>", unsafe_allow_html=True)

        with col_pw:
            st.markdown("<h3 style='color: #7D001E !important; font-weight: 800;'>🔑 Modifica Password</h3>", unsafe_allow_html=True)
            p_att = st.text_input("Password Attuale", type="password", key="p_att")
            p_nuova = st.text_input("Nuova Password", type="password", key="p_nuov")
            p_conf = st.text_input("Conferma Nuova Password", type="password", key="p_conf")
            if st.button("Aggiorna Password", key="btn_update_pw_profile"):
                if p_nuova != p_conf or len(p_nuova) < 8:
                    st.error("⚠️ Le nuove password devono coincidere ed essere lunghe almeno 8 caratteri.")
                else:
                    risposta = chiama_script("CAMBIA_PASSWORD", email=dati.get("email"), password_attuale=str(p_att).strip(), nuova_password=p_nuova)
                    if risposta == "SUCCESS":
                        st.success("🎉 Password cambiata con successo!")
                        st.session_state.dati_utente["password"] = p_nuova.strip()
                    elif risposta == "PASSWORD_ERRATA":
                        st.error("❌ La password attuale non è corretta.")
                    else:
                        st.error("❌ Aggiornamento non riuscito, riprova.")

        st.divider()
        st.markdown("<h3 style='color: #7D001E !important; font-weight: 800;'>📈 Report Valutazioni & Quiz</h3>", unsafe_allow_html=True)
        q_col1, q_col2 = st.columns(2)
        with q_col1:
            st.table(pd.DataFrame(list(st.session_state.risultati_quiz.items()), columns=["Test / Modulo Esame", "Voto (/30)"]))
        with q_col2:
            voti = list(st.session_state.risultati_quiz.values())
            media_voti = round(sum(voti) / len(voti), 1) if voti else 0.0
            totale_moduli = len(df_catalogo_base[df_catalogo_base['Indirizzo_Studio'] == dati.get('pacchetto')]) if not df_catalogo_base.empty else 10
            completati_cnt = len(st.session_state.moduli_completati)
            percentuale_prof = min(int((completati_cnt / max(totale_moduli, 1)) * 100), 100)
            st.info(f"**Giudizio Sintetico Finale:**\n\nL'alunno **{dati.get('nominativo')}** presenta un andamento complessivo **ECCELLENTE** con una media di **{media_voti}/30** e un tasso di completamento dei moduli pari al **{percentuale_prof}%**.")

    elif st.session_state.sezione_attiva == "Admin" or (is_admin and st.session_state.sezione_attiva == "Corsi" and "vista_admin" in st.session_state):
        df_catalogo = carica_catalogo_corsi()

        st.markdown("<h2 style='color: #7D001E !important; font-weight: 800;'>🛠️ Pannello Amministratore - Caricamento Corsi</h2>", unsafe_allow_html=True)
        st.markdown("<p style='color: #333333;'>Compila il modulo sottostante per inserire nuovi moduli nel database.</p>", unsafe_allow_html=True)
        st.write("")

        base_ind = ["Corso Rumeno", "Liceo Classico", "Liceo Scientifico", "Liceo Scienze Umane", "Liceo Artistico", "Istituto Tecnico"]
        if not df_catalogo.empty and 'Indirizzo_Studio' in df_catalogo.columns:
            list_ind = sorted(list(set(base_ind + [str(x).strip() for x in df_catalogo['Indirizzo_Studio'].dropna().unique() if str(x).strip()])))
        else:
            list_ind = base_ind
        list_ind.append("➕ Aggiungi Nuovo Indirizzo...")

        base_anni = [1, 2, 3, 4, 5]
        if not df_catalogo.empty and 'Anno' in df_catalogo.columns:
            db_anni = [int(x) for x in df_catalogo['Anno'].dropna().unique() if str(x).isdigit()]
            list_anni = sorted(list(set(base_anni + db_anni)))
        else:
            list_anni = base_anni
        list_anni_str = [str(a) for a in list_anni] + ["➕ Aggiungi Nuovo Anno..."]

        base_mat = ["Lingua e Letteratura Italiana", "Matematica", "Fisica", "Lingua e Cultura Latina", "Lingua e Cultura Greca", "Scienze Umane", "Diritto ed Economia", "Lingua Rumena - Base", "Grammatica Rumena"]
        if not df_catalogo.empty and 'Materia' in df_catalogo.columns:
            list_mat = sorted(list(set(base_mat + [str(x).strip() for x in df_catalogo['Materia'].dropna().unique() if str(x).strip()])))
        else:
            list_mat = base_mat
        list_mat.append("➕ Aggiungi Nuova Materia...")

        st.markdown("<h4 style='color: #7D001E;'>➕ Aggiungi Nuovo Modulo / Argomento</h4>", unsafe_allow_html=True)

        col_top1, col_top2, col_top3 = st.columns(3)

        with col_top1:
            sel_ind = st.selectbox("1. Indirizzo di Studio", list_ind, index=0)
            custom_ind = ""
            if sel_ind == "➕ Aggiungi Nuovo Indirizzo...":
                custom_ind = st.text_input("✍️ Nome Nuovo Indirizzo:", placeholder="Es. Liceo Linguistico")

        with col_top2:
            sel_anno = st.selectbox("2. Anno Scolastico", list_anni_str, index=0)
            custom_anno = ""
            if sel_anno == "➕ Aggiungi Nuovo Anno...":
                custom_anno = st.text_input("✍️ Numero/Nome Nuovo Anno:", placeholder="Es. 6")

        with col_top3:
            sel_mat = st.selectbox("3. Materia", list_mat, index=0)
            custom_mat = ""
            if sel_mat == "➕ Aggiungi Nuova Materia...":
                custom_mat = st.text_input("✍️ Nome Nuova Materia:", placeholder="Es. Filosofia")

        with st.form("form_caricamento_admin", clear_on_submit=True):
            c_arg, c_disp, c_vid = st.columns(3)
            with c_arg:
                argomento = st.text_input("Nome Modulo / Argomento *", placeholder="Es. I Promessi Sposi: Capitolo 1")
            with c_disp:
                dispensa = st.text_input("URL Dispensa (PDF/PNG)", placeholder="https://...")
            with c_vid:
                video = st.text_input("URL Video Lezione (MP4/YouTube)", placeholder="https://...")

            descrizione = st.text_area("Descrizione del Modulo / Argomento", placeholder="Inserisci una breve descrizione della lezione...")
            submit_btn = st.form_submit_button("💾 Salva e Pubblica Modulo")

            if submit_btn:
                val_ind = custom_ind.strip() if sel_ind == "➕ Aggiungi Nuovo Indirizzo..." else sel_ind
                val_anno = custom_anno.strip() if sel_anno == "➕ Aggiungi Nuovo Anno..." else sel_anno
                val_mat = custom_mat.strip() if sel_mat == "➕ Aggiungi Nuova Materia..." else sel_mat

                if not val_ind or not val_anno or not val_mat or not argomento:
                    st.error("⚠️ Compila tutti i campi obbligatori: **Indirizzo**, **Anno**, **Materia** e **Argomento**.")
                else:
                    risposta = chiama_script(
                        "AGGIUNGI_CORSO",
                        email=dati.get("email"), password=dati.get("password", ""),
                        Indirizzo_Studio=val_ind, Anno=val_anno, Materia=val_mat,
                        Argomento=argomento, Descrizione=descrizione, Dispensa=dispensa, Video=video
                    )
                    if risposta == "SUCCESS":
                        st.toast(f"✅ Modulo '{argomento}' aggiunto con successo!")
                        st.cache_data.clear()
                        st.rerun()
                    elif risposta == "UNAUTHORIZED":
                        st.error("⛔ Operazione consentita solo all'amministratore.")
                    else:
                        st.error("❌ Salvataggio non riuscito: il modulo non è stato aggiunto al foglio.")

        st.divider()
        st.markdown("<h4 style='color: #7D001E;'>📋 Database Attuale Materiale Didattico</h4>", unsafe_allow_html=True)

        if not df_catalogo.empty:
            ricerca = st.text_input("🔍 Cerca all'interno del catalogo", placeholder="Filtra per materia, indirizzo o argomento...")
            df_display = df_catalogo.copy()
            if ricerca:
                mask = df_display.astype(str).apply(lambda row: row.str.contains(ricerca, case=False).any(), axis=1)
                df_display = df_display[mask]

            st.dataframe(
                df_display,
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("Il database è attualmente vuoto o in fase di caricamento.")

    elif st.session_state.sezione_attiva in ["Corsi", "Programma"]:
        df_catalogo = carica_catalogo_corsi()
        pacchetto_utente = dati.get('pacchetto', 'Liceo Scientifico')

        # L'amministratore puo' vedere qualsiasi corso come lo vede uno studente
        if is_admin:
            indirizzi = {str(pacchetto_utente).strip()}
            if not df_catalogo.empty and 'Indirizzo_Studio' in df_catalogo.columns:
                indirizzi |= {str(x).strip() for x in df_catalogo['Indirizzo_Studio'].dropna().unique() if str(x).strip()}
            indirizzi = sorted(indirizzi)
            pacchetto_utente = st.selectbox(
                "👁️ Anteprima come studente del corso:", indirizzi,
                index=indirizzi.index(str(pacchetto_utente).strip()), key="admin_anteprima_corso"
            )

        if corso_rumeno is not None and str(pacchetto_utente).strip().lower() == corso_rumeno.INDIRIZZO_RUMENO.lower():
            render_corso_rumeno(is_admin)

        elif st.session_state.materia_attiva_card:
            nome_materia_sel = st.session_state.materia_attiva_card
            if st.button("← Torna a Tutte le Materie", key="btn_back_to_cards"):
                st.session_state.materia_attiva_card = None
                st.rerun()

            st.markdown(f"<h2 style='color:#7D001E; font-weight:800; margin-bottom: 20px;'>📚 Materia: {nome_materia_sel}</h2>", unsafe_allow_html=True)
            
            if not df_catalogo.empty:
                df_student = df_catalogo[(df_catalogo['Indirizzo_Studio'] == pacchetto_utente) & (df_catalogo['Materia'] == nome_materia_sel)]
                tab_pendenti, tab_completati = st.tabs(["⏳ Da Studiare", "✅ Lezioni Completate"])

                def render_lista_argomenti(df_lista, is_comp):
                    if df_lista.empty:
                        st.info("Nessun modulo presente in questa scheda.")
                        return

                    for num_arg, (i_row, row_data) in enumerate(df_lista.iterrows(), start=1):
                        titolo_arg = row_data.get('Argomento') if pd.notna(row_data.get('Argomento')) else f"Argomento {num_arg}"
                        anno_curr = row_data.get('Anno', 1)
                        descrizione = row_data.get('Descrizione', 'Nessuna descrizione disponibile per questa lezione.')
                        video_url = row_data.get('Video', '')
                        dispensa_url = row_data.get('Dispensa', '')
                        
                        key_aperto = f"aperto_{titolo_arg}_{i_row}"
                        is_open = st.session_state.moduli_aperti.get(key_aperto, False)

                        # LA CORNICE GRAFICA CON BORDO ORO SOLIDO
                        with st.container(border=True):
                            if is_open:
                                st.markdown("<div class='is-open-card' style='display:none;'></div>", unsafe_allow_html=True)

                            col_num, col_title, col_check = st.columns([1, 7, 2], vertical_alignment="center")

                            with col_num:
                                st.markdown(f"""
                                <div class="argomento-num {'completed' if is_comp else ''}">{num_arg}</div>
                                """, unsafe_allow_html=True)

                            with col_title:
                                key_title = f"title_toggle_{'c' if is_comp else 'p'}_{i_row}"
                                with st.container(key=key_title):
                                    if st.button(f"{titolo_arg}", key=f"btn_title_{'c' if is_comp else 'p'}_{i_row}", use_container_width=True):
                                        st.session_state.moduli_aperti[key_aperto] = not is_open
                                        st.rerun()
                                st.markdown(f"<span class='card-badge badge-anno' style='margin-left:5px;'>{anno_curr}° Anno</span>", unsafe_allow_html=True)

                            with col_check:
                                is_checked = (titolo_arg in st.session_state.moduli_completati)
                                chk_val = st.checkbox("Completato", value=is_checked, key=f"chk_mat_{'c' if is_comp else 'p'}_{i_row}")
                                if chk_val and not is_checked:
                                    st.session_state.moduli_completati.add(titolo_arg)
                                    st.rerun()
                                elif not chk_val and is_checked:
                                    st.session_state.moduli_completati.remove(titolo_arg)
                                    st.rerun()
                                    
                            # SE IL MODULO E' APERTO, MOSTRA IL CONTENUTO
                            if is_open:
                                st.markdown("<hr style='margin: 15px 0 20px 0; border: none; border-top: 1px dashed rgba(212, 175, 55, 0.4);'>", unsafe_allow_html=True)
                                lezione = trova_lezione(titolo_arg)
                                ha_video = pd.notna(video_url) and str(video_url).startswith("http")
                                col_video, col_materiali = st.columns([2, 1])

                                with col_video:
                                    if ha_video:
                                        st.markdown("<h4 style='margin-top:0; color:#7D001E; font-weight:800;'><span style='font-size:1.2rem;'>🎥</span> Video Lezione</h4>", unsafe_allow_html=True)
                                        st.video(video_url)
                                    elif lezione:
                                        render_lezione(lezione)
                                    else:
                                        st.markdown("<h4 style='margin-top:0; color:#7D001E; font-weight:800;'><span style='font-size:1.2rem;'>🎥</span> Video Lezione</h4>", unsafe_allow_html=True)
                                        st.markdown("<div class='custom-info-box'>Nessuna video lezione disponibile al momento per questo modulo.</div>", unsafe_allow_html=True)
                                        
                                with col_materiali:
                                    st.markdown("<h4 style='margin-top:0; color:#7D001E; font-weight:800;'><span style='font-size:1.2rem;'>📚</span> Materiali e Test</h4>", unsafe_allow_html=True)
                                    st.markdown(f"<p style='color: #475569; font-size: 0.95rem; margin-bottom: 20px; line-height: 1.5;'><b>Riassunto:</b> {descrizione}</p>", unsafe_allow_html=True)
                                    
                                    if pd.notna(dispensa_url) and str(dispensa_url).startswith("http"):
                                        st.markdown(f'<a href="{dispensa_url}" target="_blank" class="btn-dispensa-pdf">📄 Scarica Dispensa PDF</a>', unsafe_allow_html=True)
                                    else:
                                        st.markdown("<div class='custom-caption'>Nessuna dispensa PDF caricata.</div>", unsafe_allow_html=True)
                                        
                                    st.markdown("<br>", unsafe_allow_html=True)
                                    
                                    # TASTO TEST PRIMARY FORZATO (Amaranto e Oro via CSS)
                                    quiz_aperto_qui = (st.session_state.quiz_aperto == titolo_arg)
                                    etichetta_quiz = "✖ Chiudi Quiz" if quiz_aperto_qui else "📝 Avvia Test / Quiz"
                                    if st.button(etichetta_quiz, key=f"btn_quiz_{i_row}", type="primary", use_container_width=True):
                                        st.session_state.quiz_aperto = None if quiz_aperto_qui else titolo_arg
                                        st.rerun()

                                # Lezione sotto al video (se il modulo ha sia video sia lezione scritta)
                                if lezione and ha_video:
                                    render_lezione(lezione)

                                # QUIZ A TUTTA LARGHEZZA
                                if st.session_state.quiz_aperto == titolo_arg:
                                    st.markdown("<hr style='margin: 15px 0; border: none; border-top: 1px dashed rgba(212, 175, 55, 0.4);'>", unsafe_allow_html=True)
                                    if lezione and lezione.get("quiz"):
                                        render_quiz(lezione, f"{'c' if is_comp else 'p'}_{i_row}")
                                    else:
                                        st.markdown("<div class='custom-info-box'>Il quiz di questo modulo non è ancora disponibile.</div>", unsafe_allow_html=True)

                with tab_pendenti:
                    df_pend = df_student[~df_student['Argomento'].isin(st.session_state.moduli_completati)]
                    render_lista_argomenti(df_pend, is_comp=False)

                with tab_completati:
                    df_comp = df_student[df_student['Argomento'].isin(st.session_state.moduli_completati)]
                    render_lista_argomenti(df_comp, is_comp=True)

        else:
            # === HERO SECTION ===
            df_student = df_catalogo[df_catalogo['Indirizzo_Studio'] == pacchetto_utente] if not df_catalogo.empty else pd.DataFrame()
            materia_sb = st.session_state.get("materia_selezionata_sidebar", "Tutte le Materie")
            
            tot_moduli_globale = len(df_student)
            if tot_moduli_globale > 0:
                moduli_mat_titoli_globale = set(df_student['Argomento'].dropna().unique())
                completati_mat_globale = len(moduli_mat_titoli_globale.intersection(st.session_state.moduli_completati))
                percento_globale = min(int((completati_mat_globale / max(tot_moduli_globale, 1)) * 100), 100)
            else:
                completati_mat_globale = 0
                percento_globale = 0

            nome_solo_hero = dati.get('nominativo', 'Studente').split()[0]

            hero_html = f"""
            <div style="background: linear-gradient(135deg, #7D001E 0%, #5c0016 100%); border-radius: 16px; padding: 35px 40px; color: white; margin-bottom: 35px; box-shadow: 0 10px 30px rgba(125,0,30,0.25); display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 20px;">
                <div style="flex: 1; min-width: 250px;">
                    <h1 style="color: #D4AF37; margin-top: 0; font-weight: 900; font-size: 2.2rem; margin-bottom: 10px;">Bentornato, {nome_solo_hero}! 🎓</h1>
                    <p style="font-size: 1.15rem; opacity: 0.9; margin-bottom: 0; line-height: 1.5;">Il tuo percorso nel <b>{pacchetto_utente}</b> ti aspetta.<br>Continua a studiare per raggiungere i tuoi obiettivi!</p>
                </div>
                <div style="flex: 0 1 280px; background: rgba(255, 255, 255, 0.1); padding: 25px; border-radius: 16px; backdrop-filter: blur(10px); border: 1px solid rgba(212, 175, 55, 0.3); text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                    <div style="font-size: 0.85rem; color: #F3DFA0; text-transform: uppercase; font-weight: 800; letter-spacing: 1px; margin-bottom: 10px;">Progresso Generale</div>
                    <div style="font-size: 3rem; font-weight: 900; line-height: 1; color: #ffffff;">{percento_globale}%</div>
                    <div style="width: 100%; background-color: rgba(0,0,0,0.2); border-radius: 999px; height: 8px; margin-top: 15px; overflow: hidden; border: 1px solid rgba(255,255,255,0.1);">
                        <div style="width: {percento_globale}%; background-color: #D4AF37; height: 100%; border-radius: 999px; box-shadow: 0 0 10px rgba(212, 175, 55, 0.5);"></div>
                    </div>
                    <div style="font-size: 0.8rem; color: rgba(255,255,255,0.7); margin-top: 10px;">{completati_mat_globale} lezioni su {tot_moduli_globale} completate</div>
                </div>
            </div>
            """
            st.markdown(hero_html, unsafe_allow_html=True)

            if materia_sb != "Tutte le Materie":
                df_student = df_student[df_student['Materia'] == materia_sb]

            if not df_student.empty:
                materie_uniche = sorted([str(m).strip() for m in df_student['Materia'].dropna().unique() if str(m).strip()])
                cols_card = st.columns(3)

                for idx_mat, nome_materia in enumerate(materie_uniche):
                    col_target = cols_card[idx_mat % 3]
                    df_mat_curr = df_student[df_student['Materia'] == nome_materia]
                    tot_moduli = len(df_mat_curr)
                    moduli_mat_titoli = set(df_mat_curr['Argomento'].dropna().unique())
                    completati_mat = len(moduli_mat_titoli.intersection(st.session_state.moduli_completati))
                    percento_mat = min(int((completati_mat / max(tot_moduli, 1)) * 100), 100)

                    img_banner = IMMAGINI_MATERIE.get(nome_materia, IMMAGINE_DEFAULT)

                    with col_target:
                        st.markdown(f"""
                        <div class="materia-card-img-container">
                            <img src="{img_banner}" class="materia-banner-img">
                            <div class="materia-card-body">
                                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 5px;">
                                    <div class="materia-card-title">{nome_materia}</div>
                                    <span class="card-badge badge-anno">{tot_moduli} Moduli</span>
                                </div>
                                <div style="width: 100%; background-color: #e2e8f0; border-radius: 999px; height: 8px; margin-top: 15px; margin-bottom: 8px; overflow: hidden;">
                                    <div style="width: {percento_mat}%; background-color: #D4AF37; height: 100%; border-radius: 999px; transition: width 0.5s ease;"></div>
                                </div>
                                <div class="materia-card-sub">{completati_mat}/{tot_moduli} completati ({percento_mat}%)</div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                        if st.button(f"📖 Apri {nome_materia}", key=f"btn_open_card_{idx_mat}"):
                            st.session_state.materia_attiva_card = nome_materia
                            st.rerun()

                        st.write("")
