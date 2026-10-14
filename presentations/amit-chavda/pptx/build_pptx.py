"""Builds Amit_Chavda_x_Extol.pptx from the shared storyline (../storyline.md). Run: python3 build_pptx.py"""
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR
from pptx.util import Emu, Pt

# Extol brand tokens (extolaffiliates/website DESIGN.md §04); names kept from the first draft
DEEP = RGBColor(0x1D, 0x2A, 0x1B)    # forest: ink on oat
PINE = RGBColor(0x0C, 0x1A, 0x11)    # field top: dark slides and cards
FOREST = RGBColor(0x1B, 0x3A, 0x22)  # field mid: cards on dark
MOSS = RGBColor(0x55, 0x70, 0x3A)    # fern: accent and muted text on light
SAGE = RGBColor(0xC6, 0xDE, 0x93)    # moss: accent on dark
CREAM = RGBColor(0xED, 0xE9, 0xDC)   # oat: page
PAPER = RGBColor(0xE4, 0xDF, 0xCE)   # oat 2: cards
BONE = RGBColor(0xEA, 0xE7, 0xDA)    # ink on dark
DESIGN = Path(__file__).resolve().parent.parent / "design"
DISPLAY, TEXT, MONO = "Poppins", "Open Sans", "IBM Plex Mono"
FOOT = "Extol Affiliates · Prepared for Amit Chavda · DigitalClinic.ai · Proposal"

prs = Presentation()
prs.slide_width, prs.slide_height = Emu(12192000), Emu(6858000)  # 16:9
W, H = prs.slide_width, prs.slide_height
IN = 914400
M = int(0.55 * IN)  # side margin


def x(i):
    return int(i * IN)


def text(slide, left, top, width, height, runs, size=14, color=DEEP, font=TEXT, bold=False, anchor=MSO_ANCHOR.TOP):
    """runs: str or list of paragraphs; each paragraph str or list of (text, bold) tuples."""
    tb = slide.shapes.add_textbox(left, top, width, height)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    paras = [runs] if isinstance(runs, str) else runs
    for i, para in enumerate(paras):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_after = Pt(4)
        for t, b in ([(para, bold)] if isinstance(para, str) else para):
            r = p.add_run()
            r.text = t
            r.font.size, r.font.name, r.font.bold = Pt(size), font, b
            r.font.color.rgb = color
    return tb


def box(slide, left, top, width, height, fill, line=None, dash=False):
    s = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
    s.fill.solid()
    s.fill.fore_color.rgb = fill
    if line:
        s.line.color.rgb = line
        s.line.width = Pt(1.5)
        if dash:
            from pptx.enum.dml import MSO_LINE
            s.line.dash_style = MSO_LINE.DASH
    else:
        s.line.fill.background()
    s.shadow.inherit = False
    return s


def new_slide(page, kicker, title, dark=False, notes=None):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    s.background.fill.solid()
    s.background.fill.fore_color.rgb = PINE if dark else CREAM
    fg, sub = (BONE, SAGE) if dark else (DEEP, MOSS)
    text(s, M, x(0.4), x(8), x(0.3), kicker.upper(), 11, sub, MONO, True)
    s.shapes.add_picture(str(DESIGN / ("extol-mark-on-dark.png" if dark else "extol-mark-on-light.png")), W - M - x(0.45), x(0.3), height=x(0.4))
    if title:
        text(s, M, x(0.75), W - 2 * M, x(1.2), title, 28, fg, DISPLAY, True)
    text(s, M, H - x(0.45), x(9), x(0.3), FOOT, 9, sub)
    text(s, W - M - x(0.6), H - x(0.45), x(0.6), x(0.3), f"{page:02d} / 11", 9, sub, MONO)
    if notes:
        s.notes_slide.notes_text_frame.text = notes
    return s


def card(s, left, top, width, height, head, body, dark=False, label=None, size=12):
    box(s, left, top, width, height, PINE if dark else PAPER)
    box(s, left, top, width, Pt(4), SAGE)
    fg = CREAM if dark else DEEP
    y = top + x(0.18)
    if label:
        text(s, left + x(0.18), y, width - x(0.36), x(0.25), label, 10, SAGE if dark else MOSS, MONO, True)
        y += x(0.3)
    text(s, left + x(0.18), y, width - x(0.36), height - (y - top) - x(0.1), [[(head, True)], body], size, fg)


