#!/usr/bin/env python3
"""
cheat — interactive terminal cheat sheet (Catppuccin Frappé)
↑ ↓  navigate  ·  /  search  ·  Esc  clear  ·  q  quit
"""

import sys
from textual.app import App, ComposeResult
from textual.widgets import Footer, ListView, ListItem, Label, DataTable, Input, Static
from textual.containers import Horizontal, Vertical
from textual.binding import Binding
from textual import on

# ── Catppuccin Frappé palette ─────────────────────────────────────────
BG       = "#303446"
MANTLE   = "#292c3c"
SURFACE0 = "#414559"
SURFACE1 = "#51576d"
SURFACE2 = "#626880"
OVERLAY0 = "#737994"
OVERLAY2 = "#949cbb"
TEXT     = "#c6d0f5"
SUBTEXT1 = "#b5bfe2"
SUBTEXT0 = "#a5adce"
LAVENDER = "#babbf1"
BLUE     = "#8caaee"
SAPPHIRE = "#85c1dc"
SKY      = "#99d1db"
TEAL     = "#81c8be"
GREEN    = "#a6d189"
YELLOW   = "#e5c890"
PEACH    = "#ef9f76"
RED      = "#e78284"
MAUVE    = "#ca9ee6"
PINK     = "#f4b8e4"
ROSEWATER= "#f2d5cf"

CAT_COLORS = {
    "General":        BLUE,
    "Editing":        GREEN,
    "Navigation":     MAUVE,
    "Splits & Tabs":  PEACH,
    "Terminal":       TEAL,
    "My Shortcuts":   YELLOW,
    "Brave":          PEACH,
    "KDE / Kubuntu":  LAVENDER,
    "Alacritty":      SKY,
}

# ── Data ──────────────────────────────────────────────────────────────

VSCODE: dict[str, list[tuple[str, str]]] = {
    "General": [
        ("Ctrl+Shift+P",     "Command palette"),
        ("Ctrl+P",           "Quick open file"),
        ("Ctrl+,",           "Open settings"),
        ("Ctrl+K  Ctrl+S",   "Keyboard shortcuts"),
        ("Ctrl+Shift+N",     "New window"),
        ("Ctrl+W",           "Close editor"),
        ("Ctrl+Shift+W",     "Close window"),
    ],
    "Editing": [
        ("Ctrl+D",           "Select next occurrence"),
        ("Ctrl+Shift+L",     "Select all occurrences"),
        ("Alt+↑ / ↓",        "Move line up / down"),
        ("Shift+Alt+↑ / ↓",  "Copy line up / down"),
        ("Ctrl+Shift+K",     "Delete line"),
        ("Ctrl+/",           "Toggle comment"),
        ("Ctrl+Space",       "Trigger suggestion"),
        ("F2",               "Rename symbol"),
        ("Ctrl+.",           "Quick fix"),
        ("Tab / Shift+Tab",  "Indent / outdent"),
        ("Ctrl+Z",           "Undo"),
        ("Ctrl+Shift+Z",     "Redo"),
    ],
    "Navigation": [
        ("Ctrl+Tab",         "Cycle open files"),
        ("Ctrl+G",           "Go to line"),
        ("F12",              "Go to definition"),
        ("Alt+F12",          "Peek definition"),
        ("Shift+F12",        "Find all references"),
        ("Ctrl+Shift+F",     "Search in files"),
        ("Ctrl+H",           "Replace in file"),
        ("Ctrl+Shift+H",     "Replace in files"),
        ("Ctrl+Shift+O",     "Go to symbol"),
    ],
    "Splits & Tabs": [
        ("Ctrl+\\",          "Split editor"),
        ("Ctrl+1 / 2 / 3",   "Focus split group"),
        ("Ctrl+Shift+T",     "Reopen closed editor"),
        ("Ctrl+B",           "Toggle sidebar"),
        ("Ctrl+Shift+E",     "Explorer"),
        ("Ctrl+Shift+G",     "Source control"),
        ("Ctrl+Shift+X",     "Extensions"),
        ("Ctrl+Shift+D",     "Run & debug"),
    ],
    "Terminal": [
        ("Ctrl+`",           "Toggle integrated terminal"),
        ("Ctrl+J",           "Toggle terminal panel on / off"),
        ("Ctrl+Shift+M",     "Maximize / restore terminal (custom)"),
        ("Ctrl+Shift+`",     "New terminal"),
        ("Ctrl+Shift+5",     "Split terminal"),
        ("Ctrl+1",           "Focus back to editor"),
        ("Alt+↑ / ↓",        "Scroll terminal up / down"),
        ("Ctrl+Shift+W",     "Close VS Code window"),
        ("Ctrl+Q",           "Quit VS Code"),
    ],
}

