"""Two small workspaces for exploring the translation UI without a backend."""

from pathlib import Path

from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtWidgets import (
    QApplication, QComboBox, QFileDialog, QFrame, QHBoxLayout, QLabel,
    QListWidget, QProgressBar, QPushButton, QTextEdit, QVBoxLayout, QWidget,
)

from openmtl.preferences import LANGUAGES
from openmtl.widgets import Icon, icon_button, label


SAMPLE_SOURCE = "Hello, world! A little understanding goes a long way."
SAMPLE_TRANSLATIONS = {
    "English": SAMPLE_SOURCE,
    "Japanese": "こんにちは、世界！少しの理解が、大きな一歩につながります。",
    "Spanish": "¡Hola, mundo! Un poco de comprensión puede hacer mucho.",
    "French": "Bonjour, le monde ! Un peu de compréhension peut faire beaucoup.",
    "German": "Hallo, Welt! Ein wenig Verständnis kann viel bewirken.",
    "Korean": "안녕하세요, 세상! 작은 이해가 큰 변화를 만듭니다.",
    "Chinese (Simplified)": "你好，世界！一点理解，带来更多可能。",
    "Portuguese": "Olá, mundo! Um pouco de compreensão faz toda a diferença.",
}
FILE_TYPES = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".gif", ".tif", ".tiff", ".pdf", ".txt"}


