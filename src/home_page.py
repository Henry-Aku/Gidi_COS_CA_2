import customtkinter as ctk

BG      = "#FAFAFA"
CARD    = "#F0F0F0"
WHITE   = "#FFFFFF"
ACCENT  = "#76EE52"
HOVER   = "#5ed43a"
TEXT    = "#111111"
SUBTEXT = "#666666"


class HomePage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=BG)
        self.controller = controller
        self._build_ui()

    def _build_ui(self):
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # --- Hero banner ---
        hero = ctk.CTkFrame(self, fg_color=WHITE, corner_radius=0)
        hero.grid(row=0, column=0, sticky="ew")
        hero.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            hero,
            text="🇳🇬  GIDI",
            font=ctk.CTkFont(family="Arial", size=48, weight="bold"),
            text_color=ACCENT,
        ).grid(row=0, column=0, pady=(28, 4))

        ctk.CTkLabel(
            hero,
            text="Your safe passage to Nigeria's culture & heritage",
            font=ctk.CTkFont(family="Arial", size=14),
            text_color=SUBTEXT,
        ).grid(row=1, column=0, pady=(0, 28))

        # --- Scrollable cards area ---
        scroll = ctk.CTkScrollableFrame(self, fg_color=BG)
        scroll.grid(row=1, column=0, sticky="nsew")
        scroll.grid_columnconfigure((0, 1), weight=1)

        nav_items = [
            ("🗺️", "Explore Nigeria",    "Discover states, sites & safe routes", "ExplorePage", 0, 0),
            ("📅", "Book an Experience", "Reserve a verified tour with a guide",  "BookPage",    0, 1),
            ("🧳", "My Trips",           "View your confirmed itineraries",        "MyTripPage",  1, 0),
            ("⭐", "Reviews",            "Read and share community experiences",  "ReviewsPage", 1, 1),
        ]

        for icon, label, desc, target, row, col in nav_items:
            self._make_nav_card(scroll, icon, label, desc, target, row, col)

        # --- Footer ---
        footer = ctk.CTkFrame(self, fg_color=CARD, corner_radius=0)
        footer.grid(row=2, column=0, sticky="ew")
        ctk.CTkLabel(
            footer,
            text="© 2026 Gidi Tourism — Proudly Nigerian",
            font=ctk.CTkFont(size=11),
            text_color=SUBTEXT,
        ).pack(pady=10)

    def _make_nav_card(self, parent, icon, label, desc, target, row, col):
        card = ctk.CTkFrame(parent, fg_color=WHITE, corner_radius=16)
        card.grid(row=row, column=col, padx=16, pady=16, sticky="nsew")
        card.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            card,
            text=icon,
            font=ctk.CTkFont(size=34),
        ).grid(row=0, column=0, pady=(22, 4))

        ctk.CTkLabel(
            card,
            text=label,
            font=ctk.CTkFont(family="Arial", size=16, weight="bold"),
            text_color=TEXT,
        ).grid(row=1, column=0, pady=(0, 4))

        ctk.CTkLabel(
            card,
            text=desc,
            font=ctk.CTkFont(size=12),
            text_color=SUBTEXT,
            wraplength=200,
        ).grid(row=2, column=0, pady=(0, 12))

        ctk.CTkButton(
            card,
            text=f"Open {label}",
            fg_color=ACCENT,
            hover_color=HOVER,
            text_color=TEXT,
            font=ctk.CTkFont(size=13, weight="bold"),
            corner_radius=10,
            command=lambda t=target: self.controller.show_page(t),
        ).grid(row=3, column=0, padx=20, pady=(0, 22), sticky="ew")
