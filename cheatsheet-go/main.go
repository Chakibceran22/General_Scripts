package main

import (
	"fmt"
	"os"
	"strings"

	tea "github.com/charmbracelet/bubbletea"
	"github.com/charmbracelet/lipgloss"
)

// ── Catppuccin Frappé ────────────────────────────────────────────────

var (
	bg       = lipgloss.Color("#303446")
	surface1 = lipgloss.Color("#51576d")
	overlay0 = lipgloss.Color("#737994")
	overlay2 = lipgloss.Color("#949cbb")
	text     = lipgloss.Color("#c6d0f5")
	subtext1 = lipgloss.Color("#b5bfe2")
	subtext0 = lipgloss.Color("#a5adce")
	lavender = lipgloss.Color("#babbf1")
	blue     = lipgloss.Color("#8caaee")
	mauve    = lipgloss.Color("#ca9ee6")
)

// ── Data ─────────────────────────────────────────────────────────────

type entry struct {
	key  string
	desc string
}

type category struct {
	name    string
	section string
	entries []entry
}

var categories = []category{
	{"General", "VS Code", []entry{
		{"Ctrl+Shift+P", "Command palette"},
		{"Ctrl+P", "Quick open file"},
		{"Ctrl+,", "Open settings"},
		{"Ctrl+K Ctrl+S", "Keyboard shortcuts"},
		{"Ctrl+Shift+N", "New window"},
		{"Ctrl+W", "Close editor"},
		{"Ctrl+Shift+W", "Close window"},
	}},
	{"Editing", "VS Code", []entry{
		{"Ctrl+D", "Select next occurrence"},
		{"Ctrl+Shift+L", "Select all occurrences"},
		{"Alt+↑/↓", "Move line up/down"},
		{"Shift+Alt+↑/↓", "Copy line up/down"},
		{"Ctrl+Shift+K", "Delete line"},
		{"Ctrl+/", "Toggle comment"},
		{"Ctrl+Space", "Trigger suggestion"},
		{"F2", "Rename symbol"},
		{"Ctrl+.", "Quick fix"},
		{"Tab/Shift+Tab", "Indent/outdent"},
		{"Ctrl+Z", "Undo"},
		{"Ctrl+Shift+Z", "Redo"},
	}},
	{"Navigation", "VS Code", []entry{
		{"Ctrl+Tab", "Cycle open files"},
		{"Ctrl+G", "Go to line"},
		{"F12", "Go to definition"},
		{"Alt+F12", "Peek definition"},
		{"Shift+F12", "Find all references"},
		{"Ctrl+Shift+F", "Search in files"},
		{"Ctrl+H", "Replace in file"},
		{"Ctrl+Shift+H", "Replace in files"},
		{"Ctrl+Shift+O", "Go to symbol"},
	}},
	{"Splits & Tabs", "VS Code", []entry{
		{"Ctrl+\\", "Split editor"},
		{"Ctrl+1/2/3", "Focus split group"},
		{"Ctrl+Shift+T", "Reopen closed editor"},
		{"Ctrl+B", "Toggle sidebar"},
		{"Ctrl+Shift+E", "Explorer"},
		{"Ctrl+Shift+G", "Source control"},
		{"Ctrl+Shift+X", "Extensions"},
		{"Ctrl+Shift+D", "Run & debug"},
	}},
	{"Terminal", "VS Code", []entry{
		{"Ctrl+`", "Toggle terminal"},
		{"Ctrl+J", "Toggle terminal panel"},
		{"Ctrl+Shift+M", "Maximize terminal"},
		{"Ctrl+Shift+`", "New terminal"},
		{"Ctrl+Shift+5", "Split terminal"},
		{"Ctrl+1", "Focus back to editor"},
		{"Alt+↑/↓", "Scroll terminal"},
		{"Ctrl+Shift+W", "Close VS Code window"},
		{"Ctrl+Q", "Quit VS Code"},
	}},
	{"My Shortcuts", "PC & Apps", []entry{
		{"Ctrl+Shift+K", "Open Alacritty terminal"},
		{"Ctrl+Shift+B", "Open Brave browser"},
		{"Ctrl+Shift+L", "Open my app"},
	}},
	{"Brave", "PC & Apps", []entry{
		{"Ctrl+T", "New tab"},
		{"Ctrl+W", "Close tab"},
		{"Ctrl+Shift+T", "Reopen closed tab"},
		{"Ctrl+Tab", "Next tab"},
		{"Ctrl+Shift+Tab", "Previous tab"},
		{"Ctrl+1..8", "Jump to tab N"},
		{"Ctrl+9", "Jump to last tab"},
		{"Ctrl+L", "Focus address bar"},
		{"Ctrl+R", "Reload page"},
		{"Ctrl+Shift+R", "Hard reload (no cache)"},
		{"Ctrl+F", "Find on page"},
		{"Ctrl+D", "Bookmark page"},
		{"Ctrl+H", "History"},
		{"Ctrl+J", "Downloads"},
		{"Ctrl+Shift+N", "New incognito window"},
		{"Ctrl++/Ctrl+-", "Zoom in/out"},
		{"Ctrl+0", "Reset zoom"},
		{"F11", "Fullscreen"},
		{"Ctrl+U", "View page source"},
		{"F12", "DevTools"},
	}},
	{"KDE / Kubuntu", "PC & Apps", []entry{
		{"Meta", "App launcher (KRunner)"},
		{"Meta+D", "Show desktop"},
		{"Meta+M", "Maximize window (custom)"},
		{"Meta+PgUp", "Maximize window (default)"},
		{"Meta+PgDn", "Restore window (default)"},
		{"Meta+←/→", "Snap window left/right"},
		{"Meta+↑/↓", "Tile window top/bottom"},
		{"Meta+Shift+←/→", "Move to other screen"},
		{"Alt+F4", "Close window"},
		{"Alt+Tab", "Switch windows"},
		{"Alt+F2", "KRunner (run command)"},
		{"Ctrl+Alt+T", "Open terminal"},
		{"PrtSc", "Screenshot"},
		{"Shift+PrtSc", "Screenshot region"},
	}},
	{"Alacritty", "PC & Apps", []entry{
		{"Ctrl+Shift+C", "Copy"},
		{"Ctrl+Shift+V", "Paste"},
		{"Ctrl+Shift++", "Increase font size"},
		{"Ctrl+-", "Decrease font size"},
		{"Ctrl+0", "Reset font size"},
		{"Ctrl+Backspace", "Delete whole word"},
		{"Ctrl+Shift+Space", "Enter vi mode"},
		{"Ctrl+D", "Close pane / exit"},
	}},
}

