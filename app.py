"""
AI UTBK Readiness Dashboard - Enhanced Version
Sistem analisis kesiapan UTBK berbasis AI dengan pendekatan holistik
Skor maksimal UTBK: 1000
"""

import streamlit as st
import numpy as np
import pandas as pd
import pickle
import os
import io
import base64
import datetime
from typing import Dict, Tuple
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots


# ======================================
# PAGE CONFIG
# ======================================

st.set_page_config(
    page_title="AI UTBK Dashboard",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ======================================
# CUSTOM CSS
# ======================================

st.markdown("""
<style>
    /* Import Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Global */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        min-height: 100vh;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        border-right: 1px solid rgba(99, 179, 237, 0.2);
    }
    [data-testid="stSidebar"] * {
        color: #e2e8f0 !important;
    }
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stSlider label,
    [data-testid="stSidebar"] .stTextInput label {
        color: #90cdf4 !important;
        font-weight: 500;
    }
    
    /* Cards */
    .metric-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 20px;
        margin: 8px 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    .hero-card {
        background: linear-gradient(135deg, rgba(99, 179, 237, 0.15), rgba(154, 117, 234, 0.15));
        border: 1px solid rgba(99, 179, 237, 0.3);
        border-radius: 20px;
        padding: 30px;
        margin: 16px 0;
        text-align: center;
    }
    
    .score-display {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #63b3ed, #9f7aea);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        line-height: 1.2;
    }
    
    .badge-green {
        background: linear-gradient(135deg, #38a169, #48bb78);
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        display: inline-block;
    }
    .badge-orange {
        background: linear-gradient(135deg, #dd6b20, #ed8936);
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        display: inline-block;
    }
    .badge-red {
        background: linear-gradient(135deg, #c53030, #e53e3e);
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        display: inline-block;
    }
    
    /* Step indicators */
    .step-indicator {
        background: rgba(99, 179, 237, 0.1);
        border: 2px solid rgba(99, 179, 237, 0.4);
        border-radius: 50%;
        width: 40px;
        height: 40px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        color: #63b3ed;
        font-size: 1.1rem;
    }
    
    .step-active {
        background: linear-gradient(135deg, #4299e1, #9f7aea);
        border: none;
        color: white;
    }
    
    /* Progress bar custom */
    .progress-bar-bg {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        height: 12px;
        overflow: hidden;
    }
    .progress-bar-fill {
        height: 100%;
        border-radius: 10px;
        background: linear-gradient(90deg, #4299e1, #9f7aea);
        transition: width 0.5s ease;
    }
    
    /* Section headers */
    .section-header {
        color: #e2e8f0;
        font-size: 1.4rem;
        font-weight: 700;
        margin-bottom: 16px;
        padding-bottom: 8px;
        border-bottom: 2px solid rgba(99, 179, 237, 0.3);
    }
    
    /* Welcome page */
    .welcome-hero {
        background: linear-gradient(135deg, rgba(66, 153, 225, 0.2), rgba(159, 122, 234, 0.2));
        border: 1px solid rgba(99, 179, 237, 0.3);
        border-radius: 24px;
        padding: 40px;
        text-align: center;
        margin-bottom: 24px;
    }
    
    .feature-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 20px;
        height: 100%;
        transition: transform 0.2s, border-color 0.2s;
    }
    .feature-card:hover {
        transform: translateY(-4px);
        border-color: rgba(99, 179, 237, 0.4);
    }
    
    /* Metric value display */
    .big-number {
        font-size: 2.5rem;
        font-weight: 800;
        line-height: 1;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 4px;
        gap: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        font-weight: 600;
        color: #a0aec0 !important;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #4299e1, #9f7aea) !important;
        color: white !important;
    }
    
    /* Bobot table */
    .bobot-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 8px 12px;
        margin: 4px 0;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 8px;
        border-left: 3px solid #4299e1;
    }
    
    /* Info boxes */
    .info-box {
        background: rgba(66, 153, 225, 0.1);
        border: 1px solid rgba(66, 153, 225, 0.3);
        border-radius: 12px;
        padding: 16px;
        margin: 8px 0;
    }
    .success-box {
        background: rgba(56, 161, 105, 0.1);
        border: 1px solid rgba(56, 161, 105, 0.3);
        border-radius: 12px;
        padding: 16px;
        margin: 8px 0;
    }
    .warning-box {
        background: rgba(221, 107, 32, 0.1);
        border: 1px solid rgba(221, 107, 32, 0.3);
        border-radius: 12px;
        padding: 16px;
        margin: 8px 0;
    }
    .danger-box {
        background: rgba(197, 48, 48, 0.1);
        border: 1px solid rgba(197, 48, 48, 0.3);
        border-radius: 12px;
        padding: 16px;
        margin: 8px 0;
    }
    
    /* Button styling */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #4299e1, #9f7aea) !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        letter-spacing: 0.5px;
        box-shadow: 0 4px 15px rgba(66, 153, 225, 0.4) !important;
        transition: all 0.3s ease !important;
    }
    .stButton > button[kind="primary"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(66, 153, 225, 0.6) !important;
    }
    
    /* Plotly chart background */
    .js-plotly-plot .plotly {
        background: transparent !important;
    }
    
    /* Metric styling */
    [data-testid="metric-container"] {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 12px;
    }
    [data-testid="metric-container"] label {
        color: #a0aec0 !important;
        font-size: 0.8rem !important;
    }
    [data-testid="metric-container"] [data-testid="metric-value"] {
        color: #e2e8f0 !important;
        font-weight: 700 !important;
    }
</style>
""", unsafe_allow_html=True)


# ======================================
# LOAD MODEL LGBM
# ======================================

@st.cache_resource
def load_lgbm_model():
    model_path = os.path.join(os.path.dirname(__file__), "lgbm_model_2_.pkl")
    try:
        with open(model_path, "rb") as f:
            model = pickle.load(f)
        return model, True
    except FileNotFoundError:
        return None, False
    except Exception as e:
        return None, False


# ======================================
# KONSTANTA
# ======================================

SKOR_MAX_UTBK = 1000

LABEL_STRATEGI = [
    "Intensif & Terstruktur",
    "Penguatan Mental",
    "Optimasi & Review",
    "Pertahankan & Tingkatkan"
]

DESKRIPSI_STRATEGI = {
    "Intensif & Terstruktur": {
        "icon": "🔴",
        "deskripsi": "Kebiasaan belajar dan kondisi psikologis perlu ditingkatkan secara bersamaan.",
        "tips": [
            "Buat jadwal belajar harian yang ketat dan konsisten",
            "Mulai dari 2 jam/hari lalu tingkatkan bertahap",
            "Gunakan metode Pomodoro (25 menit fokus, 5 menit istirahat)",
            "Cari teman belajar atau bergabung dengan kelompok belajar",
            "Konsultasi dengan guru/mentor untuk panduan belajar"
        ]
    },
    "Penguatan Mental": {
        "icon": "🟠",
        "deskripsi": "Kebiasaan belajar sudah cukup baik, namun kondisi psikologis perlu diperkuat.",
        "tips": [
            "Latihan mindfulness atau meditasi 10 menit sebelum belajar",
            "Buat target kecil harian agar rasa percaya diri meningkat",
            "Kurangi perbandingan diri dengan orang lain",
            "Tetapkan rutinitas tidur yang baik untuk mengurangi kecemasan",
            "Lakukan simulasi ujian (tryout) secara rutin"
        ]
    },
    "Optimasi & Review": {
        "icon": "🟡",
        "deskripsi": "Kebiasaan dan mental sudah baik, tingkatkan kualitas review dan evaluasi soal.",
        "tips": [
            "Perbanyak review soal-soal yang pernah salah",
            "Analisis pola kesalahan di setiap subtes",
            "Tingkatkan frekuensi tryout menjadi minimal 2x/bulan",
            "Buat catatan ringkasan materi yang sering keluar",
            "Fokus pada efisiensi waktu mengerjakan soal"
        ]
    },
    "Pertahankan & Tingkatkan": {
        "icon": "🟢",
        "deskripsi": "Kebiasaan belajar dan kondisi psikologis sudah sangat baik!",
        "tips": [
            "Pertahankan konsistensi dan jangan lengah",
            "Tingkatkan target skor tryout secara bertahap",
            "Mulai fokus pada strategi manajemen waktu saat ujian",
            "Bantu teman yang kesulitan — mengajar memperkuat pemahaman",
            "Jaga kesehatan fisik agar performa tetap optimal"
        ]
    }
}

SUBTES_LABELS = {
    "PU": "Penalaran Umum",
    "PPU": "Pemahaman & Penulisan Umum",
    "PBM": "Pemahaman Bacaan & Menulis",
    "PK": "Pengetahuan Kuantitatif",
    "LBI": "Literasi Bahasa Indonesia",
    "LBE": "Literasi Bahasa Inggris",
    "PM": "Penalaran Matematika"
}

DAFTAR_JURUSAN = [
    "Kedokteran", "Kedokteran Gigi",
    "Teknik Sipil", "Teknik Mesin", "Teknik Elektro",
    "Teknik Industri", "Teknik Kimia", "Teknik Informatika",
    "Matematika", "Fisika", "Kimia", "Biologi",
    "Statistika", "Aktuaria",
    "Farmasi", "Gizi", "Keperawatan", "Kesehatan Masyarakat",
    "Ilmu Hukum",
    "Ekonomi", "Manajemen", "Akuntansi", "Bisnis",
    "Psikologi", "Ilmu Komunikasi", "Hubungan Internasional",
    "Administrasi Publik",
    "Sastra Inggris", "Pendidikan Bahasa Indonesia",
    "Pendidikan Bahasa Inggris",
    "Sosiologi", "Ilmu Politik", "Sejarah", "Geografi"
]

BOBOT_JURUSAN = {
    "kesehatan_utama": {
        "jurusan": ["Kedokteran", "Kedokteran Gigi"],
        "label": "Kelompok Kesehatan Utama",
        "bobot": {"PU": 0.20, "PPU": 0.15, "PBM": 0.10, "PK": 0.15, "LBI": 0.10, "LBE": 0.10, "PM": 0.20}
    },
    "teknik": {
        "jurusan": ["Teknik Sipil", "Teknik Mesin", "Teknik Elektro", "Teknik Industri", "Teknik Kimia", "Teknik Informatika"],
        "label": "Kelompok Teknik",
        "bobot": {"PU": 0.20, "PPU": 0.10, "PBM": 0.05, "PK": 0.20, "LBI": 0.05, "LBE": 0.10, "PM": 0.30}
    },
    "saintek_murni": {
        "jurusan": ["Matematika", "Fisika", "Kimia", "Biologi", "Statistika", "Aktuaria"],
        "label": "Sains & Teknologi Murni",
        "bobot": {"PU": 0.20, "PPU": 0.10, "PBM": 0.05, "PK": 0.20, "LBI": 0.05, "LBE": 0.05, "PM": 0.35}
    },
    "kesehatan_terapan": {
        "jurusan": ["Farmasi", "Gizi", "Keperawatan", "Kesehatan Masyarakat"],
        "label": "Kelompok Kesehatan Terapan",
        "bobot": {"PU": 0.20, "PPU": 0.15, "PBM": 0.10, "PK": 0.15, "LBI": 0.15, "LBE": 0.10, "PM": 0.15}
    },
    "hukum": {
        "jurusan": ["Ilmu Hukum"],
        "label": "Kelompok Hukum",
        "bobot": {"PU": 0.20, "PPU": 0.20, "PBM": 0.20, "PK": 0.05, "LBI": 0.20, "LBE": 0.10, "PM": 0.05}
    },
    "ekonomi_bisnis": {
        "jurusan": ["Ekonomi", "Manajemen", "Akuntansi", "Bisnis"],
        "label": "Ekonomi & Bisnis",
        "bobot": {"PU": 0.20, "PPU": 0.15, "PBM": 0.10, "PK": 0.20, "LBI": 0.10, "LBE": 0.10, "PM": 0.15}
    },
    "psikologi": {
        "jurusan": ["Psikologi"],
        "label": "Kelompok Psikologi",
        "bobot": {"PU": 0.20, "PPU": 0.15, "PBM": 0.20, "PK": 0.10, "LBI": 0.15, "LBE": 0.10, "PM": 0.10}
    },
    "komunikasi_hubungan": {
        "jurusan": ["Ilmu Komunikasi", "Hubungan Internasional", "Administrasi Publik"],
        "label": "Komunikasi & Hubungan",
        "bobot": {"PU": 0.15, "PPU": 0.20, "PBM": 0.20, "PK": 0.05, "LBI": 0.20, "LBE": 0.15, "PM": 0.05}
    },
    "bahasa": {
        "jurusan": ["Sastra Inggris", "Pendidikan Bahasa Indonesia", "Pendidikan Bahasa Inggris"],
        "label": "Kelompok Bahasa & Sastra",
        "bobot": {"PU": 0.10, "PPU": 0.15, "PBM": 0.25, "PK": 0.05, "LBI": 0.25, "LBE": 0.15, "PM": 0.05}
    },
    "sosial_humaniora": {
        "jurusan": ["Sosiologi", "Ilmu Politik", "Sejarah", "Geografi"],
        "label": "Sosial & Humaniora",
        "bobot": {"PU": 0.15, "PPU": 0.20, "PBM": 0.25, "PK": 0.05, "LBI": 0.20, "LBE": 0.10, "PM": 0.05}
    },
    "default": {
        "jurusan": [],
        "label": "Umum",
        "bobot": {"PU": 0.20, "PPU": 0.15, "PBM": 0.15, "PK": 0.10, "LBI": 0.15, "LBE": 0.10, "PM": 0.15}
    }
}

PTN_DATA = {
    "klaster_1": {
        "nama": "Klaster 1 - Top Tier",
        "universitas": [
            "Universitas Indonesia (UI)",
            "Universitas Gadjah Mada (UGM)",
            "Universitas Padjadjaran (Unpad)",
            "Institut Teknologi Bandung (ITB)",
            "Institut Pertanian Bogor (IPB)"
        ],
        "skor_aman": (700, 800),
        "warna": "🔴",
        "keterangan": "PTN dengan persaingan paling ketat dan standar tertinggi"
    },
    "klaster_2": {
        "nama": "Klaster 2 - Menengah Atas",
        "universitas": [
            "Universitas Diponegoro (Undip)",
            "Universitas Sebelas Maret (UNS)",
            "Universitas Brawijaya (UB)",
            "Universitas Airlangga (Unair)",
            "Institut Teknologi Sepuluh Nopember (ITS)",
            "Universitas Hasanuddin (Unhas)"
        ],
        "skor_aman": (620, 700),
        "warna": "🟠",
        "keterangan": "PTN favorit dengan standar tinggi"
    },
    "klaster_3": {
        "nama": "Klaster 3 - Menengah",
        "universitas": [
            "Universitas Negeri Yogyakarta (UNY)",
            "Universitas Negeri Semarang (UNNES)",
            "Universitas Negeri Malang (UM)",
            "Universitas Andalas (Unand)",
            "Universitas Sumatera Utara (USU)"
        ],
        "skor_aman": (560, 620),
        "warna": "🟡",
        "keterangan": "PTN dengan standar menengah dan persaingan moderat"
    },
    "klaster_4": {
        "nama": "Klaster 4 - PTN Regional",
        "universitas": [
            "Universitas Sriwijaya (Unsri)",
            "Universitas Lampung (Unila)",
            "Universitas Jember (Unej)",
            "Universitas Riau (Unri)"
        ],
        "skor_aman": (500, 560),
        "warna": "🟢",
        "keterangan": "PTN di luar Jawa dan PTN baru dengan peluang lebih besar"
    }
}

DAFTAR_PTN = [
    "Universitas Indonesia (UI)",
    "Universitas Gadjah Mada (UGM)",
    "Universitas Padjadjaran (Unpad)",
    "Institut Teknologi Bandung (ITB)",
    "Institut Pertanian Bogor (IPB)",
    "Universitas Diponegoro (Undip)",
    "Universitas Sebelas Maret (UNS)",
    "Universitas Brawijaya (UB)",
    "Universitas Airlangga (Unair)",
    "Institut Teknologi Sepuluh Nopember (ITS)",
    "Universitas Hasanuddin (Unhas)",
    "Universitas Negeri Yogyakarta (UNY)",
    "Universitas Negeri Semarang (UNNES)",
    "Universitas Negeri Malang (UM)",
    "Universitas Andalas (Unand)",
    "Universitas Sumatera Utara (USU)",
    "Universitas Sriwijaya (Unsri)",
    "Universitas Lampung (Unila)",
    "Universitas Jember (Unej)",
    "Universitas Riau (Unri)"
]


# ======================================
# FUNGSI PERHITUNGAN
# ======================================

def get_bobot_jurusan(jurusan: str) -> Tuple[Dict, str]:
    for kategori, data in BOBOT_JURUSAN.items():
        if jurusan in data["jurusan"]:
            return data["bobot"], data["label"]
    return BOBOT_JURUSAN["default"]["bobot"], BOBOT_JURUSAN["default"]["label"]


def hitung_skor_akademik(jurusan, PU, PPU, PBM, PK, LBI, LBE, PM):
    bobot, _ = get_bobot_jurusan(jurusan)
    skor = (
        bobot["PU"] * PU + bobot["PPU"] * PPU + bobot["PBM"] * PBM +
        bobot["PK"] * PK + bobot["LBI"] * LBI + bobot["LBE"] * LBE + bobot["PM"] * PM
    )
    return skor


def get_klaster_kampus(kampus: str) -> Dict:
    for klaster_id, data in PTN_DATA.items():
        if kampus in data["universitas"]:
            return {
                "id": klaster_id,
                "nama": data["nama"],
                "skor_min": data["skor_aman"][0],
                "skor_max": data["skor_aman"][1],
                "warna": data["warna"],
                "keterangan": data["keterangan"]
            }
    return {"id": "klaster_3", "nama": "Klaster 3", "skor_min": 560, "skor_max": 620, "warna": "🟡", "keterangan": ""}


def hitung_peluang_lolos(skor_akademik: float, kampus: str) -> Tuple[float, str, str]:
    klaster = get_klaster_kampus(kampus)
    skor_min = klaster["skor_min"]
    skor_max = klaster["skor_max"]

    if skor_akademik >= skor_max:
        peluang = 0.85
        kategori = "Sangat Tinggi"
        keterangan = f"Skor ({skor_akademik:.0f}) di atas batas aman maksimum ({skor_max})"
    elif skor_akademik >= skor_min:
        progress = (skor_akademik - skor_min) / (skor_max - skor_min)
        peluang = 0.65 + (progress * 0.15)
        kategori = "Tinggi"
        keterangan = f"Skor ({skor_akademik:.0f}) dalam zona aman ({skor_min}-{skor_max})"
    elif skor_akademik >= skor_min - 50:
        gap = skor_min - skor_akademik
        peluang = 0.40 + ((50 - gap) / 50 * 0.20)
        kategori = "Sedang"
        keterangan = f"Mendekati zona aman, butuh +{gap:.0f} poin"
    elif skor_akademik >= skor_min - 100:
        gap = skor_min - skor_akademik
        peluang = 0.20 + ((100 - gap) / 100 * 0.15)
        kategori = "Rendah"
        keterangan = f"Masih {gap:.0f} poin di bawah batas aman"
    else:
        peluang = 0.10
        kategori = "Sangat Rendah"
        keterangan = "Butuh peningkatan signifikan"

    return peluang, kategori, keterangan


def analisis_peluang_kampus(skor_akademik: float, kampus: str) -> Dict:
    klaster = get_klaster_kampus(kampus)
    skor_min = klaster["skor_min"]
    skor_max = klaster["skor_max"]
    selisih_min = skor_akademik - skor_min
    selisih_max = skor_akademik - skor_max

    if skor_akademik >= skor_max:
        kategori, warna_status, emoji, persentase = "Sangat Aman", "success", "🎯", 85
        keterangan = f"Skor melampaui batas aman ({skor_max}). Peluang sangat besar!"
    elif skor_akademik >= skor_min:
        kategori, warna_status, emoji, persentase = "Aman", "success", "✅", 70
        keterangan = f"Skor dalam rentang aman ({skor_min}-{skor_max}). Peluang cukup besar!"
    elif skor_akademik >= skor_min - 50:
        kategori, warna_status, emoji, persentase = "Kompetitif", "warning", "⚠️", 50
        keterangan = f"Mendekati batas aman. Butuh {skor_min - skor_akademik:.0f} poin lagi."
    else:
        kategori, warna_status, emoji, persentase = "Perlu Peningkatan", "error", "🔴", 25
        keterangan = f"Masih {skor_min - skor_akademik:.0f} poin di bawah batas aman."

    return {"kategori": kategori, "warna_status": warna_status, "emoji": emoji,
            "persentase": persentase, "keterangan": keterangan,
            "selisih_min": selisih_min, "selisih_max": selisih_max, "klaster": klaster}


def hitung_stabilitas_mental(fokus, percaya_diri, kecemasan, distraksi):
    positif = (fokus * 1.5 + percaya_diri * 1.5) * 10
    negatif = (kecemasan * 1.2 + distraksi * 1.2) * 8
    stabilitas = max(0, min(100, positif - negatif + 50))
    if stabilitas >= 80: return stabilitas, "Sangat Stabil", "Mental sangat siap menghadapi tekanan ujian"
    elif stabilitas >= 65: return stabilitas, "Stabil", "Mental cukup stabil, pertahankan"
    elif stabilitas >= 50: return stabilitas, "Cukup Stabil", "Perlu penguatan mental"
    else: return stabilitas, "Kurang Stabil", "Perlu perhatian serius"


def hitung_indeks_konsistensi(jam_belajar, hari_belajar, latihan_soal, frekuensi_tryout, review_soal):
    skor = (jam_belajar * 2.0 + hari_belajar * 2.2 + latihan_soal * 1.8 +
            frekuensi_tryout * 1.5 + review_soal * 1.5) * 2.0
    konsistensi = min(100, skor)
    if konsistensi >= 80: return konsistensi, "Sangat Konsisten", "Pola belajar sangat mendukung"
    elif konsistensi >= 65: return konsistensi, "Konsisten", "Sudah baik, tingkatkan lagi"
    elif konsistensi >= 50: return konsistensi, "Cukup Konsisten", "Perlu ditingkatkan"
    else: return konsistensi, "Kurang Konsisten", "Pola belajar berisiko"


def hitung_risiko_underperform(stabilitas_mental, konsistensi_belajar):
    skor = (stabilitas_mental * 0.6 + konsistensi_belajar * 0.4)
    if skor >= 75: return "Rendah", "✅", "Kemungkinan perform sesuai/di atas kemampuan"
    elif skor >= 60: return "Sedang", "⚠️", "Ada potensi fluktuasi, jaga konsistensi"
    else: return "Tinggi", "🔴", "Risiko tinggi, perlu perbaikan mental & kebiasaan"


def hitung_skor_kebiasaan_belajar(jam_belajar, hari_belajar, latihan_soal, frekuensi_tryout, review_soal):
    skor = (jam_belajar * 2.0 + hari_belajar * 1.8 + latihan_soal * 1.5 +
            frekuensi_tryout * 1.2 + review_soal * 1.5) * 2.5
    if skor >= 75: return skor, "Excellent", "Pola belajar sangat optimal", "🌟"
    elif skor >= 60: return skor, "Baik", "Sudah cukup baik, tingkatkan konsistensi", "✅"
    elif skor >= 45: return skor, "Cukup", "Perlu ditingkatkan", "⚠️"
    else: return skor, "Perlu Perbaikan", "Perlu perhatian serius", "🔴"


def hitung_risiko(fokus, percaya_diri, kecemasan, distraksi):
    risiko = (kecemasan * 2 + distraksi * 2 + (6 - fokus) * 1.5 + (6 - percaya_diri) * 1.5)
    if risiko >= 20: return risiko, "Tinggi", "sangat berpotensi menurunkan performa"
    elif risiko >= 14: return risiko, "Menengah", "dapat menyebabkan fluktuasi"
    else: return risiko, "Rendah", "mendukung kestabilan performa"


def klasifikasi_profil(fokus, percaya_diri, kecemasan, distraksi):
    if fokus >= 4 and percaya_diri >= 4 and kecemasan <= 2: return "Stabil dan Percaya Diri"
    elif kecemasan >= 4 and percaya_diri <= 3: return "Cenderung Overthinking"
    elif distraksi >= 4: return "Potensial namun Kurang Konsisten"
    elif fokus >= 3 and percaya_diri >= 3: return "Sedang Berkembang"
    else: return "Perlu Penguatan Fundamental"


def prediksi_lgbm(model, input_data):
    try:
        fitur = pd.DataFrame([{
            "Jam_Belajar": input_data["jam_belajar"],
            "Hari_Belajar": input_data["hari_belajar"],
            "Latihan_Soal": input_data["latihan_soal"],
            "Frekuensi_Tryout": input_data["frekuensi_tryout"],
            "Review_Soal": input_data["review_soal"],
            "Fokus": input_data["fokus"],
            "Percaya_Diri": input_data["percaya_diri"],
            "Kecemasan_Rev": 6 - input_data["kecemasan"],
            "Distraksi_Rev": 6 - input_data["distraksi"],
        }])
        if hasattr(model, "feature_name_"): fitur = fitur.reindex(columns=model.feature_name_, fill_value=0)
        elif hasattr(model, "feature_names_in_"): fitur = fitur.reindex(columns=model.feature_names_in_, fill_value=0)
        kode = int(model.predict(fitur)[0])
        label = LABEL_STRATEGI[kode] if kode < len(LABEL_STRATEGI) else "Pertahankan & Tingkatkan"
        proba = model.predict_proba(fitur)[0] if hasattr(model, "predict_proba") else None
        kepercayaan = float(proba[kode]) * 100 if proba is not None else None
        return {"sukses": True, "kode": kode, "strategi": label, "kepercayaan": kepercayaan,
                "probabilitas": proba.tolist() if proba is not None else None,
                "detail": DESKRIPSI_STRATEGI.get(label, {})}
    except Exception as e:
        return {"sukses": False, "error": str(e)}


# ======================================
# CHART FUNCTIONS
# ======================================

def chart_colors():
    return {
        'bg': 'rgba(0,0,0,0)',
        'grid': 'rgba(255,255,255,0.1)',
        'text': '#e2e8f0',
        'subtext': '#a0aec0',
        'blue': '#4299e1',
        'purple': '#9f7aea',
        'green': '#48bb78',
        'orange': '#ed8936',
        'red': '#fc8181',
        'yellow': '#f6e05e',
    }


def buat_radar_chart(skor_subtes: Dict, bobot: Dict, jurusan: str) -> go.Figure:
    """Radar chart untuk skor TPS"""
    c = chart_colors()
    labels = list(SUBTES_LABELS.values())
    keys = list(SUBTES_LABELS.keys())

    nilai = [skor_subtes[k] for k in keys]
    bobot_scaled = [bobot[k] * SKOR_MAX_UTBK for k in keys]

    fig = go.Figure()

    # Bobot target (sebagai referensi)
    fig.add_trace(go.Scatterpolar(
        r=bobot_scaled,
        theta=labels,
        fill='toself',
        name=f'Bobot Target ({jurusan})',
        line=dict(color=c['purple'], width=2),
        fillcolor='rgba(159, 122, 234, 0.15)',
        marker=dict(size=6)
    ))

    # Skor aktual
    fig.add_trace(go.Scatterpolar(
        r=nilai,
        theta=labels,
        fill='toself',
        name='Skor Kamu',
        line=dict(color=c['blue'], width=3),
        fillcolor='rgba(66, 153, 225, 0.25)',
        marker=dict(size=8, color=c['blue'])
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True, range=[0, SKOR_MAX_UTBK],
                gridcolor=c['grid'], tickfont=dict(color=c['subtext'], size=10),
                tickvals=[200, 400, 600, 800, 1000]
            ),
            angularaxis=dict(tickfont=dict(color=c['text'], size=11))
        ),
        showlegend=True,
        legend=dict(
            bgcolor='rgba(0,0,0,0.3)', bordercolor='rgba(255,255,255,0.2)',
            borderwidth=1, font=dict(color=c['text'], size=11)
        ),
        paper_bgcolor=c['bg'],
        plot_bgcolor=c['bg'],
        title=dict(text=f"📡 Profil TPS vs Bobot Jurusan {jurusan}", font=dict(color=c['text'], size=14)),
        margin=dict(l=40, r=40, t=60, b=40),
        height=420
    )
    return fig


