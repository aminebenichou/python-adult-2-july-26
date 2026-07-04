import sys
from PySide6 import QtCore, QtWidgets, QtGui
from manageDb import createDb, createTable

# ─────────────────────────────────────────────────────────────────────────────
#  TaskCard
# ─────────────────────────────────────────────────────────────────────────────

class TaskCard(QtWidgets.QWidget):
    """
    Self-contained card widget — add this directly to a layout.

    Palette:
        Surface:  #1E1E2E   Card: #2A2A3E   Border: #3D3D55
        Accent:   #7C6AF7   Hi:   #EAEAF5   Lo:     #8888A8
        Danger:   #E05C6A
    """

    def __init__(self, title: str, desc: str = "", status: str = "todo", parent=None):
        super().__init__(parent)
        self._build_ui(title, desc, status)

    # ── Build ──────────────────────────────────────────────────────────────

    def _build_ui(self, title: str, desc: str, status: str):
        root = QtWidgets.QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)

        # Card frame
        self.card = QtWidgets.QFrame()
        self.card.setObjectName("taskCard")
        self.card.setMinimumWidth(420)
        self.card.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))

        # Accent bar + content side-by-side
        card_row = QtWidgets.QHBoxLayout(self.card)
        card_row.setContentsMargins(0, 0, 0, 0)
        card_row.setSpacing(0)

        accent_bar = QtWidgets.QFrame()
        accent_bar.setObjectName("accentBar")
        accent_bar.setFixedWidth(4)

        content = QtWidgets.QWidget()
        content.setObjectName("cardContent")
        content_layout = QtWidgets.QVBoxLayout(content)
        content_layout.setContentsMargins(16, 14, 16, 14)
        content_layout.setSpacing(8)

        # Header row
        header_row = QtWidgets.QHBoxLayout()
        header_row.setSpacing(8)

        self.title_label = QtWidgets.QLabel(title)
        self.title_label.setObjectName("taskTitle")
        self.title_label.setWordWrap(True)

        self.status_badge = QtWidgets.QLabel(self._badge_text(status))
        self.status_badge.setObjectName(f"badge_{status}")
        self.status_badge.setFixedHeight(22)
        self.status_badge.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        header_row.addWidget(self.title_label, 1)
        header_row.addWidget(
            self.status_badge, 0, QtCore.Qt.AlignmentFlag.AlignTop
        )

        # Description
        self.desc_label = QtWidgets.QLabel(desc or "No description provided.")
        self.desc_label.setObjectName("taskDesc")
        self.desc_label.setWordWrap(True)

        # Divider
        divider = QtWidgets.QFrame()
        divider.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        divider.setObjectName("divider")

        # Buttons
        btn_row = QtWidgets.QHBoxLayout()
        btn_row.setSpacing(8)
        btn_row.addStretch()

        self.edit_btn = QtWidgets.QPushButton("Edit")
        self.edit_btn.setObjectName("editBtn")
        self.edit_btn.setFixedSize(72, 30)

        self.delete_btn = QtWidgets.QPushButton("Delete")
        self.delete_btn.setObjectName("deleteBtn")
        self.delete_btn.setFixedSize(72, 30)

        btn_row.addWidget(self.edit_btn)
        btn_row.addWidget(self.delete_btn)

        content_layout.addLayout(header_row)
        content_layout.addWidget(self.desc_label)
        content_layout.addWidget(divider)
        content_layout.addLayout(btn_row)

        card_row.addWidget(accent_bar)
        card_row.addWidget(content, 1)

        root.addWidget(self.card)
        self._apply_styles()

    # ── Helpers ────────────────────────────────────────────────────────────

    @staticmethod
    def _badge_text(status: str) -> str:
        return {
            "todo":        "· To Do",
            "in_progress": "▶ In Progress",
            "done":        "✓ Done",
        }.get(status, status.upper())

    def _apply_styles(self):
        # Apply to self so child objectNames are always in scope
        self.setStyleSheet("""
            QFrame#taskCard {
                background-color: #2A2A3E;
                border: 1px solid #3D3D55;
                border-radius: 12px;
            }
            QFrame#taskCard:hover {
                border-color: #7C6AF7;
                background-color: #2E2E45;
            }
            QFrame#accentBar {
                background-color: #7C6AF7;
                border-top-left-radius: 11px;
                border-bottom-left-radius: 11px;
                min-height: 60px;
            }
            QWidget#cardContent {
                background: transparent;
            }
            QLabel#taskTitle {
                color: #EAEAF5;
                font-family: "Segoe UI", "SF Pro Display", sans-serif;
                font-size: 14px;
                font-weight: 700;
                background: transparent;
            }
            QLabel#taskDesc {
                color: #8888A8;
                font-family: "Segoe UI", "SF Pro Text", sans-serif;
                font-size: 12px;
                background: transparent;
            }
            QFrame#divider {
                color: #3D3D55;
                max-height: 1px;
            }
            QLabel#badge_todo {
                color: #8888A8;
                border: 1px solid #3D3D55;
                border-radius: 10px;
                padding: 2px 8px;
                font-size: 10px;
                font-weight: 600;
                background: transparent;
            }
            QLabel#badge_in_progress {
                color: #F7A26A;
                border: 1px solid #F7A26A;
                border-radius: 10px;
                padding: 2px 8px;
                font-size: 10px;
                font-weight: 600;
                background: transparent;
            }
            QLabel#badge_done {
                color: #5EC887;
                border: 1px solid #5EC887;
                border-radius: 10px;
                padding: 2px 8px;
                font-size: 10px;
                font-weight: 600;
                background: transparent;
            }
            QPushButton#editBtn {
                background-color: transparent;
                color: #7C6AF7;
                border: 1px solid #7C6AF7;
                border-radius: 6px;
                font-size: 12px;
                font-weight: 600;
            }
            QPushButton#editBtn:hover {
                background-color: #7C6AF7;
                color: #EAEAF5;
            }
            QPushButton#editBtn:pressed {
                background-color: #6254D4;
            }
            QPushButton#deleteBtn {
                background-color: transparent;
                color: #E05C6A;
                border: 1px solid #E05C6A;
                border-radius: 6px;
                font-size: 12px;
                font-weight: 600;
            }
            QPushButton#deleteBtn:hover {
                background-color: #E05C6A;
                color: #EAEAF5;
            }
            QPushButton#deleteBtn:pressed {
                background-color: #B8404D;
            }
        """)


