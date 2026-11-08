"""Story: 10-Minute Delivery Truth (Zepto & Blinkit dark stores)."""

import math

import cairo

from engine import *  # noqa: F401,F403

TOPIC = "10-MINUTE DELIVERY TRUTH"
OUTPUTS = {"edge": "dark_store_short.mp4", "elevenlabs": "dark_store_elevenlabs.mp4"}


# Each scene's narration is authored as (hindi, hinglish caption) chunks so the
# kinetic captions can be aligned to edge-tts word boundaries.
SCRIPT = [
    ("clock", [
        ("सिर्फ़ दस मिनट में", "SIRF 10 MINUTE"),
        ("डिलीवरी?", "DELIVERY?"),
        ("जादू नहीं", "JAADU NAHI"),
        ("पूरा गेम है", "POORA GAME HAI!"),
        ("ज़ेप्टो ब्लिंकिट का", "ZEPTO BLINKIT KA"),
        ("सीक्रेट हथियार", "SECRET HATHIYAAR!"),
    ]),
    ("warehouse", [
        ("मिलिए", "MILIYE"),
        ("डार्क स्टोर से", "DARK STORE SE!"),
        ("कस्टमर की", "CUSTOMER KI"),
        ("एंट्री बंद", "ENTRY BAND"),
        ("अंदर हज़ारों प्रोडक्ट्स", "HAZAARON PRODUCTS"),
        ("और आपके घर से", "AAPKE GHAR SE"),
        ("बस दो किलोमीटर", "BAS 2 KM!"),
    ]),
    ("packing", [
        ("ऑर्डर आते ही", "ORDER AATE HI"),
        ("टाइमर ऑन", "TIMER ON!"),
        ("स्कैन", "SCAN"),
        ("पिक", "PICK"),
        ("पैक", "PACK"),
        ("दो मिनट में", "2 MINUTE MEIN"),
        ("बैग रेडी", "BAG READY!"),
    ]),
    ("rider", [
        ("अब राइडर के पास", "AB RIDER KE PAAS"),
        ("सिर्फ़ आठ मिनट", "SIRF 8 MINUTE!"),
        ("ट्रैफ़िक", "TRAFFIC"),
        ("गड्ढे", "GADDHE"),
        ("बारिश", "BAARISH"),
        ("हर दिन", "HAR DIN"),
        ("आपके लिए रिस्क", "AAPKE LIYE RISK!"),
    ]),
    ("door", [
        ("डिंग डॉन्ग", "DING DONG!"),
        ("ऑर्डर हाज़िर", "ORDER HAAZIR!"),
        ("अगली बार राइडर को", "AGLI BAAR RIDER KO"),
        ("थैंक यू ज़रूर बोलना", "THANK YOU BOLNA!"),
        ("ऐसी और कहानियों के लिए", "AUR KAHANIYAN?"),
        ("फ़ॉलो करो", "FOLLOW KARO!"),
    ]),
]


# ============================================================ scenes
# Each scene: draw(ctx, t, d) renders local time t of a d-second scene;
# events(d) returns [(time, sfx_name)] for the SFX mixer.

