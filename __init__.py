from aqt import mw
from aqt.qt import (
    QAction,
    QDialog,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    Qt,
)
from aqt.utils import showWarning

_selector_dialog = None


def open_add_cards(deck_name: str, note_type_name: str) -> None:
    col = mw.col
    deck = col.decks.by_name(deck_name)
    if deck is None:
        showWarning(f"Deck not found: {deck_name!r}")
        return
    model = col.models.by_name(note_type_name)
    if model is None:
        showWarning(f"Note type not found: {note_type_name!r}")
        return

    col.decks.select(deck["id"])
    col.models.set_current(model)

    from aqt import dialogs

    entry = dialogs._dialogs.get("AddCards")
    if entry and entry[1] and not entry[1].isHidden():
        add_win = entry[1]
        try:
            add_win.deck_chooser.selected_deck_id = deck["id"]
        except Exception:
            pass
        try:
            add_win.notetype_chooser.selected_notetype_id = model["id"]
        except Exception:
            pass
        add_win.raise_()
        add_win.activateWindow()
    else:
        mw.onAddCard()


class LanguageSelectorDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Language Selector")
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, True)
        layout = QVBoxLayout(self)
        layout.setSpacing(8)

        config = mw.addonManager.getConfig(__name__)
        for lang in config.get("languages", []):
            row = QHBoxLayout()
            label = QLabel(lang["name"])
            label.setMinimumWidth(80)

            sentences_btn = QPushButton("Sentences")
            sentences_btn.clicked.connect(
                lambda checked=False,
                d=lang["sentences_deck"],
                n=lang["sentences_note_type"]: open_add_cards(d, n)
            )

            misc_btn = QPushButton("Misc")
            misc_btn.clicked.connect(
                lambda checked=False,
                d=lang["misc_deck"],
                n=lang["misc_note_type"]: open_add_cards(d, n)
            )

            row.addWidget(label)
            row.addWidget(sentences_btn)
            row.addWidget(misc_btn)
            layout.addLayout(row)


def show_language_selector() -> None:
    global _selector_dialog
    if _selector_dialog is None:
        _selector_dialog = LanguageSelectorDialog(mw)
    _selector_dialog.show()
    _selector_dialog.raise_()
    _selector_dialog.activateWindow()


action = QAction("Language Selector", mw)
action.triggered.connect(show_language_selector)
mw.form.menuTools.addAction(action)
