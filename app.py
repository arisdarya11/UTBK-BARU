"""
SKORIA — AI UTBK Readiness Dashboard v4.0
Platform kecerdasan buatan untuk analisis kesiapan UTBK secara holistik
Skor: 200–1000 | S1 | 30 PTN | 60 Program Studi
Data: UTBK_SNBT_Estimasi_30PTN.xlsx (Historis 2022–2024, SNPMB/BPPP Kemdikbud)
"""

import streamlit as st
import numpy as np
import pandas as pd
import datetime
from typing import Dict, Tuple, List
import plotly.graph_objects as go

st.set_page_config(
    page_title="SKORIA — AI UTBK",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@600;700;800&display=swap');
:root{--bg:#f0f4fa;--surf:#ffffff;--surf2:#f7f9fd;--border:#e0e8f4;--accent:#3464c8;--a2:#5080e0;--gold:#d4900a;--green:#148a42;--red:#c0392b;--orange:#d4620a;--purple:#6b3fca;--teal:#0d8a80;--text:#12203f;--text2:#334466;--text3:#6a7a9a;--r:12px;--sh:0 2px 12px rgba(30,60,140,.08);--sh2:0 8px 32px rgba(30,60,140,.15);}
@keyframes fadeSlideUp{from{opacity:0;transform:translateY(30px) scale(.97)}to{opacity:1;transform:translateY(0) scale(1)}}
@keyframes fadeSlideLeft{from{opacity:0;transform:translateX(-24px)}to{opacity:1;transform:translateX(0)}}
@keyframes fadeSlideRight{from{opacity:0;transform:translateX(24px)}to{opacity:1;transform:translateX(0)}}
@keyframes popIn{0%{opacity:0;transform:scale(.5) rotate(-8deg)}65%{opacity:1;transform:scale(1.1) rotate(3deg)}85%{transform:scale(.96) rotate(-1deg)}100%{transform:scale(1) rotate(0)}}
@keyframes pulseRing{0%,100%{box-shadow:0 0 0 0 rgba(52,100,200,.35)}50%{box-shadow:0 0 0 10px rgba(52,100,200,0)}}
@keyframes orb{0%,100%{transform:scale(1) translate(0,0);opacity:.08}40%{transform:scale(1.18) translate(15px,-12px);opacity:.14}70%{transform:scale(.88) translate(-10px,14px);opacity:.04}}
@keyframes float{0%,100%{transform:translateY(0px)}50%{transform:translateY(-8px)}}
@keyframes shimmer{from{background-position:-600px 0}to{background-position:600px 0}}
@keyframes progressGrow{from{width:0!important;opacity:.4}}
@keyframes gradientFlow{0%,100%{background-position:0% 50%}50%{background-position:100% 50%}}
@keyframes countUp{from{opacity:0;transform:translateY(14px) scale(.8)}to{opacity:1;transform:translateY(0) scale(1)}}
@keyframes typeBar{from{width:0}}
html,body,[class*="css"],.stApp{background:var(--bg)!important;font-family:'Plus Jakarta Sans',sans-serif!important;color:var(--text)!important;}
#MainMenu,footer,header{visibility:hidden}.stDeployButton{display:none}
.block-container{padding:1rem 1.5rem!important;max-width:100%!important;}
.main .block-container{animation:fadeSlideUp .5s cubic-bezier(.22,.68,0,1.2) both;}
.hero{background:linear-gradient(135deg,#1a3470 0%,#3464c8 55%,#2a50a8 100%);border-radius:16px;padding:2.4rem 3rem;margin-bottom:1.8rem;position:relative;overflow:hidden;box-shadow:0 6px 32px rgba(30,60,180,.22);animation:fadeSlideUp .65s cubic-bezier(.22,.68,0,1.2) both;}
.hero::before{content:'';position:absolute;top:-70px;right:-70px;width:320px;height:320px;border-radius:50%;background:radial-gradient(circle,rgba(255,255,255,.12) 0%,transparent 65%);animation:orb 7s ease-in-out infinite;}
.hero h1{font-family:'Space Grotesk',sans-serif!important;font-size:2rem!important;font-weight:800!important;color:#fff!important;margin:0 0 .6rem!important;}
.hero h1 span{color:#ffd166;}
.hero p{color:rgba(255,255,255,.82)!important;font-size:.95rem;margin:0;line-height:1.7;}
.hero-badge{display:inline-flex;align-items:center;gap:.4rem;background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.2);padding:.3rem .85rem;border-radius:99px;font-size:.72rem;font-weight:600;color:rgba(255,255,255,.9);margin-bottom:1rem;}
.stat-row{display:grid;grid-template-columns:repeat(4,1fr);gap:.8rem;margin-bottom:1.4rem;}
.stat-box{border-radius:12px;padding:1.1rem 1rem;text-align:center;box-shadow:0 4px 16px rgba(52,100,200,.25);animation:popIn .6s ease both;}
.stat-box:nth-child(1){background:linear-gradient(135deg,var(--accent),var(--purple));}
.stat-box:nth-child(2){background:linear-gradient(135deg,var(--purple),var(--teal));animation-delay:.1s;}
.stat-box:nth-child(3){background:linear-gradient(135deg,var(--teal),var(--green));animation-delay:.2s;}
.stat-box:nth-child(4){background:linear-gradient(135deg,var(--gold),var(--orange));animation-delay:.3s;}
.stat-num{font-family:'Space Grotesk',sans-serif;font-size:1.6rem;font-weight:800;color:#fff;}
.stat-lbl{font-size:.72rem;color:rgba(255,255,255,.82);font-weight:600;margin-top:.15rem;}
.feat-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:1rem;margin-bottom:1.4rem;}
.feat-card{background:var(--surf);border:1px solid var(--border);border-radius:14px;padding:1.6rem 1.2rem;text-align:center;box-shadow:var(--sh);transition:all .32s cubic-bezier(.22,.68,0,1.2);animation:fadeSlideUp .5s ease both;}
.feat-card:hover{transform:translateY(-8px) scale(1.02);box-shadow:var(--sh2);}
.feat-icon{font-size:2.2rem;margin-bottom:.6rem;display:block;animation:float 3.2s ease-in-out infinite;}
.feat-title{font-family:'Space Grotesk',sans-serif;font-weight:700;font-size:.9rem;color:var(--text);margin-bottom:.35rem;}
.feat-desc{font-size:.76rem;color:var(--text3);line-height:1.6;}
.form-box{background:var(--surf);border:1px solid var(--border);border-radius:var(--r);padding:1.8rem 2rem;margin-bottom:1.2rem;box-shadow:var(--sh);animation:fadeSlideUp .5s cubic-bezier(.22,.68,0,1.2) both;transition:border-color .3s ease,box-shadow .3s ease;position:relative;overflow:hidden;}
.form-box::before{content:'';position:absolute;top:0;left:0;right:0;height:3px;background:linear-gradient(90deg,var(--accent),var(--purple));}
.form-box:focus-within{border-color:var(--a2);box-shadow:0 4px 20px rgba(52,100,200,.12);}
.form-box h3{font-family:'Space Grotesk',sans-serif;font-size:1rem;font-weight:700;color:var(--accent);margin:0 0 1.2rem;}
.sec{font-family:'Space Grotesk',sans-serif;font-size:.94rem;font-weight:700;color:var(--text);margin:1.6rem 0 .75rem;padding-bottom:.35rem;border-bottom:2px solid var(--border);animation:fadeSlideLeft .4s ease both;position:relative;}
.sec::after{content:'';position:absolute;bottom:-2px;left:0;height:2px;background:linear-gradient(90deg,var(--accent),var(--a2));animation:typeBar .7s ease .2s both;}
.card{background:var(--surf);border:1px solid var(--border);border-radius:var(--r);padding:1.2rem 1.4rem;box-shadow:var(--sh);transition:transform .28s ease,box-shadow .28s ease;animation:fadeSlideUp .5s ease both;}
.card:hover{transform:translateY(-4px);box-shadow:var(--sh2);}
.kpi-lbl{font-size:.67rem;font-weight:700;text-transform:uppercase;letter-spacing:.1em;color:var(--text3);margin-bottom:.3rem;}
.kpi-val{font-family:'Space Grotesk',sans-serif;font-size:1.9rem;font-weight:800;line-height:1;animation:countUp .6s cubic-bezier(.22,.68,0,1.2) .2s both;}
.kpi-sub{font-size:.71rem;color:var(--text3);margin-top:.2rem;}
.c-gold{color:var(--gold)!important}.c-green{color:var(--green)!important}.c-red{color:var(--red)!important}.c-orange{color:var(--orange)!important}.c-blue{color:var(--a2)!important}.c-purple{color:var(--purple)!important}.c-teal{color:var(--teal)!important}
.al{border-radius:var(--r);padding:1rem 1.3rem;margin-bottom:.9rem;border-left:4px solid;font-size:.86rem;line-height:1.75;color:var(--text2);box-shadow:var(--sh);animation:fadeSlideRight .45s cubic-bezier(.22,.68,0,1.2) both;}
.al h4{margin:0 0 .4rem;font-size:.9rem;font-weight:700;}
.al ul{margin:.35rem 0 0;padding-left:1.3rem;}
.al li{margin-bottom:.22rem;}
.al-s{background:#edfbf3;border-color:var(--green);}.al-s h4{color:var(--green);}
.al-w{background:#fff7ee;border-color:var(--orange);}.al-w h4{color:var(--orange);}
.al-d{background:#fff0f0;border-color:var(--red);}.al-d h4{color:var(--red);}
.al-i{background:#eef2fc;border-color:var(--accent);}.al-i h4{color:var(--accent);}
.al-p{background:#f3eeff;border-color:var(--purple);}.al-p h4{color:var(--purple);}
.prog-wrap{margin-bottom:.75rem;}
.prog-lbl{display:flex;justify-content:space-between;font-size:.79rem;font-weight:600;color:var(--text2);margin-bottom:5px;}
.prog-bg{background:var(--surf2);border-radius:99px;height:10px;overflow:hidden;border:1px solid var(--border);}
.prog-fill{height:100%;border-radius:99px;animation:progressGrow .9s cubic-bezier(.22,.68,0,1.2) .3s both;position:relative;overflow:hidden;}
.prog-fill::after{content:'';position:absolute;inset:0;background:linear-gradient(90deg,transparent 0%,rgba(255,255,255,.45) 50%,transparent 100%);background-size:200% 100%;animation:shimmer 2s ease 1.4s infinite;}
.week-card{background:var(--surf);border:1px solid var(--border);border-radius:12px;padding:1rem 1.2rem;margin-bottom:.65rem;box-shadow:var(--sh);transition:transform .25s ease,border-color .25s ease;animation:fadeSlideUp .5s ease both;border-left:4px solid transparent;}
.week-card:hover{transform:translateX(8px);border-left-color:var(--accent);box-shadow:var(--sh2);}
.week-num{font-family:'Space Grotesk',sans-serif;font-size:.72rem;font-weight:700;color:var(--accent);text-transform:uppercase;letter-spacing:.1em;margin-bottom:.28rem;}
.week-target{font-size:.84rem;font-weight:700;color:var(--text);margin-bottom:.24rem;}
.week-tasks{font-size:.79rem;color:var(--text2);line-height:1.68;}
.status-badge{display:inline-flex;align-items:center;gap:.45rem;padding:.42rem 1.1rem;border-radius:99px;font-size:.78rem;font-weight:700;animation:popIn .6s ease both;}
.sbg-sa{background:#e6f5ee;color:#148a42;border:1.5px solid #9adbb8;}.sbg-a{background:#edf6ff;color:#1a5fa0;border:1.5px solid #90c0f0;}.sbg-k{background:#fff4e6;color:#d4620a;border:1.5px solid #f4c08a;}.sbg-r{background:#fff0f0;color:#c0392b;border:1.5px solid #f4a0a0;}
div[data-testid="stButton"] button[kind="primary"]{background:linear-gradient(135deg,var(--accent),#1a3470)!important;color:#fff!important;font-weight:700!important;font-family:'Space Grotesk',sans-serif!important;border:none!important;border-radius:10px!important;font-size:.89rem!important;transition:all .28s cubic-bezier(.22,.68,0,1.2)!important;}
div[data-testid="stButton"] button[kind="primary"]:hover{transform:translateY(-3px) scale(1.02)!important;box-shadow:0 8px 28px rgba(52,100,200,.4)!important;}
div[data-testid="stButton"] button{background:var(--surf)!important;color:var(--text2)!important;border:1px solid var(--border)!important;border-radius:10px!important;font-weight:600!important;transition:all .22s ease!important;}
div[data-testid="stButton"] button:hover{border-color:var(--a2)!important;color:var(--accent)!important;transform:translateY(-2px)!important;}
div[data-testid="stMetric"]{background:var(--surf)!important;border:1px solid var(--border)!important;border-radius:var(--r)!important;padding:1.1rem 1.3rem!important;box-shadow:var(--sh)!important;transition:transform .28s ease!important;}
div[data-testid="stMetric"]:hover{transform:translateY(-4px)!important;box-shadow:var(--sh2)!important;}
div[data-testid="stMetric"] label{color:var(--text3)!important;font-size:.7rem!important;font-weight:700!important;text-transform:uppercase!important;letter-spacing:.08em!important;}
div[data-testid="stMetric"] [data-testid="stMetricValue"]{color:var(--text)!important;font-family:'Space Grotesk',sans-serif!important;}
div[data-testid="stExpander"]{background:var(--surf)!important;border:1px solid var(--border)!important;border-radius:var(--r)!important;box-shadow:var(--sh)!important;}
div[data-testid="stNumberInput"] label,div[data-testid="stSelectbox"] label,div[data-testid="stTextInput"] label,div[data-testid="stRadio"] label{color:var(--text2)!important;font-weight:700!important;font-size:.83rem!important;}
div[data-testid="stNumberInput"] input,div[data-testid="stTextInput"] input{background:var(--surf)!important;color:var(--text)!important;border-color:var(--border)!important;font-size:.9rem!important;border-radius:8px!important;}
table{border-collapse:collapse;width:100%;font-size:.84rem;}
th{background:#eef2fc;color:var(--text);padding:.55rem .9rem;border:1px solid var(--border);font-weight:700;text-align:left;}
td{padding:.5rem .9rem;border:1px solid var(--border);color:var(--text2);}
tr:nth-child(even) td{background:#f8faff;}
tr:hover td{background:#eef2fc!important;}
.anim-div{height:2px;border-radius:99px;margin:1.2rem 0;background:linear-gradient(90deg,var(--accent),var(--purple),var(--teal),var(--gold),var(--accent));background-size:300% auto;animation:gradientFlow 4s linear infinite;}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════
# SESSION STATE
# ══════════════════════════════════════════════════════════
DEFAULTS = {"page":"home","step":1,"data":{},"result":None,"_cid":0}
for k,v in DEFAULTS.items():
    if k not in st.session_state: st.session_state[k]=v

def ckey(p="c"):
    st.session_state._cid += 1
    return f"{p}_{st.session_state._cid}"

# ══════════════════════════════════════════════════════════
# KONSTANTA & LOOKUP
# ══════════════════════════════════════════════════════════
SUBTES = ["PU","PPU","PBM","PK","LBI","LBE","PM"]
SUBTES_FULL = {"PU":"Penalaran Umum","PPU":"Pem. & Pengetahuan Umum",
    "PBM":"Pemahaman Bacaan & Menulis","PK":"Pengetahuan Kuantitatif",
    "LBI":"Literasi Bahasa Indonesia","LBE":"Literasi Bahasa Inggris","PM":"Penalaran Matematika"}
SUBTES_CLR = {"PU":"#c8890a","PPU":"#3b6cb7","PBM":"#7048c8","PK":"#c0392b",
    "LBI":"#1a8a4a","LBE":"#0d8a80","PM":"#d4620a"}

# ── DAFTAR PTN & JURUSAN (30 PTN, 60 Prodi — Excel 2024)
DAFTAR_PTN = ['Universitas Indonesia', 'Universitas Gadjah Mada', 'Universitas Airlangga', 'Institut Teknologi Bandung', 'Universitas Padjadjaran', 'Institut Pertanian Bogor', 'Institut Teknologi Sepuluh Nopember', 'Universitas Diponegoro', 'Universitas Brawijaya', 'Universitas Sebelas Maret', 'Universitas Hasanuddin', 'Universitas Pendidikan Indonesia', 'Universitas Sumatera Utara', 'Universitas Negeri Yogyakarta', 'Universitas Negeri Malang', 'Universitas Lampung', 'Universitas Andalas', 'Universitas Negeri Semarang', 'Universitas Syiah Kuala', 'Universitas Mulawarman', 'Universitas Sriwijaya', 'Universitas Udayana', 'Universitas Sam Ratulangi', 'Universitas Riau', 'Universitas Jember', 'Telkom University', 'Universitas Islam Indonesia', 'Universitas Muhammadiyah Yogyakarta', 'Bina Nusantara University', 'Universitas Muhammadiyah Malang']

DAFTAR_JURUSAN_S1 = ['Administrasi Negara', 'Agribisnis', 'Agroteknologi', 'Akuntansi', 'Antropologi Sosial', 'Arsitektur', 'Biologi', 'Bioteknologi', 'Bisnis Internasional', 'Ekonomi Pembangunan', 'Farmasi', 'Filsafat', 'Fisika', 'Hubungan Internasional', 'Hukum', 'Ilmu Administrasi Bisnis', 'Ilmu Gizi', 'Ilmu Kelautan', 'Ilmu Kesejahteraan Sosial', 'Ilmu Komputer', 'Ilmu Komunikasi', 'Ilmu Pemerintahan', 'Ilmu Politik', 'Ilmu Sejarah', 'Ilmu Tanah', 'Kedokteran Gigi', 'Kehutanan', 'Keperawatan', 'Keuangan dan Perbankan', 'Kimia', 'Kriminologi', 'Manajemen', 'Matematika', 'Pariwisata', 'Pendidikan Bahasa Inggris', 'Pendidikan Dokter (Kedokteran)', 'Pendidikan Ekonomi', 'Pendidikan Pancasila dan Kewarganegaraan', 'Pendidikan Sejarah', 'Pendidikan Sosiologi', 'Perencanaan Wilayah dan Kota', 'Perpustakaan dan Ilmu Informasi', 'Peternakan', 'Psikologi', 'Sastra Arab', 'Sastra Indonesia', 'Sastra Inggris', 'Sastra Jawa', 'Sosiologi', 'Statistika', 'Teknik Elektro', 'Teknik Geologi', 'Teknik Industri', 'Teknik Informatika', 'Teknik Kimia', 'Teknik Lingkungan', 'Teknik Mesin', 'Teknik Perminyakan', 'Teknik Sipil', 'Teknologi Pangan']
DAFTAR_JURUSAN = DAFTAR_JURUSAN_S1

# ── BOBOT PER JURUSAN
BOBOT_MAP = {
    "Administrasi Negara":{"PU":.22,"PPU":.15,"PBM":.18,"PK":.08,"LBI":.20,"LBE":.10,"PM":.07},
    "Agribisnis":{"PU":.18,"PPU":.12,"PBM":.12,"PK":.15,"LBI":.12,"LBE":.08,"PM":.23},
    "Agroteknologi":{"PU":.18,"PPU":.12,"PBM":.08,"PK":.18,"LBI":.10,"LBE":.07,"PM":.27},
    "Akuntansi":{"PU":.18,"PPU":.15,"PBM":.10,"PK":.22,"LBI":.10,"LBE":.10,"PM":.15},
    "Antropologi Sosial":{"PU":.20,"PPU":.17,"PBM":.22,"PK":.06,"LBI":.20,"LBE":.10,"PM":.05},
    "Arsitektur":{"PU":.20,"PPU":.10,"PBM":.12,"PK":.18,"LBI":.10,"LBE":.08,"PM":.22},
    "Biologi":{"PU":.20,"PPU":.15,"PBM":.10,"PK":.15,"LBI":.10,"LBE":.08,"PM":.22},
    "Bioteknologi":{"PU":.20,"PPU":.13,"PBM":.08,"PK":.18,"LBI":.08,"LBE":.08,"PM":.25},
    "Bisnis Internasional":{"PU":.20,"PPU":.15,"PBM":.15,"PK":.12,"LBI":.15,"LBE":.18,"PM":.05},
    "Ekonomi Pembangunan":{"PU":.20,"PPU":.15,"PBM":.10,"PK":.20,"LBI":.10,"LBE":.10,"PM":.15},
    "Farmasi":{"PU":.18,"PPU":.12,"PBM":.08,"PK":.18,"LBI":.08,"LBE":.08,"PM":.28},
    "Filsafat":{"PU":.22,"PPU":.18,"PBM":.22,"PK":.05,"LBI":.20,"LBE":.10,"PM":.03},
    "Fisika":{"PU":.18,"PPU":.07,"PBM":.05,"PK":.20,"LBI":.05,"LBE":.05,"PM":.40},
    "Hubungan Internasional":{"PU":.20,"PPU":.15,"PBM":.15,"PK":.08,"LBI":.17,"LBE":.20,"PM":.05},
    "Hukum":{"PU":.22,"PPU":.18,"PBM":.20,"PK":.08,"LBI":.18,"LBE":.10,"PM":.04},
    "Ilmu Administrasi Bisnis":{"PU":.20,"PPU":.15,"PBM":.18,"PK":.12,"LBI":.18,"LBE":.10,"PM":.07},
    "Ilmu Gizi":{"PU":.18,"PPU":.12,"PBM":.10,"PK":.15,"LBI":.12,"LBE":.08,"PM":.25},
    "Ilmu Kelautan":{"PU":.18,"PPU":.12,"PBM":.08,"PK":.18,"LBI":.10,"LBE":.07,"PM":.27},
    "Ilmu Kesejahteraan Sosial":{"PU":.20,"PPU":.15,"PBM":.20,"PK":.08,"LBI":.22,"LBE":.10,"PM":.05},
    "Ilmu Komputer":{"PU":.20,"PPU":.05,"PBM":.05,"PK":.20,"LBI":.05,"LBE":.10,"PM":.35},
    "Ilmu Komunikasi":{"PU":.20,"PPU":.15,"PBM":.22,"PK":.08,"LBI":.20,"LBE":.10,"PM":.05},
    "Ilmu Pemerintahan":{"PU":.22,"PPU":.17,"PBM":.18,"PK":.08,"LBI":.18,"LBE":.10,"PM":.07},
    "Ilmu Politik":{"PU":.22,"PPU":.17,"PBM":.18,"PK":.08,"LBI":.18,"LBE":.10,"PM":.07},
    "Ilmu Sejarah":{"PU":.20,"PPU":.20,"PBM":.18,"PK":.05,"LBI":.22,"LBE":.10,"PM":.05},
    "Ilmu Tanah":{"PU":.18,"PPU":.12,"PBM":.08,"PK":.18,"LBI":.10,"LBE":.07,"PM":.27},
    "Kedokteran Gigi":{"PU":.20,"PPU":.15,"PBM":.10,"PK":.15,"LBI":.10,"LBE":.10,"PM":.20},
    "Kehutanan":{"PU":.18,"PPU":.12,"PBM":.08,"PK":.18,"LBI":.10,"LBE":.07,"PM":.27},
    "Keperawatan":{"PU":.18,"PPU":.12,"PBM":.12,"PK":.12,"LBI":.15,"LBE":.08,"PM":.23},
    "Keuangan dan Perbankan":{"PU":.18,"PPU":.13,"PBM":.10,"PK":.25,"LBI":.10,"LBE":.08,"PM":.16},
    "Kimia":{"PU":.18,"PPU":.10,"PBM":.07,"PK":.18,"LBI":.07,"LBE":.05,"PM":.35},
    "Kriminologi":{"PU":.22,"PPU":.17,"PBM":.20,"PK":.07,"LBI":.18,"LBE":.10,"PM":.06},
    "Manajemen":{"PU":.20,"PPU":.15,"PBM":.12,"PK":.18,"LBI":.12,"LBE":.10,"PM":.13},
    "Matematika":{"PU":.15,"PPU":.05,"PBM":.05,"PK":.20,"LBI":.05,"LBE":.05,"PM":.45},
    "Pariwisata":{"PU":.18,"PPU":.13,"PBM":.18,"PK":.08,"LBI":.18,"LBE":.20,"PM":.05},
    "Pendidikan Bahasa Inggris":{"PU":.12,"PPU":.12,"PBM":.18,"PK":.05,"LBI":.12,"LBE":.33,"PM":.08},
    "Pendidikan Dokter (Kedokteran)":{"PU":.20,"PPU":.15,"PBM":.10,"PK":.15,"LBI":.10,"LBE":.10,"PM":.20},
    "Pendidikan Ekonomi":{"PU":.20,"PPU":.15,"PBM":.13,"PK":.18,"LBI":.13,"LBE":.10,"PM":.11},
    "Pendidikan Pancasila dan Kewarganegaraan":{"PU":.20,"PPU":.17,"PBM":.18,"PK":.07,"LBI":.20,"LBE":.10,"PM":.08},
    "Pendidikan Sejarah":{"PU":.18,"PPU":.18,"PBM":.20,"PK":.06,"LBI":.22,"LBE":.10,"PM":.06},
    "Pendidikan Sosiologi":{"PU":.20,"PPU":.16,"PBM":.20,"PK":.07,"LBI":.20,"LBE":.10,"PM":.07},
    "Perencanaan Wilayah dan Kota":{"PU":.20,"PPU":.10,"PBM":.12,"PK":.18,"LBI":.10,"LBE":.08,"PM":.22},
    "Perpustakaan dan Ilmu Informasi":{"PU":.18,"PPU":.15,"PBM":.22,"PK":.08,"LBI":.22,"LBE":.10,"PM":.05},
    "Peternakan":{"PU":.18,"PPU":.12,"PBM":.08,"PK":.18,"LBI":.10,"LBE":.07,"PM":.27},
    "Psikologi":{"PU":.22,"PPU":.15,"PBM":.18,"PK":.10,"LBI":.18,"LBE":.10,"PM":.07},
    "Sastra Arab":{"PU":.14,"PPU":.15,"PBM":.22,"PK":.05,"LBI":.22,"LBE":.18,"PM":.04},
    "Sastra Indonesia":{"PU":.12,"PPU":.12,"PBM":.25,"PK":.05,"LBI":.35,"LBE":.08,"PM":.03},
    "Sastra Inggris":{"PU":.12,"PPU":.12,"PBM":.20,"PK":.05,"LBI":.15,"LBE":.31,"PM":.05},
    "Sastra Jawa":{"PU":.12,"PPU":.14,"PBM":.24,"PK":.05,"LBI":.33,"LBE":.08,"PM":.04},
    "Sosiologi":{"PU":.22,"PPU":.17,"PBM":.18,"PK":.08,"LBI":.18,"LBE":.10,"PM":.07},
    "Statistika":{"PU":.15,"PPU":.07,"PBM":.05,"PK":.20,"LBI":.05,"LBE":.05,"PM":.43},
    "Teknik Elektro":{"PU":.20,"PPU":.05,"PBM":.05,"PK":.20,"LBI":.05,"LBE":.10,"PM":.35},
    "Teknik Geologi":{"PU":.18,"PPU":.08,"PBM":.05,"PK":.20,"LBI":.05,"LBE":.07,"PM":.37},
    "Teknik Industri":{"PU":.20,"PPU":.05,"PBM":.05,"PK":.20,"LBI":.05,"LBE":.10,"PM":.35},
    "Teknik Informatika":{"PU":.20,"PPU":.05,"PBM":.05,"PK":.20,"LBI":.05,"LBE":.10,"PM":.35},
    "Teknik Kimia":{"PU":.18,"PPU":.08,"PBM":.05,"PK":.20,"LBI":.05,"LBE":.07,"PM":.37},
    "Teknik Lingkungan":{"PU":.18,"PPU":.08,"PBM":.07,"PK":.18,"LBI":.07,"LBE":.07,"PM":.35},
    "Teknik Mesin":{"PU":.20,"PPU":.05,"PBM":.05,"PK":.20,"LBI":.05,"LBE":.10,"PM":.35},
    "Teknik Perminyakan":{"PU":.18,"PPU":.07,"PBM":.05,"PK":.20,"LBI":.05,"LBE":.07,"PM":.38},
    "Teknik Sipil":{"PU":.20,"PPU":.05,"PBM":.05,"PK":.20,"LBI":.05,"LBE":.10,"PM":.35},
    "Teknologi Pangan":{"PU":.18,"PPU":.12,"PBM":.08,"PK":.18,"LBI":.10,"LBE":.07,"PM":.27},
}
DEFAULT_BOBOT = {"PU":.15,"PPU":.14,"PBM":.14,"PK":.15,"LBI":.14,"LBE":.13,"PM":.15}
def get_bobot(j): return BOBOT_MAP.get(j, DEFAULT_BOBOT)

ALTERNATIF_MAP = {
    "Administrasi Negara":["Ilmu Pemerintahan","Ilmu Politik","Sosiologi"],
    "Agribisnis":["Agroteknologi","Peternakan","Teknologi Pangan"],
    "Agroteknologi":["Agribisnis","Biologi","Peternakan"],
    "Akuntansi":["Manajemen","Ekonomi Pembangunan","Keuangan dan Perbankan"],
    "Antropologi Sosial":["Sosiologi","Ilmu Kesejahteraan Sosial","Psikologi"],
    "Arsitektur":["Perencanaan Wilayah dan Kota","Teknik Sipil","Teknik Lingkungan"],
    "Biologi":["Bioteknologi","Agroteknologi","Ilmu Gizi"],
    "Bioteknologi":["Biologi","Kimia","Farmasi"],
    "Bisnis Internasional":["Manajemen","Hubungan Internasional","Ilmu Komunikasi"],
    "Ekonomi Pembangunan":["Manajemen","Akuntansi","Ilmu Politik"],
    "Farmasi":["Kimia","Ilmu Gizi","Bioteknologi"],
    "Filsafat":["Ilmu Sejarah","Sosiologi","Ilmu Politik"],
    "Fisika":["Matematika","Teknik Mesin","Teknik Elektro"],
    "Hubungan Internasional":["Ilmu Komunikasi","Ilmu Politik","Bisnis Internasional"],
    "Hukum":["Ilmu Politik","Administrasi Negara","Sosiologi"],
    "Ilmu Administrasi Bisnis":["Manajemen","Ilmu Komunikasi","Ilmu Pemerintahan"],
    "Ilmu Gizi":["Keperawatan","Farmasi","Biologi"],
    "Ilmu Kelautan":["Kehutanan","Agribisnis","Biologi"],
    "Ilmu Kesejahteraan Sosial":["Sosiologi","Psikologi","Ilmu Komunikasi"],
    "Ilmu Komputer":["Teknik Informatika","Statistika","Matematika"],
    "Ilmu Komunikasi":["Hubungan Internasional","Ilmu Pemerintahan","Psikologi"],
    "Ilmu Pemerintahan":["Administrasi Negara","Ilmu Politik","Hukum"],
    "Ilmu Politik":["Hukum","Sosiologi","Ilmu Pemerintahan"],
    "Ilmu Sejarah":["Sosiologi","Antropologi Sosial","Pendidikan Sejarah"],
    "Ilmu Tanah":["Agribisnis","Teknik Lingkungan","Kehutanan"],
    "Kedokteran Gigi":["Pendidikan Dokter (Kedokteran)","Farmasi","Keperawatan"],
    "Kehutanan":["Ilmu Kelautan","Teknik Lingkungan","Agribisnis"],
    "Keperawatan":["Ilmu Gizi","Farmasi","Biologi"],
    "Keuangan dan Perbankan":["Akuntansi","Ekonomi Pembangunan","Manajemen"],
    "Kimia":["Farmasi","Bioteknologi","Teknik Kimia"],
    "Kriminologi":["Hukum","Sosiologi","Ilmu Kesejahteraan Sosial"],
    "Manajemen":["Ilmu Administrasi Bisnis","Ekonomi Pembangunan","Bisnis Internasional"],
    "Matematika":["Statistika","Fisika","Ilmu Komputer"],
    "Pariwisata":["Ilmu Komunikasi","Manajemen","Hubungan Internasional"],
    "Pendidikan Bahasa Inggris":["Sastra Inggris","Hubungan Internasional","Bisnis Internasional"],
    "Pendidikan Dokter (Kedokteran)":["Kedokteran Gigi","Farmasi","Keperawatan"],
    "Pendidikan Ekonomi":["Manajemen","Ekonomi Pembangunan","Akuntansi"],
    "Pendidikan Pancasila dan Kewarganegaraan":["Ilmu Politik","Sosiologi","Hukum"],
    "Pendidikan Sejarah":["Ilmu Sejarah","Sosiologi","Pendidikan Sosiologi"],
    "Pendidikan Sosiologi":["Sosiologi","Ilmu Kesejahteraan Sosial","Psikologi"],
    "Perencanaan Wilayah dan Kota":["Arsitektur","Teknik Sipil","Teknik Lingkungan"],
    "Perpustakaan dan Ilmu Informasi":["Ilmu Komunikasi","Administrasi Negara","Sosiologi"],
    "Peternakan":["Agribisnis","Agroteknologi","Kehutanan"],
    "Psikologi":["Ilmu Komunikasi","Sosiologi","Ilmu Kesejahteraan Sosial"],
    "Sastra Arab":["Sastra Inggris","Ilmu Komunikasi","Hubungan Internasional"],
    "Sastra Indonesia":["Sastra Jawa","Ilmu Komunikasi","Ilmu Sejarah"],
    "Sastra Inggris":["Pendidikan Bahasa Inggris","Hubungan Internasional","Bisnis Internasional"],
    "Sastra Jawa":["Sastra Indonesia","Ilmu Sejarah","Sosiologi"],
    "Sosiologi":["Ilmu Politik","Antropologi Sosial","Psikologi"],
    "Statistika":["Matematika","Akuntansi","Ilmu Komputer"],
    "Teknik Elektro":["Teknik Informatika","Ilmu Komputer","Teknik Mesin"],
    "Teknik Geologi":["Teknik Perminyakan","Fisika","Teknik Lingkungan"],
    "Teknik Industri":["Teknik Mesin","Manajemen","Statistika"],
    "Teknik Informatika":["Ilmu Komputer","Teknik Elektro","Statistika"],
    "Teknik Kimia":["Kimia","Teknologi Pangan","Teknik Lingkungan"],
    "Teknik Lingkungan":["Teknik Kimia","Ilmu Tanah","Kehutanan"],
    "Teknik Mesin":["Teknik Industri","Teknik Elektro","Teknik Sipil"],
    "Teknik Perminyakan":["Teknik Geologi","Teknik Kimia","Fisika"],
    "Teknik Sipil":["Arsitektur","Perencanaan Wilayah dan Kota","Teknik Lingkungan"],
    "Teknologi Pangan":["Ilmu Gizi","Agribisnis","Kimia"],
}

PTN_JURUSAN_DATA = {
    "Universitas Indonesia": {
        "Pendidikan Dokter (Kedokteran)": {"mn": 805, "mx": 840},
        "Teknik Informatika": {"mn": 795, "mx": 830},
        "Farmasi": {"mn": 780, "mx": 815},
        "Teknik Elektro": {"mn": 775, "mx": 810},
        "Ilmu Komputer": {"mn": 770, "mx": 805},
        "Teknik Kimia": {"mn": 765, "mx": 800},
        "Teknik Mesin": {"mn": 760, "mx": 795},
        "Teknik Sipil": {"mn": 755, "mx": 790},
        "Kedokteran Gigi": {"mn": 753, "mx": 788},
        "Bioteknologi": {"mn": 745, "mx": 780},
        "Teknik Industri": {"mn": 743, "mx": 778},
        "Statistika": {"mn": 737, "mx": 772},
        "Matematika": {"mn": 733, "mx": 768},
        "Fisika": {"mn": 727, "mx": 762},
        "Kimia": {"mn": 723, "mx": 758},
        "Biologi": {"mn": 720, "mx": 755},
        "Teknik Lingkungan": {"mn": 715, "mx": 750},
        "Teknik Geologi": {"mn": 713, "mx": 748},
        "Teknik Perminyakan": {"mn": 710, "mx": 745},
        "Arsitektur": {"mn": 709, "mx": 744},
        "Perencanaan Wilayah dan Kota": {"mn": 705, "mx": 740},
        "Ilmu Gizi": {"mn": 703, "mx": 738},
        "Keperawatan": {"mn": 697, "mx": 732},
        "Agroteknologi": {"mn": 690, "mx": 725},
        "Agribisnis": {"mn": 688, "mx": 723},
        "Kehutanan": {"mn": 683, "mx": 718},
        "Ilmu Tanah": {"mn": 677, "mx": 712},
        "Teknologi Pangan": {"mn": 675, "mx": 710},
        "Peternakan": {"mn": 670, "mx": 705},
        "Ilmu Kelautan": {"mn": 665, "mx": 700},
        "Psikologi": {"mn": 785, "mx": 820},
        "Hukum": {"mn": 775, "mx": 810},
        "Akuntansi": {"mn": 770, "mx": 805},
        "Manajemen": {"mn": 763, "mx": 798},
        "Ilmu Komunikasi": {"mn": 760, "mx": 795},
        "Ekonomi Pembangunan": {"mn": 753, "mx": 788},
        "Hubungan Internasional": {"mn": 750, "mx": 785},
        "Ilmu Administrasi Bisnis": {"mn": 745, "mx": 780},
        "Ilmu Politik": {"mn": 740, "mx": 775},
        "Sosiologi": {"mn": 733, "mx": 768},
        "Ilmu Kesejahteraan Sosial": {"mn": 727, "mx": 762},
        "Kriminologi": {"mn": 725, "mx": 760},
        "Ilmu Pemerintahan": {"mn": 723, "mx": 758},
        "Antropologi Sosial": {"mn": 717, "mx": 752},
        "Ilmu Sejarah": {"mn": 710, "mx": 745},
        "Sastra Inggris": {"mn": 707, "mx": 742},
        "Sastra Indonesia": {"mn": 700, "mx": 735},
        "Pendidikan Bahasa Inggris": {"mn": 697, "mx": 732},
        "Pendidikan Ekonomi": {"mn": 693, "mx": 728},
        "Pendidikan Sejarah": {"mn": 689, "mx": 724},
        "Pendidikan Sosiologi": {"mn": 685, "mx": 720},
        "Perpustakaan dan Ilmu Informasi": {"mn": 683, "mx": 718},
        "Keuangan dan Perbankan": {"mn": 680, "mx": 715},
        "Bisnis Internasional": {"mn": 677, "mx": 712},
        "Pariwisata": {"mn": 670, "mx": 705},
        "Administrasi Negara": {"mn": 667, "mx": 702},
        "Pendidikan Pancasila dan Kewarganegaraan": {"mn": 663, "mx": 698},
        "Sastra Arab": {"mn": 655, "mx": 690},
        "Sastra Jawa": {"mn": 645, "mx": 680},
        "Filsafat": {"mn": 640, "mx": 675},
        "_default": {"mn": 719, "mx": 754},
        "_klaster": 1, "_lbl": "⭐ Klaster 1 — Top Tier"
    },
    "Universitas Gadjah Mada": {
        "Pendidikan Dokter (Kedokteran)": {"mn": 805, "mx": 840},
        "Teknik Informatika": {"mn": 795, "mx": 830},
        "Farmasi": {"mn": 780, "mx": 815},
        "Teknik Elektro": {"mn": 775, "mx": 810},
        "Ilmu Komputer": {"mn": 770, "mx": 805},
        "Teknik Kimia": {"mn": 765, "mx": 800},
        "Teknik Mesin": {"mn": 760, "mx": 795},
        "Teknik Sipil": {"mn": 755, "mx": 790},
        "Kedokteran Gigi": {"mn": 753, "mx": 788},
        "Bioteknologi": {"mn": 745, "mx": 780},
        "Teknik Industri": {"mn": 743, "mx": 778},
        "Statistika": {"mn": 737, "mx": 772},
        "Matematika": {"mn": 733, "mx": 768},
        "Fisika": {"mn": 727, "mx": 762},
        "Kimia": {"mn": 723, "mx": 758},
        "Biologi": {"mn": 720, "mx": 755},
        "Teknik Lingkungan": {"mn": 715, "mx": 750},
        "Teknik Geologi": {"mn": 713, "mx": 748},
        "Teknik Perminyakan": {"mn": 710, "mx": 745},
        "Arsitektur": {"mn": 709, "mx": 744},
        "Perencanaan Wilayah dan Kota": {"mn": 705, "mx": 740},
        "Ilmu Gizi": {"mn": 703, "mx": 738},
        "Keperawatan": {"mn": 697, "mx": 732},
        "Agroteknologi": {"mn": 690, "mx": 725},
        "Agribisnis": {"mn": 688, "mx": 723},
        "Kehutanan": {"mn": 683, "mx": 718},
        "Ilmu Tanah": {"mn": 677, "mx": 712},
        "Teknologi Pangan": {"mn": 675, "mx": 710},
        "Peternakan": {"mn": 670, "mx": 705},
        "Ilmu Kelautan": {"mn": 665, "mx": 700},
        "Psikologi": {"mn": 785, "mx": 820},
        "Hukum": {"mn": 775, "mx": 810},
        "Akuntansi": {"mn": 770, "mx": 805},
        "Manajemen": {"mn": 763, "mx": 798},
        "Ilmu Komunikasi": {"mn": 760, "mx": 795},
        "Ekonomi Pembangunan": {"mn": 753, "mx": 788},
        "Hubungan Internasional": {"mn": 750, "mx": 785},
        "Ilmu Administrasi Bisnis": {"mn": 745, "mx": 780},
        "Ilmu Politik": {"mn": 740, "mx": 775},
        "Sosiologi": {"mn": 733, "mx": 768},
        "Ilmu Kesejahteraan Sosial": {"mn": 727, "mx": 762},
        "Kriminologi": {"mn": 725, "mx": 760},
        "Ilmu Pemerintahan": {"mn": 723, "mx": 758},
        "Antropologi Sosial": {"mn": 717, "mx": 752},
        "Ilmu Sejarah": {"mn": 710, "mx": 745},
        "Sastra Inggris": {"mn": 707, "mx": 742},
        "Sastra Indonesia": {"mn": 700, "mx": 735},
        "Pendidikan Bahasa Inggris": {"mn": 697, "mx": 732},
        "Pendidikan Ekonomi": {"mn": 693, "mx": 728},
        "Pendidikan Sejarah": {"mn": 689, "mx": 724},
        "Pendidikan Sosiologi": {"mn": 685, "mx": 720},
        "Perpustakaan dan Ilmu Informasi": {"mn": 683, "mx": 718},
        "Keuangan dan Perbankan": {"mn": 680, "mx": 715},
        "Bisnis Internasional": {"mn": 677, "mx": 712},
        "Pariwisata": {"mn": 670, "mx": 705},
        "Administrasi Negara": {"mn": 667, "mx": 702},
        "Pendidikan Pancasila dan Kewarganegaraan": {"mn": 663, "mx": 698},
        "Sastra Arab": {"mn": 655, "mx": 690},
        "Sastra Jawa": {"mn": 645, "mx": 680},
        "Filsafat": {"mn": 640, "mx": 675},
        "_default": {"mn": 719, "mx": 754},
        "_klaster": 1, "_lbl": "⭐ Klaster 1 — Top Tier"
    },
    "Universitas Airlangga": {
        "Pendidikan Dokter (Kedokteran)": {"mn": 780, "mx": 815},
        "Teknik Informatika": {"mn": 771, "mx": 806},
        "Farmasi": {"mn": 756, "mx": 791},
        "Teknik Elektro": {"mn": 751, "mx": 786},
        "Ilmu Komputer": {"mn": 746, "mx": 781},
        "Teknik Kimia": {"mn": 742, "mx": 777},
        "Teknik Mesin": {"mn": 737, "mx": 772},
        "Teknik Sipil": {"mn": 732, "mx": 767},
        "Kedokteran Gigi": {"mn": 730, "mx": 765},
        "Bioteknologi": {"mn": 722, "mx": 757},
        "Teknik Industri": {"mn": 720, "mx": 755},
        "Statistika": {"mn": 714, "mx": 749},
        "Matematika": {"mn": 711, "mx": 746},
        "Fisika": {"mn": 705, "mx": 740},
        "Kimia": {"mn": 701, "mx": 736},
        "Biologi": {"mn": 698, "mx": 733},
        "Teknik Lingkungan": {"mn": 693, "mx": 728},
        "Teknik Geologi": {"mn": 691, "mx": 726},
        "Teknik Perminyakan": {"mn": 688, "mx": 723},
        "Arsitektur": {"mn": 687, "mx": 722},
        "Perencanaan Wilayah dan Kota": {"mn": 683, "mx": 718},
        "Ilmu Gizi": {"mn": 681, "mx": 716},
        "Keperawatan": {"mn": 676, "mx": 711},
        "Agroteknologi": {"mn": 669, "mx": 704},
        "Agribisnis": {"mn": 667, "mx": 702},
        "Kehutanan": {"mn": 662, "mx": 697},
        "Ilmu Tanah": {"mn": 656, "mx": 691},
        "Teknologi Pangan": {"mn": 654, "mx": 689},
        "Peternakan": {"mn": 649, "mx": 684},
        "Ilmu Kelautan": {"mn": 645, "mx": 680},
        "Psikologi": {"mn": 761, "mx": 796},
        "Hukum": {"mn": 751, "mx": 786},
        "Akuntansi": {"mn": 746, "mx": 781},
        "Manajemen": {"mn": 740, "mx": 775},
        "Ilmu Komunikasi": {"mn": 737, "mx": 772},
        "Ekonomi Pembangunan": {"mn": 730, "mx": 765},
        "Hubungan Internasional": {"mn": 727, "mx": 762},
        "Ilmu Administrasi Bisnis": {"mn": 722, "mx": 757},
        "Ilmu Politik": {"mn": 717, "mx": 752},
        "Sosiologi": {"mn": 711, "mx": 746},
        "Ilmu Kesejahteraan Sosial": {"mn": 705, "mx": 740},
        "Kriminologi": {"mn": 703, "mx": 738},
        "Ilmu Pemerintahan": {"mn": 701, "mx": 736},
        "Antropologi Sosial": {"mn": 695, "mx": 730},
        "Ilmu Sejarah": {"mn": 688, "mx": 723},
        "Sastra Inggris": {"mn": 685, "mx": 720},
        "Sastra Indonesia": {"mn": 679, "mx": 714},
        "Pendidikan Bahasa Inggris": {"mn": 676, "mx": 711},
        "Pendidikan Ekonomi": {"mn": 672, "mx": 707},
        "Pendidikan Sejarah": {"mn": 668, "mx": 703},
        "Pendidikan Sosiologi": {"mn": 664, "mx": 699},
        "Perpustakaan dan Ilmu Informasi": {"mn": 662, "mx": 697},
        "Keuangan dan Perbankan": {"mn": 659, "mx": 694},
        "Bisnis Internasional": {"mn": 656, "mx": 691},
        "Pariwisata": {"mn": 649, "mx": 684},
        "Administrasi Negara": {"mn": 647, "mx": 682},
        "Pendidikan Pancasila dan Kewarganegaraan": {"mn": 643, "mx": 678},
        "Sastra Arab": {"mn": 635, "mx": 670},
        "Sastra Jawa": {"mn": 625, "mx": 660},
        "Filsafat": {"mn": 620, "mx": 655},
        "_default": {"mn": 697, "mx": 732},
        "_klaster": 1, "_lbl": "⭐ Klaster 1 — Top Tier"
    },
    "Institut Teknologi Bandung": {
        "Pendidikan Dokter (Kedokteran)": {"mn": 805, "mx": 840},
        "Teknik Informatika": {"mn": 795, "mx": 830},
        "Farmasi": {"mn": 780, "mx": 815},
        "Teknik Elektro": {"mn": 775, "mx": 810},
        "Ilmu Komputer": {"mn": 770, "mx": 805},
        "Teknik Kimia": {"mn": 765, "mx": 800},
        "Teknik Mesin": {"mn": 760, "mx": 795},
        "Teknik Sipil": {"mn": 755, "mx": 790},
        "Kedokteran Gigi": {"mn": 753, "mx": 788},
        "Bioteknologi": {"mn": 745, "mx": 780},
        "Teknik Industri": {"mn": 743, "mx": 778},
        "Statistika": {"mn": 737, "mx": 772},
        "Matematika": {"mn": 733, "mx": 768},
        "Fisika": {"mn": 727, "mx": 762},
        "Kimia": {"mn": 723, "mx": 758},
        "Biologi": {"mn": 720, "mx": 755},
        "Teknik Lingkungan": {"mn": 715, "mx": 750},
        "Teknik Geologi": {"mn": 713, "mx": 748},
        "Teknik Perminyakan": {"mn": 710, "mx": 745},
        "Arsitektur": {"mn": 709, "mx": 744},
        "Perencanaan Wilayah dan Kota": {"mn": 705, "mx": 740},
        "Ilmu Gizi": {"mn": 703, "mx": 738},
        "Keperawatan": {"mn": 697, "mx": 732},
        "Agroteknologi": {"mn": 690, "mx": 725},
        "Agribisnis": {"mn": 688, "mx": 723},
        "Kehutanan": {"mn": 683, "mx": 718},
        "Ilmu Tanah": {"mn": 677, "mx": 712},
        "Teknologi Pangan": {"mn": 675, "mx": 710},
        "Peternakan": {"mn": 670, "mx": 705},
        "Ilmu Kelautan": {"mn": 665, "mx": 700},
        "Psikologi": {"mn": 785, "mx": 820},
        "Hukum": {"mn": 775, "mx": 810},
        "Akuntansi": {"mn": 770, "mx": 805},
        "Manajemen": {"mn": 763, "mx": 798},
        "Ilmu Komunikasi": {"mn": 760, "mx": 795},
        "Ekonomi Pembangunan": {"mn": 753, "mx": 788},
        "Hubungan Internasional": {"mn": 750, "mx": 785},
        "Ilmu Administrasi Bisnis": {"mn": 745, "mx": 780},
        "Ilmu Politik": {"mn": 740, "mx": 775},
        "Sosiologi": {"mn": 733, "mx": 768},
        "Ilmu Kesejahteraan Sosial": {"mn": 727, "mx": 762},
        "Kriminologi": {"mn": 725, "mx": 760},
        "Ilmu Pemerintahan": {"mn": 723, "mx": 758},
        "Antropologi Sosial": {"mn": 717, "mx": 752},
        "Ilmu Sejarah": {"mn": 710, "mx": 745},
        "Sastra Inggris": {"mn": 707, "mx": 742},
        "Sastra Indonesia": {"mn": 700, "mx": 735},
        "Pendidikan Bahasa Inggris": {"mn": 697, "mx": 732},
        "Pendidikan Ekonomi": {"mn": 693, "mx": 728},
        "Pendidikan Sejarah": {"mn": 689, "mx": 724},
        "Pendidikan Sosiologi": {"mn": 685, "mx": 720},
        "Perpustakaan dan Ilmu Informasi": {"mn": 683, "mx": 718},
        "Keuangan dan Perbankan": {"mn": 680, "mx": 715},
        "Bisnis Internasional": {"mn": 677, "mx": 712},
        "Pariwisata": {"mn": 670, "mx": 705},
        "Administrasi Negara": {"mn": 667, "mx": 702},
        "Pendidikan Pancasila dan Kewarganegaraan": {"mn": 663, "mx": 698},
        "Sastra Arab": {"mn": 655, "mx": 690},
        "Sastra Jawa": {"mn": 645, "mx": 680},
        "Filsafat": {"mn": 640, "mx": 675},
        "_default": {"mn": 719, "mx": 754},
        "_klaster": 1, "_lbl": "⭐ Klaster 1 — Top Tier"
    },
    "Universitas Padjadjaran": {
        "Pendidikan Dokter (Kedokteran)": {"mn": 748, "mx": 783},
        "Teknik Informatika": {"mn": 738, "mx": 773},
        "Farmasi": {"mn": 724, "mx": 759},
        "Teknik Elektro": {"mn": 720, "mx": 755},
        "Ilmu Komputer": {"mn": 715, "mx": 750},
        "Teknik Kimia": {"mn": 710, "mx": 745},
        "Teknik Mesin": {"mn": 706, "mx": 741},
        "Teknik Sipil": {"mn": 701, "mx": 736},
        "Kedokteran Gigi": {"mn": 699, "mx": 734},
        "Bioteknologi": {"mn": 692, "mx": 727},
        "Teknik Industri": {"mn": 690, "mx": 725},
        "Statistika": {"mn": 684, "mx": 719},
        "Matematika": {"mn": 681, "mx": 716},
        "Fisika": {"mn": 675, "mx": 710},
        "Kimia": {"mn": 671, "mx": 706},
        "Biologi": {"mn": 669, "mx": 704},
        "Teknik Lingkungan": {"mn": 664, "mx": 699},
        "Teknik Geologi": {"mn": 662, "mx": 697},
        "Teknik Perminyakan": {"mn": 659, "mx": 694},
        "Arsitektur": {"mn": 658, "mx": 693},
        "Perencanaan Wilayah dan Kota": {"mn": 655, "mx": 690},
        "Ilmu Gizi": {"mn": 653, "mx": 688},
        "Keperawatan": {"mn": 647, "mx": 682},
        "Agroteknologi": {"mn": 641, "mx": 676},
        "Agribisnis": {"mn": 639, "mx": 674},
        "Kehutanan": {"mn": 634, "mx": 669},
        "Ilmu Tanah": {"mn": 629, "mx": 664},
        "Teknologi Pangan": {"mn": 627, "mx": 662},
        "Peternakan": {"mn": 622, "mx": 657},
        "Ilmu Kelautan": {"mn": 617, "mx": 652},
        "Psikologi": {"mn": 729, "mx": 764},
        "Hukum": {"mn": 720, "mx": 755},
        "Akuntansi": {"mn": 715, "mx": 750},
        "Manajemen": {"mn": 709, "mx": 744},
        "Ilmu Komunikasi": {"mn": 706, "mx": 741},
        "Ekonomi Pembangunan": {"mn": 699, "mx": 734},
        "Hubungan Internasional": {"mn": 696, "mx": 731},
        "Ilmu Administrasi Bisnis": {"mn": 692, "mx": 727},
        "Ilmu Politik": {"mn": 687, "mx": 722},
        "Sosiologi": {"mn": 681, "mx": 716},
        "Ilmu Kesejahteraan Sosial": {"mn": 675, "mx": 710},
        "Kriminologi": {"mn": 673, "mx": 708},
        "Ilmu Pemerintahan": {"mn": 671, "mx": 706},
        "Antropologi Sosial": {"mn": 666, "mx": 701},
        "Ilmu Sejarah": {"mn": 659, "mx": 694},
        "Sastra Inggris": {"mn": 656, "mx": 691},
        "Sastra Indonesia": {"mn": 650, "mx": 685},
        "Pendidikan Bahasa Inggris": {"mn": 647, "mx": 682},
        "Pendidikan Ekonomi": {"mn": 643, "mx": 678},
        "Pendidikan Sejarah": {"mn": 640, "mx": 675},
        "Pendidikan Sosiologi": {"mn": 636, "mx": 671},
        "Perpustakaan dan Ilmu Informasi": {"mn": 634, "mx": 669},
        "Keuangan dan Perbankan": {"mn": 631, "mx": 666},
        "Bisnis Internasional": {"mn": 629, "mx": 664},
        "Pariwisata": {"mn": 622, "mx": 657},
        "Administrasi Negara": {"mn": 619, "mx": 654},
        "Pendidikan Pancasila dan Kewarganegaraan": {"mn": 616, "mx": 651},
        "Sastra Arab": {"mn": 608, "mx": 643},
        "Sastra Jawa": {"mn": 599, "mx": 634},
        "Filsafat": {"mn": 594, "mx": 629},
        "_default": {"mn": 667, "mx": 702},
        "_klaster": 2, "_lbl": "🔷 Klaster 2 — Menengah Atas"
    },
    "Institut Pertanian Bogor": {
        "Pendidikan Dokter (Kedokteran)": {"mn": 731, "mx": 766},
        "Teknik Informatika": {"mn": 722, "mx": 757},
        "Farmasi": {"mn": 708, "mx": 743},
        "Teknik Elektro": {"mn": 704, "mx": 739},
        "Ilmu Komputer": {"mn": 699, "mx": 734},
        "Teknik Kimia": {"mn": 695, "mx": 730},
        "Teknik Mesin": {"mn": 690, "mx": 725},
        "Teknik Sipil": {"mn": 686, "mx": 721},
        "Kedokteran Gigi": {"mn": 684, "mx": 719},
        "Bioteknologi": {"mn": 677, "mx": 712},
        "Teknik Industri": {"mn": 675, "mx": 710},
        "Statistika": {"mn": 669, "mx": 704},
        "Matematika": {"mn": 666, "mx": 701},
        "Fisika": {"mn": 660, "mx": 695},
        "Kimia": {"mn": 657, "mx": 692},
        "Biologi": {"mn": 654, "mx": 689},
        "Teknik Lingkungan": {"mn": 649, "mx": 684},
        "Teknik Geologi": {"mn": 647, "mx": 682},
        "Teknik Perminyakan": {"mn": 645, "mx": 680},
        "Arsitektur": {"mn": 644, "mx": 679},
        "Perencanaan Wilayah dan Kota": {"mn": 640, "mx": 675},
        "Ilmu Gizi": {"mn": 638, "mx": 673},
        "Keperawatan": {"mn": 633, "mx": 668},
        "Agroteknologi": {"mn": 627, "mx": 662},
        "Agribisnis": {"mn": 625, "mx": 660},
        "Kehutanan": {"mn": 620, "mx": 655},
        "Ilmu Tanah": {"mn": 615, "mx": 650},
        "Teknologi Pangan": {"mn": 613, "mx": 648},
        "Peternakan": {"mn": 608, "mx": 643},
        "Ilmu Kelautan": {"mn": 604, "mx": 639},
        "Psikologi": {"mn": 713, "mx": 748},
        "Hukum": {"mn": 704, "mx": 739},
        "Akuntansi": {"mn": 699, "mx": 734},
        "Manajemen": {"mn": 693, "mx": 728},
        "Ilmu Komunikasi": {"mn": 690, "mx": 725},
        "Ekonomi Pembangunan": {"mn": 684, "mx": 719},
        "Hubungan Internasional": {"mn": 681, "mx": 716},
        "Ilmu Administrasi Bisnis": {"mn": 677, "mx": 712},
        "Ilmu Politik": {"mn": 672, "mx": 707},
        "Sosiologi": {"mn": 666, "mx": 701},
        "Ilmu Kesejahteraan Sosial": {"mn": 660, "mx": 695},
        "Kriminologi": {"mn": 658, "mx": 693},
        "Ilmu Pemerintahan": {"mn": 657, "mx": 692},
        "Antropologi Sosial": {"mn": 651, "mx": 686},
        "Ilmu Sejarah": {"mn": 645, "mx": 680},
        "Sastra Inggris": {"mn": 642, "mx": 677},
        "Sastra Indonesia": {"mn": 636, "mx": 671},
        "Pendidikan Bahasa Inggris": {"mn": 633, "mx": 668},
        "Pendidikan Ekonomi": {"mn": 629, "mx": 664},
        "Pendidikan Sejarah": {"mn": 626, "mx": 661},
        "Pendidikan Sosiologi": {"mn": 622, "mx": 657},
        "Perpustakaan dan Ilmu Informasi": {"mn": 620, "mx": 655},
        "Keuangan dan Perbankan": {"mn": 617, "mx": 652},
        "Bisnis Internasional": {"mn": 615, "mx": 650},
        "Pariwisata": {"mn": 608, "mx": 643},
        "Administrasi Negara": {"mn": 606, "mx": 641},
        "Pendidikan Pancasila dan Kewarganegaraan": {"mn": 602, "mx": 637},
        "Sastra Arab": {"mn": 595, "mx": 630},
        "Sastra Jawa": {"mn": 586, "mx": 621},
        "Filsafat": {"mn": 581, "mx": 616},
        "_default": {"mn": 653, "mx": 688},
        "_klaster": 2, "_lbl": "🔷 Klaster 2 — Menengah Atas"
    },
    "Institut Teknologi Sepuluh Nopember": {
        "Pendidikan Dokter (Kedokteran)": {"mn": 739, "mx": 774},
        "Teknik Informatika": {"mn": 730, "mx": 765},
        "Farmasi": {"mn": 716, "mx": 751},
        "Teknik Elektro": {"mn": 712, "mx": 747},
        "Ilmu Komputer": {"mn": 707, "mx": 742},
        "Teknik Kimia": {"mn": 703, "mx": 738},
        "Teknik Mesin": {"mn": 698, "mx": 733},
        "Teknik Sipil": {"mn": 693, "mx": 728},
        "Kedokteran Gigi": {"mn": 692, "mx": 727},
        "Bioteknologi": {"mn": 684, "mx": 719},
        "Teknik Industri": {"mn": 682, "mx": 717},
        "Statistika": {"mn": 677, "mx": 712},
        "Matematika": {"mn": 673, "mx": 708},
        "Fisika": {"mn": 668, "mx": 703},
        "Kimia": {"mn": 664, "mx": 699},
        "Biologi": {"mn": 661, "mx": 696},
        "Teknik Lingkungan": {"mn": 657, "mx": 692},
        "Teknik Geologi": {"mn": 655, "mx": 690},
        "Teknik Perminyakan": {"mn": 652, "mx": 687},
        "Arsitektur": {"mn": 651, "mx": 686},
        "Perencanaan Wilayah dan Kota": {"mn": 647, "mx": 682},
        "Ilmu Gizi": {"mn": 646, "mx": 681},
        "Keperawatan": {"mn": 640, "mx": 675},
        "Agroteknologi": {"mn": 634, "mx": 669},
        "Agribisnis": {"mn": 632, "mx": 667},
        "Kehutanan": {"mn": 627, "mx": 662},
        "Ilmu Tanah": {"mn": 622, "mx": 657},
        "Teknologi Pangan": {"mn": 620, "mx": 655},
        "Peternakan": {"mn": 615, "mx": 650},
        "Ilmu Kelautan": {"mn": 611, "mx": 646},
        "Psikologi": {"mn": 721, "mx": 756},
        "Hukum": {"mn": 712, "mx": 747},
        "Akuntansi": {"mn": 707, "mx": 742},
        "Manajemen": {"mn": 701, "mx": 736},
        "Ilmu Komunikasi": {"mn": 698, "mx": 733},
        "Ekonomi Pembangunan": {"mn": 692, "mx": 727},
        "Hubungan Internasional": {"mn": 689, "mx": 724},
        "Ilmu Administrasi Bisnis": {"mn": 684, "mx": 719},
        "Ilmu Politik": {"mn": 680, "mx": 715},
        "Sosiologi": {"mn": 673, "mx": 708},
        "Ilmu Kesejahteraan Sosial": {"mn": 668, "mx": 703},
        "Kriminologi": {"mn": 666, "mx": 701},
        "Ilmu Pemerintahan": {"mn": 664, "mx": 699},
        "Antropologi Sosial": {"mn": 658, "mx": 693},
        "Ilmu Sejarah": {"mn": 652, "mx": 687},
        "Sastra Inggris": {"mn": 649, "mx": 684},
        "Sastra Indonesia": {"mn": 643, "mx": 678},
        "Pendidikan Bahasa Inggris": {"mn": 640, "mx": 675},
        "Pendidikan Ekonomi": {"mn": 636, "mx": 671},
        "Pendidikan Sejarah": {"mn": 633, "mx": 668},
        "Pendidikan Sosiologi": {"mn": 629, "mx": 664},
        "Perpustakaan dan Ilmu Informasi": {"mn": 627, "mx": 662},
        "Keuangan dan Perbankan": {"mn": 624, "mx": 659},
        "Bisnis Internasional": {"mn": 622, "mx": 657},
        "Pariwisata": {"mn": 615, "mx": 650},
        "Administrasi Negara": {"mn": 612, "mx": 647},
        "Pendidikan Pancasila dan Kewarganegaraan": {"mn": 609, "mx": 644},
        "Sastra Arab": {"mn": 601, "mx": 636},
        "Sastra Jawa": {"mn": 592, "mx": 627},
        "Filsafat": {"mn": 588, "mx": 623},
        "_default": {"mn": 660, "mx": 695},
        "_klaster": 2, "_lbl": "🔷 Klaster 2 — Menengah Atas"
    },
    "Universitas Diponegoro": {
        "Pendidikan Dokter (Kedokteran)": {"mn": 731, "mx": 766},
        "Teknik Informatika": {"mn": 722, "mx": 757},
        "Farmasi": {"mn": 708, "mx": 743},
        "Teknik Elektro": {"mn": 704, "mx": 739},
        "Ilmu Komputer": {"mn": 699, "mx": 734},
        "Teknik Kimia": {"mn": 695, "mx": 730},
        "Teknik Mesin": {"mn": 690, "mx": 725},
        "Teknik Sipil": {"mn": 686, "mx": 721},
        "Kedokteran Gigi": {"mn": 684, "mx": 719},
        "Bioteknologi": {"mn": 677, "mx": 712},
        "Teknik Industri": {"mn": 675, "mx": 710},
        "Statistika": {"mn": 669, "mx": 704},
        "Matematika": {"mn": 666, "mx": 701},
        "Fisika": {"mn": 660, "mx": 695},
        "Kimia": {"mn": 657, "mx": 692},
        "Biologi": {"mn": 654, "mx": 689},
        "Teknik Lingkungan": {"mn": 649, "mx": 684},
        "Teknik Geologi": {"mn": 647, "mx": 682},
        "Teknik Perminyakan": {"mn": 645, "mx": 680},
        "Arsitektur": {"mn": 644, "mx": 679},
        "Perencanaan Wilayah dan Kota": {"mn": 640, "mx": 675},
        "Ilmu Gizi": {"mn": 638, "mx": 673},
        "Keperawatan": {"mn": 633, "mx": 668},
        "Agroteknologi": {"mn": 627, "mx": 662},
        "Agribisnis": {"mn": 625, "mx": 660},
        "Kehutanan": {"mn": 620, "mx": 655},
        "Ilmu Tanah": {"mn": 615, "mx": 650},
        "Teknologi Pangan": {"mn": 613, "mx": 648},
        "Peternakan": {"mn": 608, "mx": 643},
        "Ilmu Kelautan": {"mn": 604, "mx": 639},
        "Psikologi": {"mn": 713, "mx": 748},
        "Hukum": {"mn": 704, "mx": 739},
        "Akuntansi": {"mn": 699, "mx": 734},
        "Manajemen": {"mn": 693, "mx": 728},
        "Ilmu Komunikasi": {"mn": 690, "mx": 725},
        "Ekonomi Pembangunan": {"mn": 684, "mx": 719},
        "Hubungan Internasional": {"mn": 681, "mx": 716},
        "Ilmu Administrasi Bisnis": {"mn": 677, "mx": 712},
        "Ilmu Politik": {"mn": 672, "mx": 707},
        "Sosiologi": {"mn": 666, "mx": 701},
        "Ilmu Kesejahteraan Sosial": {"mn": 660, "mx": 695},
        "Kriminologi": {"mn": 658, "mx": 693},
        "Ilmu Pemerintahan": {"mn": 657, "mx": 692},
        "Antropologi Sosial": {"mn": 651, "mx": 686},
        "Ilmu Sejarah": {"mn": 645, "mx": 680},
        "Sastra Inggris": {"mn": 642, "mx": 677},
        "Sastra Indonesia": {"mn": 636, "mx": 671},
        "Pendidikan Bahasa Inggris": {"mn": 633, "mx": 668},
        "Pendidikan Ekonomi": {"mn": 629, "mx": 664},
        "Pendidikan Sejarah": {"mn": 626, "mx": 661},
        "Pendidikan Sosiologi": {"mn": 622, "mx": 657},
        "Perpustakaan dan Ilmu Informasi": {"mn": 620, "mx": 655},
        "Keuangan dan Perbankan": {"mn": 617, "mx": 652},
        "Bisnis Internasional": {"mn": 615, "mx": 650},
        "Pariwisata": {"mn": 608, "mx": 643},
        "Administrasi Negara": {"mn": 606, "mx": 641},
        "Pendidikan Pancasila dan Kewarganegaraan": {"mn": 602, "mx": 637},
        "Sastra Arab": {"mn": 595, "mx": 630},
        "Sastra Jawa": {"mn": 586, "mx": 621},
        "Filsafat": {"mn": 581, "mx": 616},
        "_default": {"mn": 653, "mx": 688},
        "_klaster": 2, "_lbl": "🔷 Klaster 2 — Menengah Atas"
    },
    "Universitas Brawijaya": {
        "Pendidikan Dokter (Kedokteran)": {"mn": 707, "mx": 742},
        "Teknik Informatika": {"mn": 698, "mx": 733},
        "Farmasi": {"mn": 685, "mx": 720},
        "Teknik Elektro": {"mn": 680, "mx": 715},
        "Ilmu Komputer": {"mn": 676, "mx": 711},
        "Teknik Kimia": {"mn": 671, "mx": 706},
        "Teknik Mesin": {"mn": 667, "mx": 702},
        "Teknik Sipil": {"mn": 663, "mx": 698},
        "Kedokteran Gigi": {"mn": 661, "mx": 696},
        "Bioteknologi": {"mn": 654, "mx": 689},
        "Teknik Industri": {"mn": 652, "mx": 687},
        "Statistika": {"mn": 647, "mx": 682},
        "Matematika": {"mn": 643, "mx": 678},
        "Fisika": {"mn": 638, "mx": 673},
        "Kimia": {"mn": 634, "mx": 669},
        "Biologi": {"mn": 632, "mx": 667},
        "Teknik Lingkungan": {"mn": 627, "mx": 662},
        "Teknik Geologi": {"mn": 626, "mx": 661},
        "Teknik Perminyakan": {"mn": 623, "mx": 658},
        "Arsitektur": {"mn": 622, "mx": 657},
        "Perencanaan Wilayah dan Kota": {"mn": 619, "mx": 654},
        "Ilmu Gizi": {"mn": 617, "mx": 652},
        "Keperawatan": {"mn": 612, "mx": 647},
        "Agroteknologi": {"mn": 605, "mx": 640},
        "Agribisnis": {"mn": 604, "mx": 639},
        "Kehutanan": {"mn": 599, "mx": 634},
        "Ilmu Tanah": {"mn": 594, "mx": 629},
        "Teknologi Pangan": {"mn": 592, "mx": 627},
        "Peternakan": {"mn": 588, "mx": 623},
        "Ilmu Kelautan": {"mn": 583, "mx": 618},
        "Psikologi": {"mn": 689, "mx": 724},
        "Hukum": {"mn": 680, "mx": 715},
        "Akuntansi": {"mn": 676, "mx": 711},
        "Manajemen": {"mn": 670, "mx": 705},
        "Ilmu Komunikasi": {"mn": 667, "mx": 702},
        "Ekonomi Pembangunan": {"mn": 661, "mx": 696},
        "Hubungan Internasional": {"mn": 658, "mx": 693},
        "Ilmu Administrasi Bisnis": {"mn": 654, "mx": 689},
        "Ilmu Politik": {"mn": 649, "mx": 684},
        "Sosiologi": {"mn": 643, "mx": 678},
        "Ilmu Kesejahteraan Sosial": {"mn": 638, "mx": 673},
        "Kriminologi": {"mn": 636, "mx": 671},
        "Ilmu Pemerintahan": {"mn": 634, "mx": 669},
        "Antropologi Sosial": {"mn": 629, "mx": 664},
        "Ilmu Sejarah": {"mn": 623, "mx": 658},
        "Sastra Inggris": {"mn": 620, "mx": 655},
        "Sastra Indonesia": {"mn": 614, "mx": 649},
        "Pendidikan Bahasa Inggris": {"mn": 612, "mx": 647},
        "Pendidikan Ekonomi": {"mn": 608, "mx": 643},
        "Pendidikan Sejarah": {"mn": 605, "mx": 640},
        "Pendidikan Sosiologi": {"mn": 601, "mx": 636},
        "Perpustakaan dan Ilmu Informasi": {"mn": 599, "mx": 634},
        "Keuangan dan Perbankan": {"mn": 597, "mx": 632},
        "Bisnis Internasional": {"mn": 594, "mx": 629},
        "Pariwisata": {"mn": 588, "mx": 623},
        "Administrasi Negara": {"mn": 585, "mx": 620},
        "Pendidikan Pancasila dan Kewarganegaraan": {"mn": 582, "mx": 617},
        "Sastra Arab": {"mn": 575, "mx": 610},
        "Sastra Jawa": {"mn": 566, "mx": 601},
        "Filsafat": {"mn": 561, "mx": 596},
        "_default": {"mn": 631, "mx": 666},
        "_klaster": 2, "_lbl": "🔷 Klaster 2 — Menengah Atas"
    },
    "Universitas Sebelas Maret": {
        "Pendidikan Dokter (Kedokteran)": {"mn": 698, "mx": 733},
        "Teknik Informatika": {"mn": 690, "mx": 725},
        "Farmasi": {"mn": 677, "mx": 712},
        "Teknik Elektro": {"mn": 672, "mx": 707},
        "Ilmu Komputer": {"mn": 668, "mx": 703},
        "Teknik Kimia": {"mn": 664, "mx": 699},
        "Teknik Mesin": {"mn": 659, "mx": 694},
        "Teknik Sipil": {"mn": 655, "mx": 690},
        "Kedokteran Gigi": {"mn": 653, "mx": 688},
        "Bioteknologi": {"mn": 646, "mx": 681},
        "Teknik Industri": {"mn": 644, "mx": 679},
        "Statistika": {"mn": 639, "mx": 674},
        "Matematika": {"mn": 636, "mx": 671},
        "Fisika": {"mn": 631, "mx": 666},
        "Kimia": {"mn": 627, "mx": 662},
        "Biologi": {"mn": 624, "mx": 659},
        "Teknik Lingkungan": {"mn": 620, "mx": 655},
        "Teknik Geologi": {"mn": 618, "mx": 653},
        "Teknik Perminyakan": {"mn": 616, "mx": 651},
        "Arsitektur": {"mn": 615, "mx": 650},
        "Perencanaan Wilayah dan Kota": {"mn": 611, "mx": 646},
        "Ilmu Gizi": {"mn": 610, "mx": 645},
        "Keperawatan": {"mn": 604, "mx": 639},
        "Agroteknologi": {"mn": 598, "mx": 633},
        "Agribisnis": {"mn": 597, "mx": 632},
        "Kehutanan": {"mn": 592, "mx": 627},
        "Ilmu Tanah": {"mn": 587, "mx": 622},
        "Teknologi Pangan": {"mn": 585, "mx": 620},
        "Peternakan": {"mn": 581, "mx": 616},
        "Ilmu Kelautan": {"mn": 577, "mx": 612},
        "Psikologi": {"mn": 681, "mx": 716},
        "Hukum": {"mn": 672, "mx": 707},
        "Akuntansi": {"mn": 668, "mx": 703},
        "Manajemen": {"mn": 662, "mx": 697},
        "Ilmu Komunikasi": {"mn": 659, "mx": 694},
        "Ekonomi Pembangunan": {"mn": 653, "mx": 688},
        "Hubungan Internasional": {"mn": 651, "mx": 686},
        "Ilmu Administrasi Bisnis": {"mn": 646, "mx": 681},
        "Ilmu Politik": {"mn": 642, "mx": 677},
        "Sosiologi": {"mn": 636, "mx": 671},
        "Ilmu Kesejahteraan Sosial": {"mn": 631, "mx": 666},
        "Kriminologi": {"mn": 629, "mx": 664},
        "Ilmu Pemerintahan": {"mn": 627, "mx": 662},
        "Antropologi Sosial": {"mn": 622, "mx": 657},
        "Ilmu Sejarah": {"mn": 616, "mx": 651},
        "Sastra Inggris": {"mn": 613, "mx": 648},
        "Sastra Indonesia": {"mn": 607, "mx": 642},
        "Pendidikan Bahasa Inggris": {"mn": 604, "mx": 639},
        "Pendidikan Ekonomi": {"mn": 601, "mx": 636},
        "Pendidikan Sejarah": {"mn": 597, "mx": 632},
        "Pendidikan Sosiologi": {"mn": 594, "mx": 629},
        "Perpustakaan dan Ilmu Informasi": {"mn": 592, "mx": 627},
        "Keuangan dan Perbankan": {"mn": 590, "mx": 625},
        "Bisnis Internasional": {"mn": 587, "mx": 622},
        "Pariwisata": {"mn": 581, "mx": 616},
        "Administrasi Negara": {"mn": 578, "mx": 613},
        "Pendidikan Pancasila dan Kewarganegaraan": {"mn": 575, "mx": 610},
        "Sastra Arab": {"mn": 568, "mx": 603},
        "Sastra Jawa": {"mn": 559, "mx": 594},
        "Filsafat": {"mn": 555, "mx": 590},
        "_default": {"mn": 623, "mx": 658},
        "_klaster": 2, "_lbl": "🔷 Klaster 2 — Menengah Atas"
    },
    "Universitas Hasanuddin": {
        "Pendidikan Dokter (Kedokteran)": {"mn": 690, "mx": 725},
        "Teknik Informatika": {"mn": 682, "mx": 717},
        "Farmasi": {"mn": 669, "mx": 704},
        "Teknik Elektro": {"mn": 664, "mx": 699},
        "Ilmu Komputer": {"mn": 660, "mx": 695},
        "Teknik Kimia": {"mn": 656, "mx": 691},
        "Teknik Mesin": {"mn": 651, "mx": 686},
        "Teknik Sipil": {"mn": 647, "mx": 682},
        "Kedokteran Gigi": {"mn": 645, "mx": 680},
        "Bioteknologi": {"mn": 639, "mx": 674},
        "Teknik Industri": {"mn": 637, "mx": 672},
        "Statistika": {"mn": 632, "mx": 667},
        "Matematika": {"mn": 628, "mx": 663},
        "Fisika": {"mn": 623, "mx": 658},
        "Kimia": {"mn": 620, "mx": 655},
        "Biologi": {"mn": 617, "mx": 652},
        "Teknik Lingkungan": {"mn": 613, "mx": 648},
        "Teknik Geologi": {"mn": 611, "mx": 646},
        "Teknik Perminyakan": {"mn": 609, "mx": 644},
        "Arsitektur": {"mn": 608, "mx": 643},
        "Perencanaan Wilayah dan Kota": {"mn": 604, "mx": 639},
        "Ilmu Gizi": {"mn": 602, "mx": 637},
        "Keperawatan": {"mn": 597, "mx": 632},
        "Agroteknologi": {"mn": 591, "mx": 626},
        "Agribisnis": {"mn": 590, "mx": 625},
        "Kehutanan": {"mn": 585, "mx": 620},
        "Ilmu Tanah": {"mn": 580, "mx": 615},
        "Teknologi Pangan": {"mn": 578, "mx": 613},
        "Peternakan": {"mn": 574, "mx": 609},
        "Ilmu Kelautan": {"mn": 570, "mx": 605},
        "Psikologi": {"mn": 673, "mx": 708},
        "Hukum": {"mn": 664, "mx": 699},
        "Akuntansi": {"mn": 660, "mx": 695},
        "Manajemen": {"mn": 654, "mx": 689},
        "Ilmu Komunikasi": {"mn": 651, "mx": 686},
        "Ekonomi Pembangunan": {"mn": 645, "mx": 680},
        "Hubungan Internasional": {"mn": 643, "mx": 678},
        "Ilmu Administrasi Bisnis": {"mn": 639, "mx": 674},
        "Ilmu Politik": {"mn": 634, "mx": 669},
        "Sosiologi": {"mn": 628, "mx": 663},
        "Ilmu Kesejahteraan Sosial": {"mn": 623, "mx": 658},
        "Kriminologi": {"mn": 621, "mx": 656},
        "Ilmu Pemerintahan": {"mn": 620, "mx": 655},
        "Antropologi Sosial": {"mn": 615, "mx": 650},
        "Ilmu Sejarah": {"mn": 609, "mx": 644},
        "Sastra Inggris": {"mn": 606, "mx": 641},
        "Sastra Indonesia": {"mn": 600, "mx": 635},
        "Pendidikan Bahasa Inggris": {"mn": 597, "mx": 632},
        "Pendidikan Ekonomi": {"mn": 594, "mx": 629},
        "Pendidikan Sejarah": {"mn": 590, "mx": 625},
        "Pendidikan Sosiologi": {"mn": 587, "mx": 622},
        "Perpustakaan dan Ilmu Informasi": {"mn": 585, "mx": 620},
        "Keuangan dan Perbankan": {"mn": 583, "mx": 618},
        "Bisnis Internasional": {"mn": 580, "mx": 615},
        "Pariwisata": {"mn": 574, "mx": 609},
        "Administrasi Negara": {"mn": 572, "mx": 607},
        "Pendidikan Pancasila dan Kewarganegaraan": {"mn": 568, "mx": 603},
        "Sastra Arab": {"mn": 561, "mx": 596},
        "Sastra Jawa": {"mn": 553, "mx": 588},
        "Filsafat": {"mn": 548, "mx": 583},
        "_default": {"mn": 616, "mx": 651},
        "_klaster": 2, "_lbl": "🔷 Klaster 2 — Menengah Atas"
    },
    "Universitas Pendidikan Indonesia": {
        "Pendidikan Dokter (Kedokteran)": {"mn": 657, "mx": 692},
        "Teknik Informatika": {"mn": 649, "mx": 684},
        "Farmasi": {"mn": 637, "mx": 672},
        "Teknik Elektro": {"mn": 633, "mx": 668},
        "Ilmu Komputer": {"mn": 629, "mx": 664},
        "Teknik Kimia": {"mn": 625, "mx": 660},
        "Teknik Mesin": {"mn": 621, "mx": 656},
        "Teknik Sipil": {"mn": 616, "mx": 651},
        "Kedokteran Gigi": {"mn": 615, "mx": 650},
        "Bioteknologi": {"mn": 608, "mx": 643},
        "Teknik Industri": {"mn": 607, "mx": 642},
        "Statistika": {"mn": 602, "mx": 637},
        "Matematika": {"mn": 598, "mx": 633},
        "Fisika": {"mn": 593, "mx": 628},
        "Kimia": {"mn": 590, "mx": 625},
        "Biologi": {"mn": 588, "mx": 623},
        "Teknik Lingkungan": {"mn": 584, "mx": 619},
        "Teknik Geologi": {"mn": 582, "mx": 617},
        "Teknik Perminyakan": {"mn": 579, "mx": 614},
        "Arsitektur": {"mn": 579, "mx": 614},
        "Perencanaan Wilayah dan Kota": {"mn": 575, "mx": 610},
        "Ilmu Gizi": {"mn": 574, "mx": 609},
        "Keperawatan": {"mn": 569, "mx": 604},
        "Agroteknologi": {"mn": 563, "mx": 598},
        "Agribisnis": {"mn": 561, "mx": 596},
        "Kehutanan": {"mn": 557, "mx": 592},
        "Ilmu Tanah": {"mn": 552, "mx": 587},
        "Teknologi Pangan": {"mn": 551, "mx": 586},
        "Peternakan": {"mn": 547, "mx": 582},
        "Ilmu Kelautan": {"mn": 543, "mx": 578},
        "Psikologi": {"mn": 641, "mx": 676},
        "Hukum": {"mn": 633, "mx": 668},
        "Akuntansi": {"mn": 629, "mx": 664},
        "Manajemen": {"mn": 623, "mx": 658},
        "Ilmu Komunikasi": {"mn": 621, "mx": 656},
        "Ekonomi Pembangunan": {"mn": 615, "mx": 650},
        "Hubungan Internasional": {"mn": 612, "mx": 647},
        "Ilmu Administrasi Bisnis": {"mn": 608, "mx": 643},
        "Ilmu Politik": {"mn": 604, "mx": 639},
        "Sosiologi": {"mn": 598, "mx": 633},
        "Ilmu Kesejahteraan Sosial": {"mn": 593, "mx": 628},
        "Kriminologi": {"mn": 592, "mx": 627},
        "Ilmu Pemerintahan": {"mn": 590, "mx": 625},
        "Antropologi Sosial": {"mn": 585, "mx": 620},
        "Ilmu Sejarah": {"mn": 579, "mx": 614},
        "Sastra Inggris": {"mn": 577, "mx": 612},
        "Sastra Indonesia": {"mn": 571, "mx": 606},
        "Pendidikan Bahasa Inggris": {"mn": 569, "mx": 604},
        "Pendidikan Ekonomi": {"mn": 566, "mx": 601},
        "Pendidikan Sejarah": {"mn": 562, "mx": 597},
        "Pendidikan Sosiologi": {"mn": 559, "mx": 594},
        "Perpustakaan dan Ilmu Informasi": {"mn": 557, "mx": 592},
        "Keuangan dan Perbankan": {"mn": 555, "mx": 590},
        "Bisnis Internasional": {"mn": 552, "mx": 587},
        "Pariwisata": {"mn": 547, "mx": 582},
        "Administrasi Negara": {"mn": 544, "mx": 579},
        "Pendidikan Pancasila dan Kewarganegaraan": {"mn": 541, "mx": 576},
        "Sastra Arab": {"mn": 534, "mx": 569},
        "Sastra Jawa": {"mn": 526, "mx": 561},
        "Filsafat": {"mn": 522, "mx": 557},
        "_default": {"mn": 586, "mx": 621},
        "_klaster": 3, "_lbl": "🔹 Klaster 3 — Menengah"
    },
    "Universitas Sumatera Utara": {
        "Pendidikan Dokter (Kedokteran)": {"mn": 657, "mx": 692},
        "Teknik Informatika": {"mn": 649, "mx": 684},
        "Farmasi": {"mn": 637, "mx": 672},
        "Teknik Elektro": {"mn": 633, "mx": 668},
        "Ilmu Komputer": {"mn": 629, "mx": 664},
        "Teknik Kimia": {"mn": 625, "mx": 660},
        "Teknik Mesin": {"mn": 621, "mx": 656},
        "Teknik Sipil": {"mn": 616, "mx": 651},
        "Kedokteran Gigi": {"mn": 615, "mx": 650},
        "Bioteknologi": {"mn": 608, "mx": 643},
        "Teknik Industri": {"mn": 607, "mx": 642},
        "Statistika": {"mn": 602, "mx": 637},
        "Matematika": {"mn": 598, "mx": 633},
        "Fisika": {"mn": 593, "mx": 628},
        "Kimia": {"mn": 590, "mx": 625},
        "Biologi": {"mn": 588, "mx": 623},
        "Teknik Lingkungan": {"mn": 584, "mx": 619},
        "Teknik Geologi": {"mn": 582, "mx": 617},
        "Teknik Perminyakan": {"mn": 579, "mx": 614},
        "Arsitektur": {"mn": 579, "mx": 614},
        "Perencanaan Wilayah dan Kota": {"mn": 575, "mx": 610},
        "Ilmu Gizi": {"mn": 574, "mx": 609},
        "Keperawatan": {"mn": 569, "mx": 604},
        "Agroteknologi": {"mn": 563, "mx": 598},
        "Agribisnis": {"mn": 561, "mx": 596},
        "Kehutanan": {"mn": 557, "mx": 592},
        "Ilmu Tanah": {"mn": 552, "mx": 587},
        "Teknologi Pangan": {"mn": 551, "mx": 586},
        "Peternakan": {"mn": 547, "mx": 582},
        "Ilmu Kelautan": {"mn": 543, "mx": 578},
        "Psikologi": {"mn": 641, "mx": 676},
        "Hukum": {"mn": 633, "mx": 668},
        "Akuntansi": {"mn": 629, "mx": 664},
        "Manajemen": {"mn": 623, "mx": 658},
        "Ilmu Komunikasi": {"mn": 621, "mx": 656},
        "Ekonomi Pembangunan": {"mn": 615, "mx": 650},
        "Hubungan Internasional": {"mn": 612, "mx": 647},
        "Ilmu Administrasi Bisnis": {"mn": 608, "mx": 643},
        "Ilmu Politik": {"mn": 604, "mx": 639},
        "Sosiologi": {"mn": 598, "mx": 633},
        "Ilmu Kesejahteraan Sosial": {"mn": 593, "mx": 628},
        "Kriminologi": {"mn": 592, "mx": 627},
        "Ilmu Pemerintahan": {"mn": 590, "mx": 625},
        "Antropologi Sosial": {"mn": 585, "mx": 620},
        "Ilmu Sejarah": {"mn": 579, "mx": 614},
        "Sastra Inggris": {"mn": 577, "mx": 612},
        "Sastra Indonesia": {"mn": 571, "mx": 606},
        "Pendidikan Bahasa Inggris": {"mn": 569, "mx": 604},
        "Pendidikan Ekonomi": {"mn": 566, "mx": 601},
        "Pendidikan Sejarah": {"mn": 562, "mx": 597},
        "Pendidikan Sosiologi": {"mn": 559, "mx": 594},
        "Perpustakaan dan Ilmu Informasi": {"mn": 557, "mx": 592},
        "Keuangan dan Perbankan": {"mn": 555, "mx": 590},
        "Bisnis Internasional": {"mn": 552, "mx": 587},
        "Pariwisata": {"mn": 547, "mx": 582},
        "Administrasi Negara": {"mn": 544, "mx": 579},
        "Pendidikan Pancasila dan Kewarganegaraan": {"mn": 541, "mx": 576},
        "Sastra Arab": {"mn": 534, "mx": 569},
        "Sastra Jawa": {"mn": 526, "mx": 561},
        "Filsafat": {"mn": 522, "mx": 557},
        "_default": {"mn": 586, "mx": 621},
        "_klaster": 3, "_lbl": "🔹 Klaster 3 — Menengah"
    },
    "Universitas Negeri Yogyakarta": {
        "Pendidikan Dokter (Kedokteran)": {"mn": 657, "mx": 692},
        "Teknik Informatika": {"mn": 649, "mx": 684},
        "Farmasi": {"mn": 637, "mx": 672},
        "Teknik Elektro": {"mn": 633, "mx": 668},
        "Ilmu Komputer": {"mn": 629, "mx": 664},
        "Teknik Kimia": {"mn": 625, "mx": 660},
        "Teknik Mesin": {"mn": 621, "mx": 656},
        "Teknik Sipil": {"mn": 616, "mx": 651},
        "Kedokteran Gigi": {"mn": 615, "mx": 650},
        "Bioteknologi": {"mn": 608, "mx": 643},
        "Teknik Industri": {"mn": 607, "mx": 642},
        "Statistika": {"mn": 602, "mx": 637},
        "Matematika": {"mn": 598, "mx": 633},
        "Fisika": {"mn": 593, "mx": 628},
        "Kimia": {"mn": 590, "mx": 625},
        "Biologi": {"mn": 588, "mx": 623},
        "Teknik Lingkungan": {"mn": 584, "mx": 619},
        "Teknik Geologi": {"mn": 582, "mx": 617},
        "Teknik Perminyakan": {"mn": 579, "mx": 614},
        "Arsitektur": {"mn": 579, "mx": 614},
        "Perencanaan Wilayah dan Kota": {"mn": 575, "mx": 610},
        "Ilmu Gizi": {"mn": 574, "mx": 609},
        "Keperawatan": {"mn": 569, "mx": 604},
        "Agroteknologi": {"mn": 563, "mx": 598},
        "Agribisnis": {"mn": 561, "mx": 596},
        "Kehutanan": {"mn": 557, "mx": 592},
        "Ilmu Tanah": {"mn": 552, "mx": 587},
        "Teknologi Pangan": {"mn": 551, "mx": 586},
        "Peternakan": {"mn": 547, "mx": 582},
        "Ilmu Kelautan": {"mn": 543, "mx": 578},
        "Psikologi": {"mn": 641, "mx": 676},
        "Hukum": {"mn": 633, "mx": 668},
        "Akuntansi": {"mn": 629, "mx": 664},
        "Manajemen": {"mn": 623, "mx": 658},
        "Ilmu Komunikasi": {"mn": 621, "mx": 656},
        "Ekonomi Pembangunan": {"mn": 615, "mx": 650},
        "Hubungan Internasional": {"mn": 612, "mx": 647},
        "Ilmu Administrasi Bisnis": {"mn": 608, "mx": 643},
        "Ilmu Politik": {"mn": 604, "mx": 639},
        "Sosiologi": {"mn": 598, "mx": 633},
        "Ilmu Kesejahteraan Sosial": {"mn": 593, "mx": 628},
        "Kriminologi": {"mn": 592, "mx": 627},
        "Ilmu Pemerintahan": {"mn": 590, "mx": 625},
        "Antropologi Sosial": {"mn": 585, "mx": 620},
        "Ilmu Sejarah": {"mn": 579, "mx": 614},
        "Sastra Inggris": {"mn": 577, "mx": 612},
        "Sastra Indonesia": {"mn": 571, "mx": 606},
        "Pendidikan Bahasa Inggris": {"mn": 569, "mx": 604},
        "Pendidikan Ekonomi": {"mn": 566, "mx": 601},
        "Pendidikan Sejarah": {"mn": 562, "mx": 597},
        "Pendidikan Sosiologi": {"mn": 559, "mx": 594},
        "Perpustakaan dan Ilmu Informasi": {"mn": 557, "mx": 592},
        "Keuangan dan Perbankan": {"mn": 555, "mx": 590},
        "Bisnis Internasional": {"mn": 552, "mx": 587},
        "Pariwisata": {"mn": 547, "mx": 582},
        "Administrasi Negara": {"mn": 544, "mx": 579},
        "Pendidikan Pancasila dan Kewarganegaraan": {"mn": 541, "mx": 576},
        "Sastra Arab": {"mn": 534, "mx": 569},
        "Sastra Jawa": {"mn": 526, "mx": 561},
        "Filsafat": {"mn": 522, "mx": 557},
        "_default": {"mn": 586, "mx": 621},
        "_klaster": 3, "_lbl": "🔹 Klaster 3 — Menengah"
    },
    "Universitas Negeri Malang": {
        "Pendidikan Dokter (Kedokteran)": {"mn": 641, "mx": 676},
        "Teknik Informatika": {"mn": 633, "mx": 668},
        "Farmasi": {"mn": 621, "mx": 656},
        "Teknik Elektro": {"mn": 617, "mx": 652},
        "Ilmu Komputer": {"mn": 613, "mx": 648},
        "Teknik Kimia": {"mn": 609, "mx": 644},
        "Teknik Mesin": {"mn": 605, "mx": 640},
        "Teknik Sipil": {"mn": 601, "mx": 636},
        "Kedokteran Gigi": {"mn": 599, "mx": 634},
        "Bioteknologi": {"mn": 593, "mx": 628},
        "Teknik Industri": {"mn": 591, "mx": 626},
        "Statistika": {"mn": 587, "mx": 622},
        "Matematika": {"mn": 583, "mx": 618},
        "Fisika": {"mn": 579, "mx": 614},
        "Kimia": {"mn": 575, "mx": 610},
        "Biologi": {"mn": 573, "mx": 608},
        "Teknik Lingkungan": {"mn": 569, "mx": 604},
        "Teknik Geologi": {"mn": 567, "mx": 602},
        "Teknik Perminyakan": {"mn": 565, "mx": 600},
        "Arsitektur": {"mn": 564, "mx": 599},
        "Perencanaan Wilayah dan Kota": {"mn": 561, "mx": 596},
        "Ilmu Gizi": {"mn": 559, "mx": 594},
        "Keperawatan": {"mn": 555, "mx": 590},
        "Agroteknologi": {"mn": 549, "mx": 584},
        "Agribisnis": {"mn": 547, "mx": 582},
        "Kehutanan": {"mn": 543, "mx": 578},
        "Ilmu Tanah": {"mn": 539, "mx": 574},
        "Teknologi Pangan": {"mn": 537, "mx": 572},
        "Peternakan": {"mn": 533, "mx": 568},
        "Ilmu Kelautan": {"mn": 529, "mx": 564},
        "Psikologi": {"mn": 625, "mx": 660},
        "Hukum": {"mn": 617, "mx": 652},
        "Akuntansi": {"mn": 613, "mx": 648},
        "Manajemen": {"mn": 607, "mx": 642},
        "Ilmu Komunikasi": {"mn": 605, "mx": 640},
        "Ekonomi Pembangunan": {"mn": 599, "mx": 634},
        "Hubungan Internasional": {"mn": 597, "mx": 632},
        "Ilmu Administrasi Bisnis": {"mn": 593, "mx": 628},
        "Ilmu Politik": {"mn": 589, "mx": 624},
        "Sosiologi": {"mn": 583, "mx": 618},
        "Ilmu Kesejahteraan Sosial": {"mn": 579, "mx": 614},
        "Kriminologi": {"mn": 577, "mx": 612},
        "Ilmu Pemerintahan": {"mn": 575, "mx": 610},
        "Antropologi Sosial": {"mn": 571, "mx": 606},
        "Ilmu Sejarah": {"mn": 565, "mx": 600},
        "Sastra Inggris": {"mn": 563, "mx": 598},
        "Sastra Indonesia": {"mn": 557, "mx": 592},
        "Pendidikan Bahasa Inggris": {"mn": 555, "mx": 590},
        "Pendidikan Ekonomi": {"mn": 551, "mx": 586},
        "Pendidikan Sejarah": {"mn": 548, "mx": 583},
        "Pendidikan Sosiologi": {"mn": 545, "mx": 580},
        "Perpustakaan dan Ilmu Informasi": {"mn": 543, "mx": 578},
        "Keuangan dan Perbankan": {"mn": 541, "mx": 576},
        "Bisnis Internasional": {"mn": 539, "mx": 574},
        "Pariwisata": {"mn": 533, "mx": 568},
        "Administrasi Negara": {"mn": 531, "mx": 566},
        "Pendidikan Pancasila dan Kewarganegaraan": {"mn": 527, "mx": 562},
        "Sastra Arab": {"mn": 521, "mx": 556},
        "Sastra Jawa": {"mn": 513, "mx": 548},
        "Filsafat": {"mn": 509, "mx": 544},
        "_default": {"mn": 572, "mx": 607},
        "_klaster": 3, "_lbl": "🔹 Klaster 3 — Menengah"
    },
    "Universitas Lampung": {
        "Pendidikan Dokter (Kedokteran)": {"mn": 633, "mx": 668},
        "Teknik Informatika": {"mn": 625, "mx": 660},
        "Farmasi": {"mn": 613, "mx": 648},
        "Teknik Elektro": {"mn": 609, "mx": 644},
        "Ilmu Komputer": {"mn": 605, "mx": 640},
        "Teknik Kimia": {"mn": 601, "mx": 636},
        "Teknik Mesin": {"mn": 597, "mx": 632},
        "Teknik Sipil": {"mn": 593, "mx": 628},
        "Kedokteran Gigi": {"mn": 592, "mx": 627},
        "Bioteknologi": {"mn": 585, "mx": 620},
        "Teknik Industri": {"mn": 584, "mx": 619},
        "Statistika": {"mn": 579, "mx": 614},
        "Matematika": {"mn": 576, "mx": 611},
        "Fisika": {"mn": 571, "mx": 606},
        "Kimia": {"mn": 568, "mx": 603},
        "Biologi": {"mn": 566, "mx": 601},
        "Teknik Lingkungan": {"mn": 562, "mx": 597},
        "Teknik Geologi": {"mn": 560, "mx": 595},
        "Teknik Perminyakan": {"mn": 558, "mx": 593},
        "Arsitektur": {"mn": 557, "mx": 592},
        "Perencanaan Wilayah dan Kota": {"mn": 554, "mx": 589},
        "Ilmu Gizi": {"mn": 552, "mx": 587},
        "Keperawatan": {"mn": 547, "mx": 582},
        "Agroteknologi": {"mn": 542, "mx": 577},
        "Agribisnis": {"mn": 540, "mx": 575},
        "Kehutanan": {"mn": 536, "mx": 571},
        "Ilmu Tanah": {"mn": 532, "mx": 567},
        "Teknologi Pangan": {"mn": 530, "mx": 565},
        "Peternakan": {"mn": 526, "mx": 561},
        "Ilmu Kelautan": {"mn": 522, "mx": 557},
        "Psikologi": {"mn": 617, "mx": 652},
        "Hukum": {"mn": 609, "mx": 644},
        "Akuntansi": {"mn": 605, "mx": 640},
        "Manajemen": {"mn": 600, "mx": 635},
        "Ilmu Komunikasi": {"mn": 597, "mx": 632},
        "Ekonomi Pembangunan": {"mn": 592, "mx": 627},
        "Hubungan Internasional": {"mn": 589, "mx": 624},
        "Ilmu Administrasi Bisnis": {"mn": 585, "mx": 620},
        "Ilmu Politik": {"mn": 581, "mx": 616},
        "Sosiologi": {"mn": 576, "mx": 611},
        "Ilmu Kesejahteraan Sosial": {"mn": 571, "mx": 606},
        "Kriminologi": {"mn": 570, "mx": 605},
        "Ilmu Pemerintahan": {"mn": 568, "mx": 603},
        "Antropologi Sosial": {"mn": 563, "mx": 598},
        "Ilmu Sejarah": {"mn": 558, "mx": 593},
        "Sastra Inggris": {"mn": 555, "mx": 590},
        "Sastra Indonesia": {"mn": 550, "mx": 585},
        "Pendidikan Bahasa Inggris": {"mn": 547, "mx": 582},
        "Pendidikan Ekonomi": {"mn": 544, "mx": 579},
        "Pendidikan Sejarah": {"mn": 541, "mx": 576},
        "Pendidikan Sosiologi": {"mn": 538, "mx": 573},
        "Perpustakaan dan Ilmu Informasi": {"mn": 536, "mx": 571},
        "Keuangan dan Perbankan": {"mn": 534, "mx": 569},
        "Bisnis Internasional": {"mn": 532, "mx": 567},
        "Pariwisata": {"mn": 526, "mx": 561},
        "Administrasi Negara": {"mn": 524, "mx": 559},
        "Pendidikan Pancasila dan Kewarganegaraan": {"mn": 521, "mx": 556},
        "Sastra Arab": {"mn": 514, "mx": 549},
        "Sastra Jawa": {"mn": 506, "mx": 541},
        "Filsafat": {"mn": 502, "mx": 537},
        "_default": {"mn": 564, "mx": 599},
        "_klaster": 3, "_lbl": "🔹 Klaster 3 — Menengah"
    },
    "Universitas Andalas": {
        "Pendidikan Dokter (Kedokteran)": {"mn": 649, "mx": 684},
        "Teknik Informatika": {"mn": 641, "mx": 676},
        "Farmasi": {"mn": 629, "mx": 664},
        "Teknik Elektro": {"mn": 625, "mx": 660},
        "Ilmu Komputer": {"mn": 621, "mx": 656},
        "Teknik Kimia": {"mn": 617, "mx": 652},
        "Teknik Mesin": {"mn": 613, "mx": 648},
        "Teknik Sipil": {"mn": 609, "mx": 644},
        "Kedokteran Gigi": {"mn": 607, "mx": 642},
        "Bioteknologi": {"mn": 601, "mx": 636},
        "Teknik Industri": {"mn": 599, "mx": 634},
        "Statistika": {"mn": 594, "mx": 629},
        "Matematika": {"mn": 591, "mx": 626},
        "Fisika": {"mn": 586, "mx": 621},
        "Kimia": {"mn": 583, "mx": 618},
        "Biologi": {"mn": 580, "mx": 615},
        "Teknik Lingkungan": {"mn": 576, "mx": 611},
        "Teknik Geologi": {"mn": 575, "mx": 610},
        "Teknik Perminyakan": {"mn": 572, "mx": 607},
        "Arsitektur": {"mn": 571, "mx": 606},
        "Perencanaan Wilayah dan Kota": {"mn": 568, "mx": 603},
        "Ilmu Gizi": {"mn": 567, "mx": 602},
        "Keperawatan": {"mn": 562, "mx": 597},
        "Agroteknologi": {"mn": 556, "mx": 591},
        "Agribisnis": {"mn": 554, "mx": 589},
        "Kehutanan": {"mn": 550, "mx": 585},
        "Ilmu Tanah": {"mn": 546, "mx": 581},
        "Teknologi Pangan": {"mn": 544, "mx": 579},
        "Peternakan": {"mn": 540, "mx": 575},
        "Ilmu Kelautan": {"mn": 536, "mx": 571},
        "Psikologi": {"mn": 633, "mx": 668},
        "Hukum": {"mn": 625, "mx": 660},
        "Akuntansi": {"mn": 621, "mx": 656},
        "Manajemen": {"mn": 615, "mx": 650},
        "Ilmu Komunikasi": {"mn": 613, "mx": 648},
        "Ekonomi Pembangunan": {"mn": 607, "mx": 642},
        "Hubungan Internasional": {"mn": 605, "mx": 640},
        "Ilmu Administrasi Bisnis": {"mn": 601, "mx": 636},
        "Ilmu Politik": {"mn": 597, "mx": 632},
        "Sosiologi": {"mn": 591, "mx": 626},
        "Ilmu Kesejahteraan Sosial": {"mn": 586, "mx": 621},
        "Kriminologi": {"mn": 584, "mx": 619},
        "Ilmu Pemerintahan": {"mn": 583, "mx": 618},
        "Antropologi Sosial": {"mn": 578, "mx": 613},
        "Ilmu Sejarah": {"mn": 572, "mx": 607},
        "Sastra Inggris": {"mn": 570, "mx": 605},
        "Sastra Indonesia": {"mn": 564, "mx": 599},
        "Pendidikan Bahasa Inggris": {"mn": 562, "mx": 597},
        "Pendidikan Ekonomi": {"mn": 558, "mx": 593},
        "Pendidikan Sejarah": {"mn": 555, "mx": 590},
        "Pendidikan Sosiologi": {"mn": 552, "mx": 587},
        "Perpustakaan dan Ilmu Informasi": {"mn": 550, "mx": 585},
        "Keuangan dan Perbankan": {"mn": 548, "mx": 583},
        "Bisnis Internasional": {"mn": 546, "mx": 581},
        "Pariwisata": {"mn": 540, "mx": 575},
        "Administrasi Negara": {"mn": 537, "mx": 572},
        "Pendidikan Pancasila dan Kewarganegaraan": {"mn": 534, "mx": 569},
        "Sastra Arab": {"mn": 528, "mx": 563},
        "Sastra Jawa": {"mn": 520, "mx": 555},
        "Filsafat": {"mn": 516, "mx": 551},
        "_default": {"mn": 579, "mx": 614},
        "_klaster": 3, "_lbl": "🔹 Klaster 3 — Menengah"
    },
    "Universitas Negeri Semarang": {
        "Pendidikan Dokter (Kedokteran)": {"mn": 641, "mx": 676},
        "Teknik Informatika": {"mn": 633, "mx": 668},
        "Farmasi": {"mn": 621, "mx": 656},
        "Teknik Elektro": {"mn": 617, "mx": 652},
        "Ilmu Komputer": {"mn": 613, "mx": 648},
        "Teknik Kimia": {"mn": 609, "mx": 644},
        "Teknik Mesin": {"mn": 605, "mx": 640},
        "Teknik Sipil": {"mn": 601, "mx": 636},
        "Kedokteran Gigi": {"mn": 599, "mx": 634},
        "Bioteknologi": {"mn": 593, "mx": 628},
        "Teknik Industri": {"mn": 591, "mx": 626},
        "Statistika": {"mn": 587, "mx": 622},
        "Matematika": {"mn": 583, "mx": 618},
        "Fisika": {"mn": 579, "mx": 614},
        "Kimia": {"mn": 575, "mx": 610},
        "Biologi": {"mn": 573, "mx": 608},
        "Teknik Lingkungan": {"mn": 569, "mx": 604},
        "Teknik Geologi": {"mn": 567, "mx": 602},
        "Teknik Perminyakan": {"mn": 565, "mx": 600},
        "Arsitektur": {"mn": 564, "mx": 599},
        "Perencanaan Wilayah dan Kota": {"mn": 561, "mx": 596},
        "Ilmu Gizi": {"mn": 559, "mx": 594},
        "Keperawatan": {"mn": 555, "mx": 590},
        "Agroteknologi": {"mn": 549, "mx": 584},
        "Agribisnis": {"mn": 547, "mx": 582},
        "Kehutanan": {"mn": 543, "mx": 578},
        "Ilmu Tanah": {"mn": 539, "mx": 574},
        "Teknologi Pangan": {"mn": 537, "mx": 572},
        "Peternakan": {"mn": 533, "mx": 568},
        "Ilmu Kelautan": {"mn": 529, "mx": 564},
        "Psikologi": {"mn": 625, "mx": 660},
        "Hukum": {"mn": 617, "mx": 652},
        "Akuntansi": {"mn": 613, "mx": 648},
        "Manajemen": {"mn": 607, "mx": 642},
        "Ilmu Komunikasi": {"mn": 605, "mx": 640},
        "Ekonomi Pembangunan": {"mn": 599, "mx": 634},
        "Hubungan Internasional": {"mn": 597, "mx": 632},
        "Ilmu Administrasi Bisnis": {"mn": 593, "mx": 628},
        "Ilmu Politik": {"mn": 589, "mx": 624},
        "Sosiologi": {"mn": 583, "mx": 618},
        "Ilmu Kesejahteraan Sosial": {"mn": 579, "mx": 614},
        "Kriminologi": {"mn": 577, "mx": 612},
        "Ilmu Pemerintahan": {"mn": 575, "mx": 610},
        "Antropologi Sosial": {"mn": 571, "mx": 606},
        "Ilmu Sejarah": {"mn": 565, "mx": 600},
        "Sastra Inggris": {"mn": 563, "mx": 598},
        "Sastra Indonesia": {"mn": 557, "mx": 592},
        "Pendidikan Bahasa Inggris": {"mn": 555, "mx": 590},
        "Pendidikan Ekonomi": {"mn": 551, "mx": 586},
        "Pendidikan Sejarah": {"mn": 548, "mx": 583},
        "Pendidikan Sosiologi": {"mn": 545, "mx": 580},
        "Perpustakaan dan Ilmu Informasi": {"mn": 543, "mx": 578},
        "Keuangan dan Perbankan": {"mn": 541, "mx": 576},
        "Bisnis Internasional": {"mn": 539, "mx": 574},
        "Pariwisata": {"mn": 533, "mx": 568},
        "Administrasi Negara": {"mn": 531, "mx": 566},
        "Pendidikan Pancasila dan Kewarganegaraan": {"mn": 527, "mx": 562},
        "Sastra Arab": {"mn": 521, "mx": 556},
        "Sastra Jawa": {"mn": 513, "mx": 548},
        "Filsafat": {"mn": 509, "mx": 544},
        "_default": {"mn": 572, "mx": 607},
        "_klaster": 3, "_lbl": "🔹 Klaster 3 — Menengah"
    },
    "Universitas Syiah Kuala": {
        "Pendidikan Dokter (Kedokteran)": {"mn": 633, "mx": 668},
        "Teknik Informatika": {"mn": 625, "mx": 660},
        "Farmasi": {"mn": 613, "mx": 648},
        "Teknik Elektro": {"mn": 609, "mx": 644},
        "Ilmu Komputer": {"mn": 605, "mx": 640},
        "Teknik Kimia": {"mn": 601, "mx": 636},
        "Teknik Mesin": {"mn": 597, "mx": 632},
        "Teknik Sipil": {"mn": 593, "mx": 628},
        "Kedokteran Gigi": {"mn": 592, "mx": 627},
        "Bioteknologi": {"mn": 585, "mx": 620},
        "Teknik Industri": {"mn": 584, "mx": 619},
        "Statistika": {"mn": 579, "mx": 614},
        "Matematika": {"mn": 576, "mx": 611},
        "Fisika": {"mn": 571, "mx": 606},
        "Kimia": {"mn": 568, "mx": 603},
        "Biologi": {"mn": 566, "mx": 601},
        "Teknik Lingkungan": {"mn": 562, "mx": 597},
        "Teknik Geologi": {"mn": 560, "mx": 595},
        "Teknik Perminyakan": {"mn": 558, "mx": 593},
        "Arsitektur": {"mn": 557, "mx": 592},
        "Perencanaan Wilayah dan Kota": {"mn": 554, "mx": 589},
        "Ilmu Gizi": {"mn": 552, "mx": 587},
        "Keperawatan": {"mn": 547, "mx": 582},
        "Agroteknologi": {"mn": 542, "mx": 577},
        "Agribisnis": {"mn": 540, "mx": 575},
        "Kehutanan": {"mn": 536, "mx": 571},
        "Ilmu Tanah": {"mn": 532, "mx": 567},
        "Teknologi Pangan": {"mn": 530, "mx": 565},
        "Peternakan": {"mn": 526, "mx": 561},
        "Ilmu Kelautan": {"mn": 522, "mx": 557},
        "Psikologi": {"mn": 617, "mx": 652},
        "Hukum": {"mn": 609, "mx": 644},
        "Akuntansi": {"mn": 605, "mx": 640},
        "Manajemen": {"mn": 600, "mx": 635},
        "Ilmu Komunikasi": {"mn": 597, "mx": 632},
        "Ekonomi Pembangunan": {"mn": 592, "mx": 627},
        "Hubungan Internasional": {"mn": 589, "mx": 624},
        "Ilmu Administrasi Bisnis": {"mn": 585, "mx": 620},
        "Ilmu Politik": {"mn": 581, "mx": 616},
        "Sosiologi": {"mn": 576, "mx": 611},
        "Ilmu Kesejahteraan Sosial": {"mn": 571, "mx": 606},
        "Kriminologi": {"mn": 570, "mx": 605},
        "Ilmu Pemerintahan": {"mn": 568, "mx": 603},
        "Antropologi Sosial": {"mn": 563, "mx": 598},
        "Ilmu Sejarah": {"mn": 558, "mx": 593},
        "Sastra Inggris": {"mn": 555, "mx": 590},
        "Sastra Indonesia": {"mn": 550, "mx": 585},
        "Pendidikan Bahasa Inggris": {"mn": 547, "mx": 582},
        "Pendidikan Ekonomi": {"mn": 544, "mx": 579},
        "Pendidikan Sejarah": {"mn": 541, "mx": 576},
        "Pendidikan Sosiologi": {"mn": 538, "mx": 573},
        "Perpustakaan dan Ilmu Informasi": {"mn": 536, "mx": 571},
        "Keuangan dan Perbankan": {"mn": 534, "mx": 569},
        "Bisnis Internasional": {"mn": 532, "mx": 567},
        "Pariwisata": {"mn": 526, "mx": 561},
        "Administrasi Negara": {"mn": 524, "mx": 559},
        "Pendidikan Pancasila dan Kewarganegaraan": {"mn": 521, "mx": 556},
        "Sastra Arab": {"mn": 514, "mx": 549},
        "Sastra Jawa": {"mn": 506, "mx": 541},
        "Filsafat": {"mn": 502, "mx": 537},
        "_default": {"mn": 564, "mx": 599},
        "_klaster": 3, "_lbl": "🔹 Klaster 3 — Menengah"
    },
    "Universitas Mulawarman": {
        "Pendidikan Dokter (Kedokteran)": {"mn": 616, "mx": 651},
        "Teknik Informatika": {"mn": 609, "mx": 644},
        "Farmasi": {"mn": 597, "mx": 632},
        "Teknik Elektro": {"mn": 593, "mx": 628},
        "Ilmu Komputer": {"mn": 589, "mx": 624},
        "Teknik Kimia": {"mn": 586, "mx": 621},
        "Teknik Mesin": {"mn": 582, "mx": 617},
        "Teknik Sipil": {"mn": 578, "mx": 613},
        "Kedokteran Gigi": {"mn": 576, "mx": 611},
        "Bioteknologi": {"mn": 570, "mx": 605},
        "Teknik Industri": {"mn": 569, "mx": 604},
        "Statistika": {"mn": 564, "mx": 599},
        "Matematika": {"mn": 561, "mx": 596},
        "Fisika": {"mn": 556, "mx": 591},
        "Kimia": {"mn": 553, "mx": 588},
        "Biologi": {"mn": 551, "mx": 586},
        "Teknik Lingkungan": {"mn": 547, "mx": 582},
        "Teknik Geologi": {"mn": 546, "mx": 581},
        "Teknik Perminyakan": {"mn": 543, "mx": 578},
        "Arsitektur": {"mn": 542, "mx": 577},
        "Perencanaan Wilayah dan Kota": {"mn": 539, "mx": 574},
        "Ilmu Gizi": {"mn": 538, "mx": 573},
        "Keperawatan": {"mn": 533, "mx": 568},
        "Agroteknologi": {"mn": 528, "mx": 563},
        "Agribisnis": {"mn": 526, "mx": 561},
        "Kehutanan": {"mn": 522, "mx": 557},
        "Ilmu Tanah": {"mn": 518, "mx": 553},
        "Teknologi Pangan": {"mn": 516, "mx": 551},
        "Peternakan": {"mn": 512, "mx": 547},
        "Ilmu Kelautan": {"mn": 509, "mx": 544},
        "Psikologi": {"mn": 601, "mx": 636},
        "Hukum": {"mn": 593, "mx": 628},
        "Akuntansi": {"mn": 589, "mx": 624},
        "Manajemen": {"mn": 584, "mx": 619},
        "Ilmu Komunikasi": {"mn": 582, "mx": 617},
        "Ekonomi Pembangunan": {"mn": 576, "mx": 611},
        "Hubungan Internasional": {"mn": 574, "mx": 609},
        "Ilmu Administrasi Bisnis": {"mn": 570, "mx": 605},
        "Ilmu Politik": {"mn": 566, "mx": 601},
        "Sosiologi": {"mn": 561, "mx": 596},
        "Ilmu Kesejahteraan Sosial": {"mn": 556, "mx": 591},
        "Kriminologi": {"mn": 555, "mx": 590},
        "Ilmu Pemerintahan": {"mn": 553, "mx": 588},
        "Antropologi Sosial": {"mn": 549, "mx": 584},
        "Ilmu Sejarah": {"mn": 543, "mx": 578},
        "Sastra Inggris": {"mn": 541, "mx": 576},
        "Sastra Indonesia": {"mn": 536, "mx": 571},
        "Pendidikan Bahasa Inggris": {"mn": 533, "mx": 568},
        "Pendidikan Ekonomi": {"mn": 530, "mx": 565},
        "Pendidikan Sejarah": {"mn": 527, "mx": 562},
        "Pendidikan Sosiologi": {"mn": 524, "mx": 559},
        "Perpustakaan dan Ilmu Informasi": {"mn": 522, "mx": 557},
        "Keuangan dan Perbankan": {"mn": 520, "mx": 555},
        "Bisnis Internasional": {"mn": 518, "mx": 553},
        "Pariwisata": {"mn": 512, "mx": 547},
        "Administrasi Negara": {"mn": 510, "mx": 545},
        "Pendidikan Pancasila dan Kewarganegaraan": {"mn": 507, "mx": 542},
        "Sastra Arab": {"mn": 501, "mx": 536},
        "Sastra Jawa": {"mn": 493, "mx": 528},
        "Filsafat": {"mn": 489, "mx": 524},
        "_default": {"mn": 550, "mx": 585},
        "_klaster": 3, "_lbl": "🔹 Klaster 3 — Menengah"
    },
    "Universitas Sriwijaya": {
        "Pendidikan Dokter (Kedokteran)": {"mn": 633, "mx": 668},
        "Teknik Informatika": {"mn": 625, "mx": 660},
        "Farmasi": {"mn": 613, "mx": 648},
        "Teknik Elektro": {"mn": 609, "mx": 644},
        "Ilmu Komputer": {"mn": 605, "mx": 640},
        "Teknik Kimia": {"mn": 601, "mx": 636},
        "Teknik Mesin": {"mn": 597, "mx": 632},
        "Teknik Sipil": {"mn": 593, "mx": 628},
        "Kedokteran Gigi": {"mn": 592, "mx": 627},
        "Bioteknologi": {"mn": 585, "mx": 620},
        "Teknik Industri": {"mn": 584, "mx": 619},
        "Statistika": {"mn": 579, "mx": 614},
        "Matematika": {"mn": 576, "mx": 611},
        "Fisika": {"mn": 571, "mx": 606},
        "Kimia": {"mn": 568, "mx": 603},
        "Biologi": {"mn": 566, "mx": 601},
        "Teknik Lingkungan": {"mn": 562, "mx": 597},
        "Teknik Geologi": {"mn": 560, "mx": 595},
        "Teknik Perminyakan": {"mn": 558, "mx": 593},
        "Arsitektur": {"mn": 557, "mx": 592},
        "Perencanaan Wilayah dan Kota": {"mn": 554, "mx": 589},
        "Ilmu Gizi": {"mn": 552, "mx": 587},
        "Keperawatan": {"mn": 547, "mx": 582},
        "Agroteknologi": {"mn": 542, "mx": 577},
        "Agribisnis": {"mn": 540, "mx": 575},
        "Kehutanan": {"mn": 536, "mx": 571},
        "Ilmu Tanah": {"mn": 532, "mx": 567},
        "Teknologi Pangan": {"mn": 530, "mx": 565},
        "Peternakan": {"mn": 526, "mx": 561},
        "Ilmu Kelautan": {"mn": 522, "mx": 557},
        "Psikologi": {"mn": 617, "mx": 652},
        "Hukum": {"mn": 609, "mx": 644},
        "Akuntansi": {"mn": 605, "mx": 640},
        "Manajemen": {"mn": 600, "mx": 635},
        "Ilmu Komunikasi": {"mn": 597, "mx": 632},
        "Ekonomi Pembangunan": {"mn": 592, "mx": 627},
        "Hubungan Internasional": {"mn": 589, "mx": 624},
        "Ilmu Administrasi Bisnis": {"mn": 585, "mx": 620},
        "Ilmu Politik": {"mn": 581, "mx": 616},
        "Sosiologi": {"mn": 576, "mx": 611},
        "Ilmu Kesejahteraan Sosial": {"mn": 571, "mx": 606},
        "Kriminologi": {"mn": 570, "mx": 605},
        "Ilmu Pemerintahan": {"mn": 568, "mx": 603},
        "Antropologi Sosial": {"mn": 563, "mx": 598},
        "Ilmu Sejarah": {"mn": 558, "mx": 593},
        "Sastra Inggris": {"mn": 555, "mx": 590},
        "Sastra Indonesia": {"mn": 550, "mx": 585},
        "Pendidikan Bahasa Inggris": {"mn": 547, "mx": 582},
        "Pendidikan Ekonomi": {"mn": 544, "mx": 579},
        "Pendidikan Sejarah": {"mn": 541, "mx": 576},
        "Pendidikan Sosiologi": {"mn": 538, "mx": 573},
        "Perpustakaan dan Ilmu Informasi": {"mn": 536, "mx": 571},
        "Keuangan dan Perbankan": {"mn": 534, "mx": 569},
        "Bisnis Internasional": {"mn": 532, "mx": 567},
        "Pariwisata": {"mn": 526, "mx": 561},
        "Administrasi Negara": {"mn": 524, "mx": 559},
        "Pendidikan Pancasila dan Kewarganegaraan": {"mn": 521, "mx": 556},
        "Sastra Arab": {"mn": 514, "mx": 549},
        "Sastra Jawa": {"mn": 506, "mx": 541},
        "Filsafat": {"mn": 502, "mx": 537},
        "_default": {"mn": 564, "mx": 599},
        "_klaster": 3, "_lbl": "🔹 Klaster 3 — Menengah"
    },
    "Universitas Udayana": {
        "Pendidikan Dokter (Kedokteran)": {"mn": 666, "mx": 701},
        "Teknik Informatika": {"mn": 657, "mx": 692},
        "Farmasi": {"mn": 645, "mx": 680},
        "Teknik Elektro": {"mn": 641, "mx": 676},
        "Ilmu Komputer": {"mn": 637, "mx": 672},
        "Teknik Kimia": {"mn": 632, "mx": 667},
        "Teknik Mesin": {"mn": 628, "mx": 663},
        "Teknik Sipil": {"mn": 624, "mx": 659},
        "Kedokteran Gigi": {"mn": 622, "mx": 657},
        "Bioteknologi": {"mn": 616, "mx": 651},
        "Teknik Industri": {"mn": 614, "mx": 649},
        "Statistika": {"mn": 609, "mx": 644},
        "Matematika": {"mn": 606, "mx": 641},
        "Fisika": {"mn": 601, "mx": 636},
        "Kimia": {"mn": 598, "mx": 633},
        "Biologi": {"mn": 595, "mx": 630},
        "Teknik Lingkungan": {"mn": 591, "mx": 626},
        "Teknik Geologi": {"mn": 589, "mx": 624},
        "Teknik Perminyakan": {"mn": 587, "mx": 622},
        "Arsitektur": {"mn": 586, "mx": 621},
        "Perencanaan Wilayah dan Kota": {"mn": 583, "mx": 618},
        "Ilmu Gizi": {"mn": 581, "mx": 616},
        "Keperawatan": {"mn": 576, "mx": 611},
        "Agroteknologi": {"mn": 570, "mx": 605},
        "Agribisnis": {"mn": 568, "mx": 603},
        "Kehutanan": {"mn": 564, "mx": 599},
        "Ilmu Tanah": {"mn": 559, "mx": 594},
        "Teknologi Pangan": {"mn": 558, "mx": 593},
        "Peternakan": {"mn": 554, "mx": 589},
        "Ilmu Kelautan": {"mn": 549, "mx": 584},
        "Psikologi": {"mn": 649, "mx": 684},
        "Hukum": {"mn": 641, "mx": 676},
        "Akuntansi": {"mn": 637, "mx": 672},
        "Manajemen": {"mn": 631, "mx": 666},
        "Ilmu Komunikasi": {"mn": 628, "mx": 663},
        "Ekonomi Pembangunan": {"mn": 622, "mx": 657},
        "Hubungan Internasional": {"mn": 620, "mx": 655},
        "Ilmu Administrasi Bisnis": {"mn": 616, "mx": 651},
        "Ilmu Politik": {"mn": 612, "mx": 647},
        "Sosiologi": {"mn": 606, "mx": 641},
        "Ilmu Kesejahteraan Sosial": {"mn": 601, "mx": 636},
        "Kriminologi": {"mn": 599, "mx": 634},
        "Ilmu Pemerintahan": {"mn": 598, "mx": 633},
        "Antropologi Sosial": {"mn": 593, "mx": 628},
        "Ilmu Sejarah": {"mn": 587, "mx": 622},
        "Sastra Inggris": {"mn": 584, "mx": 619},
        "Sastra Indonesia": {"mn": 578, "mx": 613},
        "Pendidikan Bahasa Inggris": {"mn": 576, "mx": 611},
        "Pendidikan Ekonomi": {"mn": 573, "mx": 608},
        "Pendidikan Sejarah": {"mn": 569, "mx": 604},
        "Pendidikan Sosiologi": {"mn": 566, "mx": 601},
        "Perpustakaan dan Ilmu Informasi": {"mn": 564, "mx": 599},
        "Keuangan dan Perbankan": {"mn": 562, "mx": 597},
        "Bisnis Internasional": {"mn": 559, "mx": 594},
        "Pariwisata": {"mn": 554, "mx": 589},
        "Administrasi Negara": {"mn": 551, "mx": 586},
        "Pendidikan Pancasila dan Kewarganegaraan": {"mn": 548, "mx": 583},
        "Sastra Arab": {"mn": 541, "mx": 576},
        "Sastra Jawa": {"mn": 533, "mx": 568},
        "Filsafat": {"mn": 529, "mx": 564},
        "_default": {"mn": 594, "mx": 629},
        "_klaster": 3, "_lbl": "🔹 Klaster 3 — Menengah"
    },
    "Universitas Sam Ratulangi": {
        "Pendidikan Dokter (Kedokteran)": {"mn": 616, "mx": 651},
        "Teknik Informatika": {"mn": 609, "mx": 644},
        "Farmasi": {"mn": 597, "mx": 632},
        "Teknik Elektro": {"mn": 593, "mx": 628},
        "Ilmu Komputer": {"mn": 589, "mx": 624},
        "Teknik Kimia": {"mn": 586, "mx": 621},
        "Teknik Mesin": {"mn": 582, "mx": 617},
        "Teknik Sipil": {"mn": 578, "mx": 613},
        "Kedokteran Gigi": {"mn": 576, "mx": 611},
        "Bioteknologi": {"mn": 570, "mx": 605},
        "Teknik Industri": {"mn": 569, "mx": 604},
        "Statistika": {"mn": 564, "mx": 599},
        "Matematika": {"mn": 561, "mx": 596},
        "Fisika": {"mn": 556, "mx": 591},
        "Kimia": {"mn": 553, "mx": 588},
        "Biologi": {"mn": 551, "mx": 586},
        "Teknik Lingkungan": {"mn": 547, "mx": 582},
        "Teknik Geologi": {"mn": 546, "mx": 581},
        "Teknik Perminyakan": {"mn": 543, "mx": 578},
        "Arsitektur": {"mn": 542, "mx": 577},
        "Perencanaan Wilayah dan Kota": {"mn": 539, "mx": 574},
        "Ilmu Gizi": {"mn": 538, "mx": 573},
        "Keperawatan": {"mn": 533, "mx": 568},
        "Agroteknologi": {"mn": 528, "mx": 563},
        "Agribisnis": {"mn": 526, "mx": 561},
        "Kehutanan": {"mn": 522, "mx": 557},
        "Ilmu Tanah": {"mn": 518, "mx": 553},
        "Teknologi Pangan": {"mn": 516, "mx": 551},
        "Peternakan": {"mn": 512, "mx": 547},
        "Ilmu Kelautan": {"mn": 509, "mx": 544},
        "Psikologi": {"mn": 601, "mx": 636},
        "Hukum": {"mn": 593, "mx": 628},
        "Akuntansi": {"mn": 589, "mx": 624},
        "Manajemen": {"mn": 584, "mx": 619},
        "Ilmu Komunikasi": {"mn": 582, "mx": 617},
        "Ekonomi Pembangunan": {"mn": 576, "mx": 611},
        "Hubungan Internasional": {"mn": 574, "mx": 609},
        "Ilmu Administrasi Bisnis": {"mn": 570, "mx": 605},
        "Ilmu Politik": {"mn": 566, "mx": 601},
        "Sosiologi": {"mn": 561, "mx": 596},
        "Ilmu Kesejahteraan Sosial": {"mn": 556, "mx": 591},
        "Kriminologi": {"mn": 555, "mx": 590},
        "Ilmu Pemerintahan": {"mn": 553, "mx": 588},
        "Antropologi Sosial": {"mn": 549, "mx": 584},
        "Ilmu Sejarah": {"mn": 543, "mx": 578},
        "Sastra Inggris": {"mn": 541, "mx": 576},
        "Sastra Indonesia": {"mn": 536, "mx": 571},
        "Pendidikan Bahasa Inggris": {"mn": 533, "mx": 568},
        "Pendidikan Ekonomi": {"mn": 530, "mx": 565},
        "Pendidikan Sejarah": {"mn": 527, "mx": 562},
        "Pendidikan Sosiologi": {"mn": 524, "mx": 559},
        "Perpustakaan dan Ilmu Informasi": {"mn": 522, "mx": 557},
        "Keuangan dan Perbankan": {"mn": 520, "mx": 555},
        "Bisnis Internasional": {"mn": 518, "mx": 553},
        "Pariwisata": {"mn": 512, "mx": 547},
        "Administrasi Negara": {"mn": 510, "mx": 545},
        "Pendidikan Pancasila dan Kewarganegaraan": {"mn": 507, "mx": 542},
        "Sastra Arab": {"mn": 501, "mx": 536},
        "Sastra Jawa": {"mn": 493, "mx": 528},
        "Filsafat": {"mn": 489, "mx": 524},
        "_default": {"mn": 550, "mx": 585},
        "_klaster": 4, "_lbl": "🔸 Klaster 4 — Regional"
    },
    "Universitas Riau": {
        "Pendidikan Dokter (Kedokteran)": {"mn": 625, "mx": 660},
        "Teknik Informatika": {"mn": 617, "mx": 652},
        "Farmasi": {"mn": 605, "mx": 640},
        "Teknik Elektro": {"mn": 601, "mx": 636},
        "Ilmu Komputer": {"mn": 597, "mx": 632},
        "Teknik Kimia": {"mn": 593, "mx": 628},
        "Teknik Mesin": {"mn": 589, "mx": 624},
        "Teknik Sipil": {"mn": 586, "mx": 621},
        "Kedokteran Gigi": {"mn": 584, "mx": 619},
        "Bioteknologi": {"mn": 578, "mx": 613},
        "Teknik Industri": {"mn": 576, "mx": 611},
        "Statistika": {"mn": 572, "mx": 607},
        "Matematika": {"mn": 568, "mx": 603},
        "Fisika": {"mn": 564, "mx": 599},
        "Kimia": {"mn": 561, "mx": 596},
        "Biologi": {"mn": 558, "mx": 593},
        "Teknik Lingkungan": {"mn": 554, "mx": 589},
        "Teknik Geologi": {"mn": 553, "mx": 588},
        "Teknik Perminyakan": {"mn": 551, "mx": 586},
        "Arsitektur": {"mn": 550, "mx": 585},
        "Perencanaan Wilayah dan Kota": {"mn": 547, "mx": 582},
        "Ilmu Gizi": {"mn": 545, "mx": 580},
        "Keperawatan": {"mn": 540, "mx": 575},
        "Agroteknologi": {"mn": 535, "mx": 570},
        "Agribisnis": {"mn": 533, "mx": 568},
        "Kehutanan": {"mn": 529, "mx": 564},
        "Ilmu Tanah": {"mn": 525, "mx": 560},
        "Teknologi Pangan": {"mn": 523, "mx": 558},
        "Peternakan": {"mn": 519, "mx": 554},
        "Ilmu Kelautan": {"mn": 515, "mx": 550},
        "Psikologi": {"mn": 609, "mx": 644},
        "Hukum": {"mn": 601, "mx": 636},
        "Akuntansi": {"mn": 597, "mx": 632},
        "Manajemen": {"mn": 592, "mx": 627},
        "Ilmu Komunikasi": {"mn": 589, "mx": 624},
        "Ekonomi Pembangunan": {"mn": 584, "mx": 619},
        "Hubungan Internasional": {"mn": 582, "mx": 617},
        "Ilmu Administrasi Bisnis": {"mn": 578, "mx": 613},
        "Ilmu Politik": {"mn": 574, "mx": 609},
        "Sosiologi": {"mn": 568, "mx": 603},
        "Ilmu Kesejahteraan Sosial": {"mn": 564, "mx": 599},
        "Kriminologi": {"mn": 562, "mx": 597},
        "Ilmu Pemerintahan": {"mn": 561, "mx": 596},
        "Antropologi Sosial": {"mn": 556, "mx": 591},
        "Ilmu Sejarah": {"mn": 551, "mx": 586},
        "Sastra Inggris": {"mn": 548, "mx": 583},
        "Sastra Indonesia": {"mn": 543, "mx": 578},
        "Pendidikan Bahasa Inggris": {"mn": 540, "mx": 575},
        "Pendidikan Ekonomi": {"mn": 537, "mx": 572},
        "Pendidikan Sejarah": {"mn": 534, "mx": 569},
        "Pendidikan Sosiologi": {"mn": 531, "mx": 566},
        "Perpustakaan dan Ilmu Informasi": {"mn": 529, "mx": 564},
        "Keuangan dan Perbankan": {"mn": 527, "mx": 562},
        "Bisnis Internasional": {"mn": 525, "mx": 560},
        "Pariwisata": {"mn": 519, "mx": 554},
        "Administrasi Negara": {"mn": 517, "mx": 552},
        "Pendidikan Pancasila dan Kewarganegaraan": {"mn": 514, "mx": 549},
        "Sastra Arab": {"mn": 508, "mx": 543},
        "Sastra Jawa": {"mn": 500, "mx": 535},
        "Filsafat": {"mn": 496, "mx": 531},
        "_default": {"mn": 557, "mx": 592},
        "_klaster": 4, "_lbl": "🔸 Klaster 4 — Regional"
    },
    "Universitas Jember": {
        "Pendidikan Dokter (Kedokteran)": {"mn": 641, "mx": 676},
        "Teknik Informatika": {"mn": 633, "mx": 668},
        "Farmasi": {"mn": 621, "mx": 656},
        "Teknik Elektro": {"mn": 617, "mx": 652},
        "Ilmu Komputer": {"mn": 613, "mx": 648},
        "Teknik Kimia": {"mn": 609, "mx": 644},
        "Teknik Mesin": {"mn": 605, "mx": 640},
        "Teknik Sipil": {"mn": 601, "mx": 636},
        "Kedokteran Gigi": {"mn": 599, "mx": 634},
        "Bioteknologi": {"mn": 593, "mx": 628},
        "Teknik Industri": {"mn": 591, "mx": 626},
        "Statistika": {"mn": 587, "mx": 622},
        "Matematika": {"mn": 583, "mx": 618},
        "Fisika": {"mn": 579, "mx": 614},
        "Kimia": {"mn": 575, "mx": 610},
        "Biologi": {"mn": 573, "mx": 608},
        "Teknik Lingkungan": {"mn": 569, "mx": 604},
        "Teknik Geologi": {"mn": 567, "mx": 602},
        "Teknik Perminyakan": {"mn": 565, "mx": 600},
        "Arsitektur": {"mn": 564, "mx": 599},
        "Perencanaan Wilayah dan Kota": {"mn": 561, "mx": 596},
        "Ilmu Gizi": {"mn": 559, "mx": 594},
        "Keperawatan": {"mn": 555, "mx": 590},
        "Agroteknologi": {"mn": 549, "mx": 584},
        "Agribisnis": {"mn": 547, "mx": 582},
        "Kehutanan": {"mn": 543, "mx": 578},
        "Ilmu Tanah": {"mn": 539, "mx": 574},
        "Teknologi Pangan": {"mn": 537, "mx": 572},
        "Peternakan": {"mn": 533, "mx": 568},
        "Ilmu Kelautan": {"mn": 529, "mx": 564},
        "Psikologi": {"mn": 625, "mx": 660},
        "Hukum": {"mn": 617, "mx": 652},
        "Akuntansi": {"mn": 613, "mx": 648},
        "Manajemen": {"mn": 607, "mx": 642},
        "Ilmu Komunikasi": {"mn": 605, "mx": 640},
        "Ekonomi Pembangunan": {"mn": 599, "mx": 634},
        "Hubungan Internasional": {"mn": 597, "mx": 632},
        "Ilmu Administrasi Bisnis": {"mn": 593, "mx": 628},
        "Ilmu Politik": {"mn": 589, "mx": 624},
        "Sosiologi": {"mn": 583, "mx": 618},
        "Ilmu Kesejahteraan Sosial": {"mn": 579, "mx": 614},
        "Kriminologi": {"mn": 577, "mx": 612},
        "Ilmu Pemerintahan": {"mn": 575, "mx": 610},
        "Antropologi Sosial": {"mn": 571, "mx": 606},
        "Ilmu Sejarah": {"mn": 565, "mx": 600},
        "Sastra Inggris": {"mn": 563, "mx": 598},
        "Sastra Indonesia": {"mn": 557, "mx": 592},
        "Pendidikan Bahasa Inggris": {"mn": 555, "mx": 590},
        "Pendidikan Ekonomi": {"mn": 551, "mx": 586},
        "Pendidikan Sejarah": {"mn": 548, "mx": 583},
        "Pendidikan Sosiologi": {"mn": 545, "mx": 580},
        "Perpustakaan dan Ilmu Informasi": {"mn": 543, "mx": 578},
        "Keuangan dan Perbankan": {"mn": 541, "mx": 576},
        "Bisnis Internasional": {"mn": 539, "mx": 574},
        "Pariwisata": {"mn": 533, "mx": 568},
        "Administrasi Negara": {"mn": 531, "mx": 566},
        "Pendidikan Pancasila dan Kewarganegaraan": {"mn": 527, "mx": 562},
        "Sastra Arab": {"mn": 521, "mx": 556},
        "Sastra Jawa": {"mn": 513, "mx": 548},
        "Filsafat": {"mn": 509, "mx": 544},
        "_default": {"mn": 572, "mx": 607},
        "_klaster": 4, "_lbl": "🔸 Klaster 4 — Regional"
    },
    "Telkom University": {
        "Pendidikan Dokter (Kedokteran)": {"mn": 633, "mx": 668},
        "Teknik Informatika": {"mn": 625, "mx": 660},
        "Farmasi": {"mn": 613, "mx": 648},
        "Teknik Elektro": {"mn": 609, "mx": 644},
        "Ilmu Komputer": {"mn": 605, "mx": 640},
        "Teknik Kimia": {"mn": 601, "mx": 636},
        "Teknik Mesin": {"mn": 597, "mx": 632},
        "Teknik Sipil": {"mn": 593, "mx": 628},
        "Kedokteran Gigi": {"mn": 592, "mx": 627},
        "Bioteknologi": {"mn": 585, "mx": 620},
        "Teknik Industri": {"mn": 584, "mx": 619},
        "Statistika": {"mn": 579, "mx": 614},
        "Matematika": {"mn": 576, "mx": 611},
        "Fisika": {"mn": 571, "mx": 606},
        "Kimia": {"mn": 568, "mx": 603},
        "Biologi": {"mn": 566, "mx": 601},
        "Teknik Lingkungan": {"mn": 562, "mx": 597},
        "Teknik Geologi": {"mn": 560, "mx": 595},
        "Teknik Perminyakan": {"mn": 558, "mx": 593},
        "Arsitektur": {"mn": 557, "mx": 592},
        "Perencanaan Wilayah dan Kota": {"mn": 554, "mx": 589},
        "Ilmu Gizi": {"mn": 552, "mx": 587},
        "Keperawatan": {"mn": 547, "mx": 582},
        "Agroteknologi": {"mn": 542, "mx": 577},
        "Agribisnis": {"mn": 540, "mx": 575},
        "Kehutanan": {"mn": 536, "mx": 571},
        "Ilmu Tanah": {"mn": 532, "mx": 567},
        "Teknologi Pangan": {"mn": 530, "mx": 565},
        "Peternakan": {"mn": 526, "mx": 561},
        "Ilmu Kelautan": {"mn": 522, "mx": 557},
        "Psikologi": {"mn": 617, "mx": 652},
        "Hukum": {"mn": 609, "mx": 644},
        "Akuntansi": {"mn": 605, "mx": 640},
        "Manajemen": {"mn": 600, "mx": 635},
        "Ilmu Komunikasi": {"mn": 597, "mx": 632},
        "Ekonomi Pembangunan": {"mn": 592, "mx": 627},
        "Hubungan Internasional": {"mn": 589, "mx": 624},
        "Ilmu Administrasi Bisnis": {"mn": 585, "mx": 620},
        "Ilmu Politik": {"mn": 581, "mx": 616},
        "Sosiologi": {"mn": 576, "mx": 611},
        "Ilmu Kesejahteraan Sosial": {"mn": 571, "mx": 606},
        "Kriminologi": {"mn": 570, "mx": 605},
        "Ilmu Pemerintahan": {"mn": 568, "mx": 603},
        "Antropologi Sosial": {"mn": 563, "mx": 598},
        "Ilmu Sejarah": {"mn": 558, "mx": 593},
        "Sastra Inggris": {"mn": 555, "mx": 590},
        "Sastra Indonesia": {"mn": 550, "mx": 585},
        "Pendidikan Bahasa Inggris": {"mn": 547, "mx": 582},
        "Pendidikan Ekonomi": {"mn": 544, "mx": 579},
        "Pendidikan Sejarah": {"mn": 541, "mx": 576},
        "Pendidikan Sosiologi": {"mn": 538, "mx": 573},
        "Perpustakaan dan Ilmu Informasi": {"mn": 536, "mx": 571},
        "Keuangan dan Perbankan": {"mn": 534, "mx": 569},
        "Bisnis Internasional": {"mn": 532, "mx": 567},
        "Pariwisata": {"mn": 526, "mx": 561},
        "Administrasi Negara": {"mn": 524, "mx": 559},
        "Pendidikan Pancasila dan Kewarganegaraan": {"mn": 521, "mx": 556},
        "Sastra Arab": {"mn": 514, "mx": 549},
        "Sastra Jawa": {"mn": 506, "mx": 541},
        "Filsafat": {"mn": 502, "mx": 537},
        "_default": {"mn": 564, "mx": 599},
        "_klaster": 4, "_lbl": "🔸 Klaster 4 — Regional"
    },
    "Universitas Islam Indonesia": {
        "Pendidikan Dokter (Kedokteran)": {"mn": 625, "mx": 660},
        "Teknik Informatika": {"mn": 617, "mx": 652},
        "Farmasi": {"mn": 605, "mx": 640},
        "Teknik Elektro": {"mn": 601, "mx": 636},
        "Ilmu Komputer": {"mn": 597, "mx": 632},
        "Teknik Kimia": {"mn": 593, "mx": 628},
        "Teknik Mesin": {"mn": 589, "mx": 624},
        "Teknik Sipil": {"mn": 586, "mx": 621},
        "Kedokteran Gigi": {"mn": 584, "mx": 619},
        "Bioteknologi": {"mn": 578, "mx": 613},
        "Teknik Industri": {"mn": 576, "mx": 611},
        "Statistika": {"mn": 572, "mx": 607},
        "Matematika": {"mn": 568, "mx": 603},
        "Fisika": {"mn": 564, "mx": 599},
        "Kimia": {"mn": 561, "mx": 596},
        "Biologi": {"mn": 558, "mx": 593},
        "Teknik Lingkungan": {"mn": 554, "mx": 589},
        "Teknik Geologi": {"mn": 553, "mx": 588},
        "Teknik Perminyakan": {"mn": 551, "mx": 586},
        "Arsitektur": {"mn": 550, "mx": 585},
        "Perencanaan Wilayah dan Kota": {"mn": 547, "mx": 582},
        "Ilmu Gizi": {"mn": 545, "mx": 580},
        "Keperawatan": {"mn": 540, "mx": 575},
        "Agroteknologi": {"mn": 535, "mx": 570},
        "Agribisnis": {"mn": 533, "mx": 568},
        "Kehutanan": {"mn": 529, "mx": 564},
        "Ilmu Tanah": {"mn": 525, "mx": 560},
        "Teknologi Pangan": {"mn": 523, "mx": 558},
        "Peternakan": {"mn": 519, "mx": 554},
        "Ilmu Kelautan": {"mn": 515, "mx": 550},
        "Psikologi": {"mn": 609, "mx": 644},
        "Hukum": {"mn": 601, "mx": 636},
        "Akuntansi": {"mn": 597, "mx": 632},
        "Manajemen": {"mn": 592, "mx": 627},
        "Ilmu Komunikasi": {"mn": 589, "mx": 624},
        "Ekonomi Pembangunan": {"mn": 584, "mx": 619},
        "Hubungan Internasional": {"mn": 582, "mx": 617},
        "Ilmu Administrasi Bisnis": {"mn": 578, "mx": 613},
        "Ilmu Politik": {"mn": 574, "mx": 609},
        "Sosiologi": {"mn": 568, "mx": 603},
        "Ilmu Kesejahteraan Sosial": {"mn": 564, "mx": 599},
        "Kriminologi": {"mn": 562, "mx": 597},
        "Ilmu Pemerintahan": {"mn": 561, "mx": 596},
        "Antropologi Sosial": {"mn": 556, "mx": 591},
        "Ilmu Sejarah": {"mn": 551, "mx": 586},
        "Sastra Inggris": {"mn": 548, "mx": 583},
        "Sastra Indonesia": {"mn": 543, "mx": 578},
        "Pendidikan Bahasa Inggris": {"mn": 540, "mx": 575},
        "Pendidikan Ekonomi": {"mn": 537, "mx": 572},
        "Pendidikan Sejarah": {"mn": 534, "mx": 569},
        "Pendidikan Sosiologi": {"mn": 531, "mx": 566},
        "Perpustakaan dan Ilmu Informasi": {"mn": 529, "mx": 564},
        "Keuangan dan Perbankan": {"mn": 527, "mx": 562},
        "Bisnis Internasional": {"mn": 525, "mx": 560},
        "Pariwisata": {"mn": 519, "mx": 554},
        "Administrasi Negara": {"mn": 517, "mx": 552},
        "Pendidikan Pancasila dan Kewarganegaraan": {"mn": 514, "mx": 549},
        "Sastra Arab": {"mn": 508, "mx": 543},
        "Sastra Jawa": {"mn": 500, "mx": 535},
        "Filsafat": {"mn": 496, "mx": 531},
        "_default": {"mn": 557, "mx": 592},
        "_klaster": 4, "_lbl": "🔸 Klaster 4 — Regional"
    },
    "Universitas Muhammadiyah Yogyakarta": {
        "Pendidikan Dokter (Kedokteran)": {"mn": 608, "mx": 643},
        "Teknik Informatika": {"mn": 601, "mx": 636},
        "Farmasi": {"mn": 589, "mx": 624},
        "Teknik Elektro": {"mn": 585, "mx": 620},
        "Ilmu Komputer": {"mn": 582, "mx": 617},
        "Teknik Kimia": {"mn": 578, "mx": 613},
        "Teknik Mesin": {"mn": 574, "mx": 609},
        "Teknik Sipil": {"mn": 570, "mx": 605},
        "Kedokteran Gigi": {"mn": 569, "mx": 604},
        "Bioteknologi": {"mn": 563, "mx": 598},
        "Teknik Industri": {"mn": 561, "mx": 596},
        "Statistika": {"mn": 557, "mx": 592},
        "Matematika": {"mn": 553, "mx": 588},
        "Fisika": {"mn": 549, "mx": 584},
        "Kimia": {"mn": 546, "mx": 581},
        "Biologi": {"mn": 544, "mx": 579},
        "Teknik Lingkungan": {"mn": 540, "mx": 575},
        "Teknik Geologi": {"mn": 538, "mx": 573},
        "Teknik Perminyakan": {"mn": 536, "mx": 571},
        "Arsitektur": {"mn": 535, "mx": 570},
        "Perencanaan Wilayah dan Kota": {"mn": 532, "mx": 567},
        "Ilmu Gizi": {"mn": 531, "mx": 566},
        "Keperawatan": {"mn": 526, "mx": 561},
        "Agroteknologi": {"mn": 521, "mx": 556},
        "Agribisnis": {"mn": 519, "mx": 554},
        "Kehutanan": {"mn": 515, "mx": 550},
        "Ilmu Tanah": {"mn": 511, "mx": 546},
        "Teknologi Pangan": {"mn": 509, "mx": 544},
        "Peternakan": {"mn": 506, "mx": 541},
        "Ilmu Kelautan": {"mn": 502, "mx": 537},
        "Psikologi": {"mn": 593, "mx": 628},
        "Hukum": {"mn": 585, "mx": 620},
        "Akuntansi": {"mn": 582, "mx": 617},
        "Manajemen": {"mn": 576, "mx": 611},
        "Ilmu Komunikasi": {"mn": 574, "mx": 609},
        "Ekonomi Pembangunan": {"mn": 569, "mx": 604},
        "Hubungan Internasional": {"mn": 566, "mx": 601},
        "Ilmu Administrasi Bisnis": {"mn": 563, "mx": 598},
        "Ilmu Politik": {"mn": 559, "mx": 594},
        "Sosiologi": {"mn": 553, "mx": 588},
        "Ilmu Kesejahteraan Sosial": {"mn": 549, "mx": 584},
        "Kriminologi": {"mn": 547, "mx": 582},
        "Ilmu Pemerintahan": {"mn": 546, "mx": 581},
        "Antropologi Sosial": {"mn": 541, "mx": 576},
        "Ilmu Sejarah": {"mn": 536, "mx": 571},
        "Sastra Inggris": {"mn": 534, "mx": 569},
        "Sastra Indonesia": {"mn": 528, "mx": 563},
        "Pendidikan Bahasa Inggris": {"mn": 526, "mx": 561},
        "Pendidikan Ekonomi": {"mn": 523, "mx": 558},
        "Pendidikan Sejarah": {"mn": 520, "mx": 555},
        "Pendidikan Sosiologi": {"mn": 517, "mx": 552},
        "Perpustakaan dan Ilmu Informasi": {"mn": 515, "mx": 550},
        "Keuangan dan Perbankan": {"mn": 513, "mx": 548},
        "Bisnis Internasional": {"mn": 511, "mx": 546},
        "Pariwisata": {"mn": 506, "mx": 541},
        "Administrasi Negara": {"mn": 503, "mx": 538},
        "Pendidikan Pancasila dan Kewarganegaraan": {"mn": 500, "mx": 535},
        "Sastra Arab": {"mn": 494, "mx": 529},
        "Sastra Jawa": {"mn": 487, "mx": 522},
        "Filsafat": {"mn": 483, "mx": 518},
        "_default": {"mn": 542, "mx": 577},
        "_klaster": 4, "_lbl": "🔸 Klaster 4 — Regional"
    },
    "Bina Nusantara University": {
        "Pendidikan Dokter (Kedokteran)": {"mn": 641, "mx": 676},
        "Teknik Informatika": {"mn": 633, "mx": 668},
        "Farmasi": {"mn": 621, "mx": 656},
        "Teknik Elektro": {"mn": 617, "mx": 652},
        "Ilmu Komputer": {"mn": 613, "mx": 648},
        "Teknik Kimia": {"mn": 609, "mx": 644},
        "Teknik Mesin": {"mn": 605, "mx": 640},
        "Teknik Sipil": {"mn": 601, "mx": 636},
        "Kedokteran Gigi": {"mn": 599, "mx": 634},
        "Bioteknologi": {"mn": 593, "mx": 628},
        "Teknik Industri": {"mn": 591, "mx": 626},
        "Statistika": {"mn": 587, "mx": 622},
        "Matematika": {"mn": 583, "mx": 618},
        "Fisika": {"mn": 579, "mx": 614},
        "Kimia": {"mn": 575, "mx": 610},
        "Biologi": {"mn": 573, "mx": 608},
        "Teknik Lingkungan": {"mn": 569, "mx": 604},
        "Teknik Geologi": {"mn": 567, "mx": 602},
        "Teknik Perminyakan": {"mn": 565, "mx": 600},
        "Arsitektur": {"mn": 564, "mx": 599},
        "Perencanaan Wilayah dan Kota": {"mn": 561, "mx": 596},
        "Ilmu Gizi": {"mn": 559, "mx": 594},
        "Keperawatan": {"mn": 555, "mx": 590},
        "Agroteknologi": {"mn": 549, "mx": 584},
        "Agribisnis": {"mn": 547, "mx": 582},
        "Kehutanan": {"mn": 543, "mx": 578},
        "Ilmu Tanah": {"mn": 539, "mx": 574},
        "Teknologi Pangan": {"mn": 537, "mx": 572},
        "Peternakan": {"mn": 533, "mx": 568},
        "Ilmu Kelautan": {"mn": 529, "mx": 564},
        "Psikologi": {"mn": 625, "mx": 660},
        "Hukum": {"mn": 617, "mx": 652},
        "Akuntansi": {"mn": 613, "mx": 648},
        "Manajemen": {"mn": 607, "mx": 642},
        "Ilmu Komunikasi": {"mn": 605, "mx": 640},
        "Ekonomi Pembangunan": {"mn": 599, "mx": 634},
        "Hubungan Internasional": {"mn": 597, "mx": 632},
        "Ilmu Administrasi Bisnis": {"mn": 593, "mx": 628},
        "Ilmu Politik": {"mn": 589, "mx": 624},
        "Sosiologi": {"mn": 583, "mx": 618},
        "Ilmu Kesejahteraan Sosial": {"mn": 579, "mx": 614},
        "Kriminologi": {"mn": 577, "mx": 612},
        "Ilmu Pemerintahan": {"mn": 575, "mx": 610},
        "Antropologi Sosial": {"mn": 571, "mx": 606},
        "Ilmu Sejarah": {"mn": 565, "mx": 600},
        "Sastra Inggris": {"mn": 563, "mx": 598},
        "Sastra Indonesia": {"mn": 557, "mx": 592},
        "Pendidikan Bahasa Inggris": {"mn": 555, "mx": 590},
        "Pendidikan Ekonomi": {"mn": 551, "mx": 586},
        "Pendidikan Sejarah": {"mn": 548, "mx": 583},
        "Pendidikan Sosiologi": {"mn": 545, "mx": 580},
        "Perpustakaan dan Ilmu Informasi": {"mn": 543, "mx": 578},
        "Keuangan dan Perbankan": {"mn": 541, "mx": 576},
        "Bisnis Internasional": {"mn": 539, "mx": 574},
        "Pariwisata": {"mn": 533, "mx": 568},
        "Administrasi Negara": {"mn": 531, "mx": 566},
        "Pendidikan Pancasila dan Kewarganegaraan": {"mn": 527, "mx": 562},
        "Sastra Arab": {"mn": 521, "mx": 556},
        "Sastra Jawa": {"mn": 513, "mx": 548},
        "Filsafat": {"mn": 509, "mx": 544},
        "_default": {"mn": 572, "mx": 607},
        "_klaster": 4, "_lbl": "🔸 Klaster 4 — Regional"
    },
    "Universitas Muhammadiyah Malang": {
        "Pendidikan Dokter (Kedokteran)": {"mn": 600, "mx": 635},
        "Teknik Informatika": {"mn": 593, "mx": 628},
        "Farmasi": {"mn": 581, "mx": 616},
        "Teknik Elektro": {"mn": 577, "mx": 612},
        "Ilmu Komputer": {"mn": 574, "mx": 609},
        "Teknik Kimia": {"mn": 570, "mx": 605},
        "Teknik Mesin": {"mn": 566, "mx": 601},
        "Teknik Sipil": {"mn": 563, "mx": 598},
        "Kedokteran Gigi": {"mn": 561, "mx": 596},
        "Bioteknologi": {"mn": 555, "mx": 590},
        "Teknik Industri": {"mn": 553, "mx": 588},
        "Statistika": {"mn": 549, "mx": 584},
        "Matematika": {"mn": 546, "mx": 581},
        "Fisika": {"mn": 541, "mx": 576},
        "Kimia": {"mn": 539, "mx": 574},
        "Biologi": {"mn": 536, "mx": 571},
        "Teknik Lingkungan": {"mn": 533, "mx": 568},
        "Teknik Geologi": {"mn": 531, "mx": 566},
        "Teknik Perminyakan": {"mn": 529, "mx": 564},
        "Arsitektur": {"mn": 528, "mx": 563},
        "Perencanaan Wilayah dan Kota": {"mn": 525, "mx": 560},
        "Ilmu Gizi": {"mn": 523, "mx": 558},
        "Keperawatan": {"mn": 519, "mx": 554},
        "Agroteknologi": {"mn": 514, "mx": 549},
        "Agribisnis": {"mn": 512, "mx": 547},
        "Kehutanan": {"mn": 509, "mx": 544},
        "Ilmu Tanah": {"mn": 504, "mx": 539},
        "Teknologi Pangan": {"mn": 503, "mx": 538},
        "Peternakan": {"mn": 499, "mx": 534},
        "Ilmu Kelautan": {"mn": 495, "mx": 530},
        "Psikologi": {"mn": 585, "mx": 620},
        "Hukum": {"mn": 577, "mx": 612},
        "Akuntansi": {"mn": 574, "mx": 609},
        "Manajemen": {"mn": 569, "mx": 604},
        "Ilmu Komunikasi": {"mn": 566, "mx": 601},
        "Ekonomi Pembangunan": {"mn": 561, "mx": 596},
        "Hubungan Internasional": {"mn": 559, "mx": 594},
        "Ilmu Administrasi Bisnis": {"mn": 555, "mx": 590},
        "Ilmu Politik": {"mn": 551, "mx": 586},
        "Sosiologi": {"mn": 546, "mx": 581},
        "Ilmu Kesejahteraan Sosial": {"mn": 541, "mx": 576},
        "Kriminologi": {"mn": 540, "mx": 575},
        "Ilmu Pemerintahan": {"mn": 539, "mx": 574},
        "Antropologi Sosial": {"mn": 534, "mx": 569},
        "Ilmu Sejarah": {"mn": 529, "mx": 564},
        "Sastra Inggris": {"mn": 527, "mx": 562},
        "Sastra Indonesia": {"mn": 521, "mx": 556},
        "Pendidikan Bahasa Inggris": {"mn": 519, "mx": 554},
        "Pendidikan Ekonomi": {"mn": 516, "mx": 551},
        "Pendidikan Sejarah": {"mn": 513, "mx": 548},
        "Pendidikan Sosiologi": {"mn": 510, "mx": 545},
        "Perpustakaan dan Ilmu Informasi": {"mn": 509, "mx": 544},
        "Keuangan dan Perbankan": {"mn": 506, "mx": 541},
        "Bisnis Internasional": {"mn": 504, "mx": 539},
        "Pariwisata": {"mn": 499, "mx": 534},
        "Administrasi Negara": {"mn": 497, "mx": 532},
        "Pendidikan Pancasila dan Kewarganegaraan": {"mn": 493, "mx": 528},
        "Sastra Arab": {"mn": 487, "mx": 522},
        "Sastra Jawa": {"mn": 480, "mx": 515},
        "Filsafat": {"mn": 476, "mx": 511},
        "_default": {"mn": 535, "mx": 570},
        "_klaster": 4, "_lbl": "🔸 Klaster 4 — Regional"
    },
}


# ══════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ══════════════════════════════════════════════════════════
def hitung_skor_weighted(scores: dict, jurusan: str) -> float:
    bobot = get_bobot(jurusan)
    return round(sum(scores.get(s,500)*bobot.get(s,0) for s in SUBTES), 1)

def get_target_range(ptn: str, jurusan: str):
    info = PTN_JURUSAN_DATA.get(ptn,{})
    p = info.get(jurusan, info.get("_default",{"mn":600,"mx":650}))
    return p["mn"], p["mx"]

def get_klaster_ptn(ptn: str):
    info = PTN_JURUSAN_DATA.get(ptn,{})
    return info.get("_klaster",3), info.get("_lbl","🔹 Klaster 3")

def get_status(skor: float, mn: int, mx: int):
    mid = (mn+mx)/2
    if skor >= mx:        return "Sangat Aman","sbg-sa","🟢"
    elif skor >= mid:     return "Aman","sbg-a","🔵"
    elif skor >= mn:      return "Batas Aman","sbg-k","🟡"
    elif skor >= mn-30:   return "Kurang","sbg-r","🔴"
    else:                 return "Perlu Kerja Keras","sbg-r","⚠️"

def bar_html(label, val, mx, color):
    pct = min(100, round((val-200)/(mx-200)*100))
    return f"""<div class="prog-wrap">
<div class="prog-lbl"><span>{label}</span><span>{val:.0f}</span></div>
<div class="prog-bg"><div class="prog-fill" style="width:{pct}%;background:{color};"></div></div>
</div>"""

def render_topbar(step:int):
    steps=[("📋","Survey"),("🧠","Analisis"),("📊","Hasil")]
    pills="".join(
        f'<span class="step-pill" style="font-size:.72rem;font-weight:600;padding:.26rem .8rem;border-radius:99px;'
        f'{"background:#e6f5ee;color:#148a42;border:1px solid #9adbb8;" if i+1<step else "background:#eef2fc;color:#3464c8;border:1px solid #aac0f0;" if i+1==step else "background:#f7f9fd;color:#6a7a9a;border:1px solid #e0e8f4;"}"'
        f'>{("✓ " if i+1<step else f"{i+1}. ")+s[0]+" "+s[1]}</span>'
        for i,s in enumerate(steps))
    st.markdown(f"""<div style="display:flex;align-items:center;gap:.8rem;background:#fff;
    border-bottom:2px solid #e0e8f4;padding:.6rem 1.5rem;margin:-1rem -1.5rem 1.5rem;
    position:sticky;top:0;z-index:999;box-shadow:0 2px 12px rgba(30,60,140,.07);">
    <span style="font-family:'Space Grotesk',sans-serif;font-size:1.05rem;font-weight:800;color:#3464c8;animation:float 3s ease-in-out infinite">🎯 SKORIA</span>
    <span style="font-size:.65rem;color:#6a7a9a;flex:1">AI UTBK Dashboard v4.0</span>
    {pills}
    </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# PAGE HOME
# ══════════════════════════════════════════════════════════
def page_home():
    st.markdown("""<div class="hero">
    <div class="hero-badge">🤖 AI-Powered · 30 PTN · 60 Prodi · Data SNPMB 2022–2024</div>
    <h1>🎯 SKORIA <span>v4.0</span></h1>
    <p>Platform kecerdasan buatan untuk analisis kesiapan UTBK-SNBT secara holistik.<br>
    Masukkan estimasi skor 7 subtes TPS dan dapatkan analisis mendalam beserta strategi belajar personal.</p>
    </div>""", unsafe_allow_html=True)

    st.markdown("""<div class="stat-row">
    <div class="stat-box"><div class="stat-num">30</div><div class="stat-lbl">PTN Terkemuka</div></div>
    <div class="stat-box"><div class="stat-num">60</div><div class="stat-lbl">Program Studi</div></div>
    <div class="stat-box"><div class="stat-num">7</div><div class="stat-lbl">Subtes TPS</div></div>
    <div class="stat-box"><div class="stat-num">AI</div><div class="stat-lbl">Analisis Cerdas</div></div>
    </div>""", unsafe_allow_html=True)

    st.markdown("""<div class="feat-grid">
    <div class="feat-card"><span class="feat-icon">📊</span>
    <div class="feat-title">Analisis 7 Subtes</div>
    <div class="feat-desc">Evaluasi mendalam PU, PPU, PBM, PK, LBI, LBE, PM dengan bobot per jurusan</div></div>
    <div class="feat-card"><span class="feat-icon">🎯</span>
    <div class="feat-title">30 PTN & 60 Prodi</div>
    <div class="feat-desc">Data estimasi nilai aman dari historis UTBK 2022-2024 sumber terpercaya</div></div>
    <div class="feat-card"><span class="feat-icon">🤖</span>
    <div class="feat-title">Rekomendasi AI</div>
    <div class="feat-desc">Strategi belajar personal berbasis analisis profil skor dan target PTN-mu</div></div>
    <div class="feat-card"><span class="feat-icon">📅</span>
    <div class="feat-title">Study Plan 8 Minggu</div>
    <div class="feat-desc">Rencana belajar terstruktur disesuaikan kelemahan dan waktu tersisa</div></div>
    </div>""", unsafe_allow_html=True)

    st.markdown("""<div class="al al-i">
    <h4>ℹ️ Tentang Data</h4>
    Data estimasi nilai aman bersumber dari historis UTBK-SNBT 2022–2024 yang dikompilasi dari 
    bocahkampus.com, quipper.com, tipskuliah.com, cerebrum.id, dan studiliv.com. 
    Data resmi: <b>snpmb.bppp.kemdikbud.go.id</b>. 
    Nilai aktual dapat berbeda tergantung tahun dan jumlah peminat.
    </div>""", unsafe_allow_html=True)

    col1,col2,col3=st.columns([1,2,1])
    with col2:
        if st.button("🚀 Mulai Analisis Sekarang",type="primary",use_container_width=True,key="btn_home_start"):
            st.session_state.page="survey"; st.session_state.step=1; st.rerun()

# ══════════════════════════════════════════════════════════
# PAGE SURVEY
# ══════════════════════════════════════════════════════════
def page_survey():
    render_topbar(1)
    d = st.session_state.data

    if st.session_state.step == 1:
        st.markdown('<div class="sec">📋 Informasi Dasar & Target</div>', unsafe_allow_html=True)
        st.markdown('<div class="form-box"><h3>👤 Data Diri & Target</h3>', unsafe_allow_html=True)
        col1,col2 = st.columns(2)
        with col1:
            nama=st.text_input("Nama / Inisial",value=d.get("nama",""),key="inp_nama",placeholder="Nama kamu...")
            ptn=st.selectbox("Target PTN",DAFTAR_PTN,index=DAFTAR_PTN.index(d.get("ptn",DAFTAR_PTN[0])),key="inp_ptn")
        with col2:
            jurusan=st.selectbox("Target Jurusan/Prodi",DAFTAR_JURUSAN_S1,
                index=DAFTAR_JURUSAN_S1.index(d.get("jurusan",DAFTAR_JURUSAN_S1[0])),key="inp_jurusan")
            asal=st.text_input("Asal Sekolah (opsional)",value=d.get("asal",""),key="inp_asal")
        st.markdown('</div>', unsafe_allow_html=True)
        if ptn and jurusan:
            mn,mx = get_target_range(ptn,jurusan)
            kl,kl_lbl = get_klaster_ptn(ptn)
            st.markdown(f"""<div class="al al-i">
            <h4>🎯 {jurusan} — {ptn}</h4>
            <b>Klaster:</b> {kl_lbl} &nbsp;|&nbsp;
            <b>Estimasi nilai aman:</b> {mn}–{mx} &nbsp;|&nbsp;
            <b>Nilai tengah:</b> {(mn+mx)//2}
            </div>""", unsafe_allow_html=True)
        col1,col2=st.columns(2)
        with col1:
            if st.button("← Beranda",key="btn_s1_back"): st.session_state.page="home"; st.rerun()
        with col2:
            if st.button("Lanjut: Input Skor →",type="primary",use_container_width=True,key="btn_s1_next"):
                if not nama: st.warning("Masukkan nama terlebih dahulu.")
                else:
                    d.update({"nama":nama,"ptn":ptn,"jurusan":jurusan,"asal":asal})
                    st.session_state.step=2; st.rerun()

    elif st.session_state.step == 2:
        st.markdown('<div class="sec">📝 Prediksi Skor 7 Subtes TPS</div>', unsafe_allow_html=True)
        st.markdown("""<div class="al al-i"><h4>ℹ️ Panduan</h4>
        Masukkan <b>estimasi skor</b> berdasarkan tryout atau perkiraanmu. Skala: <b>200–1000</b> per subtes.
        </div>""", unsafe_allow_html=True)
        scores = d.get("scores",{s:500 for s in SUBTES})
        new_scores = {}
        cola,colb = st.columns(2)
        with cola:
            st.markdown('<div class="form-box"><h3>🧠 TPS Sains & Penalaran</h3>', unsafe_allow_html=True)
            for s in ["PU","PPU","PBM","PK"]:
                new_scores[s]=st.number_input(f"{s} — {SUBTES_FULL[s]}",min_value=200,max_value=1000,
                    value=int(scores.get(s,500)),step=5,key=f"inp_{s}")
            st.markdown('</div>', unsafe_allow_html=True)
        with colb:
            st.markdown('<div class="form-box"><h3>📚 Literasi & Matematika</h3>', unsafe_allow_html=True)
            for s in ["LBI","LBE","PM"]:
                new_scores[s]=st.number_input(f"{s} — {SUBTES_FULL[s]}",min_value=200,max_value=1000,
                    value=int(scores.get(s,500)),step=5,key=f"inp_{s}")
            st.markdown('</div>', unsafe_allow_html=True)
        col1,col2,col3=st.columns(3)
        with col1:
            if st.button("← Kembali",key="btn_s2_back"): st.session_state.step=1; st.rerun()
        with col3:
            if st.button("Lanjut: Profil Belajar →",type="primary",use_container_width=True,key="btn_s2_next"):
                d["scores"]=new_scores; st.session_state.step=3; st.rerun()

    elif st.session_state.step == 3:
        st.markdown('<div class="sec">📚 Profil & Kebiasaan Belajar</div>', unsafe_allow_html=True)
        st.markdown('<div class="form-box"><h3>⏰ Kebiasaan Belajar</h3>', unsafe_allow_html=True)
        col1,col2,col3=st.columns(3)
        with col1: jam_hari=st.slider("Jam belajar/hari",0,12,int(d.get("jam_hari",4)),key="inp_jam")
        with col2: hari_minggu=st.slider("Hari belajar/minggu",1,7,int(d.get("hari_minggu",5)),key="inp_hari")
        with col3: tryout_count=st.slider("Jumlah tryout",0,30,int(d.get("tryout_count",3)),key="inp_tryout")
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('<div class="form-box"><h3>🧠 Kondisi Psikologis & Waktu</h3>', unsafe_allow_html=True)
        col1,col2=st.columns(2)
        opts_level=["Rendah","Sedang","Tinggi","Sangat Tinggi"]
        with col1:
            fokus=st.select_slider("Tingkat Fokus",opts_level,value=d.get("fokus","Tinggi"),key="inp_fokus")
            anxiety=st.select_slider("Tingkat Kecemasan",opts_level,value=d.get("anxiety","Sedang"),key="inp_anxiety")
        with col2:
            motivasi=st.select_slider("Tingkat Motivasi",opts_level,value=d.get("motivasi","Tinggi"),key="inp_motivasi")
            durasi_utbk=st.selectbox("Berapa bulan lagi UTBK?",
                ["< 1 bulan","1-2 bulan","3-4 bulan","5-6 bulan","6+ bulan"],
                index=["< 1 bulan","1-2 bulan","3-4 bulan","5-6 bulan","6+ bulan"].index(d.get("durasi_utbk","3-4 bulan")),
                key="inp_durasi")
        st.markdown('</div>', unsafe_allow_html=True)
        col1,_,col3=st.columns(3)
        with col1:
            if st.button("← Kembali",key="btn_s3_back"): st.session_state.step=2; st.rerun()
        with col3:
            if st.button("🚀 Analisis Sekarang!",type="primary",use_container_width=True,key="btn_s3_next"):
                d.update({"jam_hari":jam_hari,"hari_minggu":hari_minggu,"tryout_count":tryout_count,
                          "fokus":fokus,"anxiety":anxiety,"motivasi":motivasi,"durasi_utbk":durasi_utbk})
                st.session_state.result=run_analysis(d)
                st.session_state.page="result"; st.rerun()

# ══════════════════════════════════════════════════════════
# ANALYSIS ENGINE
# ══════════════════════════════════════════════════════════
def run_analysis(d:dict)->dict:
    scores=d.get("scores",{}); jurusan=d.get("jurusan","Teknik Informatika"); ptn=d.get("ptn","Universitas Indonesia")
    skor_w=hitung_skor_weighted(scores,jurusan)
    mn,mx=get_target_range(ptn,jurusan); mid=(mn+mx)/2
    status,badge_cls,icon=get_status(skor_w,mn,mx)
    bobot=get_bobot(jurusan)
    sa={}
    for s in SUBTES:
        sc=scores.get(s,500); w=bobot[s]; kontribusi=sc*w
        level="Unggul" if sc>=750 else "Baik" if sc>=650 else "Cukup" if sc>=550 else "Perlu Ditingkatkan" if sc>=450 else "Lemah"
        sa[s]={"skor":sc,"bobot":w,"kontribusi":kontribusi,"level":level}
    sorted_s=sorted(sa.items(),key=lambda x:x[1]["kontribusi"])
    weak_2=[s for s,_ in sorted_s[:2]]; strong_2=[s for s,_ in sorted_s[-2:]]
    return {
        "nama":d.get("nama",""),"ptn":ptn,"jurusan":jurusan,"skor_weighted":skor_w,
        "scores":scores,"mn":mn,"mx":mx,"mid":mid,"status":status,"badge_cls":badge_cls,"icon":icon,
        "gap":mn-skor_w,"subtes_analysis":sa,"bobot":bobot,"weak_2":weak_2,"strong_2":strong_2,
        "alternatif":ALTERNATIF_MAP.get(jurusan,[]),
        "plan":gen_plan(d,weak_2,mn-skor_w),
        "rekom":gen_rekom(d,sa,weak_2,strong_2,mn-skor_w),
        "klaster":get_klaster_ptn(ptn),"profil":d,
    }

def gen_plan(d,weak_2,gap):
    dur=d.get("durasi_utbk","3-4 bulan")
    wn=[SUBTES_FULL[s] for s in weak_2]
    if dur in ["< 1 bulan","1-2 bulan"]:
        return [("Minggu 1-2","Intensif Subtes Lemah",f"Fokus {wn[0]}: latihan soal intensif 2 jam/hari + review materi"),
                ("Minggu 3","Simulasi Full",f"Tryout lengkap + koreksi {wn[1]}: target naik 30-50 poin"),
                ("Minggu 4","Pemantapan","Review semua subtes, simulasi kondisi ujian, istirahat cukup")]
    return [("Minggu 1-2","Diagnosis & Fondasi",f"Tryout awal, pelajari pola soal {wn[0]} dan {wn[1]}"),
            ("Minggu 3-4",f"Intensif {wn[0]}",f"Latihan {wn[0]} 1.5 jam/hari, review materi terkait"),
            ("Minggu 5-6",f"Intensif {wn[1]}",f"Latihan {wn[1]} 1.5 jam/hari + pembahasan soal tahun lalu"),
            ("Minggu 7","Simulasi & Review","Tryout full 2x seminggu, analisis kesalahan, perkuat subtes lain"),
            ("Minggu 8","Pemantapan Final","Tryout final, manajemen waktu ujian, jaga kondisi fisik & mental")]

def gen_rekom(d,sa,weak_2,strong_2,gap):
    items=[]
    sn=" dan ".join([SUBTES_FULL[s] for s in strong_2])
    items.append(("strength",f"Kekuatan utama: {sn}",
        [f"Pertahankan konsistensi pada {sn}","Jadikan subtes ini anchor skor tertinggi",
         "Fokus ke soal level advanced untuk memaksimalkan poin"]))
    for w in weak_2:
        items.append(("weakness",f"Perlu ditingkatkan: {SUBTES_FULL[w]} (skor: {sa[w]['skor']:.0f})",
            [f"Alokasikan minimum 90 menit/hari untuk {SUBTES_FULL[w]}","Gunakan bank soal UTBK 2022-2024",
             f"Target kenaikan: +{min(50,max(20,800-sa[w]['skor']))//10*10} poin dalam 4 minggu"]))
    if gap > 0:
        items.append(("danger",f"Gap ke nilai aman: {gap:.0f} poin",
            [f"Butuh peningkatan rata-rata ~{gap/7:.0f} poin per subtes",
             "Perbanyak tryout minimal 2x seminggu","Pastikan jam belajar konsisten"]))
    else:
        items.append(("success",f"Sudah melampaui nilai minimum aman ({-gap:.0f} poin di atas batas bawah)",
            ["Pertahankan konsistensi belajar","Targetkan nilai tengah atau maksimum",
             "Jangan lengah — persaingan UTBK sangat ketat"]))
    if d.get("anxiety","Sedang") in ["Tinggi","Sangat Tinggi"]:
        items.append(("info","Manajemen Kecemasan Ujian",
            ["Latihan teknik pernapasan 4-7-8 sebelum ujian",
             "Simulasi kondisi ujian 1x/minggu","Fokus ke proses belajar, bukan hanya hasil"]))
    return items

# ══════════════════════════════════════════════════════════
# PAGE RESULT
# ══════════════════════════════════════════════════════════
def page_result():
    render_topbar(3)
    r=st.session_state.result
    if not r: st.warning("Data tidak ditemukan."); return

    nama=r["nama"]; ptn=r["ptn"]; jurusan=r["jurusan"]
    skor=r["skor_weighted"]; mn=r["mn"]; mx=r["mx"]; mid=r["mid"]
    status=r["status"]; icon=r["icon"]; gap=r["gap"]
    scores=r["scores"]; sa=r["subtes_analysis"]; bobot=r["bobot"]
    kl,kl_lbl=r["klaster"]

    st.markdown(f"""<div class="hero">
    <div class="hero-badge">📊 Hasil Analisis SKORIA v4.0</div>
    <h1>Halo, <span>{nama}</span>! 🎯</h1>
    <p>Analisis kesiapan UTBK untuk <b>{jurusan}</b> — <b>{ptn}</b> ({kl_lbl})<br>
    Estimasi Nilai Aman: <b>{mn}–{mx}</b> | Nilai Tengah: <b>{mid:.0f}</b></p>
    </div>""", unsafe_allow_html=True)

    gap_color="c-green" if gap<=0 else "c-red"
    gap_disp=f"+{-gap:.0f}" if gap<0 else f"-{gap:.0f}"
    pct=round((skor-mn)/(mx-mn)*100) if mx!=mn else 0

    c1,c2,c3,c4=st.columns(4)
    with c1: st.markdown(f'<div class="card"><div class="kpi-lbl">Skor Weighted</div><div class="kpi-val c-blue">{skor:.0f}</div><div class="kpi-sub">dari maks 1000</div></div>', unsafe_allow_html=True)
    with c2: st.markdown(f'<div class="card"><div class="kpi-lbl">Status</div><div class="kpi-val" style="font-size:1.15rem">{icon} {status}</div><div class="kpi-sub">vs target {ptn[:18]}...</div></div>', unsafe_allow_html=True)
    with c3: st.markdown(f'<div class="card"><div class="kpi-lbl">Gap Nilai Aman</div><div class="kpi-val {gap_color}">{gap_disp}</div><div class="kpi-sub">{"✓ Di atas minimum" if gap<=0 else "Masih perlu ditingkatkan"}</div></div>', unsafe_allow_html=True)
    with c4: st.markdown(f'<div class="card"><div class="kpi-lbl">Posisi dalam Range</div><div class="kpi-val c-purple">{min(100,max(0,pct))}%</div><div class="kpi-sub">dalam rentang {mn}–{mx}</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="anim-div"></div>', unsafe_allow_html=True)

    tab1,tab2,tab3,tab4=st.tabs(["📊 Skor & Subtes","🎯 Analisis Target","💡 Rekomendasi","📅 Study Plan"])

    with tab1:
        c1,c2=st.columns(2)
        with c1:
            st.markdown('<div class="sec">📊 Profil Skor Per Subtes</div>', unsafe_allow_html=True)
            for s in SUBTES:
                lv=sa[s]["level"]
                ic="🟢" if lv=="Unggul" else "🔵" if lv=="Baik" else "🟡" if lv=="Cukup" else "🔴"
                st.markdown(bar_html(f"{ic} {s} — {SUBTES_FULL[s]}",sa[s]["skor"],1000,SUBTES_CLR[s]),unsafe_allow_html=True)
        with c2:
            vals=[scores.get(s,500) for s in SUBTES]
            fig=go.Figure()
            fig.add_trace(go.Scatterpolar(r=vals+[vals[0]],theta=SUBTES+[SUBTES[0]],fill="toself",name="Skor Kamu",
                line=dict(color="#3464c8",width=2.5),fillcolor="rgba(52,100,200,.15)"))
            fig.add_trace(go.Scatterpolar(r=[mn]*len(SUBTES)+[mn],theta=SUBTES+[SUBTES[0]],mode="lines",
                name=f"Min ({mn})",line=dict(color="#d4900a",width=1.5,dash="dot")))
            fig.update_layout(polar=dict(radialaxis=dict(range=[200,1000])),showlegend=True,
                margin=dict(t=30,b=30,l=30,r=30),height=350,
                paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Plus Jakarta Sans"))
            st.plotly_chart(fig,use_container_width=True,key="chart_radar")
        st.markdown(f'<div class="sec">⚖️ Bobot Subtes untuk {jurusan}</div>', unsafe_allow_html=True)
        df=pd.DataFrame([{"Subtes":s,"Nama":SUBTES_FULL[s],"Bobot":f"{bobot[s]*100:.0f}%",
            "Skor":scores.get(s,500),"Kontribusi":f"{sa[s]['kontribusi']:.1f}","Level":sa[s]["level"]}
            for s in SUBTES])
        st.dataframe(df,use_container_width=True,hide_index=True)

    with tab2:
        c1,c2=st.columns(2)
        with c1:
            st.markdown('<div class="sec">🎯 Posisi Skor vs Target</div>', unsafe_allow_html=True)
            fig2=go.Figure()
            fig2.add_trace(go.Bar(name="Skor Kamu",x=["Skor"],y=[skor],marker_color="#3464c8",text=[f"{skor:.0f}"],textposition="outside"))
            fig2.add_trace(go.Bar(name="Nilai Min",x=["Min Aman"],y=[mn],marker_color="#d4900a",text=[str(mn)],textposition="outside"))
            fig2.add_trace(go.Bar(name="Nilai Max",x=["Max Aman"],y=[mx],marker_color="#148a42",text=[str(mx)],textposition="outside"))
            fig2.update_layout(height=300,margin=dict(t=20,b=20,l=20,r=20),
                paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Plus Jakarta Sans"),yaxis=dict(range=[0,1050]))
            st.plotly_chart(fig2,use_container_width=True,key="chart_bar")
        with c2:
            st.markdown('<div class="sec">🔄 Jurusan Alternatif di PTN Sama</div>', unsafe_allow_html=True)
            for a in r["alternatif"]:
                mn_a,mx_a=get_target_range(ptn,a)
                st_a,_,ic_a=get_status(skor,mn_a,mx_a)
                st.markdown(f'<div class="card" style="margin-bottom:.6rem"><b>{ic_a} {a}</b><br><small style="color:#6a7a9a">Nilai Aman: {mn_a}–{mx_a} | {st_a}</small></div>', unsafe_allow_html=True)
        st.markdown('<div class="sec">🏫 Semua PTN — Jurusan Sama</div>', unsafe_allow_html=True)
        rows=[]
        for p in DAFTAR_PTN:
            mn_p,mx_p=get_target_range(p,jurusan)
            st_p,_,ic_p=get_status(skor,mn_p,mx_p)
            kl_p,kl_lbl_p=get_klaster_ptn(p)
            rows.append({"PTN":p,"Klaster":kl_lbl_p,"Min":mn_p,"Max":mx_p,"Status":f"{ic_p} {st_p}"})
        st.dataframe(pd.DataFrame(rows),use_container_width=True,hide_index=True)

    with tab3:
        st.markdown('<div class="sec">💡 Rekomendasi Personal</div>', unsafe_allow_html=True)
        cls_map={"strength":"al-s","weakness":"al-w","danger":"al-d","info":"al-i","success":"al-s"}
        icon_map={"strength":"✅","weakness":"⚠️","danger":"🔴","info":"ℹ️","success":"🎉"}
        for kind,title,pts in r["rekom"]:
            pts_html="".join(f"<li>{p}</li>" for p in pts)
            al_cls = cls_map.get(kind, "al-i")
            al_icon = icon_map.get(kind, "💡")
            st.markdown(f'<div class="al {al_cls}"><h4>{al_icon} {title}</h4><ul>{pts_html}</ul></div>', unsafe_allow_html=True)

    with tab4:
        st.markdown('<div class="sec">📅 Rencana Belajar</div>', unsafe_allow_html=True)
        for period,target,tasks in r["plan"]:
            st.markdown(f'<div class="week-card"><div class="week-num">⏱ {period}</div><div class="week-target">🎯 {target}</div><div class="week-tasks">{tasks}</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="anim-div"></div>', unsafe_allow_html=True)
    c1,c2,c3=st.columns(3)
    with c1:
        if st.button("← Ubah Input",key="btn_r_back"): st.session_state.page="survey"; st.session_state.step=2; st.rerun()
    with c2:
        if st.button("🏠 Beranda",key="btn_r_home"): st.session_state.page="home"; st.rerun()
    with c3:
        if st.button("🔄 Analisis Baru",type="primary",use_container_width=True,key="btn_r_new"):
            st.session_state.data={}; st.session_state.result=None
            st.session_state.page="survey"; st.session_state.step=1; st.rerun()

# ══════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════
def main():
    page=st.session_state.page
    if page=="home": page_home()
    elif page=="survey": page_survey()
    elif page=="result": page_result()
    else: page_home()

if __name__=="__main__":
    main()
