"""Small local preference store; no account or service is required."""

from datetime import datetime, timezone

from PyQt6.QtCore import QObject, QSettings, pyqtSignal


LANGUAGES = (
    "Auto-detect", "English", "Japanese", "Spanish", "French", "German",
    "Korean", "Chinese (Simplified)", "Portuguese",
)


class Preferences(QObject):
    changed = pyqtSignal()

    def __init__(self, settings=None, parent=None):
        super().__init__(parent)
        self.settings = settings if settings is not None else QSettings("OpenMTL", "OpenMTL")
        self.name = str(self.settings.value("profile/name", "friend"))
        self.remember_languages = self.settings.value("translation/remember", True, type=bool)
        self.source_language = self._language("translation/source", "Auto-detect")
        self.target_language = self._language("translation/target", "English", target=True)
        self.returning_after_absence = self._has_been_away()

    def _language(self, key, default, target=False):
        value = self.settings.value(key, default)
        return value if value in LANGUAGES[int(target):] else default

    def _has_been_away(self):
        last_used = self.settings.value("session/last_used", "")
        if not last_used:
            return False
        try:
            previous = datetime.fromisoformat(str(last_used))
            if previous.tzinfo is None:
                previous = previous.replace(tzinfo=timezone.utc)
            return (datetime.now(timezone.utc) - previous).days >= 7
        except (ValueError, TypeError):
            return False

    def update(self, *, name=None, source_language=None, target_language=None,
               remember_languages=None):
        if name is not None:
            self.name = " ".join(name.split())[:40] or "friend"
            self.settings.setValue("profile/name", self.name)
        if remember_languages is not None:
            self.remember_languages = bool(remember_languages)
            self.settings.setValue("translation/remember", self.remember_languages)
        if source_language in LANGUAGES:
            self.source_language = source_language
        if target_language in LANGUAGES[1:]:
            self.target_language = target_language
        # Settings always saves the defaults. Workspaces call update only when
        # remembering the last language pair is enabled.
        self.settings.setValue("translation/source", self.source_language)
        self.settings.setValue("translation/target", self.target_language)
        self.settings.sync()
        self.changed.emit()

    def mark_used(self):
        self.settings.setValue("session/last_used", datetime.now(timezone.utc).isoformat())
        self.settings.sync()
