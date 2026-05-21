# Author: JhoSlen00

import tkinter as tk
import threading
import time
import pyautogui
from PIL import Image, ImageDraw, ImageFont, ImageTk

# Window background colors
GRIS = "#3C3C3C"
GRIS_CLARO = "#5A5A5A"

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
                    pyautogui.typewrite(char, interval=0.03)
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

# Section label above the text area
tk.Label(ventana, text="TEXT TO TYPE", font=("Arial", 11), bg=GRIS, fg="white").pack(pady=(15, 5))

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
