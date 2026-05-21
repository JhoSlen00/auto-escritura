# Author: JhoSlen00

import tkinter as tk
import threading
import time
import pyautogui
from PIL import Image, ImageDraw, ImageFont, ImageTk

# Window background colors
GRIS = "#3C3C3C"
GRIS_CLARO = "#5A5A5A"

SPEED_PRESETS = [
    ("Very Slow", 0.15),
    ("Slow",      0.08),
    ("Normal",    0.03),
    ("Fast",      0.01),
    ("Turbo",     0.003),
]
speed_idx = 2      # default: Normal
speed_window = None

# Event flag used to signal the typing thread to stop
detener = threading.Event()


def iniciar_escritura():
    # Get text from the text area, stripping leading/trailing whitespace
    texto = cuadro_texto.get("1.0", tk.END).strip()
    if not texto:
        estado_label.config(text="Type something first.", fg="red")
        return

    # Read the wait time; fall back to 3 seconds if the field is empty or invalid
    try:
        segundos = int(espera_entry.get())
    except ValueError:
        segundos = 3

    detener.clear()
    estado_label.config(text=f"You have {segundos} seconds to click where you want to type...", fg="orange")
    btn_escribir.config(state="disabled")
    btn_detener.config(state="normal")

    def escribir():
        # Wait for the user to focus the target field
        time.sleep(segundos)

        # Split text by | to support typing across multiple fields with Tab
        partes = texto.split("|")
        for i, parte in enumerate(partes):
            if detener.is_set():
                break
            for char in parte:
                if detener.is_set():
                    break
                if ord(char) < 128:
                    # ASCII characters are typed directly
                    pyautogui.typewrite(char, interval=SPEED_PRESETS[speed_idx][1])
                else:
                    # Non-ASCII characters (accents, symbols) are pasted via clipboard
                    ventana.clipboard_clear()
                    ventana.clipboard_append(char)
                    ventana.update()
                    pyautogui.hotkey('ctrl', 'v')
                    time.sleep(0.05)

            # Press Tab between sections to move to the next field
            if i < len(partes) - 1 and not detener.is_set():
                pyautogui.press("tab")

        if detener.is_set():
            estado_label.config(text="Stopped.", fg="red")
        else:
            estado_label.config(text="Done!", fg="green")
        btn_escribir.config(state="normal")
        btn_detener.config(state="disabled")

    # Run typing in a background thread so the UI stays responsive
    threading.Thread(target=escribir, daemon=True).start()


def detener_escritura():
    # Signal the typing thread to stop at the next character
    detener.set()


