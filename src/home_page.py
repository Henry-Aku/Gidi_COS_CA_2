import customtkinter as ctk

BG     = "#0f3460"
CARD   = "#16213e"
ACCENT = "#e94560"
TEXT   = "#eaeaea"
SUBTEXT = "#a8b2d8"


class HomePage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=BG)
        self.controller = controller
        self._build_ui()

    def _build_ui(self):
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # --- Hero banner ---
        hero = ctk.CTkFrame(self, fg_color=CARD, corner_radius=0)
        hero.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        hero.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            hero,
            text="🇳🇬  GIDI",
            font=ctk.CTkFont(family="Arial", size=52, weight="bold"),
            text_color=ACCENT,
        ).grid(row=0, column=0, pady=(40, 6))

        ctk.CTkLabel(
            hero,
            text="Your safe passage to Nigeria's culture & heritage",
            font=ctk.CTkFont(family="Arial", size=16),
            text_color=SUBTEXT,
        ).grid(row=1, column=0, pady=(0, 40))

        # --- Navigation cards grid ---
        cards_outer = ctk.CTkFrame(self, fg_color=BG)
        cards_outer.grid(row=1, column=0, sticky="nsew", padx=60, pady=40)
        cards_outer.grid_rowconfigure((0, 1), weight=1)
        cards_outer.grid_columnconfigure((0, 1), weight=1)

        nav_items = [
            ("🗺️", "Explore Nigeria",      "Discover states, sites & safe routes",  "ExplorePage",  0, 0),
            ("📅", "Book an Experience",   "Reserve a verified tour with a guide",   "BookPage",     0, 1),
            ("🧳", "My Trips",             "View your confirmed itineraries",         "MyTripPage",   1, 0),
            ("⭐", "Reviews",              "Read and share community experiences",   "ReviewsPage",  1, 1),
        ]

        for icon, label, desc, target, row, col in nav_items:
            self._make_nav_card(cards_outer, icon, label, desc, target, row, col)

        # --- Footer ---
        footer = ctk.CTkFrame(self, fg_color=CARD, corner_radius=0)
        footer.grid(row=2, column=0, sticky="ew")
        ctk.CTkLabel(
            footer,
            text="© 2025 Gidi Tourism — Proudly Nigerian",
            font=ctk.CTkFont(size=11),
            text_color=SUBTEXT,
        ).pack(pady=12)

    def _make_nav_card(self, parent, icon, label, desc, target, row, col):
        card = ctk.CTkFrame(parent, fg_color=CARD, corner_radius=16)
        card.grid(row=row, column=col, padx=16, pady=16, sticky="nsew")
        card.grid_rowconfigure(3, weight=1)
        card.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            card,
            text=icon,
            font=ctk.CTkFont(size=38),
        ).grid(row=0, column=0, pady=(28, 4))

        ctk.CTkLabel(
            card,
            text=label,
            font=ctk.CTkFont(family="Arial", size=17, weight="bold"),
            text_color=TEXT,
        ).grid(row=1, column=0, pady=(0, 4))

        ctk.CTkLabel(
            card,
            text=desc,
            font=ctk.CTkFont(size=12),
            text_color=SUBTEXT,
            wraplength=200,
        ).grid(row=2, column=0, pady=(0, 16))

        ctk.CTkButton(
            card,
            text=f"Open {label}",
            fg_color=ACCENT,
            hover_color="#c73652",
            text_color=TEXT,
            font=ctk.CTkFont(size=13, weight="bold"),
            corner_radius=10,
            command=lambda t=target: self.controller.show_page(t),
        ).grid(row=3, column=0, padx=24, pady=(0, 28), sticky="ew")
