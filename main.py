import tkinter as tk
from tkinter import ttk, messagebox
from google_play_scraper import app, reviews, search
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from wordcloud import WordCloud
import pandas as pd
from ttkthemes import ThemedTk  # Menggunakan ThemedTk untuk tema modern
import webbrowser  # Untuk membuka link di browser


class PlayStoreScraperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Play Store Scraper")
        self.root.geometry("1000x950")
        self.root.set_theme("arc")  # Menggunakan tema "arc" dari ttkthemes
        self.current_frame = None
        self.chart_frame = None  # Frame untuk menampilkan grafik
        self.create_widgets()

    def create_widgets(self):
        """Inisialisasi dan tampilkan halaman utama."""
        self.show_main_page()

    # ==================== HALAMAN UTAMA ====================
    def show_main_page(self):
        """Menampilkan halaman utama."""
        self._clear_current_frame()

        self.current_frame = ttk.Frame(self.root, padding="20")
        self.current_frame.pack(fill=tk.BOTH, expand=True)

        content_frame = ttk.Frame(self.current_frame)
        content_frame.pack(expand=True)

        # Label dan Radio Button untuk memilih mode
        ttk.Label(content_frame, text="Pilih Mode:", font=("Helvetica", 14)).grid(
            row=0, column=0, columnspan=3, padx=10, pady=10
        )
        self.mode_var = tk.StringVar(value="search")
        ttk.Radiobutton(
            content_frame, text="Search by Title", variable=self.mode_var, value="search", style="Toolbutton"
        ).grid(row=1, column=0, padx=10, pady=10)
        ttk.Radiobutton(
            content_frame, text="Input ID", variable=self.mode_var, value="id", style="Toolbutton"
        ).grid(row=1, column=1, padx=10, pady=10)

        # Tombol Next
        ttk.Button(
            content_frame, text="Next", command=self.next_page, style="Accent.TButton"
        ).grid(row=2, column=0, columnspan=3, pady=20)

    def next_page(self):
        """Navigasi ke halaman berikutnya berdasarkan mode yang dipilih."""
        mode = self.mode_var.get()
        if mode == "search":
            self.show_search_page()
        else:
            self.show_id_page()

    # ==================== HALAMAN SEARCH ====================
    def show_search_page(self):
        """Menampilkan halaman pencarian aplikasi berdasarkan judul."""
        self._clear_current_frame()

        self.current_frame = ttk.Frame(self.root, padding="20")
        self.current_frame.pack(fill=tk.BOTH, expand=True)

        content_frame = ttk.Frame(self.current_frame)
        content_frame.pack(expand=True)

        # Input judul aplikasi
        ttk.Label(content_frame, text="Masukkan Judul Aplikasi:", font=("Helvetica", 14)).grid(
            row=0, column=0, columnspan=2, padx=10, pady=10
        )
        self.search_entry = ttk.Entry(content_frame, width=40, font=("Helvetica", 12))
        self.search_entry.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        # Tombol Search dan Back
        ttk.Button(
            content_frame, text="Search", command=self.search_apps, style="Accent.TButton"
        ).grid(row=2, column=0, pady=20)
        ttk.Button(
            content_frame, text="Back", command=self.show_main_page, style="Accent.TButton"
        ).grid(row=2, column=1, pady=10)

    def search_apps(self):
        """Mencari aplikasi berdasarkan judul yang dimasukkan."""
        query = self.search_entry.get()
        if not query:
            messagebox.showwarning("Peringatan", "Masukkan judul aplikasi terlebih dahulu!")
            return

        try:
            search_results = search(query)  # Tidak menggunakan parameter limit
            self.apps = [{"title": result["title"], "id": result["appId"]} for result in search_results[:6]]

            if not self.apps:
                messagebox.showinfo("Info", "Tidak ada aplikasi yang ditemukan.")
                return

            self.show_app_selection()
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan saat mencari aplikasi: {e}")

    # ==================== HALAMAN PILIH APLIKASI ====================
    def show_app_selection(self):
        """Menampilkan daftar aplikasi yang ditemukan."""
        self._clear_current_frame()

        self.current_frame = ttk.Frame(self.root, padding="20")
        self.current_frame.pack(fill=tk.BOTH, expand=True)

        content_frame = ttk.Frame(self.current_frame)
        content_frame.pack(expand=True)

        # Label dan Radio Button untuk memilih aplikasi
        ttk.Label(content_frame, text="Pilih Aplikasi:", font=("Helvetica", 14)).grid(
            row=0, column=0, columnspan=2, padx=10, pady=10
        )
        self.app_var = tk.StringVar()
        for i, app in enumerate(self.apps):
            app_label = f"{app['title']} (ID: {app['id']})"
            ttk.Radiobutton(
                content_frame, text=app_label, variable=self.app_var, value=app["id"], style="Toolbutton"
            ).grid(row=i + 1, column=0, columnspan=2, padx=10, pady=5)

            # Tambahkan hyperlink ke aplikasi
            link_label = ttk.Label(content_frame, text="Buka di Play Store", style="Hyperlink.TLabel")
            link_label.grid(row=i + 1, column=2, padx=10, pady=5)
            link_label.bind("<Button-1>", lambda e, app_id=app["id"]: self._open_play_store_link(app_id))

        # Tombol Next dan Back
        ttk.Button(
            content_frame, text="Next", command=self.select_app, style="Accent.TButton"
        ).grid(row=len(self.apps) + 1, column=0, pady=20)
        ttk.Button(
            content_frame, text="Back", command=self.show_search_page, style="Accent.TButton"
        ).grid(row=len(self.apps) + 1, column=1, pady=10)

    def select_app(self):
        """Memilih aplikasi dan melanjutkan ke halaman input jumlah review."""
        self.app_id = self.app_var.get()
        self.show_review_count_page()

    # ==================== HALAMAN INPUT ID ====================
    def show_id_page(self):
        """Menampilkan halaman input ID aplikasi."""
        self._clear_current_frame()

        self.current_frame = ttk.Frame(self.root, padding="20")
        self.current_frame.pack(fill=tk.BOTH, expand=True)

        content_frame = ttk.Frame(self.current_frame)
        content_frame.pack(expand=True)

        # Input ID aplikasi
        ttk.Label(content_frame, text="Masukkan ID Aplikasi:", font=("Helvetica", 14)).grid(
            row=0, column=0, columnspan=2, padx=10, pady=10
        )
        self.id_entry = ttk.Entry(content_frame, width=40, font=("Helvetica", 12))
        self.id_entry.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        # Tombol Next dan Back
        ttk.Button(
            content_frame, text="Next", command=self.input_id, style="Accent.TButton"
        ).grid(row=2, column=0, pady=20)
        ttk.Button(
            content_frame, text="Back", command=self.show_main_page, style="Accent.TButton"
        ).grid(row=2, column=1, pady=10)

    def input_id(self):
        """Memproses input ID aplikasi."""
        self.app_id = self.id_entry.get()
        if not self.app_id:
            messagebox.showwarning("Peringatan", "Masukkan ID aplikasi terlebih dahulu!")
            return

        self.show_review_count_page()

    # ==================== HALAMAN INPUT JUMLAH REVIEW ====================
    def show_review_count_page(self):
        """Menampilkan halaman input jumlah review yang ingin diambil."""
        self._clear_current_frame()

        self.current_frame = ttk.Frame(self.root, padding="20")
        self.current_frame.pack(fill=tk.BOTH, expand=True)

        content_frame = ttk.Frame(self.current_frame)
        content_frame.pack(expand=True)

        # Input jumlah review
        ttk.Label(content_frame, text="Masukkan Jumlah Review yang Ingin Diambil:", font=("Helvetica", 14)).grid(
            row=0, column=0, columnspan=2, padx=10, pady=10
        )
        self.review_count_entry = ttk.Entry(content_frame, width=10, font=("Helvetica", 12))
        self.review_count_entry.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        # Tombol Scrape dan Back
        ttk.Button(
            content_frame, text="Scrape", command=self.scrape_reviews, style="Accent.TButton"
        ).grid(row=2, column=0, pady=20)
        ttk.Button(
            content_frame, text="Back", command=self.show_main_page, style="Accent.TButton"
        ).grid(row=2, column=1, pady=10)

    def scrape_reviews(self):
        """Mengambil review dari aplikasi yang dipilih."""
        try:
            review_count = int(self.review_count_entry.get())
            result, _ = reviews(self.app_id, count=review_count)
            self.reviews_df = pd.DataFrame(result)
            self.show_analysis_page()
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan saat mengambil review: {e}")

    # ==================== HALAMAN ANALISIS ====================
    def show_analysis_page(self):
        """Menampilkan halaman analisis dengan opsi visualisasi data."""
        self._clear_current_frame()

        self.current_frame = ttk.Frame(self.root, padding="20")
        self.current_frame.pack(fill=tk.BOTH, expand=True)

        content_frame = ttk.Frame(self.current_frame)
        content_frame.pack(expand=True)

        # Tampilkan link ke aplikasi di Play Store
        play_store_link = f"https://play.google.com/store/apps/details?id={self.app_id}"
        link_label = ttk.Label(content_frame, text="Buka Aplikasi di Play Store", style="Hyperlink.TLabel")
        link_label.grid(row=0, column=0, padx=10, pady=10)
        link_label.bind("<Button-1>", lambda e: self._open_play_store_link(self.app_id))

        # Tombol untuk menampilkan grafik dan opsi lainnya
        ttk.Button(
            content_frame, text="Tampilkan Grafik Rating", command=self.show_rating_chart, style="Accent.TButton"
        ).grid(row=1, column=0, padx=10, pady=10)
        ttk.Button(
            content_frame,
            text="Tampilkan Rata-rata Rating Berdasarkan Waktu",
            command=self.show_avg_rating_over_time,
            style="Accent.TButton",
        ).grid(row=2, column=0, padx=10, pady=10)
        ttk.Button(
            content_frame, text="Tampilkan Word Cloud", command=self.show_wordcloud, style="Accent.TButton"
        ).grid(row=3, column=0, padx=10, pady=10)
        ttk.Button(
            content_frame, text="Simpan Data ke CSV", command=self.save_to_csv, style="Accent.TButton"
        ).grid(row=4, column=0, padx=10, pady=10)
        ttk.Button(
            content_frame, text="Back", command=self.go_back_to_review_count_page, style="Accent.TButton"
        ).grid(row=5, column=0, pady=10)

    def go_back_to_review_count_page(self):
        """Kembali ke halaman input jumlah review dan menghapus grafik yang ditampilkan."""
        if self.chart_frame:
            self.chart_frame.pack_forget()
            self.chart_frame = None
        self.show_review_count_page()

    # ==================== VISUALISASI DATA ====================
    def show_rating_chart(self):
        """Menampilkan grafik distribusi rating."""
        self._clear_chart_frame()

        self.chart_frame = ttk.Frame(self.root)
        self.chart_frame.pack(fill=tk.BOTH, expand=True)

        fig, ax = plt.subplots(figsize=(8, 6))
        score_distribution = self.reviews_df["score"].value_counts().sort_index()
        score_distribution.plot(kind="bar", color="skyblue", edgecolor="black", ax=ax)
        ax.set_title("Distribusi Rating pada Dataset", fontsize=14)
        ax.set_xlabel("Rating", fontsize=12)
        ax.set_ylabel("Jumlah Ulasan", fontsize=12)
        ax.grid(axis="y", linestyle="--", alpha=0.7)

        self._embed_chart(fig)

    def show_avg_rating_over_time(self):
        """Menampilkan grafik rata-rata rating berdasarkan waktu."""
        self._clear_chart_frame()

        self.chart_frame = ttk.Frame(self.root)
        self.chart_frame.pack(fill=tk.BOTH, expand=True)

        fig, ax = plt.subplots(figsize=(10, 5))
        self.reviews_df["date"] = self.reviews_df["at"].dt.date
        average_ratings = self.reviews_df.groupby("date")["score"].mean().reset_index()
        ax.plot(average_ratings["date"], average_ratings["score"], marker="o")
        ax.set_title("Rata-rata Rating Berdasarkan Waktu")
        ax.set_xlabel("Tanggal")
        ax.set_ylabel("Rata-rata Rating")
        ax.grid()
        plt.xticks(rotation=45)
        plt.tight_layout()

        self._embed_chart(fig)

    def show_wordcloud(self):
        """Menampilkan word cloud dari konten review."""
        self._clear_chart_frame()

        self.chart_frame = ttk.Frame(self.root)
        self.chart_frame.pack(fill=tk.BOTH, expand=True)

        fig, ax = plt.subplots(figsize=(10, 6))
        text_content = " ".join(self.reviews_df["content"])
        wordcloud = WordCloud(width=800, height=480, background_color="white", colormap="viridis").generate(
            text_content
        )
        ax.imshow(wordcloud, interpolation="bilinear")
        ax.axis("off")
        ax.set_title("Word Cloud untuk Kolom Content", fontsize=16)

        self._embed_chart(fig)

    def _embed_chart(self, fig):
        """Menampilkan grafik di Tkinter."""
        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, self.chart_frame)
        toolbar.update()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # ==================== FUNGSI UTILITAS ====================
    def _clear_current_frame(self):
        """Menghapus frame saat ini."""
        if self.current_frame:
            self.current_frame.pack_forget()

    def _clear_chart_frame(self):
        """Menghapus frame grafik jika ada."""
        if self.chart_frame:
            self.chart_frame.pack_forget()
            self.chart_frame = None

    def save_to_csv(self):
        """Menyimpan data review ke file CSV."""
        self.reviews_df.to_csv("playstore_reviews.csv", index=False)
        messagebox.showinfo("Info", "Data telah disimpan ke playstore_reviews.csv")

    def _open_play_store_link(self, app_id):
        """Membuka link Play Store aplikasi di browser."""
        play_store_link = f"https://play.google.com/store/apps/details?id={app_id}"
        webbrowser.open(play_store_link)


if __name__ == "__main__":
    root = ThemedTk(theme="arc")  # Menggunakan ThemedTk dengan tema "arc"
    app = PlayStoreScraperApp(root)
    root.mainloop()