class Clock:
    accent = hexc("#FF5A36")
    TICK = 0.25
    BURST = 1.4

    def events(self, d):
        ev = [(0.05, "alarm")]
        ev += [(k * self.TICK, "tick" if k % 2 else "tock") for k in range(int(d / self.TICK))]
        return ev

    def draw(self, ctx, t, d):
        backdrop(ctx, hexc("#1E0B30"), hexc("#06030D"), self.accent, 540, 820, t)
        cx, cy, R = 540, 840, 290
        # rotating sunburst
        ctx.save()
        ctx.translate(cx, cy)
        ctx.rotate(t * 0.5)
        for i in range(18):
            ctx.move_to(0, 0)
            ctx.arc(0, 0, 1400, i * math.tau / 18, i * math.tau / 18 + math.tau / 36)
            ctx.close_path()
            rgba(ctx, self.accent, 0.05)
            ctx.fill()
        ctx.restore()
        # expanding pulse rings
        for k in range(3):
            u = (t * 1.1 + k / 3) % 1
            ctx.arc(cx, cy, R + 40 + u * 520, 0, math.tau)
            rgba(ctx, self.accent, 0.3 * (1 - u))
            ctx.set_line_width(6)
            ctx.stroke()
        # shake bursts
        u = t % self.BURST
        amp = 24 * math.exp(-u * 5)
        sx, sy = amp * math.sin(t * 90), amp * math.cos(t * 77)
        wob = 0.06 * math.exp(-u * 5) * math.sin(t * 60)
        ring = 0.35 * math.sin(t * 55) * math.exp(-u * 3)

        ctx.save()
        ctx.translate(cx + sx, cy + sy)
        ctx.rotate(wob)
        # legs
        for side in (-1, 1):
            line(ctx, [(side * 150, R * 0.75), (side * 210, R + 70)], hexc("#3A2A4A"), 30)
        # bells + hammer
        for side in (-1, 1):
            ctx.save()
            ctx.rotate(side * 0.62 + ring)
            ctx.arc(0, -R - 45, 85, math.pi, 2 * math.pi)
            ctx.close_path()
            rgba(ctx, hexc("#FFC300"))
            ctx.fill()
            circle(ctx, 0, -R - 45, 12, hexc("#B07D00"))
            ctx.restore()
        line(ctx, [(0, -R), (math.sin(t * 50) * 40, -R - 70)], hexc("#8D8D9A"), 12)
        circle(ctx, math.sin(t * 50) * 40, -R - 70, 18, hexc("#D9D9E3"))
        # 3D body
        circle(ctx, 14, 20, R + 30, (0, 0, 0), 0.45)
        g = cairo.LinearGradient(-R, -R, R, R)
        g.add_color_stop_rgb(0, *shade(self.accent, 1.15))
        g.add_color_stop_rgb(1, *shade(self.accent, 0.55))
        ctx.set_source(g)
        ctx.arc(0, 0, R + 30, 0, math.tau)
        ctx.fill()
        g = cairo.RadialGradient(-60, -80, 20, 0, 0, R)
        g.add_color_stop_rgb(0, 1, 0.99, 0.95)
        g.add_color_stop_rgb(1, 0.86, 0.84, 0.8)
        ctx.set_source(g)
        ctx.arc(0, 0, R, 0, math.tau)
        ctx.fill()
        for i in range(60):
            a = i * math.tau / 60
            r0 = R - (40 if i % 5 == 0 else 22)
            line(ctx, [(math.sin(a) * r0, -math.cos(a) * r0), (math.sin(a) * (R - 12), -math.cos(a) * (R - 12))],
                 (0.15, 0.15, 0.2), 8 if i % 5 == 0 else 3)
        for n, a in ((12, 0), (3, 0.25), (6, 0.5), (9, 0.75)):
            ang = a * math.tau
            text(ctx, str(n), math.sin(ang) * (R - 85), -math.cos(ang) * (R - 85), 62, (0.15, 0.15, 0.2))
        # hands spin unnaturally fast
        for ang, length, width, col in ((t * 0.9, R * 0.5, 18, (0.12, 0.12, 0.16)),
                                       (t * 7.0, R * 0.75, 12, (0.12, 0.12, 0.16)),
                                       (t * 22.0, R * 0.85, 5, self.accent)):
            line(ctx, [(-math.sin(ang) * 30, math.cos(ang) * 30), (math.sin(ang) * length, -math.cos(ang) * length)],
                 col, width)
        circle(ctx, 0, 0, 20, self.accent)
        circle(ctx, 0, 0, 8, (1, 1, 1))
        ctx.restore()

        # pulsing question marks
        for qx, qy, size, ph in ((870, 450, 260, 0.0), (190, 560, 170, 1.7), (900, 1180, 130, 3.1)):
            p = 1 + 0.18 * math.sin(t * 7 + ph)
            ctx.save()
            ctx.translate(qx, qy)
            ctx.rotate(0.25 * math.sin(t * 3 + ph))
            ctx.scale(p, p)
            text(ctx, "?", 0, 0, size, hexc("#FFD60A"), font=CAPTION_FONT, stroke=(0, 0, 0), stroke_w=10)
            ctx.restore()
        # "10 MIN" badge
        p = 1 + 0.06 * math.sin(t * 10)
        ctx.save()
        ctx.translate(540, 1290)
        ctx.scale(p, p)
        rrect(ctx, -170, -55, 340, 110, 55)
        rgba(ctx, self.accent)
        ctx.fill()
        text(ctx, "10 MIN", 0, 0, 72, (1, 1, 1), font=CAPTION_FONT)
        ctx.restore()


