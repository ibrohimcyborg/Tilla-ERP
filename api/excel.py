from http.server import BaseHTTPRequestHandler
import json, io, base64
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from collections import defaultdict

W="FFFFFF"; DARK="1F2937"; GBG="F0FFF4"; RBG="FFF5F5"
GR="2D6A4F"; RD="C0392B"; GD="B7791F"; MT="6B7280"

def st(cell, bold=False, color=DARK, bg=None, align="left", size=10, italic=False):
    cell.font = Font(name="Arial", bold=bold, color=color, size=size, italic=italic)
    if bg: cell.fill = PatternFill("solid", start_color=bg)
    cell.alignment = Alignment(horizontal=align, vertical="center")
    cell.border = Border(bottom=Side(style="thin", color="E5E7EB"))

def fmt_g(g):
    n = round(float(g), 2)
    return n

def make_kc_sheet(ws, zavodlar, filter_zavod, dan, gacha, davr_label):
    from datetime import datetime
    def parse_d(s):
        try: return datetime.strptime(s, "%d.%m.%Y")
        except: return datetime.min
    def in_davr(sana):
        if not dan and not gacha: return True
        d = parse_d(sana)
        if dan and d < datetime.strptime(dan, "%Y-%m-%d"): return False
        if gacha and d > datetime.strptime(gacha, "%Y-%m-%d"): return False
        return True

    HDR = ["Sana","Zavod","Tur","+/-","Kimga","Kirim(g)","Naqt($)","Kurs($/g)","Naqt→g","Lom(g)","LomKurs","Lom($)","Chiqim(g)","Ostatka(g)"]
    WCOL = [12,14,10,5,14,11,11,10,10,10,10,11,12,12]

    ws.merge_cells("A1:N1")
    ws["A1"] = "TILLA HISOB — Kirdi-Chiqdi" + (f" — {filter_zavod}" if filter_zavod else " (Barcha zavodlar)")
    st(ws["A1"], bold=True, color=W, bg=DARK, align="center", size=12)
    ws.row_dimensions[1].height = 28

    ws.merge_cells("A2:N2")
    ws["A2"] = f"Davr: {davr_label}"
    st(ws["A2"], color=MT, bg="F9FAFB", align="center", size=9, italic=True)
    ws.row_dimensions[2].height = 16
    ws.row_dimensions[3].height = 4

    for ci, (h, w) in enumerate(zip(HDR, WCOL), 1):
        c = ws.cell(row=4, column=ci, value=h)
        st(c, bold=True, color=W, bg="374151", align="center", size=9)
        ws.column_dimensions[get_column_letter(ci)].width = w
    ws.row_dimensions[4].height = 20

    all_rows = []
    for z in zavodlar:
        if filter_zavod and z["nom"] != filter_zavod: continue
        for t in z["turlar"]:
            bal = 0.0
            for op in t["tarix"]:
                if op["tip"] == "mol": bal += op["gramm"]
                else: bal = max(0, bal - (op.get("jami") or 0))
                if not in_davr(op["sana"]): continue
                all_rows.append({"sana":op["sana"],"zavod":z["nom"],"tur":t["nom"],"tip":op["tip"],"op":op,"ostatka":round(bal,2)})

    all_rows.sort(key=lambda r: parse_d(r["sana"]))

    ri = 5
    for row in all_rows:
        op = row["op"]; is_k = row["tip"] == "mol"
        bg = GBG if is_k else RBG
        vals = [
            row["sana"], row["zavod"], row["tur"],
            "+" if is_k else "-",
            "" if is_k else (op.get("kimga") or ""),
            fmt_g(op["gramm"]) if is_k else "",
            op.get("naqtSumma") or "" if not is_k else "",
            op.get("naqtKurs") or "" if not is_k else "",
            fmt_g(op.get("naqtGramm") or 0) or "" if not is_k else "",
            fmt_g(op.get("lomGramm") or 0) or "" if not is_k else "",
            op.get("lomKurs") or "" if not is_k else "",
            fmt_g(op.get("lomPul") or 0) or "" if not is_k else "",
            fmt_g(op.get("jami") or 0) or "" if not is_k else "",
            row["ostatka"]
        ]
        for ci, v in enumerate(vals, 1):
            c = ws.cell(row=ri, column=ci, value=v if v != "" else None)
            if ci == 4: st(c, bold=True, color=GR if is_k else RD, bg=bg, align="center", size=11)
            elif ci == 6 and is_k: st(c, bold=True, color=GR, bg=bg, align="right")
            elif ci == 13 and not is_k: st(c, bold=True, color=RD, bg=bg, align="right")
            elif ci == 14: st(c, bold=True, color=DARK, bg=bg, align="right")
            elif ci in [7,8,9,10,11,12]: st(c, color="374151", bg=bg, align="right")
            else: st(c, color="374151", bg=bg, align="left" if ci<=5 else "right")
        ws.row_dimensions[ri].height = 17
        ri += 1

    # Summary
    ri += 1
    tK = round(sum(r["op"]["gramm"] for r in all_rows if r["tip"]=="mol"), 2)
    tC = round(sum(r["op"].get("jami",0) for r in all_rows if r["tip"]=="tolov"), 2)
    tN = round(sum(r["op"].get("naqtSumma",0) for r in all_rows if r["tip"]=="tolov"), 2)
    tL = round(sum(r["op"].get("lomPul",0) for r in all_rows if r["tip"]=="tolov"), 2)
    fin = {}
    for r in all_rows: fin[r["zavod"]+"|"+r["tur"]] = r["ostatka"]
    tO = round(sum(fin.values()), 2)

    ws.merge_cells(f"A{ri}:E{ri}")
    ws[f"A{ri}"] = "JAMI"
    st(ws[f"A{ri}"], bold=True, color=W, bg=DARK, align="center", size=10)
    pairs = [("Kirim:", f"+{tK:.2f}g", "5AB87A"), ("Chiqim:", f"-{tC:.2f}g", "E05A5A"),
             ("Naqt:", f"{tN:,.2f}$", GD), ("Lom:", f"{tL:,.2f}$", GD)]
    col = 6
    for lbl, val, clr in pairs:
        c = ws.cell(row=ri, column=col, value=lbl); st(c, color=MT, bg=DARK, align="right", size=9)
        c = ws.cell(row=ri, column=col+1, value=val); st(c, bold=True, color=clr, bg=DARK, align="left", size=10)
        col += 2
    ws.row_dimensions[ri].height = 24

    ri += 1
    ws.merge_cells(f"A{ri}:K{ri}")
    ws[f"A{ri}"] = "Oxirgi ostatka (barcha turlar):"
    st(ws[f"A{ri}"], color=MT, bg="FEF9ED", align="right", size=10, italic=True)
    ws.merge_cells(f"L{ri}:N{ri}")
    ws[f"L{ri}"] = f"{tO:.2f} g"
    st(ws[f"L{ri}"], bold=True, color="C9A84C", bg="FEF9ED", align="center", size=14)
    ws.row_dimensions[ri].height = 28
    ws.freeze_panes = "A5"

