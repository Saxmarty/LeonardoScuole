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
 *
 *    (mettile DOPO il controllo del token, come le altre azioni).
 * 4. Distribuisci > Gestisci distribuzioni > modifica > Nuova versione.
 *
 * Il foglio "Progressi" viene creato da solo al primo salvataggio.
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