def buat_bar_skor_subtes(skor_subtes: Dict, bobot: Dict) -> go.Figure:
    """Bar chart perbandingan skor subtes dengan bobot"""
    c = chart_colors()
    keys = list(SUBTES_LABELS.keys())
    labels = [k for k in keys]
    nilai = [skor_subtes[k] for k in keys]
    bobot_vals = [bobot[k] * 100 for k in keys]  # dalam %

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Bar skor
    fig.add_trace(go.Bar(
        name='Skor Subtes',
        x=labels, y=nilai,
        marker=dict(
            color=[f'rgba(66,153,225,{0.6 + (v/SKOR_MAX_UTBK)*0.4})' for v in nilai],
            line=dict(color='rgba(99,179,237,0.8)', width=1)
        ),
        text=[f"{v}" for v in nilai],
        textposition='outside',
        textfont=dict(color=c['text'], size=11, family='Inter'),
    ), secondary_y=False)

    # Line bobot
    fig.add_trace(go.Scatter(
        name='Bobot Jurusan (%)',
        x=labels, y=bobot_vals,
        mode='lines+markers+text',
        line=dict(color=c['orange'], width=3, dash='dash'),
        marker=dict(size=10, color=c['orange'], symbol='diamond'),
        text=[f"{v:.0f}%" for v in bobot_vals],
        textposition='top center',
        textfont=dict(color=c['orange'], size=10)
    ), secondary_y=True)

    fig.update_xaxes(
        tickfont=dict(color=c['text'], size=11),
        gridcolor=c['grid']
    )
    fig.update_yaxes(
        title_text="Skor (0-1000)", secondary_y=False,
        range=[0, SKOR_MAX_UTBK + 100],
        tickfont=dict(color=c['text']), gridcolor=c['grid'],
        title_font=dict(color=c['subtext'])
    )
    fig.update_yaxes(
        title_text="Bobot Jurusan (%)", secondary_y=True,
        range=[0, 60], ticksuffix="%",
        tickfont=dict(color=c['orange']),
        title_font=dict(color=c['orange']),
        showgrid=False
    )
    fig.update_layout(
        paper_bgcolor=c['bg'], plot_bgcolor=c['bg'],
        legend=dict(bgcolor='rgba(0,0,0,0.3)', bordercolor='rgba(255,255,255,0.2)',
                    borderwidth=1, font=dict(color=c['text'])),
        title=dict(text="📊 Skor Subtes & Bobot Jurusan", font=dict(color=c['text'], size=14)),
        margin=dict(l=10, r=10, t=60, b=10),
        height=380,
        bargap=0.3
    )
    return fig


