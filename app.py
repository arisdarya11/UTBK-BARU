"""
SKORIA — AI UTBK Readiness Dashboard
═══════════════════════════════════════════════
Fitur:
  ✅ Multi-halaman survey (4 step)
  ✅ Skor maks 1000
  ✅ Radar Chart TPS
  ✅ Bar Chart & Pipeline Chart
  ✅ Bobot jurusan & kampus ditampilkan
  ✅ Fokus jurusan target jika skor aman (alternatif = formalitas)
  ✅ Export PDF
  ✅ Model LGBM asli diintegrasikan
  ✅ Fix: Duplicate Element ID → unik key per chart
  ✅ Fix: Kontras warna font diperbaiki
"""

import streamlit as st
import numpy as np
import pandas as pd
import pickle, os, io, base64, datetime
from typing import Dict, Tuple, List
import plotly.graph_objects as go
import plotly.express as px

# ══════════════════════════════════════════════════════════════
# PAGE CONFIG
# ══════════════════════════════════════════════════════════════
st.set_page_config(page_title="SKORIA — AI UTBK Dashboard", page_icon="🎯",
                   layout="wide", initial_sidebar_state="collapsed")

# ══════════════════════════════════════════════════════════════
# GLOBAL CSS — Warna font diperbaiki untuk keterbacaan
# ══════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Syne:wght@600;700;800&display=swap');

:root {
  --bg:      #07090f;
  --surf:    #0f1218;
  --surf2:   #171c25;
  --border:  #252b38;
  --gold:    #f5a623;
  --gold2:   #ffcf6b;
  --blue:    #60b4ff;
  --green:   #4ade80;
  --red:     #ff6b6b;
  --orange:  #fb923c;
  --purple:  #c084fc;
  --text:    #f0f4f8;
  --text2:   #c8d3e0;
  --muted:   #8b9ab0;
  --muted2:  #6b7a90;
  --r:       14px;
}
html,body,[class*="css"],.stApp{
  background:var(--bg)!important;
  font-family:'Plus Jakarta Sans',sans-serif!important;
  color:var(--text)!important;
}
#MainMenu,footer,header{visibility:hidden}
.stDeployButton{display:none}
.block-container{padding:1.2rem 2rem!important;max-width:100%!important}