def cols(n, top, height, gap=0.2, left=None, width=None):
    left = M if left is None else left
    width = (W - 2 * M) if width is None else width
    g = x(gap)
    w = int((width - g * (n - 1)) / n)
    return [(left + i * (w + g), top, w, height) for i in range(n)]


# 1 Cover
s = new_slide(1, "Extol Affiliates · Proposal", None, dark=True,
              notes="Open on the credibility gap: buyers and investors back founders they already know. Amit already has the career; this makes it visible.")
text(s, M, x(1.1), x(10.5), x(1.9), "A founder voice NHS imaging buyers and investors already trust.", 44, CREAM, DISPLAY, True)
text(s, M, x(3.15), x(10.5), x(0.4), "The founder-led marketing system for Amit Chavda and DigitalClinic.ai.", 16, SAGE)
ph = box(s, M, x(3.6), x(4.6), x(0.4), PINE, SAGE, dash=True)
text(s, M + x(0.12), x(3.66), x(4.4), x(0.3), "[One line: what DigitalClinic.ai does]", 12, SAGE, MONO)
for (l, t, w, h), (n, lab) in zip(cols(3, x(4.35), x(1.3), 0.4, width=x(9)),
                                  [("19", "years in UK imaging"), ("2", "audiences: NHS buyers, investors"), ("1", "approval a week")]):
    box(s, l, t, w, Pt(1.5), SAGE)
    text(s, l, t + x(0.1), w, x(0.75), n, 44, CREAM, DISPLAY, True)
    text(s, l, t + x(0.85), w, x(0.35), lab, 12, SAGE)
text(s, M, x(5.95), x(8), x(0.3), "Prepared for Amit Chavda · London, October 2026", 11, SAGE)

# 2 Before our view
s = new_slide(2, "Before our view", "What we think is going on. Tell us where we're wrong.", notes="Ask, don't present. Get Amit talking for 5-10 minutes before slide 3; his answers re-weight everything after. Q01 and Q03 are the deal-breakers: if he can't separate Radiobotics, AXREM and DigitalClinic.ai publicly, the founder-voice plan changes. Q06 sets outcome 01's number.")
text(s, M, x(1.35), W - 2 * M, x(0.35), 'Six questions, each from something we noticed. Your answers decide what we build.', 14, MOSS)
qs = [('You sell AI to the NHS by day at Radiobotics and are building DigitalClinic.ai alongside it.', 'Where does Radiobotics end and DigitalClinic.ai begin, and who has to agree where that line sits?'),
      ('You have been the radiographer, the commissioner and the vendor.', "When an NHS imaging lead hasn't met you, why would they pilot a startup over a vendor they already buy from?"),
      ("You now help shape AXREM's view on AI in imaging.", 'Which of your views can you say in public, and which belong to AXREM?'),
      ('An NHS AI purchase passes radiology, IT, procurement and finance.', 'Who says yes to a DigitalClinic.ai pilot, and who has the problem first?'),
      ('Investors back traction, not CVs.', 'What does an investor need to see before the first cheque: pilots, letters of intent, or an audience that listens?'),
      ("Followers don't pay. Pilots and cheques do.", 'What is one NHS pilot worth to you, and how many conversations does it take to land one?')]
text(s, M + x(0.55), x(1.85), x(4), x(0.25), "WHAT WE NOTICED", 9, MOSS, MONO, True)
text(s, M + x(4.9), x(1.85), x(4), x(0.25), "THE QUESTION", 9, MOSS, MONO, True)
top, rh = x(2.15), x(0.72)
box(s, M, top, W - 2 * M, Pt(1.5), MOSS)
for i, (seen, q) in enumerate(qs):
    y = top + i * rh
    if i:
        box(s, M, y, W - 2 * M, Pt(0.75), PAPER)
    text(s, M, y + x(0.1), x(0.5), x(0.4), f"0{i + 1}", 14, MOSS, DISPLAY, True)
    text(s, M + x(0.55), y + x(0.1), x(4.1), rh - x(0.1), seen, 12, DEEP)
    text(s, M + x(4.9), y + x(0.08), W - 2 * M - x(4.9), rh - x(0.08), q, 15, DEEP, DISPLAY, True)
text(s, M, top + 6 * rh + x(0.08), W - 2 * M, x(0.3), 'Discussion document · Public work history (LinkedIn via Apollo), October 2026', 9, MOSS)

# 3 Why Amit
s = new_slide(3, "Why Amit", "Amit has worked every side of UK imaging: clinic, NHS, vendor and industry body.",
              notes="Situation: 19 years from radiographer to AI founder. Each stage is a buyer or investor objection he can already answer.")
