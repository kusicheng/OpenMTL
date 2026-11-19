"""The quiet starting point before a translation workflow is selected."""

import random

from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtWidgets import QHBoxLayout, QPushButton, QVBoxLayout, QWidget

from ..widgets import BirdMark, Icon, icon_button, label


GREETINGS = (
    "What are we envisioning today, {name}?",
    "It's good to see you{again}, {name}.",
    "What are we drawing today, {name}?",
    "Duobird is waiting, {name}.",
    "Where will words take you today, {name}?",
)


class ActionCard(QPushButton):
    def __init__(self, icon, title, description, parent=None):
        super().__init__(parent)
        self.setObjectName("actionCard")
        self.setMinimumSize(198, 174)
        self.setMaximumWidth(264)
        self.setAccessibleName(title)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        content = QVBoxLayout(self)
        content.setContentsMargins(22, 22, 22, 20)
        content.setSpacing(9)
        top = QHBoxLayout()
        top.addWidget(Icon(icon, 25, "#444444"))
        top.addStretch()
        top.addWidget(Icon("arrow_right", 17, "#aaaaaa"))
        content.addLayout(top)
        content.addSpacing(9)
        content.addWidget(label(title, "section"))
        detail = label(description, "muted")
        detail.setMinimumHeight(35)
        content.addWidget(detail)
        for widget in self.findChildren(QWidget):
            widget.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)


class HomePage(QWidget):
    navigate = pyqtSignal(str)

    def __init__(self, preferences, parent=None):
        super().__init__(parent)
        self.preferences = preferences
        self.greeting_index = 1 if preferences.returning_after_absence else random.randrange(len(GREETINGS))
        self.setMinimumHeight(620)
        outer = QVBoxLayout(self)
        outer.setContentsMargins(30, 38, 30, 22)
        outer.addStretch(3)

        content = QWidget()
        content.setMinimumWidth(760)
        content.setMaximumWidth(810)
        hero = QVBoxLayout(content)
        hero.setContentsMargins(0, 0, 0, 0)
        hero.setSpacing(0)
        hero.addWidget(BirdMark(82), 0, Qt.AlignmentFlag.AlignHCenter)
        hero.addSpacing(24)
        eyebrow = label("A LITTLE UNDERSTANDING GOES A LONG WAY", "eyebrow")
        eyebrow.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hero.addWidget(eyebrow)
        hero.addSpacing(15)
        self.greeting = label("", "greeting")
        self.greeting.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.greeting.setMinimumHeight(104)
        hero.addWidget(self.greeting)
        hero.addSpacing(11)
        subtitle = label("Your words. A world of possibilities.\nChoose a place to begin.", "subtitle")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hero.addWidget(subtitle)
        hero.addSpacing(34)

        cards = QHBoxLayout()
        cards.setSpacing(14)
        cards.addStretch()
        for scene, icon, title, description in (
            ("auto", "sparkles", "Auto translate", "Drop in your files.\nLet us take it from there."),
            ("edit", "edit", "Translate and edit", "Make every word\nfeel like your own."),
            ("settings", "settings", "Settings", "A few small details.\nA space that feels like you."),
        ):
            card = ActionCard(icon, title, description)
            card.clicked.connect(lambda checked=False, target=scene: self.navigate.emit(target))
            cards.addWidget(card, 1)
        cards.addStretch()
        hero.addLayout(cards)
        hero.addSpacing(20)
        hint = QHBoxLayout()
        hint.addStretch()
        hint_text = label("A fresh thought, whenever you need one", "small")
        hint_text.setWordWrap(False)
        hint.addWidget(hint_text)
        shuffle = icon_button("refresh", "Show another greeting")
        shuffle.clicked.connect(self.next_greeting)
        hint.addWidget(shuffle)
        hint.addStretch()
        hero.addLayout(hint)
        outer.addWidget(content, 0, Qt.AlignmentFlag.AlignHCenter)
        outer.addStretch(4)
        footer = label("MADE FOR THE EVERYDAY. OPEN TO EVERYONE.", "eyebrow")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        outer.addWidget(footer)

        self.preferences.changed.connect(self.refresh_greeting)
        self.rotation = QTimer(self)
        self.rotation.setInterval(30000)
        self.rotation.timeout.connect(self._rotate_if_visible)
        self.rotation.start()
        self.refresh_greeting()

    def refresh_greeting(self):
        self.greeting.setText(GREETINGS[self.greeting_index].format(
            name=self.preferences.name,
            again=" again" if self.preferences.returning_after_absence else "",
        ))

    def next_greeting(self):
        self.greeting_index = (self.greeting_index + 1) % len(GREETINGS)
        self.refresh_greeting()
        self.rotation.start()

    def _rotate_if_visible(self):
        if self.isVisible():
            self.next_greeting()
