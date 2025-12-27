import theme
import tkinter as tk

def apply_theme(widget):
    try:
        widget.configure(bg=theme.current["bg"])
    except:
        pass

    for child in widget.winfo_children():
        try:
            if isinstance(child, tk.Entry):
                child.configure(
                    bg=theme.current["entry_bg"],
                    fg=theme.current["fg"],
                    insertbackground=theme.current["fg"]
                )
            elif isinstance(child, tk.Button):
                child.configure(
                    bg=theme.current["btn_bg"],
                    fg=theme.current["fg"]
                )
            else:
                child.configure(
                    bg=theme.current["bg"],
                    fg=theme.current["fg"]
                )
        except:
            pass

        apply_theme(child)
