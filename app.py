import streamlit as st
import google.generativeai as genai

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="AI Web Generator",
    page_icon="🤖",
    layout="wide"
)

# --- JUDUL & SIDEBAR ---
st.title("🤖 AI Website Generator Otomatis")
st.markdown("Tugas: Kecerdasan Artifisial & Pembelajaran Mesin")

with st.sidebar:
    st.header("⚙️ Konfigurasi")
    # Input API Key
    api_key = st.text_input("Masukkan Google Gemini API Key", type="password")
    st.info("Dapatkan API Key gratis di: aistudio.google.com")
    
    st.divider()
    st.caption("Model yang digunakan:")
    st.code("models/gemini-2.5-flash") # Menampilkan model yang dipakai

# --- FUNGSI GENERATOR (BACKEND) ---
def generate_site(prompt_text, key):
    try:
        genai.configure(api_key=key)
        
        # --- BAGIAN INI SUDAH DIPERBAIKI SESUAI DAFTAR MODELMU ---
        model = genai.GenerativeModel('models/gemini-2.5-flash')
        
        system_prompt = f"""
        Kamu adalah AI Web Developer ahli.
        Tugas: Buat file HTML Single Page lengkap (HTML+CSS+JS dalam satu file).
        
        Instruksi User: {prompt_text}
        
        Syarat Teknis:
        1. Desain harus modern, responsif, dan cantik.
        2. Gunakan CSS Internal (<style>) dan JS Internal (<script>).
        3. JANGAN minta user install apapun, gunakan CDN jika butuh library (misal Bootstrap/Tailwind).
        4. HANYA berikan kodingan mentah. Jangan pakai markdown (```html). Jangan ada teks pengantar.
        """
        
        response = model.generate_content(system_prompt)
        
        # Bersihkan format jika AI memberikan markdown wrapper
        clean_code = response.text.replace("```html", "").replace("```", "").strip()
        return clean_code
        
    except Exception as e:
        return f"Error: {str(e)}"

# --- UI UTAMA ---
col1, col2 = st.columns([1, 3])

with col1:
    st.subheader("1. Deskripsi")
    user_prompt = st.text_area(
        "Website seperti apa?", 
        height=200,
        placeholder="Contoh: Buat landing page profil diri (Portfolio). Tema warna biru gelap. Ada foto profil bulat di tengah, skill bar, dan tombol kontak WhatsApp."
    )
    generate_btn = st.button("🚀 Generate Website", type="primary", use_container_width=True)

with col2:
    st.subheader("2. Hasil Output")
    
    if generate_btn:
        if not api_key:
            st.error("⚠️ Masukkan API Key di menu sebelah kiri dulu ya!")
        elif not user_prompt:
            st.warning("⚠️ Isi deskripsi websitenya dulu.")
        else:
            with st.spinner("Gemini 2.5 Flash sedang menulis kodingan..."):
                # Proses Generasi
                generated_code = generate_site(user_prompt, api_key)
                
                # Cek jika ada error
                if generated_code.startswith("Error"):
                    st.error(generated_code)
                else:
                    st.success("Selesai! Silakan cek tab di bawah.")
                    
                    # --- FITUR TABS (PREVIEW VS KODINGAN) ---
                    tab_preview, tab_code = st.tabs(["👁️ Preview Website", "📄 Lihat Source Code"])
                    
                    with tab_preview:
                        st.caption("Tampilan hasil:")
                        st.components.v1.html(generated_code, height=600, scrolling=True)
                    
                    with tab_code:
                        st.caption("Kodingan asli:")
                        st.code(generated_code, language="html")
                    
                    # --- FITUR DOWNLOAD ---
                    st.download_button(
                        label="📥 Download File .html",
                        data=generated_code,
                        file_name="index.html",
                        mime="text/html",
                        type="primary"
                    )