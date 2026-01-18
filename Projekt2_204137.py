import sys
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QTabWidget, QPushButton, QLabel,
                             QTextEdit, QGroupBox, QGridLayout, QSlider)
from PyQt5.QtCore import Qt, QTimer, QPointF, QRectF
from PyQt5.QtGui import QPainter, QColor, QPen, QPainterPath, QBrush, QFont, QPolygonF




class ElementProcesu:
    def draw(self, painter): pass


class Rura(ElementProcesu):
    def __init__(self, punkty, grubosc=8):
        self.punkty = [QPointF(float(p[0]), float(p[1])) for p in punkty]
        self.grubosc = grubosc
        self.plynie = False
        self.kolor_wody = QColor(200, 200, 200)

    def ustaw_stan(self, czy_plynie, temp_zrodla):
        self.plynie = czy_plynie
        if czy_plynie:
            t_val = max(20.0, min(100.0, temp_zrodla))
            factor = (t_val - 20) / 80.0
            r = int(255 * factor)
            b = int(255 * (1.0 - factor))
            self.kolor_wody = QColor(r, 0, b)
        else:
            self.kolor_wody = QColor(200, 200, 200)

    def draw(self, painter):
        if len(self.punkty) < 2: return
        path = QPainterPath()
        path.moveTo(self.punkty[0])
        for p in self.punkty[1:]: path.lineTo(p)

        painter.setPen(QPen(Qt.darkGray, self.grubosc + 2, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(path)

        kolor = self.kolor_wody if self.plynie else QColor(200, 200, 200)
        painter.setPen(QPen(kolor, self.grubosc - 2, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        painter.drawPath(path)


class Zawor(ElementProcesu):
    def __init__(self, x, y, nazwa=""):
        self.x = x
        self.y = y
        self.nazwa = nazwa
        self.otwarty = True

    def przelacz(self): self.otwarty = not self.otwarty

    def czy_kliknieto(self, mx, my): return abs(self.x - mx) < 20 and abs(self.y - my) < 20

    def draw(self, painter):
        kolor = Qt.green if self.otwarty else Qt.red
        painter.setPen(QPen(Qt.black, 1))
        painter.setBrush(QBrush(kolor))
        p1 = QPolygonF([QPointF(self.x - 15, self.y - 7), QPointF(self.x - 15, self.y + 7), QPointF(self.x, self.y)])
        p2 = QPolygonF([QPointF(self.x + 15, self.y - 7), QPointF(self.x + 15, self.y + 7), QPointF(self.x, self.y)])
        painter.drawPolygon(p1)
        painter.drawPolygon(p2)

        # Ośka
        painter.setBrush(Qt.NoBrush)
        painter.drawLine(int(self.x), int(self.y), int(self.x), int(self.y - 13))
        painter.drawEllipse(int(self.x - 5), int(self.y - 18), 10, 5)
        painter.setPen(Qt.black)
        painter.setFont(QFont("Arial", 7))
        painter.drawText(int(self.x - 10), int(self.y + 20), self.nazwa)


class Pompa(ElementProcesu):
    def __init__(self, x, y, r=20):
        self.x = x
        self.y = y
        self.r = r
        self.wlaczona = False
        self.kat = 0

    def przelacz(self, stan): self.wlaczona = stan

    def draw(self, painter):
        painter.setPen(QPen(Qt.black, 2))
        painter.setBrush(QBrush(Qt.gray))
        painter.drawEllipse(int(self.x - self.r), int(self.y - self.r), int(self.r * 2), int(self.r * 2))
        painter.save()
        painter.translate(self.x, self.y)
        k = Qt.green if self.wlaczona else Qt.red
        if self.wlaczona: self.kat = (self.kat + 15) % 360; painter.rotate(self.kat)
        painter.setBrush(QBrush(k))
        painter.drawRect(-5, int(-self.r + 4), 10, int(self.r * 2 - 8))
        painter.drawRect(int(-self.r + 4), -5, int(self.r * 2 - 8), 10)
        painter.restore()
        painter.setPen(Qt.black)
        painter.drawText(int(self.x - 15), int(self.y + self.r + 15), "POMPA")


class Grzalka(ElementProcesu):
    def __init__(self, x, y, width=40):
        self.x = x
        self.y = y
        self.wlaczona = False

    def draw(self, painter):
        k = QColor(255, 69, 0) if self.wlaczona else QColor(80, 80, 80)
        pen = QPen(k, 4)
        if self.wlaczona: pen.setStyle(Qt.DotLine)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        path = QPainterPath()
        path.moveTo(self.x, self.y)
        for i in range(1, 6): path.lineTo(self.x + (10 if i % 2 != 0 else 0), self.y + i * 5)
        painter.drawPath(path)


class Zbiornik(ElementProcesu):
    def __init__(self, x, y, pojemnosc=100, nazwa="Z1"):
        self.x = float(x)
        self.y = float(y)
        self.nazwa = nazwa
        self.width_top = 100.0
        self.width_bot = 80.0
        self.height = 120.0
        self.pojemnosc = float(pojemnosc)
        self.aktualna_ilosc = 0.0
        self.temperatura = 20.0
        self.grzalka = None
        self.byl_pelny = False

    def dodaj_grzalke(self):
        self.grzalka = Grzalka(self.x + self.width_bot / 2 - 20, self.y + self.height - 25)

    def czy_pelny(self): return self.aktualna_ilosc >= self.pojemnosc

    def poziom_procent(self): return max(0.0,
    min(1.0, self.aktualna_ilosc / self.pojemnosc if self.pojemnosc > 0 else 0))

    def draw(self, painter):
        path = QPainterPath()
        p1 = QPointF(self.x, self.y)
        p2 = QPointF(self.x + self.width_top, self.y)
        p3 = QPointF(self.x + (self.width_top + self.width_bot) / 2, self.y + self.height)
        p4 = QPointF(self.x + (self.width_top - self.width_bot) / 2, self.y + self.height)
        path.moveTo(p1)
        path.lineTo(p2)
        path.lineTo(p3)
        path.lineTo(p4)
        path.lineTo(p1)
        path.closeSubpath()

        h = self.height * self.poziom_procent()
        painter.save()
        painter.setClipPath(path)


        t_factor = (max(20.0, min(100.0, self.temperatura)) - 20.0) / 80.0
        c_r = int(255 * t_factor)
        c_b = int(255 * (1.0 - t_factor))
        c = QColor(c_r, 50, c_b, 180)
        painter.fillRect(QRectF(self.x, self.y + self.height - h, self.width_top, h), c)

        painter.restore()
        painter.setPen(QPen(Qt.black, 3))
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(path)
        if self.grzalka:
            self.grzalka.wlaczona = (self.temperatura > 50)
            self.grzalka.draw(painter)
        painter.setPen(Qt.black)
        painter.setFont(QFont("Arial", 8))
        painter.drawText(int(self.x), int(self.y - 30),
                         f"{self.nazwa}\n{self.aktualna_ilosc:.0f}L\n{self.temperatura:.0f}°C")


class EkranWizualizacji(QWidget):
    def __init__(self, log_callback):
        super().__init__()
        self.log_callback = log_callback
        self.setMinimumSize(800, 500)
        self.setStyleSheet("background-color: #F0F0F0;")


        self.z1 = Zbiornik(50, 50, 150, "Z1 (0%)")
        self.z1.aktualna_ilosc = 150.0
        self.z2 = Zbiornik(250, 150, 100, "Z2 (10%)")
        self.z3 = Zbiornik(450, 250, 100, "Z3 (70%)")
        self.z4 = Zbiornik(650, 350, 100, "Z4 (0%)")
        self.zbiorniki = [self.z1, self.z2, self.z3, self.z4]
        for z in self.zbiorniki: z.dodaj_grzalke()

        self.pompa = Pompa(750, 320)


        self.h_rura1 = 0.0
        self.h_rura2 = 0.1
        self.h_rura3 = 0.7
        self.h_rura4 = 0.0


        self.rura1 = Rura([(100, 170), (100, 150), (250, 150)])
        y_r2 = 150 + 120 - (120 * self.h_rura2)
        self.rura2 = Rura([(300, y_r2), (320, y_r2), (320, 250), (450, 250)])
        y_r3 = 250 + 120 - (120 * self.h_rura3)
        self.rura3 = Rura([(500, y_r3), (520, y_r3), (520, 350), (650, 350)])
        self.rura_powrot = Rura([(700, 470), (750, 470), (750, 50), (100, 50)], 6)
        self.rury = [self.rura1, self.rura2, self.rura3, self.rura_powrot]


        self.v1 = Zawor(180, 150, "V1")
        self.v2 = Zawor(380, 250, "V2")
        self.v3 = Zawor(580, 350, "V3")
        self.v4 = Zawor(750, 100, "V4")
        self.zawory = [self.v1, self.v2, self.v3, self.v4]

        self.timer = QTimer()
        self.timer.timeout.connect(self.aktualizuj_fizyke)
        self.running = False

    def toggle_symulacja(self):
        if self.running:
            self.timer.stop()
        else:
            self.timer.start(50)
        self.running = not self.running

    def mousePressEvent(self, event):
        x = event.x()
        y = event.y()
        zmiana = False
        for v in self.zawory:
            if v.czy_kliknieto(x, y):
                v.przelacz()
                self.log_callback(f"Zawór {v.nazwa}: {'OTWARTY' if v.otwarty else 'ZAMKNIĘTY'}")
                zmiana = True
        if zmiana: self.update()

    def ustaw_poziom_suwak(self, idx, proc):
        self.zbiorniki[idx].aktualna_ilosc = (proc / 100.0) * self.zbiorniki[idx].pojemnosc
        self.update()

    def ustaw_temp_suwak(self, idx, val):
        self.zbiorniki[idx].temperatura = float(val)
        self.update()

    def aktualizuj_fizyke(self):
        flow = 1.0
        d_z1 = 0.0
        d_z2 = 0.0
        d_z3 = 0.0
        d_z4 = 0.0


        if self.z1.poziom_procent() > self.h_rura1 and self.v1.otwarty:
            if self.z2.aktualna_ilosc < self.z2.pojemnosc:
                ilosc = min(self.z1.aktualna_ilosc, flow)
                d_z1 -= ilosc
                d_z2 += ilosc
                self.rura1.ustaw_stan(True, self.z1.temperatura)
            else:
                self.rura1.ustaw_stan(False, 20)
        else:
            self.rura1.ustaw_stan(False, 20)


        if self.z2.poziom_procent() > self.h_rura2 and self.v2.otwarty:
            if self.z3.aktualna_ilosc < self.z3.pojemnosc:
                dostepna_woda = self.z2.aktualna_ilosc - (self.z2.pojemnosc * self.h_rura2)
                ilosc = min(dostepna_woda, flow)
                if ilosc > 0:
                    d_z2 -= ilosc
                    d_z3 += ilosc
                    self.rura2.ustaw_stan(True, self.z2.temperatura)
                else:
                    self.rura2.ustaw_stan(False, 20)
            else:
                self.rura2.ustaw_stan(False, 20)
        else:
            self.rura2.ustaw_stan(False, 20)

        if self.z3.poziom_procent() > self.h_rura3 and self.v3.otwarty:
            if self.z4.aktualna_ilosc < self.z4.pojemnosc:
                dostepna_woda = self.z3.aktualna_ilosc - (self.z3.pojemnosc * self.h_rura3)
                ilosc = min(dostepna_woda, flow)
                if ilosc > 0:
                    d_z3 -= ilosc
                    d_z4 += ilosc
                    self.rura3.ustaw_stan(True, self.z3.temperatura)
                else:
                    self.rura3.ustaw_stan(False, 20)
            else:
                self.rura3.ustaw_stan(False, 20)
        else:
            self.rura3.ustaw_stan(False, 20)

        if self.z4.aktualna_ilosc > 50:
            self.pompa.przelacz(True)
        elif self.z4.aktualna_ilosc < 5:
            self.pompa.przelacz(False)

        if self.pompa.wlaczona and self.z4.poziom_procent() > self.h_rura4 and self.v4.otwarty:
            if self.z1.aktualna_ilosc < self.z1.pojemnosc:
                ilosc = min(self.z4.aktualna_ilosc, 1.5)
                d_z4 -= ilosc
                d_z1 += ilosc
                self.rura_powrot.ustaw_stan(True, self.z4.temperatura)
            else:
                self.rura_powrot.ustaw_stan(False, 20)
        else:
            self.rura_powrot.ustaw_stan(False, 20)

        self.z1.aktualna_ilosc += d_z1
        self.z2.aktualna_ilosc += d_z2
        self.z3.aktualna_ilosc += d_z3
        self.z4.aktualna_ilosc += d_z4

        for z in self.zbiorniki:
            z.aktualna_ilosc = max(0.0, min(z.aktualna_ilosc, z.pojemnosc))

        self.sprawdz_alerty()
        self.update()

    def sprawdz_alerty(self):
        for z in self.zbiorniki:
            if z.czy_pelny() and not z.byl_pelny:
                self.log_callback(f"ALERT: {z.nazwa} pełny!")
                z.byl_pelny = True
            elif not z.czy_pelny():
                z.byl_pelny = False

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        for r in self.rury: r.draw(p)
        for z in self.zbiorniki: z.draw(p)
        self.pompa.draw(p)
        for v in self.zawory: v.draw(p)



class GlowneOkno(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Projekt SCADA")
        self.resize(1100, 900)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        self.logs = QTextEdit()
        self.logs.setReadOnly(True)
        self.logs.setStyleSheet("background:#222;color:#0F0")
        self.wiz = EkranWizualizacji(self.log)

        w_inst = QWidget()
        l_inst = QVBoxLayout(w_inst)
        l_inst.addWidget(self.wiz)
        grp = QGroupBox("Panel Sterowania")
        l_grp = QHBoxLayout()

        self.btn = QPushButton("START/STOP")
        self.btn.setCheckable(True)
        self.btn.setFixedSize(100, 80)
        self.btn.clicked.connect(self.proc)
        l_grp.addWidget(self.btn)

        self.suwaki_poziom = []
        g_z = QGridLayout()
        for i, z in enumerate(self.wiz.zbiorniki):
            g_z.addWidget(QLabel(f"<b>{z.nazwa}</b>"), 0, i, alignment=Qt.AlignCenter)
            g_z.addWidget(QLabel("Poziom:"), 1, i)
            s_lev = QSlider(Qt.Horizontal)
            s_lev.setRange(0, 100)
            s_lev.setValue(int(z.poziom_procent() * 100))
            s_lev.valueChanged.connect(lambda v, x=i: self.wiz.ustaw_poziom_suwak(x, v))
            self.suwaki_poziom.append(s_lev)
            g_z.addWidget(s_lev, 2, i)

            g_z.addWidget(QLabel("Temperatura:"), 3, i)
            s_temp = QSlider(Qt.Horizontal)
            s_temp.setRange(20, 100)
            s_temp.setValue(20)
            s_temp.setStyleSheet("""
                QSlider::groove:horizontal {
                    height: 8px;
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0000FF, stop:1 #FF0000);
                    border-radius: 4px;
                }
                QSlider::handle:horizontal {
                    background: white;
                    width: 14px;
                    margin: -4px 0;
                    border-radius: 7px;
                    border: 1px solid gray;
                }
            """)
            s_temp.valueChanged.connect(lambda v, x=i: self.wiz.ustaw_temp_suwak(x, v))
            g_z.addWidget(s_temp, 4, i)

        c_g = QWidget()
        c_g.setLayout(g_z)
        l_grp.addWidget(c_g)
        grp.setLayout(l_grp)
        l_inst.addWidget(grp)
        self.tabs.addTab(w_inst, "Instalacja")
        self.tabs.addTab(self.logs, "Logi")
        self.ui_timer = QTimer()
        self.ui_timer.timeout.connect(self.ui_update)
        self.ui_timer.start(200)

    def ui_update(self):
        for i, s in enumerate(self.suwaki_poziom):
            s.blockSignals(True)
            s.setValue(int(self.wiz.zbiorniki[i].poziom_procent() * 100))
            s.blockSignals(False)

    def proc(self):
        self.wiz.toggle_symulacja(); self.log("Przełączono stan")

    def log(self, t):
        self.logs.append(f"[{datetime.now().strftime('%H:%M:%S')}] {t}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = GlowneOkno()
    w.show()
    sys.exit(app.exec_())