// =====================================================================
//  LEONARDO SCUOLE - Web App (versione sicura)
//  Riceve le richieste dell'app Streamlit. Ogni richiesta deve contenere
//  la chiave segreta (token): senza chiave lo script non fa nulla.
// =====================================================================

var OTP_VALIDITA_SEC = 10 * 60;   // il codice OTP vale 10 minuti
var OTP_MAX_TENTATIVI = 5;        // tentativi possibili per ogni codice
var OTP_MAX_INVII_ORA = 3;        // codici inviabili per email in un'ora
var LOGIN_MAX_ERRORI = 10;        // password errate prima del blocco
var LOGIN_BLOCCO_SEC = 15 * 60;   // durata del blocco
var PASSWORD_MIN = 8;
var FOTO_MAX_CARATTERI = 49000;   // limite di una cella di Google Fogli

// La configurazione (chiave segreta, email admin, catalogo) e' salvata in
// Impostazioni progetto -> Proprieta' script. Non serve scriverla qui.

// ---------------------------------------------------------------------
//  INGRESSO
// ---------------------------------------------------------------------
function doPost(e) {
  var data = leggiDati_(e);
  var tokenAtteso = PropertiesService.getScriptProperties().getProperty("APP_TOKEN");
  if (!tokenAtteso || String(data.token || "") !== tokenAtteso) {
    return testo_("UNAUTHORIZED");
  }

  // Solo le azioni che SCRIVONO nel foglio passano una alla volta; login e letture vanno in parallelo
  var azione = String(data.azione || "");
  var lock = null;
  if (AZIONI_IN_FILA[azione]) {
    lock = LockService.getScriptLock();
    if (!lock.tryLock(25000)) return testo_("OCCUPATO");
  }
  try {
    switch (azione) {
      case "LOGIN":           return login_(data);
      case "RICHIEDI_OTP":    return richiediOtp_(data);
      case "RESET_PASSWORD":  return resetPassword_(data);
      case "CAMBIA_PASSWORD": return cambiaPassword_(data);
      case "AGGIORNA_FOTO":   return aggiornaFoto_(data);
      case "AGGIUNGI_CORSO":  return aggiungiCorso_(data);
      case "SALVA_PROGRESSI": return salvaProgressi_(data);
      case "LEGGI_PROGRESSI": return leggiProgressi_(data);
      case "SALVA_CONFIG":    return salvaConfig_(data);
      case "LEGGI_CONFIG":    return leggiConfig_();
      default:                return testo_("UNKNOWN_ACTION");
    }
  } catch (err) {
    console.error(err);
    return testo_("ERROR");
  } finally {
    if (lock) lock.releaseLock();
  }
}

var AZIONI_IN_FILA = {
  RESET_PASSWORD: true, CAMBIA_PASSWORD: true, AGGIORNA_FOTO: true,
  AGGIUNGI_CORSO: true, SALVA_PROGRESSI: true, SALVA_CONFIG: true
};

function doGet(e) {
  return testo_("OK");
}

// ---------------------------------------------------------------------
//  AZIONI
// ---------------------------------------------------------------------
function login_(d) {
  var email = normEmail_(d.email);
  var cache = CacheService.getScriptCache();
  var chiaveErr = "loginerr_" + email;
  var errori = Number(cache.get(chiaveErr) || 0);
  if (errori >= LOGIN_MAX_ERRORI) return json_({ esito: "BLOCCATO" });

  var u = trovaUtente_(email);
  if (!u || !passwordValida_(valore_(u, "Password"), d.password)) {
    cache.put(chiaveErr, String(errori + 1), LOGIN_BLOCCO_SEC);
    return json_({ esito: "CREDENZIALI_ERRATE" });
  }
  cache.remove(chiaveErr);

  // Abbonamento scaduto (l'amministratore non viene mai bloccato)
  var eAdmin = email === normEmail_(PropertiesService.getScriptProperties().getProperty("EMAIL_ADMIN"));
  if (!eAdmin && scaduto_(valore_(u, "Data Scadenza"))) {
    return json_({ esito: "SCADUTO", data_scadenza: formattaData_(valore_(u, "Data Scadenza")) });
  }

  // Se la password nel foglio e' ancora in chiaro, la sostituisce con la versione cifrata
  if (!eHash_(valore_(u, "Password"))) {
    var lockHash = LockService.getScriptLock();
    if (lockHash.tryLock(5000)) {           // se e' occupato la cifra al prossimo accesso
      try { scrivi_(u, "Password", creaHash_(d.password)); } finally { lockHash.releaseLock(); }
    }
  }

  return json_({
    esito: "OK",
    utente: {
      id_cliente: String(valore_(u, "IDcliente") || "1"),
      nominativo: String(valore_(u, "Nominativo") || email),
      stato: String(valore_(u, "Stato") || "Attivo").trim(),
      email: email,
      data_scadenza: formattaData_(valore_(u, "Data Scadenza")),
      pacchetto: String(valore_(u, "Pacchetto Acquistato") || "Liceo Scientifico").trim(),
      foto: String(valore_(u, "Foto") || ""),
      primo_accesso: String(valore_(u, "Primo_Accesso") || "").trim().toUpperCase() === "SI"
    }
  });
}

