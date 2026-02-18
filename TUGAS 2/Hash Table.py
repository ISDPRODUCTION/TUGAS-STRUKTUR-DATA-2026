"""
Hash Table Premium+ (Linear Probing) — matplotlib + keyboard controls (Windows CMD safe)

Controls:
  SPACE : pause/resume
  RIGHT : step forward (when paused)
  LEFT  : step backward (when paused)
  R     : restart
  ESC/Q : quit

Run:
  python hash_table_premium_keyboard.py
Options:
  python hash_table_premium_keyboard.py --size 12 --nkeys 11
  python hash_table_premium_keyboard.py --save gif

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  PENJELASAN UMUM — ANALOGI PERPUSTAKAAN 📚
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Hash Table  = Rak-rak buku di perpustakaan, bernomor 0 sampai size-1
  Key (k0,k1) = Judul setiap buku yang ingin disimpan
  Hash Func   = Petugas perpustakaan yang menentukan nomor rak tujuan
  Collision   = Kondisi di mana rak tujuan sudah terisi buku lain
  Linear Probe= Petugas geser satu per satu cari rak kosong berikutnya
  Load Factor = Seberapa penuh rak perpustakaan (0.0=kosong, 1.0=penuh)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import argparse
import random
import numpy as np

import matplotlib
matplotlib.use("TkAgg")  # CMD Windows GUI backend

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


def plan_inserts(keys, size=20):
    # ── ANALOGI ───────────────────────────────────────────────────────────────
    # Fungsi ini mensimulasikan antrean semua buku yang akan disimpan ke rak.
    # Setiap langkah kecil (cek rak, bentrok, geser) direkam sebagai "frame"
    # agar bisa ditampilkan satu per satu dalam animasi.
    # ─────────────────────────────────────────────────────────────────────────

    # Membuat deretan rak perpustakaan yang masih kosong semua
    # ANALOGI: Perpustakaan baru dibuka, semua rak masih None (belum ada buku)
    table = [None] * size

    frame_data = []   # Rekaman setiap langkah untuk animasi
    load_factors = [] # Riwayat tingkat kepenuhan rak

    for step, key in enumerate(keys, 1):
        # ── HASH FUNCTION ─────────────────────────────────────────────────────
        # Petugas perpustakaan melihat judul buku (key), lalu menghitung
        # nomor rak tujuan menggunakan rumus: hash(key) % size
        #
        # Contoh:
        #   key = "k3", size = 20
        #   hash("k3") = 2956368648 (angka besar dari Python)
        #   2956368648 % 20 = 8  → buku "k3" diarahkan ke rak nomor 8
        # ─────────────────────────────────────────────────────────────────────
        start = hash(key) % size  # Rak tujuan awal berdasarkan judul buku
        idx = start               # idx = rak yang sedang dicek saat ini
        probes = 0                # Berapa kali petugas harus geser ke rak lain

        def snap(phase, placed=False):
            # Merekam kondisi rak saat ini sebagai satu "frame" animasi
            # ANALOGI: Seperti foto snapshot kondisi perpustakaan di setiap momen
            frame_data.append({
                "phase": phase,       # Fase: start/collision/probe/place/pause
                "step": step,         # Buku ke berapa yang sedang diproses
                "key": key,           # Judul buku
                "start": start,       # Rak tujuan awal dari hash function
                "idx": idx,           # Rak yang sedang dicek sekarang
                "probes": probes,     # Berapa kali sudah geser
                "table": list(table), # Foto kondisi rak saat ini
                "placed": placed      # Apakah buku sudah berhasil disimpan?
            })

        # Fase "start": buku baru datang, menuju rak tujuan pertama
        snap("start", placed=False)

        # ── LINEAR PROBING ────────────────────────────────────────────────────
        # Selama rak yang dituju masih terisi, petugas terus geser ke kanan.
        #
        # ANALOGI:
        #   Buku datang ke rak 8, tapi rak 8 sudah ada buku lain → BENTROK
        #   Petugas: "Coba rak 9..." → rak 9 juga penuh
        #   Petugas: "Coba rak 10..." → rak 10 kosong → SIMPAN di sini!
        #
        # (idx + 1) % size memastikan pencarian memutar kembali ke rak 0
        # setelah mencapai rak terakhir (seperti rak yang tersusun melingkar)
        # ─────────────────────────────────────────────────────────────────────
        while table[idx] is not None:
            # Fase "collision": rak ini sudah terisi buku lain, terjadi bentrok
            snap("collision", placed=False)

            probes += 1              # Hitung satu kali geser
            idx = (idx + 1) % size   # Geser ke rak berikutnya (memutar)

            # Fase "probe": sedang mengecek rak berikutnya
            snap("probe", placed=False)

        # ── PLACE ─────────────────────────────────────────────────────────────
        # Rak kosong ditemukan! Buku disimpan di sini.
        # ANALOGI: Petugas menemukan rak kosong dan meletakkan buku di sana.
        # ─────────────────────────────────────────────────────────────────────
        table[idx] = key  # Buku disimpan di rak idx
        snap("place", placed=True)

        # ── LOAD FACTOR ───────────────────────────────────────────────────────
        # Hitung tingkat kepenuhan rak setelah buku ini disimpan.
        #
        # Rumus: jumlah rak terisi / total rak
        # Contoh: 10 buku di perpustakaan dengan 20 rak → load factor = 0.5
        #
        # Semakin tinggi load factor:
        #   < 50%  → Rak masih lega, jarang terjadi bentrok
        #   50-75% → Mulai padat, bentrok mulai sering terjadi
        #   > 75%  → Sangat padat, banyak bentrok, cari rak kosong lama
        # ─────────────────────────────────────────────────────────────────────
        lf = sum(v is not None for v in table) / size
        load_factors.append(lf)

        # Fase "pause": jeda setelah buku berhasil disimpan di rak
        snap("pause", placed=True)

    return frame_data, load_factors


def main():
    # ── ARGUMEN PROGRAM ───────────────────────────────────────────────────────
    # Pengaturan jumlah rak dan jumlah buku bisa diubah dari terminal.
    # Contoh: --size 12 --nkeys 11 → perpustakaan 12 rak, 11 buku
    # ─────────────────────────────────────────────────────────────────────────
    parser = argparse.ArgumentParser()
    parser.add_argument("--size", type=int, default=20)   # Jumlah rak perpustakaan
    parser.add_argument("--nkeys", type=int, default=18)  # Jumlah buku
    parser.add_argument("--seed", type=int, default=42)   # Seed acak (hasil sama tiap run)
    parser.add_argument("--save", choices=["none", "gif"], default="none")
    args = parser.parse_args()

    # Buat daftar "judul buku" secara acak (k0, k1, k2, ...)
    # ANALOGI: Daftar buku yang akan disusun ke rak perpustakaan hari ini
    random.seed(args.seed)
    keys = [f"k{i}" for i in range(args.nkeys)]
    random.shuffle(keys)  # Acak urutan kedatangan buku

    # Jalankan simulasi — rekam semua langkah sebagai frame animasi
    frames, load_factors = plan_inserts(keys, size=args.size)

    # ==== FIGURE LAYOUT ====
    # Membuat tampilan 2 bagian:
    #   Atas  → Visualisasi rak perpustakaan (hash table)
    #   Bawah → Grafik load factor (tingkat kepenuhan rak)
    fig = plt.figure(figsize=(12, 6), constrained_layout=True)
    gs = fig.add_gridspec(2, 1, height_ratios=[3, 1])

    ax_table = fig.add_subplot(gs[0])  # Area visualisasi rak perpustakaan
    ax_lf = fig.add_subplot(gs[1])     # Area grafik load factor

    fig.suptitle("Hash Table Premium+ (Linear Probing) — Keyboard Control", fontsize=14)

    # ---- TABLE GRID ----
    # Menggambar kotak-kotak rak buku di layar
    # Setiap kotak = satu rak di perpustakaan
    n = args.size
    ax_table.set_xlim(-0.5, n - 0.5)
    ax_table.set_ylim(-0.5, 0.5)
    ax_table.set_yticks([])
    ax_table.set_xticks(range(n))
    ax_table.set_xlabel("Index Bucket")

    rects, texts = [], []
    for i in range(n):
        # Gambar kotak rak ke-i
        r = plt.Rectangle((i - 0.5, -0.35), 1.0, 0.7, fill=True, alpha=0.25)
        ax_table.add_patch(r)
        rects.append(r)

        # Teks isi rak (judul buku yang tersimpan di sini, atau kosong)
        t = ax_table.text(i, 0, "", ha="center", va="center", fontsize=9)
        texts.append(t)

    # Info bar: menampilkan detail frame saat ini (judul buku, rak tujuan, dll)
    info = ax_table.text(0.01, 1.08, "", transform=ax_table.transAxes, fontsize=11)

    # Petunjuk kontrol keyboard
    legend = ax_table.text(
        0.01, 1.01,
        "SPACE: pause/resume | ←/→: step (pause) | R: restart | Q/Esc: quit",
        transform=ax_table.transAxes, fontsize=9
    )

    # ---- LOAD FACTOR CHART ----
    # Grafik yang menunjukkan tingkat kepenuhan rak dari waktu ke waktu
    # Semakin ke kanan → semakin banyak buku disimpan
    # Semakin ke atas  → rak semakin penuh
    ax_lf.set_xlim(1, max(2, args.nkeys))
    ax_lf.set_ylim(0, 1.05)
    ax_lf.set_xlabel("Insert ke-")
    ax_lf.set_ylabel("Load Factor")
    ax_lf.grid(True, alpha=0.25)

    lf_line, = ax_lf.plot([], [])                           # Garis grafik load factor
    lf_dot, = ax_lf.plot([], [], marker="o", linestyle="")  # Titik posisi terkini

    # Progress bar kepenuhan rak perpustakaan
    bar_bg = plt.Rectangle((0.02, 0.15), 0.96, 0.2, transform=ax_lf.transAxes, alpha=0.15)
    bar_fg = plt.Rectangle((0.02, 0.15), 0.00, 0.2, transform=ax_lf.transAxes, alpha=0.35)
    ax_lf.add_patch(bar_bg)  # Background bar (abu-abu)
    ax_lf.add_patch(bar_fg)  # Foreground bar (berubah sesuai load factor)
    lf_text = ax_lf.text(0.02, 0.45, "", transform=ax_lf.transAxes, fontsize=10)

    # ==== PLAYER STATE ====
    # State ini mengontrol animasi — seperti remote control untuk video
    state = {
        "i": 0,          # Frame yang sedang ditampilkan sekarang
        "paused": False  # True = animasi berhenti, False = berjalan
    }

    def render(frame):
        # ── RENDER FRAME ──────────────────────────────────────────────────────
        # Fungsi ini menggambar ulang seluruh tampilan berdasarkan satu frame.
        # ANALOGI: Seperti mengambil foto kondisi rak di satu momen tertentu
        # ─────────────────────────────────────────────────────────────────────
        table = frame["table"]
        start = frame["start"]  # Rak tujuan awal (dari hash function)
        idx = frame["idx"]      # Rak yang sedang disorot saat ini
        phase = frame["phase"]  # Fase saat ini (start/collision/probe/place/pause)

        # Reset semua kotak rak ke tampilan default
        for j in range(n):
            rects[j].set_alpha(0.25)
            rects[j].set_linewidth(1.0)
            texts[j].set_text("" if table[j] is None else str(table[j]))

        # Sorot rak tujuan hash (hasil hash function) — lebih terang
        # ANALOGI: Petugas menunjuk rak yang seharusnya dituju buku ini
        rects[start].set_alpha(0.55)
        rects[start].set_linewidth(2.5)

        # Sorot rak yang sedang dicek saat ini — paling terang
        # ANALOGI: Petugas sedang berdiri di depan rak ini untuk mengeceknya
        rects[idx].set_alpha(0.75)
        rects[idx].set_linewidth(3.0)

        # Jika terjadi collision, buat rak lebih mencolok
        # ANALOGI: Tanda "RAK PENUH" menyala karena rak ini sudah ada buku lain
        if phase == "collision":
            rects[idx].set_alpha(0.9)

        filled = sum(v is not None for v in table)
        lf = filled / n  # Hitung load factor saat ini

        # Tampilkan info lengkap di info bar
        info.set_text(
            f"Frame {state['i']+1}/{len(frames)} | Step {frame['step']}/{args.nkeys} | key='{frame['key']}' | "
            f"hash%size={start} | idx={idx} | probes={frame['probes']} | load_factor={lf:.2f} | phase={phase} | "
            f"{'PAUSED' if state['paused'] else 'PLAY'}"
        )

        # Update grafik load factor
        # Hanya tampilkan data sampai buku yang sudah selesai disimpan
        completed = frame["step"] - 1 + (1 if frame["placed"] else 0)
        if completed <= 0:
            x, y = [], []
        else:
            x = list(range(1, completed + 1))
            y = load_factors[:completed]

        lf_line.set_data(x, y)
        if x:
            lf_dot.set_data([x[-1]], [y[-1]])
            bar_fg.set_width(0.96 * y[-1])  # Panjang bar sesuai load factor
            lf_text.set_text(f"Load Factor: {y[-1]:.2f} ({int(y[-1]*100)}%)")
        else:
            lf_dot.set_data([], [])
            bar_fg.set_width(0.00)
            lf_text.set_text("Load Factor: 0.00 (0%)")

        return rects + texts + [info, legend, lf_line, lf_dot, bar_fg, lf_text]

    def update(_):
        # ── UPDATE TIAP TICK ──────────────────────────────────────────────────
        # Dipanggil otomatis setiap interval ms oleh FuncAnimation.
        # Jika tidak di-pause, maju ke frame berikutnya.
        # ANALOGI: Setiap detik, satu langkah baru terjadi di perpustakaan
        # ─────────────────────────────────────────────────────────────────────
        if not state["paused"]:
            state["i"] = min(state["i"] + 1, len(frames) - 1)
        return render(frames[state["i"]])

    # Render frame pertama saat animasi dimulai
    def init():
        return render(frames[state["i"]])

    ani = FuncAnimation(
        fig, update, init_func=init,
        frames=np.arange(len(frames)),  # Timer tick — frame dikontrol manual via state["i"]
        interval=450, blit=False, repeat=False
    )

    def on_key(event):
        # ── KONTROL KEYBOARD ──────────────────────────────────────────────────
        # Menangani tombol keyboard dari pengguna.
        # ANALOGI: Seperti tombol play/pause/rewind pada video rekaman
        #          petugas perpustakaan sedang menyusun buku ke rak
        # ─────────────────────────────────────────────────────────────────────
        k = event.key

        if k == " ":
            # SPACE: toggle pause/resume animasi
            state["paused"] = not state["paused"]
            fig.canvas.draw_idle()

        elif k == "right":
            # → : maju satu langkah (hanya saat pause)
            # ANALOGI: Lihat satu kejadian berikutnya di perpustakaan
            if state["paused"]:
                state["i"] = min(state["i"] + 1, len(frames) - 1)
                render(frames[state["i"]])
                fig.canvas.draw_idle()

        elif k == "left":
            # ← : mundur satu langkah (hanya saat pause)
            # ANALOGI: Putar balik rekaman ke momen sebelum buku diletakkan
            if state["paused"]:
                state["i"] = max(state["i"] - 1, 0)
                render(frames[state["i"]])
                fig.canvas.draw_idle()

        elif k in ("r", "R"):
            # R: restart animasi dari awal dalam kondisi pause
            # ANALOGI: Kosongkan semua rak, mulai menyusun buku dari awal lagi
            state["i"] = 0
            state["paused"] = True
            render(frames[state["i"]])
            fig.canvas.draw_idle()

        elif k in ("escape", "q", "Q"):
            # Q / Esc: tutup jendela animasi
            plt.close(fig)

    fig.canvas.mpl_connect("key_press_event", on_key)

    if args.save == "gif":
        # Simpan animasi sebagai file GIF jika diminta
        # Butuh library 'pillow': pip install pillow
        try:
            from matplotlib.animation import PillowWriter
            ani.save("hash_table_premium_keyboard.gif", writer=PillowWriter(fps=2))
            print("Tersimpan: hash_table_premium_keyboard.gif")
        except Exception as e:
            print("Gagal simpan GIF. Pastikan 'pillow' terpasang. Error:", e)

    plt.show()


if __name__ == "__main__":
    main()