def make_hisobot_sheet(ws, zavodlar, filter_zavod, dan, gacha, davr_label):
    from datetime import datetime
    def parse_d(s):
        try: return datetime.strptime(s, "%d.%m.%Y")
        except: return datetime.min
    def in_davr(sana):
        if not dan and not gacha: return True
        d = parse_d(sana)
        if dan and d < datetime.strptime(dan, "%Y-%m-%d"): return False
        if gacha and d > datetime.strptime(gacha, "%Y-%m-%d"): return False
        return True

    ws.merge_cells("A1:H1")
    ws["A1"] = "HISOBOT — Tur bo'yicha kirdi-chiqdi"
    st(ws["A1"], bold=True, color=W, bg=DARK, align="center", size=12)
    ws.row_dimensions[1].height = 28

    ws.merge_cells("A2:H2")
    ws["A2"] = f"Davr: {davr_label}"
    st(ws["A2"], color=MT, bg="F9FAFB", align="center", size=9, italic=True)
    ws.row_dimensions[2].height = 16
    ws.row_dimensions[3].height = 4

    hdrs = ["Zavod","Tur","Kirim(g)","Chiqim(g)","Ostatka(g)","Naqt($)","Lom($)","Jami pul($)"]
    wcols = [14,12,12,12,12,13,13,13]
    for ci, (h, w) in enumerate(zip(hdrs, wcols), 1):
        c = ws.cell(row=4, column=ci, value=h)
        st(c, bold=True, color=W, bg="374151", align="center", size=9)
        ws.column_dimensions[get_column_letter(ci)].width = w
    ws.row_dimensions[4].height = 20

    ri = 5
    gK=gC=gO=gN=gL = 0
    for z in zavodlar:
        if filter_zavod and z["nom"] != filter_zavod: continue
        for t in z["turlar"]:
            tk=tc=tn=tl=bal = 0
            for op in t["tarix"]:
                if op["tip"]=="mol": bal+=op["gramm"]
                else: bal=max(0,bal-(op.get("jami") or 0))
                if not in_davr(op["sana"]): continue
                if op["tip"]=="mol": tk+=op["gramm"]
                else: tc+=op.get("jami",0); tn+=op.get("naqtSumma",0); tl+=op.get("lomPul",0)
            o = round(bal, 2)
            bg = "F9FAFB" if ri%2==0 else W
            vals = [z["nom"],t["nom"],round(tk,2),round(tc,2),o,round(tn,2),round(tl,2),round(tn+tl,2)]
            for ci, v in enumerate(vals, 1):
                c = ws.cell(row=ri, column=ci, value=v)
                if ci==3: st(c, color=GR, bg=bg, align="right")
                elif ci==4: st(c, color=RD, bg=bg, align="right")
                elif ci==5: st(c, bold=True, color="C9A84C", bg=bg, align="right")
                elif ci in [6,7,8]: st(c, color=GD, bg=bg, align="right")
                else: st(c, color=DARK, bg=bg, align="left")
            ws.row_dimensions[ri].height = 18
            ri+=1
            gK+=tk; gC+=tc; gO+=o; gN+=tn; gL+=tl

    ri += 1
    ws.merge_cells(f"A{ri}:B{ri}")
    ws[f"A{ri}"] = "JAMI"
    st(ws[f"A{ri}"], bold=True, color=W, bg=DARK, align="center", size=10)
    for ci, (v, clr) in enumerate([(None,None),(None,None),(round(gK,2),GR),(round(gC,2),RD),(round(gO,2),"C9A84C"),(round(gN,2),GD),(round(gL,2),GD),(round(gN+gL,2),GD)], 1):
        if v is None: continue
        c = ws.cell(row=ri, column=ci, value=v)
        st(c, bold=True, color=clr, bg=DARK, align="right", size=10)
    ws.row_dimensions[ri].height = 24
    ws.freeze_panes = "A5"

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(length))

        zavodlar = body.get("zavodlar", [])
        dan = body.get("dan")
        gacha = body.get("gacha")
        filter_zavod = body.get("zavod")

        if dan and gacha:
            d1 = ".".join(reversed(dan.split("-")))
            d2 = ".".join(reversed(gacha.split("-")))
            davr_label = f"{d1} — {d2}"
        else:
            davr_label = "Hammasi"

        wb = Workbook()

        if filter_zavod:
            ws1 = wb.active; ws1.title = filter_zavod[:30]
            make_kc_sheet(ws1, zavodlar, filter_zavod, dan, gacha, davr_label)
            ws2 = wb.create_sheet("Hisobot")
            make_hisobot_sheet(ws2, zavodlar, filter_zavod, dan, gacha, davr_label)
        else:
            ws1 = wb.active; ws1.title = "Umumiy"
            make_kc_sheet(ws1, zavodlar, None, dan, gacha, davr_label)
            for z in zavodlar:
                wsz = wb.create_sheet(z["nom"][:30])
                make_kc_sheet(wsz, zavodlar, z["nom"], dan, gacha, davr_label)
            wsh = wb.create_sheet("Hisobot")
            make_hisobot_sheet(wsh, zavodlar, None, dan, gacha, davr_label)

        buf = io.BytesIO()
        wb.save(buf)
        xlsx_bytes = buf.getvalue()

        self.send_response(200)
        self.send_header("Content-Type", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        self.send_header("Content-Disposition", "attachment; filename=tilla-hisobot.xlsx")
        self.send_header("Content-Length", str(len(xlsx_bytes)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(xlsx_bytes)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