def toggle_speed_window():
    global speed_window
    if speed_window is not None and speed_window.winfo_exists():
        speed_window.destroy()
        speed_window = None
        return

    speed_window = tk.Toplevel(ventana)
    speed_window.title("Typing Speed")
    speed_window.resizable(True, True)
    speed_window.configure(bg=GRIS)
    speed_window.transient(ventana)

    ventana.update_idletasks()
    wx = ventana.winfo_x() + (ventana.winfo_width() - 320) // 2
    wy = ventana.winfo_y() + 55
    speed_window.geometry(f"320x118+{wx}+{wy}")

    name_var = tk.StringVar(value=SPEED_PRESETS[speed_idx][0])
    ms_var   = tk.StringVar(value=f"{int(SPEED_PRESETS[speed_idx][1] * 1000)} ms / key")

    timeline = tk.Canvas(speed_window, width=300, height=42, bg=GRIS, highlightthickness=0)

    def draw_timeline():
        timeline.delete("all")
        n = len(SPEED_PRESETS)
        margin, cy = 24, 15
        step = (300 - 2 * margin) / (n - 1)
        timeline.create_line(margin, cy, 300 - margin, cy, fill="#555555", width=2)
        if speed_idx > 0:
            timeline.create_line(margin, cy, margin + speed_idx * step, cy,
                                  fill="#FF6666", width=3)
        for i, (label, _) in enumerate(SPEED_PRESETS):
            x = margin + i * step
            r = 7 if i == speed_idx else 4
            color = "#FF6666" if i <= speed_idx else "#666666"
            timeline.create_oval(x - r, cy - r, x + r, cy + r, fill=color, outline="")
            timeline.create_text(x, 34, text=label.split()[0],
                                  fill="#DDDDDD" if i <= speed_idx else "#888888",
                                  font=("Arial", 7))

    def change_speed(delta):
        global speed_idx
        speed_idx = max(0, min(len(SPEED_PRESETS) - 1, speed_idx + delta))
        name_var.set(SPEED_PRESETS[speed_idx][0])
        ms_var.set(f"{int(SPEED_PRESETS[speed_idx][1] * 1000)} ms / key")
        draw_timeline()

    row = tk.Frame(speed_window, bg=GRIS)
    row.pack(pady=(10, 4))

    tk.Button(row, text="◀", font=("Arial", 11), bg=GRIS_CLARO, fg="white",
              relief="flat", bd=0, padx=8, pady=3,
              command=lambda: change_speed(-1)).pack(side="left", padx=6)

    info = tk.Frame(row, bg=GRIS)
    info.pack(side="left", padx=4)
    tk.Label(info, textvariable=name_var, font=("Arial", 11, "bold"),
             bg=GRIS, fg="white", width=9).pack()
    tk.Label(info, textvariable=ms_var, font=("Arial", 8),
             bg=GRIS, fg="#AAAAAA").pack()

    tk.Button(row, text="▶", font=("Arial", 11), bg=GRIS_CLARO, fg="white",
              relief="flat", bd=0, padx=8, pady=3,
              command=lambda: change_speed(+1)).pack(side="left", padx=6)

    timeline.pack(pady=(0, 4))
    draw_timeline()


