from http.server import BaseHTTPRequestHandler
import json, io
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
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

C_DARK    = colors.HexColor('#111111')
C_HDR     = colors.HexColor('#1a1a1a')
C_GOLD    = colors.HexColor('#b8860b')
C_GREEN   = colors.HexColor('#2e7d32')
C_RED     = colors.HexColor('#c62828')
C_WHITE   = colors.white
C_GRAY    = colors.HexColor('#F7F7F7')
C_BLUE    = colors.HexColor('#1565c0')
C_ORANGE  = colors.HexColor('#C05621')
C_MUTED   = colors.HexColor('#718096')
C_AMBER   = colors.HexColor('#b8860b')

def P(text, font='Helvetica', size=10, color=colors.black, align='LEFT'):
    a = {'LEFT': TA_LEFT, 'CENTER': TA_CENTER, 'RIGHT': TA_RIGHT}
    s = ParagraphStyle('p', fontName=font, fontSize=size,
        textColor=color, alignment=a.get(align, TA_LEFT), leading=size + 3)
    return Paragraph(str(text) if text is not None else '', s)

def title_p(text):
    s = ParagraphStyle('t', fontName='Helvetica-Bold', fontSize=13,
        textColor=C_DARK, alignment=TA_CENTER, spaceAfter=3)
    return Paragraph(text, s)

def sub_p(text):
    s = ParagraphStyle('s', fontName='Helvetica', fontSize=8,
        textColor=C_MUTED, alignment=TA_CENTER, spaceAfter=5)
    return Paragraph(text, s)

