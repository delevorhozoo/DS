#author lordhozoo
#edit ampas ganti by author tolol  !!
import time
import subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# --- FUNGSI UNTUK MENDAPATKAN PATH CHROMIUM DAN DRIVER ---
def get_chromedriver_path():
    """Mencari path chromedriver yang terinstal di Termux."""
    try:
        # Cari path chromedriver menggunakan perintah 'which'
        path = subprocess.check_output(['which', 'chromedriver']).decode('utf-8').strip()
        return path
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Error: chromedriver tidak ditemukan. Pastikan Anda sudah menjalankan 'pkg install chromium'.")
        return None

# --- KONFIGURASI WEBDRIVER ---
def setup_driver():
    """Mengatur dan menjalankan WebDriver Chromium dalam mode headless."""
    chromedriver_path = get_chromedriver_path()
    if not chromedriver_path:
        return None

    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Menjalankan tanpa GUI (mode latar belakang)
    chrome_options.add_argument("--no-sandbox")  # Diperlukan untuk menjalankan sebagai root di lingkungan terbatas
    chrome_options.add_argument("--disable-dev-shm-usage")  # Menghindari masalah memori
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080") # Set ukuran window agar tidak ada masalah dengan elemen yang tersembunyi

    service = Service(executable_path=chromedriver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

# --- PROSES UTAMA PELAPORAN ---
def laporkan_username(username):
    """Fungsi untuk mengunjungi halaman dan mengirimkan laporan."""
    driver = setup_driver()
    if not driver:
        return

    try:
        # URL halaman feedback/report TikTok
        # Anda bisa ganti URL ini jika ingin melaporkan hal lain
        url = "https://www.tiktok.com/legal/report/feedback"
        print(f"Membuka halaman: {url}")
        driver.get(url)

        # Tunggu beberapa detik agar halaman termuat sepenuhnya
        print("Menunggu halaman dimuat...")
        time.sleep(5) 

        # --- INI BAGIAN YANG PALING PENTING DAN MUNGKIN PERLU DIUBAH ---
        # Anda perlu mencari 'selector' yang tepat untuk elemen di halaman tersebut.
        # Cara mencarinya: Buka TikTok di Chrome PC, klik kanan pada elemen (kolom input, tombol), lalu pilih "Inspect".
        # Lihat atribut 'id', 'name', atau 'class'. Gunakan yang paling unik.

        # Contoh: Mencari kolom feedback berdasarkan placeholder-nya
        # Ini adalah XPATH, cara pencarian yang lebih fleksibel.
        # XPATH ini berarti: cari elemen textarea yang memiliki atribut placeholder dengan teks 'Tell us more...'.
        feedback_field_xpath = "//textarea[@placeholder='Tell us more...']"
        
        print(f"Mencari kolom feedback dengan XPATH: {feedback_field_xpath}")
        feedback_field = driver.find_element(By.XPATH, feedback_field_xpath)
        
        # Isi kolom feedback dengan username
        print(f"Mengisi kolom dengan username: {username}")
        feedback_field.clear()
        feedback_field.send_keys(username)

        # Contoh: Mencari tombol "Submit"
        # Ini adalah XPATH untuk mencari tombol yang teksnya 'Submit'.
        submit_button_xpath = "//button[contains(., 'Submit')]"
        
        print(f"Mencari tombol kirim dengan XPATH: {submit_button_xpath}")
        submit_button = driver.find_element(By.XPATH, submit_button_xpath)
        
        # Klik tombol submit
        print("Mengklik tombol kirim...")
        submit_button.click()
        
        print("Laporan berhasil dikirim (asumsi tidak ada captcha atau error lain).")
        time.sleep(3) # Tunggu sebentar untuk melihat hasil

    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
        print("Kemungkinan besar selector (ID/XPATH) sudah tidak berlaku atau halaman gagal dimuat.")
        print("Silakan periksa kembali selector elemen di halaman TikTok.")

    finally:
        # Tutup browser
        print("Menutup browser.")
        driver.quit()


# --- EKSEKUSI SKRIP ---
if __name__ == "__main__":
    # Meminta input username dari pengguna
    username_to_report = input("Masukkan username yang ingin dilaporkan: ")
    if username_to_report:
        laporkan_username(username_to_report)
    else:
        print("Username tidak boleh kosong.")