/* ── NAV ── */
.nav{background:linear-gradient(90deg,#0a0d14,#0f1420);
  border-bottom:1px solid var(--border);
  padding:.85rem 2rem;display:flex;align-items:center;gap:1.5rem;
  margin:-1.2rem -2rem 1.8rem -2rem;position:sticky;top:0;z-index:999}
.nav-brand{font-family:'Syne',sans-serif;font-size:1.1rem;
  font-weight:800;color:var(--gold)!important;display:flex;align-items:center;gap:.5rem;
  letter-spacing:-.02em}
.nav-brand span{color:var(--text2);font-weight:600;font-size:.8rem;letter-spacing:normal}
.nav-step{font-size:.78rem;font-weight:600;color:var(--muted);
  padding:.35rem .9rem;border-radius:99px;cursor:default}
.nav-step.active{background:rgba(245,166,35,.14);color:var(--gold);
  border:1px solid rgba(245,166,35,.35)}
.nav-step.done{color:var(--green)}

/* ── HERO ── */
.hero{background:linear-gradient(135deg,#08101f 0%,#0d1a30 50%,#0a1525 100%);
  border:1px solid var(--border);border-radius:var(--r);padding:2.5rem;
  margin-bottom:2rem;position:relative;overflow:hidden}
.hero::before{content:'';position:absolute;top:-100px;right:-100px;width:400px;height:400px;
  border-radius:50%;background:radial-gradient(circle,rgba(245,166,35,.09) 0%,transparent 65%)}
.hero::after{content:'';position:absolute;bottom:-80px;left:10%;width:300px;height:300px;
  border-radius:50%;background:radial-gradient(circle,rgba(96,180,255,.05) 0%,transparent 65%)}
.hero h1{font-family:'Syne',sans-serif!important;font-size:2.3rem!important;
  font-weight:800!important;color:#ffffff!important;margin:0 0 .6rem!important;line-height:1.15!important;
  letter-spacing:-.03em!important}
.hero h1 span{color:var(--gold)}
.hero p{color:var(--text2)!important;font-size:.95rem;margin:0;line-height:1.6}

/* ── CARDS ── */
.card{background:var(--surf);border:1px solid var(--border);border-radius:var(--r);padding:1.3rem 1.5rem}
.kpi-lbl{font-size:.68rem;font-weight:700;text-transform:uppercase;letter-spacing:.1em;
  color:var(--muted2);margin-bottom:.4rem}
.kpi-val{font-family:'Syne',sans-serif;font-size:2rem;font-weight:800;line-height:1;color:var(--text)}
.kpi-sub{font-size:.74rem;color:var(--muted);margin-top:.25rem}
.c-gold{color:var(--gold)}.c-blue{color:var(--blue)}.c-green{color:var(--green)}
.c-red{color:var(--red)}.c-orange{color:var(--orange)}.c-purple{color:var(--purple)}

/* ── SECTION TITLE ── */
.sec{font-family:'Syne',sans-serif;font-size:1rem;font-weight:700;
  color:var(--text);margin:1.8rem 0 .9rem;padding-bottom:.4rem;
  border-bottom:2px solid var(--border)}

/* ── ALERTS — teks kontras penuh ── */
.al{border-radius:var(--r);padding:1.1rem 1.4rem;margin-bottom:.9rem;
  border-left:4px solid;font-size:.87rem;line-height:1.7;color:var(--text2)}
.al h4{margin:0 0 .45rem;font-size:.92rem;font-weight:700;color:var(--text)}
.al ul{margin:.4rem 0 0;padding-left:1.2rem;color:var(--text2)}
.al ul li{margin-bottom:.25rem}
.al p{color:var(--text2)}
.al em{color:var(--text2)}
.al strong{color:var(--text)}
.al code{color:var(--gold2);background:rgba(245,166,35,.12);padding:1px 5px;border-radius:4px;font-size:.82em}
.al ol{margin:.4rem 0 0;padding-left:1.2rem;color:var(--text2)}
.al ol li{margin-bottom:.3rem}
.al-s{background:rgba(74,222,128,.07);border-color:var(--green)}
.al-s h4{color:var(--green)}
.al-w{background:rgba(251,146,60,.07);border-color:var(--orange)}
.al-w h4{color:var(--orange)}
.al-d{background:rgba(255,107,107,.07);border-color:var(--red)}
.al-d h4{color:var(--red)}
.al-i{background:rgba(96,180,255,.07);border-color:var(--blue)}
.al-i h4{color:var(--blue)}

/* ── PROGRESS BARS ── */
.prog-wrap{margin-bottom:.85rem}
.prog-lbl{display:flex;justify-content:space-between;font-size:.8rem;
  font-weight:600;color:var(--text2);margin-bottom:4px}
.prog-bg{background:var(--surf2);border-radius:99px;height:8px;overflow:hidden}
.prog-fill{height:100%;border-radius:99px}

/* ── FORM ── */
.form-box{background:var(--surf);border:1px solid var(--border);border-radius:var(--r);
  padding:1.8rem 2rem;margin-bottom:1.4rem}
.form-box h3{font-family:'Syne',sans-serif;font-size:1rem;font-weight:700;
  color:var(--gold);margin:0 0 1.2rem;display:flex;align-items:center;gap:.4rem}

/* ── STEP BAR ── */
.step-row{display:flex;gap:0;margin-bottom:2rem;background:var(--surf);
  border:1px solid var(--border);border-radius:var(--r);overflow:hidden}
.step-item{flex:1;padding:.9rem;text-align:center;font-size:.78rem;font-weight:600;
  color:var(--muted);border-right:1px solid var(--border)}
.step-item:last-child{border-right:none}
.step-item.active{background:rgba(245,166,35,.1);color:var(--gold)}
.step-item.done{background:rgba(74,222,128,.06);color:var(--green)}
.step-num{display:block;font-size:1.25rem;font-family:'Syne',sans-serif;
  font-weight:800;margin-bottom:1px}

/* ── BOBOT CHIP ── */
.bobot-chip{display:inline-flex;flex-direction:column;align-items:center;
  background:rgba(245,166,35,.08);border:1px solid rgba(245,166,35,.2);
  border-radius:10px;padding:.5rem .7rem;margin:.2rem}
.bobot-chip .sk{font-size:.68rem;color:var(--muted);margin-bottom:1px}
.bobot-chip .bv{font-size:1.05rem;font-weight:800;color:var(--gold);
  font-family:'Syne',sans-serif}

/* ── STREAMLIT OVERRIDES ── */
div[data-testid="stButton"] button[kind="primary"]{
  background:linear-gradient(135deg,var(--gold),#e8941a)!important;
  color:#000!important;font-weight:700!important;
  font-family:'Syne',sans-serif!important;border:none!important;
  border-radius:10px!important;font-size:.9rem!important;letter-spacing:.02em!important}
div[data-testid="stButton"] button{
  background:var(--surf2)!important;color:var(--text2)!important;
  border:1px solid var(--border)!important;border-radius:10px!important}
div[data-testid="stTabs"] button[data-baseweb="tab"]{
  font-family:'Syne',sans-serif!important;font-weight:600!important;
  font-size:.83rem!important;color:var(--muted)!important}
div[data-testid="stTabs"] button[aria-selected="true"]{
  color:var(--gold)!important;border-bottom-color:var(--gold)!important}
div[data-testid="stMetric"]{background:var(--surf)!important;
  border:1px solid var(--border)!important;border-radius:var(--r)!important;
  padding:1rem 1.2rem!important}
div[data-testid="stMetric"] label{color:var(--muted)!important;font-size:.75rem!important;font-weight:600!important;text-transform:uppercase!important;letter-spacing:.08em!important}
div[data-testid="stMetric"] [data-testid="stMetricValue"]{color:var(--text)!important;font-family:'Syne',sans-serif!important;font-weight:800!important}
div[data-testid="stExpander"]{background:var(--surf)!important;
  border:1px solid var(--border)!important;border-radius:var(--r)!important}
div[data-testid="stExpander"] summary{color:var(--text2)!important;font-weight:600!important}
/* Slider labels */
div[data-testid="stSlider"] label,div[data-testid="stSelectbox"] label,
div[data-testid="stTextInput"] label{color:var(--text2)!important;font-weight:600!important;font-size:.85rem!important}
div[data-testid="stSlider"] [data-testid="stMarkdownContainer"] p{color:var(--text2)!important}
/* Selectbox text */
div[data-testid="stSelectbox"] [data-baseweb="select"] [data-testid="stMarkdownContainer"]{color:var(--text)!important}
/* Caption */
.stCaption,.stCaption p,[data-testid="stCaptionContainer"]{color:var(--muted)!important;font-size:.8rem!important}
/* Dataframe */
div[data-testid="stDataFrame"]{border-radius:10px;overflow:hidden}
/* Divider */
hr{border-color:var(--border)!important;margin:1.2rem 0!important}
/* Text input */
div[data-testid="stTextInput"] input{background:var(--surf2)!important;color:var(--text)!important;border-color:var(--border)!important}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# SESSION STATE
# ══════════════════════════════════════════════════════════════
for k, v in [('page','home'),('step',1),('data',{}),('result',None)]:
    if k not in st.session_state:
        st.session_state[k] = v

# Counter untuk key unik chart (fix duplicate element ID)
if '_chart_counter' not in st.session_state:
    st.session_state._chart_counter = 0

def next_chart_key(prefix="chart"):
    st.session_state._chart_counter += 1
    return f"{prefix}_{st.session_state._chart_counter}"


# ══════════════════════════════════════════════════════════════
# KONSTANTA
# ══════════════════════════════════════════════════════════════
SKOR_MIN = 200
SKOR_MAX = 1000
APP_NAME = "SKORIA"
APP_TAGLINE = "AI UTBK Intelligence"

SUBTES = ["PU","PPU","PBM","PK","LBI","LBE","PM"]
SUBTES_LABEL = {
    "PU":"Penalaran Umum","PPU":"Pem. & Pengetahuan Umum",
    "PBM":"Pemahaman Bacaan & Menulis","PK":"Pengetahuan Kuantitatif",
    "LBI":"Literasi Bahasa Indonesia","LBE":"Literasi Bahasa Inggris",
    "PM":"Penalaran Matematika"
}
SUBTES_COLOR = {
    "PU":"#f5a623","PPU":"#60b4ff","PBM":"#c084fc",
    "PK":"#ff6b6b","LBI":"#4ade80","LBE":"#67e8f9","PM":"#fda4af"
}

DAFTAR_JURUSAN = [
    "Kedokteran","Kedokteran Gigi",
    "Teknik Sipil","Teknik Mesin","Teknik Elektro","Teknik Industri","Teknik Kimia","Teknik Informatika",
    "Matematika","Fisika","Kimia","Biologi","Statistika","Aktuaria",
    "Farmasi","Gizi","Keperawatan","Kesehatan Masyarakat",
    "Ilmu Hukum","Ekonomi","Manajemen","Akuntansi","Bisnis",
    "Psikologi","Ilmu Komunikasi","Hubungan Internasional","Administrasi Publik",
    "Sastra Inggris","Pendidikan Bahasa Indonesia","Pendidikan Bahasa Inggris",
    "Sosiologi","Ilmu Politik","Sejarah","Geografi"
]

BOBOT_MAP = {
    "Kedokteran"            :{"PU":.20,"PPU":.15,"PBM":.10,"PK":.15,"LBI":.10,"LBE":.10,"PM":.20},
    "Kedokteran Gigi"       :{"PU":.20,"PPU":.15,"PBM":.10,"PK":.15,"LBI":.10,"LBE":.10,"PM":.20},
    "Teknik Informatika"    :{"PU":.20,"PPU":.05,"PBM":.05,"PK":.20,"LBI":.05,"LBE":.10,"PM":.35},
    "Teknik Sipil"          :{"PU":.20,"PPU":.05,"PBM":.05,"PK":.20,"LBI":.05,"LBE":.10,"PM":.35},
    "Teknik Mesin"          :{"PU":.20,"PPU":.05,"PBM":.05,"PK":.20,"LBI":.05,"LBE":.10,"PM":.35},
    "Teknik Elektro"        :{"PU":.20,"PPU":.05,"PBM":.05,"PK":.20,"LBI":.05,"LBE":.10,"PM":.35},
    "Teknik Industri"       :{"PU":.20,"PPU":.05,"PBM":.05,"PK":.20,"LBI":.05,"LBE":.10,"PM":.35},
    "Teknik Kimia"          :{"PU":.18,"PPU":.08,"PBM":.05,"PK":.20,"LBI":.05,"LBE":.07,"PM":.37},
    "Matematika"            :{"PU":.15,"PPU":.05,"PBM":.05,"PK":.20,"LBI":.05,"LBE":.05,"PM":.45},
    "Fisika"                :{"PU":.18,"PPU":.07,"PBM":.05,"PK":.20,"LBI":.05,"LBE":.05,"PM":.40},
    "Kimia"                 :{"PU":.18,"PPU":.10,"PBM":.07,"PK":.18,"LBI":.07,"LBE":.05,"PM":.35},
    "Biologi"               :{"PU":.20,"PPU":.15,"PBM":.10,"PK":.15,"LBI":.10,"LBE":.08,"PM":.22},
    "Statistika"            :{"PU":.15,"PPU":.07,"PBM":.05,"PK":.20,"LBI":.05,"LBE":.05,"PM":.43},
    "Aktuaria"              :{"PU":.15,"PPU":.07,"PBM":.05,"PK":.20,"LBI":.05,"LBE":.05,"PM":.43},
    "Farmasi"               :{"PU":.18,"PPU":.12,"PBM":.08,"PK":.18,"LBI":.08,"LBE":.08,"PM":.28},
    "Gizi"                  :{"PU":.18,"PPU":.12,"PBM":.10,"PK":.15,"LBI":.12,"LBE":.08,"PM":.25},
    "Keperawatan"           :{"PU":.18,"PPU":.12,"PBM":.12,"PK":.12,"LBI":.15,"LBE":.08,"PM":.23},
    "Kesehatan Masyarakat"  :{"PU":.20,"PPU":.12,"PBM":.12,"PK":.12,"LBI":.15,"LBE":.08,"PM":.21},
    "Ilmu Hukum"            :{"PU":.22,"PPU":.18,"PBM":.20,"PK":.08,"LBI":.18,"LBE":.10,"PM":.04},
    "Ekonomi"               :{"PU":.20,"PPU":.15,"PBM":.10,"PK":.20,"LBI":.10,"LBE":.10,"PM":.15},
    "Manajemen"             :{"PU":.20,"PPU":.15,"PBM":.12,"PK":.18,"LBI":.12,"LBE":.10,"PM":.13},
    "Akuntansi"             :{"PU":.18,"PPU":.15,"PBM":.10,"PK":.22,"LBI":.10,"LBE":.10,"PM":.15},
    "Bisnis"                :{"PU":.20,"PPU":.15,"PBM":.12,"PK":.18,"LBI":.12,"LBE":.10,"PM":.13},
    "Psikologi"             :{"PU":.22,"PPU":.15,"PBM":.18,"PK":.10,"LBI":.18,"LBE":.10,"PM":.07},
    "Ilmu Komunikasi"       :{"PU":.20,"PPU":.15,"PBM":.22,"PK":.08,"LBI":.20,"LBE":.10,"PM":.05},
    "Hubungan Internasional":{"PU":.20,"PPU":.15,"PBM":.15,"PK":.08,"LBI":.17,"LBE":.20,"PM":.05},
    "Administrasi Publik"   :{"PU":.22,"PPU":.15,"PBM":.18,"PK":.08,"LBI":.20,"LBE":.10,"PM":.07},
    "Sastra Inggris"        :{"PU":.12,"PPU":.12,"PBM":.20,"PK":.05,"LBI":.15,"LBE":.31,"PM":.05},
    "Pendidikan Bahasa Indonesia":{"PU":.12,"PPU":.12,"PBM":.22,"PK":.05,"LBI":.32,"LBE":.12,"PM":.05},
    "Pendidikan Bahasa Inggris"  :{"PU":.12,"PPU":.12,"PBM":.18,"PK":.05,"LBI":.12,"LBE":.33,"PM":.08},
    "Sosiologi"             :{"PU":.22,"PPU":.17,"PBM":.18,"PK":.08,"LBI":.18,"LBE":.10,"PM":.07},
    "Ilmu Politik"          :{"PU":.22,"PPU":.17,"PBM":.18,"PK":.08,"LBI":.18,"LBE":.10,"PM":.07},
    "Sejarah"               :{"PU":.20,"PPU":.20,"PBM":.18,"PK":.05,"LBI":.22,"LBE":.10,"PM":.05},
    "Geografi"              :{"PU":.20,"PPU":.15,"PBM":.15,"PK":.12,"LBI":.15,"LBE":.08,"PM":.15},
}
DEFAULT_BOBOT = {"PU":.15,"PPU":.15,"PBM":.15,"PK":.15,"LBI":.15,"LBE":.15,"PM":.10}

PTN_DATA = {
    "Universitas Indonesia (UI)"                :{"klaster":1,"min":780,"max":870,"label":"⭐ Klaster 1 — Top Tier"},
    "Universitas Gadjah Mada (UGM)"             :{"klaster":1,"min":780,"max":870,"label":"⭐ Klaster 1 — Top Tier"},
    "Institut Teknologi Bandung (ITB)"          :{"klaster":1,"min":790,"max":880,"label":"⭐ Klaster 1 — Top Tier"},
    "Universitas Padjadjaran (Unpad)"           :{"klaster":1,"min":760,"max":840,"label":"⭐ Klaster 1 — Top Tier"},
    "Institut Pertanian Bogor (IPB)"            :{"klaster":1,"min":750,"max":830,"label":"⭐ Klaster 1 — Top Tier"},
    "Universitas Diponegoro (Undip)"            :{"klaster":2,"min":700,"max":780,"label":"🔷 Klaster 2 — Mng Atas"},
    "Universitas Airlangga (Unair)"             :{"klaster":2,"min":710,"max":790,"label":"🔷 Klaster 2 — Mng Atas"},
    "Universitas Brawijaya (UB)"                :{"klaster":2,"min":680,"max":760,"label":"🔷 Klaster 2 — Mng Atas"},
    "Institut Teknologi Sepuluh Nopember (ITS)" :{"klaster":2,"min":710,"max":790,"label":"🔷 Klaster 2 — Mng Atas"},
    "Universitas Sebelas Maret (UNS)"           :{"klaster":2,"min":660,"max":740,"label":"🔷 Klaster 2 — Mng Atas"},
    "Universitas Hasanuddin (Unhas)"            :{"klaster":2,"min":660,"max":740,"label":"🔷 Klaster 2 — Mng Atas"},
    "Universitas Negeri Yogyakarta (UNY)"       :{"klaster":3,"min":610,"max":690,"label":"🔹 Klaster 3 — Menengah"},
    "Universitas Negeri Semarang (UNNES)"       :{"klaster":3,"min":600,"max":680,"label":"🔹 Klaster 3 — Menengah"},
    "Universitas Negeri Malang (UM)"            :{"klaster":3,"min":600,"max":680,"label":"🔹 Klaster 3 — Menengah"},
    "Universitas Andalas (Unand)"               :{"klaster":3,"min":600,"max":680,"label":"🔹 Klaster 3 — Menengah"},
    "Universitas Sumatera Utara (USU)"          :{"klaster":3,"min":590,"max":670,"label":"🔹 Klaster 3 — Menengah"},
    "Universitas Sriwijaya (Unsri)"             :{"klaster":4,"min":550,"max":630,"label":"🔸 Klaster 4 — Regional"},
    "Universitas Lampung (Unila)"               :{"klaster":4,"min":540,"max":620,"label":"🔸 Klaster 4 — Regional"},
    "Universitas Jember (Unej)"                 :{"klaster":4,"min":535,"max":615,"label":"🔸 Klaster 4 — Regional"},
    "Universitas Riau (Unri)"                   :{"klaster":4,"min":530,"max":610,"label":"🔸 Klaster 4 — Regional"},
}
DAFTAR_PTN = list(PTN_DATA.keys())

ALTERNATIF_MAP = {
    "Kedokteran":["Keperawatan","Farmasi","Gizi"],
    "Kedokteran Gigi":["Farmasi","Keperawatan","Kesehatan Masyarakat"],
    "Teknik Informatika":["Statistika","Matematika","Teknik Elektro"],
    "Teknik Sipil":["Teknik Industri","Teknik Mesin","Fisika"],
    "Teknik Mesin":["Teknik Industri","Teknik Sipil","Fisika"],
    "Teknik Elektro":["Teknik Informatika","Fisika","Matematika"],
    "Teknik Industri":["Teknik Sipil","Manajemen","Statistika"],
    "Teknik Kimia":["Kimia","Farmasi","Teknik Industri"],
    "Matematika":["Statistika","Aktuaria","Fisika"],
    "Fisika":["Matematika","Teknik Mesin","Teknik Elektro"],
    "Kimia":["Farmasi","Teknik Kimia","Biologi"],
    "Biologi":["Gizi","Keperawatan","Kimia"],
    "Statistika":["Matematika","Aktuaria","Teknik Informatika"],
    "Aktuaria":["Statistika","Matematika","Ekonomi"],
    "Farmasi":["Kimia","Gizi","Kesehatan Masyarakat"],
    "Gizi":["Keperawatan","Farmasi","Kesehatan Masyarakat"],
    "Keperawatan":["Gizi","Kesehatan Masyarakat","Farmasi"],
    "Kesehatan Masyarakat":["Keperawatan","Gizi","Biologi"],
    "Ilmu Hukum":["Administrasi Publik","Ilmu Politik","Sosiologi"],
    "Ekonomi":["Akuntansi","Manajemen","Bisnis"],
    "Manajemen":["Ekonomi","Bisnis","Akuntansi"],
    "Akuntansi":["Manajemen","Ekonomi","Bisnis"],
    "Bisnis":["Manajemen","Ekonomi","Akuntansi"],
    "Psikologi":["Ilmu Komunikasi","Sosiologi","Administrasi Publik"],
    "Ilmu Komunikasi":["Hubungan Internasional","Administrasi Publik","Psikologi"],
    "Hubungan Internasional":["Ilmu Komunikasi","Ilmu Politik","Sejarah"],
    "Administrasi Publik":["Ilmu Politik","Sosiologi","Ilmu Hukum"],
    "Sastra Inggris":["Pendidikan Bahasa Inggris","Hubungan Internasional","Ilmu Komunikasi"],
    "Pendidikan Bahasa Indonesia":["Sastra Inggris","Ilmu Komunikasi","Sosiologi"],
    "Pendidikan Bahasa Inggris":["Sastra Inggris","Hubungan Internasional","Ilmu Komunikasi"],
    "Sosiologi":["Ilmu Politik","Administrasi Publik","Psikologi"],
    "Ilmu Politik":["Sosiologi","Hubungan Internasional","Administrasi Publik"],
    "Sejarah":["Sosiologi","Geografi","Ilmu Politik"],
    "Geografi":["Sejarah","Sosiologi","Kesehatan Masyarakat"],
}

LABEL_STRATEGI = [
    "Intensif & Terstruktur",
    "Penguatan Mental",
    "Optimasi & Review",
    "Pertahankan & Tingkatkan"
]
DESKRIPSI_STRATEGI = {
    "Intensif & Terstruktur":{"icon":"🔴","deskripsi":"Kebiasaan belajar dan kondisi psikologis perlu ditingkatkan secara bersamaan.",
        "tips":["Buat jadwal belajar harian yang ketat dan konsisten","Mulai dari 2 jam/hari lalu tingkatkan bertahap","Gunakan metode Pomodoro","Cari teman belajar atau kelompok belajar","Konsultasi dengan guru/mentor"]},
    "Penguatan Mental":{"icon":"🟠","deskripsi":"Kebiasaan belajar sudah cukup baik, namun kondisi psikologis perlu diperkuat.",
        "tips":["Latihan mindfulness 10 menit sebelum belajar","Buat target kecil harian","Kurangi perbandingan diri","Tetapkan rutinitas tidur yang baik","Tryout rutin untuk membiasakan tekanan"]},
    "Optimasi & Review":{"icon":"🟡","deskripsi":"Kebiasaan dan mental sudah baik, tingkatkan kualitas review dan evaluasi.",
        "tips":["Perbanyak review soal yang pernah salah","Analisis pola kesalahan tiap subtes","Tryout minimal 2x/bulan","Buat catatan ringkasan materi","Fokus efisiensi waktu mengerjakan soal"]},
    "Pertahankan & Tingkatkan":{"icon":"🟢","deskripsi":"Kebiasaan belajar dan kondisi psikologis sudah sangat baik!",
        "tips":["Pertahankan konsistensi","Tingkatkan target skor tryout bertahap","Fokus manajemen waktu saat ujian","Bantu teman belajar","Jaga kesehatan fisik"]},
}


# ══════════════════════════════════════════════════════════════
# LOAD MODEL
# ══════════════════════════════════════════════════════════════
@st.cache_resource
def load_lgbm():
    for fname in ["lgbm_model_2_.pkl","lgbm_model.pkl","model_skor_utbk_asli.pkl"]:
        if os.path.exists(fname):
            try:
                with open(fname,"rb") as f:
                    return pickle.load(f), fname
            except: pass
    return None, None

lgbm_model, lgbm_fname = load_lgbm()


# ══════════════════════════════════════════════════════════════
# KALKULASI
# ══════════════════════════════════════════════════════════════
def get_bobot(jurusan):
    return BOBOT_MAP.get(jurusan, DEFAULT_BOBOT)

def hitung_tertimbang(skor, bobot):
    return sum(skor[k]*bobot[k] for k in SUBTES)

def ptn_info(kampus):
    return PTN_DATA.get(kampus, {"klaster":4,"min":535,"max":615,"label":"🔸 Klaster 4"})

def hitung_peluang(sw, kampus):
    info = ptn_info(kampus)
    mn,mx = info["min"],info["max"]
    gap = sw - mn
    if sw >= mx:      return "Sangat Aman","#4ade80",min(92.,75+(sw-mx)/mx*15)
    elif sw >= mn:    return "Aman","#4ade80",60+(sw-mn)/(mx-mn)*15
    elif sw >= mn-60: return "Kompetitif","#fb923c",30+(60+gap)/60*25
    elif sw >= mn-120:return "Berisiko","#ff6b6b",15.
    else:             return "Perlu Peningkatan","#ff6b6b",8.

def prediksi_lgbm(model, inp):
    try:
        feat = pd.DataFrame([{
            "Jam_Belajar":inp["jam_belajar"],"Hari_Belajar":inp["hari_belajar"],
            "Latihan_Soal":inp["latihan_soal"],"Frekuensi_Tryout":inp["frekuensi_tryout"],
            "Review_Soal":inp["review_soal"],"Fokus":inp["fokus"],
            "Percaya_Diri":inp["percaya_diri"],
            "Kecemasan_Rev":6-inp["kecemasan"],"Distraksi_Rev":6-inp["distraksi"],
        }])
        if hasattr(model,"feature_name_"):
            feat = feat.reindex(columns=model.feature_name_,fill_value=0)
        elif hasattr(model,"feature_names_in_"):
            feat = feat.reindex(columns=model.feature_names_in_,fill_value=0)
        kode = int(model.predict(feat)[0])
        label = LABEL_STRATEGI[kode] if kode < len(LABEL_STRATEGI) else LABEL_STRATEGI[-1]
        kepercayaan = None
        if hasattr(model,"predict_proba"):
            proba = model.predict_proba(feat)[0]
            kepercayaan = float(proba[kode])*100
        return {"sukses":True,"kode":kode,"strategi":label,"kepercayaan":kepercayaan,
                "detail":DESKRIPSI_STRATEGI.get(label,{})}
    except Exception as e:
        return {"sukses":False,"error":str(e)}

def hitung_semua(data):
    skor  = {k: data[k] for k in SUBTES}
    bobot = get_bobot(data["jurusan"])
    sw    = hitung_tertimbang(skor, bobot)
    rata  = np.mean(list(skor.values()))
    pl, pc, ppct = hitung_peluang(sw, data["kampus"])
    info  = ptn_info(data["kampus"])
    gap   = sw - info["min"]
    psiko = (data["fokus"]*1.5+data["percaya_diri"]*1.5+(6-data["kecemasan"])+(6-data["distraksi"]))/20*100
    konsist = min(100,(data["jam_belajar"]*2+data["hari_belajar"]*2.2+
                       data["latihan_soal"]*1.8+data["frekuensi_tryout"]*1.5+data["review_soal"]*1.5)*2)
    positif=(data["fokus"]*1.5+data["percaya_diri"]*1.5)*10
    negatif=(data["kecemasan"]*1.2+data["distraksi"]*1.2)*8
    stabilitas=max(0,min(100,positif-negatif+50))
    rgb=(stabilitas*0.6+konsist*0.4)
    if rgb>=75:   risk=("Rendah","✅","Kemungkinan perform sesuai atau di atas kemampuan")
    elif rgb>=60: risk=("Sedang","⚠️","Ada potensi fluktuasi performa, jaga konsistensi")
    else:         risk=("Tinggi","🔴","Risiko perform di bawah kemampuan, perlu perbaikan")
    lgbm_hasil = prediksi_lgbm(lgbm_model, data) if lgbm_model else None
    terpenuhi = pl in ("Sangat Aman","Aman")
    return {**data,"skor":skor,"bobot":bobot,"sw":sw,"rata":rata,
            "pl":pl,"pc":pc,"ppct":ppct,"info":info,"gap":gap,
            "psiko":psiko,"konsist":konsist,"stabilitas":stabilitas,"risk":risk,
            "lgbm_hasil":lgbm_hasil,"terpenuhi":terpenuhi,
            "alternatif":ALTERNATIF_MAP.get(data["jurusan"],[])}


# ══════════════════════════════════════════════════════════════
# CHART HELPERS — Semua dengan unik key untuk hindari duplicate ID
# ══════════════════════════════════════════════════════════════
CTHEME = dict(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',
              font=dict(family='Plus Jakarta Sans',color='#c8d3e0'),
              margin=dict(l=10,r=10,t=45,b=10))

def chart_radar(skor, bobot, jurusan, key=None):
    cats  = [SUBTES_LABEL[k] for k in SUBTES] + [SUBTES_LABEL[SUBTES[0]]]
    vals  = [skor[k] for k in SUBTES] + [skor[SUBTES[0]]]
    ideal = [min(SKOR_MAX, SKOR_MAX*bobot[k]*6) for k in SUBTES] + [min(SKOR_MAX,SKOR_MAX*bobot[SUBTES[0]]*6)]
    fig   = go.Figure()
    fig.add_trace(go.Scatterpolar(r=ideal,theta=cats,fill='toself',name='Profil Ideal Jurusan',
        fillcolor='rgba(245,166,35,.07)',line=dict(color='#f5a623',dash='dot',width=2)))
    fig.add_trace(go.Scatterpolar(r=vals,theta=cats,fill='toself',name='Skor Kamu',
        fillcolor='rgba(96,180,255,.15)',line=dict(color='#60b4ff',width=2.5)))
    fig.update_layout(**CTHEME,polar=dict(
        bgcolor='rgba(15,18,24,.9)',
        radialaxis=dict(range=[0,SKOR_MAX],gridcolor='#252b38',linecolor='#252b38',
                        tickfont=dict(size=9,color='#8b9ab0')),
        angularaxis=dict(gridcolor='#252b38',linecolor='#252b38',tickfont=dict(size=10,color='#c8d3e0'))),
        legend=dict(bgcolor='rgba(0,0,0,0)',orientation='h',x=.5,xanchor='center',y=-.14,
                    font=dict(color='#c8d3e0')),
        title=dict(text=f"Radar Skor TPS — {jurusan}",font=dict(size=13,color='#f0f4f8')),height=380)
    k = key or next_chart_key("radar")
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False}, key=k)

def chart_bar_subtes(skor, bobot, info, key=None):
    lbl   = [SUBTES_LABEL[k] for k in SUBTES]
    vals  = [skor[k] for k in SUBTES]
    tgt   = [min(SKOR_MAX,(info["min"]+info["max"])/2*bobot[k]*7) for k in SUBTES]
    clrs  = [SUBTES_COLOR[k] for k in SUBTES]
    fig   = go.Figure()
    fig.add_trace(go.Bar(name='Skor Kamu',x=lbl,y=vals,marker_color=clrs,marker_line_width=0,
        text=[f"{v}" for v in vals],textposition='outside',textfont=dict(size=10,color='#f0f4f8')))
    fig.add_trace(go.Scatter(name='Target Kampus',x=lbl,y=tgt,mode='markers+lines',
        marker=dict(symbol='diamond',size=9,color='#f5a623'),
        line=dict(color='#f5a623',dash='dot',width=1.5)))
    fig.update_layout(**CTHEME,barmode='group',
        xaxis=dict(tickfont=dict(size=9,color='#c8d3e0'),gridcolor='#252b38',linecolor='#252b38'),
        yaxis=dict(range=[0,SKOR_MAX*1.06],gridcolor='#171c25',linecolor='#252b38',
                   tickfont=dict(size=9,color='#c8d3e0')),
        legend=dict(bgcolor='rgba(0,0,0,0)',orientation='h',x=.5,xanchor='center',y=-.2,
                    font=dict(color='#c8d3e0')),
        title=dict(text="Skor Per Subtes vs Target Kampus",font=dict(size=13,color='#f0f4f8')),height=360)
    k = key or next_chart_key("bar_subtes")
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False}, key=k)

