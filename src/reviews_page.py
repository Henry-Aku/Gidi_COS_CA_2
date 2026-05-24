import customtkinter as ctk
from data import SEED_REVIEWS

BG      = "#0f3460"
CARD    = "#16213e"
ACCENT  = "#e94560"
TEXT    = "#eaeaea"
SUBTEXT = "#a8b2d8"
GOLD    = "#ffd700"


class ReviewsPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=BG)
        self.controller = controller
        self._reviews = list(SEED_REVIEWS)
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
            topbar, text="⭐  Community Reviews",
            font=ctk.CTkFont(size=20, weight="bold"), text_color=TEXT,
        ).grid(row=0, column=1, pady=14)

        # --- Main layout: left (reviews list) + right (submission form) ---
        body = ctk.CTkFrame(self, fg_color=BG)
        body.grid(row=1, column=0, sticky="nsew")
        body.grid_rowconfigure(0, weight=1)
        body.grid_columnconfigure(0, weight=1)
        body.grid_columnconfigure(1, weight=0)

        self._build_reviews_panel(body)
        self._build_submission_panel(body)

    # ------------------------------------------------------------------ #
    #  Left — Reviews list                                                 #
    # ------------------------------------------------------------------ #
    def _build_reviews_panel(self, parent):
        left = ctk.CTkFrame(parent, fg_color=BG)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 0))
        left.grid_rowconfigure(1, weight=1)
        left.grid_columnconfigure(0, weight=1)

        # Filters row
        filters = ctk.CTkFrame(left, fg_color=CARD, corner_radius=10)
        filters.grid(row=0, column=0, sticky="ew", padx=20, pady=(16, 8))
        filters.grid_columnconfigure(0, weight=1)

        self.search_var = ctk.StringVar()
        search_entry = ctk.CTkEntry(
            filters, textvariable=self.search_var,
            placeholder_text="Search reviews...",
            fg_color=BG, border_color=ACCENT, text_color=TEXT, height=36,
        )
        search_entry.grid(row=0, column=0, padx=12, pady=10, sticky="ew")
        search_entry.bind("<KeyRelease>", lambda _: self._render_reviews())

        rating_options = ["All Ratings", "5 Stars", "4 Stars", "3 Stars", "2 Stars", "1 Star"]
        self.rating_filter_var = ctk.StringVar(value="All Ratings")
        ctk.CTkComboBox(
            filters, values=rating_options,
            variable=self.rating_filter_var, state="readonly",
            fg_color=BG, button_color=ACCENT, border_color=ACCENT,
            text_color=TEXT, dropdown_fg_color=CARD,
            command=lambda _: self._render_reviews(),
            width=160,
        ).grid(row=0, column=1, padx=(0, 12), pady=10)

        # Scrollable review cards
        self.reviews_scroll = ctk.CTkScrollableFrame(left, fg_color=BG)
        self.reviews_scroll.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 16))
        self.reviews_scroll.grid_columnconfigure(0, weight=1)

        self._render_reviews()

    def _get_filtered_reviews(self):
        query = self.search_var.get().lower().strip()
        rating_str = self.rating_filter_var.get()
        target_rating = None if rating_str == "All Ratings" else int(rating_str[0])

        results = self._reviews
        if target_rating is not None:
            results = [r for r in results if r["rating"] == target_rating]
        if query:
            results = [r for r in results
                       if query in r["text"].lower() or query in r["author"].lower()]
        return results

    def _render_reviews(self):
        for w in self.reviews_scroll.winfo_children():
            w.destroy()

        filtered = self._get_filtered_reviews()

        if not filtered:
            ctk.CTkLabel(self.reviews_scroll, text="No reviews match your search.",
                         text_color=SUBTEXT, font=ctk.CTkFont(size=13)).pack(pady=30)
            return

        for review in filtered:
            self._make_review_card(self.reviews_scroll, review)

    def _make_review_card(self, parent, review):
        card = ctk.CTkFrame(parent, fg_color=CARD, corner_radius=12)
        card.pack(fill="x", pady=6)
        card.grid_columnconfigure(0, weight=1)

        stars = "★" * review["rating"] + "☆" * (5 - review["rating"])
        ctk.CTkLabel(card, text=stars, font=ctk.CTkFont(size=16),
                     text_color=GOLD).grid(row=0, column=0, sticky="w", padx=16, pady=(12, 2))

        ctk.CTkLabel(card, text=f"📍 {review['location']}",
                     font=ctk.CTkFont(size=12), text_color=SUBTEXT,
                     ).grid(row=1, column=0, sticky="w", padx=16, pady=(0, 4))

        ctk.CTkLabel(card, text=f'"{review["text"]}"',
                     font=ctk.CTkFont(size=13, slant="italic"),
                     text_color=TEXT, wraplength=380, justify="left",
                     ).grid(row=2, column=0, sticky="w", padx=16, pady=(0, 4))

        ctk.CTkLabel(card, text=f"— {review['author']}",
                     font=ctk.CTkFont(size=12, weight="bold"), text_color=SUBTEXT,
                     ).grid(row=3, column=0, sticky="w", padx=16, pady=(0, 12))

    # ------------------------------------------------------------------ #
    #  Right — Submission form                                             #
    # ------------------------------------------------------------------ #
    def _build_submission_panel(self, parent):
        right = ctk.CTkFrame(parent, fg_color=CARD, corner_radius=0, width=320)
        right.grid(row=0, column=1, sticky="nsew")
        right.grid_propagate(False)
        right.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(right, text="Share Your Experience",
                     font=ctk.CTkFont(size=16, weight="bold"), text_color=ACCENT,
                     ).grid(row=0, column=0, sticky="w", padx=20, pady=(24, 2))

        divider = ctk.CTkFrame(right, height=2, fg_color=ACCENT)
        divider.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 16))

        ctk.CTkLabel(right, text="Your name", text_color=SUBTEXT,
                     font=ctk.CTkFont(size=13)).grid(row=2, column=0, sticky="w", padx=20, pady=(0, 2))

        self.name_var = ctk.StringVar()
        ctk.CTkEntry(right, textvariable=self.name_var,
                     placeholder_text="Your name",
                     fg_color=BG, border_color=ACCENT, text_color=TEXT, height=36,
                     ).grid(row=3, column=0, sticky="ew", padx=20, pady=(0, 10))

        ctk.CTkLabel(right, text="Location visited", text_color=SUBTEXT,
                     font=ctk.CTkFont(size=13)).grid(row=4, column=0, sticky="w", padx=20, pady=(0, 2))

        self.location_var = ctk.StringVar()
        ctk.CTkEntry(right, textvariable=self.location_var,
                     placeholder_text="e.g. Osun Sacred Grove",
                     fg_color=BG, border_color=ACCENT, text_color=TEXT, height=36,
                     ).grid(row=5, column=0, sticky="ew", padx=20, pady=(0, 10))

        ctk.CTkLabel(right, text="Your review", text_color=SUBTEXT,
                     font=ctk.CTkFont(size=13)).grid(row=6, column=0, sticky="w", padx=20, pady=(0, 2))

        self.review_text_box = ctk.CTkTextbox(
            right, height=80, fg_color=BG, border_color=ACCENT,
            border_width=2, text_color=TEXT, font=ctk.CTkFont(size=13),
        )
        self.review_text_box.grid(row=7, column=0, sticky="ew", padx=20, pady=(0, 10))

        ctk.CTkLabel(right, text="Rating", text_color=SUBTEXT,
                     font=ctk.CTkFont(size=13)).grid(row=8, column=0, sticky="w", padx=20, pady=(0, 4))

        self._new_rating_var = ctk.IntVar(value=5)
        stars_row = ctk.CTkFrame(right, fg_color="transparent")
        stars_row.grid(row=9, column=0, sticky="w", padx=20, pady=(0, 14))
        for val in range(1, 6):
            ctk.CTkRadioButton(
                stars_row, text=str(val),
                variable=self._new_rating_var, value=val,
                fg_color=GOLD, hover_color="#e6c200", text_color=TEXT,
                font=ctk.CTkFont(size=13),
            ).pack(side="left", padx=4)

        self.submit_error_label = ctk.CTkLabel(right, text="", text_color="#ff6b6b",
                                               font=ctk.CTkFont(size=12))
        self.submit_error_label.grid(row=10, column=0, sticky="w", padx=20)

        ctk.CTkButton(
            right, text="Submit Review",
            fg_color=ACCENT, hover_color="#c73652",
            text_color=TEXT, font=ctk.CTkFont(size=14, weight="bold"),
            height=42, corner_radius=10,
            command=self._submit_review,
        ).grid(row=11, column=0, padx=20, pady=(4, 24), sticky="ew")

    def _submit_review(self):
        name = self.name_var.get().strip()
        location = self.location_var.get().strip()
        text = self.review_text_box.get("1.0", "end").strip()

        if not name:
            self.submit_error_label.configure(text="⚠  Please enter your name.")
            return
        if not location:
            self.submit_error_label.configure(text="⚠  Please enter a location.")
            return
        if not text:
            self.submit_error_label.configure(text="⚠  Please write a review.")
            return

        self.submit_error_label.configure(text="")

        self._reviews.append({
            "author": name,
            "location": location,
            "text": text,
            "rating": self._new_rating_var.get(),
        })

        self.name_var.set("")
        self.location_var.set("")
        self.review_text_box.delete("1.0", "end")
        self._new_rating_var.set(5)

        self._render_reviews()

    # ------------------------------------------------------------------ #
    #  refresh — called by controller on navigation                        #
    # ------------------------------------------------------------------ #
    def refresh(self):
        self._render_reviews()