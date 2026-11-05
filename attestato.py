# -*- coding: utf-8 -*-
"""
ATTESTATO DI FINE CORSO - Leonardo Scuole
Genera il PDF (A4 orizzontale) che lo studente scarica dall'Area Attestati.
Font: Poppins (lo stesso del sito leonardoscuole.it), file in ./fonts
"""
import hashlib
import io
import os
from datetime import date

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

BORDEAUX = HexColor("#8D021F")   # colore titoli del sito
ORO = HexColor("#D4AF37")
GRIGIO = HexColor("#626262")     # colore testo del sito
GRIGIO_CHIARO = HexColor("#9A9A9A")

_CARTELLA_FONT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts")
_FONT = {"normale": "Helvetica", "medio": "Helvetica", "grassetto": "Helvetica-Bold", "corsivo": "Helvetica-Oblique"}


def _registra_font():
    file_font = {"normale": "Poppins-Regular.ttf", "medio": "Poppins-Medium.ttf",
                 "grassetto": "Poppins-Bold.ttf", "corsivo": "Poppins-Italic.ttf"}
    for chiave, nome in file_font.items():
        percorso = os.path.join(_CARTELLA_FONT, nome)
        nome_font = "LS-" + nome.replace(".ttf", "")
        try:
            if nome_font not in pdfmetrics.getRegisteredFontNames():
                pdfmetrics.registerFont(TTFont(nome_font, percorso))
            _FONT[chiave] = nome_font
        except Exception:
            pass  # resta il font di riserva Helvetica


_registra_font()


def codice_attestato(email, corso, data_fine):
    """Codice univoco e ripetibile (stessi dati -> stesso codice), utile per verificare l'attestato."""
    impronta = hashlib.sha256(f"{email.strip().lower()}|{corso}|{data_fine}".encode("utf-8")).hexdigest()
    return f"LS-RO-{impronta[:4].upper()}-{impronta[4:8].upper()}"


def _a_capo(c, testo, font, dim, larghezza):
    """Divide il testo in righe che stanno nella larghezza data."""
    parole, righe, riga = testo.split(), [], ""
    for p in parole:
        prova = f"{riga} {p}".strip()
        if c.stringWidth(prova, font, dim) <= larghezza:
            riga = prova
        else:
            righe.append(riga)
            riga = p
    if riga:
        righe.append(riga)
    return righe


def genera_attestato(nominativo, email, corso, contenuti, ore, n_moduli, media_quiz,
                     data_inizio, data_fine, logo_bytes=None, firmatario="", ruolo_firmatario="La Direzione",
                     luogo="", ente="Leonardo Scuole"):
    """Restituisce i byte del PDF dell'attestato."""
    buffer = io.BytesIO()
    W, H = landscape(A4)
    c = canvas.Canvas(buffer, pagesize=(W, H))
    codice = codice_attestato(email, corso, data_fine)
    c.setTitle(f"Attestato - {nominativo} - {corso}")
    c.setAuthor(ente)

    # Cornice: doppio bordo bordeaux / oro
    c.setStrokeColor(BORDEAUX); c.setLineWidth(6); c.rect(18, 18, W - 36, H - 36)
    c.setStrokeColor(ORO); c.setLineWidth(1.5); c.rect(30, 30, W - 60, H - 60)

    y = H - 70
    if logo_bytes:
        try:
            img = ImageReader(io.BytesIO(logo_bytes))
            iw, ih = img.getSize()
            lh = 52
            lw = iw * lh / ih
            c.drawImage(img, (W - lw) / 2, y - lh + 10, width=lw, height=lh, mask="auto")
            y -= lh + 8
        except Exception:
            pass
    if not logo_bytes:
        c.setFillColor(BORDEAUX); c.setFont(_FONT["grassetto"], 20)
        c.drawCentredString(W / 2, y - 10, ente.upper())
        y -= 36

    c.setFillColor(BORDEAUX); c.setFont(_FONT["grassetto"], 34)
    c.drawCentredString(W / 2, y - 30, "Attestato di formazione")
    c.setStrokeColor(ORO); c.setLineWidth(2); c.line(W / 2 - 90, y - 42, W / 2 + 90, y - 42)

    c.setFillColor(GRIGIO); c.setFont(_FONT["normale"], 13)
    c.drawCentredString(W / 2, y - 66, "Si attesta che")
    c.setFillColor(HexColor("#1F2326")); c.setFont(_FONT["grassetto"], 28)
    c.drawCentredString(W / 2, y - 100, nominativo.upper())
    c.setFillColor(GRIGIO); c.setFont(_FONT["normale"], 13)
    c.drawCentredString(W / 2, y - 124, "ha frequentato e superato con profitto il")
    c.setFillColor(BORDEAUX); c.setFont(_FONT["grassetto"], 18)
    c.drawCentredString(W / 2, y - 148, corso)

    # Dettagli
    sx, larghezza = 80, W - 160
    yy = y - 186
    righe_dettaglio = [
        ("Natura della formazione:", f"e-learning sulla piattaforma {ente}"),
        ("Contenuti:", contenuti),
        ("Esito:", f"superati tutti i {n_moduli} quiz di modulo con soglia minima dell'80% (media {media_quiz}%)."),
    ]
    for etichetta, valore in righe_dettaglio:
        c.setFont(_FONT["grassetto"], 10.5); c.setFillColor(BORDEAUX)
        c.drawString(sx, yy, etichetta)
        offset = c.stringWidth(etichetta, _FONT["grassetto"], 10.5) + 6
        c.setFont(_FONT["normale"], 10.5); c.setFillColor(GRIGIO)
        righe = _a_capo(c, valore, _FONT["normale"], 10.5, larghezza - offset)
        for i, r in enumerate(righe):
            c.drawString(sx + offset, yy, r)
            yy -= 14
        yy -= 4

    c.setFont(_FONT["medio"], 11); c.setFillColor(GRIGIO)
    c.drawCentredString(W / 2, yy - 6, f"Inizio: {data_inizio}   ·   Fine: {data_fine}   ·   Durata: {ore} ore   ·   Moduli: {n_moduli}")

    # Firma e data
    base = 70
    c.setFont(_FONT["normale"], 10.5); c.setFillColor(GRIGIO)
    luogo_data = f"{luogo + ', ' if luogo else ''}{data_fine}"
    c.drawString(80, base + 22, luogo_data)
    c.setStrokeColor(GRIGIO_CHIARO); c.setLineWidth(0.8); c.line(80, base + 16, 260, base + 16)
    c.setFont(_FONT["corsivo"], 9); c.drawString(80, base + 4, "Luogo e data")

    c.setFont(_FONT["medio"], 10.5)
    if firmatario:
        c.drawCentredString(W - 170, base + 22, firmatario)
    c.line(W - 260, base + 16, W - 80, base + 16)
    c.setFont(_FONT["corsivo"], 9); c.drawCentredString(W - 170, base + 4, ruolo_firmatario)

    c.setFont(_FONT["normale"], 8.5); c.setFillColor(GRIGIO_CHIARO)
    c.drawCentredString(W / 2, 40, f"Codice attestato: {codice}  ·  rilasciato il {date.today().strftime('%d/%m/%Y')}")

    c.showPage()
    c.save()
    return buffer.getvalue(), codice