def chart_pipeline(skor, bobot, info, jurusan, key=None):
    lbl   = [SUBTES_LABEL[k] for k in SUBTES]
    aktual= [skor[k]*bobot[k] for k in SUBTES]
    ideal = [info["min"]*bobot[k] for k in SUBTES]
    clrs  = [SUBTES_COLOR[k] for k in SUBTES]
    fig   = go.Figure()
    fig.add_trace(go.Bar(name='Kontribusi Target Min',y=lbl,x=ideal,orientation='h',
        marker_color=['rgba(245,166,35,.15)']*7,marker_line_color='#f5a623',marker_line_width=1.5))
    fig.add_trace(go.Bar(name='Kontribusi Aktual',y=lbl,x=aktual,orientation='h',
        marker_color=clrs,text=[f"{v:.1f}" for v in aktual],
        textposition='inside',textfont=dict(size=10,color='#fff')))
    fig.update_layout(**CTHEME,barmode='overlay',
        xaxis=dict(title="Kontribusi ke Skor Total",gridcolor='#171c25',linecolor='#252b38',
                   tickfont=dict(size=9,color='#c8d3e0'),title_font=dict(color='#8b9ab0')),
        yaxis=dict(gridcolor='#252b38',linecolor='#252b38',tickfont=dict(size=10,color='#c8d3e0')),
        legend=dict(bgcolor='rgba(0,0,0,0)',orientation='h',x=.5,xanchor='center',y=-.12,
                    font=dict(color='#c8d3e0')),
        title=dict(text=f"Pipeline Kontribusi Subtes — {jurusan}",font=dict(size=13,color='#f0f4f8')),height=370)
    k = key or next_chart_key("pipeline")
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False}, key=k)