PC: dict[str, list[tuple[str, str]]] = {
    "My Shortcuts": [
        ("Ctrl+Shift+K",     "Open Alacritty terminal"),
        ("Ctrl+Shift+B",     "Open Brave browser"),
        ("Ctrl+Shift+L",     "Open my app"),
    ],
    "Brave": [
        ("Ctrl+T",           "New tab"),
        ("Ctrl+W",           "Close tab"),
        ("Ctrl+Shift+T",     "Reopen closed tab"),
        ("Ctrl+Tab",         "Next tab"),
        ("Ctrl+Shift+Tab",   "Previous tab"),
        ("Ctrl+1..8",        "Jump to tab N"),
        ("Ctrl+9",           "Jump to last tab"),
        ("Ctrl+L",           "Focus address bar"),
        ("Ctrl+R",           "Reload page"),
        ("Ctrl+Shift+R",     "Hard reload (no cache)"),
        ("Ctrl+F",           "Find on page"),
        ("Ctrl+D",           "Bookmark page"),
        ("Ctrl+H",           "History"),
        ("Ctrl+J",           "Downloads"),
        ("Ctrl+Shift+N",     "New incognito window"),
        ("Ctrl++ / Ctrl+-",  "Zoom in / out"),
        ("Ctrl+0",           "Reset zoom"),
        ("F11",              "Fullscreen"),
        ("Ctrl+U",           "View page source"),
        ("F12",              "DevTools"),
    ],
    "KDE / Kubuntu": [
        ("Meta",             "App launcher (KRunner)"),
        ("Meta+D",           "Show desktop"),
        ("Meta+M",           "Maximize window (custom)"),
        ("Meta+PgUp",        "Maximize window (default)"),
        ("Meta+PgDn",        "Restore window (default)"),
        ("Meta+← / →",       "Snap window left / right"),
        ("Meta+↑ / ↓",       "Tile window top / bottom"),
        ("Meta+Shift+← / →", "Move window to other screen"),
        ("Alt+F4",           "Close window"),
        ("Alt+Tab",          "Switch windows"),
        ("Alt+F2",           "KRunner (run command)"),
        ("Ctrl+Alt+T",       "Open terminal"),
        ("PrtSc",            "Screenshot"),
        ("Shift+PrtSc",      "Screenshot region"),
    ],
    "Alacritty": [
        ("Ctrl+Shift+C",     "Copy"),
        ("Ctrl+Shift+V",     "Paste"),
        ("Ctrl+Shift++",     "Increase font size"),
        ("Ctrl+-",           "Decrease font size"),
        ("Ctrl+0",           "Reset font size"),
        ("Ctrl+Backspace",   "Delete whole word"),
        ("Ctrl+Shift+Space", "Enter vi mode"),
        ("Ctrl+D",           "Close pane / exit"),
    ],
}

# ── App ────────────────────────────────────────────────────────────────

def slugify(s: str) -> str:
    """Make a string safe to use as a textual widget id."""
    return "".join(c if c.isalnum() or c in "-_" else "-" for c in s)


