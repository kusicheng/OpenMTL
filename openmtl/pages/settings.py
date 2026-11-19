"""Local preferences for the desktop prototype."""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QCheckBox, QComboBox, QFormLayout, QFrame, QHBoxLayout, QLineEdit,
    QPushButton, QVBoxLayout, QWidget,
)

from openmtl.preferences import LANGUAGES
from openmtl.widgets import Icon, label


class SettingsPage(QWidget):
    def __init__(self, preferences, parent=None):
        super().__init__(parent)
        self.preferences = preferences
        self._dirty = False
        layout = QVBoxLayout(self)
        layout.setContentsMargins(44, 30, 44, 26)
        layout.setSpacing(18)
        layout.addWidget(label("MAKE YOURSELF AT HOME", "eyebrow"))
        layout.addWidget(label("A little more you.", "title"))
        layout.addWidget(label("Small preferences for your everyday translations.", "subtitle"))
        layout.addSpacing(6)

        profile = QFrame()
        profile.setProperty("surface", "card")
        profile_layout = QVBoxLayout(profile)
        profile_layout.setContentsMargins(24, 22, 24, 22)
        profile_layout.setSpacing(16)
        profile_layout.addWidget(label("The personal touches", "section"))
        profile_layout.addWidget(label("Tell us what to call you on the home screen.", "muted"))
        name_form = QFormLayout()
        name_form.setSpacing(14)
        self.name_edit = QLineEdit()
        self.name_edit.setMaxLength(40)
        self.name_edit.setPlaceholderText("Your name")
        self.name_edit.setAccessibleName("Display name")
        name_form.addRow("Display name", self.name_edit)
        profile_layout.addLayout(name_form)
        layout.addWidget(profile)

        languages = QFrame()
        languages.setProperty("surface", "card")
        languages_layout = QVBoxLayout(languages)
        languages_layout.setContentsMargins(24, 22, 24, 22)
        languages_layout.setSpacing(16)
        languages_layout.addWidget(label("Your language pair", "section"))
        fields = QHBoxLayout()
        fields.setSpacing(24)
        self.source_language = QComboBox()
        self.source_language.addItems(LANGUAGES)
        self.source_language.setAccessibleName("Default source language")
        self.target_language = QComboBox()
        self.target_language.addItems([item for item in LANGUAGES if item != "Auto-detect"])
        self.target_language.setAccessibleName("Default target language")
        for caption, field in (("DEFAULT SOURCE", self.source_language), ("DEFAULT TARGET", self.target_language)):
            column = QVBoxLayout()
            column.setSpacing(8)
            column.addWidget(label(caption, "eyebrow"))
            column.addWidget(field)
            fields.addLayout(column, 1)
        languages_layout.addLayout(fields)
        self.remember_languages = QCheckBox("Remember my last language pair")
        self.remember_languages.setToolTip("Update the default language pair when a workspace selection changes.")
        languages_layout.addWidget(self.remember_languages)
        layout.addWidget(languages)

        about = QFrame()
        about.setProperty("surface", "inset")
        about_layout = QHBoxLayout(about)
        about_layout.setContentsMargins(20, 16, 20, 16)
        about_layout.setSpacing(16)
        about_layout.addWidget(Icon("sparkles", 24), 0, Qt.AlignmentFlag.AlignTop)
        about_text = QVBoxLayout()
        about_text.setSpacing(5)
        about_text.addWidget(label("Free to explore. Made for everyday use.", "section"))
        description = label(
            "OpenMTL is a translation UI prototype. BackToMTL is not connected yet. "
            "Your preferences are saved on this device.", "muted"
        )
        description.setWordWrap(True)
        about_text.addWidget(description)
        about_layout.addLayout(about_text, 1)
        layout.addWidget(about)
        layout.addStretch()

        action_row = QHBoxLayout()
        self.status = label("Make it yours.", "small")
        self.status.setWordWrap(True)
        action_row.addWidget(self.status, 1)
        self.save_button = QPushButton("Save preferences  →")
        self.save_button.setProperty("kind", "primary")
        self.save_button.clicked.connect(self._save)
        action_row.addWidget(self.save_button)
        layout.addLayout(action_row)

        self._load()
        self.name_edit.textChanged.connect(self._mark_dirty)
        self.source_language.currentTextChanged.connect(self._mark_dirty)
        self.target_language.currentTextChanged.connect(self._mark_dirty)
        self.remember_languages.toggled.connect(self._mark_dirty)
        self.preferences.changed.connect(self._external_change)

    def _load(self):
        controls = (self.name_edit, self.source_language, self.target_language, self.remember_languages)
        for control in controls:
            control.blockSignals(True)
        self.name_edit.setText(self.preferences.name)
        self.source_language.setCurrentText(self.preferences.source_language)
        self.target_language.setCurrentText(self.preferences.target_language)
        self.remember_languages.setChecked(self.preferences.remember_languages)
        for control in controls:
            control.blockSignals(False)
        self._dirty = False

    def _mark_dirty(self, *_):
        self._dirty = True
        self.status.setText("You have unsaved changes.")

    def _external_change(self):
        if not self._dirty:
            self._load()

    def _save(self):
        name = self.name_edit.text().strip() or "friend"
        self.preferences.update(
            name=name,
            source_language=self.source_language.currentText(),
            target_language=self.target_language.currentText(),
            remember_languages=self.remember_languages.isChecked(),
        )
        self._load()
        self.status.setText("Saved. Your home screen is ready for you.")
