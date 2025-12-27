DARK = {
    "bg": "#1e1e1e",
    "fg": "#ffffff",
    "entry_bg": "#2e2e2e",
    "btn_bg": "#3a3a3a"
}

LIGHT = {
    "bg": "#f4f4f4",
    "fg": "#000000",
    "entry_bg": "#ffffff",
    "btn_bg": "#dddddd"
}

current = LIGHT

def toggle():
    global current
    current = DARK if current == LIGHT else LIGHT