function richiediOtp_(d) {
  var email = normEmail_(d.email);
  var u = trovaUtente_(email);
  if (!u) return testo_("SUCCESS"); // risposta identica: non riveliamo quali email esistono

  var cache = CacheService.getScriptCache();
  var chiaveInvii = "otpinvii_" + email;
  var invii = Number(cache.get(chiaveInvii) || 0);
  if (invii >= OTP_MAX_INVII_ORA) return testo_("TROPPE_RICHIESTE");

  var otp = generaOtp_();
  cache.put("otp_" + email, JSON.stringify({
    hash: hash_(otp, email),
    scadenza: Date.now() + OTP_VALIDITA_SEC * 1000,
    tentativi: 0
  }), OTP_VALIDITA_SEC);
  cache.put(chiaveInvii, String(invii + 1), 3600);

  inviaEmail_(email, "Leonardo Scuole - Codice di Recupero Password", nome_(u),
    "<p>Il tuo codice di verifica per il reset della password è:</p>" +
    "<div style='background-color: #7D001E; color: #D4AF37; font-size: 26px; font-weight: bold; padding: 15px; text-align: center; border-radius: 8px; letter-spacing: 5px; margin: 20px 0;'>" + otp + "</div>" +
    "<p>Il codice è valido per <b>10 minuti</b>. Se non hai richiesto tu il codice, ignora questa email.</p>");
  return testo_("SUCCESS");
}

function resetPassword_(d) {
  var email = normEmail_(d.email);
  var cache = CacheService.getScriptCache();
  var chiave = "otp_" + email;
  var rec = JSON.parse(cache.get(chiave) || "null");

  if (!rec || Date.now() > rec.scadenza || rec.tentativi >= OTP_MAX_TENTATIVI) {
    cache.remove(chiave);
    return testo_("OTP_SCADUTO");
  }
  if (hash_(String(d.otp || "").trim(), email) !== rec.hash) {
    rec.tentativi += 1;
    cache.put(chiave, JSON.stringify(rec), Math.max(1, Math.ceil((rec.scadenza - Date.now()) / 1000)));
    return testo_("OTP_ERRATO");
  }
  if (String(d.nuova_password || "").trim().length < PASSWORD_MIN) return testo_("PASSWORD_CORTA");

  var u = trovaUtente_(email);
  if (!u) return testo_("OTP_SCADUTO");
  scrivi_(u, "Password", creaHash_(d.nuova_password));
  scrivi_(u, "Primo_Accesso", "NO");
  cache.remove(chiave);
  emailConfermaPassword_(email, nome_(u));
  return testo_("SUCCESS");
}

function cambiaPassword_(d) {
  var email = normEmail_(d.email);
  var u = trovaUtente_(email);
  if (!u || !passwordValida_(valore_(u, "Password"), d.password_attuale)) return testo_("PASSWORD_ERRATA");
  if (String(d.nuova_password || "").trim().length < PASSWORD_MIN) return testo_("PASSWORD_CORTA");
  scrivi_(u, "Password", creaHash_(d.nuova_password));
  scrivi_(u, "Primo_Accesso", "NO");
  emailConfermaPassword_(email, nome_(u));
  return testo_("SUCCESS");
}

function aggiornaFoto_(d) {
  var email = normEmail_(d.email);
  var u = trovaUtente_(email);
  if (!u || !passwordValida_(valore_(u, "Password"), d.password)) return testo_("UNAUTHORIZED");
  var foto = String(d.foto || "");
  if (foto.length > FOTO_MAX_CARATTERI) return testo_("FOTO_TROPPO_GRANDE");
  scrivi_(u, "Foto", foto);
  return testo_("SUCCESS");
}

