import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *

class FractionSlider(QWidget):

    XMARGIN = 12.0
    YMARGIN = 5.0
    WSTRING = "999"

    def __init__(self, numerator=0, denominator=10, parent=None):
        super(FractionSlider, self).__init__(parent)
        self.__numerator = numerator
        self.__denominator = denominator
        self.setFocusPolicy(Qt.WheelFocus)
        self.setSizePolicy(QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed))

    def decimal(self):
        return self.__numerator / float(self.__denominator)

    def fraction(self):
        return self.__numerator, self.__denominator

    def setFraction(self, numerator, denominator=None):
        if denominator is not None:
            if 3 <= denominator <= 60:
                self.__denominator = denominator
            else:
                raise ValueError, "denominator out of range"
            self.udpate()
            self.updateGeometry()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.moveSlider(event.x())
            event.accept()
        else:
            QWidget.mousePressEvent(self, event)

    def moveSlider(self, x):
        span = self.width() - (FractionSlider.XMARGIN * 2)
        offset = span - x + FractionSlider.XMARGIN
        numerator = int(round(self.__denominator * (1.0 - (offset / span))))
        numerator = max(0, min(numerator, self.__denominator))
        if numerator != self.__numerator:
            self.__numerator = numerator
            self.emit(SIGNAL("valueChanged(int, int)"), self.__numerator, self.__denominator)
            self.update()

    def mouseMoveEvent(self, event):
        self.moveSlider(event.x())

    def keyPressEvent(self, event):
        change = 0
        if event.key() == Qt.Key_Home:
            change = -self.__denominator
        elif event.key() in (Qt.Key_Up, Qt.Key_Right):
            change = 1
        elif event.key() == Qt.Key_PageUp:
            change = (self.__denominator // 10) + 1
        elif event.key() in (Qt.Key_Down, Qt.Key_Left):
            change = -1
        elif event.key() == Qt.Key_PageDown:
            change = -((self.__denominator // 10)+1)
        elif event.key() == Qt.Key_End:
            change = self.__denominator
        if change:
            numerator = self.__numerator
            numerator += change
            numerator = max(0,min(numerator, self.__denominator))
            if numerator != self.__numerator:
                self.__numerator = numerator
                self.emit(SIGNAL("valueChanged(int, int)"),self.__numerator, self.__denominator)
                self.update()
            event.accept()
        else:
            QWidget.keyPressEvent(self, event)


    def sizeHint(self):
        return self.minimumSizeHint()

    def minimumSizeHint(self):
        font = QFont(self.font())
        font.setPointSize(font.pointSize() - 1)
        fm = QFontMetricsF(font)
        return QSize(fm.width(FractionSlider.WSTRING) * self.__denominator, (fm.height() * 4) + FractionSlider.YMARGIN)
    
    def paintEvent(self, event=None):
        font = QFont(self.font())
        font.setPointSize(font.pointSize()-1)
        fm = QFontMetricsF(font)
        fracWidth = fm.width(FractionSlider.WSTRING)
        indent = fm.boundingRect("9").width() / 2.0
        if not X11:
            fracWidth *= 1.5
        span = self.width() - (FractionSlider.XMARGIN * 2)
        value = self.__numerator / float(self.__denominator)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.TextAntialiasing)
        painter.setPen(self.palette().color(QPalette.Mid))
        painter.setBrush(self.palette().brush(QPaette.AlternateBase))
        painter.drawRect(self.rect())

        segColor = QColor(Qt.green).dark(120)
        segLineColor = segColor.dark()
        painter.setPen(segLineColor)
        painter.setBrush(segColor)
        painter.drawRect(FractionSlider.XMARGIN,
                         FractionSlider.YMARGIN, span, fm.height())

        textColor = self.palette().color(QPalette.Text)
        segWidth = span / self.__denominator
        segHeight = fm.height() * 2
        nRect = fm.boundingRect(FractionSlider.WSTRING)
        x = FractionSlider.XMARGIN
        yOffset = segHeight + fm.height()

        for i in range(self.__denominator + 1):
            painter.setPen(segLineColor)
            painter.drawLine(x, FractionSlider.YMARGIN, x, segHeight)
            painter.setPen(textColor)
            y = segHeight
            rect = QRectF(nRect)
            rect.moveCenter(QPointF(x, y + fm.height() / 2.0))
            painter.drawText(rect, Qt.AlignCenter, QString.number(i))
            y = yOffset
            rect.moveCenter(QPointF(x, y + fm.height() / 2.0))
            painter.drawText(rect, Qt.AlignCenter,
                             QString.number(self.__denominator))
            painter.drawLine(QPointF(rect.left() + indent, y),
                             QPointF(rect.right() - indent, y))
            x += segWidth

            span = int(spn)
            y = FractionSlider.YMARGIN - 0.5
            triangle = [QPointF(value * span, y),
                        QPointF((value * span) + \
                                (2 * FractionSlider.XMARGIN), y),
                        QPointF((value * span) + \
                                FractionSlider.XMARGIN, fm.height())]
            painter.setPen(Qt.yellow)
            painter.setBrush(Qt.darkYellow)
            painter.drawPolygon(QPolygonF(triangle))