def base_style():
    return [
        ('BACKGROUND',   (0, 0), (-1,  0), C_HDR),
        ('VALIGN',       (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID',         (0, 0), (-1, -1), 0.4, colors.HexColor('#dddddd')),
        ('ROWHEIGHT',    (0, 0), ( 0,  0), 22),
        ('TOPPADDING',   (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING',(0, 0), (-1, -1), 5),
        ('LEFTPADDING',  (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]

# ═══════════════════════════════════════════════════════════════
# KURS TARIXI PDF — A4 portrait
# ═══════════════════════════════════════════════════════════════
def build_kurs_tarix(sarlavha, davr, sana, kunlar):
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4,
        leftMargin=15*mm, rightMargin=15*mm, topMargin=12*mm, bottomMargin=12*mm)
    story = []
    W_total = A4[0] - 30*mm

    story.append(title_p(sarlavha))
    story.append(sub_p("Davr: " + davr))
    story.append(sub_p("Chiqarildi: " + sana))
    story.append(Spacer(1, 6*mm))

    for kun in kunlar:
        # Kun sarlavhasi
        hdr_tbl = Table([[
            P(kun['sana'], 'Helvetica-Bold', 11, C_DARK),
            P(kun['soat'] + " da kiritilgan", 'Helvetica', 8, C_MUTED, 'RIGHT'),
            P(str(kun['kurs']) + " $/g", 'Helvetica-Bold', 11, C_GOLD, 'RIGHT'),
        ]], colWidths=[W_total*0.35, W_total*0.35, W_total*0.30])
        hdr_tbl.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F8F4E8')),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
            ('LINEBELOW', (0,0), (-1,-1), 1, C_GOLD),
        ]))
        story.append(hdr_tbl)

        # Turlar jadvali
        turlar = kun.get('turlar', [])
        if turlar:
            tdata = [[
                P("Zavod", 'Helvetica-Bold', 8, C_WHITE, 'LEFT'),
                P("Tur", 'Helvetica-Bold', 8, C_WHITE, 'LEFT'),
                P("Narx", 'Helvetica-Bold', 8, C_WHITE, 'RIGHT'),
            ]]
            rstyles = [
                ('BACKGROUND', (0,0), (-1,0), C_HDR),
            ]
            cur_zavod = ''
            for ri, t in enumerate(turlar, 1):
                zavod = t.get('zavod','')
                tur = t.get('tur','')
                narx = t.get('narx', 0)
                bg = C_GRAY if ri % 2 == 0 else C_WHITE
                tdata.append([
                    P(zavod if zavod != cur_zavod else '', 'Helvetica-Bold' if zavod != cur_zavod else 'Helvetica', 9, C_AMBER if zavod != cur_zavod else C_MUTED),
                    P('  ' + tur, size=9, color=C_DARK),
                    P(str(narx) + " $", 'Helvetica-Bold', 9, C_GREEN, 'RIGHT'),
                ])
                rstyles.append(('BACKGROUND', (0,ri), (-1,ri), bg))
                cur_zavod = zavod

            t_tbl = Table(tdata, colWidths=[W_total*0.35, W_total*0.40, W_total*0.25])
            t_tbl.setStyle(TableStyle(base_style() + rstyles))
            story.append(t_tbl)

        story.append(Spacer(1, 5*mm))

    story.append(sub_p(f"Jami: {len(kunlar)} ta kurs yozuvi"))

    doc.build(story)
    return buf.getvalue()


def build_pdf(zavodlar, filter_zavod, dan, gacha, label):
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=landscape(A4),
        leftMargin=8*mm, rightMargin=8*mm, topMargin=8*mm, bottomMargin=8*mm)
    story = []
    HDR = ["Sana","Zavod","Tur","+/-","Kimga","Kirim(g)","Naqt($)","Kurs","Naqt→g","Lom(g)","Lom($)","Chiqim(g)","Ostatka(g)"]
    CW  = [x*mm for x in [24, 26, 16, 9, 26, 22, 24, 16, 20, 20, 24, 22, 24]]
    hdr_row = [P(h, 'Helvetica-Bold', 9, C_WHITE, 'CENTER') for h in HDR]
    all_rows = []
    for z in zavodlar:
        if filter_zavod and z["nom"] != filter_zavod: continue
        for t in z.get("turlar", []):
            bal = 0.0
            for op in t.get("tarix", []):
                if op["tip"] == "mol":      bal += op.get("gramm", 0)
                elif op["tip"] == "vozvrat": bal  = max(0, bal - op.get("gramm", 0))
                else:                        bal  = max(0, bal - (op.get("jami") or 0))
                if not in_davr(op["sana"], dan, gacha): continue
                all_rows.append({"sana": op["sana"], "zavod": z["nom"], "tur": t["nom"],
                    "tip": op["tip"], "op": op, "ostatka": round(bal, 2)})
    all_rows.sort(key=lambda r: parse_d(r["sana"]))
    tdata = [hdr_row]; rstyles = []
    for ri, row in enumerate(all_rows, 1):
        op = row["op"]; is_k = row["tip"] == "mol"; is_v = row["tip"] == "vozvrat"
        def cell(v, bold=False, color=colors.HexColor('#212121'), align='LEFT'):
            return P(v, 'Helvetica-Bold' if bold else 'Helvetica', 9, color, align)
        trow = [
            cell(row["sana"]), cell(row["zavod"]), cell(row["tur"]),
            P("↓" if is_k else ("↩" if is_v else "↑"), 'Helvetica-Bold', 11,
              C_GREEN if is_k else (C_BLUE if is_v else C_RED), 'CENTER'),
            cell("" if is_k else (op.get("kimga") or "")),
            cell(f"+{op.get('gramm',0):,.2f}" if is_k else (f"-{op.get('gramm',0):,.2f}" if is_v else ""),
                 bold=True, color=C_GREEN if is_k else C_BLUE, align='RIGHT'),
            cell(f"{op.get('naqtSumma',0):,.0f}" if not is_k else "", align='RIGHT'),
            cell(str(op.get("naqtKurs","")) if not is_k else "", align='RIGHT'),
            cell(f"{op.get('naqtGramm',0):,.2f}" if not is_k else "", align='RIGHT'),
            cell(f"{op.get('lomGramm',0):,.2f}" if not is_k else "", align='RIGHT'),
            cell(f"{op.get('lomPul',0):,.0f}" if not is_k else "", align='RIGHT'),
            cell(f"{op.get('jami',0):,.2f}" if not is_k else "", bold=True, color=C_RED, align='RIGHT'),
            P(f"{row['ostatka']:,.2f}", 'Helvetica-Bold', 9, C_AMBER, 'RIGHT'),
        ]
        tdata.append(trow)
        rstyles.append(('BACKGROUND', (0, ri), (-1, ri), C_WHITE if ri % 2 else C_GRAY))
    tK = round(sum(r["op"].get("gramm", 0) for r in all_rows if r["tip"] == "mol"), 2)
    tC = round(sum(r["op"].get("jami", 0) for r in all_rows if r["tip"] == "tolov"), 2)
    tN = round(sum(r["op"].get("naqtSumma", 0) for r in all_rows if r["tip"] == "tolov"), 2)
    tL = round(sum(r["op"].get("lomPul", 0) for r in all_rows if r["tip"] == "tolov"), 2)
    fin = {}
    for r in all_rows: fin[r["zavod"] + "|" + r["tur"]] = r["ostatka"]
    tO = round(sum(fin.values()), 2)
    jr = len(tdata)
    tdata.append([
        P('JAMI', 'Helvetica-Bold', 9, C_WHITE, 'CENTER'), '', '', '', '',
        P(f'+{tK:,.2f}g', 'Helvetica-Bold', 9, colors.HexColor('#68D391'), 'RIGHT'),
        P(f'Naqt: {tN:,.0f}$', 'Helvetica-Bold', 9, colors.HexColor('#F6E05E'), 'RIGHT'),
        '', '', '', P(f'Lom: {tL:,.0f}$', 'Helvetica-Bold', 9, colors.HexColor('#F6E05E'), 'RIGHT'),
        P(f'-{tC:,.2f}g', 'Helvetica-Bold', 9, colors.HexColor('#FC8181'), 'RIGHT'),
        P(f'{tO:,.2f}g', 'Helvetica-Bold', 10, colors.HexColor('#F6E05E'), 'RIGHT'),
    ])
    rstyles += [('BACKGROUND', (0, jr), (-1, jr), C_DARK), ('SPAN', (0, jr), (4, jr))]
    t1 = Table(tdata, colWidths=CW, repeatRows=1)
    t1.setStyle(TableStyle(base_style() + rstyles))
    story.append(title_p("TILLA HISOB — Kirdi-Chiqdi" + (" — " + filter_zavod if filter_zavod else " (Barcha)")))
    story.append(sub_p("Davr: " + label)); story.append(t1); story.append(Spacer(1, 8*mm))
    H2 = ["Zavod", "Tur", "Kirim(g)", "Chiqim(g)", "Ostatka(g)", "Naqt($)", "Lom($)", "Jami($)"]
    H2CW = [x*mm for x in [35, 25, 30, 30, 30, 36, 36, 36]]
    h2data = [[P(h, 'Helvetica-Bold', 9, C_WHITE, 'CENTER') for h in H2]]; h2styles = []
    gK = gC = gO = gN = gL = 0; ri2 = 1
    for z in zavodlar:
        if filter_zavod and z["nom"] != filter_zavod: continue
        for t in z.get("turlar", []):
            tk = tc = tn = tl = bal = 0
            for op in t.get("tarix", []):
                if op["tip"] == "mol":      bal += op.get("gramm", 0)
                elif op["tip"] == "vozvrat": bal = max(0, bal - op.get("gramm", 0))
                else:                        bal = max(0, bal - (op.get("jami") or 0))
                if not in_davr(op["sana"], dan, gacha): continue
                if op["tip"] == "mol": tk += op.get("gramm", 0)
                else: tc += op.get("jami", 0); tn += op.get("naqtSumma", 0); tl += op.get("lomPul", 0)
            o = round(bal, 2); bg = C_GRAY if ri2 % 2 == 0 else C_WHITE
            h2data.append([P(z["nom"], size=9), P(t["nom"], size=9),
                P(f'{tk:,.2f}', 'Helvetica-Bold', 9, C_GREEN, 'RIGHT'),
                P(f'{tc:,.2f}', 'Helvetica-Bold', 9, C_RED, 'RIGHT'),
                P(f'{o:,.2f}', 'Helvetica-Bold', 10, C_GOLD, 'RIGHT'),
                P(f'{tn:,.2f}', size=9, color=C_ORANGE, align='RIGHT'),
                P(f'{tl:,.2f}', size=9, color=C_ORANGE, align='RIGHT'),
                P(f'{(tn+tl):,.2f}', size=9, color=C_ORANGE, align='RIGHT')])
            h2styles.append(('BACKGROUND', (0, ri2), (-1, ri2), bg))
            gK += tk; gC += tc; gO += o; gN += tn; gL += tl; ri2 += 1
    jr2 = len(h2data)
    h2data.append([P('JAMI', 'Helvetica-Bold', 9, C_WHITE, 'CENTER'), '',
        P(f'{gK:,.2f}', 'Helvetica-Bold', 9, colors.HexColor('#68D391'), 'RIGHT'),
        P(f'{gC:,.2f}', 'Helvetica-Bold', 9, colors.HexColor('#FC8181'), 'RIGHT'),
        P(f'{gO:,.2f}', 'Helvetica-Bold', 9, colors.HexColor('#F6E05E'), 'RIGHT'),
        P(f'{gN:,.2f}', 'Helvetica-Bold', 9, colors.HexColor('#FBD38D'), 'RIGHT'),
        P(f'{gL:,.2f}', 'Helvetica-Bold', 9, colors.HexColor('#FBD38D'), 'RIGHT'),
        P(f'{(gN+gL):,.2f}', 'Helvetica-Bold', 9, colors.HexColor('#FBD38D'), 'RIGHT')])
    h2styles += [('BACKGROUND', (0, jr2), (-1, jr2), C_DARK), ('SPAN', (0, jr2), (1, jr2))]
    ht = Table(h2data, colWidths=H2CW, repeatRows=1)
    ht.setStyle(TableStyle(base_style() + h2styles))
    story.append(title_p("HISOBOT — Tur bo'yicha kirdi-chiqdi"))
    story.append(sub_p("Davr: " + label)); story.append(ht)
    doc.build(story); return buf.getvalue()


def build_klient_chek(klient_nom, ops_grouped, sana, qarz_tarkib=None):
    buf = io.BytesIO(); W = 72*mm
    est_h = 35 + len(ops_grouped)*28 + (len(qarz_tarkib)*6 if qarz_tarkib else 0) + 18
    def CP(text, font='Helvetica', size=8, color=colors.black, align='CENTER'):
        a = {'LEFT': TA_LEFT, 'CENTER': TA_CENTER, 'RIGHT': TA_RIGHT}
        s = ParagraphStyle('cp', fontName=font, fontSize=size, textColor=color, alignment=a.get(align, TA_CENTER), leading=size+2)
        return Paragraph(str(text) if text else '', s)
    def row(a, b, fa='Helvetica', fb='Helvetica', sa=8, sb=8, ca=C_MUTED, cb=colors.black):
        return Table([[CP(a,fa,sa,ca,'LEFT'), CP(b,fb,sb,cb,'RIGHT')]], colWidths=[W*0.55-3*mm, W*0.45-3*mm],
            style=[('TOPPADDING',(0,0),(-1,-1),1),('BOTTOMPADDING',(0,0),(-1,-1),1)])
    def dline():
        return Table([['']], colWidths=[W-6*mm], style=[('LINEBELOW',(0,0),(-1,-1),0.5,C_MUTED),
            ('TOPPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),2)])
    story = []
    story.append(CP('TILLA HISOB', 'Helvetica-Bold', 11, C_GOLD))
    story.append(CP('TOLOV CHEKI', size=8, color=C_MUTED))
    story.append(Spacer(1, 2*mm)); story.append(dline()); story.append(Spacer(1, 1*mm))
    story.append(row('Klient:', klient_nom, fb='Helvetica-Bold', cb=C_DARK))
    story.append(row('Sana:', sana, cb=C_DARK))
    story.append(Spacer(1, 1*mm)); story.append(dline()); story.append(Spacer(1, 1*mm))
    total_pul = total_tolov_g = total_vozvrat_g = total_qolgan = 0
    for item in ops_grouped:
        tur_nom = (item.get('zavod','') + ' · ' + item.get('tur','')) if item.get('tur') else item.get('zavod','')
        avvalgi=item.get('avvalgi_qarz',0); tolov_g=item.get('tolov_g',0)
        vozvrat_g=item.get('vozvrat_g',0); tolov_summa=item.get('tolov_summa',0)
        tolov_kurs=item.get('tolov_kurs',0); qolgan=max(0,avvalgi-tolov_g-vozvrat_g)
        story.append(CP(tur_nom,'Helvetica-Bold',8,C_DARK,'LEFT'))
        if avvalgi>0: story.append(row('  Qarz:',f'-{avvalgi:.2f}g',cb=C_RED))
        if tolov_g>0 and tolov_summa>0:
            story.append(row(f'  Tolov: {tolov_summa:,.0f}$/{tolov_kurs:.1f}$/g',f'+{tolov_g:.2f}g',cb=C_GREEN))
        elif tolov_g>0: story.append(row('  Tolov:',f'+{tolov_g:.2f}g',cb=C_GREEN))
        if vozvrat_g>0: story.append(row('  Vozvrat:',f'+{vozvrat_g:.2f}g',cb=C_GREEN))
        story.append(row('  Qoldi:',f'-{qolgan:.2f}g',fb='Helvetica-Bold',cb=C_GOLD))
        story.append(Spacer(1,1*mm))
        total_pul+=tolov_summa; total_tolov_g+=tolov_g; total_vozvrat_g+=vozvrat_g; total_qolgan+=qolgan
    story.append(dline()); story.append(Spacer(1,1*mm))
    if qarz_tarkib:
        story.append(CP('QARZ TARKIBI','Helvetica-Bold',7,C_MUTED,'CENTER'))
        story.append(Spacer(1,1*mm))
        for item in qarz_tarkib:
            nom=(item.get('zavod','')+' · '+item.get('tur','')); qarz=item.get('qarz',0)
            if qarz>0: story.append(row(nom,f'-{qarz:.2f}g',cb=C_RED))
        story.append(dline()); story.append(Spacer(1,1*mm))
    if total_pul>0: story.append(row('Jami pul:',f'{total_pul:,.0f}$',fb='Helvetica-Bold',cb=C_BLUE))
    story.append(row('Jami tolov:',f'+{total_tolov_g:.2f}g',fb='Helvetica-Bold',cb=C_GREEN))
    if total_vozvrat_g>0: story.append(row('Jami vozvrat:',f'+{total_vozvrat_g:.2f}g',fb='Helvetica-Bold',cb=C_GREEN))
    story.append(row('Umumiy qolgan:',f'-{total_qolgan:.2f}g',fb='Helvetica-Bold',cb=C_RED))
    story.append(Spacer(1,2*mm)); story.append(dline())
    story.append(CP('— Rahmat —',size=7,color=C_MUTED))
    doc = SimpleDocTemplate(buf, pagesize=(W, est_h*mm), leftMargin=3*mm, rightMargin=3*mm, topMargin=4*mm, bottomMargin=4*mm)
    doc.build(story); buf.seek(0); return buf.read()


def build_klient_qarz_chek(klient_nom, sana, jami_qarz, qarz_tarkib, biz_qarz=0):
    buf = io.BytesIO(); W = 72*mm; est_h = 50 + len(qarz_tarkib)*15 + 38
    def CP(text, font='Helvetica', size=8, color=colors.black, align='CENTER'):
        a = {'LEFT': TA_LEFT, 'CENTER': TA_CENTER, 'RIGHT': TA_RIGHT}
        s = ParagraphStyle('cp', fontName=font, fontSize=size, textColor=color, alignment=a.get(align, TA_CENTER), leading=size+2)
        return Paragraph(str(text) if text else '', s)
    def row2(a, b, fa='Helvetica', fb='Helvetica', sa=8, sb=8, ca=C_MUTED, cb=colors.black):
        return Table([[CP(a,fa,sa,ca,'LEFT'), CP(b,fb,sb,cb,'RIGHT')]], colWidths=[W*0.55-3*mm, W*0.45-3*mm],
            style=[('TOPPADDING',(0,0),(-1,-1),1),('BOTTOMPADDING',(0,0),(-1,-1),1)])
    def dline2():
        return Table([['']], colWidths=[W-6*mm], style=[('LINEBELOW',(0,0),(-1,-1),0.5,C_MUTED),
            ('TOPPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),2)])
    story = []
    story.append(CP('TILLA HISOB', 'Helvetica-Bold', 11, C_GOLD))
    story.append(CP('QARZ HOLATI', size=8, color=C_MUTED))
    story.append(Spacer(1, 2*mm)); story.append(dline2())
    story.append(row2('Klient:', klient_nom, fb='Helvetica-Bold', cb=C_DARK))
    story.append(row2('Sana:', sana, cb=C_DARK))
    story.append(Spacer(1, 1*mm)); story.append(dline2()); story.append(Spacer(1, 1*mm))
    by_zavod = {}
    for item in qarz_tarkib:
        z = item.get('zavod', '')
        if z not in by_zavod: by_zavod[z] = []
        by_zavod[z].append(item)
    # v172.12: biz qarzdor bo'lgan turlar avval BUTUNLAY tashlab yuborilardi
    # (qarz < 0.01 -> continue), lekin z_total ga qo'shilardi. Endi ular
    # "(biz qarz)" bo'lib ko'rinadi, zavod jamisi esa faqat klient qarzidan.
    for znom, turs in by_zavod.items():
        z_total = sum(t.get('qarz', 0) for t in turs if t.get('qarz', 0) > 0)
        story.append(CP(znom, 'Helvetica-Bold', 9, C_GOLD, 'LEFT'))
        for t in turs:
            q = t.get('qarz', 0)
            if q > 0.01:
                story.append(row2('  ' + t.get('tur',''), f"-{q:.2f}g", cb=C_RED))
            elif q < -0.01:
                story.append(row2('  ' + t.get('tur','') + ' (biz qarz)', f"+{abs(q):.2f}g", cb=C_GREEN))
        story.append(row2('  Jami:', f'-{z_total:.2f}g', fb='Helvetica-Bold', cb=C_RED))
        story.append(Spacer(1, 1*mm))
    story.append(dline2()); story.append(Spacer(1, 1*mm))
    # v172.12: "UMUMIY QARZ" o'rniga ikkita qator — klient ostatkasi va bizning
    # qarz alohida. Sof qoldiq YOZILMAYDI. Bizning qarz 0 bo'lsa chiqmaydi.
    story.append(Table([[CP('KLIENT OSTATKASI:', 'Helvetica-Bold', 10, C_RED, 'LEFT'),
        CP(f'-{abs(jami_qarz):.2f}g', 'Helvetica-Bold', 12, C_RED, 'RIGHT')]],
        colWidths=[W*0.55-3*mm, W*0.45-3*mm],
        style=[('BACKGROUND',(0,0),(-1,-1),colors.HexColor('#FFF0F0')),
               ('TOPPADDING',(0,0),(-1,-1),3),('BOTTOMPADDING',(0,0),(-1,-1),3)]))
    if abs(biz_qarz) > 0.001:
        story.append(Table([[CP('BIZNING QARZ:', 'Helvetica-Bold', 10, C_GREEN, 'LEFT'),
            CP(f'+{abs(biz_qarz):.2f}g', 'Helvetica-Bold', 12, C_GREEN, 'RIGHT')]],
            colWidths=[W*0.55-3*mm, W*0.45-3*mm],
            style=[('BACKGROUND',(0,0),(-1,-1),colors.HexColor('#F0FFF4')),
                   ('TOPPADDING',(0,0),(-1,-1),3),('BOTTOMPADDING',(0,0),(-1,-1),3)]))
    story.append(Spacer(1, 2*mm)); story.append(dline2())
    story.append(CP('— Tilla Hisob —', size=7, color=C_MUTED))
    doc = SimpleDocTemplate(buf, pagesize=(W, est_h*mm), leftMargin=3*mm, rightMargin=3*mm, topMargin=4*mm, bottomMargin=4*mm)
    doc.build(story); buf.seek(0); return buf.read()


def _ost_blok(b, kw):
    """v172.39: bitta zavod·tur bloki. Ibrohim so'ragan ko'rinish:
    nom (o'rtada) -> boshlang'ich qoldiq -> kunlik amallar (sana+gramm+amal) ->
    har kun oxiridagi qoldiq -> QOLDI. Qora fon YO'Q (Ibrohim: "yoqmadi")."""
    W = [kw * 0.30, kw * 0.36, kw * 0.34]
    d = [[P(f"{b.get('zavod','')} · {b.get('tur','')}", 'Helvetica-Bold', 7.5, C_DARK, 'CENTER'), '', '']]
    st = [('SPAN', (0, 0), (2, 0)),
          ('BACKGROUND', (0, 0), (2, 0), colors.HexColor('#FBF3E0')),
          ('LINEBELOW', (0, 0), (2, 0), 0.9, C_GOLD)]
    d.append([P('boshi', 'Helvetica-Oblique', 6.5, C_MUTED), '',
              P(str(b.get('boshi', '')), 'Helvetica-Bold', 7, C_DARK, 'RIGHT')])
    st.append(('SPAN', (0, 1), (1, 1)))
    st.append(('BACKGROUND', (0, 1), (2, 1), colors.HexColor('#F4F4F4')))
    r = 2
    for kun in (b.get('kunlar') or []):
        amal = kun.get('amallar') or []
        for i, a in enumerate(amal):
            nom = a.get('amal', '')
            c = C_RED if nom == 'berildi' else (C_BLUE if nom == 'vozvrat' else C_GREEN)
            d.append([P(kun.get('sana', '') if i == 0 else '', 'Helvetica', 6.5, C_MUTED),
                      P(str(a.get('g', '')), 'Helvetica-Bold', 7, c, 'RIGHT'),
                      P(' ' + nom, 'Helvetica', 6.5, C_MUTED)])
            r += 1
        d.append(['', '', P(str(kun.get('qoldi', '')), 'Helvetica-Bold', 7, C_DARK, 'RIGHT')])
        st.append(('LINEABOVE', (0, r), (2, r), 0.5, colors.HexColor('#999999')))
        st.append(('BACKGROUND', (0, r), (2, r), colors.HexColor('#FFFDF6')))
        r += 1
    d.append([P('QOLDI', 'Helvetica-Bold', 7, colors.HexColor('#5c4708')), '',
              P(str(b.get('oxiri', '')), 'Helvetica-Bold', 7.5, C_DARK, 'RIGHT')])
    st += [('SPAN', (0, r), (1, r)),
           ('BACKGROUND', (0, r), (2, r), colors.HexColor('#FBF3E0')),
           ('LINEABOVE', (0, r), (2, r), 0.9, C_GOLD)]
    st += [('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#CCCCCC')),
           ('TOPPADDING', (0, 0), (-1, -1), 1.4), ('BOTTOMPADDING', (0, 0), (-1, -1), 1.4),
           ('LEFTPADDING', (0, 0), (-1, -1), 3), ('RIGHTPADDING', (0, 0), (-1, -1), 3),
           ('VALIGN', (0, 0), (-1, -1), 'TOP')]
    t = Table(d, colWidths=W)
    t.setStyle(TableStyle(st))
    return t


def build_klient_tarix(klient_nom, klient_tel, ops, dan, gacha,
                        jami_berildi, jami_vozvrat, jami_tolov_g, jami_tolov_pul, qarz_tarkib,
                        ost_bloklar=None):
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=landscape(A4), leftMargin=8*mm, rightMargin=8*mm, topMargin=8*mm, bottomMargin=8*mm)
    story = []; W_total = landscape(A4)[0] - 16*mm
    tt = Table([[P("TILLA HISOB — Klient hisoboti", 'Helvetica-Bold', 13, C_DARK),
                 P(klient_nom, 'Helvetica-Bold', 12, C_DARK, 'RIGHT')],
                [P(f"Davr: {davr_label(dan, gacha)}", 'Helvetica', 8, C_MUTED),
                 P(klient_tel or '', 'Helvetica', 8, C_MUTED, 'RIGHT')]],
        colWidths=[W_total*0.6, W_total*0.4])
    tt.setStyle(TableStyle([('TOPPADDING',(0,0),(-1,-1),2),('BOTTOMPADDING',(0,0),(-1,-1),2),
        ('LINEBELOW',(0,1),(-1,1),0.5,colors.HexColor('#dddddd'))]))
    story.append(tt); story.append(Spacer(1, 4*mm))
    qolgan = round(jami_berildi - jami_vozvrat - jami_tolov_g, 2)
    stat_data = [[P("JAMI BERILDI",'Helvetica-Bold',8,C_WHITE,'CENTER'),P("VOZVRAT",'Helvetica-Bold',8,C_WHITE,'CENTER'),
                  P("TOLOV (PUL)",'Helvetica-Bold',8,C_WHITE,'CENTER'),P("QOLGAN QARZ",'Helvetica-Bold',8,C_WHITE,'CENTER')],
                 [P(f"-{jami_berildi:,.2f}g",'Helvetica-Bold',13,C_RED,'CENTER'),P(f"+{jami_vozvrat:,.2f}g",'Helvetica-Bold',13,C_GREEN,'CENTER'),
                  P(f"+{jami_tolov_g:,.2f}g\n{jami_tolov_pul:,.0f}$",'Helvetica-Bold',13,C_GREEN,'CENTER'),
                  P(f"-{qolgan:,.2f}g",'Helvetica-Bold',13,C_RED if qolgan>0 else C_GREEN,'CENTER')]]
    st = Table(stat_data, colWidths=[W_total/4]*4)
    st.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),C_HDR),('BACKGROUND',(0,1),(-1,1),colors.HexColor('#F8F6F0')),
        ('GRID',(0,0),(-1,-1),0.4,colors.HexColor('#dddddd')),('TOPPADDING',(0,0),(-1,-1),6),
        ('BOTTOMPADDING',(0,0),(-1,-1),6),('ALIGN',(0,0),(-1,-1),'CENTER'),('VALIGN',(0,0),(-1,-1),'MIDDLE')]))
    story.append(st); story.append(Spacer(1, 5*mm))
    HDR = ["Sana","Amal","Zavod","Tur","Gramm","Summa ($)","Kurs ($/g)","Ostatka"]
    CW  = [x*mm for x in [26, 22, 30, 22, 26, 26, 24, 28]]
    tdata = [[P(h,'Helvetica-Bold',9,C_WHITE,'CENTER') for h in HDR]]; rstyles = []
    for si, row in enumerate(ops):
        tip=row.get('tip',''); ostatka=row.get('ostatka',0)
        if tip=='berish': amal_txt='↑ Berildi'; ac=C_RED; gc=C_RED; gsign=''
        elif tip=='vozvrat': amal_txt='↩ Vozvrat'; ac=C_BLUE; gc=C_GREEN; gsign='+'
        else: amal_txt='$ Tolov'; ac=C_GREEN; gc=C_GREEN; gsign='+'
        oc=C_RED if ostatka<-0.001 else C_GREEN
        bg=C_GRAY if si%2 else C_WHITE
        turlar=row.get('turlar') or []
        r0=len(tdata)
        if turlar:
            for ti, t in enumerate(turlar):
                tg=t.get('gramm',0); tsum=t.get('summa',0); tk=t.get('kurs',0)
                tdata.append([
                    P(row.get('sana','') if ti==0 else '',size=9,color=C_MUTED),
                    P(amal_txt if ti==0 else '','Helvetica-Bold',9,ac,'CENTER'),
                    P(t.get('zavod',''),size=9,color=C_MUTED),
                    P(t.get('tur',''),'Helvetica-Bold',9,C_DARK),
                    P(f"{gsign}{abs(tg):,.2f}g",'Helvetica-Bold',9,gc,'RIGHT'),
                    P(f"{tsum:,.0f}$" if tsum else "—",size=9,align='RIGHT'),
                    P(f"{tk:,.1f}$/g" if tk else "—",size=9,color=C_MUTED,align='RIGHT'),
                    P(f"{ostatka:,.2f}g" if ti==0 else '','Helvetica-Bold',9,oc,'RIGHT')])
        else:
            tg=row.get('gramm',0); tsum=row.get('summa',0); tk=row.get('kurs',0)
            tdata.append([P(row.get('sana',''),size=9,color=C_MUTED),
                P(amal_txt,'Helvetica-Bold',9,ac,'CENTER'),
                P('',size=9,color=C_MUTED),P('',size=9),
                P(f"{gsign}{abs(tg):,.2f}g",'Helvetica-Bold',9,gc,'RIGHT'),
                P(f"{tsum:,.0f}$" if tsum else "—",size=9,align='RIGHT'),
                P(f"{tk:,.1f}$/g" if tk else "—",size=9,color=C_MUTED,align='RIGHT'),
                P(f"{ostatka:,.2f}g",'Helvetica-Bold',9,oc,'RIGHT')])
        r1=len(tdata)-1
        rstyles.append(('BACKGROUND',(0,r0),(-1,r1),bg))
        if r1>r0:
            rstyles.append(('SPAN',(0,r0),(0,r1)))
            rstyles.append(('SPAN',(1,r0),(1,r1)))
            rstyles.append(('SPAN',(7,r0),(7,r1)))
        rstyles.append(('LINEBELOW',(0,r1),(-1,r1),0.4,colors.HexColor('#cccccc')))
    jr=len(tdata)
    tdata.append([P('JAMI','Helvetica-Bold',9,C_WHITE,'CENTER'),'','','',
        P(f"-{jami_berildi:,.2f}g",'Helvetica-Bold',9,colors.HexColor('#E05A5A'),'RIGHT'),
        P(f"{jami_tolov_pul:,.0f}$",'Helvetica-Bold',9,colors.HexColor('#F6E05E'),'RIGHT'),'',
        P(f"-{qolgan:,.2f}g",'Helvetica-Bold',9,colors.HexColor('#E05A5A') if qolgan>0 else colors.HexColor('#68D391'),'RIGHT')])
    rstyles+=[('BACKGROUND',(0,jr),(-1,jr),C_DARK),('SPAN',(0,jr),(3,jr))]
    mt=Table(tdata,colWidths=CW,repeatRows=1); mt.setStyle(TableStyle(base_style()+rstyles)); story.append(mt)
    if qarz_tarkib:
        story.append(Spacer(1,6*mm)); story.append(sub_p("Joriy qarz tarkibi"))
        qd=[]
        for q in qarz_tarkib:
            qv=q.get('qarz',0); col=C_RED if qv>0.001 else (C_GREEN if qv<-0.001 else C_MUTED)
            sign="−" if qv>0 else ("+" if qv<0 else "")
            qd.append([P(q.get('zavod','')+' · '+q.get('tur',''),size=9),P(f"{sign}{abs(qv):,.2f}g",'Helvetica-Bold',9,col,'RIGHT')])
        qt=Table(qd,colWidths=[80*mm,40*mm])
        qt.setStyle(TableStyle([('GRID',(0,0),(-1,-1),0.4,colors.HexColor('#dddddd')),('TOPPADDING',(0,0),(-1,-1),4),
            ('BOTTOMPADDING',(0,0),(-1,-1),4),('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),
            ('ROWBACKGROUNDS',(0,0),(-1,-1),[C_WHITE,C_GRAY])])); story.append(qt)
    # v172.39: ZAVOD·TUR BO'YICHA KUNLIK OSTATKA — yangi bo'lim.
    # Yuqoridagi jadval TEGILMAYDI, bu uning ostiga tushadi.
    ost = ost_bloklar or []
    if ost:
        story.append(Spacer(1, 6*mm))
        story.append(sub_p("Zavod·tur bo'yicha kunlik ostatka"))
        NUS = 5                                   # bir qatorga nechta blok
        kw = (W_total - (NUS - 1) * 3*mm) / NUS
        for i in range(0, len(ost), NUS):
            qism = ost[i:i + NUS]
            hujayra = [_ost_blok(b, kw) for b in qism]
            while len(hujayra) < NUS:
                hujayra.append('')                # oxirgi qator to'lmasa - bo'sh
            qt2 = Table([hujayra], colWidths=[kw]*NUS)
            qt2.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('LEFTPADDING', (0,0), (-1,-1), 0), ('RIGHTPADDING', (0,0), (-1,-1), 3*mm),
                ('TOPPADDING', (0,0), (-1,-1), 0), ('BOTTOMPADDING', (0,0), (-1,-1), 3*mm)]))
            story.append(qt2)
    doc.build(story); return buf.getvalue()