function aggiungiCorso_(d) {
  var props = PropertiesService.getScriptProperties();
  var email = normEmail_(d.email);
  var u = trovaUtente_(email);
  if (email !== normEmail_(props.getProperty("EMAIL_ADMIN")) || !u || !passwordValida_(valore_(u, "Password"), d.password)) {
    return testo_("UNAUTHORIZED");
  }

  var ss = SpreadsheetApp.openById(props.getProperty("CATALOGO_ID"));
  var gid = Number(props.getProperty("CATALOGO_GID"));
  var foglio = ss.getSheets().filter(function (s) { return s.getSheetId() === gid; })[0];
  if (!foglio) return testo_("CATALOGO_NON_TROVATO");

  var alias = {
    Indirizzo_Studio: ["Indirizzo_Studio", "Indirizzo Studio"],
    Anno: ["Anno", "Anno_Scolastico", "Anno_Scolastico:", "Anno Scolastico"],
    Materia: ["Materia", "NOME_MATERIA", "Nome_Materia"],
    Argomento: ["Argomento", "NomeModulo"],
    Descrizione: ["Descrizione", "DescrizioneModulo"],
    Dispensa: ["Dispensa", "FileDispensa"],
    Video: ["Video", "VideoLezione"]
  };
  var intestazioni = foglio.getRange(1, 1, 1, foglio.getLastColumn()).getValues()[0];
  var riga = intestazioni.map(function (h) {
    var nome = String(h).trim();
    for (var campo in alias) {
      if (alias[campo].indexOf(nome) !== -1) return d[campo] !== undefined ? String(d[campo]) : "";
    }
    return "";
  });
  foglio.appendRow(riga);
  return testo_("SUCCESS");
}

// ---------------------------------------------------------------------
//  PROGRESSI DEGLI STUDENTI (servono per riprendere il corso e per l'attestato)
// ---------------------------------------------------------------------
function utenteVerificato_(d) {
  var u = trovaUtente_(normEmail_(d.email));
  return (u && passwordValida_(valore_(u, "Password"), d.password)) ? u : null;
}

function foglioProgressi_() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sh = ss.getSheetByName("Progressi");
  if (!sh) {
    sh = ss.insertSheet("Progressi");
    sh.appendRow(["Email", "Progressi (JSON)", "Aggiornato il"]);
  }
  return sh;
}

function salvaProgressi_(d) {
  if (!utenteVerificato_(d)) return testo_("UNAUTHORIZED");
  var email = normEmail_(d.email);
  var sh = foglioProgressi_();
  var dati = sh.getDataRange().getValues();
  for (var i = 1; i < dati.length; i++) {
    if (normEmail_(dati[i][0]) === email) {
      sh.getRange(i + 1, 2, 1, 2).setValues([[String(d.progressi || "{}"), new Date()]]);
      return testo_("SUCCESS");
    }
  }
  sh.appendRow([email, String(d.progressi || "{}"), new Date()]);
  return testo_("SUCCESS");
}

function leggiProgressi_(d) {
  if (!utenteVerificato_(d)) return testo_("{}");
  var email = normEmail_(d.email);
  var dati = foglioProgressi_().getDataRange().getValues();
  for (var i = 1; i < dati.length; i++) {
    if (normEmail_(dati[i][0]) === email) return testo_(String(dati[i][1] || "{}"));
  }
  return testo_("{}");
}

// ---------------------------------------------------------------------
//  PANNELLO DI CONTROLLO (colori, logo, testi): solo il proprietario
// ---------------------------------------------------------------------
var PEZZO_CONFIG = 40000; // una cella tiene al massimo 50.000 caratteri

function foglioConfig_() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  return ss.getSheetByName("Config") || ss.insertSheet("Config");
}

function salvaConfig_(d) {
  var proprietario = normEmail_(PropertiesService.getScriptProperties().getProperty("EMAIL_ADMIN"));
  if (normEmail_(d.email) !== proprietario || !utenteVerificato_(d)) return testo_("UNAUTHORIZED");
  var testo = String(d.config || "{}");
  var pezzi = [];
  for (var i = 0; i < testo.length; i += PEZZO_CONFIG) pezzi.push([testo.substring(i, i + PEZZO_CONFIG)]);
  var sh = foglioConfig_();
  sh.clear();
  sh.getRange(1, 1, 1, 2).setValues([["Aggiornato il", new Date()]]);
  if (pezzi.length) sh.getRange(2, 1, pezzi.length, 1).setValues(pezzi);
  return testo_("SUCCESS");
}

function leggiConfig_() {
  var sh = foglioConfig_();
  var ultima = sh.getLastRow();
  if (ultima < 2) return testo_("{}");
  var valori = sh.getRange(2, 1, ultima - 1, 1).getValues();
  return testo_(valori.map(function (r) { return String(r[0]); }).join("") || "{}");
}

// ---------------------------------------------------------------------
//  FUNZIONI DI SUPPORTO
// ---------------------------------------------------------------------
function leggiDati_(e) {
  if (e && e.postData && e.postData.type && e.postData.type.indexOf("json") !== -1) {
    try { return JSON.parse(e.postData.contents); } catch (err) {}
  }
  return (e && e.parameter) ? e.parameter : {};
}

