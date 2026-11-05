/**
 * LEONARDO SCUOLE - salvataggio progressi studenti (serve per l'attestato di fine corso)
 *
 * Senza queste due azioni la piattaforma funziona lo stesso, ma i moduli superati
 * restano solo per la sessione: chiudendo il browser lo studente riparte da zero.
 *
 * COME INSTALLARE
 * 1. Apri lo script Google collegato alla piattaforma (quello che gestisce LOGIN, RICHIEDI_OTP, ...).
 * 2. Incolla in fondo le due funzioni qui sotto.
 * 3. Nella funzione doPost, dove smisti le azioni, aggiungi:
 *
 *      if (azione === "SALVA_PROGRESSI") return salvaProgressi_(e.parameter);
 *      if (azione === "LEGGI_PROGRESSI") return leggiProgressi_(e.parameter);
 *      if (azione === "SALVA_CONFIG")    return salvaConfig_(e.parameter);
 *      if (azione === "LEGGI_CONFIG")    return leggiConfig_();
 *
 *    (mettile DOPO il controllo del token, come le altre azioni).
 * 4. Distribuisci > Gestisci distribuzioni > modifica > Nuova versione.
 *
 * I fogli "Progressi" e "Config" vengono creati da soli al primo salvataggio.
 * SALVA_CONFIG (pannello di controllo) accetta solo l'email del proprietario.
 * Per sicurezza le funzioni ricontrollano email e password con verificaUtente_():
 * sostituiscila con la funzione che il tuo script usa gia' per il LOGIN.
 */

function foglioProgressi_() {
  var ss = SpreadsheetApp.getActive();
  var sh = ss.getSheetByName("Progressi");
  if (!sh) {
    sh = ss.insertSheet("Progressi");
    sh.appendRow(["Email", "Progressi (JSON)", "Aggiornato il"]);
  }
  return sh;
}

function salvaProgressi_(p) {
  var email = String(p.email || "").trim().toLowerCase();
  if (!email || !verificaUtente_(email, p.password)) return ContentService.createTextOutput("UNAUTHORIZED");
  var sh = foglioProgressi_();
  var dati = sh.getDataRange().getValues();
  for (var i = 1; i < dati.length; i++) {
    if (String(dati[i][0]).trim().toLowerCase() === email) {
      sh.getRange(i + 1, 2, 1, 2).setValues([[p.progressi || "{}", new Date()]]);
      return ContentService.createTextOutput("SUCCESS");
    }
  }
  sh.appendRow([email, p.progressi || "{}", new Date()]);
  return ContentService.createTextOutput("SUCCESS");
}

function leggiProgressi_(p) {
  var email = String(p.email || "").trim().toLowerCase();
  if (!email || !verificaUtente_(email, p.password)) return ContentService.createTextOutput("{}");
  var dati = foglioProgressi_().getDataRange().getValues();
  for (var i = 1; i < dati.length; i++) {
    if (String(dati[i][0]).trim().toLowerCase() === email) {
      return ContentService.createTextOutput(String(dati[i][1] || "{}"));
    }
  }
  return ContentService.createTextOutput("{}");
}

/** DA SOSTITUIRE con la verifica gia' usata dall'azione LOGIN del tuo script. */
function verificaUtente_(email, password) {
  return true;
}


/* ---------- PANNELLO DI CONTROLLO: colori, logo, testi ---------- */
var PROPRIETARIO_PANNELLO = "gison.salvatore@gmail.com";
var PEZZO = 40000; // una cella di Google Sheets tiene al massimo 50.000 caratteri

function foglioConfig_() {
  var ss = SpreadsheetApp.getActive();
  return ss.getSheetByName("Config") || ss.insertSheet("Config");
}

function salvaConfig_(p) {
  var email = String(p.email || "").trim().toLowerCase();
  if (email !== PROPRIETARIO_PANNELLO || !verificaUtente_(email, p.password)) return ContentService.createTextOutput("UNAUTHORIZED");
  var testo = String(p.config || "{}");
  var pezzi = [];
  for (var i = 0; i < testo.length; i += PEZZO) pezzi.push(testo.substring(i, i + PEZZO));
  var sh = foglioConfig_();
  sh.clear();
  sh.getRange(1, 1, 1, 2).setValues([["Aggiornato il", new Date()]]);
  if (pezzi.length) sh.getRange(2, 1, pezzi.length, 1).setValues(pezzi.map(function (x) { return [x]; }));
  return ContentService.createTextOutput("SUCCESS");
}

function leggiConfig_() {
  var sh = foglioConfig_();
  var ultima = sh.getLastRow();
  if (ultima < 2) return ContentService.createTextOutput("{}");
  var valori = sh.getRange(2, 1, ultima - 1, 1).getValues();
  return ContentService.createTextOutput(valori.map(function (r) { return String(r[0]); }).join("") || "{}");
}
