"""A single grayscale palette for the desktop prototype."""

STYLESHEET = """
QWidget {
    color: #222222;
    font-family: 'Segoe UI', 'Helvetica Neue', sans-serif;
    font-size: 14px;
}
QMainWindow { background: #f7f7f7; }
QLabel { background: transparent; }
QLabel[role="eyebrow"] {
    color: #858585; font-size: 10px; font-weight: 600; letter-spacing: 2px;
}
QLabel[role="title"] { font-size: 30px; font-weight: 600; letter-spacing: -1px; }
QLabel[role="greeting"] { font-size: 38px; font-weight: 500; letter-spacing: -1px; }
QLabel[role="subtitle"] { color: #777777; font-size: 14px; }
QLabel[role="muted"] { color: #888888; font-size: 12px; }
QLabel[role="small"] { color: #969696; font-size: 11px; }
QLabel[role="section"] { font-size: 15px; font-weight: 600; }
QFrame[surface="card"] {
    background: #ffffff; border: 1px solid #e4e4e4; border-radius: 14px;
}
QFrame[surface="inset"] {
    background: #f5f5f5; border: 1px solid #e8e8e8; border-radius: 10px;
}
QFrame#sidebar { background: #fbfbfb; border-right: 1px solid #e5e5e5; }
QFrame#topbar { background: #f7f7f7; border-bottom: 1px solid #e9e9e9; }
QPushButton {
    background: #ffffff; border: 1px solid #dddddd; border-radius: 8px;
    padding: 10px 16px; font-weight: 500;
}
QPushButton:hover { background: #eeeeee; border-color: #c5c5c5; }
QPushButton:pressed { background: #e2e2e2; }
QPushButton:focus { border-color: #777777; }
QPushButton:disabled { color: #aaaaaa; background: #eeeeee; border-color: #e5e5e5; }
QPushButton[kind="primary"] {
    background: #252525; color: white; border: 1px solid #252525;
}
QPushButton[kind="primary"]:hover { background: #444444; border-color: #444444; }
QPushButton[kind="primary"]:pressed { background: #111111; }
QPushButton[kind="primary"]:disabled { background: #d2d2d2; border-color: #d2d2d2; color: #f9f9f9; }
QPushButton[kind="ghost"] { background: transparent; border: 1px solid transparent; }
QPushButton[kind="ghost"]:hover { background: #ebebeb; }
QPushButton[kind="ghost"]:focus { border-color: #888888; }
QPushButton#navButton {
    background: transparent; border: 1px solid transparent; text-align: left;
    color: #777777; padding: 11px 12px; border-radius: 8px;
}
QPushButton#navButton:hover { background: #f0f0f0; color: #333333; }
QPushButton#navButton:checked {
    background: #eaeaea; border-color: #e3e3e3; color: #222222;
}
QPushButton#navButton:focus { border-color: #aaaaaa; }
QPushButton#actionCard {
    background: #ffffff; border: 1px solid #dddddd; border-radius: 12px;
}
QPushButton#actionCard:hover { background: #fafafa; border-color: #aaaaaa; }
QPushButton#actionCard:pressed { background: #efefef; }
QPushButton#actionCard:focus { border: 2px solid #777777; }
QLineEdit, QComboBox, QTextEdit, QPlainTextEdit {
    background: #ffffff; border: 1px solid #dddddd; border-radius: 8px;
    padding: 10px 12px; selection-background-color: #dddddd; selection-color: #222222;
}
QLineEdit:focus, QComboBox:focus, QTextEdit:focus, QPlainTextEdit:focus {
    border-color: #777777;
}
QLineEdit:disabled, QComboBox:disabled { color: #aaaaaa; background: #f3f3f3; }
QComboBox { min-height: 19px; padding-right: 24px; }
QComboBox::drop-down { border: none; width: 22px; }
QComboBox QAbstractItemView {
    background: #ffffff; border: 1px solid #dddddd;
    selection-background-color: #eeeeee; selection-color: #222222; padding: 5px;
}
QTextEdit, QPlainTextEdit { line-height: 1.5; }
QCheckBox { spacing: 10px; }
QCheckBox::indicator {
    width: 17px; height: 17px; border: 1px solid #cccccc;
    border-radius: 4px; background: #ffffff;
}
QCheckBox::indicator:checked { background: #333333; border: 4px solid #777777; }
QCheckBox::indicator:focus { border-color: #333333; }
QProgressBar {
    border: none; background: #e9e9e9; border-radius: 3px;
    height: 6px; text-align: center;
}
QProgressBar::chunk { background: #555555; border-radius: 3px; }
QScrollArea, QStackedWidget { border: none; background: transparent; }
QScrollBar:vertical { background: transparent; width: 7px; margin: 3px; }
QScrollBar::handle:vertical { background: #cccccc; border-radius: 3px; min-height: 28px; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }
QToolTip { background: #222222; color: white; border: none; padding: 6px; }
"""