def crear_icono():
    # Generate a 64x64 pastel green circle with a white K for the window icon
    size = 64
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse([2, 2, size - 3, size - 3], fill=(152, 214, 152))
    try:
        font = ImageFont.truetype("arialbd.ttf", 40)
    except Exception:
        font = ImageFont.load_default()
    draw.text((size // 2, size // 2), "K", fill="white", font=font, anchor="mm")
    return ImageTk.PhotoImage(img)


# Main window setup
ventana = tk.Tk()
ventana.title("KODO")
ventana.geometry("600x520")
ventana.resizable(True, True)
ventana.configure(bg=GRIS)
icono = crear_icono()
ventana.iconphoto(True, icono)

# Top bar: section label + speed button
frame_top = tk.Frame(ventana, bg=GRIS)
frame_top.pack(fill="x", padx=15, pady=(15, 5))
tk.Label(frame_top, text="TEXT TO TYPE", font=("Arial", 11), bg=GRIS, fg="white").pack(side="left")
tk.Button(frame_top, text="⚡ Speed", font=("Arial", 9), bg=GRIS_CLARO, fg="white",
          relief="flat", bd=0, padx=7, pady=2,
          command=toggle_speed_window).pack(side="right")

# Canvas used to render a rounded rectangle background behind the text area
canvas_cuadro = tk.Canvas(ventana, bg=GRIS, highlightthickness=0)
canvas_cuadro.pack(padx=15, pady=5, fill="both", expand=True)

# Text input area where the user writes the text to be typed
cuadro_texto = tk.Text(canvas_cuadro, font=("Arial", 10),
                       bg=GRIS_CLARO, fg="white", insertbackground="white",
                       relief="flat", bd=0)

txt_win = canvas_cuadro.create_window(12, 12, window=cuadro_texto, anchor="nw")


def _resize_canvas(event):
    # Redraws the rounded rectangle and resizes the text widget when the window is resized
    w, h, pad, r = event.width, event.height, 4, 16
    canvas_cuadro.delete("bg")
    canvas_cuadro.create_arc(pad, pad, pad+2*r, pad+2*r, start=90, extent=90, fill=GRIS_CLARO, outline="", style="pieslice", tags="bg")
    canvas_cuadro.create_arc(w-pad-2*r, pad, w-pad, pad+2*r, start=0, extent=90, fill=GRIS_CLARO, outline="", style="pieslice", tags="bg")
    canvas_cuadro.create_arc(pad, h-pad-2*r, pad+2*r, h-pad, start=180, extent=90, fill=GRIS_CLARO, outline="", style="pieslice", tags="bg")
    canvas_cuadro.create_arc(w-pad-2*r, h-pad-2*r, w-pad, h-pad, start=270, extent=90, fill=GRIS_CLARO, outline="", style="pieslice", tags="bg")
    canvas_cuadro.create_rectangle(pad+r, pad, w-pad-r, h-pad, fill=GRIS_CLARO, outline="", tags="bg")
    canvas_cuadro.create_rectangle(pad, pad+r, w-pad, h-pad-r, fill=GRIS_CLARO, outline="", tags="bg")
    canvas_cuadro.tag_lower("bg")
    canvas_cuadro.itemconfig(txt_win, width=w-2*pad-16, height=h-2*pad-16)
    canvas_cuadro.coords(txt_win, pad+8, pad+8)


canvas_cuadro.bind("<Configure>", _resize_canvas)

# Wait time row: label + numeric-only entry
frame = tk.Frame(ventana, bg=GRIS)
frame.pack(pady=8)
tk.Label(frame, text="Wait (seconds):", font=("Arial", 10), bg=GRIS, fg="white").pack(side="left")

# Validator that blocks any non-numeric input
solo_numeros = ventana.register(lambda val: val.isdigit() or val == "")
espera_entry = tk.Entry(frame, width=5, font=("Arial", 10), bg=GRIS_CLARO, fg="white",
                        insertbackground="white", relief="flat", bd=0,
                        validate="key", validatecommand=(solo_numeros, "%P"))
espera_entry.insert(0, "3")
espera_entry.pack(side="left", padx=5)

# Button row
frame_botones = tk.Frame(ventana, bg=GRIS)
frame_botones.pack(pady=5)

# Type button: starts the auto-typing process
btn_escribir = tk.Button(frame_botones, text="Type", font=("Arial", 11),
                         bg="#FF6666", fg="white", padx=10, pady=5,
                         relief="flat", bd=0, highlightthickness=0,
                         command=iniciar_escritura)
btn_escribir.pack(side="left", padx=5)

# Stop button: cancels typing mid-process
btn_detener = tk.Button(frame_botones, text="Stop", font=("Arial", 11),
                        bg="#555555", fg="white", padx=10, pady=5,
                        relief="flat", bd=0, highlightthickness=0,
                        state="disabled", command=detener_escritura)
btn_detener.pack(side="left", padx=5)

# Clear text button: wipes the text area
btn_limpiar = tk.Button(frame_botones, text="Clear text", font=("Arial", 11),
                        bg="#444444", fg="white", padx=10, pady=5,
                        relief="flat", bd=0, highlightthickness=0,
                        command=lambda: cuadro_texto.delete("1.0", tk.END))
btn_limpiar.pack(side="right", padx=5)

# TAB button: inserts a | separator so the app presses Tab between fields
btn_tab = tk.Button(frame_botones, text="TAB", font=("Arial", 11),
                    bg="#2E7D32", fg="white", padx=10, pady=5,
                    relief="flat", bd=0, highlightthickness=0,
                    command=lambda: cuadro_texto.insert(tk.INSERT, "\n|\n"))
btn_tab.pack(side="left", padx=5)

# Status bar: shows countdown, done, or error messages
estado_label = tk.Label(ventana, text="", font=("Arial", 10), bg=GRIS, fg="white")
estado_label.pack()

ventana.mainloop()
