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
C_GOLD_BG = colors.HexColor('#FEFCE8')
C_GREEN   = colors.HexColor('#276749')
C_GREEN_BG= colors.HexColor('#E6FFED')
C_RED     = colors.HexColor('#9B2335')
C_RED_BG  = colors.HexColor('#FFF0F0')
C_WHITE   = colors.white
C_GRAY    = colors.HexColor('#F7F7F7')
C_BLUE    = colors.HexColor('#2B4AA0')
C_ORANGE  = colors.HexColor('#C05621')
C_MUTED   = colors.HexColor('#718096')

def title_p(text):
    s = ParagraphStyle('t', fontName='Helvetica-Bold', fontSize=12,
        textColor=C_DARK, alignment=TA_CENTER, spaceAfter=4)
    return Paragraph(text, s)

def sub_p(text):
    s = ParagraphStyle('s', fontName='Helvetica', fontSize=8,
        textColor=C_MUTED, alignment=TA_CENTER, spaceAfter=5)
    return Paragraph(text, s)

def brd(color='#CCCCCC'):
    s = colors.HexColor(color)
    return {'top': ('GRID', (0,0), (-1,-1), 0.4, s)}

def build_pdf(zavodlar, filter_zavod, dan, gacha, label):
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=landscape(A4),
        leftMargin=10*mm, rightMargin=10*mm, topMargin=10*mm, bottomMargin=10*mm)
    story = []

    # ── KIRDI-CHIQDI ──────────────────────────────────────────────
    HDR = ["Sana","Zavod","Tur","+/-","Kimga","Kirim(g)","Naqt($)","Kurs","Naqt→g","Lom(g)","Lom($)","Chiqim(g)","Ostatka(g)"]
    CW  = [x*mm for x in [22,22,15,8,24,18,18,14,14,16,18,18,20]]

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

    tdata = [HDR]
    rstyles = []

    for ri, row in enumerate(all_rows, 1):
        op=row["op"]; is_k=row["tip"]=="mol"
        tdata.append([
            row["sana"], row["zavod"], row["tur"],
            "+" if is_k else "-",
            "" if is_k else (op.get("kimga") or ""),
            f"{op['gramm']:.2f}" if is_k else "",
            f"{op.get('naqtSumma',0):,.0f}" if not is_k else "",
            str(op.get("naqtKurs","")) if not is_k else "",
            f"{op.get('naqtGramm',0):.2f}" if not is_k else "",
            f"{op.get('lomGramm',0):.2f}" if not is_k else "",
            f"{op.get('lomPul',0):,.0f}" if not is_k else "",
            f"{op.get('jami',0):.2f}" if not is_k else "",
            f"{row['ostatka']:.2f}"
        ])
        bg = C_GREEN_BG if is_k else C_RED_BG
        rstyles += [('BACKGROUND',(0,ri),(-1,ri),bg)]
        if is_k:
            rstyles += [('TEXTCOLOR',(3,ri),(3,ri),C_GREEN),('FONTNAME',(3,ri),(3,ri),'Helvetica-Bold'),
                        ('TEXTCOLOR',(5,ri),(5,ri),C_GREEN),('FONTNAME',(5,ri),(5,ri),'Helvetica-Bold')]
        else:
            rstyles += [('TEXTCOLOR',(3,ri),(3,ri),C_RED),('FONTNAME',(3,ri),(3,ri),'Helvetica-Bold'),
                        ('TEXTCOLOR',(11,ri),(11,ri),C_RED),('FONTNAME',(11,ri),(11,ri),'Helvetica-Bold')]
        rstyles += [('TEXTCOLOR',(12,ri),(12,ri),C_BLUE),('FONTNAME',(12,ri),(12,ri),'Helvetica-Bold')]

    # JAMI row
    tK=round(sum(r["op"]["gramm"] for r in all_rows if r["tip"]=="mol"),2)
    tC=round(sum(r["op"].get("jami",0) for r in all_rows if r["tip"]=="tolov"),2)
    tN=round(sum(r["op"].get("naqtSumma",0) for r in all_rows if r["tip"]=="tolov"),2)
    tL=round(sum(r["op"].get("lomPul",0) for r in all_rows if r["tip"]=="tolov"),2)
    fin={}
    for r in all_rows: fin[r["zavod"]+"|"+r["tur"]]=r["ostatka"]
    tO=round(sum(fin.values()),2)

    jr=len(tdata)
    tdata.append(["JAMI","","","","",
        f"+{tK:.2f}g", f"Naqt:{tN:,.0f}$","","",
        "",f"Lom:{tL:,.0f}$",
        f"-{tC:.2f}g", f"{tO:.2f}g"])
    rstyles += [
        ('BACKGROUND',(0,jr),(-1,jr),C_DARK),
        ('TEXTCOLOR',(0,jr),(-1,jr),C_WHITE),
        ('FONTNAME',(0,jr),(-1,jr),'Helvetica-Bold'),
        ('TEXTCOLOR',(5,jr),(5,jr),colors.HexColor('#68D391')),
        ('TEXTCOLOR',(11,jr),(11,jr),colors.HexColor('#FC8181')),
        ('TEXTCOLOR',(12,jr),(12,jr),colors.HexColor('#F6E05E')),
    ]

    kt = Table(tdata, colWidths=CW, repeatRows=1)
    kt.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0),C_HDR),
        ('TEXTCOLOR',(0,0),(-1,0),C_WHITE),
        ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),
        ('FONTSIZE',(0,0),(-1,0),8),
        ('ALIGN',(0,0),(-1,0),'CENTER'),
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        ('FONTNAME',(0,1),(-1,-2),'Helvetica'),
        ('FONTSIZE',(0,1),(-1,-1),8),
        ('ALIGN',(5,1),(-1,-1),'RIGHT'),
        ('ALIGN',(3,0),(3,-1),'CENTER'),
        ('GRID',(0,0),(-1,-1),0.4,colors.HexColor('#CCCCCC')),
        ('ROWHEIGHT',(0,0),(-1,-1),16),
        ('ROWHEIGHT',(0,0),(0,0),18),
        ('TOPPADDING',(0,0),(-1,-1),3),
        ('BOTTOMPADDING',(0,0),(-1,-1),3),
        ('LEFTPADDING',(0,0),(-1,-1),4),
        ('RIGHTPADDING',(0,0),(-1,-1),4),
    ] + rstyles))

    story.append(title_p("TILLA HISOB — Kirdi-Chiqdi" + (" — " + filter_zavod if filter_zavod else " (Barcha)")))
    story.append(sub_p("Davr: " + label))
    story.append(kt)
    story.append(Spacer(1,8*mm))

    # ── HISOBOT ───────────────────────────────────────────────────
    H2HDR=["Zavod","Tur","Kirim(g)","Chiqim(g)","Ostatka(g)","Naqt($)","Lom($)","Jami($)"]
    H2CW=[x*mm for x in [32,24,28,28,28,34,34,34]]
    h2data=[H2HDR]; h2styles=[]; gK=gC=gO=gN=gL=0; ri2=1

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
            h2data.append([z["nom"],t["nom"],f"{tk:.2f}",f"{tc:.2f}",f"{o:.2f}",
                           f"{tn:,.2f}",f"{tl:,.2f}",f"{(tn+tl):,.2f}"])
            bg=C_GRAY if ri2%2==0 else C_WHITE
            h2styles+=[
                ('BACKGROUND',(0,ri2),(-1,ri2),bg),
                ('TEXTCOLOR',(2,ri2),(2,ri2),C_GREEN),('FONTNAME',(2,ri2),(2,ri2),'Helvetica-Bold'),
                ('TEXTCOLOR',(3,ri2),(3,ri2),C_RED),('FONTNAME',(3,ri2),(3,ri2),'Helvetica-Bold'),
                ('TEXTCOLOR',(4,ri2),(4,ri2),C_GOLD),('FONTNAME',(4,ri2),(4,ri2),'Helvetica-Bold'),
                ('TEXTCOLOR',(5,ri2),(7,ri2),C_ORANGE),
            ]
            gK+=tk;gC+=tc;gO+=o;gN+=tn;gL+=tl;ri2+=1

    jr2=len(h2data)
    h2data.append(["JAMI","",f"{gK:.2f}",f"{gC:.2f}",f"{gO:.2f}",
                   f"{gN:,.2f}",f"{gL:,.2f}",f"{(gN+gL):,.2f}"])
    h2styles+=[
        ('BACKGROUND',(0,jr2),(-1,jr2),C_DARK),
        ('TEXTCOLOR',(0,jr2),(-1,jr2),C_WHITE),
        ('FONTNAME',(0,jr2),(-1,jr2),'Helvetica-Bold'),
        ('TEXTCOLOR',(2,jr2),(2,jr2),colors.HexColor('#68D391')),
        ('TEXTCOLOR',(3,jr2),(3,jr2),colors.HexColor('#FC8181')),
        ('TEXTCOLOR',(4,jr2),(4,jr2),colors.HexColor('#F6E05E')),
    ]

    ht=Table(h2data,colWidths=H2CW,repeatRows=1)
    ht.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0),C_HDR),
        ('TEXTCOLOR',(0,0),(-1,0),C_WHITE),
        ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),
        ('FONTSIZE',(0,0),(-1,0),9),
        ('ALIGN',(0,0),(-1,0),'CENTER'),
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        ('FONTNAME',(0,1),(-1,-2),'Helvetica'),
        ('FONTSIZE',(0,1),(-1,-1),10),
        ('ALIGN',(2,1),(-1,-1),'RIGHT'),
        ('GRID',(0,0),(-1,-1),0.4,colors.HexColor('#CCCCCC')),
        ('ROWHEIGHT',(0,0),(-1,-1),18),
        ('TOPPADDING',(0,0),(-1,-1),4),
        ('BOTTOMPADDING',(0,0),(-1,-1),4),
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
        zavodlar = body.get("zavodlar", [])
        dan = body.get("dan")
        gacha = body.get("gacha")
        filter_zavod = body.get("zavod")
        label = davr_label(dan, gacha)

        pdf_bytes = build_pdf(zavodlar, filter_zavod, dan, gacha, label)

        self.send_response(200)
        self.send_header("Content-Type", "application/pdf")
        self.send_header("Content-Disposition", "attachment; filename=tilla-hisobot.pdf")
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
