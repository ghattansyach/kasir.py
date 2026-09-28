import sqlite3
from datetime import datetime


db = sqlite3.connect("smart_retail.db")
cur = db.cursor()

print("-" * 30)
print("        SMART RETAIL")
print("   TOKO KELONTONG GHATTAN")
print("-" * 30)

cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT,
    role TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS produk (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama TEXT,
    harga INTEGER,
    stok INTEGER
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS transaksi (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tanggal TEXT,
    username TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS detail_transaksi (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_transaksi INTEGER,
    id_produk INTEGER,
    jumlah INTEGER,
    subtotal INTEGER
)
""")

cur.execute("SELECT * FROM users WHERE username = ?", ("admin",))

if cur.fetchone() is None:
    cur.execute(
        "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
        ("admin", "456", "admin")
    )

cur.execute("SELECT * FROM users WHERE username = ?", ("kasir",))

if cur.fetchone() is None:
    cur.execute(
        "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
        ("kasir", "123", "kasir")
    )

produk_awal = [
    ("Beras 5 Kg", 75000, 20),
    ("Gula 1 Kg", 18000, 30),
    ("Minyak Goreng", 20000, 25),
    ("Mie Instan", 3500, 50)
]

for nama, harga, stok in produk_awal:
    cur.execute(
        "SELECT id FROM produk WHERE nama = ?",
        (nama,)
    )

    if cur.fetchone() is None:
        cur.execute(
            "INSERT INTO produk (nama, harga, stok) VALUES (?, ?, ?)",
            (nama, harga, stok)
        )

db.commit()


def input_angka(pesan, minimal=None):

    while True:

        try:
            angka = int(input(pesan))

            if minimal is not None and angka < minimal:
                print("Nilai terlalu kecil.")
                continue

            return angka

        except ValueError:
            print("Masukkan angka yang benar.")


def login():

    print("\n" + "-" * 30)
    print("           LOGIN")
    print("   TOKO KELONTONG GHATTAN")
    print("-" * 30)

    username = input("Username : ")
    password = input("Password : ")

    cur.execute(
        "SELECT username, role FROM users WHERE username = ? AND password = ?",
        (username, password)
    )

    user = cur.fetchone()

    if user:
        print("-" * 30)
        print("Login berhasil.")
        return user

    print("Username atau password salah.")
    return None


def lihat_produk():

    cur.execute(
        "SELECT id, nama, harga, stok FROM produk ORDER BY id"
    )

    data = cur.fetchall()

    print("\n" + "-" * 30)
    print("       DAFTAR PRODUK")
    print("   TOKO KELONTONG GHATTAN")
    print("-" * 30)

    if not data:
        print("Belum ada produk.")
        return

    for id_produk, nama, harga, stok in data:
        print(
            f"ID: {id_produk} | {nama} | Rp{harga} | Stok: {stok}"
        )


def tambah_produk():

    print("\n" + "-" * 30)
    print("       TAMBAH PRODUK")
    print("-" * 30)

    nama = input("Nama produk : ")
    harga = input_angka("Harga       : ", 0)
    stok = input_angka("Stok        : ", 0)

    cur.execute(
        "INSERT INTO produk (nama, harga, stok) VALUES (?, ?, ?)",
        (nama, harga, stok)
    )

    db.commit()

    print("Produk berhasil ditambahkan.")


def edit_produk():

    lihat_produk()

    id_produk = input_angka(
        "\nMasukkan ID produk : ",
        1
    )

    cur.execute(
        "SELECT * FROM produk WHERE id = ?",
        (id_produk,)
    )

    produk = cur.fetchone()

    if produk is None:
        print("Produk tidak ditemukan.")
        return

    nama = input("Nama baru  : ")
    harga = input_angka("Harga baru : ", 0)
    stok = input_angka("Stok baru  : ", 0)

    cur.execute(
        """
        UPDATE produk
        SET nama = ?, harga = ?, stok = ?
        WHERE id = ?
        """,
        (nama, harga, stok, id_produk)
    )

    db.commit()

    print("Produk berhasil diubah.")


def hapus_produk():

    lihat_produk()

    id_produk = input_angka(
        "\nMasukkan ID produk : ",
        1
    )

    cur.execute(
        "SELECT nama FROM produk WHERE id = ?",
        (id_produk,)
    )

    produk = cur.fetchone()

    if produk is None:
        print("Produk tidak ditemukan.")
        return

    yakin = input(
        f"Hapus {produk[0]}? (y/n): "
    )

    if yakin.lower() == "y":

        cur.execute(
            "DELETE FROM produk WHERE id = ?",
            (id_produk,)
        )

        db.commit()

        print("Produk berhasil dihapus.")

    else:
        print("Penghapusan dibatalkan.")


def cari_produk():

    nama = input(
        "\nMasukkan nama produk : "
    )

    cur.execute(
        """
        SELECT id, nama, harga, stok
        FROM produk
        WHERE nama LIKE ?
        """,
        (f"%{nama}%",)
    )

    data = cur.fetchall()

    print("\n" + "-" * 30)
    print("       HASIL PENCARIAN")
    print("-" * 30)

    if not data:
        print("Produk tidak ditemukan.")
        return

    for id_produk, nama, harga, stok in data:
        print(
            f"ID: {id_produk} | "
            f"{nama} | Rp{harga} | Stok: {stok}"
        )


def transaksi(username):

    keranjang = []
    total = 0

    while True:

        lihat_produk()

        id_produk = input_angka(
            "\nMasukkan ID produk (0 selesai): ",
            0
        )

        if id_produk == 0:
            break

        cur.execute(
            """
            SELECT id, nama, harga, stok
            FROM produk
            WHERE id = ?
            """,
            (id_produk,)
        )

        produk = cur.fetchone()

        if produk is None:
            print("Produk tidak ditemukan.")
            continue

        jumlah = input_angka(
            "Jumlah beli : ",
            1
        )

        if jumlah > produk[3]:
            print("Stok tidak cukup.")
            continue

        subtotal = produk[2] * jumlah

        keranjang.append(
            [
                produk[0],
                produk[1],
                jumlah,
                subtotal
            ]
        )

        total += subtotal

        print("Produk berhasil ditambahkan.")

    if not keranjang:
        print("Tidak ada transaksi.")
        return

    print("\n" + "-" * 30)
    print("          BELANJA")
    print("-" * 30)

    for item in keranjang:
        print(
            f"{item[1]} x {item[2]} = Rp{item[3]}"
        )

    print("-" * 30)
    print(f"Total = Rp{total}")

    while True:

        bayar = input_angka(
            "Bayar = Rp",
            0
        )

        if bayar < total:
            print("Uang kurang.")

        else:
            break

    kembali = bayar - total

    print(f"Kembalian = Rp{kembali}")

    tanggal = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    cur.execute(
        """
        INSERT INTO transaksi
        (tanggal, username)
        VALUES (?, ?)
        """,
        (tanggal, username)
    )

    id_transaksi = cur.lastrowid

    for item in keranjang:

        cur.execute(
            """
            INSERT INTO detail_transaksi
            (id_transaksi, id_produk, jumlah, subtotal)
            VALUES (?, ?, ?, ?)
            """,
            (
                id_transaksi,
                item[0],
                item[2],
                item[3]
            )
        )

        cur.execute(
            """
            UPDATE produk
            SET stok = stok - ?
            WHERE id = ?
            """,
            (item[2], item[0])
        )

    db.commit()

    print("Transaksi berhasil.")


def riwayat():

    cur.execute(
        """
        SELECT
            transaksi.id,
            transaksi.tanggal,
            transaksi.username,
            produk.nama,
            detail_transaksi.jumlah,
            detail_transaksi.subtotal
        FROM transaksi
        JOIN detail_transaksi
            ON transaksi.id = detail_transaksi.id_transaksi
        JOIN produk
            ON detail_transaksi.id_produk = produk.id
        ORDER BY transaksi.id DESC
        """
    )

    data = cur.fetchall()

    print("\n" + "-" * 30)
    print("     RIWAYAT TRANSAKSI")
    print("-" * 30)

    if not data:
        print("Belum ada transaksi.")
        return

    for item in data:

        print(f"ID transaksi : {item[0]}")
        print(f"Tanggal      : {item[1]}")
        print(f"Kasir        : {item[2]}")
        print(f"Produk       : {item[3]}")
        print(f"Jumlah       : {item[4]}")
        print(f"Subtotal     : Rp{item[5]}")
        print("-" * 30)


def laporan():

    cur.execute(
        "SELECT COUNT(*) FROM transaksi"
    )

    jumlah_transaksi = cur.fetchone()[0]

    cur.execute(
        "SELECT SUM(subtotal) FROM detail_transaksi"
    )

    total_penjualan = cur.fetchone()[0] or 0

    cur.execute(
        """
        SELECT
            produk.nama,
            SUM(detail_transaksi.jumlah)
        FROM detail_transaksi
        JOIN produk
            ON detail_transaksi.id_produk = produk.id
        GROUP BY produk.id
        ORDER BY SUM(detail_transaksi.jumlah) DESC
        LIMIT 1
        """
    )

    terlaris = cur.fetchone()

    print("\n" + "-" * 30)
    print("     LAPORAN PENJUALAN")
    print("-" * 30)

    print(
        f"Jumlah transaksi : {jumlah_transaksi}"
    )

    print(
        f"Total penjualan  : Rp{total_penjualan}"
    )

    if terlaris:

        print(
            f"Produk terlaris  : "
            f"{terlaris[0]} "
            f"({terlaris[1]} terjual)"
        )

    else:

        print(
            "Produk terlaris  : Belum ada"
        )


def grafik():

    try:
        import matplotlib.pyplot as plt

    except ImportError:

        print("Matplotlib belum terpasang.")
        print(
            "Jalankan: "
            "python -m pip install matplotlib"
        )
        return

    cur.execute(
        """
        SELECT
            produk.nama,
            SUM(detail_transaksi.jumlah)
        FROM detail_transaksi
        JOIN produk
            ON detail_transaksi.id_produk = produk.id
        GROUP BY produk.id
        """
    )

    data = cur.fetchall()

    if not data:
        print("Belum ada data penjualan.")
        return

    nama = [
        item[0]
        for item in data
    ]

    jumlah = [
        item[1]
        for item in data
    ]

    plt.figure(figsize=(8, 5))

    plt.bar(
        nama,
        jumlah
    )

    plt.title(
        "Grafik Penjualan - "
        "Toko Kelontong Ghattan"
    )

    plt.xlabel("Produk")
    plt.ylabel("Jumlah Terjual")

    plt.xticks(
        rotation=30
    )

    plt.tight_layout()

    plt.show()
    plt.close('all')

def menu_admin(username):

    while True:

        print("\n" + "-" * 30)
        print("          MENU ADMIN")
        print("   TOKO KELONTONG GHATTAN")
        print("-" * 30)

        print("1. Lihat produk")
        print("2. Tambah produk")
        print("3. Edit produk")
        print("4. Hapus produk")
        print("5. Cari produk")
        print("6. Riwayat transaksi")
        print("7. Laporan penjualan")
        print("8. Grafik penjualan")
        print("9. Logout")

        print("-" * 30)

        pilih = input(
            "Pilih menu : "
        )

        if pilih == "1":
            lihat_produk()

        elif pilih == "2":
            tambah_produk()

        elif pilih == "3":
            edit_produk()

        elif pilih == "4":
            hapus_produk()

        elif pilih == "5":
            cari_produk()

        elif pilih == "6":
            riwayat()

        elif pilih == "7":
            laporan()

        elif pilih == "8":
            grafik()

        elif pilih == "9":
            print("Logout.")
            break

        else:
            print("Menu tidak tersedia.")


def menu_kasir(username):

    while True:

        print("\n" + "-" * 30)
        print("          MENU KASIR")
        print("   TOKO KELONTONG GHATTAN")
        print("-" * 30)

        print("1. Transaksi")
        print("2. Lihat produk")
        print("3. Cari produk")
        print("4. Logout")

        print("-" * 30)

        pilih = input(
            "Pilih menu : "
        )

        if pilih == "1":
            transaksi(username)

        elif pilih == "2":
            lihat_produk()

        elif pilih == "3":
            cari_produk()

        elif pilih == "4":
            print("Logout.")
            break

        else:
            print("Menu tidak tersedia.")


try:

    while True:

        print("\n" + "-" * 30)
        print("        SMART RETAIL")
        print("   TOKO KELONTONG GHATTAN")
        print("-" * 30)

        print("1. Login")
        print("2. Keluar")

        print("-" * 30)

        pilih = input(
            "Pilih : "
        )

        if pilih == "1":

            user = login()

            if user:

                username, role = user

                if role == "admin":
                    menu_admin(username)

                elif role == "kasir":
                    menu_kasir(username)

        elif pilih == "2":

            print("\nProgram selesai.")
            break

        else:

            print(
                "Menu tidak tersedia."
            )

finally:

    db.close()