// ── Model ────────────────────────────────────────────────────────────

type focus int

const (
	focusList focus = iota
	focusTable
)

type model struct {
	focus       focus
	cursor      int
	tableCursor int
	width       int
	height      int
}

func initialModel() model {
	return model{focus: focusList, cursor: 0, tableCursor: 0}
}

func (m model) Init() tea.Cmd { return nil }

// ── Update ───────────────────────────────────────────────────────────

func (m model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
	switch msg := msg.(type) {
	case tea.WindowSizeMsg:
		m.width = msg.Width
		m.height = msg.Height

	case tea.KeyMsg:
		switch msg.String() {
		case "q", "ctrl+c":
			return m, tea.Quit

		case "j", "down":
			if m.focus == focusList {
				if m.cursor < len(categories)-1 {
					m.cursor++
				}
				m.tableCursor = 0
			} else {
				entries := categories[m.cursor].entries
				if m.tableCursor < len(entries)-1 {
					m.tableCursor++
				}
			}

		case "k", "up":
			if m.focus == focusList {
				if m.cursor > 0 {
					m.cursor--
				}
				m.tableCursor = 0
			} else {
				if m.tableCursor > 0 {
					m.tableCursor--
				}
			}

		case "l", "right", "enter":
			if m.focus == focusList {
				m.focus = focusTable
				m.tableCursor = 0
			}

		case "h", "left", "esc":
			if m.focus == focusTable {
				m.focus = focusList
			}
		}
	}
	return m, nil
}

// ── View ─────────────────────────────────────────────────────────────