def buat_bar_peluang_kampus(skor_akademik: float) -> go.Figure:
    """Bar chart perbandingan skor vs semua klaster"""
    c = chart_colors()
    
    kampus_list = []
    skor_min_list = []
    skor_max_list = []
    warna_list = []
    color_map = {"klaster_1": c['red'], "klaster_2": c['orange'],
                 "klaster_3": c['yellow'], "klaster_4": c['green']}

    for kid, kdata in PTN_DATA.items():
        for univ in kdata["universitas"]:
            kampus_list.append(univ.split("(")[0].strip()[:20])
            skor_min_list.append(kdata["skor_aman"][0])
            skor_max_list.append(kdata["skor_aman"][1])
            warna_list.append(color_map[kid])

    fig = go.Figure()

    # Range skor aman (min to max)
    fig.add_trace(go.Bar(
        name='Rentang Skor Aman',
        x=kampus_list,
        y=[mx - mn for mx, mn in zip(skor_max_list, skor_min_list)],
        base=skor_min_list,
        marker=dict(color=[w.replace(')', ',0.3)').replace('rgb', 'rgba') for w in warna_list],
                    line=dict(color=warna_list, width=1)),
        text=[f"{mn}-{mx}" for mn, mx in zip(skor_min_list, skor_max_list)],
        textposition='inside',
        textfont=dict(size=9, color='rgba(255,255,255,0.8)'),
        hovertemplate='%{x}<br>Zona Aman: %{base} - %{y}<extra></extra>'
    ))

    # Garis skor kamu
    fig.add_hline(
        y=skor_akademik, line_dash="solid",
        line_color=c['blue'], line_width=3,
        annotation_text=f"Skor Kamu: {skor_akademik:.0f}",
        annotation_font_color=c['blue'],
        annotation_font_size=12,
        annotation_bgcolor='rgba(66,153,225,0.2)'
    )

    fig.update_layout(
        paper_bgcolor=c['bg'], plot_bgcolor=c['bg'],
        xaxis=dict(tickfont=dict(color=c['text'], size=9), tickangle=-45,
                   gridcolor=c['grid']),
        yaxis=dict(tickfont=dict(color=c['text']), gridcolor=c['grid'],
                   title_text="Skor UTBK (0-1000)", title_font=dict(color=c['subtext']),
                   range=[400, 1000]),
        title=dict(text="🏛️ Posisi Skor vs Zona Aman Semua PTN", font=dict(color=c['text'], size=14)),
        legend=dict(bgcolor='rgba(0,0,0,0.3)', font=dict(color=c['text'])),
        margin=dict(l=10, r=10, t=60, b=100),
        height=420
    )
    return fig


def buat_gauge_chart(nilai: float, judul: str, min_val=0, max_val=100) -> go.Figure:
    c = chart_colors()
    pct = (nilai - min_val) / (max_val - min_val) * 100
    
    if pct >= 70: color = c['green']
    elif pct >= 50: color = c['yellow']
    else: color = c['red']
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=nilai,
        title={'text': judul, 'font': {'color': c['text'], 'size': 13}},
        number={'font': {'color': c['text'], 'size': 28}, 'suffix': ""},
        gauge={
            'axis': {'range': [min_val, max_val], 'tickcolor': c['subtext'],
                     'tickfont': {'color': c['subtext'], 'size': 10}},
            'bar': {'color': color, 'thickness': 0.75},
            'bgcolor': 'rgba(255,255,255,0.05)',
            'borderwidth': 0,
            'steps': [
                {'range': [min_val, min_val + (max_val-min_val)*0.4], 'color': 'rgba(252,129,129,0.15)'},
                {'range': [min_val + (max_val-min_val)*0.4, min_val + (max_val-min_val)*0.7], 'color': 'rgba(246,224,94,0.15)'},
                {'range': [min_val + (max_val-min_val)*0.7, max_val], 'color': 'rgba(72,187,120,0.15)'},
            ],
            'threshold': {
                'line': {'color': "white", 'width': 2},
                'thickness': 0.85,
                'value': nilai
            }
        }
    ))
    fig.update_layout(
        paper_bgcolor=c['bg'], plot_bgcolor=c['bg'],
        margin=dict(l=20, r=20, t=40, b=20),
        height=220,
        font=dict(family='Inter')
    )
    return fig


def buat_pipeline_subtes(skor_subtes: Dict, bobot: Dict) -> go.Figure:
    """Pipeline comparison: skor aktual vs kontribusi tertimbang"""
    c = chart_colors()
    keys = list(SUBTES_LABELS.keys())
    labels = [SUBTES_LABELS[k] for k in keys]
    
    skor_raw = [skor_subtes[k] for k in keys]
    kontribusi = [skor_subtes[k] * bobot[k] for k in keys]
    bobot_pct = [bobot[k] * 100 for k in keys]
    
    # Sort by kontribusi descending
    sorted_data = sorted(zip(labels, skor_raw, kontribusi, bobot_pct), key=lambda x: x[2], reverse=True)
    labels_s, skor_s, kontrib_s, bobot_s = zip(*sorted_data)

    fig = go.Figure()
    
    # Kontribusi bar (horizontal)
    fig.add_trace(go.Bar(
        y=list(labels_s),
        x=list(kontrib_s),
        orientation='h',
        name='Kontribusi Tertimbang',
        marker=dict(
            color=[f'rgba(99,179,237,{0.4 + (k/max(kontrib_s))*0.6})' for k in kontrib_s],
            line=dict(color='rgba(99,179,237,0.9)', width=1.5)
        ),
        text=[f"  {v:.0f} pts ({b:.0f}% bobot)" for v, b in zip(kontrib_s, bobot_s)],
        textposition='outside',
        textfont=dict(color=c['text'], size=10),
        hovertemplate='%{y}<br>Kontribusi: %{x:.1f}<br><extra></extra>'
    ))

    fig.update_layout(
        paper_bgcolor=c['bg'], plot_bgcolor=c['bg'],
        xaxis=dict(tickfont=dict(color=c['subtext'], size=10), gridcolor=c['grid'],
                   title_text="Kontribusi Skor (Skor × Bobot)", title_font=dict(color=c['subtext'])),
        yaxis=dict(tickfont=dict(color=c['text'], size=11), gridcolor='rgba(0,0,0,0)'),
        title=dict(text="🔀 Pipeline: Kontribusi Tertimbang Setiap Subtes", font=dict(color=c['text'], size=14)),
        margin=dict(l=10, r=120, t=60, b=20),
        height=360,
        showlegend=False
    )
    return fig


def buat_bar_kebiasaan(data: Dict) -> go.Figure:
    """Bar chart kebiasaan belajar"""
    c = chart_colors()
    
    labels = ["Jam Belajar", "Hari/Minggu", "Latihan Soal", "Tryout/Bulan", "Review Soal"]
    nilai = [data['jam_belajar'], data['hari_belajar'], data['latihan_soal'],
             data['frekuensi_tryout'], data['review_soal']]
    
    bar_colors = [c['green'] if v >= 4 else c['yellow'] if v >= 3 else c['red'] for v in nilai]

    fig = go.Figure(go.Bar(
        x=labels, y=nilai,
        marker=dict(color=[c.replace(')', ',0.8)').replace('rgb', 'rgba') for c in bar_colors],
                    line=dict(color=bar_colors, width=1.5)),
        text=[f"{v}/5" for v in nilai],
        textposition='outside',
        textfont=dict(color=c['text'], size=12)
    ))

    # Target line
    fig.add_hline(y=4, line_dash="dash", line_color=c['green'], line_width=2,
                  annotation_text="Target Ideal (4/5)",
                  annotation_font_color=c['green'])

    fig.update_layout(
        paper_bgcolor=c['bg'], plot_bgcolor=c['bg'],
        xaxis=dict(tickfont=dict(color=c['text'], size=11), gridcolor=c['grid']),
        yaxis=dict(tickfont=dict(color=c['text']), gridcolor=c['grid'],
                   range=[0, 6], title_text="Level (1-5)", title_font=dict(color=c['subtext'])),
        title=dict(text="📚 Level Kebiasaan Belajar", font=dict(color=c['text'], size=14)),
        margin=dict(l=10, r=10, t=60, b=20),
        height=300,
        showlegend=False,
        bargap=0.3
    )
    return fig