stages = [("Clinic", "2007-2013", "Lead Radiographer, Brighton and Sussex University Hospital"),
          ("NHS", "2014-2018", "NHS England and commissioning analytics"),
          ("Vendor", "2018-now", "Siemens Healthineers, Ergéa, Radiobotics"),
          ("Industry voice", "2026-now", "Vice Convenor, AXREM AI Special Focus Group")]
for i, ((l, t, w, h), (head, yrs, body)) in enumerate(zip(cols(4, x(2.2), x(1.9)), stages)):
    card(s, l, t, w, h, head, body, dark=i == 3, label=yrs, size=13)
box(s, M, x(4.35), W - 2 * M, x(0.8), PINE)
text(s, M + x(0.25), x(4.35), W - 2 * M - x(0.5), x(0.8),
     "Few AI founders have stood in the reading room, the commissioning meeting and the vendor pitch. That is DigitalClinic.ai's edge, and almost nobody outside his network sees it yet.",
     14, CREAM, anchor=MSO_ANCHOR.MIDDLE)
text(s, M, x(5.35), W - 2 * M, x(0.3), "Source: LinkedIn work history via Apollo, October 2026. AXREM: UK trade association, 120+ member companies.", 9, MOSS)

# 4 Same room
s = new_slide(4, "Same event, same gap", "Uche Nnene, met at the same event, has the same gap in finance. We've put the same engine to Effectivepoint.",
              notes="We met them in the same room and the pattern is identical. Share the approach, never the other client's numbers. Confirm with Uche before naming Effectivepoint.")
c3 = cols(3, x(2.2), x(2.55), 0.25)
card(s, *c3[0], "Dr Uche Nnene FCCA", "Co-founder, Effectivepoint. Former EY partner. ERP, Finance and AI transformation for CFOs. Met at [Event name].", label="WHO", size=13)
card(s, *c3[1], "Expertise buyers can't see", "Deep expertise and named results live in the work, not where senior buyers look. CFOs and NHS imaging leaders both pick people they already know.", label="THE SHARED GAP", size=13)
card(s, *c3[2], "Watch · Draft · Approve · Publish · Measure", "Agents watch buyers' posts and draft comments and proof posts in the founder's voice; the founder approves each in a minute. First outcome: one Finance Director conversation started on LinkedIn.", dark=True, label="THE APPROACH WE'VE PUT TO THEM", size=12)
box(s, M, x(4.95), W - 2 * M, x(0.6), PINE)
text(s, M + x(0.25), x(4.95), W - 2 * M - x(0.5), x(0.6), "For Amit: the same buyer-comment engine on NHS imaging leaders' posts, alongside the weekly recording.", 14, BONE, anchor=MSO_ANCHOR.MIDDLE)
text(s, M, x(5.7), W - 2 * M, x(0.3), "Effectivepoint named with permission [confirm with Uche before sending].", 9, MOSS)

# 5 Goal
s = new_slide(5, "The goal", "Two audiences, one voice: NHS buyers for pilots, investors for the raise.",
              notes="Complication: a startup with no public voice starts every buyer and investor conversation cold. Resolution: founder-led content.")
for (l, t, w, h), (lab, head, body) in zip(cols(2, x(2.2), x(1.9), 0.3), [
        ("01", "Qualified conversations with NHS imaging buyers", "Radiology leads, PACS/IT and procurement see a founder who knows their workflow. Every post leads to a page and a tracked enquiry route."),
        ("02", "Investor-ready credibility", "A visible track record and audience that shortens diligence and warms investor introductions.")]):
    card(s, l, t, w, h, head, body, label=lab, size=15)
box(s, M, x(4.35), W - 2 * M, x(0.7), PINE)
text(s, M + x(0.25), x(4.35), W - 2 * M, x(0.7), "Founder first. The DigitalClinic.ai page amplifies. Radiobotics and AXREM content stays out.", 15, CREAM, anchor=MSO_ANCHOR.MIDDLE)

# 6 How it works
s = new_slide(6, "How it works", "One recording a week becomes a week of founder content.",
              notes="Amit appears twice a week: recording and one review. Everything else is Extol.")
steps = [("Record", "One 30-min session: explainer, conversation or event debrief (format to agree)", True),
         ("Edit", "Full video and short clips", False), ("Package", "LinkedIn posts, article, newsletter, investor update", False),
         ("Approve", "One weekly review", True), ("Publish", "Every channel, scheduled", False), ("Learn", "The numbers set next week", False)]
