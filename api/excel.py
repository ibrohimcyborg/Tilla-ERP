from http.server import BaseHTTPRequestHandler
import json, io
import xlsxwriter
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
        return d1 + " - " + d2
    return "Hammasi"

def make_kc_sheet(wb, ws, zavodlar, filter_zavod, dan, gacha, label):
    # Formats
    f_title  = wb.add_format({'bg_color':'#1F2937','font_color':'#FFFFFF','bold':True,'font_size':13,'align':'center','valign':'vcenter'})
    f_sub    = wb.add_format({'bg_color':'#F5F5F5','font_color':'#757575','italic':True,'font_size':9,'align':'center','valign':'vcenter'})
    f_hdr    = wb.add_format({'bg_color':'#374151','font_color':'#FFFFFF','bold':True,'font_size':8,'align':'center','valign':'vcenter','border':1,'border_color':'#555555'})
    f_k_txt  = wb.add_format({'bg_color':'#E8F5E9','font_color':'#212121','font_size':8,'valign':'vcenter','border':1,'border_color':'#DDDDDD'})
    f_k_r    = wb.add_format({'bg_color':'#E8F5E9','font_color':'#212121','font_size':8,'valign':'vcenter','align':'right','border':1,'border_color':'#DDDDDD'})
    f_k_plus = wb.add_format({'bg_color':'#E8F5E9','font_color':'#1B5E20','bold':True,'font_size':11,'align':'center','valign':'vcenter','border':1,'border_color':'#DDDDDD'})
    f_k_g    = wb.add_format({'bg_color':'#E8F5E9','font_color':'#1B5E20','bold':True,'font_size':8,'align':'right','valign':'vcenter','border':1,'border_color':'#DDDDDD'})
    f_c_txt  = wb.add_format({'bg_color':'#FFEBEE','font_color':'#212121','font_size':8,'valign':'vcenter','border':1,'border_color':'#DDDDDD'})
    f_c_r    = wb.add_format({'bg_color':'#FFEBEE','font_color':'#212121','font_size':8,'valign':'vcenter','align':'right','border':1,'border_color':'#DDDDDD'})
    f_c_minus= wb.add_format({'bg_color':'#FFEBEE','font_color':'#B71C1C','bold':True,'font_size':11,'align':'center','valign':'vcenter','border':1,'border_color':'#DDDDDD'})
    f_c_chiq = wb.add_format({'bg_color':'#FFEBEE','font_color':'#B71C1C','bold':True,'font_size':8,'align':'right','valign':'vcenter','border':1,'border_color':'#DDDDDD'})
    f_ostatka= wb.add_format({'bg_color':'#FFEBEE','font_color':'#1A237E','bold':True,'font_size':8,'align':'right','valign':'vcenter','border':1,'border_color':'#DDDDDD'})
    f_ostatka_k= wb.add_format({'bg_color':'#E8F5E9','font_color':'#1A237E','bold':True,'font_size':8,'align':'right','valign':'vcenter','border':1,'border_color':'#DDDDDD'})
    f_jami   = wb.add_format({'bg_color':'#1F2937','font_color':'#FFFFFF','bold':True,'font_size':9,'valign':'vcenter','border':1,'border_color':'#333333'})
    f_jami_g = wb.add_format({'bg_color':'#1F2937','font_color':'#5AB87A','bold':True,'font_size':9,'align':'right','valign':'vcenter','border':1,'border_color':'#333333'})
    f_jami_r = wb.add_format({'bg_color':'#1F2937','font_color':'#E05A5A','bold':True,'font_size':9,'align':'right','valign':'vcenter','border':1,'border_color':'#333333'})
    f_jami_o = wb.add_format({'bg_color':'#1F2937','font_color':'#F6E05E','bold':True,'font_size':9,'align':'right','valign':'vcenter','border':1,'border_color':'#333333'})
    f_ostatka_final = wb.add_format({'bg_color':'#FEF9ED','font_color':'#C9A84C','bold':True,'font_size':14,'align':'center','valign':'vcenter'})
    f_ostatka_lbl   = wb.add_format({'bg_color':'#FEF9ED','font_color':'#757575','italic':True,'font_size':10,'align':'right','valign':'vcenter'})

    HDR = ["Sana","Zavod","Tur","+/-","Kimga","Kirim(g)","Naqt($)","Kurs($/g)","Naqt->g","Lom(g)","LomKurs","Lom($)","Chiqim(g)","Ostatka(g)"]
    WCOL = [13,14,10,5,14,11,11,10,10,10,10,13,12,12]

    # Title
    ws.merge_range(0, 0, 0, 13, "TILLA HISOB - Kirdi-Chiqdi" + (" - " + filter_zavod if filter_zavod else " (Barcha)"), f_title)
    ws.set_row(0, 28)
    ws.merge_range(1, 0, 1, 13, "Davr: " + label, f_sub)
    ws.set_row(1, 16)
    ws.set_row(2, 4)

    # Headers
    for ci, (h, w) in enumerate(zip(HDR, WCOL)):
        ws.write(3, ci, h, f_hdr)
        ws.set_column(ci, ci, w)
    ws.set_row(3, 20)

    # Data
    all_rows = []
    for z in zavodlar:
        if filter_zavod and z["nom"] != filter_zavod: continue
        for t in z["turlar"]:
            bal = 0.0
            for op in t["tarix"]:
                if op["tip"] == "mol": bal += op["gramm"]
                else: bal = max(0, bal - (op.get("jami") or 0))
                if not in_davr(op["sana"], dan, gacha): continue
                all_rows.append({"sana":op["sana"],"zavod":z["nom"],"tur":t["nom"],"tip":op["tip"],"op":op,"ostatka":round(bal,2)})
    all_rows.sort(key=lambda r: parse_d(r["sana"]))

    ri = 4
    for row in all_rows:
        op = row["op"]; is_k = row["tip"] == "mol"
        ft = f_k_txt if is_k else f_c_txt
        fr = f_k_r   if is_k else f_c_r
        ws.set_row(ri, 17)
        ws.write(ri, 0, row["sana"],  ft)
        ws.write(ri, 1, row["zavod"], ft)
        ws.write(ri, 2, row["tur"],   ft)
        ws.write(ri, 3, "+" if is_k else "-", f_k_plus if is_k else f_c_minus)
        ws.write(ri, 4, "" if is_k else (op.get("kimga") or ""), ft)
        if is_k:
            ws.write(ri, 5, round(op["gramm"],2), f_k_g)
            for c in [6,7,8,9,10,11,12]: ws.write(ri, c, "", ft)
            ws.write(ri, 13, row["ostatka"], f_ostatka_k)
        else:
            ws.write(ri, 5, "", ft)
            ws.write(ri, 6,  op.get("naqtSumma") or "", fr)
            ws.write(ri, 7,  op.get("naqtKurs")  or "", fr)
            ws.write(ri, 8,  round(op.get("naqtGramm",0),2) or "", fr)
            ws.write(ri, 9,  round(op.get("lomGramm",0),2)  or "", fr)
            ws.write(ri, 10, op.get("lomKurs")   or "", fr)
            ws.write(ri, 11, round(op.get("lomPul",0),2)    or "", fr)
            ws.write(ri, 12, round(op.get("jami",0),2),  f_c_chiq)
            ws.write(ri, 13, row["ostatka"], f_ostatka)
        ri += 1

    # Summary
    tK = round(sum(r["op"]["gramm"] for r in all_rows if r["tip"]=="mol"),2)
    tC = round(sum(r["op"].get("jami",0) for r in all_rows if r["tip"]=="tolov"),2)
    tN = round(sum(r["op"].get("naqtSumma",0) for r in all_rows if r["tip"]=="tolov"),2)
    tL = round(sum(r["op"].get("lomPul",0) for r in all_rows if r["tip"]=="tolov"),2)
    fin = {}
    for r in all_rows: fin[r["zavod"]+"|"+r["tur"]] = r["ostatka"]
    tO = round(sum(fin.values()),2)

    ri += 1
    ws.set_row(ri, 22)
    ws.merge_range(ri, 0, ri, 4, "JAMI", f_jami)
    ws.write(ri, 5,  f"+{tK:.2f}g", f_jami_g)
    ws.write(ri, 6,  f"Naqt: {tN:,.0f}$", f_jami_o)
    for c in [7,8,9,10]: ws.write(ri, c, "", f_jami)
    ws.write(ri, 11, f"Lom: {tL:,.0f}$", f_jami_o)
    ws.write(ri, 12, f"-{tC:.2f}g", f_jami_r)
    ws.write(ri, 13, f"{tO:.2f}g", f_jami_o)

    ri += 1
    ws.set_row(ri, 28)
    ws.merge_range(ri, 0, ri, 10, "Oxirgi ostatka:", f_ostatka_lbl)
    ws.merge_range(ri, 11, ri, 13, f"{tO:.2f} g", f_ostatka_final)

    ws.freeze_panes(4, 0)