class CheatApp(App):

    CSS = f"""
    * {{
        background-tint: {BG};
    }}

    Screen {{
        background: {BG};
    }}

    #titlebar {{
        height: 1;
        color: {MAUVE};
        content-align: center middle;
    }}

    #main {{
        height: 1fr;
        padding: 0 1;
    }}

    #category-list {{
        width: 26;
        border: round {SURFACE1};
        border-title-color: {OVERLAY0};
        border-title-style: bold;
        margin-right: 1;
        scrollbar-size-horizontal: 0;
    }}

    #category-list:focus {{
        border: round {MAUVE};
        border-title-color: {MAUVE};
    }}

    ListItem {{
        padding: 0 1;
        color: {SUBTEXT1};
    }}

    ListItem:hover {{
        color: {TEXT};
    }}

    ListItem.--highlight {{
        color: {MAUVE};
        text-style: bold;
    }}

    ListItem.section-header {{
        padding: 1 1 0 1;
        color: {OVERLAY2};
        text-style: bold;
    }}

    ListItem.section-header.--highlight {{
        color: {OVERLAY2};
    }}

    ListItem.section-header:hover {{
        color: {OVERLAY2};
    }}

    #right {{
        width: 1fr;
        border: round {SURFACE1};
        border-title-color: {OVERLAY0};
        border-title-style: bold;
    }}

    #right:focus-within {{
        border: round {MAUVE};
        border-title-color: {MAUVE};
    }}

    DataTable {{
        height: 1fr;
        background: {BG};
    }}

    DataTable > .datatable--header {{
        background: {BG};
        color: {LAVENDER};
        text-style: bold;
    }}

    DataTable > .datatable--header-cursor {{
        background: {BG};
        color: {LAVENDER};
    }}

    DataTable > .datatable--cursor {{
        background: {BG};
        color: {MAUVE};
        text-style: bold;
    }}

    DataTable > .datatable--hover {{
        background: {BG};
    }}

    DataTable > .datatable--odd-row {{
        background: {BG};
    }}

    DataTable > .datatable--even-row {{
        background: {BG};
    }}

    #search-bar {{
        height: 3;
        display: none;
    }}

    #search-bar.active {{
        display: block;
    }}

    #search-input {{
        color: {TEXT};
        border: round {SURFACE1};
    }}

    #search-input:focus {{
        border: round {MAUVE};
    }}

    Footer {{
        dock: bottom;
        height: 1;
        color: {SUBTEXT0};
    }}

    FooterKey {{
        color: {SUBTEXT0};
    }}

    FooterKey > .footer-key--key {{
        color: {MAUVE};
        text-style: bold;
    }}

    FooterKey > .footer-key--description {{
        color: {SUBTEXT0};
    }}
    """

    BINDINGS = [
        Binding("q",       "quit",          "Quit"),
        Binding("/",       "toggle_search", "Search"),
        Binding("l",       "focus_table",   "→ Shortcuts"),
        Binding("h",       "focus_list",    "← List"),
        Binding("right",   "focus_table",   "→ Shortcuts", show=False),
        Binding("left",    "focus_list",    "← List",      show=False),
        Binding("escape",  "do_escape",     "Back / Clear", priority=True, show=False),
        Binding("j",       "nav_down",      "↓",  show=False),
        Binding("k",       "nav_up",        "↑",  show=False),
    ]

    def __init__(self, initial_sheet: str | None = None, initial_search: str = ""):
        super().__init__()
        self._initial_sheet  = initial_sheet
        self._initial_search = initial_search
        self._current_sheet: str | None = None
        self._current_cat:   str | None = None
        self._search_active  = False

    # ── Layout ────────────────────────────────────────────────────────

    def compose(self) -> ComposeResult:
        yield Static(
            f"[bold {MAUVE}] cheat[/]  [dim {OVERLAY0}]Catppuccin Frappé[/]",
            id="titlebar",
        )

        items: list[ListItem] = []
        items.append(ListItem(
            Label(f"[bold {MAUVE}] VS Code[/]"),
            id="hdr-vscode", classes="section-header",
        ))
        for cat in VSCODE:
            items.append(ListItem(
                Label(f"  {cat}"),
                id=f"vscode__{slugify(cat)}",
            ))
        items.append(ListItem(
            Label(f"[bold {MAUVE}] PC & Apps[/]"),
            id="hdr-pc", classes="section-header",
        ))
        for cat in PC:
            items.append(ListItem(
                Label(f"  {cat}"),
                id=f"pc__{slugify(cat)}",
            ))

        with Horizontal(id="main"):
            yield ListView(*items, id="category-list")
            with Vertical(id="right"):
                yield DataTable(id="shortcuts-table", cursor_type="row")
                with Vertical(id="search-bar"):
                    yield Input(placeholder=" type to filter…", id="search-input")

        yield Footer()

    def on_mount(self) -> None:
        self._build_slug_map()

        self.query_one("#category-list").border_title = "categories"
        self.query_one("#right").border_title = "shortcuts"

        table = self.query_one("#shortcuts-table", DataTable)
        table.add_column("Shortcut",    key="key",  width=26)
        table.add_column("Description", key="desc")

        if self._initial_sheet == "pc":
            self._load_category("pc", next(iter(PC)))
        else:
            self._load_category("vscode", next(iter(VSCODE)))

        if self._initial_search:
            self._open_search(prefill=self._initial_search)

        self.query_one("#category-list", ListView).focus()

    # ── Data loading ──────────────────────────────────────────────────

    def _load_category(self, sheet: str, category: str) -> None:
        self._current_sheet = sheet
        self._current_cat   = category
        self.query_one("#right").border_title = category
        self._refresh_table()

    def _refresh_table(self) -> None:
        table = self.query_one("#shortcuts-table", DataTable)
        table.clear()

        if not self._current_sheet or not self._current_cat:
            return

        search = ""
        if self._search_active:
            search = self.query_one("#search-input", Input).value.lower().strip()

        data    = VSCODE if self._current_sheet == "vscode" else PC
        entries = data.get(self._current_cat, [])
        color   = CAT_COLORS.get(self._current_cat, MAUVE)

        for key, desc in entries:
            if not search or search in key.lower() or search in desc.lower():
                table.add_row(
                    f"[bold {color}]{key}[/]",
                    f"[{SUBTEXT1}]{desc}[/]",
                )

    # ── Event handlers ────────────────────────────────────────────────

    # slug → real category name lookup built at class level
    _SLUG_TO_CAT: dict[str, tuple[str, str]] = {}

    def _build_slug_map(self) -> None:
        for cat in VSCODE:
            self._SLUG_TO_CAT[f"vscode__{slugify(cat)}"] = ("vscode", cat)
        for cat in PC:
            self._SLUG_TO_CAT[f"pc__{slugify(cat)}"] = ("pc", cat)

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        item_id = event.item.id or ""
        entry = self._SLUG_TO_CAT.get(item_id)
        if entry:
            self._load_category(*entry)
            # move focus to table so user can scroll with arrows/j/k
            self.query_one("#shortcuts-table", DataTable).focus()

    @on(Input.Changed, "#search-input")
    def _on_search_changed(self, _: Input.Changed) -> None:
        self._refresh_table()

    @on(Input.Submitted, "#search-input")
    def _on_search_submitted(self, _: Input.Submitted) -> None:
        self.query_one("#category-list", ListView).focus()

    # ── Actions ───────────────────────────────────────────────────────

    def _open_search(self, prefill: str = "") -> None:
        self._search_active = True
        self.query_one("#search-bar").add_class("active")
        inp = self.query_one("#search-input", Input)
        inp.value = prefill
        inp.focus()

    def _close_search(self) -> None:
        self._search_active = False
        self.query_one("#search-bar").remove_class("active")
        self.query_one("#search-input", Input).value = ""
        self._refresh_table()
        self.query_one("#category-list", ListView).focus()

    def action_toggle_search(self) -> None:
        if self._search_active:
            self._close_search()
        else:
            self._open_search()

    def action_do_escape(self) -> None:
        if self._search_active:
            self._close_search()
        else:
            # always return focus to the list
            self.query_one("#category-list", ListView).focus()

    def action_nav_down(self) -> None:
        focused = self.focused
        if isinstance(focused, DataTable):
            focused.action_cursor_down()
        else:
            self.query_one("#category-list", ListView).action_cursor_down()

    def action_nav_up(self) -> None:
        focused = self.focused
        if isinstance(focused, DataTable):
            focused.action_cursor_up()
        else:
            self.query_one("#category-list", ListView).action_cursor_up()

    def action_focus_table(self) -> None:
        self.query_one("#shortcuts-table", DataTable).focus()

    def action_focus_list(self) -> None:
        self.query_one("#category-list", ListView).focus()


# ── Entry point ───────────────────────────────────────────────────────

def main() -> None:
    args = [a.lower() for a in sys.argv[1:]]

    if args and args[0] in ("help", "-h", "--help"):
        print("Usage:")
        print("  cheat              open interactive viewer")
        print("  cheat vscode       start on VS Code tab")
        print("  cheat pc           start on PC & Apps tab")
        print("  cheat <term>       open with search pre-filled")
        print("  cheat vscode <t>   start on VS Code with search")
        sys.exit(0)

    initial_sheet  = None
    initial_search = ""

    if args:
        if args[0] in ("vscode", "pc"):
            initial_sheet  = args[0]
            initial_search = " ".join(args[1:])
        else:
            initial_search = " ".join(args)

    CheatApp(initial_sheet=initial_sheet, initial_search=initial_search).run()


if __name__ == "__main__":
    main()
