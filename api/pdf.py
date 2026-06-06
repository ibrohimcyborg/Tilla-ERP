from http.server import BaseHTTPRequestHandler
import json, io
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from datetime import datetime

def parse_d(s):
    try: return datetime.strptime(s, "%d.%m.%Y")
    except: return datetime.min

def in_davr(sana, dan, gacha):
    if not dan and not gacha: return True
    d = parse_d(sana)
    if dan and d < datetime.strptime(dan, "%Y-%m-%d"): return False
    if gacha and d > datetime.strptime(gacha, "%Y-%m-%d"): return False
    return True

def davr_label(dan, gacha):
    if dan and gacha:
        d1 = ".".join(reversed(dan.split("-")))
        d2 = ".".join(reversed(gacha.split("-")))
        return d1 + " — " + d2
    return "Hammasi"

C_DARK    = colors.HexColor('#2D3748')
C_HDR     = colors.HexColor('#4A5568')
C_GOLD    = colors.HexColor('#B7791F')
C_GREEN   = colors.HexColor('#276749')
C_GREEN_BG= colors.HexColor('#E6FFED')
C_RED     = colors.HexColor('#9B2335')
C_RED_BG  = colors.HexColor('#FFF0F0')
C_WHITE   = colors.white
C_GRAY    = colors.HexColor('#F7F7F7')
C_BLUE    = colors.HexColor('#2B4AA0')
C_ORANGE  = colors.HexColor('#C05621')
C_MUTED   = colors.HexColor('#718096')

def P(text, font='Helvetica', size=10, color=colors.black, align='LEFT'):
    s = ParagraphStyle('p', fontName=font, fontSize=size,
        textColor=color, alignment={'LEFT':0,'CENTER':1,'RIGHT':2}[align],
        leading=10)
    return Paragraph(str(text) if text is not None else '', s)

def title_p(text):
    s = ParagraphStyle('t', fontName='Helvetica-Bold', fontSize=13,
        textColor=C_DARK, alignment=TA_CENTER, spaceAfter=3)
    return Paragraph(text, s)

def sub_p(text):
    s = ParagraphStyle('s', fontName='Helvetica', fontSize=8,
        textColor=C_MUTED, alignment=TA_CENTER, spaceAfter=5)
    return Paragraph(text, s)

