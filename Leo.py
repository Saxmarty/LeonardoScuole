import streamlit as st
import pandas as pd
import requests
import base64
import random

# 1. CONFIGURAZIONE PAGINA
st.set_page_config(
    page_title="Leonardo Scuole - Area Riservata",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

WEB_APP_URL = "https://script.google.com/macros/s/AKfycbxDUpdEfTdpb87LLVpojzilavVfpEXldiSWvciWdyzn9vP_WD5jj9XTsIKZJ2-BODyN3g/exec"
SPREADSHEET_CATALOGO_ID = "1e5DD36IPkFzKi1I2dAtAGXJNLJU8PO56M2dNIGPOuVc"
CATALOGO_GID = "698645009"
EMAIL_ADMIN = "gison.salvatore@gmail.com"

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
    "Educazione Civica": "https://images.unsplash.com/photo-1541872703-74c5e44368f9?auto=format&fit=crop&w=600&q=80"
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

if "otp_generato" not in st.session_state:
    st.session_state.otp_generato = ""

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
        return df
    except Exception as e:
        st.error(f"Errore nel caricamento del catalogo: {e}")
        return pd.DataFrame()

def invia_email_otp_google_script(email, otp_code):
    try:
        payload = {"azione": "INVIA_OTP", "email": email, "otp_code": otp_code}
        res = requests.post(WEB_APP_URL, data=payload, timeout=15)
        return (True, "OK") if "SUCCESS" in res.text else (False, f"Risposta server: {res.text[:50]}")
    except Exception as e:
        return False, str(e)

def aggiorna_password_google_sheet(email, nuova_password):
    try:
        payload = {"email": email, "nuova_password": nuova_password, "primo_accesso": "NO"}
        res = requests.post(WEB_APP_URL, data=payload, timeout=10)
        return res.status_code == 200 and ("SUCCESS" in res.text)
    except Exception:
        return False

def aggiorna_foto_google_sheet(email, foto_base64_or_url):
    try:
        payload = {"email": email, "foto": foto_base64_or_url}
        res = requests.post(WEB_APP_URL, data=payload, timeout=10)
        return res.status_code == 200 and ("SUCCESS" in res.text)
    except Exception:
        return False

def verifica_credenziali(email_input, password_input, ricordami_spuntato):
    SPREADSHEET_ID = "1WnnnrDvRSOtxFa09TWLo9_AqK4zeOdh73-Hg5E1ZnnU"
    url = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/export?format=csv"
    try:
        df = pd.read_csv(url)
        df.columns = df.columns.str.strip()
        df['Email'] = df['Email'].astype(str).str.strip().str.lower()
        df['Password'] = df['Password'].astype(str).str.strip()

        email_clean = email_input.strip().lower()
        password_clean = str(password_input).strip()

        utente = df[(df['Email'] == email_clean) & (df['Password'] == password_clean)]
        if utente.empty:
            st.error("❌ Email o password non corrette.")
            return False

        riga = utente.iloc[0]
        stato_utente = str(riga.get('Stato', 'Attivo')).strip()
        if stato_utente.lower() != 'attivo':
            st.error(f"⛔ Accesso negato: Account '{stato_utente}'. Contatta la segreteria.")
            return False

        nominativo_usr = riga.get('Nominativo', email_clean)
        foto_url = str(riga.get('Foto', '')).strip()

        st.session_state.dati_utente = {
            "id_cliente": str(riga.get('IDcliente', '1')),
            "nominativo": nominativo_usr,
            "stato": stato_utente,
            "email": email_clean,
            "password": password_clean,
            "data_scadenza": str(riga.get('Data Scadenza', '-')),
            "pacchetto": str(riga.get('Pacchetto Acquistato', 'Liceo Scientifico')),
            "foto": foto_url if foto_url.lower() != "nan" else ""
        }
        return True
    except Exception as e:
        st.error(f"Errore di connessione: {e}")
        return False

def verifica_email_esistente(email_input):
    SPREADSHEET_ID = "1WnnnrDvRSOtxFa09TWLo9_AqK4zeOdh73-Hg5E1ZnnU"
    url = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/export?format=csv"
    try:
        df = pd.read_csv(url)
        df.columns = df.columns.str.strip()
        df['Email'] = df['Email'].astype(str).str.strip().str.lower()
        return not df[df['Email'] == email_input.strip().lower()].empty
    except Exception:
        return False


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
    div[data-testid="stDialog"] .stButton > button:not([kind="tertiary"]) {
        background-color: #D4AF37 !important; color: #7D001E !important; font-weight: 800 !important; width: 100% !important; border: 2px solid #D4AF37 !important; margin-top: 10px !important;
    }
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
    
    email = st.text_input("Email", value="gison.salvatore@gmail.com", placeholder="Email", label_visibility="collapsed", key="in_email")
    password = st.text_input("Password", value="121212", type="password", placeholder="Password", label_visibility="collapsed", key="in_pw")
    ricordami = st.checkbox("Ricordami", value=True, key="in_remember")

    if st.button("Accedi", key="btn_login_act"):
        if email and password:
            if verifica_credenziali(email, password, ricordami):
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
            st.session_state.otp_generato = ""
            st.rerun()
        return

    email_rec = st.text_input("Email recupero", placeholder="E-mail registrata", label_visibility="collapsed", key="rec_email_in")

    if st.button("Invia codice OTP via email", key="btn_send_otp_single"):
        if email_rec and verifica_email_esistente(email_rec):
            code_otp = str(random.randint(100000, 999999))
            st.session_state.otp_generato = code_otp
            esito, msgg = invia_email_otp_google_script(email_rec.strip().lower(), code_otp)
            if esito:
                st.success("📩 Codice inviato con successo!")
            else:
                st.error(f"❌ {msgg}")

    st.divider()
    otp_val = st.text_input("Codice OTP", placeholder="Codice OTP a 6 cifre", label_visibility="collapsed", key="rec_otp_in")
    new_p1 = st.text_input("Nuova Password", type="password", placeholder="Nuova Password", label_visibility="collapsed", key="rec_p1_in")
    new_p2 = st.text_input("Conferma Password", type="password", placeholder="Conferma Nuova Password", label_visibility="collapsed", key="rec_p2_in")

    if st.button("Aggiorna Password", key="btn_save_pw_single"):
        if email_rec and otp_val == st.session_state.otp_generato and new_p1 == new_p2 and len(new_p1) >= 6:
            if aggiorna_password_google_sheet(email_rec.strip().lower(), new_p1):
                st.session_state.password_cambiata_successo = True
                st.rerun()

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
            st.image("https://i.ibb.co/PZHspbqt/TV1-copia-2.jpg", width=240)
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

    # Menu Custom
    if st.session_state.sidebar_aperta:
        with st.container(key="menu_custom_panel"):
            st.markdown("""
            <div class="menu-logo-box">
                <img src="https://i.ibb.co/PZHspbqt/TV1-copia-2.jpg" style="width: 160px; margin: 0 auto; display: block;">
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
    if st.session_state.sezione_attiva == "Profilo":
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
                    st.session_state.dati_utente["foto"] = base64_src
                    aggiorna_foto_google_sheet(dati.get("email"), base64_src)
                    st.success("✅ Foto profilo aggiornata con successo!")
                    st.rerun()

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
                if p_nuova == p_conf and len(p_nuova) >= 6:
                    if aggiorna_password_google_sheet(dati.get("email"), p_nuova):
                        st.success("🎉 Password cambiata con successo!")
                        st.session_state.dati_utente["password"] = p_nuova
                else:
                    st.error("⚠️ Verifica le password inserite.")

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
                    payload = {
                        "azione": "AGGIUNGI_CORSO",
                        "Indirizzo_Studio": val_ind,
                        "Anno": val_anno,
                        "Materia": val_mat,
                        "Argomento": argomento,
                        "Descrizione": descrizione,
                        "Dispensa": dispensa,
                        "Video": video
                    }
                    try:
                        res = requests.post(WEB_APP_URL, json=payload, timeout=10)
                        if res.status_code == 200:
                            st.success(f"✅ Modulo **'{argomento}'** aggiunto con successo!")
                            st.cache_data.clear()
                            st.rerun()
                        else:
                            st.error(f"❌ Errore durante il salvataggio: HTTP {res.status_code}")
                    except Exception as e:
                        st.error(f"❌ Errore di connessione: {e}")

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

        if st.session_state.materia_attiva_card:
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
                                col_video, col_materiali = st.columns([2, 1])
                                
                                with col_video:
                                    st.markdown("<h4 style='margin-top:0; color:#7D001E; font-weight:800;'><span style='font-size:1.2rem;'>🎥</span> Video Lezione</h4>", unsafe_allow_html=True)
                                    if pd.notna(video_url) and str(video_url).startswith("http"):
                                        st.video(video_url)
                                    else:
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
                                    st.button("📝 Avvia Test / Quiz", key=f"btn_quiz_{i_row}", type="primary", use_container_width=True)

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