def build_klientlar_tarix(ops, dan, gacha, jami_berildi, jami_vozvrat, jami_tolov_g, jami_tolov_pul, qarz_tarkib):
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=landscape(A4), leftMargin=8*mm, rightMargin=8*mm, topMargin=8*mm, bottomMargin=8*mm)
    story = []; W_total = landscape(A4)[0] - 16*mm
    story.append(title_p("TILLA HISOB — Klientlar tarixi")); story.append(sub_p(f"Davr: {davr_label(dan, gacha)}")); story.append(Spacer(1, 4*mm))
    qolgan = round(jami_berildi - jami_vozvrat - jami_tolov_g, 2)
    stat_data = [[P("JAMI BERILDI",'Helvetica-Bold',8,C_WHITE,'CENTER'),P("VOZVRAT",'Helvetica-Bold',8,C_WHITE,'CENTER'),
                  P("TOLOV (PUL)",'Helvetica-Bold',8,C_WHITE,'CENTER'),P("TOLOV (GRAMM)",'Helvetica-Bold',8,C_WHITE,'CENTER'),P("QOLGAN QARZ",'Helvetica-Bold',8,C_WHITE,'CENTER')],
                 [P(f"-{jami_berildi:,.2f}g",'Helvetica-Bold',12,C_RED,'CENTER'),P(f"+{jami_vozvrat:,.2f}g",'Helvetica-Bold',12,C_GREEN,'CENTER'),
                  P(f"{jami_tolov_pul:,.0f}$",'Helvetica-Bold',12,C_GOLD,'CENTER'),P(f"+{jami_tolov_g:,.2f}g",'Helvetica-Bold',12,C_GREEN,'CENTER'),
                  P(f"-{qolgan:,.2f}g",'Helvetica-Bold',12,C_RED if qolgan>0 else C_GREEN,'CENTER')]]
    st=Table(stat_data,colWidths=[W_total/5]*5)
    st.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),C_HDR),('BACKGROUND',(0,1),(-1,1),colors.HexColor('#F8F6F0')),
        ('GRID',(0,0),(-1,-1),0.4,colors.HexColor('#dddddd')),('TOPPADDING',(0,0),(-1,-1),6),
        ('BOTTOMPADDING',(0,0),(-1,-1),6),('ALIGN',(0,0),(-1,-1),'CENTER'),('VALIGN',(0,0),(-1,-1),'MIDDLE')]))
    story.append(st); story.append(Spacer(1,5*mm))
    HDR=["Sana","Klient","Amal","Zavod","Tur","Gramm","Summa ($)","Kurs ($/g)","Klient ostatka"]
    CW=[x*mm for x in [22,30,20,26,20,22,22,20,24]]
    tdata=[[P(h,'Helvetica-Bold',8,C_WHITE,'CENTER') for h in HDR]]; rstyles=[]
    for ri,row in enumerate(ops,1):
        tip=row.get('tip',''); gramm=row.get('gramm',0); summa=row.get('summa',0); kurs=row.get('kurs',0); ostatka=row.get('ostatka',0)
        if tip=='berish': amal='↑ Berildi'; ac=C_RED; gc=C_RED; gs=f"{abs(gramm):,.2f}g"
        elif tip=='vozvrat': amal='↩ Vozvrat'; ac=C_BLUE; gc=C_GREEN; gs=f"+{abs(gramm):,.2f}g"
        else: amal='$ Tolov'; ac=C_BLUE; gc=C_GREEN; gs=f"+{abs(gramm):,.2f}g"
        oc=C_RED if ostatka<-0.001 else C_GREEN; bg=C_GRAY if ri%2==0 else C_WHITE
        tdata.append([P(row.get('sana',''),size=9,color=C_MUTED),P(row.get('klient_nom',''),'Helvetica-Bold',9),
            P(amal,'Helvetica-Bold',9,ac,'CENTER'),P(row.get('zavod',''),size=9,color=C_MUTED),P(row.get('tur',''),size=9,color=C_MUTED),
            P(gs,'Helvetica-Bold',9,gc,'RIGHT'),P(f"{summa:,.0f}$" if summa else "—",size=9,align='RIGHT'),
            P(f"{kurs:,.1f}$/g" if kurs else "—",size=9,color=C_MUTED,align='RIGHT'),P(f"{ostatka:,.2f}g",'Helvetica-Bold',9,oc,'RIGHT')])
        rstyles.append(('BACKGROUND',(0,ri),(-1,ri),bg))
    jr=len(tdata)
    tdata.append([P('JAMI','Helvetica-Bold',9,C_WHITE,'CENTER'),'','','','',
        P(f"-{jami_berildi:,.2f}g",'Helvetica-Bold',9,colors.HexColor('#E05A5A'),'RIGHT'),
        P(f"{jami_tolov_pul:,.0f}$",'Helvetica-Bold',9,colors.HexColor('#F6E05E'),'RIGHT'),'',
        P(f"-{qolgan:,.2f}g",'Helvetica-Bold',9,colors.HexColor('#E05A5A') if qolgan>0 else colors.HexColor('#68D391'),'RIGHT')])
    rstyles+=[('BACKGROUND',(0,jr),(-1,jr),C_DARK),('SPAN',(0,jr),(4,jr))]
    mt=Table(tdata,colWidths=CW,repeatRows=1); mt.setStyle(TableStyle(base_style()+rstyles)); story.append(mt)
    if qarz_tarkib:
        story.append(Spacer(1,6*mm)); story.append(sub_p("Joriy qarz tarkibi"))
        qd=[]
        for q in qarz_tarkib:
            qv=q.get('qarz',0); col=C_RED if qv>0.001 else (C_GREEN if qv<-0.001 else C_MUTED)
            sign="−" if qv>0 else ("+" if qv<0 else "")
            qd.append([P(q.get('klient_nom',''),size=9),P(f"{sign}{abs(qv):,.2f}g",'Helvetica-Bold',9,col,'RIGHT')])
        qt=Table(qd,colWidths=[60*mm,40*mm])
        qt.setStyle(TableStyle([('GRID',(0,0),(-1,-1),0.4,colors.HexColor('#dddddd')),('TOPPADDING',(0,0),(-1,-1),4),
            ('BOTTOMPADDING',(0,0),(-1,-1),4),('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),
            ('ROWBACKGROUNDS',(0,0),(-1,-1),[C_WHITE,C_GRAY])])); story.append(qt)
    doc.build(story); return buf.getvalue()


def build_kassa(ops, dan, gacha, jami_summa, jami_gramm, label):
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4, leftMargin=15*mm, rightMargin=15*mm, topMargin=12*mm, bottomMargin=12*mm)
    story = []; W_total = A4[0] - 30*mm
    story.append(title_p("TILLA HISOB — Kassa hisoboti")); story.append(sub_p("Davr: " + label)); story.append(Spacer(1, 4*mm))
    stat_data = [[P("JAMI KASSA",'Helvetica-Bold',8,C_WHITE,'CENTER'),P("JAMI GRAMM",'Helvetica-Bold',8,C_WHITE,'CENTER'),P("TOLOVLAR SONI",'Helvetica-Bold',8,C_WHITE,'CENTER')],
                 [P(f"${jami_summa:,.2f}",'Helvetica-Bold',14,C_GOLD,'CENTER'),P(f"{jami_gramm:,.2f}g",'Helvetica-Bold',14,C_GREEN,'CENTER'),P(f"{len(ops)} ta",'Helvetica-Bold',14,C_DARK,'CENTER')]]
    st=Table(stat_data,colWidths=[W_total/3]*3)
    st.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),C_HDR),('BACKGROUND',(0,1),(-1,1),colors.HexColor('#F8F6F0')),
        ('GRID',(0,0),(-1,-1),0.4,colors.HexColor('#dddddd')),('TOPPADDING',(0,0),(-1,-1),6),
        ('BOTTOMPADDING',(0,0),(-1,-1),6),('ALIGN',(0,0),(-1,-1),'CENTER'),('VALIGN',(0,0),(-1,-1),'MIDDLE')]))
    story.append(st); story.append(Spacer(1,6*mm))
    HDR=["Sana","Klient","Zavod","Tur","Gramm (g)","Kurs ($/g)","Summa ($)"]
    CW=[x*mm for x in [24,34,30,22,24,24,28]]
    tdata=[[P(h,'Helvetica-Bold',9,C_WHITE,'CENTER') for h in HDR]]; rstyles=[]
    for ri,op in enumerate(ops,1):
        bg=C_GRAY if ri%2==0 else C_WHITE
        tdata.append([P(op.get('sana',''),size=9,color=C_MUTED),P(op.get('klient',''),'Helvetica-Bold',9),
            P(op.get('zavod',''),size=9,color=C_MUTED),P(op.get('tur',''),size=9,color=C_MUTED),
            P(f"{op.get('gramm',0):,.2f}",size=9,align='RIGHT'),P(f"{op.get('kurs',0):,.1f}",size=9,color=C_MUTED,align='RIGHT'),
            P(f"${op.get('summa',0):,.2f}",'Helvetica-Bold',9,C_GOLD,'RIGHT')])
        rstyles.append(('BACKGROUND',(0,ri),(-1,ri),bg))
    jr=len(tdata)
    tdata.append([P('JAMI','Helvetica-Bold',9,C_WHITE,'CENTER'),'','','',
        P(f"{jami_gramm:,.2f}",'Helvetica-Bold',9,colors.HexColor('#68D391'),'RIGHT'),'',
        P(f"${jami_summa:,.2f}",'Helvetica-Bold',10,colors.HexColor('#F6E05E'),'RIGHT')])
    rstyles+=[('BACKGROUND',(0,jr),(-1,jr),C_DARK),('SPAN',(0,jr),(3,jr))]
    mt=Table(tdata,colWidths=CW,repeatRows=1); mt.setStyle(TableStyle(base_style()+rstyles)); story.append(mt)
    doc.build(story); return buf.getvalue()


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            length = int(self.headers.get("Content-Length", 0))
            body   = json.loads(self.rfile.read(length))
            tip    = body.get("tip", "")

            if tip == "kurs_tarix":
                pdf = build_kurs_tarix(
                    body.get("sarlavha", "KURS TARIXI"),
                    body.get("davr", ""),
                    body.get("sana", ""),
                    body.get("kunlar", []))
                return self._send_pdf(pdf, "kurs-tarix.pdf")

            if tip == "klient_qarz_chek":
                pdf = build_klient_qarz_chek(body.get("klient_nom",""), body.get("sana",""),
                    body.get("jami_qarz",0), body.get("qarz_tarkib",[]),
                    body.get("biz_qarz",0)); return self._send_pdf(pdf, "qarz-chek.pdf")

            if tip == "klient_chek":
                pdf = build_klient_chek(body.get("klient_nom",""), body.get("ops_grouped",[]),
                    body.get("sana",""), body.get("qarz_tarkib")); return self._send_pdf(pdf, "chek.pdf")

            if tip == "klient_tarix":
                pdf = build_klient_tarix(body.get("klient_nom",""), body.get("klient_tel",""),
                    body.get("ops",[]), body.get("dan"), body.get("gacha"),
                    body.get("jami_berildi",0), body.get("jami_vozvrat",0),
                    body.get("jami_tolov_g",0), body.get("jami_tolov_pul",0),
                    body.get("qarz_tarkib",[]),
                    body.get("ost_bloklar",[])); return self._send_pdf(pdf, "klient-hisobot.pdf")

            if tip == "klientlar_tarix":
                pdf = build_klientlar_tarix(body.get("ops",[]), body.get("dan"), body.get("gacha"),
                    body.get("jami_berildi",0), body.get("jami_vozvrat",0),
                    body.get("jami_tolov_g",0), body.get("jami_tolov_pul",0),
                    body.get("qarz_tarkib",[])); return self._send_pdf(pdf, "klientlar-tarix.pdf")

            if tip == "kassa":
                pdf = build_kassa(body.get("ops",[]), body.get("dan"), body.get("gacha"),
                    body.get("jami_summa",0), body.get("jami_gramm",0),
                    body.get("label","Hammasi")); return self._send_pdf(pdf, "kassa.pdf")

            zavodlar=body.get("zavodlar",[]); dan=body.get("dan"); gacha=body.get("gacha")
            filter_zavod=body.get("zavod"); label=davr_label(dan, gacha)
            pdf=build_pdf(zavodlar, filter_zavod, dan, gacha, label)
            self._send_pdf(pdf, "tilla-hisobot.pdf")

        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type","application/json")
            self.send_header("Access-Control-Allow-Origin","*")
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())

    def _send_pdf(self, pdf_bytes, filename):
        self.send_response(200)
        self.send_header("Content-Type","application/pdf")
        self.send_header("Content-Disposition",f"inline; filename={filename}")
        self.send_header("Content-Length",str(len(pdf_bytes)))
        self.send_header("Access-Control-Allow-Origin","*")
        self.end_headers()
        self.wfile.write(pdf_bytes)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin","*")
        self.send_header("Access-Control-Allow-Methods","POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers","Content-Type")
        self.end_headers()

    def log_message(self, format, *args):
        pass