function testo_(t) {
  return ContentService.createTextOutput(t).setMimeType(ContentService.MimeType.TEXT);
}

function json_(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON);
}

function normEmail_(v) {
  return String(v || "").trim().toLowerCase();
}

function trovaUtente_(email) {
  if (!email) return null;
  var foglio = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  var valori = foglio.getDataRange().getValues();
  if (valori.length < 2) return null;
  var intestazioni = valori[0].map(function (h) { return String(h).trim(); });
  var colEmail = intestazioni.indexOf("Email");
  if (colEmail === -1) return null;
  for (var i = 1; i < valori.length; i++) {
    if (normEmail_(valori[i][colEmail]) === email) {
      return { foglio: foglio, riga: i + 1, valori: valori[i], intestazioni: intestazioni };
    }
  }
  return null;
}

function valore_(u, colonna) {
  var c = u.intestazioni.indexOf(colonna);
  return c === -1 ? "" : u.valori[c];
}

function scrivi_(u, colonna, valore) {
  var c = u.intestazioni.indexOf(colonna);
  if (c !== -1) u.foglio.getRange(u.riga, c + 1).setValue(valore);
}

function nome_(u) {
  return String(valore_(u, "Nominativo") || "Studente");
}

function scaduto_(v) {
  var d = null;
  if (v instanceof Date) {
    d = v;
  } else {
    var m = String(v || "").trim().match(/^(\d{1,2})\/(\d{1,2})\/(\d{4})$/);
    if (m) d = new Date(Number(m[3]), Number(m[2]) - 1, Number(m[1]));
  }
  if (!d || isNaN(d.getTime())) return false; // nessuna data valida: nessun blocco
  var fineGiorno = new Date(d.getFullYear(), d.getMonth(), d.getDate(), 23, 59, 59);
  return new Date() > fineGiorno;
}

function formattaData_(v) {
  if (v instanceof Date) return Utilities.formatDate(v, Session.getScriptTimeZone(), "dd/MM/yyyy");
  return String(v || "-");
}

// Password: salvate come "sha256$sale$impronta", mai in chiaro
function hash_(testo, sale) {
  var byte = Utilities.computeDigest(Utilities.DigestAlgorithm.SHA_256, sale + "|" + testo, Utilities.Charset.UTF_8);
  return byte.map(function (b) { return ("0" + (b & 0xff).toString(16)).slice(-2); }).join("");
}

function eHash_(salvata) {
  return String(salvata || "").indexOf("sha256$") === 0;
}

function creaHash_(password) {
  var sale = Utilities.getUuid().replace(/-/g, "");
  return "sha256$" + sale + "$" + hash_(String(password).trim(), sale);
}

function passwordValida_(salvata, inserita) {
  salvata = String(salvata || "");
  inserita = String(inserita || "").trim();
  if (!inserita) return false;
  if (eHash_(salvata)) {
    var parti = salvata.split("$");
    return parti.length === 3 && hash_(inserita, parti[1]) === parti[2];
  }
  return salvata.trim() !== "" && salvata.trim() === inserita;
}

function generaOtp_() {
  var byte = Utilities.computeDigest(Utilities.DigestAlgorithm.SHA_256, Utilities.getUuid() + Utilities.getUuid(), Utilities.Charset.UTF_8);
  var otp = "";
  for (var i = 0; i < 6; i++) otp += String((byte[i] & 0xff) % 10);
  return otp;
}

function inviaEmail_(destinatario, oggetto, nome, corpo) {
  MailApp.sendEmail({
    to: destinatario,
    name: "Leonardo Scuole",
    replyTo: "no-reply@leonardoscuole.it",
    subject: oggetto,
    htmlBody: "<div style='font-family: Arial, sans-serif; padding: 20px; border: 2px solid #D4AF37; border-radius: 10px; background-color: #ffffff;'>" +
              "<h2 style='color: #7D001E;'>Leonardo Scuole</h2>" +
              "<p>Ciao <b>" + escapeHtml_(nome) + "</b>,</p>" + corpo +
              "<p style='font-size: 0.85rem; color: #777;'>Questa è una mail automatica generata da un indirizzo non monitorato (no-reply). Si prega di non rispondere.</p>" +
              "</div>"
  });
}

function emailConfermaPassword_(email, nome) {
  try {
    inviaEmail_(email, "Leonardo Scuole - Conferma Cambio Password", nome,
      "<p>La password del tuo account è stata <b>aggiornata con successo</b>.</p>" +
      "<p>Se non sei stato tu ad effettuare questa modifica, contatta immediatamente la segreteria didattica.</p>");
  } catch (err) {}
}

function escapeHtml_(t) {
  return String(t).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}