class FileDropArea(QFrame):
    files_dropped = pyqtSignal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setObjectName("fileDropArea")
        self.setStyleSheet(
            "QFrame#fileDropArea { background: #fcfcfc; border: 1px dashed #c9c9c9; "
            "border-radius: 14px; }"
        )
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 25, 24, 25)
        layout.setSpacing(10)
        layout.addWidget(Icon("upload", 28), 0, Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(label("Drop a little possibility here", "section"), 0, Qt.AlignmentFlag.AlignHCenter)
        hint = label("Images, PDFs, or text files · staged locally", "muted")
        layout.addWidget(hint, 0, Qt.AlignmentFlag.AlignHCenter)
        self.browse_button = QPushButton("Browse files")
        self.browse_button.setProperty("kind", "secondary")
        layout.addWidget(self.browse_button, 0, Qt.AlignmentFlag.AlignHCenter)

    def dragEnterEvent(self, event):
        if any(url.isLocalFile() for url in event.mimeData().urls()):
            event.acceptProposedAction()

    def dropEvent(self, event):
        paths = [url.toLocalFile() for url in event.mimeData().urls() if url.isLocalFile()]
        if paths:
            self.files_dropped.emit(paths)
            event.acceptProposedAction()


class TranslationPage(QWidget):
    def __init__(self, mode, preferences, parent=None):
        super().__init__(parent)
        self.mode = mode
        self.preferences = preferences
        self._paths = []
        self._busy = False
        layout = QVBoxLayout(self)
        layout.setContentsMargins(44, 30, 44, 26)
        layout.setSpacing(16)
        layout.addWidget(label("YOUR WORKSPACE  /  " + ("01" if mode == "auto" else "02"), "eyebrow"))
        layout.addWidget(label("Auto translate" if mode == "auto" else "Translate and edit", "title"))
        subtitle = "Give your files a new language." if mode == "auto" else "Find the words. Make them your own."
        layout.addWidget(label(subtitle, "subtitle"))
        layout.addSpacing(8)
        layout.addWidget(self._language_bar())
        if mode == "auto":
            self._build_auto(layout)
        else:
            self._build_edit(layout)
        self.status = label("Prototype workspace · BackToMTL is not connected.", "small")
        self.status.setWordWrap(True)
        layout.addWidget(self.status)
        self.refresh_preferences()
        self.source_language.currentTextChanged.connect(self._language_changed)
        self.target_language.currentTextChanged.connect(self._language_changed)
        self.preferences.changed.connect(self.refresh_preferences)
        if mode == "edit":
            self.source_editor.textChanged.connect(self._source_changed)

    def _language_bar(self):
        bar = QFrame()
        bar.setProperty("surface", "card")
        bar.setObjectName("languageBar")
        row = QHBoxLayout(bar)
        row.setContentsMargins(18, 12, 18, 12)
        row.setSpacing(16)
        self.source_language = QComboBox()
        self.source_language.addItems(LANGUAGES)
        self.source_language.setAccessibleName("Source language")
        self.target_language = QComboBox()
        self.target_language.addItems([item for item in LANGUAGES if item != "Auto-detect"])
        self.target_language.setAccessibleName("Target language")
        row.addWidget(label("FROM", "eyebrow"))
        row.addWidget(self.source_language, 1)
        row.addWidget(Icon("arrow_right", 18))
        row.addWidget(label("TO", "eyebrow"))
        row.addWidget(self.target_language, 1)
        return bar

    def _build_auto(self, layout):
        self.drop_area = FileDropArea()
        self.drop_area.browse_button.clicked.connect(self._browse)
        self.drop_area.files_dropped.connect(self._add_files)
        layout.addWidget(self.drop_area)
        file_header = QHBoxLayout()
        self.file_count = label("YOUR FILES  /  0", "eyebrow")
        file_header.addWidget(self.file_count)
        file_header.addStretch()
        self.remove_button = QPushButton("Remove selected")
        self.remove_button.setProperty("kind", "ghost")
        self.remove_button.setEnabled(False)
        self.remove_button.clicked.connect(self._remove_files)
        file_header.addWidget(self.remove_button)
        layout.addLayout(file_header)
        self.file_list = QListWidget()
        self.file_list.setAccessibleName("Staged files")
        self.file_list.setStyleSheet(
            "QListWidget { background: #ffffff; border: 1px solid #e4e4e4; "
            "border-radius: 10px; padding: 6px; } "
            "QListWidget::item { padding: 7px; border-radius: 5px; } "
            "QListWidget::item:selected { background: #e9e9e9; color: #222222; }"
        )
        self.file_list.setSelectionMode(QListWidget.SelectionMode.ExtendedSelection)
        self.file_list.setMinimumHeight(70)
        self.file_list.setMaximumHeight(140)
        self.file_list.itemSelectionChanged.connect(
            lambda: self.remove_button.setEnabled(bool(self.file_list.selectedItems()) and not self._busy)
        )
        layout.addWidget(self.file_list, 1)
        self.progress = QProgressBar()
        self.progress.setRange(0, 0)
        self.progress.setFixedHeight(4)
        self.progress.setTextVisible(False)
        self.progress.hide()
        layout.addWidget(self.progress)
        action_row = QHBoxLayout()
        caption = label("A preview of the flow. Your files stay on your device.", "small")
        caption.setWordWrap(True)
        action_row.addWidget(caption, 1)
        self.action_button = QPushButton("Preview translation  →")
        self.action_button.setProperty("kind", "primary")
        self.action_button.setEnabled(False)
        self.action_button.clicked.connect(self._preview_files)
        action_row.addWidget(self.action_button)
        layout.addLayout(action_row)

    def _build_edit(self, layout):
        editors = QHBoxLayout()
        editors.setSpacing(16)
        for output in (False, True):
            card = QFrame()
            card.setProperty("surface", "card")
            column = QVBoxLayout(card)
            column.setContentsMargins(20, 16, 20, 16)
            header = QHBoxLayout()
            header.addWidget(label("YOUR WORDS" if not output else "SAMPLE PREVIEW", "eyebrow"))
            header.addStretch()
            editor = QTextEdit()
            editor.setAcceptRichText(False)
            editor.setMinimumHeight(180)
            editor.setStyleSheet("QTextEdit { border: none; background: transparent; padding: 0; }")
            if output:
                self.output_editor = editor
                editor.setAccessibleName("Editable sample translation")
                self.copy_button = icon_button("copy", "Copy preview")
                self.copy_button.setEnabled(False)
                self.copy_button.clicked.connect(self._copy_output)
                header.addWidget(self.copy_button)
                editor.setPlaceholderText("The sample appears here. You can edit every word.")
                editor.textChanged.connect(lambda: self.copy_button.setEnabled(bool(editor.toPlainText())))
            else:
                self.source_editor = editor
                editor.setAccessibleName("Source text")
                editor.setPlainText(SAMPLE_SOURCE)
                editor.setPlaceholderText("Type or paste your text here…")
            column.addLayout(header)
            column.addWidget(editor, 1)
            footer = label("Editable output" if output else "Start with our sample, or try your own words", "small")
            column.addWidget(footer)
            editors.addWidget(card, 1)
        layout.addLayout(editors, 1)
        action_row = QHBoxLayout()
        reset = QPushButton("Reset sample")
        reset.setProperty("kind", "ghost")
        reset.clicked.connect(self._reset_sample)
        action_row.addWidget(reset)
        action_row.addStretch()
        self.action_button = QPushButton("Preview translation  →")
        self.action_button.setProperty("kind", "primary")
        self.action_button.clicked.connect(self._preview_text)
        action_row.addWidget(self.action_button)
        layout.addLayout(action_row)

    def refresh_preferences(self):
        snapshot = (
            self.preferences.source_language, self.preferences.target_language,
            self.preferences.remember_languages,
        )
        if snapshot == getattr(self, "_saved_preferences", None):
            return
        self._saved_preferences = snapshot
        changed = False
        for combo, value in ((self.source_language, self.preferences.source_language),
                             (self.target_language, self.preferences.target_language)):
            changed = changed or combo.currentText() != value
            combo.blockSignals(True)
            combo.setCurrentText(value)
            combo.blockSignals(False)
        if changed and self.mode == "edit" and self.output_editor.toPlainText():
            self.output_editor.clear()
            self.status.setText("Language preferences changed. Generate a new sample preview.")

    def _language_changed(self):
        if self.preferences.remember_languages:
            self.preferences.update(source_language=self.source_language.currentText(),
                                    target_language=self.target_language.currentText())
        if self.mode == "edit" and self.output_editor.toPlainText():
            self.output_editor.clear()
            self.status.setText("Language changed. Generate a new sample preview.")

    def _source_changed(self):
        if self.output_editor.toPlainText():
            self.output_editor.clear()
            self.status.setText("Source changed. Generate a new sample preview.")

    def _browse(self):
        paths, _ = QFileDialog.getOpenFileNames(
            self, "Choose files", "", "Supported files (*.png *.jpg *.jpeg *.webp *.bmp *.gif *.tif *.tiff *.pdf *.txt)"
        )
        self._add_files(paths)

    def _add_files(self, paths):
        rejected = 0
        for raw in paths:
            path = Path(raw)
            if path.suffix.lower() not in FILE_TYPES or not path.is_file():
                rejected += 1
            elif str(path) not in self._paths:
                self._paths.append(str(path))
                self.file_list.addItem(path.name)
                self.file_list.item(self.file_list.count() - 1).setToolTip(str(path))
        self._update_file_count()
        if rejected:
            self.status.setText("Some items were skipped. Choose an image, PDF, or text file.")
        elif paths:
            self.status.setText("Files staged locally. This prototype does not read or upload their contents.")

    def _remove_files(self):
        rows = sorted((self.file_list.row(item) for item in self.file_list.selectedItems()), reverse=True)
        for row in rows:
            self.file_list.takeItem(row)
            self._paths.pop(row)
        self._update_file_count()
        self.status.setText("Selection updated. Files on your device are unchanged.")

    def _update_file_count(self):
        self.file_count.setText(f"YOUR FILES  /  {len(self._paths)}")
        self.action_button.setEnabled(bool(self._paths) and not self._busy)

    def _preview_files(self):
        self._busy = True
        self.action_button.setEnabled(False)
        self.remove_button.setEnabled(False)
        self.drop_area.setEnabled(False)
        self.progress.show()
        self.status.setText("Preparing a sample workflow preview…")
        QTimer.singleShot(650, self._finish_file_preview)

    def _finish_file_preview(self):
        self._busy = False
        self.progress.hide()
        self.drop_area.setEnabled(True)
        self.remove_button.setEnabled(bool(self.file_list.selectedItems()))
        self._update_file_count()
        count = len(self._paths)
        self.status.setText(
            f"Preview ready · {count} file{'s' if count != 1 else ''} → {self.target_language.currentText()}. "
            "Connect BackToMTL to translate and export files."
        )

    def _preview_text(self):
        if not self.source_editor.toPlainText().strip():
            self.status.setText("Add a little text first, or reset the sample.")
            self.source_editor.setFocus()
            return
        if self.source_language.currentText() not in ("Auto-detect", "English"):
            self.output_editor.clear()
            self.status.setText("Select English or Auto-detect as the source language to preview the English sample.")
            return
        if self.source_editor.toPlainText().strip() != SAMPLE_SOURCE:
            self.output_editor.clear()
            self.status.setText("Custom text needs BackToMTL. Use Reset sample to explore the editable preview.")
            return
        self.output_editor.setPlainText(SAMPLE_TRANSLATIONS[self.target_language.currentText()])
        self.status.setText("Bundled sample preview · edit or copy the result. No translation service was called.")

    def _reset_sample(self):
        self.source_editor.setPlainText(SAMPLE_SOURCE)
        self.output_editor.clear()
        self.status.setText("Sample restored. Choose a language and preview the result.")

    def _copy_output(self):
        QApplication.clipboard().setText(self.output_editor.toPlainText())
        self.status.setText("Preview copied to your clipboard.")
