import google.generativeai as genai

# MASUKKAN API KEY KAMU DI SINI
api_key = "AIzaSyDjMU7_X8Bdt-Zvw7EJwjqUmriIrdNAlh0"

genai.configure(api_key=api_key)

print("Sedang mengecek daftar model yang tersedia...")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"- {m.name}")
except Exception as e:
    print(f"Error: {e}")