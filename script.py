import requests
import os
import threading
from urllib.parse import urlparse, unquote
import sys
import time

# Variabel global untuk menyimpan token Authorization
authorization_token = None

def get_authorization_token():
    global authorization_token

    # Jika token sudah ada, gunakan yang ada
    if authorization_token:
        return authorization_token

    # Jika token belum ada, minta dari pengguna
    authorization_token = input("Masukkan token Authorization: ")

    # Tambahkan "Key " di depan token jika belum ada
    if not authorization_token.startswith("Key "):
        authorization_token = f"Key {authorization_token}"

    return authorization_token

def loading_animation():
    chars = "/—\|/-\|/-\✓"  # Karakter untuk animasi loading
    for char in chars:
        sys.stdout.write(f"\rSending request... {char}")
        sys.stdout.flush()
        time.sleep(0.1)

def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def create_image():
    # Meminta input dari pengguna
    image_url = input("Masukkan URL gambar: ")
    prompt = input("Masukkan prompt: ")

    # Menambahkan parameter tambahan
    additional_params = {
        "guidance_scale": 7.5,
        "controlnet_conditioning_scale": 1,
        "control_guidance_start": 0,
        "control_guidance_end": 1,
        "seed": 65423178,
        "scheduler": "Euler",
        "num_inference_steps": 40
    }

    # Membentuk payload dengan input dari pengguna dan parameter tambahan
    payload = {
        "image_url": image_url,
        "prompt": prompt,
        **additional_params
    }

    url = "https://54285744-illusion-diffusion.gateway.alpha.fal.ai/"

    # Mengambil token Authorization
    headers = {
        "Authorization": get_authorization_token(),
        "Content-Type": "application/json"
    }

    # Menjalankan animasi loading dalam thread terpisah
    loading_thread = threading.Thread(target=loading_animation)
    loading_thread.start()

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()

        # Menunggu thread loading selesai
        loading_thread.join()

        # Mendapatkan URL gambar dari respons
        image_url_from_response = response.json().get('image', {}).get('url', '')

        # Memastikan bahwa URL gambar dari respons tidak kosong
        if image_url_from_response:
            # Mendapatkan nama file dari URL
            file_name = unquote(os.path.basename(urlparse(image_url_from_response).path))

            # Mendapatkan path dari folder saat ini
            current_folder = os.getcwd()

            # Menentukan path untuk menyimpan file gambar di folder saat ini
            file_path = os.path.join(current_folder, f"{prompt}_{file_name}")

            # Mengunduh dan menyimpan gambar
            image_response = requests.get(image_url_from_response, stream=True)
            image_response.raise_for_status()

            with open(file_path, 'wb') as file:
                for chunk in image_response.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)

            print(f"Gambar telah diunduh dan disimpan di: {file_path}")
            input("Tekan Enter untuk membuat gambar lainnya....")
            clear_screen()

        else:
            print("URL gambar dari respons kosong.")

    except requests.exceptions.RequestException as e:
        # Menunggu thread loading selesai
        loading_thread.join()
        print(f"Terjadi kesalahan pada permintaan: {e}")

    except Exception as e:
        # Menunggu thread loading selesai
        loading_thread.join()
        print(f"Terjadi kesalahan tak terduga: {e}")

def main():
    while True:
        print("""
Selamat Datang

Sebelum menggunakan script ini, hal yang perlu disiapkan adalah:
1. Akses Token Fal.ai
2. Link langsung gambar dasar (saya memakai imgbb)
3. Prompts/Perintah gambar
""")

        # Mengambil token Authorization
        get_authorization_token()

        lanjutkan = input("Apakah Anda siap melanjutkan? (Y/N): ")

        if lanjutkan.upper() != "Y":
            print("\033[1;31mTerimakasih Sudah menggunakan script ini. Jangan lupa follow @amin_maskur88 di TikTok dan Instagram\033[0m")
            break
        else:
            print("Melanjutkan eksekusi script...")
            create_image()

if __name__ == "__main__":
    main()
