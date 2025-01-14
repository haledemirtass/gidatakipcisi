import time
import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime, timedelta
import threading
import os

class GelismisMutfakTakip:
    def __init__(self):
        self.pencere = tk.Tk()
        self.pencere.title("Gelişmiş Mutfak Takip")
        self.pencere.geometry("800x600")

        # Tema değişkenleri
        self.theme_colors = {
            'light': {
                'bg': '#fdfaf9',
                'fg': '#333333',
                'notebook_bg': '#065d22',
                'tab_bg': '#d38548',
                'selected_tab': '#f3ef80',
                'frame_bg': '#a0df90',
                'button_bg': '#b93124',
                'button_fg': 'white',
                'tree_bg': 'white',
                'tree_fg': 'black'
            },
            'dark': {
                'bg': '#2d2d2d',
                'fg': '#ffffff',
                'notebook_bg': '#1a472a',
                'tab_bg': '#854f1b',
                'selected_tab': '#8f8b30',
                'frame_bg': '#2d5f1f',
                'button_bg': '#641b14',
                'button_fg': '#ffffff',
                'tree_bg': '#363636',
                'tree_fg': '#ffffff'
            }
        }
        
        self.current_theme = 'light'
        
        # Tema değiştirme butonu
        self.theme_button = ttk.Button(
            self.pencere, 
            text="🌙 Dark Mode", 
            command=self.toggle_theme,
            style="Theme.TButton"
        )
        self.theme_button.pack(anchor='ne', padx=10, pady=5)

        # Stil oluşturma
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.apply_theme()

        # JSON dosya işlemleri
        self.veritabani_dosyasi = 'mutfak.json'
        self.veritabani_olustur()

        # Ana notebook (sekmeli arayüz)
        self.notebook = ttk.Notebook(self.pencere)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=5)

        # Sekmeler
        self.urun_ekle_tab = ttk.Frame(self.notebook)
        self.urun_listesi_tab = ttk.Frame(self.notebook)
        self.rapor_tab = ttk.Frame(self.notebook)
        self.alisveris_listesi_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.urun_ekle_tab, text='Ürün Ekle')
        self.notebook.add(self.urun_listesi_tab, text='Ürün Listesi')
        self.notebook.add(self.rapor_tab, text='Raporlar')
        self.notebook.add(self.alisveris_listesi_tab, text='Alışveriş Listesi')

        # Arayüz elemanlarını oluştur
        self.urun_ekle_arayuzu()
        self.urun_liste_arayuzu()
        self.rapor_arayuzu()
        self.alisveris_listesi_arayuzu()

        # Otomatik silme işlemini başlat
        self.otomatik_silme_thread = threading.Thread(target=self.otomatik_silme_kontrol, daemon=True)
        self.otomatik_silme_thread.start()

        self.pencere.mainloop()

    def apply_theme(self):
        colors = self.theme_colors[self.current_theme]
        
        # Ana pencere teması
        self.pencere.configure(bg=colors['bg'])
        
        # Stil konfigürasyonları
        self.style.configure("TFrame", background=colors['bg'])
        self.style.configure("TLabelFrame", 
                           background=colors['frame_bg'],
                           foreground=colors['fg'])
        self.style.configure("TLabel", 
                           background=colors['bg'],
                           foreground=colors['fg'])
        self.style.configure("TNotebook", 
                           background=colors['notebook_bg'])
        self.style.configure("TNotebook.Tab", 
                           background=colors['tab_bg'],
                           foreground=colors['fg'])
        self.style.map("TNotebook.Tab", 
                      background=[("selected", colors['selected_tab'])])
        self.style.configure("Treeview", 
                           background=colors['tree_bg'],
                           foreground=colors['tree_fg'],
                           fieldbackground=colors['tree_bg'])
        self.style.configure("Treeview.Heading", 
                           background=colors['bg'],
                           foreground=colors['fg'])
        self.style.configure("TButton", 
                           background=colors['button_bg'],
                           foreground=colors['button_fg'])
        self.style.configure("Theme.TButton", 
                           padding=5)

        # Tema butonu metnini güncelle
        self.theme_button.configure(
            text="🌙 Dark Mode" if self.current_theme == 'light' else "☀️ Light Mode"
        )

    def toggle_theme(self):
        self.current_theme = 'dark' if self.current_theme == 'light' else 'light'
        self.apply_theme()

    def veritabani_olustur(self):
        if not os.path.exists(self.veritabani_dosyasi):
            veritabani_yapisi = {
                'kategoriler': [
                    {'id': 1, 'kategori_adi': 'Meyve/Sebze'},
                    {'id': 2, 'kategori_adi': 'Et Ürünleri'},
                    {'id': 3, 'kategori_adi': 'Süt Ürünleri'},
                    {'id': 4, 'kategori_adi': 'Kuru Gıda'},
                    {'id': 5, 'kategori_adi': 'Diğer'}
                ],
                'urunler': []
            }
            with open(self.veritabani_dosyasi, 'w', encoding='utf-8') as dosya:
                json.dump(veritabani_yapisi, dosya, ensure_ascii=False, indent=4)

    def json_veri_oku(self):
        with open(self.veritabani_dosyasi, 'r', encoding='utf-8') as dosya:
            return json.load(dosya)

    def json_veri_yaz(self, veri):
        with open(self.veritabani_dosyasi, 'w', encoding='utf-8') as dosya:
            json.dump(veri, dosya, ensure_ascii=False, indent=4)

    def urun_ekle_arayuzu(self):
        frame = ttk.LabelFrame(self.urun_ekle_tab, text="Yeni Ürün Ekle", padding="10")
        frame.pack(fill='x', padx=10, pady=5)

        # Kategori seçimi
        ttk.Label(frame, text="Kategori:").grid(row=0, column=0, padx=5, pady=5)
        self.kategori_secim = ttk.Combobox(frame, values=self.kategorileri_getir())
        self.kategori_secim.grid(row=0, column=1, padx=5, pady=5)
        self.kategori_secim.set("Seçiniz")

        # Ürün adı
        ttk.Label(frame, text="Ürün Adı:").grid(row=1, column=0, padx=5, pady=5)
        self.urun_adi = ttk.Entry(frame)
        self.urun_adi.grid(row=1, column=1, padx=5, pady=5)

        # Miktar
        ttk.Label(frame, text="Miktar:").grid(row=2, column=0, padx=5, pady=5)
        self.miktar = ttk.Entry(frame)
        self.miktar.grid(row=2, column=1, padx=5, pady=5)

        # Birim
        ttk.Label(frame, text="Birim:").grid(row=2, column=2, padx=5, pady=5)
        self.birim = ttk.Combobox(frame, values=['Adet', 'Kg', 'Gram', 'Litre', 'mL'])
        self.birim.grid(row=2, column=3, padx=5, pady=5)
        self.birim.set("Adet")

        # Son kullanma süresi
        ttk.Label(frame, text="Son Kullanma Süresi (Gün):").grid(row=3, column=0, padx=5, pady=5)
        self.skt = ttk.Entry(frame)
        self.skt.grid(row=3, column=1, padx=5, pady=5)

        # Not
        ttk.Label(frame, text="Not:").grid(row=4, column=0, padx=5, pady=5)
        self.not_giris = ttk.Entry(frame)
        self.not_giris.grid(row=4, column=1, columnspan=3, padx=5, pady=5, sticky='ew')

        # Ekle butonu
        ttk.Button(frame, text="Ürün Ekle", command=self.urun_ekle).grid(row=5, column=0, columnspan=4, pady=10)

    def urun_ekle(self):
        try:
            kategori = self.kategori_secim.get()
            urun = self.urun_adi.get()
            miktar = int(self.miktar.get())
            birim = self.birim.get()
            gun = int(self.skt.get())
            not_giris = self.not_giris.get()

            if not all([kategori, urun, miktar, birim, gun]):
                raise ValueError("Tüm alanları doldurun!")

            eklenme = datetime.now()
            son_kullanma = eklenme + timedelta(days=gun)

            # JSON dosyasını oku
            veri = self.json_veri_oku()

            # Kategori ID'sini al
            kategori_id = next((item['id'] for item in veri['kategoriler'] if item['kategori_adi'] == kategori), None)
            if kategori_id is None:
                raise ValueError("Seçilen kategori bulunamadı.")

            # Ürünü ekle
            urun_bilgisi = {
                'id': len(veri['urunler']) + 1,
                'urun_adi': urun,
                'miktar': miktar,
                'birim': birim,
                'kategori_id': kategori_id,
                'eklenme_tarihi': eklenme.strftime('%Y-%m-%d'),
                'son_kullanma': son_kullanma.strftime('%Y-%m-%d'),
                'notlar': not_giris
            }
            veri['urunler'].append(urun_bilgisi)

            # JSON dosyasına yaz
            self.json_veri_yaz(veri)
            messagebox.showinfo("Başarılı", "Ürün başarıyla eklendi!")

            # Formu temizle
            self.urun_adi.delete(0, tk.END)
            self.miktar.delete(0, tk.END)
            self.skt.delete(0, tk.END)
            self.not_giris.delete(0, tk.END)

            # Listeyi güncelle
            self.liste_guncelle()

        except ValueError as e:
            messagebox.showerror("Hata", str(e))
        except Exception as e:
            import traceback
            messagebox.showerror("Hata", f"Beklenmeyen bir hata oluştu: {str(e)}\n{traceback.format_exc()}")

    def urun_liste_arayuzu(self):
        # Filtreleme alanı
        filtre_frame = ttk.LabelFrame(self.urun_listesi_tab, text="Filtrele", padding="10")
        filtre_frame.pack(fill='x', padx=10, pady=5)

        ttk.Label(filtre_frame, text="Kategori:").pack(side='left', padx=5)
        self.filtre_kategori = ttk.Combobox(filtre_frame, values=['Tümü'] + self.kategorileri_getir())
        self.filtre_kategori.pack(side='left', padx=5)
        self.filtre_kategori.set("Tümü")

        ttk.Button(filtre_frame, text="Filtrele", command=self.liste_guncelle).pack(side='left', padx=5)

        # Ürün listesi
        self.tree = ttk.Treeview(self.urun_listesi_tab, columns=('Ürün', 'Miktar', 'Kategori', 'Eklenme', 'SKT', 'Not'), show='headings')
        self.tree.pack(fill='both', expand=True, padx=10, pady=5)

        self.tree.heading('Ürün', text='Ürün Adı')
        self.tree.heading('Miktar', text='Miktar')
        self.tree.heading('Kategori', text='Kategori')
        self.tree.heading('Eklenme', text='Eklenme Tarihi')
        self.tree.heading('SKT', text='Son Kullanma')
        self.tree.heading('Not', text='Not')

        # Silme butonu
        ttk.Button(self.urun_listesi_tab, text="Seçili Ürünü Sil", command=self.urun_sil).pack(pady=5)

        # Miktar artırma ve azaltma butonları
        ttk.Button(self.urun_listesi_tab, text="Miktar Artır", command=self.urun_miktar_artir).pack(pady=5)
        ttk.Button(self.urun_listesi_tab, text="Miktar Azalt", command=self.urun_miktar_azalt).pack(pady=5)

    def urun_miktar_artir(self):
        secili = self.tree.selection()
        if not secili:
            messagebox.showerror("Hata", "Lütfen miktarını artırmak istediğiniz ürünü seçin!")
            return

        urun_adi = self.tree.item(secili[0])['values'][0]

        # JSON dosyasını oku
        veri = self.json_veri_oku()

        # Ürün miktarını artır
        for urun in veri['urunler']:
            if urun['urun_adi'] == urun_adi:
                urun['miktar'] += 1
                break

        # JSON dosyasına yaz
        self.json_veri_yaz(veri)
        self.liste_guncelle()
        messagebox.showinfo("Başarılı", "Ürün miktarı artırıldı!")

    def urun_miktar_azalt(self):
        secili = self.tree.selection()
        if not secili:
            messagebox.showerror("Hata", "Lütfen miktarını azaltmak istediğiniz ürünü seçin!")
            return

        urun_adi = self.tree.item(secili[0])['values'][0]

        # JSON dosyasını oku
        veri = self.json_veri_oku()

        # Ürün miktarını azalt
        for urun in veri['urunler']:
            if urun['urun_adi'] == urun_adi:
                if urun['miktar'] > 0:
                    urun['miktar'] -= 1
                break

        # JSON dosyasına yaz
        self.json_veri_yaz(veri)
        self.liste_guncelle()
        messagebox.showinfo("Başarılı", "Ürün miktarı azaltıldı!")

    def liste_guncelle(self):
        # Mevcut listeyi temizle
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Filtre kategorisini al
        filtre_kategori = self.filtre_kategori.get()

        # JSON dosyasını oku
        veri = self.json_veri_oku()

        # Ürünleri kategoriye göre sıralayarak listele
        kategoriler = {kategori['id']: kategori['kategori_adi'] for kategori in veri['kategoriler']}
        urunler = sorted(veri['urunler'], key=lambda x: (x['kategori_id'], x['urun_adi']))

        for urun in urunler:
            kategori_adi = kategoriler.get(urun['kategori_id'], 'Bilinmiyor')
            if filtre_kategori == "Tümü" or kategori_adi == filtre_kategori:
                miktar_str = f"{urun['miktar']} {urun['birim']}"  # miktar ve birim
                self.tree.insert('', 'end', values=(urun['urun_adi'], miktar_str, kategori_adi, urun['eklenme_tarihi'], urun['son_kullanma'], urun['notlar']))

    def urun_sil(self):
        secili = self.tree.selection()
        if not secili:
            messagebox.showerror("Hata", "Lütfen silinecek ürünü seçin!")
            return

        if messagebox.askyesno("Onay", "Seçili ürünü silmek istediğinizden emin misiniz?"):
            urun_adi = self.tree.item(secili[0])['values'][0]

            # JSON dosyasını oku
            veri = self.json_veri_oku()

            # Ürünü sil
            veri['urunler'] = [urun for urun in veri['urunler'] if urun['urun_adi'] != urun_adi]

            # JSON dosyasına yaz
            self.json_veri_yaz(veri)
            self.liste_guncelle()
            messagebox.showinfo("Başarılı", "Ürün silindi!")

    def rapor_arayuzu(self):
        # Rapor seçenekleri
        ttk.Button(self.rapor_tab, text="Son Kullanma Tarihi Yaklaşanlar",
                   command=lambda: self.rapor_goster("yaklasan")).pack(pady=5)
        ttk.Button(self.rapor_tab, text="Kategori Bazlı Stok Raporu",
                   command=lambda: self.rapor_goster("kategori")).pack(pady=5)

        # Rapor sonuçları için text alanı
        self.rapor_sonuc = tk.Text(self.rapor_tab, height=20, width=60)
        self.rapor_sonuc.pack(pady=10, padx=10)

    def rapor_goster(self, rapor_tipi):
        self.rapor_sonuc.delete(1.0, tk.END)

        # JSON dosyasını oku
        veri = self.json_veri_oku()

        if rapor_tipi == "yaklasan":
            # Son kullanma tarihi yaklaşan ürünler (7 gün içinde)
            self.rapor_sonuc.insert(tk.END, "SON KULLANMA TARİHİ YAKLAŞAN ÜRÜNLER\n")
            self.rapor_sonuc.insert(tk.END, "-" * 50 + "\n\n")

            for urun in veri['urunler']:
                son_kullanma_tarihi = datetime.strptime(urun['son_kullanma'], '%Y-%m-%d')
                if (son_kullanma_tarihi - datetime.now()).days <= 7:
                    kategori_adi = next((item['kategori_adi'] for item in veri['kategoriler'] if item['id'] == urun['kategori_id']), 'Bilinmiyor')
                    self.rapor_sonuc.insert(tk.END,
                        f"Ürün: {urun['urun_adi']}\n"
                        f"Miktar: {urun['miktar']} {urun['birim']}\n"
                        f"Kategori: {kategori_adi}\n"
                        f"Son Kullanma: {urun['son_kullanma']}\n"
                        f"Not: {urun['notlar']}\n"
                        f"{'-' * 30}\n")

        elif rapor_tipi == "kategori":
            # Kategori bazlı stok raporu
            self.rapor_sonuc.insert(tk.END, "KATEGORİ BAZLI STOK RAPORU\n")
            self.rapor_sonuc.insert(tk.END, "-" * 50 + "\n\n")

            kategori_urunleri = {kategori['kategori_adi']: [] for kategori in veri['kategoriler']}
            for urun in veri['urunler']:
                kategori_adi = next((item['kategori_adi'] for item in veri['kategoriler'] if item['id'] == urun['kategori_id']), 'Bilinmiyor')
                kategori_urunleri[kategori_adi].append(urun['urun_adi'])

            for kategori, urunler in kategori_urunleri.items():
                self.rapor_sonuc.insert(tk.END, f"Kategori: {kategori}\n")
                for urun in urunler:
                    self.rapor_sonuc.insert(tk.END, f"  - {urun}\n")
                self.rapor_sonuc.insert(tk.END, f"{'-' * 30}\n")

    def kategorileri_getir(self):
        veri = self.json_veri_oku()
        return [kategori['kategori_adi'] for kategori in veri['kategoriler']]

    def alisveris_listesi_arayuzu(self):
        frame = ttk.LabelFrame(self.alisveris_listesi_tab, text="Alışveriş Listesi", padding="10")
        frame.pack(fill='x', padx=10, pady=5)

        # Ürün adı girişi
        ttk.Label(frame, text="Ürün Adı:").grid(row=0, column=0, padx=5, pady=5)
        self.alisveris_urun_adi = ttk.Entry(frame)
        self.alisveris_urun_adi.grid(row=0, column=1, padx=5, pady=5)

        # Miktar girişi
        ttk.Label(frame, text="Miktar:").grid(row=1, column=0, padx=5, pady=5)
        self.alisveris_miktar = ttk.Entry(frame)
        self.alisveris_miktar.grid(row=1, column=1, padx=5, pady=5)

        # Birim seçimi
        ttk.Label(frame, text="Birim:").grid(row=1, column=2, padx=5, pady=5)
        self.alisveris_birim = ttk.Combobox(frame, values=['Adet', 'Kg', 'Gram', 'Litre', 'mL'])
        self.alisveris_birim.grid(row=1, column=3, padx=5, pady=5)
        self.alisveris_birim.set("Adet")

        # Alışveriş listesine ekle butonu
        ttk.Button(frame, text="Listeye Ekle", command=self.alisveris_listesine_ekle).grid(row=2, column=0, columnspan=4, pady=10)

        # Alışveriş listesi
        self.alisveris_tree = ttk.Treeview(self.alisveris_listesi_tab, columns=('Ürün', 'Miktar', 'Birim'), show='headings')
        self.alisveris_tree.pack(fill='both', expand=True, padx=10, pady=5)

        self.alisveris_tree.heading('Ürün', text='Ürün Adı')
        self.alisveris_tree.heading('Miktar', text='Miktar')
        self.alisveris_tree.heading('Birim', text='Birim')

        # Listeyi temizleme butonu
        ttk.Button(self.alisveris_listesi_tab, text="Listeyi Temizle", command=self.alisveris_listesini_temizle).pack(pady=5)

    def alisveris_listesine_ekle(self):
        try:
            urun = self.alisveris_urun_adi.get()
            miktar = int(self.alisveris_miktar.get())
            birim = self.alisveris_birim.get()

            if not all([urun, miktar, birim]):
                raise ValueError("Tüm alanları doldurun!")

            self.alisveris_tree.insert('', 'end', values=(urun, miktar, birim))

            # Formu temizle
            self.alisveris_urun_adi.delete(0, tk.END)
            self.alisveris_miktar.delete(0, tk.END)

        except ValueError as e:
            messagebox.showerror("Hata", str(e))

    def alisveris_listesini_temizle(self):
        for item in self.alisveris_tree.get_children():
            self.alisveris_tree.delete(item)

    def otomatik_silme_kontrol(self):
        while True:
            current_date = datetime.now().strftime('%Y-%m-%d')

            # JSON dosyasını oku
            veri = self.json_veri_oku()

            # Tarihi geçmiş ürünleri sil
            veri['urunler'] = [urun for urun in veri['urunler'] if urun['son_kullanma'] >= current_date]

            # JSON dosyasına yaz
            self.json_veri_yaz(veri)
            time.sleep(86400)  # Bir gün (24 saat) bekle

if __name__ == "__main__":
    GelismisMutfakTakip()

        