def chart_bobot(jurusan, key=None):
    bobot = get_bobot(jurusan)
    lbl   = [SUBTES_LABEL[k] for k in SUBTES]
    vals  = [bobot[k]*100 for k in SUBTES]
    clrs  = [SUBTES_COLOR[k] for k in SUBTES]
    fig   = go.Figure(go.Bar(x=lbl,y=vals,marker_color=clrs,marker_line_width=0,
        text=[f"{v:.0f}%" for v in vals],textposition='outside',textfont=dict(size=10,color='#f0f4f8')))
    fig.update_layout(**CTHEME,
        xaxis=dict(tickfont=dict(size=9,color='#c8d3e0'),gridcolor='#252b38'),
        yaxis=dict(range=[0,55],ticksuffix="%",gridcolor='#171c25',title="Bobot (%)",
                   title_font=dict(color='#8b9ab0'),tickfont=dict(size=9,color='#c8d3e0')),
        title=dict(text=f"Bobot Subtes — {jurusan}",font=dict(size=13,color='#f0f4f8')),height=300)
    k = key or next_chart_key("bobot")
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False}, key=k)

def chart_klaster(sw, key=None):
    klaster_info = [
        ("Klaster 1\nTop Tier", 780, 880, "#ff6b6b"),
        ("Klaster 2\nMng Atas",  680, 790, "#fb923c"),
        ("Klaster 3\nMenengah",  600, 690, "#4ade80"),
        ("Klaster 4\nRegional",  530, 630, "#60b4ff"),
    ]
    fig = go.Figure()
    for lbl,mn,mx,clr in klaster_info:
        rgba = f"rgba({int(clr[1:3],16)},{int(clr[3:5],16)},{int(clr[5:7],16)},0.18)"
        fig.add_trace(go.Bar(x=[lbl],y=[mx-mn],base=[mn],name=lbl,
            marker_color=rgba,marker_line_color=clr,marker_line_width=2,showlegend=False,
            text=[f"{mn}–{mx}"],textposition='inside',textfont=dict(size=10,color=clr)))
    fig.add_hline(y=sw,line_dash="dash",line_color="#c084fc",line_width=2.5,
        annotation_text=f"  Skor kamu: {sw:.0f}",annotation_font_color="#c084fc",
        annotation_font_size=11)
    fig.update_layout(**CTHEME,barmode='overlay',
        xaxis=dict(gridcolor='#252b38',linecolor='#252b38',tickfont=dict(size=10,color='#c8d3e0')),
        yaxis=dict(range=[400,SKOR_MAX],gridcolor='#171c25',linecolor='#252b38',
                   title="Rentang Skor Aman",title_font=dict(color='#8b9ab0'),
                   tickfont=dict(size=9,color='#c8d3e0')),
        title=dict(text="Posisi Skor vs Klaster PTN",font=dict(size=13,color='#f0f4f8')),height=360)
    k = key or next_chart_key("klaster")
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False}, key=k)

def chart_ptn_klaster(sw, klaster_no, key=None):
    ptn_kl = {k:v for k,v in PTN_DATA.items() if v['klaster']==klaster_no}
    fig=go.Figure()
    for nm,d in ptn_kl.items():
        short = nm.split("(")[0].strip()[:22]
        clr   = "#60b4ff"
        rgba  = "rgba(96,180,255,0.18)"
        fig.add_trace(go.Bar(x=[short],y=[d['max']-d['min']],base=[d['min']],name=short,
            marker_color=rgba,marker_line_color=clr,marker_line_width=1.5,showlegend=False,
            text=[f"{d['min']}–{d['max']}"],textposition='inside',textfont=dict(size=9,color='#f0f4f8')))
    fig.add_hline(y=sw,line_dash="dash",line_color="#f5a623",line_width=2,
        annotation_text=f"  Skor kamu: {sw:.0f}",annotation_font_color="#f5a623",
        annotation_font_size=11)
    fig.update_layout(**CTHEME,barmode='overlay',
        yaxis=dict(range=[400,SKOR_MAX],gridcolor='#171c25',title="Rentang Skor",
                   title_font=dict(color='#8b9ab0'),tickfont=dict(size=9,color='#c8d3e0')),
        xaxis=dict(gridcolor='#252b38',tickfont=dict(size=9,color='#c8d3e0')),
        title=dict(text=f"PTN Klaster {klaster_no}",font=dict(size=13,color='#f0f4f8')),height=300)
    k = key or next_chart_key("ptn_klaster")
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False}, key=k)


