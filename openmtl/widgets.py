"""Small vector illustrations and reusable desktop controls."""

from PyQt6.QtCore import QByteArray, QPointF, QRectF, Qt
from PyQt6.QtGui import (
    QColor, QIcon, QPainter, QPainterPath, QPen, QPixmap, QRadialGradient,
)
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtWidgets import QLabel, QPushButton, QWidget


_PATHS = {
    "home": '<path d="m3 10 9-7 9 7v10a1 1 0 0 1-1 1h-5v-7H9v7H4a1 1 0 0 1-1-1z"/>',
    "arrow_right": '<path d="M5 12h14m-6-6 6 6-6 6"/>',
    "arrow_left": '<path d="M19 12H5m6-6-6 6 6 6"/>',
    "upload": '<path d="M12 16V3m-5 5 5-5 5 5M4 15v5h16v-5"/>',
    "file": '<path d="M14 3H5v18h14V8zm0 0v5h5M8 13h8m-8 4h5"/>',
    "sparkles": '<path d="m12 3 2.5 6.5L21 12l-6.5 2.5L12 21l-2.5-6.5L3 12l6.5-2.5zM20 2v4m-2-2h4"/>',
    "edit": '<path d="m15 5 4 4M4 20l5-1L21 7a2.8 2.8 0 0 0-4-4L5 15z"/>',
    "settings": '<path d="m10 3-.8 2.3-2.1 1L4.8 6 3 9l1.4 1.8v2.4L3 15l1.8 3 2.3-.3 2.1 1L10 21h4l.8-2.3 2.1-1 2.3.3 1.8-3-1.4-1.8v-2.4L21 9l-1.8-3-2.3.3-2.1-1L14 3z"/><circle cx="12" cy="12" r="3"/>',
    "check": '<path d="m5 12 4 4L19 6"/>',
    "chevron_down": '<path d="m6 9 6 6 6-6"/>',
    "copy": '<rect x="8" y="8" width="12" height="13" rx="2"/><path d="M16 8V3H3v13h5"/>',
    "close": '<path d="m6 6 12 12M6 18 18 6"/>',
    "swap": '<path d="M4 7h16m-4-4 4 4-4 4M20 17H4m4-4-4 4 4 4"/>',
    "plus": '<path d="M12 4v16M4 12h16"/>',
    "refresh": '<path d="M20 10a8 8 0 1 0-1 7M20 4v6h-6"/>',
    "globe": '<circle cx="12" cy="12" r="9"/><ellipse cx="12" cy="12" rx="4" ry="9"/><path d="M3 12h18"/>',
}


class Icon(QWidget):
    def __init__(self, name, size=20, color="#707070", parent=None):
        super().__init__(parent)
        paths = _PATHS.get(name, _PATHS["globe"])
        svg = (
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" '
            f'fill="none" stroke="{color}" stroke-width="1.5" '
            f'stroke-linecap="round" stroke-linejoin="round">{paths}</svg>'
        )
        self.renderer = QSvgRenderer(QByteArray(svg.encode()), self)
        self.setFixedSize(size, size)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.renderer.render(painter)

    def as_icon(self):
        pixmap = QPixmap(48, 48)
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        self.renderer.render(painter)
        painter.end()
        return QIcon(pixmap)


def icon_button(name, tooltip, parent=None):
    button = QPushButton(parent)
    button.setProperty("kind", "ghost")
    button.setIcon(Icon(name).as_icon())
    button.setFixedSize(34, 34)
    button.setToolTip(tooltip)
    button.setAccessibleName(tooltip)
    button.setCursor(Qt.CursorShape.PointingHandCursor)
    return button


def label(text, role="body", parent=None):
    widget = QLabel(text, parent)
    widget.setProperty("role", role)
    widget.setWordWrap(True)
    widget.setTextFormat(Qt.TextFormat.PlainText)
    return widget


class BirdMark(QWidget):
    """Duobird: a tiny, entirely grayscale bird drawn at any display scale."""

    def __init__(self, size=72, parent=None):
        super().__init__(parent)
        self.setFixedSize(size, size)
        self.setAccessibleName("Duobird")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.scale(self.width() / 80, self.height() / 80)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor("#eeeeee"))
        painter.drawRoundedRect(QRectF(1, 1, 78, 78), 23, 23)
        body = QPainterPath()
        body.moveTo(19, 47)
        body.cubicTo(16, 24, 33, 16, 45, 25)
        body.cubicTo(61, 19, 68, 34, 62, 48)
        body.cubicTo(58, 65, 29, 69, 19, 47)
        painter.setBrush(QColor("#333333"))
        painter.drawPath(body)
        painter.setBrush(QColor("#f8f8f8"))
        painter.drawEllipse(QRectF(28, 31, 14, 18))
        painter.drawEllipse(QRectF(44, 31, 14, 18))
        painter.setBrush(QColor("#333333"))
        painter.drawEllipse(QRectF(35, 37, 4, 6))
        painter.drawEllipse(QRectF(48, 37, 4, 6))
        beak = QPainterPath()
        beak.moveTo(40, 48)
        beak.lineTo(47, 48)
        beak.lineTo(43.5, 53)
        beak.closeSubpath()
        painter.setBrush(QColor("#b0b0b0"))
        painter.drawPath(beak)
        painter.setPen(QPen(QColor("#888888"), 2.4, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
        painter.drawLine(QPointF(32, 64), QPointF(30, 68))
        painter.drawLine(QPointF(49, 64), QPointF(51, 68))


class GridBackground(QWidget):
    """Graph paper with a radial alpha mask that fades into the page edges."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._grid = None

    def resizeEvent(self, event):
        self._grid = None
        super().resizeEvent(event)

    def _make_grid(self):
        ratio = self.devicePixelRatioF()
        pixmap = QPixmap(round(self.width() * ratio), round(self.height() * ratio))
        pixmap.setDevicePixelRatio(ratio)
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        painter.setPen(QPen(QColor("#d7d7d7"), 0.7))
        spacing = 32
        for x in range(self.width() % spacing // 2, self.width(), spacing):
            painter.drawLine(x, 0, x, self.height())
        for y in range(0, self.height(), spacing):
            painter.drawLine(0, y, self.width(), y)
        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_DestinationIn)
        mask = QRadialGradient(
            QPointF(self.width() * .5, self.height() * .46),
            max(self.width() * .57, self.height() * .75),
        )
        mask.setColorAt(0, QColor(0, 0, 0, 175))
        mask.setColorAt(.45, QColor(0, 0, 0, 110))
        mask.setColorAt(1, QColor(0, 0, 0, 0))
        painter.fillRect(self.rect(), mask)
        painter.end()
        return pixmap

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor("#f7f7f7"))
        if self._grid is None:
            self._grid = self._make_grid()
        painter.drawPixmap(0, 0, self._grid)