for i, ((l, t, w, h), (head, body, you)) in enumerate(zip(cols(6, x(2.2), x(1.9), 0.15), steps)):
    card(s, l, t, w, h, head, body, dark=you, label=f"0{i + 1}" + (" · YOU" if you else ""), size=12)
text(s, M, x(4.2), W - 2 * M, x(0.3), "Dark steps are the only ones that need Amit.", 11, MOSS)
box(s, M, x(4.6), W - 2 * M, x(0.7), PINE)
text(s, M + x(0.25), x(4.6), W - 2 * M - x(0.5), x(0.7), "The DigitalClinic.ai website is home base. Every post points to a page about Amit, the product, an article or a demo request.", 14, CREAM, anchor=MSO_ANCHOR.MIDDLE)

# 7 Proof
s = new_slide(7, "Running today", "The engine already runs: four Extol agents, each with a sourced result.",
              notes="Proof that the pieces already work. Amit's version reuses the LinkedIn Manager and the Social Media Manager directly.")
for (l, t, w, h), (big, head, body) in zip(cols(4, x(2.1), x(2.45), 0.2), [
        ("40%", "LinkedIn Manager", "of invites accepted across 25 live personal brand campaigns. A personal note for every request."),
        ("+326.2%", "AI Social Media Manager", "LinkedIn impressions over 90 days. One approval click in Slack per post."),
        ("57.4%", "Lead Magnet Agent", "open rate across 61 sequences. One email written for one business."),
        ("2 min", "Finance Handler Agent", "from call transcript to priced proposal, down from 2 days.")]):
    box(s, l, t, w, h, PAPER)
    box(s, l, t, w, Pt(4), MOSS)
    text(s, l + x(0.18), t + x(0.2), w - x(0.36), x(0.7), big, 34, DEEP, DISPLAY, True)
    text(s, l + x(0.18), t + x(0.95), w - x(0.36), h - x(1.0), [[(head, True)], body], 12, DEEP)
box(s, M, x(4.8), W - 2 * M, x(0.6), PINE)
text(s, M + x(0.25), x(4.8), W - 2 * M - x(0.5), x(0.6), "Fixed price, agreed up front. Built in your accounts; you own everything. No lock-in.", 14, BONE, anchor=MSO_ANCHOR.MIDDLE)
text(s, M, x(5.55), W - 2 * M, x(0.3), "Source: extol.si case studies; LinkedIn analytics to 29 Apr 2026; Instantly dashboard 29 Mar to 29 Apr 2026.", 9, MOSS)

# 8 Tools
s = new_slide(8, "The tools", "The stack. One job each.")
rows = [("TOOL", "ITS JOB", "WHAT YOU GET"),
        ("ChatGPT", "The writer behind everything", "Scripts, posts, articles, newsletters and investor updates, drafted from your recordings"),
        ("Higgsfield", "Video quality", "Clean edits, subtitles, motion and covers. Full videos plus vertical shorts"),
        ("Apollo", "Lists, outreach, newsletter", "Targeted NHS imaging buyer and investor lists, outreach sequences, the newsletter"),
        ("Bloggerly.ai", "SEO and AI search", "Articles that rank on Google and show up in AI answers"),
        ("LinkedIn manager", "Authority and conversations", "Founder profile, posting and engagement in your voice; DigitalClinic.ai page amplifies")]
widths, top = [x(2.4), x(3.2), W - 2 * M - x(5.6)], x(1.75)
for r, row in enumerate(rows):
    rh = x(0.35) if r == 0 else x(0.55)
    if r:
        box(s, M, top, W - 2 * M, Pt(0.75), MOSS)
    left = M
    for c, cell in enumerate(row):
        if r == 0:
            text(s, left, top + x(0.05), widths[c], rh, cell, 10, MOSS, MONO, True)
        else:
            text(s, left, top + x(0.12), widths[c] - x(0.15), rh, cell, 14 if c == 0 else 12, DEEP, DISPLAY if c == 0 else TEXT, c == 0)
        left += widths[c]
    top += rh
text(s, M, top + x(0.2), W - 2 * M, x(0.4), "LinkedIn is the main channel for NHS and investor audiences. Full recordings go to YouTube; the newsletter doubles as the investor update.", 11, MOSS)