# ══════════════════════════════════════════════════════════════
# PDF EXPORT
# ══════════════════════════════════════════════════════════════
def generate_pdf_html(r):
    now  = datetime.datetime.now().strftime("%d %B %Y, %H:%M")
    nama = r.get("nama","—")
    bobot_rows="".join(
        f"<tr><td>{SUBTES_LABEL[k]}</td><td>{int(r['bobot'][k]*100)}%</td>"
        f"<td>{r['skor'][k]}</td><td>{r['skor'][k]*r['bobot'][k]:.1f}</td></tr>" for k in SUBTES)
    altj=", ".join(r['alternatif']) if r['alternatif'] else "—"
    lgbm_txt=""
    if r.get("lgbm_hasil") and r["lgbm_hasil"].get("sukses"):
        h=r["lgbm_hasil"]
        kpct=f"{h['kepercayaan']:.1f}%" if h.get('kepercayaan') else "—"
        lgbm_txt=f"<p><strong>Rekomendasi Strategi SKORIA AI:</strong> {h['strategi']} (kepercayaan: {kpct})</p>"
    gc="green" if r['gap']>=0 else "red"
    pc="green" if r['ppct']>=65 else "orange" if r['ppct']>=35 else "red"
    return f"""<!DOCTYPE html><html lang="id"><head><meta charset="UTF-8">
<title>Laporan SKORIA — {nama}</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700&family=Syne:wght@700;800&display=swap');
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:'Plus Jakarta Sans',sans-serif;font-size:11pt;color:#1e293b;background:#fff;padding:1.5cm 2cm}}
h1{{font-size:20pt;font-weight:800;color:#0f172a;margin-bottom:4px;font-family:'Syne',sans-serif}}
h2{{font-size:12pt;font-weight:700;color:#0f172a;margin:16px 0 7px;border-bottom:2px solid #f5a623;padding-bottom:3px}}
p{{font-size:10pt;line-height:1.6;color:#374151;margin-bottom:5px}}
.hdr{{background:linear-gradient(135deg,#07090f,#0d1a30);color:#fff;padding:1.2cm 1.5cm;border-radius:10px;margin-bottom:1cm}}
.hdr .brand{{font-family:'Syne',sans-serif;font-size:14pt;font-weight:800;color:#f5a623;margin-bottom:4px}}
.hdr .sub{{color:#8b9ab0;font-size:9pt;margin-top:3px}}
.kpi-row{{display:flex;gap:10px;margin-bottom:10px}}
.kpi{{flex:1;border:1px solid #e2e8f0;border-radius:8px;padding:10px;text-align:center}}
.kpi .val{{font-size:20pt;font-weight:800;font-family:'Syne',sans-serif}}
.kpi .lbl{{font-size:8pt;color:#64748b;text-transform:uppercase;letter-spacing:.06em}}
.green{{color:#16a34a}}.yellow{{color:#ca8a04}}.red{{color:#dc2626}}.blue{{color:#1d4ed8}}
table{{width:100%;border-collapse:collapse;font-size:9.5pt;margin-bottom:9px}}
th{{background:#f1f5f9;text-align:left;padding:5px 9px;font-weight:600;border:1px solid #e2e8f0}}
td{{padding:5px 9px;border:1px solid #e2e8f0;color:#374151}}
tr:nth-child(even) td{{background:#f8fafc}}
.footer{{margin-top:1cm;font-size:8pt;color:#94a3b8;text-align:center;border-top:1px solid #e2e8f0;padding-top:7px}}
@media print{{body{{padding:.8cm 1cm}}.no-print{{display:none}}}}
</style></head><body>
<div class="hdr">
  <div class="brand">🎯 SKORIA</div>
  <h1>AI UTBK Readiness Report</h1>
  <div class="sub">Laporan Kesiapan UTBK · {now}</div>
</div>
<h2>👤 Profil Siswa</h2>
<table><tr><th>Nama</th><td>{nama}</td><th>Jurusan Target</th><td>{r['jurusan']}</td></tr>
<tr><th>Kampus Target</th><td>{r['kampus']}</td><th>Klaster</th><td>{r['info']['label']}</td></tr></table>
<h2>📊 Ringkasan Hasil</h2>
<div class="kpi-row">
<div class="kpi"><div class="lbl">Skor Tertimbang</div><div class="val {gc}">{r['sw']:.0f}</div><div class="lbl">dari {SKOR_MAX}</div></div>
<div class="kpi"><div class="lbl">Rata-rata Subtes</div><div class="val blue">{r['rata']:.0f}</div></div>
<div class="kpi"><div class="lbl">Peluang Lolos</div><div class="val {pc}">{r['ppct']:.0f}%</div><div class="lbl">{r['pl']}</div></div>
<div class="kpi"><div class="lbl">Gap vs Minimum</div><div class="val {gc}">{'+' if r['gap']>=0 else ''}{r['gap']:.0f}</div></div>
</div>
{lgbm_txt}
<h2>📋 Bobot & Skor Subtes</h2>
<table><tr><th>Subtes</th><th>Bobot ({r['jurusan']})</th><th>Skor (maks {SKOR_MAX})</th><th>Kontribusi</th></tr>
{bobot_rows}
<tr><th colspan="2">Total Skor Tertimbang</th><th colspan="2"><strong>{r['sw']:.1f}</strong></th></tr></table>
<h2>🧠 Psikologis & Kebiasaan</h2>
<table>
<tr><th>Fokus</th><td>{r['fokus']}/5</td><th>Percaya Diri</th><td>{r['percaya_diri']}/5</td></tr>
<tr><th>Kecemasan</th><td>{r['kecemasan']}/5</td><th>Distraksi</th><td>{r['distraksi']}/5</td></tr>
<tr><th>Kesiapan Mental</th><td>{r['psiko']:.0f}/100</td><th>Konsistensi Belajar</th><td>{r['konsist']:.0f}/100</td></tr>
<tr><th>Risiko Underperform</th><td colspan="3">{r['risk'][0]}</td></tr></table>
<h2>🎓 Jurusan Alternatif (Formalitas)</h2><p>{altj}</p>
<p style="font-size:9pt;color:#64748b;"><em>Alternatif disajikan sebagai formalitas. Fokus tetap pada jurusan target.</em></p>
<div class="footer">SKORIA — AI UTBK Intelligence · Laporan ini bersifat estimasi berdasarkan data yang diinput</div>
<div class="no-print" style="margin-top:18px;text-align:center;">
<button onclick="window.print()" style="padding:9px 22px;background:#f5a623;border:none;
  border-radius:8px;font-weight:700;cursor:pointer;font-size:11pt;font-family:'Syne',sans-serif">
  🖨️ Print / Save as PDF</button>
</div></body></html>"""


# ══════════════════════════════════════════════════════════════
# NAV BAR
# ══════════════════════════════════════════════════════════════
def render_nav():
    p = st.session_state.page
    s1 = "done" if p in ['survey','result'] else "active" if p=='home' else ""
    s2 = "done" if p=='result' else "active" if p=='survey' else ""
    s3 = "active" if p=='result' else ""
    st.markdown(f"""<div class="nav">
      <div class="nav-brand">🎯 {APP_NAME} <span>AI UTBK Intelligence</span></div>
      <div class="nav-step {s1}">{'✓' if p in ['survey','result'] else '①'} Beranda</div>
      <div class="nav-step {s2}">{'✓' if p=='result' else '②'} Input Data</div>
      <div class="nav-step {s3}">③ Hasil Analisis</div>
    </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# PAGE: HOME
# ══════════════════════════════════════════════════════════════
def page_home():
    st.markdown(f"""
    <div class="hero">
      <h1>{APP_NAME} — Analisis Kesiapan<br><span>UTBK</span> Berbasis AI</h1>
      <p>Platform cerdas berbasis LightGBM untuk memahami peluang, gap skor,<br>
         dan strategi belajar yang dipersonalisasi sesuai profil akademik & psikologis kamu.</p>
    </div>""", unsafe_allow_html=True)

    c1,c2,c3,c4 = st.columns(4)
    for col,(ico,ttl,desc) in zip([c1,c2,c3,c4],[
        ("📡","Radar Chart TPS","Visualisasi 7 subtes vs profil ideal jurusan target"),
        ("📊","Bar & Pipeline","Diagram batang skor + pipeline kontribusi per subtes"),
        ("🎯","Gap Analysis","Selisih skor vs minimum kampus & klaster PTN"),
        ("📄","Export PDF","Simpan laporan lengkap sebagai PDF"),
    ]):
        with col:
            st.markdown(f"""<div class="card" style="text-align:center;padding:1.4rem">
              <div style="font-size:2rem;margin-bottom:.5rem">{ico}</div>
              <div style="font-family:'Syne',sans-serif;font-weight:700;font-size:.9rem;
                   margin-bottom:.35rem;color:#f0f4f8">{ttl}</div>
              <div style="font-size:.77rem;color:#8b9ab0;line-height:1.5">{desc}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown(f'<div class="sec">🤖 Tentang {APP_NAME}</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="al al-i">
      <h4>Perkenalkan {APP_NAME} — Score + Aria = AI Navigator UTBK-mu</h4>
      <strong>{APP_NAME}</strong> mengintegrasikan <strong>Model LightGBM</strong> terlatih dengan pendekatan holistik:
      <ul>
        <li>📊 Analisis akademik tertimbang sesuai bobot jurusan target</li>
        <li>🧠 Evaluasi psikologis: fokus, percaya diri, kecemasan, distraksi</li>
        <li>📚 Analisis kebiasaan belajar & prediksi strategi optimal dari model AI</li>
        <li>🎯 Gap analysis berbasis klaster PTN (skor skala 200–1000)</li>
        <li>📡 Radar chart, bar chart, pipeline chart, dan tabel interaktif</li>
      </ul>
    </div>""", unsafe_allow_html=True)

    if lgbm_model:
        st.markdown(f'<div class="al al-s"><h4>✅ Model AI Aktif</h4>File: <code>{lgbm_fname}</code> — Prediksi strategi belajar siap digunakan.</div>',
                    unsafe_allow_html=True)
    else:
        st.markdown('<div class="al al-w"><h4>⚠️ Model AI Tidak Ditemukan</h4>Letakkan file <code>lgbm_model_2_.pkl</code> di folder yang sama. Kalkulasi manual akan digunakan sebagai fallback.</div>',
                    unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚀  Mulai Analisis Sekarang", type="primary"):
        st.session_state.page='survey'; st.session_state.step=1; st.rerun()


# ══════════════════════════════════════════════════════════════
# PAGE: SURVEY — 4 STEPS
# ══════════════════════════════════════════════════════════════
def step_bar(cur):
    steps=["👤 Profil","📊 Skor TPS","🧠 Psikologis","📚 Kebiasaan"]
    html='<div class="step-row">'
    for i,s in enumerate(steps,1):
        cls="active" if i==cur else "done" if i<cur else ""
        mk="✓" if i<cur else str(i)
        html+=f'<div class="step-item {cls}"><span class="step-num">{mk}</span>{s}</div>'
    st.markdown(html+"</div>",unsafe_allow_html=True)

def show_bobot_chips(jurusan):
    bobot=get_bobot(jurusan)
    chips="".join(
        f'<div class="bobot-chip"><span class="sk">{k}</span><span class="bv">{int(bobot[k]*100)}%</span></div>'
        for k in SUBTES)
    st.markdown(f'<div style="display:flex;flex-wrap:wrap;gap:4px;margin-top:.5rem">{chips}</div>',unsafe_allow_html=True)

def survey_step1():
    st.markdown('<div class="form-box">', unsafe_allow_html=True)
    st.markdown('<h3>👤 Profil Siswa</h3>', unsafe_allow_html=True)
    nama    = st.text_input("Nama Lengkap", value=st.session_state.data.get("nama",""), placeholder="Nama kamu...")
    jurusan = st.selectbox("Target Jurusan", DAFTAR_JURUSAN,
                           index=DAFTAR_JURUSAN.index(st.session_state.data.get("jurusan",DAFTAR_JURUSAN[0])))
    kampus  = st.selectbox("Target Kampus (PTN)", DAFTAR_PTN,
                           index=DAFTAR_PTN.index(st.session_state.data.get("kampus",DAFTAR_PTN[0])))
    st.markdown("---")
    st.markdown(f"<p style='color:#c8d3e0;font-weight:600;font-size:.88rem'>📋 Bobot Subtes untuk Jurusan <strong style='color:#f5a623'>{jurusan}</strong>:</p>", unsafe_allow_html=True)
    show_bobot_chips(jurusan)
    info = ptn_info(kampus)
    st.markdown(f"""<div class="al al-i" style="margin-top:.8rem">
      <h4>{info['label']} — {kampus}</h4>
      Rentang skor aman: <strong>{info['min']} – {info['max']}</strong> (skala 1000)
    </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    if st.button("Lanjut → Skor TPS", type="primary"):
        if not nama.strip():
            st.error("Nama harus diisi!")
        else:
            st.session_state.data.update({"nama":nama,"jurusan":jurusan,"kampus":kampus})
            st.session_state.step=2; st.rerun()

def survey_step2():
    st.markdown('<div class="form-box">', unsafe_allow_html=True)
    st.markdown('<h3>📊 Skor TPS (Tes Potensi Skolastik)</h3>', unsafe_allow_html=True)
    st.caption(f"Skala skor: {SKOR_MIN} – {SKOR_MAX} · Masukkan skor tryout terbaru per subtes")
    skor={}
    pairs=[("PU","PPU"),("PBM","PK"),("LBI","LBE"),("PM",None)]
    for pair in pairs:
        cols=st.columns(2)
        for col,k in zip(cols,pair):
            if k is None: continue
            with col:
                skor[k]=st.slider(f"{SUBTES_LABEL[k]} ({k})",SKOR_MIN,SKOR_MAX,
                                  st.session_state.data.get(k,500),step=5,key=f"sl_{k}")
    jurusan=st.session_state.data.get("jurusan",DAFTAR_JURUSAN[0])
    bobot=get_bobot(jurusan)
    # Radar di step survey — pakai key unik
    cats  = [SUBTES_LABEL[k] for k in SUBTES] + [SUBTES_LABEL[SUBTES[0]]]
    vals  = [skor[k] for k in SUBTES] + [skor[SUBTES[0]]]
    ideal = [min(SKOR_MAX, SKOR_MAX*bobot[k]*6) for k in SUBTES] + [min(SKOR_MAX,SKOR_MAX*bobot[SUBTES[0]]*6)]
    fig   = go.Figure()
    fig.add_trace(go.Scatterpolar(r=ideal,theta=cats,fill='toself',name='Profil Ideal Jurusan',
        fillcolor='rgba(245,166,35,.07)',line=dict(color='#f5a623',dash='dot',width=2)))
    fig.add_trace(go.Scatterpolar(r=vals,theta=cats,fill='toself',name='Skor Kamu',
        fillcolor='rgba(96,180,255,.15)',line=dict(color='#60b4ff',width=2.5)))
    fig.update_layout(**CTHEME,polar=dict(
        bgcolor='rgba(15,18,24,.9)',
        radialaxis=dict(range=[0,SKOR_MAX],gridcolor='#252b38',linecolor='#252b38',
                        tickfont=dict(size=9,color='#8b9ab0')),
        angularaxis=dict(gridcolor='#252b38',linecolor='#252b38',tickfont=dict(size=10,color='#c8d3e0'))),
        legend=dict(bgcolor='rgba(0,0,0,0)',orientation='h',x=.5,xanchor='center',y=-.14,
                    font=dict(color='#c8d3e0')),
        title=dict(text=f"Radar Skor TPS — {jurusan}",font=dict(size=13,color='#f0f4f8')),height=380)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False}, key="survey_radar")
    st.markdown('</div>', unsafe_allow_html=True)
    cb,cn=st.columns([1,5])
    with cb:
        if st.button("← Kembali"): st.session_state.step=1; st.rerun()
    with cn:
        if st.button("Lanjut → Psikologis",type="primary"):
            st.session_state.data.update(skor); st.session_state.step=3; st.rerun()