# ======================================
# PDF EXPORT
# ======================================

def generate_pdf_html(data: Dict) -> str:
    """Generate HTML untuk PDF export"""
    bobot, label_kel = get_bobot_jurusan(data['jurusan'])
    klaster = get_klaster_kampus(data['kampus'])
    peluang_pct = data['peluang'] * 100
    
    subtes_rows = ""
    for k, label in SUBTES_LABELS.items():
        skor = data[k]
        bw = bobot[k] * 100
        kontrib = skor * bobot[k]
        bar_w = int(skor / SKOR_MAX_UTBK * 100)
        subtes_rows += f"""
        <tr>
            <td>{label} ({k})</td>
            <td><div style="background:#e2e8f0;border-radius:4px;height:10px;">
                <div style="background:#4299e1;width:{bar_w}%;height:10px;border-radius:4px;"></div>
            </div></td>
            <td style="text-align:center;font-weight:600;">{skor}</td>
            <td style="text-align:center;">{bw:.0f}%</td>
            <td style="text-align:center;color:#4299e1;font-weight:600;">{kontrib:.1f}</td>
        </tr>"""

    now = datetime.datetime.now().strftime("%d %B %Y, %H:%M")
    
    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
  body {{ font-family: Arial, sans-serif; color: #1a202c; padding: 30px; }}
  h1 {{ color: #2d3748; border-bottom: 3px solid #4299e1; padding-bottom: 10px; }}
  h2 {{ color: #4299e1; font-size: 1rem; margin-top: 20px; text-transform: uppercase; letter-spacing: 1px; }}
  .header {{ background: linear-gradient(135deg, #1a365d, #2a4a8a); color: white; padding: 20px 30px; border-radius: 12px; margin-bottom: 20px; }}
  .header h1 {{ color: white; border-bottom: 1px solid rgba(255,255,255,0.3); }}
  .grid2 {{ display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin: 16px 0; }}
  .card {{ background: #f7fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 16px; }}
  .card-label {{ color: #718096; font-size: 0.8rem; font-weight: 600; text-transform: uppercase; }}
  .card-value {{ font-size: 1.8rem; font-weight: 800; color: #2d3748; }}
  .card-sub {{ color: #a0aec0; font-size: 0.8rem; }}
  .green {{ color: #38a169; }} .orange {{ color: #dd6b20; }} .red {{ color: #e53e3e; }}
  table {{ width: 100%; border-collapse: collapse; margin: 12px 0; }}
  th {{ background: #2d3748; color: white; padding: 10px; text-align: left; font-size: 0.85rem; }}
  td {{ padding: 8px 10px; border-bottom: 1px solid #e2e8f0; font-size: 0.85rem; }}
  tr:nth-child(even) {{ background: #f7fafc; }}
  .badge {{ display: inline-block; padding: 2px 10px; border-radius: 12px; font-size: 0.75rem; font-weight: 600; }}
  .badge-green {{ background: #c6f6d5; color: #276749; }}
  .badge-orange {{ background: #feebc8; color: #9c4221; }}
  .badge-red {{ background: #fed7d7; color: #9b2c2c; }}
  .footer {{ color: #a0aec0; font-size: 0.75rem; text-align: center; margin-top: 30px; border-top: 1px solid #e2e8f0; padding-top: 16px; }}
</style>
</head>
<body>
<div class="header">
  <h1>🎯 AI UTBK Readiness Report</h1>
  <p style="margin:0;opacity:0.8;">Digenerate: {now}</p>
</div>

<h2>📋 Profil Siswa</h2>
<div class="grid2">
  <div class="card"><div class="card-label">Nama</div><div class="card-value" style="font-size:1.2rem;">{data.get('nama','—')}</div></div>
  <div class="card"><div class="card-label">Target Jurusan</div><div class="card-value" style="font-size:1.1rem;">{data['jurusan']}</div><div class="card-sub">{label_kel}</div></div>
  <div class="card"><div class="card-label">Target Kampus</div><div class="card-value" style="font-size:1rem;">{data['kampus']}</div><div class="card-sub">{klaster['nama']}</div></div>
  <div class="card"><div class="card-label">Zona Aman Kampus</div><div class="card-value" style="font-size:1.2rem;">{klaster['skor_min']} – {klaster['skor_max']}</div></div>
</div>

<h2>📊 Ringkasan Metrik Utama</h2>
<div class="grid2">
  <div class="card"><div class="card-label">Skor Akademik Tertimbang</div>
    <div class="card-value {'green' if data['akademik'] >= klaster['skor_max'] else 'orange' if data['akademik'] >= klaster['skor_min'] else 'red'}">{data['akademik']:.0f}</div>
    <div class="card-sub">dari {SKOR_MAX_UTBK}</div></div>
  <div class="card"><div class="card-label">Peluang Lolos</div>
    <div class="card-value {'green' if peluang_pct >= 65 else 'orange' if peluang_pct >= 40 else 'red'}">{peluang_pct:.0f}%</div>
    <div class="card-sub">{data['peluang_kategori']}</div></div>
  <div class="card"><div class="card-label">Stabilitas Mental</div>
    <div class="card-value {'green' if data['stabilitas'] >= 65 else 'orange' if data['stabilitas'] >= 50 else 'red'}">{data['stabilitas']:.0f}%</div>
    <div class="card-sub">{data['stabilitas_kategori']}</div></div>
  <div class="card"><div class="card-label">Konsistensi Belajar</div>
    <div class="card-value {'green' if data['konsistensi'] >= 65 else 'orange' if data['konsistensi'] >= 50 else 'red'}">{data['konsistensi']:.0f}%</div>
    <div class="card-sub">{data['konsistensi_kategori']}</div></div>
</div>

<h2>📈 Detail Skor TPS & Bobot Jurusan</h2>
<table>
  <tr><th>Subtes</th><th>Progress</th><th>Skor</th><th>Bobot</th><th>Kontribusi</th></tr>
  {subtes_rows}
</table>

<h2>🧠 Analisis Psikologi & Kebiasaan</h2>
<table>
  <tr><th>Aspek</th><th>Nilai</th><th>Keterangan</th></tr>
  <tr><td>Fokus</td><td>{data['fokus']}/5</td><td>{'Sangat baik' if data['fokus']>=4 else 'Cukup' if data['fokus']>=3 else 'Perlu ditingkatkan'}</td></tr>
  <tr><td>Percaya Diri</td><td>{data['percaya_diri']}/5</td><td>{'Kuat' if data['percaya_diri']>=4 else 'Cukup' if data['percaya_diri']>=3 else 'Perlu penguatan'}</td></tr>
  <tr><td>Kecemasan</td><td>{data['kecemasan']}/5</td><td>{'Tinggi – perlu manajemen stres' if data['kecemasan']>=4 else 'Moderat' if data['kecemasan']>=3 else 'Terkendali'}</td></tr>
  <tr><td>Distraksi</td><td>{data['distraksi']}/5</td><td>{'Tinggi – perlu fokus lingkungan' if data['distraksi']>=4 else 'Moderat' if data['distraksi']>=3 else 'Rendah'}</td></tr>
  <tr><td>Jam Belajar/hari</td><td>Level {data['jam_belajar']}/5</td><td>{'Sangat baik' if data['jam_belajar']>=4 else 'Cukup' if data['jam_belajar']>=3 else 'Perlu ditingkatkan'}</td></tr>
  <tr><td>Hari Belajar/minggu</td><td>Level {data['hari_belajar']}/5</td><td>{'Sangat konsisten' if data['hari_belajar']>=4 else 'Cukup' if data['hari_belajar']>=3 else 'Kurang konsisten'}</td></tr>
  <tr><td>Latihan Soal/minggu</td><td>Level {data['latihan_soal']}/5</td><td>{'Intensif' if data['latihan_soal']>=4 else 'Cukup' if data['latihan_soal']>=3 else 'Perlu ditingkatkan'}</td></tr>
  <tr><td>Tryout/bulan</td><td>Level {data['frekuensi_tryout']}/5</td><td>{'Sangat rutin' if data['frekuensi_tryout']>=4 else 'Cukup' if data['frekuensi_tryout']>=3 else 'Perlu lebih sering'}</td></tr>
  <tr><td>Review Soal/minggu</td><td>Level {data['review_soal']}/5</td><td>{'Sangat baik' if data['review_soal']>=4 else 'Cukup' if data['review_soal']>=3 else 'Perlu ditingkatkan'}</td></tr>
</table>

<h2>🎯 Kesimpulan & Rekomendasi</h2>
<div class="card">
  <p><strong>Status Peluang:</strong> {data['peluang_kategori']} ({peluang_pct:.0f}%)</p>
  <p><strong>Profil Belajar:</strong> {klasifikasi_profil(data['fokus'],data['percaya_diri'],data['kecemasan'],data['distraksi'])}</p>
  <p><strong>Risiko Underperform:</strong> {data['risiko_level']} {data['risiko_emoji']}</p>
  <p>{data['peluang_keterangan']}</p>
</div>

<div class="footer">
  🤖 AI UTBK Readiness Dashboard • Dibuat dengan Streamlit & Python<br>
  Hasil analisis bersifat indikatif berdasarkan data yang diinput. Performa aktual bergantung pada persiapan dan kondisi hari H.
</div>
</body></html>"""


# ======================================
# PAGE: SURVEY (Multi-step)
# ======================================

def render_survey_page():
    """Multi-page survey form"""
    
    if 'survey_step' not in st.session_state:
        st.session_state.survey_step = 1
    
    # Header
    st.markdown("""
    <div style="text-align:center; padding: 20px 0;">
        <h1 style="color:#e2e8f0; font-size:2.2rem; font-weight:800;">🎯 AI UTBK Dashboard</h1>
        <p style="color:#a0aec0; font-size:1rem;">Isi survey untuk mendapatkan analisis kesiapan UTBK kamu</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Step progress
    steps = ["👤 Profil", "📊 Skor TPS", "🧠 Psikologi", "📚 Kebiasaan"]
    step = st.session_state.survey_step
    
    cols = st.columns(4)
    for i, (col, label) in enumerate(zip(cols, steps), 1):
        with col:
            if i < step:
                st.markdown(f"""<div style="text-align:center;">
                    <div style="background:linear-gradient(135deg,#4299e1,#9f7aea);color:white;width:40px;height:40px;border-radius:50%;display:flex;align-items:center;justify-content:center;margin:0 auto;font-weight:700;font-size:1.1rem;">✓</div>
                    <p style="color:#4299e1;font-size:0.8rem;margin-top:4px;font-weight:600;">{label}</p>
                </div>""", unsafe_allow_html=True)
            elif i == step:
                st.markdown(f"""<div style="text-align:center;">
                    <div style="background:linear-gradient(135deg,#4299e1,#9f7aea);color:white;width:40px;height:40px;border-radius:50%;display:flex;align-items:center;justify-content:center;margin:0 auto;font-weight:700;font-size:1rem;">{i}</div>
                    <p style="color:#e2e8f0;font-size:0.8rem;margin-top:4px;font-weight:700;">{label}</p>
                </div>""", unsafe_allow_html=True)
            else:
                st.markdown(f"""<div style="text-align:center;">
                    <div style="background:rgba(255,255,255,0.1);color:#a0aec0;width:40px;height:40px;border-radius:50%;display:flex;align-items:center;justify-content:center;margin:0 auto;font-weight:700;font-size:1rem;">{i}</div>
                    <p style="color:#718096;font-size:0.8rem;margin-top:4px;">{label}</p>
                </div>""", unsafe_allow_html=True)
    
    # Progress bar
    pct = (step - 1) / 3 * 100
    st.markdown(f"""
    <div style="margin: 16px 0 24px;">
        <div style="background:rgba(255,255,255,0.1);border-radius:10px;height:8px;overflow:hidden;">
            <div style="background:linear-gradient(90deg,#4299e1,#9f7aea);width:{pct}%;height:8px;border-radius:10px;transition:width 0.5s;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # ===== STEP 1: PROFIL =====
    if step == 1:
        st.markdown("### 👤 Step 1: Profil Siswa")
        st.markdown("<p style='color:#a0aec0;'>Masukkan data pribadi dan target kamu</p>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            nama = st.text_input("📝 Nama Lengkap", value=st.session_state.get('nama', ''), 
                                  placeholder="Masukkan nama kamu...")
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            st.info("💡 Nama akan digunakan untuk personalisasi analisis")
        
        jurusan = st.selectbox("🎓 Target Jurusan", DAFTAR_JURUSAN,
                                index=DAFTAR_JURUSAN.index(st.session_state.get('jurusan', DAFTAR_JURUSAN[0])))
        
        kampus = st.selectbox("🏛️ Target Kampus (PTN)", DAFTAR_PTN,
                               index=DAFTAR_PTN.index(st.session_state.get('kampus', DAFTAR_PTN[0])))
        
        # Tampilkan info klaster
        klaster = get_klaster_kampus(kampus)
        bobot_j, label_kel = get_bobot_jurusan(jurusan)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div class="info-box">
                <p style="color:#63b3ed;font-weight:600;margin-bottom:4px;">{klaster['warna']} {klaster['nama']}</p>
                <p style="color:#a0aec0;font-size:0.85rem;margin:0;">{klaster['keterangan']}</p>
                <p style="color:#e2e8f0;font-weight:700;margin-top:8px;font-size:1.1rem;">
                    Zona Aman: {klaster['skor_min']} – {klaster['skor_max']}
                </p>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="info-box">
                <p style="color:#63b3ed;font-weight:600;margin-bottom:4px;">📚 {label_kel}</p>
                <p style="color:#a0aec0;font-size:0.85rem;margin-bottom:6px;">Bobot subtes utama:</p>
                {''.join([f'<span style="background:rgba(99,179,237,0.2);color:#e2e8f0;padding:2px 8px;border-radius:8px;font-size:0.8rem;margin:2px;display:inline-block;">{k}: {v*100:.0f}%</span>' for k,v in sorted(bobot_j.items(), key=lambda x:-x[1])[:3]])}
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Lanjut ke Skor TPS →", type="primary", use_container_width=True):
            st.session_state.nama = nama
            st.session_state.jurusan = jurusan
            st.session_state.kampus = kampus
            st.session_state.survey_step = 2
            st.rerun()
    
    # ===== STEP 2: SKOR TPS =====
    elif step == 2:
        st.markdown("### 📊 Step 2: Skor TPS (Try Out / Prediksi)")
        st.markdown(f"<p style='color:#a0aec0;'>Skor berdasarkan skala UTBK 2024 (0–{SKOR_MAX_UTBK})</p>", unsafe_allow_html=True)
        
        bobot_j, label_kel = get_bobot_jurusan(st.session_state.get('jurusan', DAFTAR_JURUSAN[0]))
        
        # Tampilkan bobot referensi
        with st.expander("📋 Lihat Bobot Subtes untuk Jurusan Kamu", expanded=True):
            cols = st.columns(7)
            for i, (k, v) in enumerate(bobot_j.items()):
                with cols[i]:
                    st.metric(k, f"{v*100:.0f}%")
        
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            PU = st.slider(f"🧠 Penalaran Umum (PU) — Bobot {bobot_j['PU']*100:.0f}%",
                           0, SKOR_MAX_UTBK, st.session_state.get('PU', 550))
            PPU = st.slider(f"📖 Pemahaman & Penulisan Umum (PPU) — Bobot {bobot_j['PPU']*100:.0f}%",
                            0, SKOR_MAX_UTBK, st.session_state.get('PPU', 550))
            PBM = st.slider(f"📝 Pemahaman Bacaan & Menulis (PBM) — Bobot {bobot_j['PBM']*100:.0f}%",
                            0, SKOR_MAX_UTBK, st.session_state.get('PBM', 550))
            PK = st.slider(f"🔢 Pengetahuan Kuantitatif (PK) — Bobot {bobot_j['PK']*100:.0f}%",
                           0, SKOR_MAX_UTBK, st.session_state.get('PK', 550))
        
        with col2:
            LBI = st.slider(f"🇮🇩 Literasi Bahasa Indonesia (LBI) — Bobot {bobot_j['LBI']*100:.0f}%",
                            0, SKOR_MAX_UTBK, st.session_state.get('LBI', 550))
            LBE = st.slider(f"🇺🇸 Literasi Bahasa Inggris (LBE) — Bobot {bobot_j['LBE']*100:.0f}%",
                            0, SKOR_MAX_UTBK, st.session_state.get('LBE', 550))
            PM = st.slider(f"📐 Penalaran Matematika (PM) — Bobot {bobot_j['PM']*100:.0f}%",
                           0, SKOR_MAX_UTBK, st.session_state.get('PM', 550))
        
        # Preview skor
        skor_preview = hitung_skor_akademik(
            st.session_state.get('jurusan', DAFTAR_JURUSAN[0]),
            PU, PPU, PBM, PK, LBI, LBE, PM
        )
        klaster = get_klaster_kampus(st.session_state.get('kampus', DAFTAR_PTN[0]))
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Skor Rata-rata", f"{(PU+PPU+PBM+PK+LBI+LBE+PM)/7:.0f}")
        with col2:
            color_score = "normal" if skor_preview >= klaster['skor_min'] else "inverse"
            st.metric("Skor Tertimbang", f"{skor_preview:.0f}", 
                      delta=f"{skor_preview - klaster['skor_min']:+.0f} dari min aman")
        with col3:
            st.metric("Zona Aman Target", f"{klaster['skor_min']}–{klaster['skor_max']}")
        
        c1, c2 = st.columns(2)
        with c1:
            if st.button("← Kembali", use_container_width=True):
                st.session_state.survey_step = 1
                st.rerun()
        with c2:
            if st.button("Lanjut ke Psikologi →", type="primary", use_container_width=True):
                st.session_state.PU = PU
                st.session_state.PPU = PPU
                st.session_state.PBM = PBM
                st.session_state.PK = PK
                st.session_state.LBI = LBI
                st.session_state.LBE = LBE
                st.session_state.PM = PM
                st.session_state.survey_step = 3
                st.rerun()
    
    # ===== STEP 3: PSIKOLOGI =====
    elif step == 3:
        st.markdown("### 🧠 Step 3: Kondisi Psikologi")
        st.markdown("<p style='color:#a0aec0;'>Jawab dengan jujur — tidak ada jawaban benar/salah</p>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**😎 Faktor Positif**")
            fokus = st.slider("Tingkat Fokus Belajar", 1, 5, st.session_state.get('fokus', 3),
                              help="1 = Sangat sulit fokus, 5 = Sangat mudah fokus")
            percaya_diri = st.slider("Tingkat Percaya Diri", 1, 5, st.session_state.get('percaya_diri', 3),
                                     help="1 = Sangat tidak yakin, 5 = Sangat yakin")
            
            # Visual indicator
            total_positif = (fokus + percaya_diri) / 10 * 100
            st.markdown(f"""
            <div style="margin-top:12px;">
                <p style="color:#a0aec0;font-size:0.8rem;">Skor Positif: {total_positif:.0f}%</p>
                <div style="background:rgba(255,255,255,0.1);border-radius:6px;height:8px;">
                    <div style="background:linear-gradient(90deg,#48bb78,#68d391);width:{total_positif}%;height:8px;border-radius:6px;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("**😰 Faktor Tantangan**")
            kecemasan = st.slider("Tingkat Kecemasan Ujian", 1, 5, st.session_state.get('kecemasan', 3),
                                  help="1 = Tidak cemas, 5 = Sangat cemas")
            distraksi = st.slider("Tingkat Distraksi", 1, 5, st.session_state.get('distraksi', 3),
                                  help="1 = Tidak mudah terdistraksi, 5 = Sangat mudah terdistraksi")
            
            total_negatif = (kecemasan + distraksi) / 10 * 100
            st.markdown(f"""
            <div style="margin-top:12px;">
                <p style="color:#a0aec0;font-size:0.8rem;">Level Tantangan: {total_negatif:.0f}%</p>
                <div style="background:rgba(255,255,255,0.1);border-radius:6px;height:8px;">
                    <div style="background:linear-gradient(90deg,#fc8181,#feb2b2);width:{total_negatif}%;height:8px;border-radius:6px;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Preview stabilitas
        stab, stab_kat, _ = hitung_stabilitas_mental(fokus, percaya_diri, kecemasan, distraksi)
        color = "#48bb78" if stab >= 65 else "#f6e05e" if stab >= 50 else "#fc8181"
        st.markdown(f"""
        <div class="info-box" style="margin-top:16px;">
            <p style="color:#a0aec0;margin:0;font-size:0.85rem;">Preview Stabilitas Mental:</p>
            <p style="color:{color};font-size:1.5rem;font-weight:800;margin:4px 0;">{stab:.0f}% — {stab_kat}</p>
        </div>
        """, unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1:
            if st.button("← Kembali", use_container_width=True):
                st.session_state.survey_step = 2
                st.rerun()
        with c2:
            if st.button("Lanjut ke Kebiasaan →", type="primary", use_container_width=True):
                st.session_state.fokus = fokus
                st.session_state.percaya_diri = percaya_diri
                st.session_state.kecemasan = kecemasan
                st.session_state.distraksi = distraksi
                st.session_state.survey_step = 4
                st.rerun()
    
    # ===== STEP 4: KEBIASAAN =====
    elif step == 4:
        st.markdown("### 📚 Step 4: Kebiasaan Belajar")
        st.markdown("<p style='color:#a0aec0;'>Ceritakan rutinitas belajar kamu saat ini</p>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            jam_belajar_str = st.selectbox("⏰ Rata-rata jam belajar per hari",
                ["<1 jam", "1-2 jam", "3-4 jam", "5-6 jam", ">6 jam"],
                index=st.session_state.get('jam_belajar', 2) - 1)
            map_jam = {"<1 jam": 1, "1-2 jam": 2, "3-4 jam": 3, "5-6 jam": 4, ">6 jam": 5}
            Jam_Belajar = map_jam[jam_belajar_str]
            
            hari_belajar_str = st.selectbox("📅 Hari belajar per minggu",
                ["≤1 hari", "2 hari", "3 hari", "4-5 hari", "≥6 hari"],
                index=st.session_state.get('hari_belajar', 2) - 1)
            map_hari = {"≤1 hari": 1, "2 hari": 2, "3 hari": 3, "4-5 hari": 4, "≥6 hari": 5}
            Hari_Belajar = map_hari[hari_belajar_str]
            
            Latihan_Soal = st.slider("📋 Latihan soal per minggu (sesi)", 1, 5,
                                      st.session_state.get('latihan_soal', 2))
        
        with col2:
            Frekuensi_Tryout = st.slider("🏆 Tryout per bulan", 1, 5,
                                          st.session_state.get('frekuensi_tryout', 2))
            
            review_str = st.selectbox("🔍 Review soal per minggu",
                ["≤1 kali", "2 kali", "3 kali", "4-5 kali", "≥6 kali"],
                index=st.session_state.get('review_soal', 2) - 1)
            Review_Soal = map_hari.get(review_str.replace(" kali", " hari").replace("≤1 kali", "≤1 hari")
                          .replace("≥6 kali", "≥6 hari"), 2)
            
            skor_keb, kat_keb, _, emoji_keb = hitung_skor_kebiasaan_belajar(
                Jam_Belajar, Hari_Belajar, Latihan_Soal, Frekuensi_Tryout, Review_Soal)
            
            color_keb = "#48bb78" if skor_keb >= 65 else "#f6e05e" if skor_keb >= 45 else "#fc8181"
            st.markdown(f"""
            <div class="info-box" style="margin-top:8px;">
                <p style="color:#a0aec0;margin:0;font-size:0.85rem;">Preview Skor Kebiasaan:</p>
                <p style="color:{color_keb};font-size:1.8rem;font-weight:800;margin:4px 0;">{emoji_keb} {skor_keb:.0f}/100</p>
                <p style="color:#e2e8f0;font-size:0.85rem;margin:0;font-weight:600;">{kat_keb}</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1:
            if st.button("← Kembali", use_container_width=True):
                st.session_state.survey_step = 3
                st.rerun()
        with c2:
            if st.button("🚀 LIHAT HASIL ANALISIS!", type="primary", use_container_width=True):
                st.session_state.jam_belajar = Jam_Belajar
                st.session_state.hari_belajar = Hari_Belajar
                st.session_state.latihan_soal = Latihan_Soal
                st.session_state.frekuensi_tryout = Frekuensi_Tryout
                st.session_state.review_soal = Review_Soal
                st.session_state.survey_done = True
                st.session_state.page = 'dashboard'
                st.rerun()


# ======================================
# PAGE: DASHBOARD
# ======================================

def render_dashboard_page(lgbm_model, lgbm_tersedia):
    """Render hasil analisis dashboard"""
    
    # Ambil data dari session state
    input_data = {
        'nama': st.session_state.get('nama', ''),
        'jurusan': st.session_state.get('jurusan', DAFTAR_JURUSAN[0]),
        'kampus': st.session_state.get('kampus', DAFTAR_PTN[0]),
        'PU': st.session_state.get('PU', 550),
        'PPU': st.session_state.get('PPU', 550),
        'PBM': st.session_state.get('PBM', 550),
        'PK': st.session_state.get('PK', 550),
        'LBI': st.session_state.get('LBI', 550),
        'LBE': st.session_state.get('LBE', 550),
        'PM': st.session_state.get('PM', 550),
        'fokus': st.session_state.get('fokus', 3),
        'percaya_diri': st.session_state.get('percaya_diri', 3),
        'kecemasan': st.session_state.get('kecemasan', 3),
        'distraksi': st.session_state.get('distraksi', 3),
        'jam_belajar': st.session_state.get('jam_belajar', 2),
        'hari_belajar': st.session_state.get('hari_belajar', 2),
        'latihan_soal': st.session_state.get('latihan_soal', 2),
        'frekuensi_tryout': st.session_state.get('frekuensi_tryout', 2),
        'review_soal': st.session_state.get('review_soal', 2),
    }
    
    # Hitung semua metrik
    skor_akademik = hitung_skor_akademik(
        input_data['jurusan'],
        input_data['PU'], input_data['PPU'], input_data['PBM'],
        input_data['PK'], input_data['LBI'], input_data['LBE'], input_data['PM']
    )
    
    lgbm_hasil = None
    if lgbm_tersedia and lgbm_model:
        lgbm_hasil = prediksi_lgbm(lgbm_model, input_data)
    
    peluang_lolos, peluang_kategori, peluang_ket = hitung_peluang_lolos(skor_akademik, input_data['kampus'])
    stabilitas_mental, stabilitas_kategori, stabilitas_ket = hitung_stabilitas_mental(
        input_data['fokus'], input_data['percaya_diri'],
        input_data['kecemasan'], input_data['distraksi']
    )
    konsistensi_belajar, konsistensi_kategori, konsistensi_ket = hitung_indeks_konsistensi(
        input_data['jam_belajar'], input_data['hari_belajar'],
        input_data['latihan_soal'], input_data['frekuensi_tryout'], input_data['review_soal']
    )
    risiko_level, risiko_emoji, risiko_ket = hitung_risiko_underperform(stabilitas_mental, konsistensi_belajar)
    skor_kebiasaan, kategori_kebiasaan, ket_kebiasaan, emoji_kebiasaan = hitung_skor_kebiasaan_belajar(
        input_data['jam_belajar'], input_data['hari_belajar'],
        input_data['latihan_soal'], input_data['frekuensi_tryout'], input_data['review_soal']
    )
    
    bobot, label_kel = get_bobot_jurusan(input_data['jurusan'])
    klaster = get_klaster_kampus(input_data['kampus'])
    
    data = {
        **input_data,
        'akademik': skor_akademik,
        'peluang': peluang_lolos,
        'peluang_kategori': peluang_kategori,
        'peluang_keterangan': peluang_ket,
        'stabilitas': stabilitas_mental,
        'stabilitas_kategori': stabilitas_kategori,
        'stabilitas_keterangan': stabilitas_ket,
        'konsistensi': konsistensi_belajar,
        'konsistensi_kategori': konsistensi_kategori,
        'konsistensi_keterangan': konsistensi_ket,
        'risiko_level': risiko_level,
        'risiko_emoji': risiko_emoji,
        'risiko_keterangan': risiko_ket,
        'kebiasaan': skor_kebiasaan,
        'kebiasaan_kategori': kategori_kebiasaan,
        'kebiasaan_keterangan': ket_kebiasaan,
        'kebiasaan_emoji': emoji_kebiasaan,
        'lgbm_tersedia': lgbm_tersedia,
        'lgbm_hasil': lgbm_hasil,
        'bobot': bobot,
        'label_kel': label_kel,
        'klaster': klaster
    }
    
    # ===== TOP BAR =====
    col_back, col_title, col_pdf = st.columns([1, 4, 1])
    with col_back:
        if st.button("← Survey Ulang"):
            st.session_state.survey_done = False
            st.session_state.page = 'survey'
            st.session_state.survey_step = 1
            st.rerun()
    with col_title:
        nama_display = data['nama'] if data['nama'] else "Peserta UTBK"
        jam = datetime.datetime.now().hour
        salam = "Selamat pagi" if jam < 11 else "Selamat siang" if jam < 15 else "Selamat sore" if jam < 18 else "Selamat malam"
        st.markdown(f"""
        <div style="text-align:center;">
            <h1 style="color:#e2e8f0;font-size:1.8rem;font-weight:800;margin:0;">🎯 AI UTBK Dashboard</h1>
            <p style="color:#63b3ed;margin:0;">{salam}, <strong>{nama_display}</strong>! 👋</p>
        </div>
        """, unsafe_allow_html=True)
    with col_pdf:
        # PDF Download
        pdf_html = generate_pdf_html(data)
        b64 = base64.b64encode(pdf_html.encode()).decode()
        st.markdown(f"""
        <a href="data:text/html;base64,{b64}" download="UTBK_Report_{nama_display}.html" 
           style="background:linear-gradient(135deg,#4299e1,#9f7aea);color:white;padding:10px 16px;
                  border-radius:10px;text-decoration:none;font-weight:600;font-size:0.9rem;
                  display:block;text-align:center;">
            💾 Save Report
        </a>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # ===== TABS =====
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Dashboard",
        "🎯 Peluang Kampus",
        "🔬 Analisis TPS",
        "🚀 Strategi",
        "🎓 Jurusan"
    ])
    
    # ========================
    # TAB 1: DASHBOARD UTAMA
    # ========================
    with tab1:
        # LGBM Info
        if data.get('lgbm_tersedia') and data.get('lgbm_hasil') and data['lgbm_hasil']['sukses']:
            hasil = data['lgbm_hasil']
            detail = hasil.get('detail', {})
            icon = detail.get('icon', '🤖')
            kep = f"{hasil['kepercayaan']:.1f}%" if hasil.get('kepercayaan') else ""
            st.success(f"🤖 **Model AI LightGBM:** {icon} **{hasil['strategi']}** (Kepercayaan: {kep}) — _{detail.get('deskripsi','')}_")
        else:
            st.info("📊 Skor dihitung dari TPS tertimbang vs passing grade. Model AI LGBM tidak tersedia.")
        
        # METRIK UTAMA - 4 gauge charts
        st.markdown("### 📈 Metrik Utama")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.plotly_chart(buat_gauge_chart(data['peluang']*100, "🎯 Peluang Lolos"), 
                           use_container_width=True, key="gauge1")
            st.markdown(f"<p style='text-align:center;color:#a0aec0;font-size:0.8rem;margin-top:-15px;'>{data['peluang_kategori']}</p>", unsafe_allow_html=True)
        with col2:
            st.plotly_chart(buat_gauge_chart(data['stabilitas'], "🧠 Stabilitas Mental"),
                           use_container_width=True, key="gauge2")
            st.markdown(f"<p style='text-align:center;color:#a0aec0;font-size:0.8rem;margin-top:-15px;'>{data['stabilitas_kategori']}</p>", unsafe_allow_html=True)
        with col3:
            st.plotly_chart(buat_gauge_chart(data['konsistensi'], "📚 Konsistensi Belajar"),
                           use_container_width=True, key="gauge3")
            st.markdown(f"<p style='text-align:center;color:#a0aec0;font-size:0.8rem;margin-top:-15px;'>{data['konsistensi_kategori']}</p>", unsafe_allow_html=True)
        with col4:
            st.plotly_chart(buat_gauge_chart(data['kebiasaan'], "⭐ Kebiasaan Belajar"),
                           use_container_width=True, key="gauge4")
            st.markdown(f"<p style='text-align:center;color:#a0aec0;font-size:0.8rem;margin-top:-15px;'>{data['kebiasaan_kategori']}</p>", unsafe_allow_html=True)
        
        st.divider()
        
        # SKOR AKADEMIK
        col_s1, col_s2 = st.columns([2, 1])
        with col_s1:
            progress_pct = min(data['akademik'] / SKOR_MAX_UTBK, 1.0)
            color_bar = "#48bb78" if data['akademik'] >= klaster['skor_min'] else "#ed8936" if data['akademik'] >= klaster['skor_min'] - 50 else "#fc8181"
            
            st.markdown(f"""
            <div class="metric-card">
                <p style="color:#a0aec0;font-size:0.85rem;font-weight:600;text-transform:uppercase;letter-spacing:1px;">📊 Skor Akademik Tertimbang</p>
                <div style="display:flex;align-items:baseline;gap:12px;margin:8px 0;">
                    <span style="color:{color_bar};font-size:3rem;font-weight:800;">{data['akademik']:.0f}</span>
                    <span style="color:#718096;font-size:1rem;">/ {SKOR_MAX_UTBK}</span>
                </div>
                <p style="color:#a0aec0;font-size:0.8rem;margin-bottom:8px;">Disesuaikan bobot jurusan <strong style="color:#63b3ed;">{data['jurusan']}</strong> ({data['label_kel']})</p>
                <div style="background:rgba(255,255,255,0.1);border-radius:10px;height:16px;overflow:hidden;">
                    <div style="background:linear-gradient(90deg,{color_bar},{color_bar}cc);width:{progress_pct*100:.1f}%;height:16px;border-radius:10px;position:relative;">
                    </div>
                </div>
                <div style="display:flex;justify-content:space-between;margin-top:4px;">
                    <span style="color:#a0aec0;font-size:0.75rem;">0</span>
                    <span style="color:#f6e05e;font-size:0.75rem;">Min Aman: {klaster['skor_min']}</span>
                    <span style="color:#48bb78;font-size:0.75rem;">Aman: {klaster['skor_max']}</span>
                    <span style="color:#a0aec0;font-size:0.75rem;">{SKOR_MAX_UTBK}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_s2:
            status = analisis_peluang_kampus(data['akademik'], data['kampus'])
            c_map = {"success": "#48bb78", "warning": "#ed8936", "error": "#fc8181"}
            c_col = c_map.get(status['warna_status'], '#a0aec0')
            st.markdown(f"""
            <div class="metric-card" style="text-align:center;">
                <p style="color:#a0aec0;font-size:0.85rem;font-weight:600;text-transform:uppercase;">Status Kampus</p>
                <p style="font-size:2rem;margin:8px 0;">{status['emoji']}</p>
                <p style="color:{c_col};font-size:1.2rem;font-weight:700;">{status['kategori']}</p>
                <p style="color:#a0aec0;font-size:0.8rem;">{data['kampus']}</p>
                <p style="color:{c_col};font-size:1.5rem;font-weight:800;">{status['persentase']}%</p>
                <p style="color:#718096;font-size:0.75rem;">Estimasi Peluang</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.divider()
        
        # CHARTS BARIS 1
        col_r, col_b = st.columns(2)
        with col_r:
            skor_subtes = {k: data[k] for k in SUBTES_LABELS.keys()}
            st.plotly_chart(buat_radar_chart(skor_subtes, bobot, data['jurusan']),
                           use_container_width=True, key="radar1")
        with col_b:
            st.plotly_chart(buat_bar_kebiasaan(data),
                           use_container_width=True, key="bar_keb")
    
    # ========================
    # TAB 2: PELUANG KAMPUS
    # ========================
    with tab2:
        nama_disp = data['nama'] if data['nama'] else "Kamu"
        st.markdown(f"### 🏛️ Analisis Peluang {nama_disp} di {data['kampus']}")
        
        peluang_kampus = analisis_peluang_kampus(data['akademik'], data['kampus'])
        kl = peluang_kampus['klaster']
        
        # Info klaster
        st.markdown(f"""
        <div class="info-box">
            <span style="font-size:1.3rem;">{kl['warna']}</span>
            <strong style="color:#e2e8f0;font-size:1.1rem;margin-left:8px;">{kl['nama']}</strong>
            <p style="color:#a0aec0;margin:4px 0 0;">{kl['keterangan']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Skor Akademik Kamu", f"{data['akademik']:.0f}",
                      delta=f"{peluang_kampus['selisih_min']:+.0f} dari minimum")
        with col2:
            st.metric("Zona Aman Kampus", f"{kl['skor_min']} – {kl['skor_max']}")
        with col3:
            st.metric("Estimasi Peluang", f"{peluang_kampus['persentase']}%",
                      delta=peluang_kampus['kategori'])
        
        # STATUS
        status_colors = {"success": "success-box", "warning": "warning-box", "error": "danger-box"}
        box_class = status_colors.get(peluang_kampus['warna_status'], 'info-box')
        
        if peluang_kampus['warna_status'] == "success":
            st.success(f"{peluang_kampus['emoji']} **{peluang_kampus['kategori']}** — {peluang_kampus['keterangan']}")
        elif peluang_kampus['warna_status'] == "warning":
            st.warning(f"{peluang_kampus['emoji']} **{peluang_kampus['kategori']}** — {peluang_kampus['keterangan']}")
        else:
            st.error(f"{peluang_kampus['emoji']} **{peluang_kampus['kategori']}** — {peluang_kampus['keterangan']}")
        
        # BAR CHART KAMPUS
        st.markdown("### 📊 Posisi Skor vs Semua PTN")
        st.plotly_chart(buat_bar_peluang_kampus(data['akademik']),
                       use_container_width=True, key="bar_kampus")
        
        # TABEL PERBANDINGAN
        st.markdown("### 📋 Tabel Perbandingan Klaster")
        comparison_data = []
        for kid, kdata in PTN_DATA.items():
            smin, smax = kdata["skor_aman"]
            selisih = data['akademik'] - smin
            if data['akademik'] >= smax: status, peluang = "🎯 Sangat Aman", "85%"
            elif data['akademik'] >= smin: status, peluang = "✅ Aman", "70%"
            elif data['akademik'] >= smin - 50: status, peluang = "⚠️ Kompetitif", "50%"
            else: status, peluang = "🔴 Berisiko", "25%"
            comparison_data.append({
                "Klaster": kdata['warna'] + " " + kdata['nama'],
                "Zona Aman": f"{smin} – {smax}",
                "Skor Kamu": f"{data['akademik']:.0f}",
                "Selisih": f"{selisih:+.0f}",
                "Status": status,
                "Peluang": peluang
            })
        
        df_comp = pd.DataFrame(comparison_data)
        st.dataframe(df_comp, use_container_width=True, hide_index=True)
        
        # REKOMENDASI 3 PILIHAN
        st.divider()
        st.markdown("### 🎓 Strategi 3 Pilihan Kampus")
        
        kampus_sangat_aman, kampus_aman, kampus_kompetitif, kampus_berisiko = [], [], [], []
        skor_a = data['akademik']
        for kid, kdata in PTN_DATA.items():
            smin, smax = kdata["skor_aman"]
            for univ in kdata["universitas"]:
                sd = {"kampus": univ, "klaster": kdata["nama"], "skor_min": smin, "skor_max": smax,
                      "warna": kdata["warna"], "selisih": skor_a - smin}
                if skor_a >= smax: kampus_sangat_aman.append(sd)
                elif skor_a >= smin: kampus_aman.append(sd)
                elif skor_a >= smin - 50: kampus_kompetitif.append(sd)
                else: kampus_berisiko.append(sd)
        
        # Tentukan 3 pilihan
        semua_aman = kampus_sangat_aman + kampus_aman
        
        if semua_aman or kampus_kompetitif:
            col_p1, col_p2, col_p3 = st.columns(3)
            
            with col_p1:
                p1 = kampus_kompetitif[0] if kampus_kompetitif else (kampus_aman[0] if kampus_aman else None)
                if p1:
                    st.markdown(f"""
                    <div style="background:rgba(252,129,129,0.1);border:1px solid rgba(252,129,129,0.3);border-radius:12px;padding:16px;text-align:center;">
                        <p style="color:#fc8181;font-weight:700;font-size:0.85rem;">🏔️ PILIHAN 1 — AMBISIUS</p>
                        <p style="color:#e2e8f0;font-weight:700;">{p1['kampus']}</p>
                        <p style="color:#a0aec0;font-size:0.8rem;">{p1['klaster']}</p>
                        <p style="color:#fc8181;font-weight:600;">Zona: {p1['skor_min']}–{p1['skor_max']}</p>
                        <p style="color:#a0aec0;font-size:0.75rem;">Gap: {p1['skor_min']-skor_a:.0f} poin menuju zona aman</p>
                    </div>""", unsafe_allow_html=True)
            
            with col_p2:
                p2 = kampus_aman[0] if kampus_aman else (kampus_sangat_aman[0] if kampus_sangat_aman else None)
                if p2:
                    st.markdown(f"""
                    <div style="background:rgba(246,224,94,0.1);border:1px solid rgba(246,224,94,0.3);border-radius:12px;padding:16px;text-align:center;">
                        <p style="color:#f6e05e;font-weight:700;font-size:0.85rem;">⚖️ PILIHAN 2 — REALISTIS</p>
                        <p style="color:#e2e8f0;font-weight:700;">{p2['kampus']}</p>
                        <p style="color:#a0aec0;font-size:0.8rem;">{p2['klaster']}</p>
                        <p style="color:#f6e05e;font-weight:600;">Zona: {p2['skor_min']}–{p2['skor_max']}</p>
                        <p style="color:#48bb78;font-size:0.75rem;">✅ Skor sudah dalam zona aman</p>
                    </div>""", unsafe_allow_html=True)
            
            with col_p3:
                p3 = kampus_sangat_aman[0] if kampus_sangat_aman else (kampus_aman[-1] if len(kampus_aman) > 1 else None)
                if p3:
                    st.markdown(f"""
                    <div style="background:rgba(72,187,120,0.1);border:1px solid rgba(72,187,120,0.3);border-radius:12px;padding:16px;text-align:center;">
                        <p style="color:#48bb78;font-weight:700;font-size:0.85rem;">🛡️ PILIHAN 3 — AMAN</p>
                        <p style="color:#e2e8f0;font-weight:700;">{p3['kampus']}</p>
                        <p style="color:#a0aec0;font-size:0.8rem;">{p3['klaster']}</p>
                        <p style="color:#48bb78;font-weight:600;">Zona: {p3['skor_min']}–{p3['skor_max']}</p>
                        <p style="color:#48bb78;font-size:0.75rem;">🎯 Safety net terjamin</p>
                    </div>""", unsafe_allow_html=True)
        else:
            st.error("Skor saat ini masih di bawah zona aman semua kampus. Tingkatkan persiapan intensif!")
    
    # ========================
    # TAB 3: ANALISIS TPS
    # ========================
    with tab3:
        st.markdown("### 🔬 Analisis Mendalam Skor TPS")
        
        skor_subtes = {k: data[k] for k in SUBTES_LABELS.keys()}
        
        # Bobot jurusan
        st.markdown(f"#### 📋 Bobot Subtes untuk Jurusan **{data['jurusan']}** ({data['label_kel']})")
        
        cols = st.columns(7)
        for i, (k, v) in enumerate(bobot.items()):
            with cols[i]:
                color = "#48bb78" if v >= 0.20 else "#f6e05e" if v >= 0.12 else "#a0aec0"
                st.markdown(f"""
                <div style="text-align:center;background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);border-radius:10px;padding:10px;">
                    <p style="color:#a0aec0;font-size:0.75rem;margin:0;">{k}</p>
                    <p style="color:{color};font-size:1.4rem;font-weight:800;margin:4px 0;">{v*100:.0f}%</p>
                    <p style="color:#718096;font-size:0.7rem;margin:0;">bobot</p>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Radar chart
        st.plotly_chart(buat_radar_chart(skor_subtes, bobot, data['jurusan']),
                       use_container_width=True, key="radar_tab3")
        
        # Bar + bobot overlay
        st.plotly_chart(buat_bar_skor_subtes(skor_subtes, bobot),
                       use_container_width=True, key="bar_subtes")
        
        # Pipeline
        st.plotly_chart(buat_pipeline_subtes(skor_subtes, bobot),
                       use_container_width=True, key="pipeline")
        
        # Tabel detail
        st.markdown("#### 📊 Tabel Detail Subtes")
        tabel_subtes = []
        for k, label in SUBTES_LABELS.items():
            skor = skor_subtes[k]
            bw = bobot[k]
            kontrib = skor * bw
            persen = skor / SKOR_MAX_UTBK * 100
            status = "🟢 Kuat" if persen >= 70 else "🟡 Cukup" if persen >= 50 else "🔴 Perlu Ditingkatkan"
            tabel_subtes.append({
                "Subtes": f"{label} ({k})",
                "Skor": skor,
                "Bobot": f"{bw*100:.0f}%",
                "Kontribusi": f"{kontrib:.1f}",
                "Persentil": f"{persen:.0f}%",
                "Status": status
            })
        
        df_subtes = pd.DataFrame(tabel_subtes)
        st.dataframe(df_subtes, use_container_width=True, hide_index=True)
        
        # Total skor tertimbang
        total_kontrib = sum(skor_subtes[k] * bobot[k] for k in skor_subtes)
        st.success(f"✅ **Total Skor Tertimbang: {total_kontrib:.1f}** (dari maks ~{SKOR_MAX_UTBK})")
        
        st.divider()
        
        # Analisis psikologis
        st.markdown("### 🧠 Analisis Psikologi & Kebiasaan")
        
        tipe = klasifikasi_profil(data['fokus'], data['percaya_diri'], data['kecemasan'], data['distraksi'])
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <p style="color:#a0aec0;font-size:0.85rem;">📌 Profil Belajar</p>
                <p style="color:#63b3ed;font-size:1.2rem;font-weight:700;">{tipe}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.metric("Fokus", f"{data['fokus']}/5")
            st.metric("Percaya Diri", f"{data['percaya_diri']}/5")
            st.metric("Kecemasan", f"{data['kecemasan']}/5")
            st.metric("Distraksi", f"{data['distraksi']}/5")
        
        with col2:
            st.plotly_chart(buat_gauge_chart(data['stabilitas'], "🧠 Stabilitas Mental"),
                           use_container_width=True, key="gauge_stab")
            st.plotly_chart(buat_gauge_chart(data['konsistensi'], "📚 Konsistensi Belajar"),
                           use_container_width=True, key="gauge_kons")
    
    # ========================
    # TAB 4: STRATEGI
    # ========================
    with tab4:
        nama_d = data['nama'] if data['nama'] else "kamu"
        st.markdown(f"### 🚀 Strategi Belajar Personal untuk {nama_d}")
        
        # LGBM Strategi
        if data.get('lgbm_tersedia') and data.get('lgbm_hasil') and data['lgbm_hasil']['sukses']:
            hasil = data['lgbm_hasil']
            detail = hasil.get('detail', {})
            st.markdown(f"""
            <div style="background:linear-gradient(135deg,rgba(66,153,225,0.2),rgba(159,122,234,0.2));
                        border:1px solid rgba(99,179,237,0.4);border-radius:16px;padding:20px;margin-bottom:20px;">
                <p style="color:#63b3ed;font-weight:700;margin-bottom:4px;">🤖 Rekomendasi AI LightGBM</p>
                <p style="color:#e2e8f0;font-size:1.3rem;font-weight:800;">{detail.get('icon','')} {hasil['strategi']}</p>
                <p style="color:#a0aec0;margin:4px 0;">{detail.get('deskripsi','')}</p>
            </div>
            """, unsafe_allow_html=True)
            if detail.get('tips'):
                st.markdown("**📋 Tips Strategi:**")
                for tip in detail['tips']:
                    st.markdown(f"• {tip}")
        
        st.divider()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📅 Strategi Harian")
            st.markdown("""
            1. Belajar 2-3 sesi/hari, durasi 45-60 menit per sesi
            2. Setiap sesi fokus pada 1 subtes utama
            3. Gunakan metode *active recall* dan latihan soal
            4. Akhiri sesi dengan rangkuman pribadi
            """)
            
            st.markdown("#### 🗓️ Timeline Persiapan")
            st.markdown("""
            **Bulan 1-2: Fondasi**
            - Penguatan konsep dasar
            - Identifikasi gap pengetahuan
            
            **Bulan 3-4: Intensifikasi**
            - Latihan soal intensif (50-100 soal/minggu)
            - Mulai tryout bulanan
            
            **Bulan 5-6: Pemantapan**
            - Tryout mingguan
            - Review kesalahan berulang
            - Manajemen stamina mental
            """)
        
        with col2:
            st.markdown("#### 🎯 Fokus Subtes")
            skor_subtes = {k: data[k] for k in SUBTES_LABELS.keys()}
            bobot_j, _ = get_bobot_jurusan(data['jurusan'])
            
            # Urutkan berdasarkan gap tertinggi (skor rendah & bobot tinggi)
            priority = [(k, skor_subtes[k], bobot_j[k], skor_subtes[k] * bobot_j[k]) 
                       for k in skor_subtes.keys()]
            priority.sort(key=lambda x: x[3])  # urut dari kontribusi terendah
            
            for k, skor, bw, kontrib in priority[:3]:
                color = "#fc8181" if skor < 500 else "#f6e05e"
                st.markdown(f"""
                <div style="background:rgba(255,255,255,0.05);border-left:3px solid {color};
                            border-radius:8px;padding:10px 14px;margin:6px 0;">
                    <p style="color:{color};font-weight:700;margin:0;">{SUBTES_LABELS[k]} ({k})</p>
                    <p style="color:#a0aec0;font-size:0.8rem;margin:2px 0;">
                        Skor: {skor} | Bobot: {bw*100:.0f}% | Kontribusi: {kontrib:.1f}
                    </p>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("#### 😌 Manajemen Stres")
            if data['kecemasan'] >= 3:
                st.markdown("""
                - Tryout rutin minimal 2x/bulan
                - Teknik pernapasan 4-7-8 sebelum belajar
                - Hindari membandingkan dengan orang lain
                - Journaling progres harian
                """)
            else:
                st.markdown("""
                - Pertahankan keseimbangan belajar & istirahat
                - Tryout berkala untuk menjaga familiaritas
                """)
        
        # Rekomendasi akhir
        st.success(f"""
        💪 **Kunci Keberhasilan untuk {nama_d}:**
        Konsistensi eksekusi + Evaluasi rutin + Manajemen mental = Hasil Optimal!
        Peluang di **{data['jurusan']}** akan semakin kompetitif dengan pendekatan sistematis.
        """)
    
    # ========================
    # TAB 5: JURUSAN
    # ========================
    with tab5:
        nama_d = data['nama'] if data['nama'] else "kamu"
        st.markdown(f"### 🎓 Analisis Jurusan untuk {nama_d}")
        
        akademik = data['akademik']
        peluang_kampus = analisis_peluang_kampus(akademik, data['kampus'])
        
        # Cek apakah peluang lolos sudah terpenuhi
        peluang_lolos_ok = peluang_kampus['warna_status'] == "success"
        
        # Info target utama
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,rgba(66,153,225,0.2),rgba(159,122,234,0.2));
                    border:1px solid rgba(99,179,237,0.4);border-radius:16px;padding:24px;margin-bottom:20px;">
            <div style="display:flex;align-items:center;gap:12px;margin-bottom:12px;">
                <span style="font-size:2rem;">{peluang_kampus['emoji']}</span>
                <div>
                    <p style="color:#e2e8f0;font-size:1.2rem;font-weight:800;margin:0;">Target: {data['jurusan']}</p>
                    <p style="color:#a0aec0;font-size:0.9rem;margin:0;">di {data['kampus']}</p>
                </div>
                <div style="margin-left:auto;text-align:right;">
                    <p style="color:{'#48bb78' if peluang_lolos_ok else '#ed8936'};font-size:1.8rem;font-weight:800;margin:0;">
                        {peluang_kampus['persentase']}%
                    </p>
                    <p style="color:#a0aec0;font-size:0.8rem;margin:0;">Peluang Lolos</p>
                </div>
            </div>
            <p style="color:#a0aec0;font-size:0.85rem;margin:0;">{peluang_kampus['keterangan']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        if peluang_lolos_ok:
            # Peluang sudah terpenuhi: fokus ke target, jurusan alternatif hanya formalitas
            st.success(f"""
            ✅ **Peluang Lolos TERPENUHI!**
            
            Skor kamu sudah berada dalam zona aman untuk **{data['jurusan']}** di **{data['kampus']}**.
            Fokuskan semua energi untuk mempertahankan dan meningkatkan performa ini!
            """)
            
            st.markdown("### 🎯 Fokus Utama: Pertahankan Target Jurusan")
            
            # Bobot jurusan target
            st.markdown(f"#### 📊 Bobot Subtes untuk {data['jurusan']}")
            
            cols = st.columns(7)
            for i, (k, v) in enumerate(bobot.items()):
                with cols[i]:
                    skor_k = data[k]
                    is_strong = skor_k >= klaster['skor_min'] * v / sum(bobot.values())
                    brd = "#48bb78" if v >= 0.20 else "#f6e05e" if v >= 0.12 else "#718096"
                    st.markdown(f"""
                    <div style="text-align:center;background:rgba(255,255,255,0.05);
                                border:2px solid {brd};border-radius:10px;padding:10px;">
                        <p style="color:#a0aec0;font-size:0.75rem;margin:0;">{k}</p>
                        <p style="color:{brd};font-size:1.3rem;font-weight:800;margin:4px 0;">{v*100:.0f}%</p>
                        <p style="color:#e2e8f0;font-size:0.8rem;margin:0;">{skor_k}</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Tips pertahankan
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("""
                #### ✅ Yang Harus Dipertahankan:
                - Konsistensi jadwal belajar saat ini
                - Frekuensi tryout minimal 2x/bulan
                - Review soal rutin setiap minggu
                - Manajemen stres & tidur yang baik
                """)
            with col2:
                st.markdown("""
                #### 🚀 Yang Perlu Ditingkatkan:
                - Simulasi kondisi ujian sesungguhnya
                - Perkuat subtes dengan bobot tertinggi
                - Evaluasi setiap tryout secara detail
                - Jaga stamina fisik dan mental menjelang hari H
                """)
            
            # Jurusan alternatif (formalitas)
            st.divider()
            with st.expander("📋 Jurusan Alternatif (untuk strategi cadangan — opsional)", expanded=False):
                st.info("ℹ️ Karena peluang kamu sudah sangat baik di target utama, jurusan alternatif ini hanya bersifat formalitas sebagai safety net pilihan.")
                
                alt_jurusan_map = {
                    "Kedokteran": ["Kedokteran Gigi", "Farmasi", "Gizi"],
                    "Kedokteran Gigi": ["Farmasi", "Keperawatan", "Gizi"],
                    "Teknik Informatika": ["Teknik Elektro", "Matematika", "Statistika"],
                    "Teknik Sipil": ["Teknik Mesin", "Teknik Industri", "Fisika"],
                    "Ekonomi": ["Manajemen", "Akuntansi", "Bisnis"],
                    "Manajemen": ["Akuntansi", "Bisnis", "Ilmu Komunikasi"],
                    "Akuntansi": ["Manajemen", "Ekonomi", "Bisnis"],
                    "Psikologi": ["Ilmu Komunikasi", "Sosiologi", "Kesehatan Masyarakat"],
                    "Ilmu Hukum": ["Administrasi Publik", "Ilmu Politik", "Sosiologi"],
                    "Matematika": ["Statistika", "Aktuaria", "Fisika"],
                }
                alts = alt_jurusan_map.get(data['jurusan'], ["Jurusan serumpun lainnya", "Jurusan lintas bidang"])
                
                for i, alt in enumerate(alts[:3], 1):
                    st.markdown(f"**{i}.** {alt} *(alternatif formalitas)*")
        
        else:
            # Peluang belum terpenuhi: tampilkan rekomendasi jurusan
            if peluang_kampus['warna_status'] == "warning":
                st.warning(f"⚠️ Skor mendekati zona aman — butuh peningkatan untuk memastikan lolos di **{data['jurusan']}**")
            else:
                st.error(f"🔴 Skor masih di bawah zona aman untuk **{data['jurusan']}** di kampus target")
            
            # Rekomendasi jurusan alternatif berdasarkan skor
            st.markdown("### 🔄 Rekomendasi Jurusan Alternatif")
            st.markdown("Berikut jurusan yang lebih sesuai dengan profil skor saat ini:")
            
            if akademik > 750:
                alts = ["Teknik Informatika", "Kedokteran Gigi", "Statistika", "Farmasi", "Manajemen"]
                label_alt = "Skor Tinggi — Pilihan Kompetitif"
                color_alt = "#48bb78"
            elif akademik > 600:
                alts = ["Teknik Industri", "Ekonomi", "Akuntansi", "Psikologi", "Ilmu Komunikasi"]
                label_alt = "Skor Menengah-Atas — Pilihan Seimbang"
                color_alt = "#f6e05e"
            else:
                alts = ["Sosiologi", "Geografi", "Sejarah", "Pendidikan Bahasa", "Administrasi Publik"]
                label_alt = "Skor Perlu Peningkatan — Pilihan Strategis"
                color_alt = "#ed8936"
            
            st.markdown(f"<p style='color:{color_alt};font-weight:600;'>📌 {label_alt}</p>", unsafe_allow_html=True)
            
            cols_alt = st.columns(len(alts))
            for i, (col, alt) in enumerate(zip(cols_alt, alts)):
                with col:
                    bobot_alt, label_alt2 = get_bobot_jurusan(alt)
                    skor_alt = hitung_skor_akademik(alt, data['PU'], data['PPU'], data['PBM'],
                                                    data['PK'], data['LBI'], data['LBE'], data['PM'])
                    st.markdown(f"""
                    <div style="background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.15);
                                border-radius:12px;padding:12px;text-align:center;height:100%;">
                        <p style="color:#e2e8f0;font-weight:700;font-size:0.85rem;">{alt}</p>
                        <p style="color:{color_alt};font-size:1.2rem;font-weight:800;">{skor_alt:.0f}</p>
                        <p style="color:#a0aec0;font-size:0.7rem;">Skor tertimbang</p>
                    </div>
                    """, unsafe_allow_html=True)
        
        st.divider()
        st.info("""
        💡 **Tips Memilih Jurusan:**
        1. **Minat & Passion** — Pilih yang sesuai minat jangka panjang
        2. **Kemampuan** — Sesuaikan dengan profil skor TPS kamu
        3. **Prospek Karir** — Pertimbangkan peluang kerja masa depan
        4. **Peluang Kelulusan** — Realistis dengan skor yang dimiliki
        """)
    
    # FOOTER
    st.divider()
    if data['nama']:
        st.success(f"""
        💪 **Pesan untuk {data['nama']}:**
        Perjalanan menuju UTBK adalah maraton, bukan sprint. Setiap langkah kecil yang kamu ambil hari ini 
        akan membawa dampak besar. Tetap konsisten, percaya pada proses!
        **Semangat, {data['nama']}! Kamu pasti bisa! 🚀✨**
        """)
    
    st.caption("🤖 AI UTBK Readiness Dashboard v2.0 • Enhanced Edition • Skor max UTBK: 1000")


# ======================================
# WELCOME PAGE
# ======================================

def render_welcome_page():
    st.markdown("""
    <div class="welcome-hero">
        <h1 style="color:#e2e8f0;font-size:3rem;font-weight:900;margin-bottom:8px;">🎯 AI UTBK</h1>
        <h2 style="color:#e2e8f0;font-size:2rem;font-weight:700;margin-bottom:8px;">Readiness Dashboard</h2>
        <p style="color:#a0aec0;font-size:1.1rem;margin-bottom:20px;">
            Sistem analisis kesiapan UTBK berbasis AI — Komprehensif, Personal, Data-Driven
        </p>
        <div style="display:inline-block;background:rgba(99,179,237,0.2);border:1px solid rgba(99,179,237,0.4);
                    border-radius:20px;padding:6px 16px;">
            <span style="color:#63b3ed;font-size:0.9rem;">✨ Skor UTBK 1000 • Radar TPS • Pipeline Bobot • Export PDF</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    features = [
        ("📊", "Dashboard Komprehensif", "Gauge, radar, bar chart interaktif untuk analisis lengkap"),
        ("🎯", "Analisis Bobot Jurusan", "Pipeline perbandingan skor vs bobot target kampus & jurusan"),
        ("🧠", "Profil Psikologis", "Evaluasi stabilitas mental dan konsistensi belajar"),
        ("🏛️", "Peluang 20 PTN", "Visualisasi posisi skor vs zona aman semua kampus"),
        ("🚀", "Strategi Personal", "Rekomendasi AI LightGBM + strategi berbasis profil unik kamu"),
        ("💾", "Export Report", "Download laporan lengkap dalam format HTML/PDF"),
    ]
    
    for i, (icon, title, desc) in enumerate(features):
        col = [col1, col2, col3][i % 3]
        with col:
            st.markdown(f"""
            <div class="feature-card">
                <p style="font-size:2rem;margin:0 0 8px;">{icon}</p>
                <p style="color:#e2e8f0;font-weight:700;font-size:1rem;margin:0 0 6px;">{title}</p>
                <p style="color:#718096;font-size:0.85rem;margin:0;">{desc}</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_btn = st.columns([1, 2, 1])
    with col_btn[1]:
        if st.button("🚀 MULAI ANALISIS SEKARANG", type="primary", use_container_width=True):
            st.session_state.page = 'survey'
            st.rerun()
    
    st.markdown("""
    <p style="text-align:center;color:#4a5568;font-size:0.85rem;margin-top:16px;">
        Gratis • Privat • Berbasis AI • Tidak perlu login
    </p>
    """, unsafe_allow_html=True)


# ======================================
# MAIN
# ======================================

def main():
    lgbm_model, lgbm_tersedia = load_lgbm_model()
    
    # Init session state
    if 'page' not in st.session_state:
        st.session_state.page = 'welcome'
    if 'survey_done' not in st.session_state:
        st.session_state.survey_done = False
    if 'survey_step' not in st.session_state:
        st.session_state.survey_step = 1
    
    # Sidebar navigation (minimal)
    with st.sidebar:
        st.markdown("""
        <div style="text-align:center;padding:16px 0;">
            <h2 style="color:#e2e8f0;margin:0;">🎯 UTBK AI</h2>
            <p style="color:#4a5568;font-size:0.8rem;margin:4px 0;">Dashboard v2.0</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        
        if st.button("🏠 Beranda", use_container_width=True):
            st.session_state.page = 'welcome'
            st.rerun()
        
        if st.button("📝 Isi Survey", use_container_width=True):
            st.session_state.page = 'survey'
            st.session_state.survey_step = 1
            st.rerun()
        
        if st.session_state.survey_done:
            if st.button("📊 Lihat Dashboard", type="primary", use_container_width=True):
                st.session_state.page = 'dashboard'
                st.rerun()
        
        st.divider()
        
        st.markdown("""
        <div style="padding:8px;">
            <p style="color:#4a5568;font-size:0.75rem;text-align:center;">
                Skor Max UTBK: <strong style="color:#63b3ed;">1000</strong><br>
                AI Model: <strong style="color:#63b3ed;">LightGBM</strong><br>
                Charts: <strong style="color:#63b3ed;">Plotly Interactive</strong>
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Route pages
    if st.session_state.page == 'welcome':
        render_welcome_page()
    elif st.session_state.page == 'survey':
        render_survey_page()
    elif st.session_state.page == 'dashboard' and st.session_state.survey_done:
        render_dashboard_page(lgbm_model, lgbm_tersedia)
    else:
        render_welcome_page()


if __name__ == "__main__":
    main()
