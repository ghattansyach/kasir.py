import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
import os

# ==========================
# TEMA SMART RETAIL GHATTAN
# ==========================
MERAH = "#C62828"
PUTIH = "#FFFFFF"
ABU = "#F5F5F5"

# ==========================
# DATABASE SQLITE
# ==========================
conn = sqlite3.connect("smart_retail.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS users(
    username TEXT PRIMARY KEY,
    password TEXT,
    role TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS produk(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama TEXT,
    harga INTEGER,
    stok INTEGER
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS transaksi(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tanggal TEXT,
    kasir TEXT,
    total INTEGER,
    bayar INTEGER,
    kembali INTEGER
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS detail_transaksi(
    id_transaksi INTEGER,
    nama TEXT,
    jumlah INTEGER,
    subtotal INTEGER
)
""")

# ==========================
# USER LOGIN
# ==========================
cur.execute("DELETE FROM users")

cur.execute(
    "INSERT INTO users VALUES(?,?,?)",
    ("admin","1234","admin")
)

cur.execute(
    "INSERT INTO users VALUES(?,?,?)",
    ("kasir","1234","kasir")
)

# ==========================
# PRODUK AWAL
# ==========================
cur.execute("SELECT COUNT(*) FROM produk")

if cur.fetchone()[0] == 0:

    produk_awal = [
        ("Beras Premium 5 Kg",78000,25),
        ("Minyak Goreng 1 Liter",22000,40),
        ("Gula Pasir 1 Kg",19000,35),
        ("Mie Instan",3500,120),
        ("Telur Ayam 1 Kg",30000,20),
        ("Susu UHT 1 Liter",18000,30),
        ("Air Mineral 600 ml",4000,150),
        ("Sabun Mandi",8500,45),
        ("Shampoo Sachet",2000,100),
        ("Pasta Gigi",12000,40)
    ]

    cur.executemany(
        "INSERT INTO produk(nama,harga,stok) VALUES(?,?,?)",
        produk_awal
    )

conn.commit()

# ==========================
# WINDOW LOGIN
# ==========================
root = tk.Tk()
root.title("SMART RETAIL GHATTAN")
root.geometry("400x500")
root.configure(bg=PUTIH)
root.resizable(False, False)

# Header
tk.Label(
    root,
    text="SMART RETAIL GHATTAN",
    bg=MERAH,
    fg="white",
    font=("Arial",16,"bold"),
    pady=15
).pack(fill="x")

tk.Label(
    root,
    text="Aplikasi Kasir Toko Kelontong",
    bg=PUTIH,
    fg=MERAH,
    font=("Arial",10)
).pack(pady=15)

# Form Login
tk.Label(root, text="Username", bg=PUTIH).pack(anchor="w", padx=40)
entry_user = tk.Entry(root, width=30, font=("Arial",11))
entry_user.pack(pady=5)

tk.Label(root, text="Password", bg=PUTIH).pack(anchor="w", padx=40)
entry_pass = tk.Entry(root, width=30, show="*", font=("Arial",11))
entry_pass.pack(pady=5)

status_login = tk.Label(
    root,
    text="",
    bg=PUTIH,
    fg="red",
    font=("Arial",10)
)
status_login.pack(pady=10)

# ==========================
# FUNGSI LOGIN
# ==========================

def login():

    username = entry_user.get().strip()
    password = entry_pass.get().strip()

    cur.execute(
        "SELECT role FROM users WHERE username=? AND password=?",
        (username, password)
    )

    hasil = cur.fetchone()

    if hasil:
        role = hasil[0]

        status_login.config(
            text="Login Berhasil ✔",
            fg="green"
        )

        messagebox.showinfo(
            "SMART RETAIL GHATTAN",
            f"Selamat datang {username}"
        )

        root.withdraw()      # sembunyikan login

        if role == "admin":
            dashboard_admin(username)
        else:
            dashboard_kasir(username)

    else:
        status_login.config(
            text="Username atau Password Salah!",
            fg="red"
        )

        entry_pass.delete(0, tk.END)

# Tombol Login
tk.Button(
    root,
    text="LOGIN",
    bg=MERAH,
    fg="white",
    width=20,
    font=("Arial",11,"bold"),
    command=login
).pack(pady=20)

# Info Login
tk.Label(
    root,
    text="Admin : admin / 1234\nKasir : kasir / 1234",
    bg=PUTIH,
    fg="gray"
).pack(side="bottom", pady=20)
# =====================================================
# PART 2 - DASHBOARD ADMIN & KASIR
# =====================================================

# ---------------- DASHBOARD ADMIN ----------------

def dashboard_admin(username):

    admin = tk.Toplevel()
    admin.title("SMART RETAIL GHATTAN - ADMIN")
    admin.geometry("700x500")
    admin.configure(bg=PUTIH)

    tk.Label(
        admin,
        text=f"SMART RETAIL GHATTAN - ADMIN ({username})",
        bg=MERAH,
        fg="white",
        font=("Arial",14,"bold"),
        pady=10
    ).pack(fill="x")

    # ===== TABEL PRODUK =====
    tree = ttk.Treeview(
        admin,
        columns=("ID","Nama","Harga","Stok"),
        show="headings",
        height=12
    )

    for col in ("ID","Nama","Harga","Stok"):
        tree.heading(col, text=col)

    tree.column("ID", width=50, anchor="center")
    tree.column("Nama", width=250)
    tree.column("Harga", width=120, anchor="center")
    tree.column("Stok", width=80, anchor="center")

    tree.pack(padx=10, pady=10, fill="x")

    def tampil_produk():
        tree.delete(*tree.get_children())

        cur.execute("SELECT * FROM produk ORDER BY id")

        for row in cur.fetchall():
            tree.insert("", tk.END, values=row)

    tampil_produk()

    # ===== FORM =====
    frame_form = tk.Frame(admin, bg=PUTIH)
    frame_form.pack(pady=10)

    tk.Label(frame_form, text="Nama", bg=PUTIH).grid(row=0, column=0)
    nama_entry = tk.Entry(frame_form, width=25)
    nama_entry.grid(row=0, column=1)

    tk.Label(frame_form, text="Harga", bg=PUTIH).grid(row=1, column=0)
    harga_entry = tk.Entry(frame_form, width=25)
    harga_entry.grid(row=1, column=1)

    tk.Label(frame_form, text="Stok", bg=PUTIH).grid(row=2, column=0)
    stok_entry = tk.Entry(frame_form, width=25)
    stok_entry.grid(row=2, column=1)

    id_produk = tk.StringVar()

    # Klik tabel
    def pilih_produk(event):
        data = tree.focus()
        if not data:
            return

        item = tree.item(data)["values"]

        id_produk.set(item[0])

        nama_entry.delete(0, tk.END)
        harga_entry.delete(0, tk.END)
        stok_entry.delete(0, tk.END)

        nama_entry.insert(0, item[1])
        harga_entry.insert(0, item[2])
        stok_entry.insert(0, item[3])

    tree.bind("<<TreeviewSelect>>", pilih_produk)

    # Tambah Produk
    def tambah_produk():

        cur.execute("""
            INSERT INTO produk(nama,harga,stok)
            VALUES(?,?,?)
        """,(
            nama_entry.get(),
            int(harga_entry.get()),
            int(stok_entry.get())
        ))

        conn.commit()
        tampil_produk()

        messagebox.showinfo("Sukses","Produk berhasil ditambahkan.")

    # Edit Produk
    def edit_produk():

        if id_produk.get()=="":
            return

        cur.execute("""
            UPDATE produk
            SET nama=?, harga=?, stok=?
            WHERE id=?
        """,(
            nama_entry.get(),
            int(harga_entry.get()),
            int(stok_entry.get()),
            id_produk.get()
        ))

        conn.commit()
        tampil_produk()

        messagebox.showinfo("Sukses","Produk berhasil diubah.")

    # Hapus Produk
    def hapus_produk():

        if id_produk.get()=="":
            return

        jawab = messagebox.askyesno(
            "Konfirmasi",
            "Hapus produk ini?"
        )

        if jawab:

            cur.execute(
                "DELETE FROM produk WHERE id=?",
                (id_produk.get(),)
            )

            conn.commit()
            tampil_produk()

            messagebox.showinfo("Sukses","Produk berhasil dihapus.")

    # Tombol
    tombol = tk.Frame(admin, bg=PUTIH)
    tombol.pack()

    tk.Button(
        tombol,
        text="Tambah",
        bg=MERAH,
        fg="white",
        width=10,
        command=tambah_produk
    ).grid(row=0,column=0,padx=5)

    tk.Button(
        tombol,
        text="Edit",
        bg="orange",
        fg="white",
        width=10,
        command=edit_produk
    ).grid(row=0,column=1,padx=5)

    tk.Button(
        tombol,
        text="Hapus",
        bg="gray",
        fg="white",
        width=10,
        command=hapus_produk
    ).grid(row=0,column=2,padx=5)

    tk.Button(
        tombol,
        text="Logout",
        bg="black",
        fg="white",
        width=10,
        command=lambda:[admin.destroy(), root.deiconify()]
    ).grid(row=0,column=3,padx=5)


# ---------------- DASHBOARD KASIR ----------------

def dashboard_kasir(username):

    kasir = tk.Toplevel()
    kasir.title("SMART RETAIL GHATTAN - KASIR")
    kasir.geometry("700x500")
    kasir.configure(bg=PUTIH)

    tk.Label(
        kasir,
        text=f"SMART RETAIL GHATTAN - KASIR ({username})",
        bg=MERAH,
        fg="white",
        font=("Arial",14,"bold"),
        pady=10
    ).pack(fill="x")

    tree = ttk.Treeview(
        kasir,
        columns=("ID","Nama","Harga","Stok"),
        show="headings",
        height=15
    )

    for col in ("ID","Nama","Harga","Stok"):
        tree.heading(col,text=col)

    tree.column("ID",width=50,anchor="center")
    tree.column("Nama",width=260)
    tree.column("Harga",width=120,anchor="center")
    tree.column("Stok",width=80,anchor="center")

    tree.pack(fill="x",padx=10,pady=15)

    def tampil_produk():
        tree.delete(*tree.get_children())

        cur.execute("SELECT * FROM produk ORDER BY id")

        for row in cur.fetchall():
            tree.insert("",tk.END,values=row)

    tampil_produk()

    tk.Label(
        kasir,
        text="Silakan pilih produk untuk transaksi.",
        bg=PUTIH,
        fg=MERAH,
        font=("Arial",11,"bold")
    ).pack()

    tk.Button(
        kasir,
        text="Logout",
        bg="black",
        fg="white",
        width=12,
        command=lambda:[kasir.destroy(), root.deiconify()]
    ).pack(pady=20)
    # =====================================================
# PART 3 - TRANSAKSI KASIR
# =====================================================

# GANTI fungsi dashboard_kasir() yang ada di PART 2 dengan fungsi ini.

def dashboard_kasir(username):

    kasir = tk.Toplevel()
    kasir.title("SMART RETAIL GHATTAN - KASIR")
    kasir.geometry("900x600")
    kasir.configure(bg=PUTIH)

    tk.Label(
        kasir,
        text=f"SMART RETAIL GHATTAN - KASIR ({username})",
        bg=MERAH,
        fg="white",
        font=("Arial",14,"bold"),
        pady=10
    ).pack(fill="x")

    # ================= TABEL PRODUK =================
    tree = ttk.Treeview(
        kasir,
        columns=("ID","Nama","Harga","Stok"),
        show="headings",
        height=10
    )

    for col in ("ID","Nama","Harga","Stok"):
        tree.heading(col, text=col)

    tree.column("ID", width=50, anchor="center")
    tree.column("Nama", width=250)
    tree.column("Harga", width=120, anchor="center")
    tree.column("Stok", width=80, anchor="center")

    tree.pack(fill="x", padx=10, pady=10)

    def tampil_produk():
        tree.delete(*tree.get_children())

        cur.execute("SELECT * FROM produk ORDER BY id")

        for row in cur.fetchall():
            tree.insert("", tk.END, values=row)

    tampil_produk()

    # ================= KERANJANG =================
    tk.Label(
        kasir,
        text="KERANJANG BELANJA",
        bg=PUTIH,
        fg=MERAH,
        font=("Arial",12,"bold")
    ).pack()

    keranjang = ttk.Treeview(
        kasir,
        columns=("Produk","Jumlah","Subtotal"),
        show="headings",
        height=6
    )

    keranjang.heading("Produk", text="Produk")
    keranjang.heading("Jumlah", text="Jumlah")
    keranjang.heading("Subtotal", text="Subtotal")

    keranjang.column("Produk", width=250)
    keranjang.column("Jumlah", width=80, anchor="center")
    keranjang.column("Subtotal", width=120, anchor="center")

    keranjang.pack(fill="x", padx=10)

    daftar_belanja = []
    total_belanja = 0

    # ================= FORM BELI =================
    frame = tk.Frame(kasir, bg=PUTIH)
    frame.pack(pady=10)

    tk.Label(frame, text="Jumlah Beli", bg=PUTIH).grid(row=0, column=0)

    jumlah_entry = tk.Entry(frame, width=10)
    jumlah_entry.grid(row=0, column=1, padx=5)

    total_label = tk.Label(
        kasir,
        text="TOTAL : Rp0",
        bg=PUTIH,
        fg=MERAH,
        font=("Arial",13,"bold")
    )
    total_label.pack(pady=10)

    # ================= TAMBAH KE KERANJANG =================
    def tambah_keranjang():

        nonlocal total_belanja

        pilih = tree.focus()

        if pilih == "":
            messagebox.showwarning(
                "Pilih Produk",
                "Pilih produk terlebih dahulu."
            )
            return

        item = tree.item(pilih)["values"]

        jumlah = int(jumlah_entry.get())

        if jumlah > item[3]:
            messagebox.showerror(
                "Stok",
                "Stok tidak mencukupi."
            )
            return

        subtotal = item[2] * jumlah

        total_belanja += subtotal

        total_label.config(
            text=f"TOTAL : Rp{total_belanja:,}"
        )

        keranjang.insert(
            "",
            tk.END,
            values=(item[1], jumlah, f"Rp{subtotal:,}")
        )

        daftar_belanja.append(
            {
                "id": item[0],
                "nama": item[1],
                "jumlah": jumlah,
                "subtotal": subtotal
            }
        )

        jumlah_entry.delete(0, tk.END)

    tk.Button(
        frame,
        text="Tambah Keranjang",
        bg=MERAH,
        fg="white",
        command=tambah_keranjang
    ).grid(row=0, column=2, padx=10)

    # ================= PEMBAYARAN =================
    bayar_frame = tk.Frame(kasir, bg=PUTIH)
    bayar_frame.pack(pady=10)

    tk.Label(
        bayar_frame,
        text="Bayar (Rp)",
        bg=PUTIH
    ).grid(row=0, column=0)

    bayar_entry = tk.Entry(bayar_frame, width=18)
    bayar_entry.grid(row=0, column=1, padx=5)

    kembali_label = tk.Label(
        bayar_frame,
        text="KEMBALIAN : Rp0",
        bg=PUTIH,
        fg="green",
        font=("Arial",12,"bold")
    )
    kembali_label.grid(row=1, column=0, columnspan=2, pady=8)

    # ================= HITUNG KEMBALIAN =================
    def hitung_kembalian():

        bayar = int(bayar_entry.get())

        if bayar < total_belanja:
            messagebox.showerror(
                "Pembayaran",
                "Uang pelanggan kurang."
            )
            return

        kembali = bayar - total_belanja

        kembali_label.config(
            text=f"KEMBALIAN : Rp{kembali:,}"
        )

    tk.Button(
        bayar_frame,
        text="Hitung Kembalian",
        bg="green",
        fg="white",
        command=hitung_kembalian
    ).grid(row=0, column=2, padx=10)

    # ================= SIMPAN TRANSAKSI =================
    def simpan_transaksi():

        nonlocal total_belanja

        if len(daftar_belanja) == 0:
            messagebox.showwarning(
                "Keranjang",
                "Belum ada barang."
            )
            return

        bayar = int(bayar_entry.get())
        kembali = bayar - total_belanja

        tanggal = datetime.now().strftime("%d/%m/%Y %H:%M")

        cur.execute("""
            INSERT INTO transaksi
            (tanggal,kasir,total,bayar,kembali)
            VALUES(?,?,?,?,?)
        """, (
            tanggal,
            username,
            total_belanja,
            bayar,
            kembali
        ))

        id_transaksi = cur.lastrowid

        # Simpan detail & update stok
        for item in daftar_belanja:

            cur.execute("""
                INSERT INTO detail_transaksi
                VALUES(?,?,?,?)
            """, (
                id_transaksi,
                item["nama"],
                item["jumlah"],
                item["subtotal"]
            ))

            cur.execute("""
                UPDATE produk
                SET stok = stok - ?
                WHERE id = ?
            """, (
                item["jumlah"],
                item["id"]
            ))

        conn.commit()

        messagebox.showinfo(
            "Sukses",
            f"Transaksi berhasil!\nKembalian : Rp{kembali:,}"
        )

        # Bersihkan keranjang
        keranjang.delete(*keranjang.get_children())
        daftar_belanja.clear()
        total_belanja = 0

        total_label.config(text="TOTAL : Rp0")
        kembali_label.config(text="KEMBALIAN : Rp0")
        bayar_entry.delete(0, tk.END)

        tampil_produk()

    tk.Button(
        kasir,
        text="Simpan Transaksi",
        bg=MERAH,
        fg="white",
        width=20,
        command=simpan_transaksi
    ).pack(pady=10)

    tk.Button(
        kasir,
        text="Logout",
        bg="black",
        fg="white",
        width=15,
        command=lambda:[kasir.destroy(), root.deiconify()]
    ).pack()
    # =====================================================
# PART 4 - STRUK, RIWAYAT DAN LAPORAN
# =====================================================

import matplotlib.pyplot as plt

# ================= CETAK STRUK =================

def cetak_struk(id_transaksi):

    if not os.path.exists("receipt"):
        os.makedirs("receipt")

    cur.execute("""
        SELECT tanggal, kasir, total, bayar, kembali
        FROM transaksi
        WHERE id=?
    """, (id_transaksi,))

    trx = cur.fetchone()

    cur.execute("""
        SELECT nama, jumlah, subtotal
        FROM detail_transaksi
        WHERE id_transaksi=?
    """, (id_transaksi,))

    barang = cur.fetchall()

    with open("receipt/struk.txt", "w", encoding="utf-8") as f:

        f.write("="*35 + "\n")
        f.write("   SMART RETAIL GHATTAN\n")
        f.write(" TOKO KELONTONG MODERN\n")
        f.write("="*35 + "\n\n")

        f.write(f"Tanggal : {trx[0]}\n")
        f.write(f"Kasir   : {trx[1]}\n")
        f.write("-"*35 + "\n")

        for item in barang:
            f.write(f"{item[0]}\n")
            f.write(f"{item[1]} x Rp{item[2]//item[1]:,}")
            f.write(f" = Rp{item[2]:,}\n\n")

        f.write("-"*35 + "\n")
        f.write(f"TOTAL      : Rp{trx[2]:,}\n")
        f.write(f"BAYAR      : Rp{trx[3]:,}\n")
        f.write(f"KEMBALIAN  : Rp{trx[4]:,}\n")
        f.write("="*35 + "\n")
        f.write(" Terima Kasih Sudah Berbelanja\n")
        f.write(" SMART RETAIL GHATTAN\n")

# ================= RIWAYAT TRANSAKSI =================

def riwayat_transaksi():

    win = tk.Toplevel(root)
    win.title("Riwayat Transaksi")
    win.geometry("750x450")
    win.configure(bg=PUTIH)

    tk.Label(
        win,
        text="RIWAYAT TRANSAKSI SMART RETAIL GHATTAN",
        bg=MERAH,
        fg="white",
        font=("Arial",13,"bold"),
        pady=10
    ).pack(fill="x")

    tree = ttk.Treeview(
        win,
        columns=("ID","Tanggal","Kasir","Total"),
        show="headings",
        height=15
    )

    for col in ("ID","Tanggal","Kasir","Total"):
        tree.heading(col, text=col)

    tree.column("ID", width=50, anchor="center")
    tree.column("Tanggal", width=180)
    tree.column("Kasir", width=100, anchor="center")
    tree.column("Total", width=120, anchor="center")

    tree.pack(fill="both", expand=True, padx=10, pady=10)

    cur.execute("""
        SELECT id, tanggal, kasir, total
        FROM transaksi
        ORDER BY id DESC
    """)

    for row in cur.fetchall():
        tree.insert("", tk.END, values=row)

# ================= LAPORAN PENJUALAN =================

def laporan_penjualan():

    win = tk.Toplevel(root)
    win.title("Laporan Penjualan")
    win.geometry("450x350")
    win.configure(bg=PUTIH)

    tk.Label(
        win,
        text="LAPORAN PENJUALAN",
        bg=MERAH,
        fg="white",
        font=("Arial",13,"bold"),
        pady=10
    ).pack(fill="x")

    cur.execute("SELECT COUNT(*) FROM transaksi")
    jumlah = cur.fetchone()[0]

    cur.execute("SELECT SUM(total) FROM transaksi")
    total = cur.fetchone()[0]

    if total is None:
        total = 0

    cur.execute("""
        SELECT nama, SUM(jumlah)
        FROM detail_transaksi
        GROUP BY nama
        ORDER BY SUM(jumlah) DESC
        LIMIT 1
    """)

    produk = cur.fetchone()

    tk.Label(
        win,
        text=f"Jumlah Transaksi : {jumlah}",
        bg=PUTIH,
        font=("Arial",11)
    ).pack(anchor="w", padx=20, pady=8)

    tk.Label(
        win,
        text=f"Total Penjualan : Rp{total:,}",
        bg=PUTIH,
        font=("Arial",11)
    ).pack(anchor="w", padx=20, pady=8)

    if produk:
        tk.Label(
            win,
            text=f"Produk Terlaris : {produk[0]} ({produk[1]} terjual)",
            bg=PUTIH,
            fg="green",
            font=("Arial",11,"bold")
        ).pack(anchor="w", padx=20, pady=8)

# ================= GRAFIK PENJUALAN =================

def grafik_penjualan():

    cur.execute("""
        SELECT nama, SUM(jumlah)
        FROM detail_transaksi
        GROUP BY nama
    """)

    data = cur.fetchall()

    if not data:
        messagebox.showwarning(
            "Grafik",
            "Belum ada transaksi."
        )
        return

    nama = [d[0] for d in data]
    jumlah = [d[1] for d in data]

    plt.figure(figsize=(7,4))
    plt.bar(nama, jumlah, color="#C62828")
    plt.title("Grafik Penjualan SMART RETAIL GHATTAN")
    plt.xlabel("Produk")
    plt.ylabel("Jumlah Terjual")
    plt.xticks(rotation=20)
    plt.tight_layout()
    plt.show()