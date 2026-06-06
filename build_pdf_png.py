from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from PIL import Image, ImageDraw, ImageFont

# ---- shared content ----
TITLE = "ENGINO STEM CENTRE"
SUBTITLE = "Daily Takings"
LABELS = ["Date", "Gross £", "Card Machine", "Worldpay", "Total card",
          "Expenses", "Red box", "Cash 2 bank", "Till Total"]
BLOCKS = [list(range(1, 12)), list(range(12, 23)), list(range(23, 32))]  # 11,11,9 -> 31
NCOLS = 11  # day columns

# colours
BLUE_HDR  = (0xD9, 0xE1, 0xF2)
BLUE_DATE = (0xBD, 0xD7, 0xEE)
GREY_LBL  = (0xF2, 0xF2, 0xF2)
BLACK = (0, 0, 0)

# ============ PDF (reportlab) ============
def build_pdf(path):
    W, H = landscape(A4)              # 297 x 210 mm in points
    c = canvas.Canvas(path, pagesize=(W, H))
    ml, mr, mt, mb = 8*mm, 8*mm, 8*mm, 8*mm
    usable_w = W - ml - mr

    # title
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(W/2, H - mt - 6*mm, TITLE)
    c.setFont("Helvetica-Bold", 11)
    top = H - mt - 13*mm
    c.drawString(ml, top, f"{SUBTITLE}   —   Month / Year: ______________________")

    # geometry
    label_w = 30*mm
    day_w = (usable_w - label_w) / NCOLS
    grid_top = top - 5*mm
    row_h = 6.0*mm
    nrows = len(LABELS)
    block_gap = 4*mm

    y = grid_top
    for blk in BLOCKS:
        ndays = len(blk)
        for ri, label in enumerate(LABELS):
            ry = y - ri*row_h
            is_date = (ri == 0)
            # label cell fill
            c.setFillColorRGB(*[v/255 for v in (BLUE_DATE if is_date else GREY_LBL)])
            c.rect(ml, ry - row_h, label_w, row_h, stroke=0, fill=1)
            # day cells fill (only header row coloured)
            for di in range(ndays):
                cx = ml + label_w + di*day_w
                if is_date:
                    c.setFillColorRGB(*[v/255 for v in BLUE_HDR])
                    c.rect(cx, ry - row_h, day_w, row_h, stroke=0, fill=1)
            # borders
            c.setStrokeColorRGB(0,0,0); c.setLineWidth(0.7)
            c.rect(ml, ry - row_h, label_w, row_h, stroke=1, fill=0)
            for di in range(ndays):
                cx = ml + label_w + di*day_w
                c.rect(cx, ry - row_h, day_w, row_h, stroke=1, fill=0)
            # text
            c.setFillColorRGB(0,0,0)
            c.setFont("Helvetica-Bold", 9)
            c.drawString(ml + 2*mm, ry - row_h + 2.6*mm, label)
            if is_date:
                c.setFont("Helvetica-Bold", 11)
                for di, d in enumerate(blk):
                    cx = ml + label_w + di*day_w
                    c.drawCentredString(cx + day_w/2, ry - row_h + 2.4*mm, str(d))
        y = y - nrows*row_h - block_gap
    c.showPage(); c.save()
    print("saved", path)

# ============ PNG (Pillow) ============
def build_png(path, scale=4):
    # A4 landscape proportions at ~ 150ppi*scale-ish; use mm->px
    mm_px = 5.0  # px per mm
    W = int(297*mm_px); H = int(210*mm_px)
    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)
    def F(sz, bold=True):
        for name in (["DejaVuSans-Bold.ttf"] if bold else ["DejaVuSans.ttf"]):
            try: return ImageFont.truetype(name, sz)
            except: pass
        return ImageFont.load_default()
    def mmx(v): return int(v*mm_px)
    ml=mmx(8); mr=mmx(8); mt=mmx(8)
    usable_w = W - ml - mr
    # title
    ft=F(int(7*mm_px)); 
    tw=d.textlength(TITLE, font=ft); d.text(((W-tw)/2, mt), TITLE, fill=BLACK, font=ft)
    fs=F(int(4*mm_px)); 
    d.text((ml, mt+mmx(9)), f"{SUBTITLE}   —   Month / Year: ______________________", fill=BLACK, font=fs)
    label_w=mmx(30); day_w=(usable_w-label_w)/NCOLS
    row_h=mmx(6); grid_top=mt+mmx(15)
    flab=F(int(3.3*mm_px)); fday=F(int(4*mm_px))
    y=grid_top
    for blk in BLOCKS:
        ndays=len(blk)
        for ri,label in enumerate(LABELS):
            ry=y+ri*row_h; is_date=(ri==0)
            d.rectangle([ml,ry,ml+label_w,ry+row_h], fill=(BLUE_DATE if is_date else GREY_LBL))
            for di in range(ndays):
                cx=ml+label_w+di*day_w
                if is_date:
                    d.rectangle([cx,ry,cx+day_w,ry+row_h], fill=BLUE_HDR)
            d.rectangle([ml,ry,ml+label_w,ry+row_h], outline=BLACK, width=2)
            for di in range(ndays):
                cx=ml+label_w+di*day_w
                d.rectangle([cx,ry,cx+day_w,ry+row_h], outline=BLACK, width=2)
            d.text((ml+mmx(2), ry+row_h*0.28), label, fill=BLACK, font=flab)
            if is_date:
                for di,dd in enumerate(blk):
                    cx=ml+label_w+di*day_w
                    tw=d.textlength(str(dd),font=fday)
                    d.text((cx+day_w/2-tw/2, ry+row_h*0.20), str(dd), fill=BLACK, font=fday)
        y=y+len(LABELS)*row_h+mmx(4)
    img.save(path, dpi=(300,300))
    print("saved", path)

build_pdf("/home/user/claude-skills/output/ENGINO_STEM_CENTRE_daily_takings_blank.pdf")
build_png("/home/user/claude-skills/output/ENGINO_STEM_CENTRE_daily_takings_blank.png")
