import customtkinter as ctk
from data import NIGERIA_DATA, TOUR_GUIDES

BG      = "#0f3460"
CARD    = "#16213e"
ACCENT  = "#e94560"
TEXT    = "#eaeaea"
SUBTEXT = "#a8b2d8"
GREEN   = "#4caf50"


class BookPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=BG)
        self.controller = controller
        self._selected_guide_index = ctk.IntVar(value=-1)
        self._guide_state_var = ctk.StringVar(value="All States")
        self._travellers_var = ctk.IntVar(value=1)
        self._build_ui()

    def _build_ui(self):
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # --- Top bar ---
        topbar = ctk.CTkFrame(self, fg_color=CARD, corner_radius=0)
        topbar.grid(row=0, column=0, sticky="ew")
        topbar.grid_columnconfigure(1, weight=1)

        ctk.CTkButton(
            topbar, text="← Home", width=90, fg_color="transparent",
            text_color=SUBTEXT, hover_color=BG,
            command=lambda: self.controller.show_page("HomePage"),
        ).grid(row=0, column=0, padx=10, pady=10)

        ctk.CTkLabel(
            topbar, text="📅  Book an Experience",
            font=ctk.CTkFont(size=20, weight="bold"), text_color=TEXT,
        ).grid(row=0, column=1, pady=14)

        # --- Scrollable body ---
        self.body = ctk.CTkScrollableFrame(self, fg_color=BG)
        self.body.grid(row=1, column=0, sticky="nsew")
        self.body.grid_columnconfigure(0, weight=1)

        self._build_trip_details()
        self._build_guide_section()
        self._build_confirm_section()

    # ------------------------------------------------------------------ #
    #  Section 1 — Trip Details                                            #
    # ------------------------------------------------------------------ #
    def _build_trip_details(self):
        section = self._make_section(self.body, "1.  Trip Details", 0)

        ctk.CTkLabel(section, text="Destination", text_color=SUBTEXT,
                     font=ctk.CTkFont(size=13)).grid(row=0, column=0, sticky="w", padx=20, pady=(16, 2))

        self.dest_var = ctk.StringVar()
        self.dest_entry = ctk.CTkEntry(
            section, textvariable=self.dest_var,
            placeholder_text="e.g. Nike Art Gallery",
            fg_color=BG, border_color=ACCENT, text_color=TEXT, height=38,
        )
        self.dest_entry.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 12))
        self.dest_var.trace_add("write", self._update_summary)

        ctk.CTkLabel(section, text="Travel Date (DD/MM/YYYY)", text_color=SUBTEXT,
                     font=ctk.CTkFont(size=13)).grid(row=2, column=0, sticky="w", padx=20, pady=(0, 2))

        self.date_var = ctk.StringVar()
        ctk.CTkEntry(
            section, textvariable=self.date_var,
            placeholder_text="DD/MM/YYYY",
            fg_color=BG, border_color=ACCENT, text_color=TEXT, height=38,
        ).grid(row=3, column=0, sticky="ew", padx=20, pady=(0, 12))
        self.date_var.trace_add("write", self._update_summary)

        ctk.CTkLabel(section, text="Number of Travellers", text_color=SUBTEXT,
                     font=ctk.CTkFont(size=13)).grid(row=4, column=0, sticky="w", padx=20, pady=(0, 2))

        traveller_row = ctk.CTkFrame(section, fg_color="transparent")
        traveller_row.grid(row=5, column=0, sticky="ew", padx=20, pady=(0, 20))
        traveller_row.grid_columnconfigure(0, weight=1)

        self.travellers_label = ctk.CTkLabel(traveller_row, text="1",
                                             font=ctk.CTkFont(size=16, weight="bold"),
                                             text_color=ACCENT, width=30)
        self.travellers_label.grid(row=0, column=1, padx=(12, 0))

        ctk.CTkSlider(
            traveller_row, from_=1, to=20, number_of_steps=19,
            variable=self._travellers_var,
            button_color=ACCENT, button_hover_color="#c73652",
            progress_color=ACCENT, fg_color=CARD,
            command=self._on_travellers_change,
        ).grid(row=0, column=0, sticky="ew")

    def _on_travellers_change(self, value):
        n = int(value)
        self._travellers_var.set(n)
        self.travellers_label.configure(text=str(n))
        self._update_summary()

    # ------------------------------------------------------------------ #
    #  Section 2 — Tour Guides                                            #
    # ------------------------------------------------------------------ #
    def _build_guide_section(self):
        section = self._make_section(self.body, "2.  Choose a Tour Guide", 1)

        filter_row = ctk.CTkFrame(section, fg_color="transparent")
        filter_row.grid(row=0, column=0, sticky="ew", padx=20, pady=(16, 12))
        filter_row.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(filter_row, text="Filter by state:", text_color=SUBTEXT,
                     font=ctk.CTkFont(size=13)).grid(row=0, column=0, padx=(0, 10))

        state_options = ["All States"] + sorted(NIGERIA_DATA.keys())
        ctk.CTkComboBox(
            filter_row, values=state_options,
            variable=self._guide_state_var, state="readonly",
            fg_color=BG, button_color=ACCENT, border_color=ACCENT,
            text_color=TEXT, dropdown_fg_color=CARD,
            command=self._refresh_guides,
        ).grid(row=0, column=1, sticky="ew")

        self.guides_container = ctk.CTkFrame(section, fg_color="transparent")
        self.guides_container.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 16))
        self.guides_container.grid_columnconfigure(0, weight=1)

        self._refresh_guides()

    def _refresh_guides(self, _=None):
        for w in self.guides_container.winfo_children():
            w.destroy()

        selected_state = self._guide_state_var.get()
        guides = TOUR_GUIDES if selected_state == "All States" else [
            g for g in TOUR_GUIDES if g["state"] == selected_state
        ]

        if not guides:
            ctk.CTkLabel(self.guides_container, text="No guides found for this state.",
                         text_color=SUBTEXT).pack(pady=10)
            return

        for i, guide in enumerate(guides):
            self._make_guide_card(self.guides_container, guide, i)

    def _make_guide_card(self, parent, guide, index):
        card = ctk.CTkFrame(parent, fg_color=CARD, corner_radius=12)
        card.pack(fill="x", pady=6)
        card.grid_columnconfigure(0, weight=1)

        top = ctk.CTkFrame(card, fg_color="transparent")
        top.grid(row=0, column=0, sticky="ew", padx=16, pady=(14, 0))
        top.grid_columnconfigure(0, weight=1)

        stars = "★" * guide["rating"] + "☆" * (5 - guide["rating"])
        ctk.CTkLabel(top, text=f"{guide['name']}  {stars}",
                     font=ctk.CTkFont(size=15, weight="bold"),
                     text_color=TEXT).grid(row=0, column=0, sticky="w")

        ctk.CTkLabel(top, text=guide["fee"],
                     font=ctk.CTkFont(size=13, weight="bold"),
                     text_color=ACCENT).grid(row=0, column=1, sticky="e")

        ctk.CTkLabel(card, text=guide["specialty"],
                     font=ctk.CTkFont(size=12), text_color=SUBTEXT
                     ).grid(row=1, column=0, sticky="w", padx=16, pady=(2, 0))

        ctk.CTkLabel(card, text=guide["bio"],
                     font=ctk.CTkFont(size=12), text_color=TEXT,
                     wraplength=500, justify="left",
                     ).grid(row=2, column=0, sticky="w", padx=16, pady=(4, 0))

        langs = "🗣  " + ", ".join(guide["languages"])
        ctk.CTkLabel(card, text=langs,
                     font=ctk.CTkFont(size=12), text_color=SUBTEXT,
                     ).grid(row=3, column=0, sticky="w", padx=16, pady=(4, 0))

        ctk.CTkRadioButton(
            card, text=f"Select {guide['name']}",
            variable=self._selected_guide_index, value=index,
            fg_color=ACCENT, hover_color="#c73652", text_color=TEXT,
            font=ctk.CTkFont(size=13),
            command=self._update_summary,
        ).grid(row=4, column=0, sticky="w", padx=16, pady=(8, 14))

    # ------------------------------------------------------------------ #
    #  Section 3 — Confirm                                                 #
    # ------------------------------------------------------------------ #
    def _build_confirm_section(self):
        section = self._make_section(self.body, "3.  Confirm Booking", 2)

        self.summary_label = ctk.CTkLabel(
            section,
            text="Fill in the details above to see your booking summary.",
            font=ctk.CTkFont(size=13, slant="italic"),
            text_color=SUBTEXT, wraplength=540, justify="left",
        )
        self.summary_label.grid(row=0, column=0, sticky="w", padx=20, pady=(16, 8))

        self.error_label = ctk.CTkLabel(section, text="", text_color="#ff6b6b",
                                        font=ctk.CTkFont(size=12))
        self.error_label.grid(row=1, column=0, sticky="w", padx=20)

        ctk.CTkButton(
            section,
            text="✅  Confirm Booking",
            fg_color=GREEN, hover_color="#388e3c",
            text_color=TEXT, font=ctk.CTkFont(size=15, weight="bold"),
            height=46, corner_radius=10,
            command=self._confirm_booking,
        ).grid(row=2, column=0, padx=20, pady=(8, 28), sticky="ew")

    # ------------------------------------------------------------------ #
    #  Logic helpers                                                       #
    # ------------------------------------------------------------------ #
    def _get_selected_guide(self):
        idx = self._selected_guide_index.get()
        state = self._guide_state_var.get()
        guides = TOUR_GUIDES if state == "All States" else [
            g for g in TOUR_GUIDES if g["state"] == state
        ]
        if 0 <= idx < len(guides):
            return guides[idx]
        return None

    def _update_summary(self, *_):
        dest = self.dest_var.get().strip()
        date = self.date_var.get().strip()
        guide = self._get_selected_guide()
        guide_name = guide["name"] if guide else "—"
        dest_str = dest if dest else "—"
        date_str = date if date else "—"
        n = self._travellers_var.get()
        self.summary_label.configure(
            text=f"Booking: {dest_str}  |  Date: {date_str}  |  "
                 f"Travellers: {n}  |  Guide: {guide_name}"
        )

    def _confirm_booking(self):
        dest = self.dest_var.get().strip()
        date = self.date_var.get().strip()
        guide = self._get_selected_guide()

        if not dest:
            self.error_label.configure(text="⚠  Please enter a destination.")
            return
        if not date:
            self.error_label.configure(text="⚠  Please enter a travel date.")
            return
        if guide is None:
            self.error_label.configure(text="⚠  Please select a tour guide.")
            return

        self.error_label.configure(text="")

        trip = {
            "destination": dest,
            "date": date,
            "travellers": self._travellers_var.get(),
            "guide": guide,
        }
        self.controller.booked_trips.append(trip)

        self._reset_form()
        self.controller.show_page("MyTripPage")

    def _reset_form(self):
        self.dest_var.set("")
        self.date_var.set("")
        self._travellers_var.set(1)
        self.travellers_label.configure(text="1")
        self._selected_guide_index.set(-1)
        self._guide_state_var.set("All States")
        self._refresh_guides()
        self._update_summary()

    # ------------------------------------------------------------------ #
    #  Public API                                                          #
    # ------------------------------------------------------------------ #
    def set_destination(self, name: str):
        self.dest_var.set(name)

    # ------------------------------------------------------------------ #
    #  Shared section builder                                              #
    # ------------------------------------------------------------------ #
    def _make_section(self, parent, title, section_row):
        outer = ctk.CTkFrame(parent, fg_color=CARD, corner_radius=14)
        outer.grid(row=section_row, column=0, sticky="ew", padx=30, pady=12)
        outer.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(outer, text=title,
                     font=ctk.CTkFont(size=16, weight="bold"), text_color=ACCENT
                     ).grid(row=0, column=0, sticky="w", padx=20, pady=(16, 0))

        divider = ctk.CTkFrame(outer, height=2, fg_color=ACCENT)
        divider.grid(row=1, column=0, sticky="ew", padx=20, pady=(6, 0))

        return outer