def make_hisobot_sheet(wb, ws, zavodlar, filter_zavod, dan, gacha, label):
    f_title = wb.add_format({'bg_color':'#1F2937','font_color':'#FFFFFF','bold':True,'font_size':13,'align':'center','valign':'vcenter'})
    f_sub   = wb.add_format({'bg_color':'#F5F5F5','font_color':'#757575','italic':True,'font_size':9,'align':'center','valign':'vcenter'})
    f_hdr   = wb.add_format({'bg_color':'#374151','font_color':'#FFFFFF','bold':True,'font_size':9,'align':'center','valign':'vcenter','border':1,'border_color':'#555555'})
    f_even  = wb.add_format({'bg_color':'#FAFAFA','font_color':'#212121','font_size':10,'valign':'vcenter','border':1,'border_color':'#E0E0E0'})
    f_odd   = wb.add_format({'bg_color':'#FFFFFF','font_color':'#212121','font_size':10,'valign':'vcenter','border':1,'border_color':'#E0E0E0'})
    f_e_r   = wb.add_format({'bg_color':'#FAFAFA','font_color':'#212121','font_size':10,'valign':'vcenter','align':'right','border':1,'border_color':'#E0E0E0'})
    f_o_r   = wb.add_format({'bg_color':'#FFFFFF','font_color':'#212121','font_size':10,'valign':'vcenter','align':'right','border':1,'border_color':'#E0E0E0'})
    f_jami  = wb.add_format({'bg_color':'#1F2937','font_color':'#FFFFFF','bold':True,'font_size':10,'valign':'vcenter','border':1,'border_color':'#333333'})
    f_jami_r= wb.add_format({'bg_color':'#1F2937','font_color':'#FFFFFF','bold':True,'font_size':10,'valign':'vcenter','align':'right','border':1,'border_color':'#333333'})

    def green_f(bg): return wb.add_format({'bg_color':bg,'font_color':'#1B5E20','bold':True,'font_size':10,'align':'right','valign':'vcenter','border':1,'border_color':'#E0E0E0'})
    def red_f(bg):   return wb.add_format({'bg_color':bg,'font_color':'#B71C1C','bold':True,'font_size':10,'align':'right','valign':'vcenter','border':1,'border_color':'#E0E0E0'})
    def gold_f(bg):  return wb.add_format({'bg_color':bg,'font_color':'#C9A84C','bold':True,'font_size':11,'align':'right','valign':'vcenter','border':1,'border_color':'#E0E0E0'})
    def ora_f(bg):   return wb.add_format({'bg_color':bg,'font_color':'#C05621','font_size':10,'align':'right','valign':'vcenter','border':1,'border_color':'#E0E0E0'})

    HDR = ["Zavod","Tur","Kirim(g)","Chiqim(g)","Ostatka(g)","Naqt($)","Lom($)","Jami pul($)"]
    WCOL = [16,12,13,13,14,16,16,16]

    ws.merge_range(0,0,0,7,"HISOBOT - Tur boyicha kirdi-chiqdi",f_title)
    ws.set_row(0,28)
    ws.merge_range(1,0,1,7,"Davr: "+label,f_sub)
    ws.set_row(1,16)
    ws.set_row(2,4)
    for ci,(h,w) in enumerate(zip(HDR,WCOL)):
        ws.write(3,ci,h,f_hdr); ws.set_column(ci,ci,w)
    ws.set_row(3,20)

    ri=4; gK=gC=gO=gN=gL=0; idx=0
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
            bg = "#FAFAFA" if idx%2==0 else "#FFFFFF"
            ft = f_even if idx%2==0 else f_odd
            fr = f_e_r  if idx%2==0 else f_o_r
            ws.write(ri,0,z["nom"],ft); ws.write(ri,1,t["nom"],ft)
            ws.write(ri,2,round(tk,2),green_f(bg))
            ws.write(ri,3,round(tc,2),red_f(bg))
            ws.write(ri,4,o,gold_f(bg))
            ws.write(ri,5,round(tn,2),ora_f(bg))
            ws.write(ri,6,round(tl,2),ora_f(bg))
            ws.write(ri,7,round(tn+tl,2),ora_f(bg))
            ws.set_row(ri,18); ri+=1; idx+=1
            gK+=tk;gC+=tc;gO+=o;gN+=tn;gL+=tl

    ri+=1; ws.set_row(ri,22)
    ws.merge_range(ri,0,ri,1,"JAMI",f_jami)
    f_jg=wb.add_format({'bg_color':'#1F2937','font_color':'#68D391','bold':True,'font_size':10,'align':'right','valign':'vcenter','border':1,'border_color':'#333333'})
    f_jr=wb.add_format({'bg_color':'#1F2937','font_color':'#FC8181','bold':True,'font_size':10,'align':'right','valign':'vcenter','border':1,'border_color':'#333333'})
    f_jgo=wb.add_format({'bg_color':'#1F2937','font_color':'#F6E05E','bold':True,'font_size':10,'align':'right','valign':'vcenter','border':1,'border_color':'#333333'})
    f_jo=wb.add_format({'bg_color':'#1F2937','font_color':'#FBD38D','bold':True,'font_size':10,'align':'right','valign':'vcenter','border':1,'border_color':'#333333'})
    ws.write(ri,2,round(gK,2),f_jg); ws.write(ri,3,round(gC,2),f_jr)
    ws.write(ri,4,round(gO,2),f_jgo); ws.write(ri,5,round(gN,2),f_jo)
    ws.write(ri,6,round(gL,2),f_jo); ws.write(ri,7,round(gN+gL,2),f_jo)
    ws.freeze_panes(4,0)

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get("Content-Length",0))
        body = json.loads(self.rfile.read(length))
        zavodlar = body.get("zavodlar",[])
        dan = body.get("dan")
        gacha = body.get("gacha")
        filter_zavod = body.get("zavod")
        label = davr_label(dan, gacha)

        buf = io.BytesIO()
        wb = xlsxwriter.Workbook(buf, {'in_memory': True})

        if filter_zavod:
            ws1 = wb.add_worksheet(filter_zavod[:30])
            make_kc_sheet(wb, ws1, zavodlar, filter_zavod, dan, gacha, label)
            ws2 = wb.add_worksheet("Hisobot")
            make_hisobot_sheet(wb, ws2, zavodlar, filter_zavod, dan, gacha, label)
        else:
            ws1 = wb.add_worksheet("Umumiy")
            make_kc_sheet(wb, ws1, zavodlar, None, dan, gacha, label)
            for z in zavodlar:
                wsz = wb.add_worksheet(z["nom"][:30])
                make_kc_sheet(wb, wsz, zavodlar, z["nom"], dan, gacha, label)
            wsh = wb.add_worksheet("Hisobot")
            make_hisobot_sheet(wb, wsh, zavodlar, None, dan, gacha, label)

        wb.close()
        xlsx_bytes = buf.getvalue()

        self.send_response(200)
        self.send_header("Content-Type","application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        self.send_header("Content-Disposition","attachment; filename=tilla-hisobot.xlsx")
        self.send_header("Content-Length",str(len(xlsx_bytes)))
        self.send_header("Access-Control-Allow-Origin","*")
        self.end_headers()
        self.wfile.write(xlsx_bytes)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin","*")
        self.send_header("Access-Control-Allow-Methods","POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers","Content-Type")
        self.end_headers()
