import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import datetime

# ================== KONFIGURASI ==================
NAMA_TOKO = "Toko Kelontong Ghattan"
ALAMAT_TOKO = "Jl. Raya No. 1"
DATA_FILE = "produk_ghattan.json"
FOLDER_STRUK = "struk"

# username : (password, peran)
AKUN = {
    "kasir": ("123", "Kasir"),
    "admin": ("456", "Admin"),
}

MERAH = "#C62828"
MERAH_TUA = "#8E0000"
PUTIH = "#FFFFFF"
ABU = "#F5F5F5"

PRODUK_AWAL = [
    {"kode": "1", "nama": "Beras 5 Kg", "harga_beli": 85000, "harga_jual": 97000, "stok": 20},
    {"kode": "2", "nama": "Gula 1 Kg", "harga_beli": 17000, "harga_jual": 20000, "stok": 35},
    {"kode": "3", "nama": "Minyak Goreng 1 Liter", "harga_beli": 20000, "harga_jual": 25000, "stok": 50},
    {"kode": "4", "nama": "Mie Instan", "harga_beli": 3000, "harga_jual": 4000, "stok": 80},
]


def rp(angka):
    return "Rp {:,.0f}".format(angka).replace(",", ".")


def muat_produk():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    simpan_produk(PRODUK_AWAL)
    return [p.copy() for p in PRODUK_AWAL]


