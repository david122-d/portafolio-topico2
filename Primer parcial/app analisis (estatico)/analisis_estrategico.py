#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analisis Estrategico 360 - Version texto fijo (sin IA)
-------------------------------------------------------
Aplicacion de escritorio (Tkinter) que analiza un texto predeterminado
(de solo lectura) y muestra:
  - Analisis FODA
  - Seis Sombreros para Pensar
  - Diagrama de Ishikawa (con sub-causas)
  - Diagrama de Pareto
  - Analisis CATWOE

No usa ninguna API ni conexion a internet: todo el analisis esta
definido en la seccion "ANALISIS DEL TEXTO PREDETERMINADO".
"""

import os
import tkinter as tk
from tkinter import ttk

# ----------------------------------------------------------------------
# PALETA DE COLORES Y ESTILO
# ----------------------------------------------------------------------
BG = "#F5F6FA"
CARD_BG = "#FFFFFF"
DARK = "#2D3436"
PURPLE = "#6C5CE7"
TURQUOISE = "#00CEC9"
CORAL = "#FF6B6B"
YELLOW = "#FDCB6E"
GREEN = "#00B894"
BLUE = "#0984E3"
GREY = "#B2BEC3"
NAVBAR_BG = "#EDEBFF"

FONT_TITLE = ("Segoe UI", 22, "bold")
FONT_SUB = ("Segoe UI", 12)
FONT_BTN = ("Segoe UI", 12, "bold")
FONT_CARD_TITLE = ("Segoe UI", 14, "bold")
FONT_CARD_TEXT = ("Segoe UI", 10)

WIN_W, WIN_H = 1020, 700
COLORS = [PURPLE, TURQUOISE, CORAL, YELLOW, GREEN, BLUE]

# ----------------------------------------------------------------------
# IMAGENES: LOGO Y FOTO DEL CREADOR
# ----------------------------------------------------------------------
LOGO_PATH = "logo.png"
CREATOR_PHOTO_PATH = "creador.png"

try:
    from PIL import Image, ImageTk, ImageOps
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


def _load_round_image(path, size):
    if not path or not os.path.exists(path):
        return None
    try:
        if PIL_AVAILABLE:
            img = Image.open(path).convert("RGBA").resize((size, size))
            return ImageTk.PhotoImage(img)
        return tk.PhotoImage(file=path)
    except Exception:
        return None


def load_creator_image_3to2(path, target_width, target_height):
    if not path or not os.path.exists(path):
        return None
    try:
        if PIL_AVAILABLE:
            img = Image.open(path).convert("RGBA")
            img = ImageOps.fit(img, (target_width, target_height),
                               Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(img)
        return tk.PhotoImage(file=path)
    except Exception:
        return None


# ----------------------------------------------------------------------
# ANALISIS DEL TEXTO PREDETERMINADO (todo definido a mano, sin IA)
# ----------------------------------------------------------------------
DEFAULT_TEXT = (
    "Nuestra empresa de desarrollo de software ha experimentado un "
    "crecimiento rápido en el último año. Sin embargo, enfrentamos "
    "problemas de alta rotación de personal debido a la sobrecarga de "
    "trabajo. La calidad de nuestro producto principal es excelente y los "
    "clientes están muy satisfechos, pero nuestra infraestructura de "
    "servidores se ha vuelto obsoleta, causando caídas frecuentes. "
    "Además, ha surgido un nuevo competidor agresivo en el mercado con "
    "precios más bajos. A nivel interno, carecemos de procesos "
    "documentados. Tenemos la oportunidad de expandirnos al mercado "
    "internacional si logramos estabilizar nuestro equipo."
)

# Datos clave del texto. "foda" = cuadrante FODA, "m" = categoria de las 6M
# (Ishikawa) y "subs" = sub-causas que salen de cada escama. Los pesos suman 100.
ITEMS = [
    {"name": "Rotación de personal", "value": 22, "foda": "Debilidades",
     "m": "Mano de obra",
     "subs": ["Sobrecarga de trabajo", "Equipo agotado"]},
    {"name": "Falta de procesos", "value": 10, "foda": "Debilidades",
     "m": "Método",
     "subs": ["Procesos sin documentar", "Conocimiento en pocas personas"]},
    {"name": "Infraestructura obsoleta", "value": 18, "foda": "Debilidades",
     "m": "Maquinaria",
     "subs": ["Servidores sin renovar", "Caídas frecuentes"]},
    {"name": "Calidad del producto", "value": 22, "foda": "Fortalezas",
     "m": "Material",
     "subs": ["Producto principal sólido", "Clientes muy satisfechos"]},
    {"name": "Expansión internacional", "value": 14, "foda": "Oportunidades",
     "m": "Medición",
     "subs": ["Sin métricas de preparación", "Depende de estabilizar al equipo"]},
    {"name": "Competidor agresivo", "value": 14, "foda": "Amenazas",
     "m": "Medio ambiente",
     "subs": ["Precios más bajos", "Nuevo en el mercado"]},
]

FODA_RECOS = {
    "Fortalezas": "Usar la calidad y la satisfacción de los clientes como argumento de venta frente al competidor de bajo precio.",
    "Debilidades": "Reducir la sobrecarga del equipo, modernizar los servidores y documentar los procesos clave.",
    "Oportunidades": "Preparar un piloto internacional cuando el equipo y la infraestructura estén estables.",
    "Amenazas": "Diferenciarse por calidad y estabilidad del servicio en lugar de competir solo por precio.",
}

# (letra, nombre, descripcion, factor relacionado, interpretacion)
CATWOE = [
    ("C", "Clientes", "Quienes reciben el beneficio o impacto", "Calidad del producto",
     "Clientes satisfechos que sufren las caídas del servicio."),
    ("A", "Actores", "Quienes ejecutan la transformacion", "Rotación de personal",
     "El equipo de desarrollo, hoy sobrecargado y con alta rotación."),
    ("T", "Transformacion", "El proceso de cambio central", "Falta de procesos",
     "Pasar de una operación improvisada a una documentada y estable."),
    ("W", "Weltanschauung", "La vision o creencia que da sentido", "Expansión internacional",
     "Crecer sin sacrificar la calidad ni al equipo."),
    ("D", "Dueño", "Quien puede detener o autorizar el proceso", "Infraestructura obsoleta",
     "La dirección, que decide la inversión en nuevos servidores."),
    ("E", "Entorno", "Restricciones del contexto", "Competidor agresivo",
     "Un competidor con precios bajos y un mercado internacional por abrir."),
]


def compute_foda(items):
    foda = {"Fortalezas": [], "Debilidades": [], "Oportunidades": [], "Amenazas": []}
    for it in items:
        foda[it["foda"]].append(it)
    return foda


def compute_hats(items):
    ranked = sorted(items, key=lambda i: -i["value"])
    lista = ", ".join(f"{i['name']} ({i['value']} pts)" for i in items)
    orden = " > ".join(i["name"] for i in ranked)
    return {
        "Sombrero Blanco (Datos objetivos)":
            f"Crecimiento rápido en el último año, producto de excelente calidad y "
            f"clientes satisfechos, servidores obsoletos con caídas frecuentes, "
            f"alta rotación, un competidor con precios más bajos y ningún proceso "
            f"documentado. Pesos: {lista}.",
        "Sombrero Rojo (Emociones e intuicion)":
            "Hay orgullo por la calidad y la satisfacción de los clientes, pero "
            "también cansancio y frustración en el equipo por la sobrecarga, y "
            "preocupación por las caídas y el nuevo competidor.",
        "Sombrero Negro (Riesgos y precaucion)":
            "Si la rotación continúa se pierde conocimiento y la sobrecarga empeora; "
            "las caídas pueden costar clientes y la falta de procesos vuelve frágil "
            "cualquier intento de expansión.",
        "Sombrero Amarillo (Beneficios y optimismo)":
            "La calidad del producto y la satisfacción de los clientes son una base "
            "sólida. Estabilizar al equipo abre la puerta a la expansión "
            "internacional.",
        "Sombrero Verde (Creatividad)":
            "Rotar guardias y reservar tiempo para mejora continua, migrar a "
            "infraestructura con redundancia, documentar procesos junto al propio "
            "equipo y probar un piloto en un solo mercado extranjero.",
        "Sombrero Azul (Control del proceso)":
            f"Orden de atención por peso: {orden}. Plan sugerido: 1) estabilizar "
            f"al equipo, 2) modernizar la infraestructura, 3) documentar procesos, "
            f"4) responder al competidor, 5) planear la expansión.",
    }


def compute_pareto(items):
    ranked = sorted(items, key=lambda i: -i["value"])
    total = sum(i["value"] for i in ranked) or 1
    cum = 0
    rows = []
    for i in ranked:
        cum += i["value"]
        rows.append({"name": i["name"], "value": i["value"],
                     "pct": i["value"] / total * 100, "cum": cum / total * 100})
    return rows


# ----------------------------------------------------------------------
# UTILIDADES DE DIBUJO Y COMPONENTES UI
# ----------------------------------------------------------------------
def rounded_rect(canvas, x1, y1, x2, y2, r=22, **kwargs):
    points = [
        x1 + r, y1, x2 - r, y1, x2, y1, x2, y1 + r, x2, y2 - r, x2, y2,
        x2 - r, y2, x1 + r, y2, x1, y2, x1, y2 - r, x1, y1 + r, x1, y1,
    ]
    return canvas.create_polygon(points, smooth=True, **kwargs)


def _darken(hexcolor, factor=0.85):
    hexcolor = hexcolor.lstrip('#')
    r, g, b = tuple(int(hexcolor[i:i + 2], 16) for i in (0, 2, 4))
    return f"#{int(r * factor):02x}{int(g * factor):02x}{int(b * factor):02x}"


class RoundedButton(tk.Canvas):
    def __init__(self, parent, text, command=None, bg=PURPLE, fg="white",
                 width=220, height=52, radius=22, font=FONT_BTN, parent_bg=BG):
        super().__init__(parent, width=width, height=height, bg=parent_bg,
                         highlightthickness=0, cursor="hand2")
        self.command = command
        self.bg = bg
        self.hover_bg = _darken(bg)
        self.radius = radius
        self.text = text
        self.font = font
        self.fg = fg
        self.btn_w, self.btn_h = width, height
        self._draw(bg)
        self.bind("<Button-1>", self._on_click)
        self.bind("<Enter>", lambda e: self._draw(self.hover_bg))
        self.bind("<Leave>", lambda e: self._draw(self.bg))

    def _draw(self, color):
        self.delete("all")
        rounded_rect(self, 2, 2, self.btn_w - 2, self.btn_h - 2,
                     r=self.radius, fill=color, outline=color)
        self.create_text(self.btn_w / 2, self.btn_h / 2, text=self.text,
                         fill=self.fg, font=self.font)

    def _on_click(self, _e):
        if self.command:
            self.command()


def make_card(parent, width, height, bg=CARD_BG, radius=22, parent_bg=BG):
    c = tk.Canvas(parent, width=width, height=height, bg=parent_bg,
                  highlightthickness=0)
    rounded_rect(c, 2, 2, width - 2, height - 2, r=radius, fill=bg, outline=bg)
    inner = tk.Frame(c, bg=bg)
    c.create_window(width / 2, height / 2, window=inner,
                    width=width - 34, height=height - 30)
    return c, inner


class ScrollableFrame(tk.Frame):
    def __init__(self, parent, bg=BG):
        super().__init__(parent, bg=bg)
        canvas = tk.Canvas(self, bg=bg, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas, bg=bg)
        window_id = canvas.create_window((0, 0), window=self.scrollable_frame,
                                         anchor="n")

        def _resize_content(_e=None):
            canvas.configure(scrollregion=canvas.bbox("all"))
            canvas.coords(window_id, canvas.winfo_width() / 2, 0)

        self.scrollable_frame.bind("<Configure>", _resize_content)
        canvas.bind("<Configure>", _resize_content)
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        canvas.bind("<Enter>", lambda e: canvas.bind_all(
            "<MouseWheel>",
            lambda ev: canvas.yview_scroll(int(-1 * (ev.delta / 120)), "units")))
        canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))
        self.canvas = canvas


# ----------------------------------------------------------------------
# WIDGETS COMUNES
# ----------------------------------------------------------------------
def add_logo(frame):
    c = tk.Canvas(frame, width=76, height=76, bg=BG, highlightthickness=0)
    c.place(relx=1.0, x=-14, y=14, anchor="ne")
    img = _load_round_image(LOGO_PATH, 72)
    if img:
        c.image = img
        c.create_image(38, 38, image=img)
    else:
        c.create_oval(4, 4, 72, 72, fill=CARD_BG, outline=PURPLE, width=2,
                      dash=(4, 2))
        c.create_text(38, 38, text="TU\nLOGO", fill=PURPLE,
                      font=("Segoe UI", 9, "bold"), justify="center")
    return c


def add_about_button(frame, controller, parent_bg=BG):
    btn = RoundedButton(frame, text="\u2139",
                        command=lambda: controller.show_frame("AboutScreen"),
                        bg=CORAL, width=54, height=54, radius=27,
                        font=("Segoe UI", 18, "bold"), parent_bg=parent_bg)
    btn.place(relx=1.0, rely=1.0, x=-18, y=-18, anchor="se")
    return btn


def add_back_button(frame, controller, command=None, parent_bg=BG):
    btn = RoundedButton(frame, text="\u2190", command=command or controller.go_back,
                        bg=PURPLE, fg="white", width=54, height=54, radius=27,
                        font=("Segoe UI", 20, "bold"), parent_bg=parent_bg)
    btn.place(x=18, y=18)
    return btn


def add_common_widgets(frame, controller, show_back=True, back_command=None):
    add_logo(frame)
    add_about_button(frame, controller)
    if show_back:
        add_back_button(frame, controller, back_command)


def go_dashboard(controller):
    return lambda: controller.show_frame("Dashboard")


# ----------------------------------------------------------------------
# PANTALLA 1: TEXTO PREDETERMINADO (SOLO LECTURA)
# ----------------------------------------------------------------------
class StartScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG)
        self.controller = controller

        add_logo(self)
        add_about_button(self, controller)

        header = tk.Frame(self, bg=BG)
        header.pack(side="top", fill="x", pady=(40, 10))
        tk.Label(header, text="Analisis Estrategico 360", font=FONT_TITLE,
                 bg=BG, fg=DARK).pack()
        tk.Label(header, text="Este es el contexto que se analizara en los "
                              "diagramas (solo lectura).",
                 font=FONT_SUB, bg=BG, fg=DARK).pack(pady=(5, 10))

        navbar = tk.Frame(self, bg=NAVBAR_BG, height=76)
        navbar.pack(side="bottom", fill="x")
        navbar.pack_propagate(False)
        self.next_btn = RoundedButton(
            navbar, text="Analizar  \u2192", command=go_dashboard(controller),
            bg=PURPLE, width=220, height=52, radius=26, parent_bg=NAVBAR_BG)
        self.next_btn.pack(side="right", padx=24, pady=12)

        text_frame = tk.Frame(self, bg=CARD_BG, padx=15, pady=15)
        text_frame.pack(expand=True, fill="both", padx=60, pady=(10, 20))

        self.text_view = tk.Text(text_frame, font=("Segoe UI", 12), wrap="word",
                                 bd=0, bg=CARD_BG, fg=DARK, cursor="arrow",
                                 spacing2=4)
        self.text_view.pack(expand=True, fill="both")
        self.text_view.insert("1.0", DEFAULT_TEXT)
        self.text_view.config(state="disabled")  # no se puede editar


# ----------------------------------------------------------------------
# PANTALLA 2: DASHBOARD
# ----------------------------------------------------------------------
class Dashboard(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG)
        self.controller = controller
        add_common_widgets(self, controller, show_back=True,
                           back_command=lambda: controller.show_frame("StartScreen"))

        tk.Label(self, text="Panel de Analisis", font=FONT_TITLE, bg=BG,
                 fg=DARK).pack(pady=(28, 4))
        resumen = " | ".join(f"{i['name']} ({i['value']})" for i in ITEMS)
        tk.Label(self, text=resumen, font=("Segoe UI", 10), bg=BG, fg=DARK,
                 wraplength=820, justify="center").pack(pady=(0, 6))

        center = tk.Frame(self, bg=BG)
        center.pack(expand=True)

        buttons = [
            ("\U0001F4CA  Analisis FODA", TURQUOISE, "FodaScreen"),
            ("\U0001F3A9  6 Sombreros para Pensar", CORAL, "HatsScreen"),
            ("\U0001F41F  Diagrama de Ishikawa", YELLOW, "FishboneScreen"),
            ("\U0001F4C8  Diagrama de Pareto", GREEN, "ParetoScreen"),
            ("\U0001F9ED  Analisis CATWOE", BLUE, "CatwoeScreen"),
        ]
        for label, color, target in buttons:
            fg = DARK if color == YELLOW else "white"
            RoundedButton(center, text=label,
                          command=lambda t=target: controller.show_frame(t),
                          bg=color, fg=fg, width=380, height=64, radius=28,
                          font=("Segoe UI", 13, "bold")).pack(pady=10)


# ----------------------------------------------------------------------
# FODA
# ----------------------------------------------------------------------
class FodaScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG)
        self.controller = controller
        add_common_widgets(self, controller, back_command=go_dashboard(controller))
        tk.Label(self, text="Analisis FODA", font=FONT_TITLE, bg=BG,
                 fg=DARK).pack(pady=(60, 8))
        grid = tk.Frame(self, bg=BG)
        grid.pack(expand=True)

        foda = compute_foda(ITEMS)
        specs = [("Fortalezas", GREEN, 0, 0), ("Debilidades", CORAL, 0, 1),
                 ("Oportunidades", TURQUOISE, 1, 0), ("Amenazas", YELLOW, 1, 1)]
        for title, color, r, c in specs:
            card, inner = make_card(grid, 430, 215, parent_bg=BG)
            card.grid(row=r, column=c, padx=14, pady=8)
            tk.Frame(inner, bg=color, height=6).pack(fill="x", pady=(0, 8))
            tk.Label(inner, text=title, font=FONT_CARD_TITLE, bg=CARD_BG,
                     fg=color).pack()
            for it in foda[title]:
                tk.Label(inner, text=f"\u2022 {it['name']} ({it['value']})",
                         font=FONT_CARD_TEXT, bg=CARD_BG, fg=DARK).pack(pady=1)
            tk.Label(inner, text=f"\U0001F4A1 {FODA_RECOS[title]}",
                     font=("Segoe UI", 9, "italic"), bg=CARD_BG, fg=PURPLE,
                     wraplength=380, justify="center").pack(pady=(8, 0))


# ----------------------------------------------------------------------
# SEIS SOMBREROS
# ----------------------------------------------------------------------
class HatsScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG)
        self.controller = controller
        add_common_widgets(self, controller, back_command=go_dashboard(controller))
        tk.Label(self, text="Seis Sombreros para Pensar", font=FONT_TITLE,
                 bg=BG, fg=DARK).pack(pady=(70, 6))
        scroll = ScrollableFrame(self, bg=BG)
        scroll.pack(fill="both", expand=True, padx=40, pady=(0, 30))

        colors = ["#DFE6E9", CORAL, DARK, YELLOW, GREEN, BLUE]
        for (title, text), color in zip(compute_hats(ITEMS).items(), colors):
            card, inner = make_card(scroll.scrollable_frame, 860, 130,
                                    parent_bg=BG)
            card.pack(pady=8)
            head = tk.Frame(inner, bg=CARD_BG)
            head.pack()
            dot = tk.Canvas(head, width=16, height=16, bg=CARD_BG,
                            highlightthickness=0)
            dot.pack(side="left", padx=(0, 10))
            dot.create_oval(1, 1, 15, 15, fill=color, outline=color)
            tk.Label(head, text=title, font=FONT_CARD_TITLE, bg=CARD_BG,
                     fg=DARK).pack(side="left")
            tk.Label(inner, text=text, font=FONT_CARD_TEXT, bg=CARD_BG,
                     fg=DARK, wraplength=800, justify="center").pack(pady=(6, 0))


# ----------------------------------------------------------------------
# ISHIKAWA
# ----------------------------------------------------------------------
class FishboneScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG)
        self.controller = controller
        add_common_widgets(self, controller, back_command=go_dashboard(controller))
        tk.Label(self, text="Diagrama de Ishikawa", font=FONT_TITLE, bg=BG,
                 fg=DARK).pack(pady=(60, 8))
        self.canvas = tk.Canvas(self, bg="white", highlightthickness=1,
                                highlightbackground=GREY)
        self.canvas.pack(fill="both", expand=True, padx=40, pady=(0, 24))
        self.canvas.bind("<Configure>", lambda e: self.draw())

    def on_show(self):
        self.draw()

    def draw(self):
        c = self.canvas
        c.delete("all")
        w, h = c.winfo_width() or 900, c.winfo_height() or 420
        cx1, cx2, cy = 60, w - 200, h / 2
        c.create_oval(w - 190, cy - 55, w - 40, cy + 55, fill=PURPLE, outline=PURPLE)
        c.create_text(w - 115, cy, text="INESTABILIDAD\nOPERATIVA", fill="white",
                      font=("Segoe UI", 10, "bold"), justify="center")
        c.create_line(cx1, cy, cx2, cy, width=4, fill=DARK)
        c.create_polygon(cx2, cy - 12, cx2, cy + 12, cx2 + 20, cy,
                         fill=DARK, outline=DARK)

        step = (cx2 - cx1 - 60) / max(1, (len(ITEMS) + 1) // 2)
        for idx, item in enumerate(ITEMS):
            up = idx % 2 == 0
            start = (cx1 + 60 + (idx // 2) * step, cy)
            end = (start[0] + 70, cy - 100 if up else cy + 100)
            color = COLORS[idx % len(COLORS)]
            c.create_line(*start, *end, width=3, fill=color)
            c.create_text(end[0], end[1] + (-16 if up else 16),
                          text=f"{item['m']}\n{item['name']} ({item['value']})",
                          fill=DARK, font=("Segoe UI", 9, "bold"), justify="center")

            # sub-escamas: cada sub-causa sale de la escama principal
            dx, dy = end[0] - start[0], end[1] - start[1]
            largo = max(1.0, (dx ** 2 + dy ** 2) ** 0.5)
            ux, uy = dx / largo, dy / largo
            px, py = -uy, ux
            n = len(item["subs"])
            for j, sub in enumerate(item["subs"]):
                t = (j + 1) / (n + 1)
                bx, by = start[0] + ux * largo * t, start[1] + uy * largo * t
                lado = 1 if j % 2 == 0 else -1
                c.create_line(bx, by, bx + px * 32 * lado, by + py * 32 * lado,
                              width=2, fill=_darken(color, 0.7))
                c.create_text(bx + px * 36 * lado, by + py * 36 * lado, text=sub,
                              fill=DARK, font=("Segoe UI", 7), justify="center",
                              width=95)


# ----------------------------------------------------------------------
# PARETO
# ----------------------------------------------------------------------
class ParetoScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG)
        self.controller = controller
        add_common_widgets(self, controller, back_command=go_dashboard(controller))
        tk.Label(self, text="Diagrama de Pareto", font=FONT_TITLE, bg=BG,
                 fg=DARK).pack(pady=(70, 4))
        self.canvas = tk.Canvas(self, bg="white", highlightthickness=1,
                                highlightbackground=GREY)
        self.canvas.pack(fill="both", expand=True, padx=40, pady=(0, 30))
        self.canvas.bind("<Configure>", lambda e: self.draw())

    def on_show(self):
        self.draw()

    def draw(self):
        c = self.canvas
        c.delete("all")
        w, h = c.winfo_width() or 900, c.winfo_height() or 420
        rows = compute_pareto(ITEMS)
        m_l, m_r, m_t, m_b = 70, 70, 30, 60
        plot_w, plot_h = w - m_l - m_r, h - m_t - m_b
        gap = plot_w / len(rows)
        bar_w = gap * 0.55
        max_val = max(r["value"] for r in rows) or 1

        c.create_line(m_l, m_t, m_l, h - m_b, w - m_r, h - m_b, width=2, fill=DARK)
        c.create_line(w - m_r, m_t, w - m_r, h - m_b, width=2, fill=DARK)

        points = []
        for idx, row in enumerate(rows):
            x0 = m_l + idx * gap + (gap - bar_w) / 2
            bar_h = (row["value"] / max_val) * (plot_h - 10)
            color = COLORS[idx % len(COLORS)]
            rounded_rect(c, x0, h - m_b - bar_h, x0 + bar_w, h - m_b, r=8,
                         fill=color, outline=color)
            c.create_text(x0 + bar_w / 2, h - m_b - bar_h - 12,
                          text=str(row["value"]), font=("Segoe UI", 9, "bold"))
            c.create_text(x0 + bar_w / 2, h - m_b + 22, text=row["name"],
                          font=("Segoe UI", 8), width=gap, justify="center")
            points.append((m_l + idx * gap + gap / 2,
                           m_t + (1 - row["cum"] / 100) * (plot_h - 10)))

        for i in range(len(points) - 1):
            c.create_line(*points[i], *points[i + 1], width=2, fill=DARK)
        for (px, py), row in zip(points, rows):
            c.create_oval(px - 4, py - 4, px + 4, py + 4, fill=DARK, outline=DARK)
            c.create_text(px, py - 14, text=f"{row['cum']:.0f}%",
                          font=("Segoe UI", 8, "bold"), fill=BLUE)
        y80 = m_t + (1 - 0.8) * (plot_h - 10)
        c.create_line(m_l, y80, w - m_r, y80, dash=(4, 3), fill=CORAL, width=1)
        c.create_text(w - m_r + 30, y80, text="80%", fill=CORAL,
                      font=("Segoe UI", 9, "bold"))


# ----------------------------------------------------------------------
# CATWOE
# ----------------------------------------------------------------------
class CatwoeScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG)
        self.controller = controller
        add_common_widgets(self, controller, back_command=go_dashboard(controller))
        tk.Label(self, text="Analisis CATWOE", font=FONT_TITLE, bg=BG,
                 fg=DARK).pack(pady=(60, 10))
        scroll = ScrollableFrame(self, bg=BG)
        scroll.pack(fill="both", expand=True, padx=40, pady=(0, 24))
        grid = tk.Frame(scroll.scrollable_frame, bg=BG)
        grid.pack(expand=True, anchor="center")

        pesos = {i["name"]: i["value"] for i in ITEMS}
        for idx, (letter, name, desc, factor, texto) in enumerate(CATWOE):
            color = COLORS[idx % len(COLORS)]
            fg = DARK if color == YELLOW else "white"
            card, inner = make_card(grid, 420, 200, parent_bg=BG)
            card.grid(row=idx // 2, column=idx % 2, padx=14, pady=10)
            top = tk.Frame(inner, bg=CARD_BG)
            top.pack()
            badge = tk.Canvas(top, width=34, height=34, bg=CARD_BG,
                              highlightthickness=0)
            badge.pack(side="left", padx=(0, 10))
            badge.create_oval(1, 1, 33, 33, fill=color, outline=color)
            badge.create_text(17, 17, text=letter, fill=fg,
                              font=("Segoe UI", 13, "bold"))
            tk.Label(top, text=name, font=FONT_CARD_TITLE, bg=CARD_BG,
                     fg=DARK).pack(side="left")
            tk.Label(inner, text=desc, font=("Segoe UI", 9, "italic"),
                     bg=CARD_BG, fg=GREY, wraplength=370).pack(pady=(4, 4))
            tk.Label(inner, text=f"\u2192 {factor} ({pesos[factor]} pts)",
                     font=FONT_CARD_TEXT, bg=CARD_BG, fg=color).pack()
            tk.Label(inner, text=f"\U0001F4A1 {texto}",
                     font=("Segoe UI", 9, "italic"), bg=CARD_BG, fg=PURPLE,
                     wraplength=370, justify="center").pack(pady=(8, 0))


# ----------------------------------------------------------------------
# ACERCA DEL CREADOR
# ----------------------------------------------------------------------
class AboutScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG)
        self.controller = controller
        add_logo(self)
        add_back_button(self, controller)
        tk.Label(self, text="Acerca del Creador", font=FONT_TITLE, bg=BG,
                 fg=DARK).pack(pady=(70, 20))
        card, inner = make_card(self, 560, 420, parent_bg=BG)
        card.pack(pady=10)
        photo = tk.Canvas(inner, width=210, height=140, bg=CARD_BG,
                          highlightthickness=0)
        photo.pack(pady=(15, 14))
        img = load_creator_image_3to2(CREATOR_PHOTO_PATH, 206, 136)
        if img:
            photo.image = img
            photo.create_image(105, 70, image=img)
        else:
            photo.create_rectangle((4, 4, 206, 136), outline=PURPLE, width=2,
                                   dash=(4, 2), fill="#EFEBFF")
            photo.create_text(105, 70, text="FOTO 3:2", fill=PURPLE,
                              font=("Segoe UI", 12, "bold"))
        tk.Label(inner, text="David Esau Lopez Ordoñez",
                 font=("Segoe UI", 16, "bold"), bg=CARD_BG, fg=DARK).pack()
        tk.Label(inner, text="desarrollador / Ingeniero de software",
                 font=("Segoe UI", 11), bg=CARD_BG, fg=PURPLE).pack(pady=(0, 12))
        tk.Label(inner, text="Esta aplicacion analiza un contexto empresarial "
                             "predeterminado y construye los diagramas de toma "
                             "de decisiones estrategicas: FODA, Seis Sombreros, "
                             "Ishikawa, Pareto y CATWOE.",
                 font=("Segoe UI", 10), bg=CARD_BG, fg=DARK, wraplength=480,
                 justify="center").pack(padx=10, pady=(0, 10))


# ----------------------------------------------------------------------
# CONTROLADOR PRINCIPAL
# ----------------------------------------------------------------------
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Analisis Estrategico 360")
        self.geometry(f"{WIN_W}x{WIN_H}")
        self.minsize(920, 640)
        self.configure(bg=BG)
        self.history = []
        self.current = None
        container = tk.Frame(self, bg=BG)
        container.pack(fill="both", expand=True)
        self.frames = {}
        for F in (StartScreen, Dashboard, FodaScreen, HatsScreen, FishboneScreen,
                  ParetoScreen, CatwoeScreen, AboutScreen):
            frame = F(container, self)
            self.frames[F.__name__] = frame
            frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.show_frame("StartScreen", push_history=False)

    def show_frame(self, name, push_history=True):
        if push_history and self.current is not None and self.current != name:
            self.history.append(self.current)
        frame = self.frames[name]
        frame.tkraise()
        if hasattr(frame, "on_show"):
            frame.on_show()
        self.current = name

    def go_back(self):
        prev = self.history.pop() if self.history else "StartScreen"
        frame = self.frames[prev]
        frame.tkraise()
        if hasattr(frame, "on_show"):
            frame.on_show()
        self.current = prev


if __name__ == "__main__":
    app = App()
    app.mainloop()