func (m model) View() string {
	if m.width == 0 {
		return ""
	}

	sideW := 24
	rightW := m.width - sideW - 5 // borders + margin
	if rightW < 20 {
		rightW = 20
	}
	contentH := m.height - 4 // title + footer + borders

	// ── Left panel ──────────────────────────────────
	var listItems []string
	lastSection := ""
	for i, cat := range categories {
		if cat.section != lastSection {
			if lastSection != "" {
				listItems = append(listItems, "")
			}
			header := lipgloss.NewStyle().
				Foreground(mauve).
				Bold(true).
				Render(cat.section)
			listItems = append(listItems, header)
			lastSection = cat.section
		}

		name := "  " + cat.name
		style := lipgloss.NewStyle().Foreground(blue)
		if i == m.cursor {
			style = lipgloss.NewStyle().Foreground(mauve).Bold(true)
		}
		listItems = append(listItems, style.Render(name))
	}

	listContent := strings.Join(listItems, "\n")

	leftBorderColor := surface1
	leftTitleColor := overlay0
	if m.focus == focusList {
		leftBorderColor = mauve
		leftTitleColor = mauve
	}

	leftPanel := renderPanel("categories", listContent, sideW, contentH, leftBorderColor, leftTitleColor)

	// ── Right panel ─────────────────────────────────
	cat := categories[m.cursor]
	keyW := 22

	var rows []string
	// header
	hdrKey := lipgloss.NewStyle().
		Width(keyW).
		Foreground(lavender).
		Bold(true).
		Render("Shortcut")
	hdrDesc := lipgloss.NewStyle().
		Foreground(lavender).
		Bold(true).
		Render("Description")
	rows = append(rows, hdrKey+hdrDesc)

	for i, e := range cat.entries {
		keyStyle := lipgloss.NewStyle().Width(keyW).Foreground(blue)
		descStyle := lipgloss.NewStyle().Foreground(subtext1)

		if m.focus == focusTable && i == m.tableCursor {
			keyStyle = keyStyle.Foreground(mauve).Bold(true)
			descStyle = descStyle.Foreground(text).Bold(true)
		}

		rows = append(rows, keyStyle.Render(e.key)+descStyle.Render(e.desc))
	}

	tableContent := strings.Join(rows, "\n")

	rightBorderColor := surface1
	rightTitleColor := overlay0
	if m.focus == focusTable {
		rightBorderColor = mauve
		rightTitleColor = mauve
	}

	rightPanel := renderPanel(cat.name, tableContent, rightW, contentH, rightBorderColor, rightTitleColor)

	// ── Title bar ───────────────────────────────────
	title := lipgloss.NewStyle().
		Width(m.width).
		Align(lipgloss.Center).
		Render(
			lipgloss.NewStyle().Foreground(mauve).Bold(true).Render("cheat") +
				lipgloss.NewStyle().Foreground(overlay0).Render("  Catppuccin Frappé"))

	// ── Footer ──────────────────────────────────────
	footerParts := []string{
		renderKey("q", "quit"),
		renderKey("j/k", "navigate"),
		renderKey("h/l", "switch panel"),
		renderKey("enter", "select"),
		renderKey("/", "search"),
		renderKey("esc", "back"),
	}
	footer := lipgloss.NewStyle().
		Width(m.width).
		Foreground(subtext0).
		Render(" " + strings.Join(footerParts, "  "))

	// ── Compose ─────────────────────────────────────
	body := lipgloss.JoinHorizontal(lipgloss.Top, leftPanel, " ", rightPanel)

	return title + "\n" + body + "\n" + footer
}

func renderKey(key, desc string) string {
	k := lipgloss.NewStyle().Foreground(mauve).Bold(true).Render(key)
	d := lipgloss.NewStyle().Foreground(subtext0).Render(" " + desc)
	return k + d
}

func renderPanel(title, content string, w, h int, borderColor, titleColor lipgloss.Color) string {
	bs := lipgloss.NewStyle().Foreground(borderColor)
	ts := lipgloss.NewStyle().Foreground(titleColor).Bold(true)

	titleRendered := ts.Render(" " + title + " ")
	titleW := lipgloss.Width(titleRendered)
	fill := w - 3 - titleW // corner + dash + title + fill + corner
	if fill < 0 {
		fill = 0
	}
	top := bs.Render("╭─") + titleRendered + bs.Render(strings.Repeat("─", fill)+"╮")

	innerW := w - 2
	lines := strings.Split(content, "\n")
	var body strings.Builder
	for i := 0; i < h; i++ {
		line := ""
		if i < len(lines) {
			line = lines[i]
		}
		pad := innerW - lipgloss.Width(line)
		if pad < 0 {
			pad = 0
		}
		body.WriteString(bs.Render("│") + line + strings.Repeat(" ", pad) + bs.Render("│") + "\n")
	}

	bottom := bs.Render("╰" + strings.Repeat("─", innerW) + "╯")
	return top + "\n" + body.String() + bottom
}

// ── Main ─────────────────────────────────────────────────────────────

func main() {
	p := tea.NewProgram(
		initialModel(),
		tea.WithAltScreen(),
	)
	if _, err := p.Run(); err != nil {
		fmt.Fprintf(os.Stderr, "Error: %v\n", err)
		os.Exit(1)
	}
}