def build_pdf(zavodlar, filter_zavod, dan, gacha, label):
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=landscape(A4),
        leftMargin=8*mm, rightMargin=8*mm, topMargin=8*mm, bottomMargin=8*mm)
    story = []

    # ── KIRDI-CHIQDI ──────────────────────────────────────────────
    HDR_LABELS = ["Sana","Zavod","Tur","+/-","Kimga","Kirim(g)","Naqt($)","Kurs","Naqt→g","Lom(g)","Lom($)","Chiqim(g)","Ostatka(g)"]
    # A4 landscape = 297mm - 16mm margins = 281mm total
    CW = [x*mm for x in [24, 26, 16, 9, 26, 22, 24, 16, 20, 20, 24, 22, 24]]
    # total = 246mm, fits well

    # Header row
    hdr_row = [P(h, 'Helvetica-Bold', 9, C_WHITE, 'CENTER') for h in HDR_LABELS]

    all_rows = []
    for z in zavodlar:
        if filter_zavod and z["nom"] != filter_zavod: continue
        for t in z["turlar"]:
            bal = 0.0
            for op in t["tarix"]:
                if op["tip"] == "mol": bal += op["gramm"]
                else: bal = max(0, bal - (op.get("jami") or 0))
                if not in_davr(op["sana"], dan, gacha): continue
                all_rows.append({
                    "sana":op["sana"],"zavod":z["nom"],"tur":t["nom"],
                    "tip":op["tip"],"op":op,"ostatka":round(bal,2)
                })
    all_rows.sort(key=lambda r: parse_d(r["sana"]))

    tdata = [hdr_row]
    rstyles = []

    for ri, row in enumerate(all_rows, 1):
        op = row["op"]; is_k = row["tip"] == "mol"
        bg = C_GREEN_BG if is_k else C_RED_BG

        def cell(v, bold=False, color=colors.HexColor('#212121'), align='LEFT'):
            f = 'Helvetica-Bold' if bold else 'Helvetica'
            return P(v, f, 10, color, align)

        trow = [
            cell(row["sana"]),
            cell(row["zavod"]),
            cell(row["tur"]),
            P("+" if is_k else "−", 'Helvetica-Bold', 12, C_GREEN if is_k else C_RED, 'CENTER'),
            cell("" if is_k else (op.get("kimga") or "")),
            cell(f"{op['gramm']:,.2f}" if is_k else "", bold=True, color=C_GREEN, align='RIGHT'),
            cell(f"{op.get('naqtSumma',0):,.0f}" if not is_k else "", align='RIGHT'),
            cell(str(op.get("naqtKurs","")) if not is_k else "", align='RIGHT'),
            cell(f"{op.get('naqtGramm',0):,.2f}" if not is_k else "", align='RIGHT'),
            cell(f"{op.get('lomGramm',0):,.2f}" if not is_k else "", align='RIGHT'),
            cell(f"{op.get('lomPul',0):,.0f}" if not is_k else "", align='RIGHT'),
            cell(f"{op.get('jami',0):,.2f}" if not is_k else "", bold=True, color=C_RED, align='RIGHT'),
            P(f"{row['ostatka']:,.2f}", 'Helvetica-Bold', 10, C_BLUE, 'RIGHT'),
        ]
        tdata.append(trow)
        rstyles.append(('BACKGROUND',(0,ri),(-1,ri),bg))

    # JAMI
    tK=round(sum(r["op"]["gramm"] for r in all_rows if r["tip"]=="mol"),2)
    tC=round(sum(r["op"].get("jami",0) for r in all_rows if r["tip"]=="tolov"),2)
    tN=round(sum(r["op"].get("naqtSumma",0) for r in all_rows if r["tip"]=="tolov"),2)
    tL=round(sum(r["op"].get("lomPul",0) for r in all_rows if r["tip"]=="tolov"),2)
    fin={}
    for r in all_rows: fin[r["zavod"]+"|"+r["tur"]]=r["ostatka"]
    tO=round(sum(fin.values()),2)

    jr=len(tdata)
    tdata.append([
        P('JAMI','Helvetica-Bold',10,C_WHITE,'CENTER'),'','','','',
        P(f'+{tK:,.2f}g','Helvetica-Bold',10,colors.HexColor('#68D391'),'RIGHT'),
        P(f'Naqt: {tN:,.0f}$','Helvetica-Bold',10,colors.HexColor('#F6E05E'),'RIGHT'),
        '','','',
        P(f'Lom: {tL:,.0f}$','Helvetica-Bold',10,colors.HexColor('#F6E05E'),'RIGHT'),
        P(f'-{tC:,.2f}g','Helvetica-Bold',10,colors.HexColor('#E05A5A'),'RIGHT'),
        P(f'{tO:,.2f}g','Helvetica-Bold',11,colors.HexColor('#F6E05E'),'RIGHT'),
    ])
    rstyles += [
        ('BACKGROUND',(0,jr),(-1,jr),C_DARK),
        ('SPAN',(0,jr),(4,jr)),
    ]

    kt = Table(tdata, colWidths=CW, repeatRows=1)
    kt.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0),C_HDR),
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        ('ALIGN',(3,0),(3,-1),'CENTER'),
        ('GRID',(0,0),(-1,-1),0.4,colors.HexColor('#CCCCCC')),
        ('ROWHEIGHT',(0,0),(0,0),22),
        ('TOPPADDING',(0,0),(-1,-1),5),
        ('BOTTOMPADDING',(0,0),(-1,-1),5),
        ('LEFTPADDING',(0,0),(-1,-1),5),
        ('RIGHTPADDING',(0,0),(-1,-1),5),
    ] + rstyles))

    story.append(title_p("TILLA HISOB — Kirdi-Chiqdi" + (" — " + filter_zavod if filter_zavod else " (Barcha)")))
    story.append(sub_p("Davr: " + label))
    story.append(kt)
    story.append(Spacer(1,8*mm))

    # ── HISOBOT ───────────────────────────────────────────────────
    H2HDR = ["Zavod","Tur","Kirim(g)","Chiqim(g)","Ostatka(g)","Naqt($)","Lom($)","Jami($)"]
    H2CW  = [x*mm for x in [35,25,30,30,30,36,36,36]]

    h2hdr = [P(h,'Helvetica-Bold',9,C_WHITE,'CENTER') for h in H2HDR]
    h2data=[h2hdr]; h2styles=[]; gK=gC=gO=gN=gL=0; ri2=1

    for z in zavodlar:
        if filter_zavod and z["nom"]!=filter_zavod: continue
        for t in z["turlar"]:
            tk=tc=tn=tl=bal=0
            for op in t["tarix"]:
                if op["tip"]=="mol": bal+=op["gramm"]
                else: bal=max(0,bal-(op.get("jami") or 0))
                if not in_davr(op["sana"],dan,gacha): continue
                if op["tip"]=="mol": tk+=op["gramm"]
                else: tc+=op.get("jami",0); tn+=op.get("naqtSumma",0); tl+=op.get("lomPul",0)
            o=round(bal,2)
            bg=C_GRAY if ri2%2==0 else C_WHITE
            h2data.append([
                P(z["nom"],'Helvetica',10,colors.HexColor('#212121')),
                P(t["nom"],'Helvetica',10,colors.HexColor('#212121')),
                P(f'{tk:,.2f}','Helvetica-Bold',10,C_GREEN,'RIGHT'),
                P(f'{tc:,.2f}','Helvetica-Bold',10,C_RED,'RIGHT'),
                P(f'{o:,.2f}','Helvetica-Bold',11,C_GOLD,'RIGHT'),
                P(f'{tn:,.2f}','Helvetica',10,C_ORANGE,'RIGHT'),
                P(f'{tl:,.2f}','Helvetica',10,C_ORANGE,'RIGHT'),
                P(f'{(tn+tl):,.2f}','Helvetica',10,C_ORANGE,'RIGHT'),
            ])
            h2styles.append(('BACKGROUND',(0,ri2),(-1,ri2),bg))
            gK+=tk;gC+=tc;gO+=o;gN+=tn;gL+=tl;ri2+=1

    jr2=len(h2data)
    h2data.append([
        P('JAMI','Helvetica-Bold',10,C_WHITE,'CENTER'),'',
        P(f'{gK:,.2f}','Helvetica-Bold',10,colors.HexColor('#68D391'),'RIGHT'),
        P(f'{gC:,.2f}','Helvetica-Bold',10,colors.HexColor('#FC8181'),'RIGHT'),
        P(f'{gO:,.2f}','Helvetica-Bold',10,colors.HexColor('#F6E05E'),'RIGHT'),
        P(f'{gN:,.2f}','Helvetica-Bold',10,colors.HexColor('#FBD38D'),'RIGHT'),
        P(f'{gL:,.2f}','Helvetica-Bold',10,colors.HexColor('#FBD38D'),'RIGHT'),
        P(f'{(gN+gL):,.2f}','Helvetica-Bold',10,colors.HexColor('#FBD38D'),'RIGHT'),
    ])
    h2styles += [
        ('BACKGROUND',(0,jr2),(-1,jr2),C_DARK),
        ('SPAN',(0,jr2),(1,jr2)),
    ]

    ht=Table(h2data,colWidths=H2CW,repeatRows=1)
    ht.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0),C_HDR),
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        ('ALIGN',(2,0),(-1,0),'CENTER'),
        ('GRID',(0,0),(-1,-1),0.4,colors.HexColor('#CCCCCC')),
        ('ROWHEIGHT',(0,0),(0,0),20),
        ('TOPPADDING',(0,0),(-1,-1),5),
        ('BOTTOMPADDING',(0,0),(-1,-1),5),
        ('LEFTPADDING',(0,0),(-1,-1),5),
        ('RIGHTPADDING',(0,0),(-1,-1),5),
    ]+h2styles))

    story.append(title_p("HISOBOT — Tur bo'yicha kirdi-chiqdi"))
    story.append(sub_p("Davr: " + label))
    story.append(ht)

    doc.build(story)
    return buf.getvalue()

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(length))

        # Klient chek
        if body.get("tip") == "klient_chek":
            pdf_bytes = build_klient_chek(
                body.get("klient_nom", ""),
                body.get("ops_grouped", []),
                body.get("sana", "")
            )
            self.send_response(200)
            self.send_header("Content-Type", "application/pdf")
            self.send_header("Content-Disposition", "inline; filename=chek.pdf")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(pdf_bytes)
            return

        zavodlar = body.get("zavodlar", [])
        dan = body.get("dan")
        gacha = body.get("gacha")
        filter_zavod = body.get("zavod")
        label = davr_label(dan, gacha)

        pdf_bytes = build_pdf(zavodlar, filter_zavod, dan, gacha, label)

        self.send_response(200)
        self.send_header("Content-Type", "application/pdf")
        self.send_header("Content-Disposition", "inline; filename=tilla-hisobot.pdf")
        self.send_header("Content-Length", str(len(pdf_bytes)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(pdf_bytes)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()


def build_klient_chek(klient_nom, ops_grouped, sana):
    """Klient tolov cheki - 80mm thermal printer uchun"""
    buf = io.BytesIO()
    W = 72*mm  # 80mm printer, ~72mm print area
    doc = SimpleDocTemplate(buf, pagesize=(W, 400*mm),
        leftMargin=3*mm, rightMargin=3*mm, topMargin=5*mm, bottomMargin=5*mm)
    story = []

    def CP(text, font='Helvetica', size=9, color=colors.black, align='CENTER'):
        s = ParagraphStyle('cp', fontName=font, fontSize=size,
            textColor=color, alignment={'LEFT':0,'CENTER':1,'RIGHT':2}[align],
            leading=size+2)
        return Paragraph(str(text), s)

    def dline():
        return Table([['- '*30]], colWidths=[W-6*mm],
            style=[('TEXTCOLOR',(0,0),(-1,-1),C_MUTED),('FONTSIZE',(0,0),(-1,-1),7),
                   ('TOPPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),0)])

    # Header
    story.append(CP('⬡  TILLA HISOB', 'Helvetica-Bold', 12, C_GOLD))
    story.append(CP('TOLOV CHEKI', 'Helvetica', 8, C_MUTED))
    story.append(Spacer(1, 3*mm))
    story.append(dline())
    story.append(Spacer(1, 2*mm))

    # Info
    info = [
        [CP('Klient:', size=9, align='LEFT'), CP(klient_nom, 'Helvetica-Bold', 9, C_DARK, 'RIGHT')],
        [CP('Sana:', size=9, align='LEFT'), CP(sana, size=9, align='RIGHT')],
    ]
    story.append(Table(info, colWidths=[W*0.4-3*mm, W*0.6-3*mm],
        style=[('TOPPADDING',(0,0),(-1,-1),1),('BOTTOMPADDING',(0,0),(-1,-1),1)]))
    story.append(Spacer(1, 2*mm))
    story.append(dline())
    story.append(Spacer(1, 2*mm))

    total_pul = 0
    total_tolov_g = 0
    total_vozvrat_g = 0
    total_qolgan = 0

    for item in ops_grouped:
        tur_nom = item.get('zavod','') + ' · ' + item.get('tur','')
        avvalgi = item.get('avvalgi_qarz', 0)
        tolov_g = item.get('tolov_g', 0)
        vozvrat_g = item.get('vozvrat_g', 0)
        tolov_summa = item.get('tolov_summa', 0)
        tolov_kurs = item.get('tolov_kurs', 0)
        qolgan = avvalgi - tolov_g - vozvrat_g

        story.append(CP(tur_nom, 'Helvetica-Bold', 9, C_DARK, 'LEFT'))
        story.append(Spacer(1, 1*mm))

        rows = [
            [CP('Avvalgi qarz:', size=8, align='LEFT'), CP('-'+'{:.2f}'.format(avvalgi)+'g', size=8, color=C_RED, align='RIGHT')],
        ]
        if tolov_g > 0:
            rows.append([CP('Tolov: {:,.0f}$/{}$/g'.format(tolov_summa, tolov_kurs), size=8, align='LEFT'),
                        CP('+{:.2f}g'.format(tolov_g), size=8, color=C_GREEN, align='RIGHT')])
        if vozvrat_g > 0:
            rows.append([CP('Vozvrat:', size=8, align='LEFT'),
                        CP('+{:.2f}g'.format(vozvrat_g), size=8, color=C_GREEN, align='RIGHT')])
        rows.append([CP('Qolgan qarz:', 'Helvetica-Bold', 8, C_GOLD, 'LEFT'),
                    CP('-{:.2f}g'.format(max(0, qolgan)), 'Helvetica-Bold', 8, C_GOLD, 'RIGHT')])

        story.append(Table(rows, colWidths=[W*0.6-3*mm, W*0.4-3*mm],
            style=[('TOPPADDING',(0,0),(-1,-1),1),('BOTTOMPADDING',(0,0),(-1,-1),1),
                   ('LINEBELOW',(0,-1),(-1,-1),0.5,C_MUTED)]))
        story.append(Spacer(1, 2*mm))

        total_pul += tolov_summa
        total_tolov_g += tolov_g
        total_vozvrat_g += vozvrat_g
        total_qolgan += max(0, qolgan)

    story.append(dline())
    story.append(Spacer(1, 2*mm))

    # Jami
    jami_rows = [
        [CP('Jami tolov (pul):', size=9, align='LEFT'), CP('{:,.0f}$'.format(total_pul), 'Helvetica-Bold', 9, C_BLUE, 'RIGHT')],
        [CP('Jami tolov (gramm):', size=9, align='LEFT'), CP('+{:.2f}g'.format(total_tolov_g), 'Helvetica-Bold', 9, C_GREEN, 'RIGHT')],
    ]
    if total_vozvrat_g > 0:
        jami_rows.append([CP('Jami vozvrat:', size=9, align='LEFT'),
                         CP('+{:.2f}g'.format(total_vozvrat_g), 'Helvetica-Bold', 9, C_GREEN, 'RIGHT')])
    jami_rows.append([CP('Umumiy qolgan qarz:', 'Helvetica-Bold', 9, C_RED, 'LEFT'),
                     CP('-{:.2f}g'.format(total_qolgan), 'Helvetica-Bold', 10, C_RED, 'RIGHT')])

    story.append(Table(jami_rows, colWidths=[W*0.55-3*mm, W*0.45-3*mm],
        style=[('TOPPADDING',(0,0),(-1,-1),2),('BOTTOMPADDING',(0,0),(-1,-1),2),
               ('BACKGROUND',(0,-1),(-1,-1),colors.HexColor('#FFF8E7')),
               ('LINEABOVE',(0,-1),(-1,-1),1,C_GOLD)]))

    story.append(Spacer(1, 4*mm))
    story.append(dline())
    story.append(CP('— Rahmat —', size=8, color=C_MUTED))

    doc.build(story)
    buf.seek(0)
    return buf.read()
