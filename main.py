import customtkinter as ctk
from src.home_page import HomePage
from src.explore_page import ExplorePage
from src.book_page import BookPage
from src.my_trip_page import MyTripPage
from src.reviews_page import ReviewsPage

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class GidiApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Gidi — Nigeria Tourism App")
        self.geometry("900x700")
        self.minsize(800, 600)

        self.booked_trips = []

        container = ctk.CTkFrame(self, fg_color="#FAFAFA")
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.pages = {}
        for PageClass in (HomePage, ExplorePage, BookPage, MyTripPage, ReviewsPage):
            page = PageClass(container, self)
            self.pages[PageClass.__name__] = page
            page.grid(row=0, column=0, sticky="nsew")

        self.show_page("HomePage")

    def show_page(self, page_name: str):
        for frame in self.pages.values():
            frame.grid_remove()
        frame = self.pages[page_name]
        if hasattr(frame, "refresh"):
            frame.refresh()
        frame.grid(row=0, column=0, sticky="nsew")


if __name__ == "__main__":
    app = GidiApp()
    app.mainloop()
