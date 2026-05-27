import customtkinter as ctk

BG      = "#FAFAFA"
CARD    = "#FFFFFF"
SIDEBAR = "#F0F0F0"
ACCENT  = "#76EE52"
HOVER   = "#5ed43a"
TEXT    = "#111111"
SUBTEXT = "#666666"
BORDER  = "#E0E0E0"


class MyTripPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=BG)
        self.controller = controller
        self._build_ui()

    def _build_ui(self):
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

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
            topbar, text="🧳  My Trips",
            font=ctk.CTkFont(size=20, weight="bold"), text_color=TEXT,
        ).grid(row=0, column=1, pady=14)

        self.content_frame = ctk.CTkScrollableFrame(self, fg_color=BG)
        self.content_frame.grid(row=1, column=0, sticky="nsew")
        self.content_frame.grid_columnconfigure(0, weight=1)

    def refresh(self):
        for w in self.content_frame.winfo_children():
            w.destroy()

        trips = self.controller.booked_trips

        if not trips:
            ctk.CTkLabel(
                self.content_frame,
                text="No trips yet. Start exploring!",
                font=ctk.CTkFont(size=18), text_color=SUBTEXT,
            ).grid(row=0, column=0, pady=(80, 16))

            ctk.CTkButton(
                self.content_frame,
                text="🗺️  Explore Nigeria",
                fg_color=ACCENT, hover_color=HOVER,
                text_color=TEXT, font=ctk.CTkFont(size=14, weight="bold"),
                height=42, corner_radius=10,
                command=lambda: self.controller.show_page("ExplorePage"),
            ).grid(row=1, column=0, padx=120, pady=4, sticky="ew")
            return

        for i, trip in enumerate(trips):
            self._make_trip_card(self.content_frame, trip, i)

        ctk.CTkButton(
            self.content_frame,
            text="📅  Book Another Trip",
            fg_color=ACCENT, hover_color=HOVER,
            text_color=TEXT, font=ctk.CTkFont(size=14, weight="bold"),
            height=42, corner_radius=10,
            command=lambda: self.controller.show_page("BookPage"),
        ).grid(row=len(trips), column=0, padx=30, pady=(12, 28), sticky="ew")

    def _make_trip_card(self, parent, trip, index):
        card = ctk.CTkFrame(parent, fg_color=CARD, corner_radius=14,
                             border_width=1, border_color=BORDER)
        card.grid(row=index, column=0, sticky="ew", padx=30, pady=10)
        card.grid_columnconfigure(0, weight=1)

        header = ctk.CTkFrame(card, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=20, pady=(16, 0))
        header.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            header, text=trip["destination"],
            font=ctk.CTkFont(size=20, weight="bold"), text_color=TEXT,
        ).grid(row=0, column=0, sticky="w")

        ctk.CTkLabel(
            header, text="Confirmed ✓",
            font=ctk.CTkFont(size=12, weight="bold"), text_color="#1a6e00",
            fg_color=ACCENT, corner_radius=8,
        ).grid(row=0, column=1, sticky="e")

        guide = trip["guide"]
        details = (
            f"📅  Date: {trip['date']}     "
            f"👥  Travellers: {trip['travellers']}"
        )
        ctk.CTkLabel(card, text=details,
                     font=ctk.CTkFont(size=13), text_color=SUBTEXT,
                     ).grid(row=1, column=0, sticky="w", padx=20, pady=(8, 0))

        guide_info = (
            f"🧑‍🦯  Guide: {guide['name']}  —  {guide['specialty']}  |  {guide['fee']}"
        )
        ctk.CTkLabel(card, text=guide_info,
                     font=ctk.CTkFont(size=13), text_color=TEXT,
                     ).grid(row=2, column=0, sticky="w", padx=20, pady=(4, 16))