# 9 Example
s = new_slide(9, "An example", "One topic becomes four assets for two audiences.",
              notes="Proposed topic only. Nothing is quoted or published; the real example replaces this after the first recording.")
box(s, M, x(1.85), W - 2 * M, x(1.05), CREAM, MOSS, dash=True)
text(s, M + x(0.25), x(1.97), W - 2 * M - x(0.5), x(0.3), "PLACEHOLDER · EXAMPLE TO BE PRODUCED FROM AMIT'S FIRST RECORDING", 10, MOSS, MONO, True)
text(s, M + x(0.25), x(2.3), W - 2 * M - x(0.5), x(0.5), 'Proposed topic: "What should an NHS imaging department ask before it buys AI?"', 18, DEEP, DISPLAY, True)
for (l, t, w, h), (head, body) in zip(cols(4, x(3.2), x(1.5)), [
        ("LinkedIn clip", "60 seconds, subtitled. For buyers."), ("Search article", "Ranks on Google and in AI answers. For buyers."),
        ("Newsletter", "One section, sent via Apollo. For both."), ("Investor update", "What buyers are asking this month. For investors.")]):
    card(s, l, t, w, h, head, body, size=13)

# 10 Control
s = new_slide(10, "Control and the first outcome", "One approval keeps Radiobotics, AXREM and DigitalClinic.ai cleanly separate.",
              notes="He is still employed at Radiobotics: separation is a feature, not a risk. The four-week pilot proves the first outcome.")
lw = x(6.7)
for i, ((l, t, w, h), (head, body)) in enumerate(zip(cols(4, x(2.2), x(1.35), 0.12, width=lw), [
        ("Build", "The weekly pack"), ("Review", "Claims, brand, links, once"), ("Publish", "Only approved items"), ("Learn", "Views, clicks, enquiries, investor replies")])):
    card(s, l, t, w, h, head, body, dark=i == 1, label=f"{i + 1}", size=11)
box(s, M, x(3.75), lw, x(1.55), PAPER)
box(s, M, x(3.75), Pt(4), x(1.55), PINE)
text(s, M + x(0.25), x(3.87), lw - x(0.4), x(1.35),
     "No Radiobotics products, customers or pipeline. AXREM positions only once AXREM has published them. Clinical, regulatory and performance claims need explicit sign-off. Check the Radiobotics contract and conflict-of-interest policy before launch. Everything runs in Amit's own accounts; he owns every account, credential and file.",
     12, DEEP)
rl = M + lw + x(0.3)
card(s, rl, x(2.2), W - M - rl, x(3.1), "The first qualified NHS buyer conversation that came from content.",
     "Target: a number we agree before we start.\nProof: every enquiry traced to the post that sent it.\nWeekly output (proposed): 1 edited recording, 4-6 shorts, 3 LinkedIn posts, 1 article, 1 newsletter.",
     dark=True, label="OUTCOME 01", size=13)

# 11 Next
s = new_slide(11, "Next", "Six answers, then we price the pilot.", dark=True)
qs = [("DigitalClinic.ai", "What it does in one line, its stage, and are you raising now?"),
      ("Audience", "Which trusts, roles and investors, and where should each post send them?"),
      ("Roles", "What does your Radiobotics contract allow, and how do you disclose AXREM and DigitalClinic.ai?"),
      ("Production", "Can you record once a week, and in what style?"),
      ("Access", "Which accounts connect, and who handles enquiries?"),
      ("Budget", "What pilot budget and tool cap works for you?")]
grid = cols(3, x(1.75), x(1.35), 0.2) + cols(3, x(3.3), x(1.35), 0.2)
for i, ((l, t, w, h), (head, body)) in enumerate(zip(grid, qs)):
    box(s, l, t, w, h, FOREST)
    box(s, l, t, w, Pt(4), SAGE)
    text(s, l + x(0.18), t + x(0.15), w - x(0.36), x(0.25), f"0{i + 1}", 10, SAGE, MONO, True)
    text(s, l + x(0.18), t + x(0.42), w - x(0.36), h - x(0.5), [[(head, True)], body], 12, CREAM)
text(s, M, x(4.9), W - 2 * M, x(0.6),
     "Fixed price, agreed up front: setup + monthly operation + capped tools (ChatGPT, Higgsfield, Apollo; Bloggerly.ai at no tool cost). You own everything. Nothing publishes until you approve the complete pack.",
     12, SAGE)

out = Path(__file__).with_name("Amit_Chavda_x_Extol.pptx")
prs.save(out)
print(out)