# ─────────────────────────────────────────────────────────────────────────────
#  Main Window
# ─────────────────────────────────────────────────────────────────────────────

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        connectionToDb = createDb()
        createTable(connectionToDb)
        self.tasks: list[tuple[str, str]] = []
        self._build_ui()

    def _build_ui(self):
        self.setWindowTitle("Task Manager")
        self.setMinimumSize(860, 540)
        self.setStyleSheet("background-color: #1E1E2E;")

        main_layout = QtWidgets.QHBoxLayout(self)
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(24)

        # ── Left panel (input form) ────────────────────────────────────
        left_panel = QtWidgets.QFrame()
        left_panel.setObjectName("leftPanel")
        left_panel.setFixedWidth(260)
        left_panel.setStyleSheet("""
            QFrame#leftPanel {
                background-color: #2A2A3E;
                border: 1px solid #3D3D55;
                border-radius: 14px;
            }
        """)

        form_layout = QtWidgets.QVBoxLayout(left_panel)
        form_layout.setContentsMargins(20, 20, 20, 20)
        form_layout.setSpacing(12)

        panel_label = QtWidgets.QLabel("New Task")
        panel_label.setStyleSheet("""
            color: #EAEAF5;
            font-family: "Segoe UI", sans-serif;
            font-size: 15px;
            font-weight: 700;
            background: transparent;
        """)

        self.title_input = QtWidgets.QLineEdit()
        self.title_input.setPlaceholderText("Task title…")
        self.title_input.setFixedHeight(36)

        self.desc_input = QtWidgets.QTextEdit()
        self.desc_input.setPlaceholderText("Description (optional)…")
        self.desc_input.setFixedHeight(100)

        self.add_btn = QtWidgets.QPushButton("＋  Add Task")
        self.add_btn.setFixedHeight(38)
        self.add_btn.clicked.connect(self._add_task)

        input_style = """
            QLineEdit, QTextEdit {
                background-color: #1E1E2E;
                color: #EAEAF5;
                border: 1px solid #3D3D55;
                border-radius: 8px;
                padding: 6px 10px;
                font-family: "Segoe UI", sans-serif;
                font-size: 12px;
            }
            QLineEdit:focus, QTextEdit:focus {
                border-color: #7C6AF7;
            }
            QLineEdit::placeholder, QTextEdit::placeholder {
                color: #55556A;
            }
        """
        btn_style = """
            QPushButton {
                background-color: #7C6AF7;
                color: #EAEAF5;
                border: none;
                border-radius: 8px;
                font-family: "Segoe UI", sans-serif;
                font-size: 13px;
                font-weight: 700;
            }
            QPushButton:hover  { background-color: #8F7EFF; }
            QPushButton:pressed{ background-color: #6254D4; }
        """
        self.title_input.setStyleSheet(input_style)
        self.desc_input.setStyleSheet(input_style)
        self.add_btn.setStyleSheet(btn_style)

        form_layout.addWidget(panel_label)
        form_layout.addWidget(self.title_input)
        form_layout.addWidget(self.desc_input)
        form_layout.addWidget(self.add_btn)
        form_layout.addStretch()

        # ── Right panel (card list, scrollable) ───────────────────────
        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        scroll_area.setStyleSheet("""
            QScrollArea { background: transparent; border: none; }
            QScrollBar:vertical {
                background: #2A2A3E; width: 6px; border-radius: 3px;
            }
            QScrollBar::handle:vertical {
                background: #3D3D55; border-radius: 3px; min-height: 20px;
            }
            QScrollBar::handle:vertical:hover { background: #7C6AF7; }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
        """)

        self.cards_container = QtWidgets.QWidget()
        self.cards_container.setStyleSheet("background: transparent;")
        self.right_layout = QtWidgets.QVBoxLayout(self.cards_container)
        self.right_layout.setContentsMargins(0, 0, 8, 0)
        self.right_layout.setSpacing(12)
        self.right_layout.addStretch()           # pushes cards to the top

        scroll_area.setWidget(self.cards_container)

        main_layout.addWidget(left_panel)
        main_layout.addWidget(scroll_area, 1)

    # ── Slots ──────────────────────────────────────────────────────────────

    def _add_task(self):
        title = self.title_input.text().strip()
        if not title:
            return                              # don't add blank cards
        desc = self.desc_input.toPlainText().strip()
        self.tasks.append((title, desc))
        self.title_input.clear()
        self.desc_input.clear()
        self._rebuild_cards()

    def _rebuild_cards(self):
        # Remove all widgets except the trailing stretch
        while self.right_layout.count() > 1:
            item = self.right_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Insert cards before the stretch
        for title, desc in self.tasks:
            card = TaskCard(title=title, desc=desc)
            self.right_layout.insertWidget(self.right_layout.count() - 1, card)


# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = MyWidget()
    widget.show()
    sys.exit(app.exec())