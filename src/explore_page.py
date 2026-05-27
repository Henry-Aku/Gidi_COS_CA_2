import os
import customtkinter as ctk
from PIL import Image
from data import NIGERIA_DATA, CATEGORIES

ASSETS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "images")

BG      = "#FAFAFA"
CARD    = "#FFFFFF"
SIDEBAR = "#F0F0F0"
ACCENT  = "#76EE52"
HOVER   = "#5ed43a"
TEXT    = "#111111"
SUBTEXT = "#666666"
BORDER  = "#E0E0E0"
GREEN   = "#76EE52"


class ExplorePage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=BG)
        self.controller = controller
        self._current_places = []
        self._build_ui()

    def _build_ui(self):
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # --- Top bar ---
        topbar = ctk.CTkFrame(self, fg_color=CARD, corner_radius=0,
                              border_width=1, border_color=BORDER)
        topbar.grid(row=0, column=0, sticky="ew")
        topbar.grid_columnconfigure(1, weight=1)

        ctk.CTkButton(
            topbar, text="← Home", width=90, fg_color="transparent",
            text_color=SUBTEXT, hover_color=SIDEBAR,
            command=lambda: self.controller.show_page("HomePage"),
        ).grid(row=0, column=0, padx=10, pady=10)

        ctk.CTkLabel(
            topbar, text="🗺️  Explore Nigeria",
            font=ctk.CTkFont(size=20, weight="bold"), text_color=TEXT,
        ).grid(row=0, column=1, pady=14)

        # --- Body: two panels ---
        body = ctk.CTkFrame(self, fg_color=BG)
        body.grid(row=1, column=0, sticky="nsew")
        body.grid_rowconfigure(0, weight=1)
        body.grid_columnconfigure(0, weight=0)
        body.grid_columnconfigure(1, weight=1)

        self._build_left_panel(body)
        self._build_right_panel(body)

    def _build_left_panel(self, parent):
        left = ctk.CTkFrame(parent, fg_color=SIDEBAR, corner_radius=0, width=270,
                            border_width=1, border_color=BORDER)
        left.grid(row=0, column=0, sticky="nsew")
        left.grid_propagate(False)
        left.grid_rowconfigure(6, weight=1)
        left.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(left, text="Select a State", font=ctk.CTkFont(size=13, weight="bold"),
                     text_color=SUBTEXT).grid(row=0, column=0, sticky="w", padx=18, pady=(20, 2))

        states = sorted(NIGERIA_DATA.keys())
        self.state_var = ctk.StringVar(value=states[0])
        self.state_combo = ctk.CTkComboBox(
            left, values=states, variable=self.state_var, state="readonly",
            fg_color=CARD, button_color=ACCENT, border_color=BORDER,
            text_color=TEXT, dropdown_fg_color=CARD,
            command=self._on_state_change,
        )
        self.state_combo.grid(row=1, column=0, padx=18, pady=(0, 12), sticky="ew")

        ctk.CTkLabel(left, text="Filter by Category", font=ctk.CTkFont(size=13, weight="bold"),
                     text_color=SUBTEXT).grid(row=2, column=0, sticky="w", padx=18, pady=(0, 2))

        self.category_var = ctk.StringVar(value="All")
        self.category_combo = ctk.CTkComboBox(
            left, values=CATEGORIES, variable=self.category_var, state="readonly",
            fg_color=CARD, button_color=ACCENT, border_color=BORDER,
            text_color=TEXT, dropdown_fg_color=CARD,
            command=self._on_filter_change,
        )
        self.category_combo.grid(row=3, column=0, padx=18, pady=(0, 12), sticky="ew")

        self.search_var = ctk.StringVar()
        search_entry = ctk.CTkEntry(
            left, textvariable=self.search_var,
            placeholder_text="Search places...",
            fg_color=CARD, border_color=BORDER, text_color=TEXT,
        )
        search_entry.grid(row=4, column=0, padx=18, pady=(0, 12), sticky="ew")
        search_entry.bind("<KeyRelease>", self._on_filter_change)

        ctk.CTkLabel(left, text="Cultural Sites", font=ctk.CTkFont(size=13, weight="bold"),
                     text_color=SUBTEXT).grid(row=5, column=0, sticky="w", padx=18, pady=(0, 4))

        self.place_scroll = ctk.CTkScrollableFrame(left, fg_color=SIDEBAR, corner_radius=8)
        self.place_scroll.grid(row=6, column=0, padx=10, pady=(0, 14), sticky="nsew")

        self._populate_places()

    def _build_right_panel(self, parent):
        self.right = ctk.CTkScrollableFrame(parent, fg_color=BG)
        self.right.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)
        self.right.grid_columnconfigure(0, weight=1)
        self._show_prompt()

    def _show_prompt(self):
        self._clear_right()
        ctk.CTkLabel(
            self.right,
            text="← Select a state and site to explore",
            font=ctk.CTkFont(size=16), text_color=SUBTEXT,
            wraplength=420,
        ).grid(row=0, column=0, pady=80)

    def _clear_right(self):
        for w in self.right.winfo_children():
            w.destroy()

    def _get_filtered_places(self):
        state = self.state_var.get()
        if state not in NIGERIA_DATA:
            return []
        places = NIGERIA_DATA[state]["places"]
        category = self.category_var.get()
        query = self.search_var.get().lower().strip()
        if category != "All":
            places = [p for p in places if p["category"] == category]
        if query:
            places = [p for p in places
                      if query in p["name"].lower() or query in p["desc"].lower()]
        return places

    def _populate_places(self):
        for w in self.place_scroll.winfo_children():
            w.destroy()

        places = self._get_filtered_places()
        self._current_places = places

        if not places:
            ctk.CTkLabel(self.place_scroll, text="No sites match your filters.",
                         text_color=SUBTEXT, font=ctk.CTkFont(size=12)).pack(pady=20)
            return

        for place in places:
            btn = ctk.CTkButton(
                self.place_scroll,
                text=place["name"],
                anchor="w",
                fg_color=CARD,
                hover_color=SIDEBAR,
                text_color=TEXT,
                font=ctk.CTkFont(size=13),
                corner_radius=8,
                border_width=1,
                border_color=BORDER,
                command=lambda p=place: self._show_place_detail(p),
            )
            btn.pack(fill="x", padx=4, pady=4)

    def _on_state_change(self, _=None):
        self.category_var.set("All")
        self.search_var.set("")
        self._populate_places()
        self._show_prompt()

    def _on_filter_change(self, _=None):
        self._populate_places()

    def _load_image(self, image_placeholder):
        for ext in ("jpg", "jpeg", "png", "webp"):
            path = os.path.join(ASSETS_DIR, f"{image_placeholder}.{ext}")
            if os.path.exists(path):
                try:
                    return ctk.CTkImage(
                        light_image=Image.open(path),
                        dark_image=Image.open(path),
                        size=(500, 240),
                    )
                except Exception:
                    pass
        return None

    def _show_place_detail(self, place):
        self._clear_right()

        r = self.right
        r.grid_columnconfigure(0, weight=1)

        img = self._load_image(place.get("image_placeholder", ""))
        if img:
            ctk.CTkLabel(r, image=img, text="", corner_radius=12).grid(
                row=0, column=0, sticky="ew", padx=30, pady=(24, 0)
            )
        else:
            placeholder = ctk.CTkFrame(r, fg_color=SIDEBAR, corner_radius=12, height=140,
                                       border_width=1, border_color=BORDER)
            placeholder.grid(row=0, column=0, sticky="ew", padx=30, pady=(24, 0))
            placeholder.grid_propagate(False)
            placeholder.grid_columnconfigure(0, weight=1)
            placeholder.grid_rowconfigure(0, weight=1)
            ctk.CTkLabel(
                placeholder, text="📷  Image coming soon",
                font=ctk.CTkFont(size=13), text_color=SUBTEXT,
            ).grid(row=0, column=0)

        ctk.CTkLabel(r, text=place["name"],
                     font=ctk.CTkFont(size=24, weight="bold"),
                     text_color=TEXT, wraplength=480,
                     justify="left").grid(row=1, column=0, sticky="w", padx=30, pady=(20, 4))

        ctk.CTkLabel(r, text=f"  {place['category']}  ",
                     font=ctk.CTkFont(size=12), text_color="#1a6e00",
                     fg_color=ACCENT, corner_radius=8).grid(row=2, column=0, sticky="w", padx=30, pady=(0, 12))

        divider = ctk.CTkFrame(r, height=1, fg_color=BORDER)
        divider.grid(row=3, column=0, sticky="ew", padx=30, pady=(0, 16))

        ctk.CTkLabel(r, text="About this place",
                     font=ctk.CTkFont(size=14, weight="bold"),
                     text_color=SUBTEXT).grid(row=4, column=0, sticky="w", padx=30, pady=(0, 6))

        ctk.CTkLabel(r, text=place["desc"],
                     font=ctk.CTkFont(size=13), text_color=TEXT,
                     wraplength=480, justify="left").grid(row=5, column=0, sticky="w", padx=30, pady=(0, 20))

        route_card = ctk.CTkFrame(r, fg_color="#f0faf0", corner_radius=12,
                                   border_width=1, border_color="#c8e6c9")
        route_card.grid(row=6, column=0, sticky="ew", padx=30, pady=(0, 20))
        route_card.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(route_card, text="✅  Verified Safe Route",
                     font=ctk.CTkFont(size=13, weight="bold"),
                     text_color="#2e7d32").grid(row=0, column=0, sticky="w", padx=16, pady=(14, 4))

        ctk.CTkLabel(route_card, text=place["route"],
                     font=ctk.CTkFont(size=12), text_color=TEXT,
                     wraplength=460, justify="left").grid(row=1, column=0, sticky="w", padx=16, pady=(0, 14))

        ctk.CTkButton(
            r, text="📅  Book This Experience",
            fg_color=ACCENT, hover_color=HOVER,
            text_color=TEXT, font=ctk.CTkFont(size=14, weight="bold"),
            height=44, corner_radius=10,
            command=lambda: self._book_place(place["name"]),
        ).grid(row=7, column=0, padx=30, pady=(0, 30), sticky="ew")

    def _book_place(self, name):
        book_page = self.controller.pages["BookPage"]
        book_page.set_destination(name)
        self.controller.show_page("BookPage")

    def refresh(self):
        self.state_var.set(sorted(NIGERIA_DATA.keys())[0])
        self.category_var.set("All")
        self.search_var.set("")
        self._populate_places()
        self._show_prompt()