class Warehouse:
    accent = hexc("#8B5CFF")
    PICK = 0.85
    FLY = 0.55
    BOX_COLS = [hexc(c) for c in ("#C98B4E", "#E0A458", "#4EA8DE", "#F25F5C", "#57CC99", "#FFD166")]
    LEVELS = (500, 690, 880, 1070)

    def pick_times(self, d):
        return [k * self.PICK + 0.3 for k in range(int(d / self.PICK) + 1) if k * self.PICK + 0.3 + self.FLY < d]

    def events(self, d):
        return [(t0 + self.FLY, "pick") for t0 in self.pick_times(d)]

    def shelves(self, ctx, t, speed, scale, y0, dim):
        unit = 360 * scale
        off = t * speed
        first = math.floor(off / unit)
        for u in range(first - 1, first + int(W / unit) + 3):
            x0 = u * unit - off
            post = shade(hexc("#3B3F58"), dim)
            for px in (x0 + 8 * scale, x0 + unit - 22 * scale):
                ctx.rectangle(px, y0 - 760 * scale, 16 * scale, 790 * scale)
                rgba(ctx, post)
                ctx.fill()
            for li, lv in enumerate(self.LEVELS):
                ly = y0 - (1100 - lv) * scale
                for j in range(3):
                    bw = (60 + 40 * rnd(u * 7 + li * 3 + j, 1)) * scale
                    bh = (55 + 60 * rnd(u * 7 + li * 3 + j, 2)) * scale
                    col = shade(self.BOX_COLS[int(rnd(u * 7 + li * 3 + j, 3) * 6)], dim)
                    box(ctx, x0 + (70 + j * 105) * scale, ly - bh / 2, bw, bh, col)
                ctx.rectangle(x0, ly, unit, 16 * scale)
                rgba(ctx, shade(hexc("#5A6080"), dim))
                ctx.fill()

    def draw(self, ctx, t, d):
        backdrop(ctx, hexc("#0D0B24"), hexc("#040309"), self.accent, 540, 300, t, motes=60)
        self.shelves(ctx, t, 110, 0.62, 1090, 0.45)  # far parallax row
        # ceiling lamps
        for lx in (200, 540, 880):
            flick = 0.85 + 0.15 * math.sin(t * 30 + lx)
            ctx.move_to(lx - 40, 210)
            ctx.line_to(lx + 40, 210)
            ctx.line_to(lx + 260, 1250)
            ctx.line_to(lx - 260, 1250)
            ctx.close_path()
            g = cairo.LinearGradient(0, 210, 0, 1250)
            g.add_color_stop_rgba(0, 1, 0.95, 0.8, 0.22 * flick)
            g.add_color_stop_rgba(1, 1, 0.95, 0.8, 0)
            ctx.set_source(g)
            ctx.fill()
            rrect(ctx, lx - 50, 196, 100, 18, 9)
            rgba(ctx, (1, 0.97, 0.85), flick)
            ctx.fill()
        self.shelves(ctx, t, 260, 1.0, 1210, 1.0)
        # floor
        g = cairo.LinearGradient(0, 1210, 0, 1500)
        g.add_color_stop_rgb(0, *hexc("#1B1A33"))
        g.add_color_stop_rgb(1, *hexc("#08070F"))
        ctx.set_source(g)
        ctx.rectangle(0, 1210, W, H - 1210)
        ctx.fill()
        for i in range(-2, 14):
            x = i * 120 - (t * 260) % 120
            line(ctx, [(x, 1215), (x - 160, 1500)], (1, 1, 1), 2, 0.06)
        # neon sign
        on = 1.0 if rnd(math.floor(t * 12), 9) > 0.1 else 0.3
        for w_, a_ in ((34, 0.08), (20, 0.15), (8, 0.35)):
            ctx.select_font_face(UI_FONT, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
            ctx.set_font_size(96)
            tw = ctx.text_extents("DARK STORE")[2]
            ctx.move_to(540 - tw / 2, 345)
            ctx.text_path("DARK STORE")
            rgba(ctx, hexc("#FF4FD8"), a_ * on)
            ctx.set_line_width(w_)
            ctx.set_line_join(cairo.LINE_JOIN_ROUND)
            ctx.stroke()
        text(ctx, "DARK STORE", 540, 312, 96, hexc("#FFD6F6"), a=on)

        # worker running and catching boxes into a crate
        wx = 520 + 50 * math.sin(t * 0.9)
        ctx.save()
        ctx.translate(wx, 1300)
        ctx.scale(1, 0.25)
        circle(ctx, 0, 0, 120, (0, 0, 0), 0.4)
        ctx.restore()
        hand = person(ctx, wx, 1300, 1.3, t * 11, self.accent, mode="carry", cap=hexc("#FFD60A"))
        bx, by = hand[0] + 10, hand[1] - 20
        picked = [t0 for t0 in self.pick_times(d) if t0 <= t]
        landed = sum(1 for t0 in picked if t - t0 >= self.FLY)
        # crate
        rrect(ctx, bx - 85, by - 30, 170, 95, 12)
        rgba(ctx, hexc("#FFD60A"))
        ctx.fill()
        for k in range(1, 4):
            line(ctx, [(bx - 85 + k * 42, by - 22), (bx - 85 + k * 42, by + 56)], hexc("#C9A400"), 6)
        for k in range(min(landed, 3)):
            box(ctx, bx - 45 + k * 45, by - 45, 50, 40, self.BOX_COLS[(landed - k) % 6])
        for i, t0 in enumerate(picked):
            u = (t - t0) / self.FLY
            if u >= 1:
                if u < 1 + 0.5 / self.FLY:
                    k = (t - t0 - self.FLY) / 0.5
                    text(ctx, "+1", bx + 90, by - 90 - 80 * k, 70, hexc("#57CC99"), font=CAPTION_FONT,
                         a=1 - k, stroke=(0, 0, 0), stroke_w=6)
                continue
            sx = 150 + rnd(i, 11) * 780
            sy = self.LEVELS[i % 4] + 110 - 60
            px = lerp(sx, bx, ease_in_out(u))
            py = lerp(sy, by - 40, u) - 320 * math.sin(math.pi * u)
            box(ctx, px, py, 70, 60, self.BOX_COLS[i % 6], rot=u * 5)
        # counter chip
        rrect(ctx, 80, 1380, 300, 80, 40)
        rgba(ctx, (0, 0, 0), 0.55)
        ctx.fill()
        text(ctx, f"PICKED  {landed:02d}", 230, 1420, 40, (1, 1, 1))


class Packing:
    accent = hexc("#00D68F")
    PERIOD = 0.9
    SPEED = 600
    SCAN_X = 470
    BELT_END = 800
    DROP = 0.4

    def schedule(self, d):
        out = []
        for k in range(int(d / self.PERIOD) + 2):
            t0 = k * self.PERIOD
            scan = t0 + (self.SCAN_X + 80) / self.SPEED
            edge = t0 + (self.BELT_END + 80) / self.SPEED
            out.append((k, t0, scan, edge, edge + self.DROP))
        return out

    def events(self, d):
        ev = []
        for _, _, scan, _, land in self.schedule(d):
            if scan < d:
                ev.append((scan, "beep"))
            if land < d:
                ev.append((land, "soft_thud"))
        return ev

    def draw(self, ctx, t, d):
        backdrop(ctx, hexc("#04211A"), hexc("#020A08"), self.accent, 540, 480, t)
        # timer panel
        total = max(d - 0.5, 1)
        val = 120 * (1 - clamp(t / total))
        n = math.ceil(val)
        frac = val - math.floor(val)
        col = (lerp(1, 0, n / 120) * 1.0 + 0.0, lerp(0.3, 0.84, n / 120), lerp(0.3, 0.56, n / 120))
        pulse = 1 + 0.1 * frac ** 3
        ctx.save()
        ctx.translate(540, 520)
        ctx.scale(pulse, pulse)
        rrect(ctx, -330, -170, 660, 340, 50)
        rgba(ctx, (0.02, 0.05, 0.04), 0.9)
        ctx.fill()
        rrect(ctx, -330, -170, 660, 340, 50)
        rgba(ctx, col, 0.9)
        ctx.set_line_width(6)
        ctx.stroke()
        text(ctx, "PACKING TIMER", 0, -110, 40, (1, 1, 1), a=0.7)
        glow(ctx, 0, 20, 300, col, 0.25)
        text(ctx, f"{n}s", 0, 25, 200, col, font=CAPTION_FONT)
        rrect(ctx, -270, 120, 540, 18, 9)
        rgba(ctx, (1, 1, 1), 0.12)
        ctx.fill()
        rrect(ctx, -270, 120, 540 * val / 120, 18, 9)
        rgba(ctx, col)
        ctx.fill()
        ctx.restore()

        belt_y = 1040
        # picker behind the belt
        person(ctx, 230, 1200, 1.15, 0, hexc("#2F80ED"), mode="pack", cap=self.accent, t=t)
        # conveyor
        ctx.rectangle(-20, belt_y, self.BELT_END + 20, 60)
        rgba(ctx, hexc("#2B2F3A"))
        ctx.fill()
        ctx.save()
        ctx.rectangle(-20, belt_y, self.BELT_END + 20, 60)
        ctx.clip()
        for i in range(-2, 30):
            x = i * 40 + (t * self.SPEED) % 40
            line(ctx, [(x, belt_y), (x - 25, belt_y + 60)], (1, 1, 1), 5, 0.08)
        ctx.restore()
        for rx in range(30, self.BELT_END, 110):
            circle(ctx, rx, belt_y + 80, 26, hexc("#4A5060"))
            ang = t * 20
            line(ctx, [(rx - 20 * math.cos(ang), belt_y + 80 - 20 * math.sin(ang)),
                       (rx + 20 * math.cos(ang), belt_y + 80 + 20 * math.sin(ang))], hexc("#2B2F3A"), 6)
        for lx in (60, self.BELT_END - 60):
            ctx.rectangle(lx - 12, belt_y + 60, 24, 240)
            rgba(ctx, hexc("#3A3F4E"))
            ctx.fill()

        bag_x, bag_bottom = 920, 1330
        # bag back
        rrect(ctx, bag_x - 140, bag_bottom - 300, 280, 300, 24)
        rgba(ctx, shade(hexc("#7B2FF7"), 0.55))
        ctx.fill()
        landed, last_land = 0, -9
        scanning = False
        for k, t0, scan, edge, land in self.schedule(d):
            if t < t0:
                continue
            bw, bh = 90 + 50 * rnd(k, 4), 70 + 40 * rnd(k, 5)
            colr = Warehouse.BOX_COLS[k % 6]
            if t < edge:
                x = -80 + (t - t0) * self.SPEED
                if abs(x - self.SCAN_X) < 50:
                    scanning = True
                tag = (t > scan)
                box(ctx, x, belt_y - bh / 2, bw, bh, colr)
                if tag:
                    circle(ctx, x, belt_y - bh - 18, 16, self.accent)
            elif t < land:
                u = (t - edge) / self.DROP
                x = lerp(self.BELT_END, bag_x, u)
                y = lerp(belt_y - bh / 2, bag_bottom - 120, u * u) - 90 * math.sin(math.pi * u)
                box(ctx, x, y, bw, bh, colr, rot=u * 2.5)
            else:
                landed += 1
                last_land = land
        # scanner arch + laser
        ax = self.SCAN_X
        for px in (ax - 80, ax + 80):
            ctx.rectangle(px - 10, 820, 20, belt_y - 820)
            rgba(ctx, hexc("#3A3F4E"))
            ctx.fill()
        rrect(ctx, ax - 100, 800, 200, 50, 14)
        rgba(ctx, hexc("#2B2F3A"))
        ctx.fill()
        laser = hexc("#FF2E4D")
        circle(ctx, ax + 70, 825, 9, laser if scanning else shade(laser, 0.4))
        if scanning:
            ctx.move_to(ax - 30, 850)
            ctx.line_to(ax + 30, 850)
            ctx.line_to(ax + 70, belt_y)
            ctx.line_to(ax - 70, belt_y)
            ctx.close_path()
            rgba(ctx, laser, 0.3)
            ctx.fill()
            line(ctx, [(ax - 70, belt_y - 4), (ax + 70, belt_y - 4)], laser, 6)
            text(ctx, "BEEP!", ax, 760, 54, laser, font=CAPTION_FONT, stroke=(0, 0, 0), stroke_w=6)
        # bag front (squishes on each landing)
        u = (t - last_land) / 0.25
        sq = 1 - 0.09 * math.sin(math.pi * u) if 0 <= u <= 1 else 1
        ctx.save()
        ctx.translate(bag_x, bag_bottom)
        ctx.scale(2 - sq, sq)
        rrect(ctx, -150, -260, 300, 260, 26)
        g = cairo.LinearGradient(0, -260, 0, 0)
        g.add_color_stop_rgb(0, *hexc("#9D5CFF"))
        g.add_color_stop_rgb(1, *hexc("#6420D6"))
        ctx.set_source(g)
        ctx.fill()
        for side in (-1, 1):
            ctx.arc(side * 60, -300, 40, math.pi, 2 * math.pi)
            rgba(ctx, hexc("#4B14A8"))
            ctx.set_line_width(12)
            ctx.stroke()
        text(ctx, "10 MIN", 0, -150, 62, (1, 1, 1), font=CAPTION_FONT)
        text(ctx, f"{landed} ITEMS", 0, -80, 34, (1, 1, 1), a=0.85)
        ctx.restore()


class Rider:
    accent = hexc("#FF4D4D")
    WORLD = 1100   # road scroll speed px/s
    HOLE = 2.4
    CAR = 4.6
    RIDER_X = 430

    def holes(self, d):
        return [1.0 + k * self.HOLE for k in range(int(d / self.HOLE) + 1)]

    def hop_time(self, ts):
        return ts + (1250 - self.RIDER_X) / self.WORLD

    def cars(self, d):
        return [1.8 + k * self.CAR for k in range(int(d / self.CAR) + 1)]

    def events(self, d):
        ev = [(0.0, "engine", d)]
        ev += [(self.hop_time(ts) + 0.2, "thud") for ts in self.holes(d) if self.hop_time(ts) + 0.2 < d]
        ev += [(tc + (1400 - self.RIDER_X) / 1900 - 0.2, "whoosh") for tc in self.cars(d)
               if tc + 0.5 < d]
        return ev

    def scooter(self, ctx, x, y, t):
        ctx.save()
        ctx.translate(x, y)
        ctx.rotate(-0.03 + 0.01 * math.sin(t * 25))
        # headlight beam
        ctx.move_to(118, -190)
        ctx.line_to(560, -300)
        ctx.line_to(560, -20)
        ctx.close_path()
        g = cairo.LinearGradient(118, 0, 560, 0)
        g.add_color_stop_rgba(0, 1, 0.95, 0.7, 0.45)
        g.add_color_stop_rgba(1, 1, 0.95, 0.7, 0)
        ctx.set_source(g)
        ctx.fill()
        # wheels
        for wx in (-115, 120):
            circle(ctx, wx, -48, 50, hexc("#111317"))
            circle(ctx, wx, -48, 30, hexc("#9AA0AE"))
            for k in range(5):
                a = t * 22 + k * math.tau / 5
                line(ctx, [(wx, -48), (wx + 28 * math.cos(a), -48 + 28 * math.sin(a))], hexc("#55596A"), 5)
            circle(ctx, wx, -48, 8, hexc("#2B2F3A"))
        # delivery box
        rrect(ctx, -235, -315, 150, 135, 14)
        rgba(ctx, hexc("#FFD60A"))
        ctx.fill()
        rrect(ctx, -235, -315, 150, 30, 14)
        rgba(ctx, hexc("#FFE666"))
        ctx.fill()
        text(ctx, "10", -160, -235, 54, hexc("#1A1A1A"), font=CAPTION_FONT)
        # rear body + seat
        ctx.move_to(-185, -60)
        ctx.curve_to(-200, -120, -170, -160, -120, -165)
        ctx.line_to(-20, -160)
        ctx.curve_to(-20, -110, -30, -70, -40, -55)
        ctx.close_path()
        rgba(ctx, self.accent)
        ctx.fill()
        rrect(ctx, -165, -185, 140, 26, 13)
        rgba(ctx, hexc("#1B1D24"))
        ctx.fill()
        rrect(ctx, -60, -72, 130, 18, 8)
        rgba(ctx, hexc("#2B2F3A"))
        ctx.fill()
        # rider (sitting)
        jacket = hexc("#2F80ED")
        hip, knee, foot = (-80, -180), (10, -175), (0, -78)
        shoulder, head = (-40, -282), (-18, -335)
        line(ctx, [hip, knee, foot], PANTS, 30)
        line(ctx, [foot, (25, -74)], (0.1, 0.1, 0.1), 20)
        line(ctx, [hip, shoulder], jacket, 66)
        circle(ctx, head[0], head[1], 40, SKIN)
        ctx.arc(head[0], head[1] + 2, 46, math.pi * 0.85, math.pi * 2.15)
        rgba(ctx, self.accent)
        ctx.fill()
        rrect(ctx, head[0] + 8, head[1] - 12, 42, 26, 10)
        rgba(ctx, hexc("#9FD3FF"), 0.85)
        ctx.fill()
        line(ctx, [shoulder, (30, -240), (82, -214)], jacket, 24)
        circle(ctx, 84, -214, 13, SKIN)
        # front shield, fork, bars, lamp
        ctx.move_to(40, -62)
        ctx.line_to(78, -200)
        ctx.line_to(108, -196)
        ctx.line_to(80, -55)
        ctx.close_path()
        rgba(ctx, shade(self.accent, 0.85))
        ctx.fill()
        line(ctx, [(104, -190), (120, -48)], hexc("#3A3F4E"), 12)
        line(ctx, [(70, -220), (100, -206)], hexc("#1B1D24"), 12)
        circle(ctx, 116, -190, 15, hexc("#FFF4C2"))
        ctx.restore()

    def draw(self, ctx, t, d):
        g = cairo.LinearGradient(0, 0, 0, 1200)
        g.add_color_stop_rgb(0, *hexc("#070B1F"))
        g.add_color_stop_rgb(1, *hexc("#2A1630"))
        ctx.set_source(g)
        ctx.paint()
        glow(ctx, 800, 420, 700, self.accent, 0.18)
        # far skyline
        off = t * 70
        for i in range(-1, 14):
            u = math.floor(off / 110) + i
            x = u * 110 - off
            bh = 260 + 380 * rnd(u, 1)
            ctx.rectangle(x, 1180 - bh, 104, bh)
            rgba(ctx, hexc("#151A33"))
            ctx.fill()
            for wy in range(int(1180 - bh + 30), 1150, 46):
                for wxk in range(3):
                    if rnd(u * 31 + wy + wxk, 2) > 0.55:
                        ctx.rectangle(x + 16 + wxk * 30, wy, 14, 20)
                        rgba(ctx, hexc("#FFD27A"), 0.55)
                        ctx.fill()
        # road
        ctx.rectangle(0, 1180, W, 340)
        rgba(ctx, hexc("#1C1E26"))
        ctx.fill()
        ctx.rectangle(0, 1170, W, 16)
        rgba(ctx, hexc("#555A6A"))
        ctx.fill()
        ctx.rectangle(0, 1520, W, H - 1520)
        rgba(ctx, hexc("#0B0C10"))
        ctx.fill()
        for i in range(-1, 8):
            x = i * 200 - (t * self.WORLD) % 200
            rrect(ctx, x, 1352, 110, 12, 6)
            rgba(ctx, (1, 1, 1), 0.7)
            ctx.fill()
        # streetlights
        for i in range(-1, 4):
            x = i * 460 - (t * 700) % 460 + 200
            line(ctx, [(x, 1180), (x, 560), (x + 90, 545)], hexc("#3A3F4E"), 14)
            ctx.move_to(x + 90, 560)
            ctx.line_to(x + 250, 1180)
            ctx.line_to(x - 70, 1180)
            ctx.close_path()
            g = cairo.LinearGradient(0, 560, 0, 1180)
            g.add_color_stop_rgba(0, 1, 0.85, 0.5, 0.25)
            g.add_color_stop_rgba(1, 1, 0.85, 0.5, 0.02)
            ctx.set_source(g)
            ctx.fill()
            glow(ctx, x + 90, 555, 90, hexc("#FFD27A"), 0.7)
        # potholes + hop
        hop = 0.0
        for ts in self.holes(d):
            hx = 1250 - (t - ts) * self.WORLD
            if -200 < hx < 1300 and t >= ts:
                ctx.save()
                ctx.translate(hx, 1300)
                ctx.scale(1, 0.22)
                circle(ctx, 0, 0, 80, hexc("#07080B"))
                ctx.restore()
            u = (t - (self.hop_time(ts) - 0.2)) / 0.4
            if 0 <= u <= 1:
                hop = 90 * math.sin(math.pi * u)
        # cones on the far side of the lane
        for k in range(int(d / 1.7) + 2):
            cx = 1200 - (t - (0.6 + k * 1.7)) * self.WORLD
            if -100 < cx < 1200 and t >= 0.6 + k * 1.7:
                ctx.move_to(cx - 30, 1225)
                ctx.line_to(cx, 1150)
                ctx.line_to(cx + 30, 1225)
                ctx.close_path()
                rgba(ctx, hexc("#FF8A00"))
                ctx.fill()
                ctx.rectangle(cx - 16, 1180, 32, 12)
                rgba(ctx, (1, 1, 1))
                ctx.fill()
        # exhaust
        ry = 1310 - hop + 3 * math.sin(t * 25)
        rx = self.RIDER_X + 25 * math.sin(t * 0.8)
        for k in range(10):
            age = (t + k * 0.09) % 0.9
            circle(ctx, rx - 190 - 380 * age, ry - 30 - 50 * age, 10 + 45 * age, (0.75, 0.75, 0.8), 0.35 * (1 - age / 0.9))
        ctx.save()
        ctx.translate(rx, 1312)
        ctx.scale(1, 0.12)
        circle(ctx, 0, 0, 240 - hop, (0, 0, 0), 0.5)
        ctx.restore()
        self.scooter(ctx, rx, ry, t)
        # oncoming car in the near lane
        for tc in self.cars(d):
            cx = 1400 - (t - tc) * 1900
            if t < tc or cx < -500:
                continue
            cy = 1470
            rrect(ctx, cx - 210, cy - 120, 420, 90, 30)
            rgba(ctx, hexc("#E8E8F0"))
            ctx.fill()
            rrect(ctx, cx - 130, cy - 185, 240, 80, 30)
            ctx.fill()
            rrect(ctx, cx - 110, cy - 172, 90, 55, 12)
            rgba(ctx, hexc("#2B3550"))
            ctx.fill()
            rrect(ctx, cx - 5, cy - 172, 90, 55, 12)
            ctx.fill()
            for wx in (-120, 120):
                circle(ctx, cx + wx, cy - 30, 42, hexc("#111317"))
                circle(ctx, cx + wx, cy - 30, 18, hexc("#9AA0AE"))
            glow(ctx, cx - 205, cy - 90, 120, hexc("#FFF4C2"), 0.8)
        # rain
        for i in range(90):
            x = (rnd(i, 1) * 1400 - t * 350) % 1400 - 160
            y = (rnd(i, 2) * 2000 + t * 1900) % 2000 - 60
            line(ctx, [(x, y), (x - 14, y + 46)], hexc("#9FB7FF"), 2.5, 0.35)
        # speed lines
        for i in range(8):
            y = 450 + rnd(i, 7) * 750
            x = W - ((t * 2600 + rnd(i, 8) * 2000) % 2200)
            line(ctx, [(x, y), (x + 220, y)], (1, 1, 1), 4, 0.25)
        # ETA HUD
        eta = 480 * (1 - clamp(t / max(d - 0.5, 1)))
        rrect(ctx, 340, 300, 400, 100, 50)
        rgba(ctx, (0, 0, 0), 0.6)
        ctx.fill()
        circle(ctx, 395, 350, 14, self.accent, 0.6 + 0.4 * math.sin(t * 8))
        text(ctx, f"ETA {int(eta // 60)}:{int(eta % 60):02d}", 565, 350, 58, (1, 1, 1), font=CAPTION_FONT)


class Door:
    accent = hexc("#00B8FF")
    RINGS = (0.05, 1.6)
    DROP_T, DROP_DUR = 0.6, 0.8

    def open_t(self, d):
        return min(3.0, d * 0.4)

    def cta_t(self, d):
        return max(self.open_t(d) + 0.6, d - 3.0)

    def events(self, d):
        ev = [(r, "dingdong") for r in self.RINGS if r < d - 1]
        for u, vol in ((1 / 2.75, "thud"), (2 / 2.75, "soft_thud"), (2.5 / 2.75, "soft_thud")):
            ev.append((self.DROP_T + u * self.DROP_DUR, vol))
        ev.append((self.open_t(d), "whoosh"))
        return ev

    def draw(self, ctx, t, d):
        self.OPEN_T = self.open_t(d)
        backdrop(ctx, hexc("#0E1A2B"), hexc("#05080F"), self.accent, 540, 900, t, motes=30)
        # brick wall
        for row in range(0, 30):
            y = 440 + row * 44
            if y > 1310:
                break
            off = 60 if row % 2 else 0
            for col in range(-1, 10):
                ctx.rectangle(col * 120 + off + 4, y + 4, 112, 36)
                rgba(ctx, hexc("#1C2A40"), 0.55 + 0.25 * rnd(row * 13 + col, 4))
                ctx.fill()
        dx, dy, dw, dh = 320, 520, 440, 780
        # interior (revealed when door opens)
        o = ease_in_out((t - self.OPEN_T) / 0.8)
        ctx.save()
        ctx.rectangle(dx, dy, dw, dh)
        ctx.clip()
        g = cairo.RadialGradient(540, 900, 50, 540, 900, 600)
        g.add_color_stop_rgb(0, *hexc("#FFE3A3"))
        g.add_color_stop_rgb(1, *hexc("#C9822E"))
        ctx.set_source(g)
        ctx.paint()
        if o > 0:
            person(ctx, 600, 1300, 1.45, 0, hexc("#F25F5C"), mode="wave", t=t, flip=True)
        ctx.restore()
        if o > 0:
            glow(ctx, 540, 1250, 520, hexc("#FFD27A"), 0.35 * o)
        # door frame + panel (hinged on the left)
        rrect(ctx, dx - 26, dy - 26, dw + 52, dh + 26, 12)
        rgba(ctx, hexc("#3B2A1E"))
        ctx.set_line_width(26)
        ctx.stroke()
        pw = dw * (1 - 0.82 * o)
        g = cairo.LinearGradient(dx, 0, dx + pw, 0)
        g.add_color_stop_rgb(0, *hexc("#8A4B2A"))
        g.add_color_stop_rgb(1, *hexc("#6B3519"))
        ctx.set_source(g)
        ctx.rectangle(dx, dy, pw, dh)
        ctx.fill()
        for py in (dy + 60, dy + 430):
            rrect(ctx, dx + pw * 0.12, py, pw * 0.76, 300, 10)
            rgba(ctx, hexc("#5A2C14"))
            ctx.set_line_width(8)
            ctx.stroke()
        circle(ctx, dx + pw * 0.88, dy + 420, 16, hexc("#FFC300"))
        text(ctx, "10", dx + pw / 2, dy + 30, 40, hexc("#FFC300"), a=1 - o)
        # wall lamp
        flick = 0.9 + 0.1 * math.sin(t * 13)
        glow(ctx, 200, 700, 220, hexc("#FFD27A"), 0.55 * flick)
        rrect(ctx, 180, 660, 40, 80, 12)
        rgba(ctx, hexc("#FFE9B0"))
        ctx.fill()
        # doormat
        rrect(ctx, 330, 1300, 420, 60, 10)
        rgba(ctx, hexc("#5C3D2E"))
        ctx.fill()
        text(ctx, "WELCOME", 540, 1330, 34, hexc("#D9B99B"))
        # doorbell + sound waves
        bx, by = 870, 880
        ringing = any(0 <= t - r < 0.9 for r in self.RINGS)
        rrect(ctx, bx - 40, by - 70, 80, 140, 20)
        rgba(ctx, hexc("#D9D9E3"))
        ctx.fill()
        circle(ctx, bx, by, 26, self.accent if ringing else hexc("#5A6070"))
        if ringing:
            glow(ctx, bx, by, 90, self.accent, 0.6)
        for r0 in self.RINGS:
            for k in range(4):
                age = t - r0 - k * 0.14
                if 0 <= age < 0.9:
                    rad = 60 + age * 260
                    for side in (0, math.pi):
                        ctx.arc(bx, by, rad, side - 0.6, side + 0.6)
                        rgba(ctx, self.accent, 1 - age / 0.9)
                        ctx.set_line_width(9)
                        ctx.stroke()
                        ctx.new_path()
        # package drop with bounce + squash
        u = (t - self.DROP_T) / self.DROP_DUR
        if u >= 0:
            b = bounce_out(u)
            py = lerp(-200, 1225, b)
            squash = 1.0
            for imp in (1 / 2.75, 2 / 2.75):
                k = (u - imp) / 0.08
                if 0 <= k <= 1:
                    squash = 1 - 0.18 * math.sin(math.pi * k)
            ctx.save()
            ctx.translate(540, 1300)
            ctx.scale(1, 0.15)
            circle(ctx, 0, 0, 40 + 120 * b, (0, 0, 0), 0.5 * b)
            ctx.restore()
            ctx.save()
            ctx.translate(540, py + 75)
            ctx.scale(2 - squash, squash)
            box(ctx, 0, -75, 210, 150, hexc("#C98B4E"), label="10 MIN")
            ctx.restore()
        # hearts once the door is open
        if o > 0.5:
            for k in range(12):
                age = (t - self.OPEN_T - 0.4 - k * 0.3)
                if 0 <= age < 1.8:
                    hx = 540 + 160 * math.sin(k * 2.1) + 30 * math.sin(age * 5 + k)
                    hy = 1150 - age * 380
                    s = 0.6 + 0.6 * rnd(k, 3)
                    self.heart(ctx, hx, hy, 40 * s, hexc("#FF4D6D"), 1 - age / 1.8)
        # CTA
        if t > self.cta_t(d):
            p = ease_out_back((t - self.cta_t(d)) / 0.4) * (1 + 0.05 * math.sin(t * 10))
            ctx.save()
            ctx.translate(540, 360)
            ctx.scale(p, p)
            rrect(ctx, -300, -60, 600, 120, 60)
            rgba(ctx, hexc("#FF2E4D"))
            ctx.fill()
            text(ctx, "FOLLOW FOR MORE", 0, 0, 62, (1, 1, 1), font=CAPTION_FONT)
            ctx.restore()

    @staticmethod
    def heart(ctx, x, y, s, c, a):
        ctx.save()
        ctx.translate(x, y)
        ctx.scale(s / 40, s / 40)
        ctx.move_to(0, 30)
        ctx.curve_to(-60, -10, -30, -55, 0, -25)
        ctx.curve_to(30, -55, 60, -10, 0, 30)
        rgba(ctx, c, a)
        ctx.fill()
        ctx.restore()


SCENE_CLASSES = {"clock": Clock, "warehouse": Warehouse, "packing": Packing, "rider": Rider, "door": Door}
