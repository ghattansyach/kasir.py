import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
import os

# ==========================
# DATABASE
# ==========================

db = sqlite3.connect("smart_retail.db")
cur = db.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
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
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_transaksi INTEGER,
    nama_produk TEXT,
    jumlah INTEGER,
    subtotal INTEGER
)
""")

db.commit()

# ==========================
# USER LOGIN
# ==========================

users = [
    ("admin", "123", "admin"),
    ("kasir", "456", "kasir")
]

for u in users:
    cur.execute("SELECT * FROM users WHERE username=?", (u[0],))
    if cur.fetchone() is None:
        cur.execute(
            "INSERT INTO users(username,password,role) VALUES(?,?,?)",
            u
        )

db.commit()

# ==========================
# PRODUK AWAL SMART RETAIL GHATTAN
# ==========================

produk_awal = [
    ("Beras Premium 5 Kg",78000,25),
    ("Minyak Goreng 1 Liter",22000,40),
    ("Gula Pasir 1 Kg",19000,35),
    ("Mie Instan",3500,120),
]

for p in produk_awal:
    cur.execute("SELECT * FROM produk WHERE nama=?", (p[0],))
    if cur.fetchone() is None:
        cur.execute(
            "INSERT INTO produk(nama,harga,stok) VALUES(?,?,?)",
            p
        )

db.commit()

# ==========================
# WARNA TEMA
# ==========================

MERAH = "#C62828"
MERAH2 = "#E53935"
PUTIH = "#FFFFFF"
ABU = "#F2F2F2"

# ==========================
# WINDOW LOGIN
# ==========================

root = tk.Tk()
root.title("SMART RETAIL GHATTAN")
root.geometry("450x550")
root.configure(bg=PUTIH)
root.resizable(False,False)

judul = tk.Label(
    root,
    text="SMART RETAIL GHATTAN",
    bg=MERAH,
    fg="white",
    font=("Arial",18,"bold"),
    pady=15
)
judul.pack(fill="x")

tk.Label(
    root,
    text="TOKO KELONTONG",
    bg=PUTIH,
    fg=MERAH,
    font=("Arial",12,"bold")
).pack(pady=15)

frame_login = tk.Frame(root,bg=PUTIH)
frame_login.pack(pady=20)

tk.Label(
    frame_login,
    text="Username",
    bg=PUTIH,
    font=("Arial",11)
).pack(anchor="w")

entry_user = tk.Entry(frame_login,font=("Arial",12),width=28)
entry_user.pack(pady=8)

tk.Label(
    frame_login,
    text="Password",
    bg=PUTIH,
    font=("Arial",11)
).pack(anchor="w")

entry_pass = tk.Entry(frame_login,font=("Arial",12),show="*",width=28)
entry_pass.pack(pady=8)

status_login = tk.Label(
    root,
    text="Silakan Login",
    bg=PUTIH,
    fg="green",
    font=("Arial",10)
)
status_login.pack()

# ==========================
# DASHBOARD ADMIN
# ==========================

def dashboard_admin(username):

    admin = tk.Toplevel()
    admin.title("Dashboard Admin")
    admin.geometry("900x600")
    admin.configure(bg=PUTIH)

    tk.Label(
        admin,
        text=f"ADMIN : {username}",
        bg=MERAH,
        fg="white",
        font=("Arial",15,"bold"),
        pady=12
    ).pack(fill="x")

    tombol = tk.Frame(admin,bg=PUTIH)
    tombol.pack(fill="x",pady=10)

    tree = ttk.Treeview(
        admin,
        columns=("Harga","Stok"),
        show="headings",
        height=18
    )

    tree.heading("Harga",text="Harga")
    tree.heading("Stok",text="Stok")

    tree.column("Harga",width=180)
    tree.column("Stok",width=120)

    tree.pack(fill="both",expand=True,padx=15,pady=10)

    def tampil_produk():
        tree.delete(*tree.get_children())

        cur.execute("SELECT nama,harga,stok FROM produk ORDER BY nama")

        for row in cur.fetchall():
            tree.insert("",tk.END,values=row)

    tampil_produk()

    def tambah_produk():
        win = tk.Toplevel(admin)
        win.title("Tambah Produk")
        win.geometry("350x260")
        win.configure(bg=PUTIH)

        tk.Label(win,text="Nama Produk",bg=PUTIH).pack()
        nama = tk.Entry(win,width=30)
        nama.pack()

        tk.Label(win,text="Harga",bg=PUTIH).pack()
        harga = tk.Entry(win,width=30)
        harga.pack()

        tk.Label(win,text="Stok",bg=PUTIH).pack()
        stok = tk.Entry(win,width=30)
        stok.pack()

        def simpan():
            cur.execute(
                "INSERT INTO produk(nama,harga,stok) VALUES(?,?,?)",
                (
                    nama.get(),
                    int(harga.get()),
                    int(stok.get())
                )
            )

            db.commit()
            tampil_produk()
            messagebox.showinfo("Sukses","Produk berhasil ditambahkan.")
            win.destroy()

        tk.Button(
            win,
            text="SIMPAN",
            bg=MERAH,
            fg="white",
            command=simpan
        ).pack(pady=12)

    tk.Button(
        tombol,
        text="Tambah Produk",
        bg=MERAH2,
        fg="white",
        command=tambah_produk
    ).pack(side="left",padx=5)

    tk.Button(
        tombol,
        text="Refresh",
        bg="green",
        fg="white",
        command=tampil_produk
    ).pack(side="left",padx=5)

# ==========================
# DASHBOARD KASIR
# ==========================

def dashboard_kasir(username):

    kasir = tk.Toplevel()
    kasir.title("Dashboard Kasir")
    kasir.geometry("900x650")
    kasir.configure(bg=PUTIH)

    tk.Label(
        kasir,
        text=f"KASIR : {username}",
        bg=MERAH,
        fg="white",
        font=("Arial",15,"bold"),
        pady=12
    ).pack(fill="x")

    tk.Label(
        kasir,
        text="Menu transaksi akan dibuat di PART 2",
        bg=PUTIH,
        fg=MERAH,
        font=("Arial",12,"bold")
    ).pack(pady=30)

# ==========================
# LOGIN
# ==========================

def login():

    username = entry_user.get()
    password = entry_pass.get()

    cur.execute(
        """
        SELECT username,role
        FROM users
        WHERE username=? AND password=?
        """,
        (username,password)
    )

    user = cur.fetchone()

    if user is None:
        status_login.config(
            text="Username / Password Salah",
            fg="red"
        )
        return

    messagebox.showinfo(
        "Login Berhasil",
        f"Selamat datang {user[0]}"
    )

    if user[1]=="admin":
        dashboard_admin(user[0])

    else:
        dashboard_kasir(user[0])

# ==========================
# TOMBOL LOGIN
# ==========================

tk.Button(
    root,
    text="LOGIN",
    bg=MERAH,
    fg="white",
    font=("Arial",12,"bold"),
    width=22,
    command=login
).pack(pady=20)

tk.Label(
    root,
    text="Username Admin : admin\nPassword : 123\n\nUsername Kasir : kasir\nPassword : 456",
    bg=PUTIH,
    fg="gray",
    font=("Arial",10)
).pack(pady=20)

root.mainloop()

db.close()
# =====================================================
# PART 2 - CRUD PRODUK SMART RETAIL GHATTAN
# Tempel di bawah fungsi dashboard_admin()
# =====================================================

def dashboard_admin(username):

    admin = tk.Toplevel()
    admin.title("SMART RETAIL GHATTAN - ADMIN")
    admin.geometry("1000x620")
    admin.configure(bg=PUTIH)

    tk.Label(
        admin,
        text=f"SMART RETAIL GHATTAN | ADMIN : {username}",
        bg=MERAH,
        fg="white",
        font=("Arial",16,"bold"),
        pady=12
    ).pack(fill="x")

    # ---------------- SEARCH ----------------

    frame_search = tk.Frame(admin, bg=PUTIH)
    frame_search.pack(fill="x", pady=10, padx=15)

    tk.Label(frame_search, text="Cari Produk :", bg=PUTIH,
             font=("Arial",11,"bold")).pack(side="left")

    cari_entry = tk.Entry(frame_search, width=30, font=("Arial",11))
    cari_entry.pack(side="left", padx=10)

    # ---------------- TABEL ----------------

    frame_table = tk.Frame(admin, bg=PUTIH)
    frame_table.pack(fill="both", expand=True, padx=15)

    kolom = ("ID","Nama","Harga","Stok")

    tree = ttk.Treeview(frame_table,
                        columns=kolom,
                        show="headings")

    for k in kolom:
        tree.heading(k, text=k)

    tree.column("ID", width=60, anchor="center")
    tree.column("Nama", width=380)
    tree.column("Harga", width=180, anchor="center")
    tree.column("Stok", width=120, anchor="center")

    scroll = ttk.Scrollbar(frame_table,
                           orient="vertical",
                           command=tree.yview)

    tree.configure(yscrollcommand=scroll.set)

    tree.pack(side="left", fill="both", expand=True)
    scroll.pack(side="right", fill="y")

    # ---------------- TAMPIL DATA ----------------

    def tampil_produk():

        tree.delete(*tree.get_children())

        cur.execute("""
            SELECT id,nama,harga,stok
            FROM produk
            ORDER BY id
        """)

        data = cur.fetchall()

        for row in data:
            tree.insert("", tk.END, values=row)

    tampil_produk()

    # ---------------- CARI ----------------

    def cari_produk():

        tree.delete(*tree.get_children())

        keyword = "%" + cari_entry.get() + "%"

        cur.execute("""
            SELECT id,nama,harga,stok
            FROM produk
            WHERE nama LIKE ?
        """,(keyword,))

        for row in cur.fetchall():
            tree.insert("", tk.END, values=row)

    tk.Button(frame_search,
              text="Cari",
              bg=MERAH2,
              fg="white",
              command=cari_produk).pack(side="left", padx=5)

    tk.Button(frame_search,
              text="Refresh",
              bg="green",
              fg="white",
              command=tampil_produk).pack(side="left")

    # ---------------- FORM CRUD ----------------

    frame_form = tk.LabelFrame(admin,
                               text="Kelola Produk",
                               bg=PUTIH,
                               padx=10,
                               pady=10)

    frame_form.pack(fill="x", padx=15, pady=12)

    tk.Label(frame_form,text="Nama Produk",bg=PUTIH).grid(row=0,column=0)
    nama = tk.Entry(frame_form,width=35)
    nama.grid(row=0,column=1,padx=5,pady=5)

    tk.Label(frame_form,text="Harga",bg=PUTIH).grid(row=1,column=0)
    harga = tk.Entry(frame_form,width=35)
    harga.grid(row=1,column=1,padx=5,pady=5)

    tk.Label(frame_form,text="Stok",bg=PUTIH).grid(row=2,column=0)
    stok = tk.Entry(frame_form,width=35)
    stok.grid(row=2,column=1,padx=5,pady=5)

    # ---------------- PILIH DATA ----------------

    id_produk = tk.StringVar()

    def pilih_data(event):

        data = tree.focus()

        if not data:
            return

        isi = tree.item(data,"values")

        id_produk.set(isi[0])

        nama.delete(0,tk.END)
        harga.delete(0,tk.END)
        stok.delete(0,tk.END)

        nama.insert(0,isi[1])
        harga.insert(0,isi[2])
        stok.insert(0,isi[3])

    tree.bind("<<TreeviewSelect>>", pilih_data)

    # ---------------- TAMBAH ----------------

    def tambah_produk():

        if nama.get()=="":
            messagebox.showwarning("Peringatan","Nama produk kosong.")
            return

        cur.execute("""
            INSERT INTO produk(nama,harga,stok)
            VALUES(?,?,?)
        """,
        (
            nama.get(),
            int(harga.get()),
            int(stok.get())
        ))

        db.commit()

        tampil_produk()

        messagebox.showinfo("Sukses","Produk berhasil ditambahkan.")

    # ---------------- EDIT ----------------

    def edit_produk():

        if id_produk.get()=="":
            messagebox.showwarning("Pilih Produk","Pilih produk terlebih dahulu.")
            return

        cur.execute("""
            UPDATE produk
            SET nama=?,
                harga=?,
                stok=?
            WHERE id=?
        """,
        (
            nama.get(),
            int(harga.get()),
            int(stok.get()),
            id_produk.get()
        ))

        db.commit()

        tampil_produk()

        messagebox.showinfo("Sukses","Produk berhasil diubah.")

    # ---------------- HAPUS ----------------

    def hapus_produk():

        if id_produk.get()=="":
            messagebox.showwarning("Pilih Produk","Pilih produk terlebih dahulu.")
            return

        jawab = messagebox.askyesno(
            "Konfirmasi",
            "Yakin ingin menghapus produk?"
        )

        if jawab:

            cur.execute("""
                DELETE FROM produk
                WHERE id=?
            """,(id_produk.get(),))

            db.commit()

            tampil_produk()

            nama.delete(0,tk.END)
            harga.delete(0,tk.END)
            stok.delete(0,tk.END)

            id_produk.set("")

            messagebox.showinfo("Sukses","Produk berhasil dihapus.")

    # ---------------- TOMBOL ----------------

    frame_btn = tk.Frame(frame_form,bg=PUTIH)
    frame_btn.grid(row=3,column=0,columnspan=2,pady=10)

    tk.Button(frame_btn,
              text="Tambah",
              bg=MERAH2,
              fg="white",
              width=12,
              command=tambah_produk).pack(side="left",padx=5)

    tk.Button(frame_btn,
              text="Edit",
              bg="#FB8C00",
              fg="white",
              width=12,
              command=edit_produk).pack(side="left",padx=5)

    tk.Button(frame_btn,
              text="Hapus",
              bg="#616161",
              fg="white",
              width=12,
              command=hapus_produk).pack(side="left",padx=5)

    tk.Button(frame_btn,
              text="Logout",
              bg="black",
              fg="white",
              width=12,
              command=admin.destroy).pack(side="left",padx=5)
    # =====================================================
# PART 3 - DASHBOARD KASIR + TRANSAKSI
# Ganti fungsi dashboard_kasir() yang lama dengan ini.
# =====================================================

def dashboard_kasir(username):

    kasir = tk.Toplevel()
    kasir.title("SMART RETAIL GHATTAN - KASIR")
    kasir.geometry("1100x650")
    kasir.configure(bg=PUTIH)

    tk.Label(
        kasir,
        text=f"SMART RETAIL GHATTAN | KASIR : {username}",
        bg=MERAH,
        fg="white",
        font=("Arial",16,"bold"),
        pady=10
    ).pack(fill="x")

    # ================= DAFTAR PRODUK =================

    frame_kiri = tk.Frame(kasir,bg=PUTIH)
    frame_kiri.pack(side="left",fill="both",expand=True,padx=10,pady=10)

    tk.Label(frame_kiri,text="DAFTAR PRODUK",
             bg=PUTIH,fg=MERAH,font=("Arial",12,"bold")).pack()

    kolom = ("ID","Nama","Harga","Stok")

    tree = ttk.Treeview(frame_kiri,columns=kolom,show="headings",height=16)

    for k in kolom:
        tree.heading(k,text=k)

    tree.column("ID",width=50,anchor="center")
    tree.column("Nama",width=220)
    tree.column("Harga",width=100,anchor="center")
    tree.column("Stok",width=70,anchor="center")

    tree.pack(fill="both",expand=True)

    def tampil_produk():
        tree.delete(*tree.get_children())
        cur.execute("SELECT id,nama,harga,stok FROM produk ORDER BY nama")
        for row in cur.fetchall():
            tree.insert("",tk.END,values=row)

    tampil_produk()

    # ================= KERANJANG =================

    frame_kanan = tk.Frame(kasir,bg=PUTIH)
    frame_kanan.pack(side="right",fill="y",padx=10,pady=10)

    tk.Label(frame_kanan,text="KERANJANG BELANJA",
             bg=PUTIH,fg=MERAH,font=("Arial",12,"bold")).pack()

    keranjang = ttk.Treeview(
        frame_kanan,
        columns=("Produk","Jumlah","Subtotal"),
        show="headings",
        height=12
    )

    keranjang.heading("Produk",text="Produk")
    keranjang.heading("Jumlah",text="Jumlah")
    keranjang.heading("Subtotal",text="Subtotal")

    keranjang.column("Produk",width=170)
    keranjang.column("Jumlah",width=60,anchor="center")
    keranjang.column("Subtotal",width=110,anchor="center")

    keranjang.pack()

    data_belanja = []
    total_belanja = tk.IntVar(value=0)

    # ================= PILIH PRODUK =================

    tk.Label(frame_kanan,text="Jumlah",bg=PUTIH).pack(pady=(10,0))
    entry_jumlah = tk.Entry(frame_kanan,width=10)
    entry_jumlah.pack()

    def tambah_keranjang():

        pilih = tree.focus()

        if not pilih:
            messagebox.showwarning("Pilih Produk","Pilih produk terlebih dahulu.")
            return

        data = tree.item(pilih,"values")

        id_produk = int(data[0])
        nama = data[1]
        harga = int(data[2])
        stok = int(data[3])

        if entry_jumlah.get()=="":
            return

        jumlah = int(entry_jumlah.get())

        if jumlah > stok:
            messagebox.showerror("Stok","Stok tidak mencukupi.")
            return

        subtotal = harga * jumlah

        data_belanja.append({
            "id":id_produk,
            "nama":nama,
            "harga":harga,
            "jumlah":jumlah,
            "subtotal":subtotal
        })

        keranjang.insert(
            "",
            tk.END,
            values=(nama,jumlah,f"Rp{subtotal:,}")
        )

        total_belanja.set(total_belanja.get()+subtotal)
        lbl_total.config(text=f"Rp {total_belanja.get():,}")

        entry_jumlah.delete(0,tk.END)

    tk.Button(
        frame_kanan,
        text="Tambah ke Keranjang",
        bg=MERAH2,
        fg="white",
        command=tambah_keranjang
    ).pack(pady=8)

    # ================= TOTAL =================

    tk.Label(frame_kanan,text="TOTAL BELANJA",bg=PUTIH,
             font=("Arial",11,"bold")).pack()

    lbl_total = tk.Label(
        frame_kanan,
        text="Rp 0",
        bg=PUTIH,
        fg=MERAH,
        font=("Arial",15,"bold")
    )

    lbl_total.pack(pady=5)

    # ================= BAYAR =================

    tk.Label(frame_kanan,text="Bayar (Rp)",bg=PUTIH).pack()

    entry_bayar = tk.Entry(frame_kanan,width=20)
    entry_bayar.pack()

    lbl_kembali = tk.Label(
        frame_kanan,
        text="Kembalian : Rp 0",
        bg=PUTIH,
        fg="green",
        font=("Arial",11,"bold")
    )

    lbl_kembali.pack(pady=8)

    # ================= HITUNG KEMBALIAN =================

    def hitung_kembalian():

        if entry_bayar.get()=="":
            return

        bayar = int(entry_bayar.get())

        if bayar < total_belanja.get():
            messagebox.showerror("Pembayaran","Uang pelanggan kurang.")
            return

        kembali = bayar - total_belanja.get()

        lbl_kembali.config(
            text=f"Kembalian : Rp {kembali:,}"
        )

    tk.Button(
        frame_kanan,
        text="Hitung Kembalian",
        bg="green",
        fg="white",
        command=hitung_kembalian
    ).pack(pady=5)

    # ================= SIMPAN TRANSAKSI =================

    def simpan_transaksi():

        if len(data_belanja)==0:
            messagebox.showwarning("Keranjang","Belum ada barang.")
            return

        if entry_bayar.get()=="":
            messagebox.showwarning("Pembayaran","Masukkan uang bayar.")
            return

        bayar = int(entry_bayar.get())

        if bayar < total_belanja.get():
            messagebox.showerror("Pembayaran","Uang tidak cukup.")
            return

        kembali = bayar - total_belanja.get()

        tanggal = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

        cur.execute("""
            INSERT INTO transaksi
            (tanggal,kasir,total,bayar,kembali)
            VALUES(?,?,?,?,?)
        """,
        (
            tanggal,
            username,
            total_belanja.get(),
            bayar,
            kembali
        ))

        id_transaksi = cur.lastrowid

        # Detail transaksi + update stok

        for item in data_belanja:

            cur.execute("""
                INSERT INTO detail_transaksi
                (id_transaksi,nama_produk,jumlah,subtotal)
                VALUES(?,?,?,?)
            """,
            (
                id_transaksi,
                item["nama"],
                item["jumlah"],
                item["subtotal"]
            ))

            cur.execute("""
                UPDATE produk
                SET stok = stok - ?
                WHERE id = ?
            """,
            (
                item["jumlah"],
                item["id"]
            ))

        db.commit()

        messagebox.showinfo(
            "Berhasil",
            f"Transaksi berhasil!\nKembalian Rp {kembali:,}"
        )

        # Bersihkan keranjang

        keranjang.delete(*keranjang.get_children())
        data_belanja.clear()

        total_belanja.set(0)
        lbl_total.config(text="Rp 0")
        lbl_kembali.config(text="Kembalian : Rp 0")

        entry_bayar.delete(0,tk.END)

        tampil_produk()

    tk.Button(
        frame_kanan,
        text="Simpan Transaksi",
        bg=MERAH,
        fg="white",
        width=22,
        command=simpan_transaksi
    ).pack(pady=12)

    tk.Button(
        frame_kanan,
        text="Logout",
        bg="black",
        fg="white",
        width=22,
        command=kasir.destroy
    ).pack()
    # =====================================================
# PART 4 - STRUK, RIWAYAT, LAPORAN, GRAFIK
# =====================================================

import os
import matplotlib.pyplot as plt

# ===========================
# CETAK STRUK
# ===========================

def cetak_struk(id_transaksi):

    if not os.path.exists("receipt"):
        os.makedirs("receipt")

    cur.execute("""
        SELECT tanggal,kasir,total,bayar,kembali
        FROM transaksi
        WHERE id=?
    """,(id_transaksi,))

    transaksi = cur.fetchone()

    cur.execute("""
        SELECT nama_produk,jumlah,subtotal
        FROM detail_transaksi
        WHERE id_transaksi=?
    """,(id_transaksi,))

    barang = cur.fetchall()

    file = open("receipt/struk.txt","w",encoding="utf-8")

    file.write("="*40+"\n")
    file.write("       SMART RETAIL GHATTAN\n")
    file.write("     TOKO KELONTONG MODERN\n")
    file.write("="*40+"\n\n")

    file.write(f"Tanggal : {transaksi[0]}\n")
    file.write(f"Kasir   : {transaksi[1]}\n")
    file.write("-"*40+"\n")

    for item in barang:
        file.write(f"{item[0]}\n")
        file.write(f"{item[1]} x Rp{item[2]//item[1]:,}")
        file.write(f" = Rp{item[2]:,}\n\n")

    file.write("-"*40+"\n")
    file.write(f"TOTAL      : Rp{transaksi[2]:,}\n")
    file.write(f"BAYAR      : Rp{transaksi[3]:,}\n")
    file.write(f"KEMBALIAN  : Rp{transaksi[4]:,}\n")
    file.write("="*40+"\n")
    file.write(" TERIMA KASIH SUDAH BERBELANJA\n")
    file.write("      SMART RETAIL GHATTAN\n")
    file.write("="*40)

    file.close()

    messagebox.showinfo(
        "Struk Berhasil",
        "Struk berhasil disimpan di folder receipt/struk.txt"
    )

# ===========================
# RIWAYAT TRANSAKSI
# ===========================

def riwayat_transaksi():

    win = tk.Toplevel()
    win.title("Riwayat Transaksi")
    win.geometry("900x500")
    win.configure(bg=PUTIH)

    tk.Label(
        win,
        text="RIWAYAT TRANSAKSI SMART RETAIL GHATTAN",
        bg=MERAH,
        fg="white",
        font=("Arial",15,"bold"),
        pady=10
    ).pack(fill="x")

    kolom = ("ID","Tanggal","Kasir","Total")

    tree = ttk.Treeview(
        win,
        columns=kolom,
        show="headings"
    )

    for k in kolom:
        tree.heading(k,text=k)

    tree.column("ID",width=60,anchor="center")
    tree.column("Tanggal",width=180)
    tree.column("Kasir",width=150,anchor="center")
    tree.column("Total",width=150,anchor="center")

    tree.pack(fill="both",expand=True,padx=15,pady=15)

    cur.execute("""
        SELECT id,tanggal,kasir,total
        FROM transaksi
        ORDER BY id DESC
    """)

    for row in cur.fetchall():
        tree.insert("",tk.END,values=row)

    def lihat_detail():

        pilih = tree.focus()

        if not pilih:
            return

        data = tree.item(pilih,"values")
        id_transaksi = data[0]

        detail = tk.Toplevel(win)
        detail.title("Detail Transaksi")
        detail.geometry("450x450")

        tk.Label(
            detail,
            text=f"Transaksi #{id_transaksi}",
            bg=MERAH,
            fg="white",
            font=("Arial",13,"bold"),
            pady=10
        ).pack(fill="x")

        cur.execute("""
            SELECT nama_produk,jumlah,subtotal
            FROM detail_transaksi
            WHERE id_transaksi=?
        """,(id_transaksi,))

        total = 0

        for item in cur.fetchall():

            tk.Label(
                detail,
                text=f"{item[0]} ({item[1]} pcs)  Rp{item[2]:,}",
                anchor="w"
            ).pack(fill="x",padx=15,pady=3)

            total += item[2]

        tk.Label(
            detail,
            text=f"TOTAL : Rp{total:,}",
            fg=MERAH,
            font=("Arial",12,"bold")
        ).pack(pady=15)

        tk.Button(
            detail,
            text="Cetak Struk",
            bg=MERAH,
            fg="white",
            command=lambda:cetak_struk(id_transaksi)
        ).pack()

    tk.Button(
        win,
        text="Lihat Detail / Cetak Struk",
        bg=MERAH,
        fg="white",
        command=lihat_detail
    ).pack(pady=10)

# ===========================
# LAPORAN PENJUALAN
# ===========================

def laporan_penjualan():

    win = tk.Toplevel()
    win.title("Laporan Penjualan")
    win.geometry("550x420")
    win.configure(bg=PUTIH)

    tk.Label(
        win,
        text="LAPORAN PENJUALAN",
        bg=MERAH,
        fg="white",
        font=("Arial",15,"bold"),
        pady=10
    ).pack(fill="x")

    cur.execute("SELECT COUNT(*) FROM transaksi")
    jumlah = cur.fetchone()[0]

    cur.execute("SELECT SUM(total) FROM transaksi")
    total = cur.fetchone()[0]

    if total is None:
        total = 0

    cur.execute("""
        SELECT nama_produk,
               SUM(jumlah)
        FROM detail_transaksi
        GROUP BY nama_produk
        ORDER BY SUM(jumlah) DESC
        LIMIT 1
    """)

    terlaris = cur.fetchone()

    isi = tk.Frame(win,bg=PUTIH)
    isi.pack(pady=25)

    tk.Label(
        isi,
        text=f"Jumlah Transaksi : {jumlah}",
        bg=PUTIH,
        font=("Arial",12)
    ).pack(anchor="w",pady=6)

    tk.Label(
        isi,
        text=f"Total Penjualan : Rp{total:,}",
        bg=PUTIH,
        font=("Arial",12)
    ).pack(anchor="w",pady=6)

    if terlaris:
        tk.Label(
            isi,
            text=f"Produk Terlaris : {terlaris[0]} ({terlaris[1]} Terjual)",
            bg=PUTIH,
            fg="green",
            font=("Arial",12,"bold")
        ).pack(anchor="w",pady=6)
    else:
        tk.Label(
            isi,
            text="Belum ada transaksi.",
            bg=PUTIH
        ).pack(anchor="w")

# ===========================
# GRAFIK PENJUALAN
# ===========================

def grafik_penjualan():

    cur.execute("""
        SELECT nama_produk,
               SUM(jumlah)
        FROM detail_transaksi
        GROUP BY nama_produk
    """)

    data = cur.fetchall()

    if len(data)==0:
        messagebox.showwarning(
            "Grafik",
            "Belum ada transaksi."
        )
        return

    nama = [i[0] for i in data]
    jumlah = [i[1] for i in data]

    plt.figure(figsize=(8,5))

    plt.bar(nama,jumlah,color="#C62828")

    plt.title("Grafik Penjualan SMART RETAIL GHATTAN")
    plt.xlabel("Produk")
    plt.ylabel("Jumlah Terjual")

    plt.xticks(rotation=25)

    plt.tight_layout()
    plt.show()

# ===========================
# TAMBAHKAN MENU ADMIN
# ===========================

# Tambahkan tombol ini DI DALAM dashboard_admin()
#
# tk.Button(frame_btn,
#           text="Riwayat",
#           bg="#1976D2",
#           fg="white",
#           width=12,
#           command=riwayat_transaksi).pack(side="left",padx=5)
#
# tk.Button(frame_btn,
#           text="Laporan",
#           bg="green",
#           fg="white",
#           width=12,
#           command=laporan_penjualan).pack(side="left",padx=5)
#
# tk.Button(frame_btn,
#           text="Grafik",
#           bg="#8E24AA",
#           fg="white",
#           width=12,
#           command=grafik_penjualan).pack(side="left",padx=5)

# ===========================
# UBAH simpan_transaksi()
# ===========================

# Di akhir fungsi simpan_transaksi() pada PART 3,
# setelah db.commit(), tambahkan:

# cetak_struk(id_transaksi)