def simpan_produk(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# ================== APLIKASI ==================
class Aplikasi:
    def __init__(self, root):
        self.root = root
        self.root.title(NAMA_TOKO)
        self.root.geometry("1150x650")
        self.root.configure(bg=PUTIH)
        self.produk = muat_produk()
        self.keranjang = {}  # kode -> qty
        self.role = None
        self.atur_style()
        self.tampil_login()

    # ---------- Style ----------
    def atur_style(self):
        s = ttk.Style()
        s.theme_use("clam")
        s.configure("Treeview", background=PUTIH, fieldbackground=PUTIH,
                    rowheight=26, font=("Segoe UI", 10))
        s.configure("Treeview.Heading", background=MERAH, foreground=PUTIH,
                    font=("Segoe UI", 10, "bold"))
        s.map("Treeview.Heading", background=[("active", MERAH_TUA)])
        s.map("Treeview", background=[("selected", "#FFCDD2")],
              foreground=[("selected", "black")])
        s.configure("TNotebook.Tab", padding=(20, 8), font=("Segoe UI", 10, "bold"))
        s.map("TNotebook.Tab", background=[("selected", MERAH)],
              foreground=[("selected", PUTIH)])

    def bersihkan(self):
        for w in self.root.winfo_children():
            w.destroy()

    def tombol(self, parent, teks, cmd, warna=MERAH, **kw):
        return tk.Button(parent, text=teks, command=cmd, bg=warna, fg=PUTIH,
                         activebackground=MERAH_TUA, activeforeground=PUTIH,
                         font=("Segoe UI", 10, "bold"), relief="flat",
                         padx=12, pady=6, cursor="hand2", **kw)

    # ---------- Login ----------
    def tampil_login(self):
        self.bersihkan()
        self.keranjang = {}
        self.root.configure(bg=MERAH)
        box = tk.Frame(self.root, bg=PUTIH, padx=40, pady=30)
        box.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(box, text="🛒 " + NAMA_TOKO.upper(), bg=PUTIH, fg=MERAH,
                 font=("Segoe UI", 18, "bold")).pack(pady=(0, 5))
        tk.Label(box, text="Silakan Login", bg=PUTIH, fg="gray",
                 font=("Segoe UI", 11)).pack(pady=(0, 20))

        tk.Label(box, text="Username", bg=PUTIH, anchor="w").pack(fill="x")
        self.ent_user = tk.Entry(box, font=("Segoe UI", 11), bd=2, relief="groove")
        self.ent_user.pack(fill="x", pady=(0, 10), ipady=4)
        self.ent_user.bind("<Return>", lambda e: self.ent_pass.focus())
        self.ent_user.focus()

        tk.Label(box, text="Password", bg=PUTIH, anchor="w").pack(fill="x")
        self.ent_pass = tk.Entry(box, show="*", font=("Segoe UI", 11), bd=2,
                                 relief="groove")
        self.ent_pass.pack(fill="x", pady=(0, 20), ipady=4)
        self.ent_pass.bind("<Return>", lambda e: self.proses_login())

        self.tombol(box, "LOGIN", self.proses_login).pack(fill="x")

    def proses_login(self):
        user = self.ent_user.get().strip().lower()
        pw = self.ent_pass.get()
        if user in AKUN and AKUN[user][0] == pw:
            self.role = AKUN[user][1]
            self.tampil_utama()
        else:
            messagebox.showerror("Gagal", "Username atau password salah!")
            self.ent_pass.delete(0, "end")

    # ---------- Halaman Utama ----------
    def tampil_utama(self):
        self.bersihkan()
        self.root.configure(bg=PUTIH)

        header = tk.Frame(self.root, bg=MERAH)
        header.pack(fill="x")
        tk.Label(header, text="🛒 " + NAMA_TOKO, bg=MERAH, fg=PUTIH,
                 font=("Segoe UI", 16, "bold")).pack(side="left", padx=15, pady=10)
        tk.Button(header, text="Logout", command=self.tampil_login, bg=PUTIH,
                  fg=MERAH, font=("Segoe UI", 10, "bold"), relief="flat",
                  padx=10).pack(side="right", padx=15)
        tk.Label(header, text=f"Login: {self.role}", bg=MERAH, fg=PUTIH,
                 font=("Segoe UI", 10)).pack(side="right")

        nb = ttk.Notebook(self.root)
        nb.pack(fill="both", expand=True, padx=8, pady=8)

        tab_kasir = tk.Frame(nb, bg=PUTIH)
        nb.add(tab_kasir, text="  KASIR  ")
        self.buat_tab_kasir(tab_kasir)

        if self.role == "Admin":
            tab_admin = tk.Frame(nb, bg=PUTIH)
            nb.add(tab_admin, text="  KELOLA STOK & HARGA  ")
            self.buat_tab_admin(tab_admin)

    # ---------- Tab Kasir ----------
    def buat_tab_kasir(self, parent):
        kiri = tk.Frame(parent, bg=PUTIH)
        kiri.pack(side="left", fill="both", expand=True, padx=(5, 5), pady=5)
        kanan = tk.Frame(parent, bg=ABU, width=430)
        kanan.pack(side="right", fill="y", padx=(5, 5), pady=5)
        kanan.pack_propagate(False)

        # -- Kiri: daftar produk --
        tk.Label(kiri, text="Daftar Barang", bg=PUTIH, fg=MERAH,
                 font=("Segoe UI", 13, "bold")).pack(anchor="w")
        frm_cari = tk.Frame(kiri, bg=PUTIH)
        frm_cari.pack(fill="x", pady=5)
        tk.Label(frm_cari, text="Cari:", bg=PUTIH).pack(side="left")
        self.var_cari = tk.StringVar()
        self.var_cari.trace_add("write", lambda *a: self.isi_tabel_kasir())
        tk.Entry(frm_cari, textvariable=self.var_cari, font=("Segoe UI", 11),
                 bd=2, relief="groove").pack(side="left", fill="x", expand=True,
                                              padx=5, ipady=3)

        cols = ("kode", "nama", "harga", "stok")
        self.tv_kasir = ttk.Treeview(kiri, columns=cols, show="headings")
        for c, t, w in [("kode", "Kode", 70), ("nama", "Nama Barang", 250),
                        ("harga", "Harga Jual", 110), ("stok", "Stok", 60)]:
            self.tv_kasir.heading(c, text=t)
            self.tv_kasir.column(c, width=w, anchor="w" if c == "nama" else "center")
        self.tv_kasir.pack(fill="both", expand=True)
        self.tv_kasir.bind("<Double-1>", lambda e: self.tambah_keranjang())
        self.tv_kasir.tag_configure("habis", foreground="red")

        frm_add = tk.Frame(kiri, bg=PUTIH)
        frm_add.pack(fill="x", pady=8)
        tk.Label(frm_add, text="Jumlah:", bg=PUTIH).pack(side="left")
        self.spin_qty = tk.Spinbox(frm_add, from_=1, to=999, width=6,
                                   font=("Segoe UI", 11))
        self.spin_qty.pack(side="left", padx=5)
        self.tombol(frm_add, "+ Tambah ke Keranjang",
                    self.tambah_keranjang).pack(side="left", padx=5)

        # -- Kanan: keranjang --
        tk.Label(kanan, text="Keranjang Belanja", bg=ABU, fg=MERAH,
                 font=("Segoe UI", 13, "bold")).pack(anchor="w", padx=8, pady=5)
        cols2 = ("nama", "qty", "sub")
        self.tv_cart = ttk.Treeview(kanan, columns=cols2, show="headings", height=10)
        for c, t, w in [("nama", "Barang", 180), ("qty", "Qty", 45),
                        ("sub", "Subtotal", 110)]:
            self.tv_cart.heading(c, text=t)
            self.tv_cart.column(c, width=w, anchor="w" if c == "nama" else "center")
        self.tv_cart.pack(fill="x", padx=8)

        frm_btn = tk.Frame(kanan, bg=ABU)
        frm_btn.pack(fill="x", padx=8, pady=5)
        self.tombol(frm_btn, "Hapus Item", self.hapus_item,
                    warna="#616161").pack(side="left", padx=(0, 5))
        self.tombol(frm_btn, "Kosongkan", self.kosongkan,
                    warna="#616161").pack(side="left")

        self.lbl_total = tk.Label(kanan, text="TOTAL: Rp 0", bg=ABU, fg=MERAH,
                                  font=("Segoe UI", 18, "bold"))
        self.lbl_total.pack(pady=(10, 5))

        tk.Label(kanan, text="Uang Bayar (Rp):", bg=ABU,
                 font=("Segoe UI", 10)).pack(anchor="w", padx=8)
        self.var_bayar = tk.StringVar()
        self.var_bayar.trace_add("write", lambda *a: self.hitung_kembalian())
        ent = tk.Entry(kanan, textvariable=self.var_bayar,
                       font=("Segoe UI", 14), bd=2, relief="groove")
        ent.pack(fill="x", padx=8, pady=3, ipady=4)
        ent.bind("<Return>", lambda e: self.bayar())

        self.lbl_kembali = tk.Label(kanan, text="Kembalian: Rp 0", bg=ABU,
                                    fg="#1B5E20", font=("Segoe UI", 14, "bold"))
        self.lbl_kembali.pack(pady=8)

        self.tombol(kanan, "BAYAR & CETAK STRUK", self.bayar).pack(
            fill="x", padx=8, pady=5)

        self.isi_tabel_kasir()

    def cari_produk(self, kode):
        for p in self.produk:
            if p["kode"] == kode:
                return p
        return None

    def isi_tabel_kasir(self):
        self.tv_kasir.delete(*self.tv_kasir.get_children())
        kata = self.var_cari.get().lower()
        for p in self.produk:
            if kata in p["nama"].lower() or kata in p["kode"].lower():
                tag = ("habis",) if p["stok"] <= 0 else ()
                self.tv_kasir.insert("", "end", iid=p["kode"], tags=tag,
                                     values=(p["kode"], p["nama"],
                                             rp(p["harga_jual"]), p["stok"]))

    def tambah_keranjang(self):
        sel = self.tv_kasir.selection()
        if not sel:
            messagebox.showwarning("Info", "Pilih barang terlebih dahulu.")
            return
        try:
            qty = int(self.spin_qty.get())
            if qty <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Jumlah tidak valid.")
            return
        p = self.cari_produk(sel[0])
        sudah = self.keranjang.get(p["kode"], 0)
        if sudah + qty > p["stok"]:
            messagebox.showwarning("Stok Kurang",
                                   f"Stok {p['nama']} hanya {p['stok']}.")
            return
        self.keranjang[p["kode"]] = sudah + qty
        self.refresh_keranjang()

    def hapus_item(self):
        sel = self.tv_cart.selection()
        if sel:
            self.keranjang.pop(sel[0], None)
            self.refresh_keranjang()

    def kosongkan(self):
        self.keranjang.clear()
        self.refresh_keranjang()

    def total(self):
        return sum(self.cari_produk(k)["harga_jual"] * q
                   for k, q in self.keranjang.items())

    def refresh_keranjang(self):
        self.tv_cart.delete(*self.tv_cart.get_children())
        for k, q in self.keranjang.items():
            p = self.cari_produk(k)
            self.tv_cart.insert("", "end", iid=k,
                                values=(p["nama"], q, rp(p["harga_jual"] * q)))
        self.lbl_total.config(text=f"TOTAL: {rp(self.total())}")
        self.hitung_kembalian()

    def ambil_bayar(self):
        teks = self.var_bayar.get().replace(".", "").replace(",", "").strip()
        return int(teks) if teks.isdigit() else 0

    def hitung_kembalian(self):
        kembali = self.ambil_bayar() - self.total()
        if self.ambil_bayar() > 0 and kembali >= 0:
            self.lbl_kembali.config(text=f"Kembalian: {rp(kembali)}", fg="#1B5E20")
        elif self.ambil_bayar() > 0:
            self.lbl_kembali.config(text=f"Kurang: {rp(-kembali)}", fg="red")
        else:
            self.lbl_kembali.config(text="Kembalian: Rp 0", fg="#1B5E20")

    def bayar(self):
        if not self.keranjang:
            messagebox.showwarning("Info", "Keranjang masih kosong.")
            return
        total = self.total()
        bayar = self.ambil_bayar()
        if bayar < total:
            messagebox.showerror("Gagal", "Uang bayar kurang!")
            return
        kembali = bayar - total

        item_struk = []
        for k, q in self.keranjang.items():
            p = self.cari_produk(k)
            p["stok"] -= q
            item_struk.append((p["nama"], q, p["harga_jual"]))
        simpan_produk(self.produk)

        struk = self.buat_struk(item_struk, total, bayar, kembali)
        self.tampil_struk(struk)

        self.keranjang.clear()
        self.var_bayar.set("")
        self.refresh_keranjang()
        self.isi_tabel_kasir()
        if self.role == "Admin":
            self.isi_tabel_admin()

    # ---------- Struk ----------
    def buat_struk(self, items, total, bayar, kembali):
        lebar = 38
        now = datetime.datetime.now()
        baris = [
            NAMA_TOKO.upper().center(lebar),
            ALAMAT_TOKO.center(lebar),
            "=" * lebar,
            f"Tanggal : {now.strftime('%d-%m-%Y %H:%M:%S')}",
            f"Kasir   : {self.role}",
            "-" * lebar,
        ]
        for nama, qty, harga in items:
            baris.append(nama[:lebar])
            kiri = f"  {qty} x {rp(harga)}"
            kanan = rp(qty * harga)
            baris.append(kiri + kanan.rjust(lebar - len(kiri)))
        baris.append("-" * lebar)
        for label, nilai in [("TOTAL", total), ("BAYAR", bayar), ("KEMBALI", kembali)]:
            kiri = f"{label}"
            kanan = rp(nilai)
            baris.append(kiri + kanan.rjust(lebar - len(kiri)))
        baris += ["=" * lebar, "Terima Kasih".center(lebar),
                  "Selamat Belanja Kembali".center(lebar)]
        return "\n".join(baris)

    def tampil_struk(self, teks):
        os.makedirs(FOLDER_STRUK, exist_ok=True)
        nama_file = os.path.join(
            FOLDER_STRUK,
            "struk_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + ".txt")
        with open(nama_file, "w", encoding="utf-8") as f:
            f.write(teks)

        win = tk.Toplevel(self.root)
        win.title("Struk Pembayaran")
        win.configure(bg=PUTIH)
        win.geometry("400x520")
        txt = tk.Text(win, font=("Courier New", 10), width=40, bd=0)
        txt.pack(fill="both", expand=True, padx=10, pady=10)
        txt.insert("1.0", teks)
        txt.config(state="disabled")

        frm = tk.Frame(win, bg=PUTIH)
        frm.pack(pady=8)

        def cetak():
            try:
                os.startfile(os.path.abspath(nama_file), "print")  # Windows
            except Exception:
                messagebox.showinfo(
                    "Info", f"Struk tersimpan di:\n{os.path.abspath(nama_file)}\n"
                            "Silakan cetak manual dari file tersebut.")

        self.tombol(frm, "🖨 Cetak", cetak).pack(side="left", padx=5)
        self.tombol(frm, "Tutup", win.destroy, warna="#616161").pack(side="left", padx=5)

    # ---------- Tab Admin ----------
    def buat_tab_admin(self, parent):
        form = tk.Frame(parent, bg=ABU, width=320)
        form.pack(side="right", fill="y", padx=5, pady=5)
        form.pack_propagate(False)
        kiri = tk.Frame(parent, bg=PUTIH)
        kiri.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        cols = ("kode", "nama", "beli", "jual", "laba", "stok")
        self.tv_admin = ttk.Treeview(kiri, columns=cols, show="headings")
        for c, t, w in [("kode", "Kode", 60), ("nama", "Nama Barang", 200),
                        ("beli", "Harga Beli", 100), ("jual", "Harga Jual", 100),
                        ("laba", "Laba/Item", 90), ("stok", "Stok", 60)]:
            self.tv_admin.heading(c, text=t)
            self.tv_admin.column(c, width=w, anchor="w" if c == "nama" else "center")
        self.tv_admin.pack(fill="both", expand=True)
        self.tv_admin.bind("<<TreeviewSelect>>", self.pilih_admin)

        tk.Label(form, text="Data Barang", bg=ABU, fg=MERAH,
                 font=("Segoe UI", 13, "bold")).pack(pady=10)
        self.f_kode, self.f_nama = tk.StringVar(), tk.StringVar()
        self.f_beli, self.f_jual = tk.StringVar(), tk.StringVar()
        self.f_stok = tk.StringVar()
        for label, var in [("Kode (angka, kosongkan untuk otomatis)", self.f_kode),
                           ("Nama Barang", self.f_nama),
                           ("Harga Beli (Rp)", self.f_beli),
                           ("Harga Jual (Rp)", self.f_jual), ("Stok", self.f_stok)]:
            tk.Label(form, text=label, bg=ABU, anchor="w").pack(fill="x", padx=12)
            tk.Entry(form, textvariable=var, font=("Segoe UI", 11), bd=2,
                     relief="groove").pack(fill="x", padx=12, pady=(0, 6), ipady=3)

        self.tombol(form, "Simpan (Tambah/Update)", self.simpan_admin).pack(
            fill="x", padx=12, pady=4)
        self.tombol(form, "Hapus Barang", self.hapus_admin, warna="#616161").pack(
            fill="x", padx=12, pady=4)
        self.tombol(form, "Kosongkan Form", self.reset_form, warna="#616161").pack(
            fill="x", padx=12, pady=4)

        self.isi_tabel_admin()

    def isi_tabel_admin(self):
        self.tv_admin.delete(*self.tv_admin.get_children())
        for p in self.produk:
            laba = p["harga_jual"] - p["harga_beli"]
            self.tv_admin.insert("", "end", iid=p["kode"],
                                 values=(p["kode"], p["nama"], rp(p["harga_beli"]),
                                         rp(p["harga_jual"]), rp(laba), p["stok"]))

    def pilih_admin(self, _=None):
        sel = self.tv_admin.selection()
        if sel:
            p = self.cari_produk(sel[0])
            self.f_kode.set(p["kode"])
            self.f_nama.set(p["nama"])
            self.f_beli.set(p["harga_beli"])
            self.f_jual.set(p["harga_jual"])
            self.f_stok.set(p["stok"])

    def reset_form(self):
        for v in (self.f_kode, self.f_nama, self.f_beli, self.f_jual, self.f_stok):
            v.set("")

    def kode_berikutnya(self):
        angka = [int(p["kode"]) for p in self.produk if p["kode"].isdigit()]
        return str(max(angka) + 1 if angka else 1)

    def simpan_admin(self):
        kode = self.f_kode.get().strip()
        nama = self.f_nama.get().strip()
        if kode and not kode.isdigit():
            messagebox.showerror("Error", "Kode barang harus berupa angka saja.")
            return
        try:
            beli = int(self.f_beli.get())
            jual = int(self.f_jual.get())
            stok = int(self.f_stok.get())
            if beli < 0 or jual < 0 or stok < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Harga dan stok harus angka (>= 0).")
            return
        if not nama:
            messagebox.showerror("Error", "Nama barang wajib diisi.")
            return
        if not kode:
            kode = self.kode_berikutnya()
        if jual < beli:
            if not messagebox.askyesno(
                    "Peringatan", "Harga jual lebih kecil dari harga beli (rugi).\n"
                                  "Tetap simpan?"):
                return
        p = self.cari_produk(kode)
        if p:
            p.update({"nama": nama, "harga_beli": beli,
                      "harga_jual": jual, "stok": stok})
        else:
            self.produk.append({"kode": kode, "nama": nama, "harga_beli": beli,
                                "harga_jual": jual, "stok": stok})
        simpan_produk(self.produk)
        self.isi_tabel_admin()
        self.isi_tabel_kasir()
        self.reset_form()
        messagebox.showinfo("Sukses", f"Data barang (kode {kode}) tersimpan.")

    def hapus_admin(self):
        sel = self.tv_admin.selection()
        if not sel:
            messagebox.showwarning("Info", "Pilih barang yang akan dihapus.")
            return
        if messagebox.askyesno("Konfirmasi", "Yakin hapus barang ini?"):
            self.produk = [p for p in self.produk if p["kode"] != sel[0]]
            self.keranjang.pop(sel[0], None)
            simpan_produk(self.produk)
            self.isi_tabel_admin()
            self.isi_tabel_kasir()
            self.refresh_keranjang()
            self.reset_form()


if __name__ == "__main__":
    root = tk.Tk()
    Aplikasi(root)
    root.mainloop()