"""Application shell and scene navigation for the OpenMTL prototype."""

import sys

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QColor, QIcon, QKeySequence, QPalette, QPixmap, QShortcut
from PyQt6.QtWidgets import (
    QApplication, QFrame, QHBoxLayout, QMainWindow, QPushButton, QScrollArea,
    QStackedWidget, QVBoxLayout, QWidget,
)

from . import __version__
from .pages.home import HomePage
from .pages.settings import SettingsPage
from .pages.translate import TranslationPage
from .preferences import Preferences
from .theme import STYLESHEET
from .widgets import BirdMark, GridBackground, Icon, label


SCENES = (
    ("home", "home", "Home"),
    ("auto", "sparkles", "Auto translate"),
    ("edit", "edit", "Translate and edit"),
    ("settings", "settings", "Settings"),
)


class MainWindow(QMainWindow):
    def __init__(self, preferences=None):
        super().__init__()
        self.preferences = preferences if preferences is not None else Preferences(parent=self)
        self.setWindowTitle("OpenMTL: the free translator for everyday use")
        self.resize(1280, 840)
        self.setMinimumSize(1060, 720)
        mark = BirdMark(80)
        pixmap = QPixmap(mark.size())
        pixmap.fill(Qt.GlobalColor.transparent)
        mark.render(pixmap)
        self.setWindowIcon(QIcon(pixmap))

        root = QWidget()
        layout = QHBoxLayout(root)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setCentralWidget(root)
        self.nav_buttons = {}
        layout.addWidget(self._sidebar())

        workspace = QWidget()
        workspace_layout = QVBoxLayout(workspace)
        workspace_layout.setContentsMargins(0, 0, 0, 0)
        workspace_layout.setSpacing(0)
        workspace_layout.addWidget(self._topbar())
        background = GridBackground()
        background_layout = QVBoxLayout(background)
        background_layout.setContentsMargins(0, 0, 0, 0)
        self.stack = QStackedWidget()
        background_layout.addWidget(self.stack)
        workspace_layout.addWidget(background, 1)
        layout.addWidget(workspace, 1)

        self.pages = {
            "home": HomePage(self.preferences),
            "auto": TranslationPage("auto", self.preferences),
            "edit": TranslationPage("edit", self.preferences),
            "settings": SettingsPage(self.preferences),
        }
        self.pages["home"].navigate.connect(self.navigate)
        self.scene_indices = {}
        for name, page in self.pages.items():
            scroll = QScrollArea()
            scroll.setWidgetResizable(True)
            scroll.setFrameShape(QFrame.Shape.NoFrame)
            scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            scroll.viewport().setAutoFillBackground(False)
            scroll.setWidget(page)
            page.setAutoFillBackground(False)
            self.scene_indices[name] = self.stack.addWidget(scroll)
        self.preferences.changed.connect(self._refresh_profile)
        self._shortcuts = []
        for key, scene in (("Ctrl+1", "home"), ("Ctrl+2", "auto"),
                           ("Ctrl+3", "edit"), ("Ctrl+,", "settings")):
            shortcut = QShortcut(QKeySequence(key), self)
            shortcut.activated.connect(lambda target=scene: self.navigate(target))
            self._shortcuts.append(shortcut)
        self.navigate("home")
        self.preferences.mark_used()

    def _sidebar(self):
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(220)
        content = QVBoxLayout(sidebar)
        content.setContentsMargins(19, 28, 19, 22)
        content.setSpacing(6)
        branding = QHBoxLayout()
        branding.setSpacing(11)
        branding.addWidget(BirdMark(39))
        words = QVBoxLayout()
        words.setSpacing(0)
        name = label("OpenMTL", "section")
        name.setStyleSheet("font-size: 20px; font-weight: 650; letter-spacing: -0.7px;")
        words.addWidget(name)
        words.addWidget(label("The free translator.", "small"))
        branding.addLayout(words)
        branding.addStretch()
        content.addLayout(branding)
        content.addSpacing(46)
        content.addWidget(label("YOUR WORKSPACE", "eyebrow"))
        content.addSpacing(8)
        for scene, icon, title in SCENES:
            if scene == "settings":
                continue
            button = self._nav_button(scene, icon, title)
            content.addWidget(button)
        content.addStretch()

        note = QFrame()
        note.setProperty("surface", "inset")
        note_layout = QVBoxLayout(note)
        note_layout.setContentsMargins(14, 14, 14, 14)
        note_layout.setSpacing(6)
        note_layout.addWidget(Icon("globe", 21, "#666666"))
        note_layout.addWidget(label("Less distance.\nMore understanding.", "body"))
        note_layout.addWidget(label("Free for your everyday.", "small"))
        content.addWidget(note)
        content.addSpacing(18)
        content.addWidget(self._nav_button("settings", "settings", "Settings"))
        content.addSpacing(12)

        profile = QHBoxLayout()
        self.avatar = label("", "body")
        self.avatar.setFixedSize(33, 33)
        self.avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.avatar.setStyleSheet("background: #e7e7e7; border-radius: 16px; font-weight: 600;")
        profile.addWidget(self.avatar)
        identity = QVBoxLayout()
        identity.setSpacing(1)
        self.profile_name = label("", "body")
        self.profile_name.setMaximumWidth(130)
        identity.addWidget(self.profile_name)
        identity.addWidget(label("Your local workspace", "small"))
        profile.addLayout(identity, 1)
        content.addLayout(profile)
        content.addSpacing(13)
        content.addWidget(label(f"OpenMTL  /  v{__version__}", "small"))
        self._refresh_profile()
        return sidebar

    def _nav_button(self, scene, icon, title):
        button = QPushButton("  " + title)
        button.setObjectName("navButton")
        button.setCheckable(True)
        button.setMinimumHeight(43)
        button.setIcon(Icon(icon, color="#666666").as_icon())
        button.setIconSize(QSize(18, 18))
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.clicked.connect(lambda checked=False: self.navigate(scene))
        self.nav_buttons[scene] = button
        return button

    def _topbar(self):
        topbar = QFrame()
        topbar.setObjectName("topbar")
        topbar.setFixedHeight(71)
        content = QHBoxLayout(topbar)
        content.setContentsMargins(35, 0, 35, 0)
        content.setSpacing(13)
        content.addWidget(label("Workspace", "muted"))
        content.addWidget(label("/", "small"))
        self.scene_title = label("Home", "body")
        content.addWidget(self.scene_title)
        content.addStretch()
        badge = label("●   PROTOTYPE", "small")
        badge.setFixedHeight(25)
        badge.setWordWrap(False)
        badge.setStyleSheet(
            "background: #eeeeee; border: 1px solid #e2e2e2; border-radius: 11px;"
            "padding: 4px 10px; font-size: 9px; letter-spacing: 1px; color: #777777;"
        )
        content.addWidget(badge)
        return topbar

    def _refresh_profile(self):
        self.profile_name.setText(self.profile_name.fontMetrics().elidedText(
            self.preferences.name, Qt.TextElideMode.ElideRight, 130,
        ))
        self.profile_name.setToolTip(self.preferences.name)
        self.avatar.setText(self.preferences.name[:1].upper())

    def navigate(self, scene):
        if scene not in self.pages:
            return
        self.stack.setCurrentIndex(self.scene_indices[scene])
        for name, button in self.nav_buttons.items():
            button.setChecked(name == scene)
        self.scene_title.setText(dict((name, title) for name, _, title in SCENES)[scene])

    def closeEvent(self, event):
        self.preferences.mark_used()
        super().closeEvent(event)


def create_application(argv=None):
    application = QApplication(sys.argv if argv is None else argv)
    application.setApplicationName("OpenMTL")
    application.setOrganizationName("OpenMTL")
    application.setApplicationVersion(__version__)
    application.setStyle("Fusion")
    palette = application.palette()
    for role, color in (
        (QPalette.ColorRole.Window, "#f7f7f7"),
        (QPalette.ColorRole.WindowText, "#222222"),
        (QPalette.ColorRole.Base, "#ffffff"),
        (QPalette.ColorRole.Text, "#222222"),
        (QPalette.ColorRole.Button, "#ffffff"),
        (QPalette.ColorRole.ButtonText, "#222222"),
        (QPalette.ColorRole.Highlight, "#dddddd"),
        (QPalette.ColorRole.HighlightedText, "#222222"),
    ):
        palette.setColor(role, QColor(color))
    application.setPalette(palette)
    application.setStyleSheet(STYLESHEET)
    return application


def main():
    application = create_application()
    window = MainWindow()
    window.show()
    return application.exec()