def survey_step3():
    st.markdown('<div class="form-box">', unsafe_allow_html=True)
    st.markdown('<h3>🧠 Kondisi Psikologis</h3>', unsafe_allow_html=True)
    st.caption("1 = Sangat Rendah · 5 = Sangat Tinggi")
    c1,c2=st.columns(2)
    with c1:
        fokus=st.slider("🎯 Kemampuan Fokus Belajar",1,5,st.session_state.data.get("fokus",3))
        percaya_diri=st.slider("💪 Percaya Diri",1,5,st.session_state.data.get("percaya_diri",3))
    with c2:
        kecemasan=st.slider("😰 Tingkat Kecemasan (1=tenang, 5=sangat cemas)",1,5,st.session_state.data.get("kecemasan",3))
        distraksi=st.slider("📱 Mudah Terdistraksi (1=fokus, 5=sangat mudah)",1,5,st.session_state.data.get("distraksi",3))
    psiko=(fokus*1.5+percaya_diri*1.5+(6-kecemasan)+(6-distraksi))/20*100
    pc="c-green" if psiko>=65 else "c-gold" if psiko>=45 else "c-red"
    st.markdown(f"""<div class="card" style="text-align:center;margin-top:.8rem">
      <div class="kpi-lbl">Indeks Kesiapan Mental</div>
      <div class="kpi-val {pc}">{psiko:.0f}<span style="font-size:1rem;color:#8b9ab0">/100</span></div>
    </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    cb,cn=st.columns([1,5])
    with cb:
        if st.button("← Kembali"): st.session_state.step=2; st.rerun()
    with cn:
        if st.button("Lanjut → Kebiasaan Belajar",type="primary"):
            st.session_state.data.update({"fokus":fokus,"percaya_diri":percaya_diri,"kecemasan":kecemasan,"distraksi":distraksi})
            st.session_state.step=4; st.rerun()

def survey_step4():
    st.markdown('<div class="form-box">', unsafe_allow_html=True)
    st.markdown('<h3>📚 Kebiasaan Belajar</h3>', unsafe_allow_html=True)
    map_jam={"< 1 jam":1,"1–2 jam":2,"3–4 jam":3,"5–6 jam":4,"> 6 jam":5}
    map_hari={"≤ 1 hari":1,"2 hari":2,"3 hari":3,"4–5 hari":4,"≥ 6 hari":5}
    c1,c2=st.columns(2)
    with c1:
        jam_str=st.selectbox("⏰ Jam belajar/hari",list(map_jam.keys()),
                             index=st.session_state.data.get("jam_belajar",3)-1)
        hari_str=st.selectbox("📅 Hari belajar/minggu",list(map_hari.keys()),
                              index=st.session_state.data.get("hari_belajar",3)-1)
        latihan=st.slider("✏️ Frekuensi latihan soal/minggu (1–5)",1,5,st.session_state.data.get("latihan_soal",3))
    with c2:
        tryout=st.slider("📝 Frekuensi tryout/bulan (1–5)",1,5,st.session_state.data.get("frekuensi_tryout",2))
        review=st.slider("🔄 Frekuensi review soal salah (1–5)",1,5,st.session_state.data.get("review_soal",3))
    jb=map_jam[jam_str]; hb=map_hari[hari_str]
    konsist=min(100,(jb*2+hb*2.2+latihan*1.8+tryout*1.5+review*1.5)*2)
    kc="c-green" if konsist>=65 else "c-gold" if konsist>=45 else "c-red"
    st.markdown(f"""<div class="card" style="text-align:center;margin-top:.8rem">
      <div class="kpi-lbl">Indeks Konsistensi Belajar</div>
      <div class="kpi-val {kc}">{konsist:.0f}<span style="font-size:1rem;color:#8b9ab0">/100</span></div>
    </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    cb,cn=st.columns([1,5])
    with cb:
        if st.button("← Kembali"): st.session_state.step=3; st.rerun()
    with cn:
        if st.button("🎯  Lihat Hasil Analisis",type="primary"):
            st.session_state.data.update({"jam_belajar":jb,"hari_belajar":hb,
                "latihan_soal":latihan,"frekuensi_tryout":tryout,"review_soal":review})
            st.session_state.result=hitung_semua(st.session_state.data)
            st.session_state.page='result'; st.rerun()

def page_survey():
    step_bar(st.session_state.step)
    {1:survey_step1,2:survey_step2,3:survey_step3,4:survey_step4}[st.session_state.step]()


# ══════════════════════════════════════════════════════════════
# PAGE: RESULT
# ══════════════════════════════════════════════════════════════
def prog_bar(label,val,color):
    st.markdown(f"""<div class="prog-wrap">
      <div class="prog-lbl"><span>{label}</span><span style="color:{color};font-weight:700">{val:.0f}/100</span></div>
      <div class="prog-bg"><div class="prog-fill" style="width:{val:.0f}%;background:{color}"></div></div>
    </div>""", unsafe_allow_html=True)

def page_result():
    r=st.session_state.result
    if not r:
        st.session_state.page='home'; st.rerun()

    nama=r.get("nama","Pejuang UTBK")
    jam=datetime.datetime.now().hour
    salam="Selamat pagi" if jam<11 else "Selamat siang" if jam<15 else "Selamat sore" if jam<18 else "Selamat malam"

    st.markdown(f"""<div class="hero" style="padding:2rem 2.5rem">
      <h1 style="font-size:1.75rem!important">{salam}, <span>{nama}!</span> 👋</h1>
      <p>Hasil analisis <strong style="color:#f5a623">SKORIA</strong> untuk jurusan 
         <strong style="color:#f5a623">{r['jurusan']}</strong>
         di <strong style="color:#60b4ff">{r['kampus']}</strong></p>
    </div>""", unsafe_allow_html=True)

    # ── KPI ──
    kc="c-green" if r['pl'] in ("Sangat Aman","Aman") else "c-orange" if r['pl']=="Kompetitif" else "c-red"
    gc="c-green" if r['gap']>=0 else "c-red"
    pc="c-green" if r['ppct']>=65 else "c-orange" if r['ppct']>=35 else "c-red"
    rc="c-green" if r['risk'][0]=="Rendah" else "c-orange" if r['risk'][0]=="Sedang" else "c-red"
    k1,k2,k3,k4,k5=st.columns(5)
    for col,lbl,val,cls,sub in [
        (k1,"Skor Tertimbang",f"{r['sw']:.0f}",kc,f"dari {SKOR_MAX}"),
        (k2,"Rata-rata Subtes",f"{r['rata']:.0f}","c-blue","7 subtes"),
        (k3,"Peluang Lolos",f"{r['ppct']:.0f}%",pc,r['pl']),
        (k4,"Gap vs Minimum",f"{'+' if r['gap']>=0 else ''}{r['gap']:.0f}",gc,f"Min {r['info']['min']}"),
        (k5,"Risiko Underperform",r['risk'][0],rc,r['risk'][1]),
    ]:
        with col:
            st.markdown(f"""<div class="card">
              <div class="kpi-lbl">{lbl}</div>
              <div class="kpi-val {cls}">{val}</div>
              <div class="kpi-sub">{sub}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── LGBM Banner ──
    if r.get("lgbm_hasil") and r["lgbm_hasil"].get("sukses"):
        h=r["lgbm_hasil"]; d=h.get("detail",{})
        kpct=f"{h['kepercayaan']:.1f}%" if h.get("kepercayaan") else ""
        tips="".join(f"<li>{t}</li>" for t in d.get("tips",[]))
        st.markdown(f"""<div class="al al-s">
          <h4>🤖 Rekomendasi Strategi SKORIA AI — {d.get('icon','')} {h['strategi']} &nbsp;
            <span style="font-size:.8rem;font-weight:500;color:#8b9ab0">Kepercayaan: {kpct}</span></h4>
          <em>{d.get('deskripsi','')}</em>
          <ul style="margin-top:.4rem">{tips}</ul>
        </div>""", unsafe_allow_html=True)

    # ── Status Banner ──
    if r['pl']=="Sangat Aman":
        st.markdown(f"""<div class="al al-s"><h4>🎯 Status: SANGAT AMAN</h4>
          Skor tertimbang <strong>{r['sw']:.0f}</strong> melampaui batas maksimum aman {r['info']['max']}.
          Fokus: pertahankan performa & jaga kondisi mental menjelang hari H.</div>""", unsafe_allow_html=True)
    elif r['pl']=="Aman":
        st.markdown(f"""<div class="al al-s"><h4>✅ Status: AMAN</h4>
          Skor {r['sw']:.0f} dalam zona aman ({r['info']['min']}–{r['info']['max']}).
          Tingkatkan <strong>{r['info']['max']-r['sw']:.0f} poin</strong> lagi untuk zona sangat aman.</div>""", unsafe_allow_html=True)
    elif r['pl']=="Kompetitif":
        st.markdown(f"""<div class="al al-w"><h4>⚡ Status: KOMPETITIF</h4>
          Butuh <strong>+{r['info']['min']-r['sw']:.0f} poin</strong> untuk zona aman.
          Intensifkan latihan pada subtes berbobot tinggi.</div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""<div class="al al-d"><h4>🔴 Status: PERLU PENINGKATAN</h4>
          Gap <strong>{abs(r['gap']):.0f} poin</strong> dari minimum. Pertimbangkan bimbingan intensif.</div>""", unsafe_allow_html=True)

    # ── TABS ──
    t1,t2,t3,t4,t5,t6=st.tabs([
        "📡 Radar & Skor TPS",
        "📊 Analisis Kampus",
        "🔀 Pipeline & Bobot",
        "🎓 Jurusan & Alternatif",
        "🚀 Strategi Belajar",
        "📄 Export PDF",
    ])

    # ═══ TAB 1: RADAR + BAR ═══
    with t1:
        st.markdown('<div class="sec">📡 Radar Profil TPS vs Profil Ideal Jurusan</div>', unsafe_allow_html=True)
        chart_radar(r['skor'],r['bobot'],r['jurusan'], key="result_radar_t1")

        st.markdown('<div class="sec">📊 Bar Chart Skor Per Subtes vs Target Kampus</div>', unsafe_allow_html=True)
        chart_bar_subtes(r['skor'],r['bobot'],r['info'], key="result_bar_t1")

        st.markdown('<div class="sec">📋 Tabel Detail Skor Per Subtes</div>', unsafe_allow_html=True)
        df_sub=pd.DataFrame([{
            "Subtes":SUBTES_LABEL[k],
            "Bobot":f"{r['bobot'][k]*100:.0f}%",
            "Skor Kamu":r['skor'][k],
            "Kontribusi":f"{r['skor'][k]*r['bobot'][k]:.1f}",
            "Target Kampus":f"{(r['info']['min']+r['info']['max'])/2*r['bobot'][k]*7:.0f}",
            "Gap":f"{r['skor'][k]-(r['info']['min']+r['info']['max'])/2*r['bobot'][k]*7:+.0f}",
            "Status":"✅ Kuat" if r['skor'][k]>=650 else "⚡ Sedang" if r['skor'][k]>=450 else "🔴 Lemah",
        } for k in SUBTES])
        st.dataframe(df_sub,use_container_width=True,hide_index=True)

    # ═══ TAB 2: ANALISIS KAMPUS ═══
    with t2:
        st.markdown('<div class="sec">📊 Posisi Skor vs Klaster PTN</div>', unsafe_allow_html=True)
        chart_klaster(r['sw'], key="result_klaster_t2")

        st.markdown(f'<div class="sec">🏛️ PTN Klaster {r["info"]["klaster"]} — Perbandingan</div>', unsafe_allow_html=True)
        chart_ptn_klaster(r['sw'],r['info']['klaster'], key="result_ptn_t2")

        st.markdown('<div class="sec">📋 Tabel Perbandingan Semua Klaster</div>', unsafe_allow_html=True)
        kl_data=[(1,780,880,"⭐ Klaster 1 — Top Tier"),(2,680,790,"🔷 Klaster 2 — Mng Atas"),
                 (3,600,690,"🔹 Klaster 3 — Menengah"),(4,530,630,"🔸 Klaster 4 — Regional")]
        rows=[]
        for kno,mn,mx,kname in kl_data:
            g=r['sw']-mn
            if r['sw']>=mx: st_kl,p_kl="🎯 Sangat Aman","~85%"
            elif r['sw']>=mn: st_kl,p_kl="✅ Aman","~70%"
            elif r['sw']>=mn-60: st_kl,p_kl="⚡ Kompetitif","~40%"
            else: st_kl,p_kl="🔴 Berisiko","~15%"
            rows.append({"Klaster":kname,"Rentang Skor":f"{mn}–{mx}",
                         "Skor Kamu":f"{r['sw']:.0f}","Gap":f"{g:+.0f}",
                         "Status":st_kl,"Est. Peluang":p_kl})
        st.dataframe(pd.DataFrame(rows),use_container_width=True,hide_index=True)

        st.markdown('<div class="sec">🎯 Detail Target Kampus</div>', unsafe_allow_html=True)
        d1,d2,d3=st.columns(3)
        with d1: st.metric("Skor Minimum",r['info']['min'])
        with d2: st.metric("Skor Sangat Aman",r['info']['max'])
        with d3: st.metric("Skor Kamu (Tertimbang)",f"{r['sw']:.0f}",
                           delta=f"{r['gap']:+.0f} vs minimum",
                           delta_color="normal" if r['gap']>=0 else "inverse")

    # ═══ TAB 3: PIPELINE & BOBOT ═══
    with t3:
        st.markdown('<div class="sec">🔀 Pipeline Kontribusi Subtes → Skor Total</div>', unsafe_allow_html=True)
        st.caption("Batang berwarna = kontribusi aktual per subtes. Batang transparan = kontribusi target minimum kampus.")
        chart_pipeline(r['skor'],r['bobot'],r['info'],r['jurusan'], key="result_pipeline_t3")

        st.markdown(f'<div class="sec">📐 Bobot Subtes — {r["jurusan"]}</div>', unsafe_allow_html=True)
        chart_bobot(r['jurusan'], key="result_bobot_t3")  # KEY UNIK — fix duplicate!

        st.markdown('<div class="sec">📋 Tabel Bobot & Kontribusi</div>', unsafe_allow_html=True)
        df_b=pd.DataFrame([{
            "Subtes":SUBTES_LABEL[k],
            "Bobot":f"{r['bobot'][k]*100:.0f}%",
            "Skor":r['skor'][k],
            "Kontribusi Aktual":f"{r['skor'][k]*r['bobot'][k]:.1f}",
            "Kontribusi Target":f"{r['info']['min']*r['bobot'][k]:.1f}",
            "Selisih":f"{(r['skor'][k]-r['info']['min'])*r['bobot'][k]:+.1f}",
        } for k in SUBTES]+[{
            "Subtes":"TOTAL","Bobot":"100%","Skor":"—",
            "Kontribusi Aktual":f"{r['sw']:.1f}",
            "Kontribusi Target":f"{r['info']['min']:.0f}",
            "Selisih":f"{r['gap']:+.1f}",
        }])
        st.dataframe(df_b,use_container_width=True,hide_index=True)

        st.markdown('<div class="sec">📊 Perbandingan Bobot Antar Jurusan</div>', unsafe_allow_html=True)
        with st.expander("Lihat tabel bobot lengkap semua jurusan"):
            rows_b=[]
            for j,b in BOBOT_MAP.items():
                row={"Jurusan":j}
                row.update({f"{k} (%)":f"{b[k]*100:.0f}" for k in SUBTES})
                rows_b.append(row)
            st.dataframe(pd.DataFrame(rows_b),use_container_width=True,hide_index=True)

    # ═══ TAB 4: JURUSAN & ALTERNATIF ═══
    with t4:
        st.markdown(f'<div class="sec">🎓 Analisis Jurusan Target — {r["jurusan"]}</div>', unsafe_allow_html=True)

        if r['terpenuhi']:
            st.markdown(f"""<div class="al al-s">
              <h4>🎯 FOKUS KE JURUSAN TARGET: {r['jurusan']}</h4>
              Peluang lolos kamu sudah <strong>{r['pl']}</strong> ({r['ppct']:.0f}%) — tidak perlu berpindah jurusan.
              Pertahankan performa dan tingkatkan konsistensi belajar menjelang UTBK.
            </div>""", unsafe_allow_html=True)

            st.markdown(f"<p style='color:#c8d3e0;font-weight:600;font-size:.88rem;margin:.5rem 0'>📋 Bobot subtes untuk <strong style='color:#f5a623'>{r['jurusan']}</strong> (fokus belajar kamu):</p>", unsafe_allow_html=True)
            show_bobot_chips(r['jurusan'])

            col_a,col_b=st.columns([1,1])
            with col_a:
                chart_bobot(r['jurusan'], key="result_bobot_t4_main")  # KEY UNIK berbeda dari t3!
            with col_b:
                st.markdown("<p style='color:#c8d3e0;font-weight:600;font-size:.88rem;margin-bottom:.8rem'>📈 Indikator Kesiapan:</p>", unsafe_allow_html=True)
                prog_bar("Kesiapan Mental",r['psiko'],"#60b4ff")
                prog_bar("Konsistensi Belajar",r['konsist'],"#4ade80")
                prog_bar("Stabilitas Mental",r['stabilitas'],"#c084fc")

            bobot_sorted=sorted(r['bobot'].items(),key=lambda x:x[1],reverse=True)
            st.markdown('<div class="sec">🔑 Subtes Kunci untuk Jurusan Ini</div>', unsafe_allow_html=True)
            sc=st.columns(3)
            for col,(k,bv) in zip(sc,bobot_sorted[:3]):
                with col:
                    sv=r['skor'][k]
                    kc2="c-green" if sv>=650 else "c-gold" if sv>=450 else "c-red"
                    st.markdown(f"""<div class="card" style="text-align:center">
                      <div class="kpi-lbl">{SUBTES_LABEL[k]}</div>
                      <div class="kpi-val {kc2}">{sv}</div>
                      <div class="kpi-sub">Bobot {int(bv*100)}% — {'✅' if sv>=650 else '⚡' if sv>=450 else '🔴'}</div>
                    </div>""", unsafe_allow_html=True)

            st.markdown('<div class="sec">📋 Jurusan Alternatif (Formalitas)</div>', unsafe_allow_html=True)
            st.markdown('<div class="al al-i"><h4>ℹ️ Alternatif Disajikan Sebagai Formalitas</h4>Karena skor kamu sudah aman, jurusan alternatif di bawah hanya pilihan cadangan formalitas — tidak perlu dipertimbangkan serius.</div>',
                        unsafe_allow_html=True)
            alt=r['alternatif']
            if alt:
                ac=st.columns(len(alt))
                for col,j in zip(ac,alt):
                    with col:
                        st.markdown(f"""<div class="card" style="text-align:center;opacity:.6">
                          <div style="font-size:.72rem;color:#6b7a90">Alternatif Formalitas</div>
                          <div style="font-weight:700;font-size:.88rem;margin:.3rem 0;color:#c8d3e0">{j}</div>
                          <div style="font-size:.7rem;color:#6b7a90">Serumpun</div>
                        </div>""", unsafe_allow_html=True)

        else:
            st.markdown(f"""<div class="al al-w">
              <h4>⚡ Skor Belum Mencapai Zona Aman — {r['jurusan']}</h4>
              Butuh <strong>+{r['info']['min']-r['sw']:.0f} poin</strong> untuk zona aman.
              Pertimbangkan jurusan alternatif yang sesuai kemampuan saat ini.
            </div>""", unsafe_allow_html=True)

            st.markdown(f"<p style='color:#c8d3e0;font-weight:600;font-size:.88rem;margin:.5rem 0'>📋 Bobot subtes jurusan target kamu:</p>", unsafe_allow_html=True)
            show_bobot_chips(r['jurusan'])
            chart_bobot(r['jurusan'], key="result_bobot_t4_alt")  # KEY UNIK!

            st.markdown('<div class="sec">🔄 Jurusan Alternatif yang Direkomendasikan</div>', unsafe_allow_html=True)
            for idx, j in enumerate(r['alternatif']):
                bj=get_bobot(j)
                swj=hitung_tertimbang(r['skor'],bj)
                plj,_,pctj=hitung_peluang(swj,r['kampus'])
                with st.expander(f"📚 {j}  —  Skor Tertimbang: {swj:.0f}  |  {plj}"):
                    ca,cb2=st.columns(2)
                    with ca:
                        st.metric("Skor Tertimbang",f"{swj:.0f}")
                        st.metric("Peluang Est.",f"{pctj:.0f}% ({plj})")
                        st.markdown(f"<p style='color:#c8d3e0;font-weight:600;font-size:.85rem;margin:.3rem 0'>Bobot subtes:</p>", unsafe_allow_html=True)
                        show_bobot_chips(j)
                    with cb2:
                        chart_bobot(j, key=f"result_bobot_alt_{idx}")  # KEY UNIK per jurusan alternatif!

    # ═══ TAB 5: STRATEGI ═══
    with t5:
        st.markdown('<div class="sec">🚀 Strategi Belajar Personal</div>', unsafe_allow_html=True)

        prog_bar("Kesiapan Mental (Psikologis)",r['psiko'],"#60b4ff")
        prog_bar("Konsistensi Belajar",r['konsist'],"#4ade80")
        prog_bar("Stabilitas Mental",r['stabilitas'],"#c084fc")

        st.markdown('<div class="sec">📌 Prioritas Subtes</div>', unsafe_allow_html=True)
        sorted_s=sorted(r['skor'].items(),key=lambda x:x[1])
        lemah=sorted_s[:3]; kuat=sorted_s[-2:]

        c1p,c2p=st.columns(2)
        with c1p:
            il="".join(f"<li><strong>{SUBTES_LABEL[k]}</strong>: {v} → +{max(0,650-v)} poin dibutuhkan</li>" for k,v in lemah)
            st.markdown(f'<div class="al al-d"><h4>🔴 Prioritas Utama (3 Terlemah)</h4><ul>{il}</ul></div>',unsafe_allow_html=True)
        with c2p:
            ik="".join(f"<li><strong>{SUBTES_LABEL[k]}</strong>: {v} ✅</li>" for k,v in kuat)
            st.markdown(f'<div class="al al-s"><h4>🟢 Kekuatan Akademik</h4><ul>{ik}</ul></div>',unsafe_allow_html=True)

        st.markdown('<div class="sec">📋 Rencana Aksi</div>', unsafe_allow_html=True)
        if r['sw']>=r['info']['max']:
            st.markdown("""<div class="al al-s"><h4>🏆 Maintenance Mode</h4><ul>
              <li>Tryout 1–2x/minggu untuk menjaga ketajaman</li>
              <li>Review kesalahan kecil yang masih berulang</li>
              <li>Fokus manajemen waktu dan mental</li>
              <li>Jaga pola tidur minimal 7–8 jam</li></ul></div>""",unsafe_allow_html=True)
        elif r['sw']>=r['info']['min']:
            st.markdown(f"""<div class="al al-i"><h4>✅ Penguatan & Konsistensi</h4><ul>
              <li>Target +{r['info']['max']-r['sw']:.0f} poin untuk zona sangat aman</li>
              <li>Fokus 60% waktu pada {SUBTES_LABEL[sorted_s[0][0]]} (subtes terlemah)</li>
              <li>Tryout minimal 2x/bulan + review mendalam</li>
              <li>Simulasi 150 soal dalam 2.5 jam per sesi</li></ul></div>""",unsafe_allow_html=True)
        else:
            st.markdown(f"""<div class="al al-w"><h4>⚡ Intensifikasi</h4><ul>
              <li>Target +{r['info']['min']-r['sw']:.0f} poin — bertahap +{min(50,r['info']['min']-r['sw']):.0f}/bulan</li>
              <li>Belajar 4–5 jam/hari dengan jadwal terstruktur</li>
              <li>Tryout mingguan + analisis soal salah mendalam</li>
              <li>Konsultasi tutor untuk subtes berbobot tinggi</li></ul></div>""",unsafe_allow_html=True)

        st.markdown('<div class="sec">🧠 Tips Psikologis & Kebiasaan</div>', unsafe_allow_html=True)
        tp1,tp2=st.columns(2)
        with tp1:
            if r.get('fokus',3) <= 2:
                st.markdown('<div class="al al-d"><h4>🎯 Fokus Rendah</h4><ul><li>Teknik Pomodoro: 25 mnt belajar, 5 mnt istirahat</li><li>Matikan notifikasi HP saat belajar</li><li>Mulai sesi pendek (15 mnt) lalu naikkan</li></ul></div>',unsafe_allow_html=True)
            elif r.get('fokus',3) <= 3:
                st.markdown('<div class="al al-w"><h4>⚡ Fokus Sedang</h4><ul><li>Target sesi 45 mnt tanpa gangguan</li><li>Checklist harian untuk motivasi</li></ul></div>',unsafe_allow_html=True)
            if r.get('kecemasan',3) >= 4:
                st.markdown('<div class="al al-d"><h4>😰 Kecemasan Tinggi</h4><ul><li>Pernapasan 4-7-8 setiap pagi</li><li>Fokus pada proses, bukan hasil semata</li><li>Tidur cukup 7–8 jam tiap malam</li></ul></div>',unsafe_allow_html=True)
        with tp2:
            if r.get('distraksi',3) >= 4:
                st.markdown('<div class="al al-d"><h4>📱 Distraksi Tinggi</h4><ul><li>Gunakan Cold Turkey / Forest app</li><li>HP di ruangan lain saat belajar</li><li>Reward diri setelah selesai sesi</li></ul></div>',unsafe_allow_html=True)
            if r.get('review_soal',3) <= 2:
                st.markdown('<div class="al al-w"><h4>📝 Review Soal Kurang</h4><ul><li>Review SETIAP soal yang salah — ini kunci kemajuan</li><li>Buku catatan soal sulit untuk diulang rutin</li></ul></div>',unsafe_allow_html=True)

    # ═══ TAB 6: PDF ═══
    with t6:
        st.markdown('<div class="sec">📄 Export Laporan ke PDF</div>', unsafe_allow_html=True)
        st.markdown("""<div class="al al-i"><h4>Cara Menyimpan sebagai PDF</h4><ol>
          <li>Klik tombol <strong>Generate & Download Laporan HTML</strong> di bawah</li>
          <li>Buka file HTML yang terdownload di browser</li>
          <li>Tekan <strong>Ctrl+P</strong> (Windows) atau <strong>Cmd+P</strong> (Mac)</li>
          <li>Pilih <strong>"Save as PDF"</strong> sebagai printer</li>
          <li>Klik <strong>Save</strong></li>
        </ol></div>""", unsafe_allow_html=True)

        if st.button("📄  Generate & Download Laporan HTML", type="primary"):
            html = generate_pdf_html(r)
            b64  = base64.b64encode(html.encode()).decode()
            fn   = f"laporan_skoria_{r.get('nama','').replace(' ','_')}.html"
            st.markdown(f"""<a href="data:text/html;base64,{b64}" download="{fn}"
              style="display:inline-block;background:linear-gradient(135deg,#f5a623,#e8941a);
                     color:#000;font-weight:700;padding:.6rem 1.4rem;border-radius:10px;
                     text-decoration:none;font-family:'Syne',sans-serif;font-size:.9rem;margin-top:.5rem">
              ⬇️ Download {fn}</a>""", unsafe_allow_html=True)

        st.markdown('<div class="sec">👁️ Preview Ringkasan</div>', unsafe_allow_html=True)
        cp1,cp2=st.columns(2)
        with cp1:
            st.markdown(f"""| Info | Detail |
|---|---|
| Nama | {r.get('nama','—')} |
| Jurusan | {r['jurusan']} |
| Kampus | {r['kampus']} |
| Klaster | {r['info']['label']} |
| Skor Tertimbang | {r['sw']:.0f} |
| Gap | {r['gap']:+.0f} |""")
        with cp2:
            st.markdown(f"""| Indikator | Nilai |
|---|---|
| Peluang Lolos | {r['ppct']:.0f}% ({r['pl']}) |
| Kesiapan Mental | {r['psiko']:.0f}/100 |
| Konsistensi | {r['konsist']:.0f}/100 |
| Stabilitas | {r['stabilitas']:.0f}/100 |
| Risiko | {r['risk'][0]} {r['risk'][1]} |""")

    # ── Footer nav ──
    st.divider()
    nb1,nb2,_=st.columns([1,1,4])
    with nb1:
        if st.button("← Ubah Data"):
            st.session_state.page='survey'; st.session_state.step=1; st.rerun()
    with nb2:
        if st.button("🏠 Beranda"):
            st.session_state.page='home'; st.rerun()

    st.markdown(f"""<div style="text-align:center;padding:1.4rem;background:var(--surf);
      border-radius:var(--r);border:1px solid var(--border);margin-top:1rem">
      <div style="font-family:'Syne',sans-serif;font-size:1.1rem;font-weight:800;color:#ffffff">
        💪 {nama}, kamu pasti bisa!
      </div>
      <div style="color:#8b9ab0;font-size:.83rem;margin-top:.3rem">
        Konsistensi + strategi tepat = PTN impianmu pasti bisa diraih 🚀
      </div>
      <div style="color:#30363d;font-size:.72rem;margin-top:.4rem">
        🎯 SKORIA — AI UTBK Intelligence · LightGBM + Analisis Holistik · Skor skala 200–{SKOR_MAX}
      </div>
    </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════
def main():
    render_nav()
    {'home':page_home,'survey':page_survey,'result':page_result}[st.session_state.page]()

if __name__=="__main__":
    main()
