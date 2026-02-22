"""
SKORIA — AI UTBK Readiness Dashboard v5.0
Platform kecerdasan buatan untuk analisis kesiapan UTBK secara holistik
Skor maksimal: 1000 | Jenjang S1 & D3 | Multi-halaman | Charts | PDF Export
Data skor aman berbasis SNPMB/BPPP Kemdikbud & referensi media pendidikan 2025/2026
per jurusan, jenjang (S1/D3), dan 30 PTN
"""

import streamlit as st
import numpy as np
import pandas as pd
import pickle, os, base64, datetime, json
from typing import Dict, Tuple, List
import plotly.graph_objects as go
import plotly.express as px

# ══════════════════════════════════════════════════════════
# PAGE CONFIG
# ══════════════════════════════════════════════════════════
st.set_page_config(
    page_title="SKORIA — AI UTBK",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ══════════════════════════════════════════════════════════
# GLOBAL CSS — Animated Design System v4.1
# ══════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@600;700;800&display=swap');

:root {
  --bg:      #f0f4fa;
  --surf:    #ffffff;
  --surf2:   #f7f9fd;
  --border:  #e0e8f4;
  --accent:  #3464c8;
  --a2:      #5080e0;
  --gold:    #d4900a;
  --green:   #148a42;
  --red:     #c0392b;
  --orange:  #d4620a;
  --purple:  #6b3fca;
  --teal:    #0d8a80;
  --text:    #12203f;
  --text2:   #334466;
  --text3:   #6a7a9a;
  --r:       12px;
  --sh:      0 2px 12px rgba(30,60,140,.08);
  --sh2:     0 8px 32px rgba(30,60,140,.15);
}

/* ─── KEYFRAMES ─── */
@keyframes fadeSlideUp {
  from { opacity:0; transform:translateY(30px) scale(.97); }
  to   { opacity:1; transform:translateY(0) scale(1); }
}
@keyframes fadeSlideLeft {
  from { opacity:0; transform:translateX(-24px); }
  to   { opacity:1; transform:translateX(0); }
}
@keyframes fadeSlideRight {
  from { opacity:0; transform:translateX(24px); }
  to   { opacity:1; transform:translateX(0); }
}
@keyframes popIn {
  0%   { opacity:0; transform:scale(.5) rotate(-8deg); }
  65%  { opacity:1; transform:scale(1.1) rotate(3deg); }
  85%  { transform:scale(.96) rotate(-1deg); }
  100% { transform:scale(1) rotate(0); }
}
@keyframes pulseRing {
  0%,100% { box-shadow: 0 0 0 0 rgba(52,100,200,.35); }
  50%      { box-shadow: 0 0 0 10px rgba(52,100,200,0); }
}
@keyframes orb {
  0%,100% { transform:scale(1) translate(0,0); opacity:.08; }
  40%      { transform:scale(1.18) translate(15px,-12px); opacity:.14; }
  70%      { transform:scale(.88) translate(-10px,14px); opacity:.04; }
}
@keyframes float {
  0%,100% { transform:translateY(0px); }
  50%      { transform:translateY(-8px); }
}
@keyframes shimmer {
  from { background-position:-600px 0; }
  to   { background-position:600px 0; }
}
@keyframes progressGrow {
  from { width:0 !important; opacity:.4; }
}
@keyframes gradientFlow {
  0%,100% { background-position:0% 50%; }
  50%      { background-position:100% 50%; }
}
@keyframes ticker {
  from { transform:translateX(0); }
  to   { transform:translateX(-50%); }
}
@keyframes spinSlow {
  to { transform:rotate(360deg); }
}
@keyframes typeBar {
  from { width:0; }
}
@keyframes countUp {
  from { opacity:0; transform:translateY(14px) scale(.8); }
  to   { opacity:1; transform:translateY(0) scale(1); }
}
@keyframes rippleOut {
  from { transform:scale(0); opacity:.6; }
  to   { transform:scale(3); opacity:0; }
}
@keyframes borderTrail {
  0%   { clip-path:inset(0 100% 0 0); }
  100% { clip-path:inset(0 0% 0 0); }
}
@keyframes starSpin {
  0%   { opacity:0; transform:rotate(-30deg) scale(0); }
  60%  { opacity:1; transform:rotate(10deg) scale(1.2); }
  100% { opacity:1; transform:rotate(0) scale(1); }
}

/* ─── GLOBAL ─── */
html,body,[class*="css"],.stApp {
  background: var(--bg) !important;
  font-family: 'Plus Jakarta Sans', sans-serif !important;
  color: var(--text) !important;
}
#MainMenu, footer, header { visibility:hidden }
.stDeployButton { display:none }
.block-container { padding:1rem 1.5rem !important; max-width:100% !important; }

/* Page entry */
.main .block-container { animation: fadeSlideUp .5s cubic-bezier(.22,.68,0,1.2) both; }

/* ─── TOPBAR ─── */
.topbar {
  background:#fff;
  border-bottom:2px solid var(--border);
  padding:.6rem 2rem;
  display:flex; align-items:center; gap:1.2rem;
  margin:-1rem -1.5rem 1.5rem -1.5rem;
  position:sticky; top:0; z-index:999;
  box-shadow:0 2px 12px rgba(30,60,140,.07);
  animation:fadeSlideLeft .4s ease both;
}
.topbar-brand {
  font-family:'Space Grotesk',sans-serif;
  font-size:1.1rem; font-weight:800;
  color:var(--accent) !important;
  display:flex; align-items:center; gap:.5rem;
  animation:float 4s ease-in-out infinite;
}
.topbar-tag { font-size:.68rem; color:var(--text3); letter-spacing:.04em; }
.step-pill {
  font-size:.72rem; font-weight:600;
  padding:.26rem .8rem; border-radius:99px;
  color:var(--text3); background:var(--surf2);
  border:1px solid var(--border);
  transition:all .3s ease;
}
.step-pill.done  { background:#e6f5ee; color:var(--green); border-color:#9adbb8; animation:popIn .5s ease both; }
.step-pill.active{ background:#eef2fc; color:var(--accent); border-color:#aac0f0; animation:pulseRing 2.5s ease-in-out infinite; }

/* ─── HERO ─── */
.hero {
  background:linear-gradient(135deg,#1a3470 0%,#3464c8 55%,#2a50a8 100%);
  border-radius:16px; padding:2.4rem 3rem;
  margin-bottom:1.8rem; position:relative; overflow:hidden;
  box-shadow:0 6px 32px rgba(30,60,180,.22);
  animation:fadeSlideUp .65s cubic-bezier(.22,.68,0,1.2) both;
}
.hero::before {
  content:''; position:absolute; top:-70px; right:-70px;
  width:320px; height:320px; border-radius:50%;
  background:radial-gradient(circle,rgba(255,255,255,.12) 0%,transparent 65%);
  animation:orb 7s ease-in-out infinite;
}
.hero::after {
  content:''; position:absolute; bottom:-90px; left:8%;
  width:240px; height:240px; border-radius:50%;
  background:radial-gradient(circle,rgba(255,209,102,.09) 0%,transparent 65%);
  animation:orb 9s ease-in-out infinite reverse;
}
.hero h1 {
  font-family:'Space Grotesk',sans-serif !important;
  font-size:2rem !important; font-weight:800 !important;
  color:#fff !important; margin:0 0 .6rem !important;
  animation:fadeSlideLeft .7s cubic-bezier(.22,.68,0,1.2) .1s both;
}
.hero h1 span { color:#ffd166; }
.hero p {
  color:rgba(255,255,255,.82) !important; font-size:.95rem; margin:0; line-height:1.7;
  animation:fadeSlideUp .7s ease .2s both;
}
.hero-badge {
  display:inline-flex; align-items:center; gap:.4rem;
  background:rgba(255,255,255,.12); backdrop-filter:blur(4px);
  border:1px solid rgba(255,255,255,.2);
  padding:.3rem .85rem; border-radius:99px;
  font-size:.72rem; font-weight:600; color:rgba(255,255,255,.9);
  margin-bottom:1rem; animation:fadeSlideLeft .5s ease .05s both;
}

/* ─── ANIMATED DIVIDER ─── */
.anim-div {
  height:2px; border-radius:99px; margin:1.2rem 0;
  background:linear-gradient(90deg,var(--accent),var(--purple),var(--teal),var(--gold),var(--accent));
  background-size:300% auto;
  animation:gradientFlow 4s linear infinite;
}

/* ─── TICKER ─── */
.ticker-wrap {
  overflow:hidden; white-space:nowrap;
  background:linear-gradient(90deg,#eef2fc,#f2eeff,#eef6fc);
  background-size:200% auto; animation:gradientFlow 6s linear infinite;
  border:1px solid var(--border); border-radius:10px;
  padding:.5rem 0; margin-bottom:1.3rem;
}
.ticker-inner { display:inline-block; animation:ticker 28s linear infinite; }
.ticker-item { display:inline-block; padding:0 2.8rem; font-size:.8rem; font-weight:600; color:var(--text2); }
.ticker-item span { color:var(--accent); font-family:'Space Grotesk',sans-serif; font-weight:700; }

/* ─── FEATURE CARDS (Home) ─── */
.feat-grid { display:grid; grid-template-columns:repeat(4,1fr); gap:1rem; margin-bottom:1.4rem; }
.feat-card {
  background:var(--surf); border:1px solid var(--border); border-radius:14px;
  padding:1.6rem 1.2rem; text-align:center;
  box-shadow:var(--sh);
  transition:all .32s cubic-bezier(.22,.68,0,1.2);
  position:relative; overflow:hidden;
  animation:fadeSlideUp .5s ease both;
}
.feat-card::after {
  content:''; position:absolute; inset:0;
  background:linear-gradient(135deg,rgba(52,100,200,.04),rgba(107,63,202,.04));
  opacity:0; transition:opacity .3s ease;
}
.feat-card:hover { transform:translateY(-8px) scale(1.02); box-shadow:var(--sh2); }
.feat-card:hover::after { opacity:1; }
.feat-icon {
  font-size:2.2rem; margin-bottom:.6rem; display:block;
  animation:float 3.2s ease-in-out infinite;
}
.feat-card:nth-child(2) .feat-icon { animation-delay:.3s; }
.feat-card:nth-child(3) .feat-icon { animation-delay:.6s; }
.feat-card:nth-child(4) .feat-icon { animation-delay:.9s; }
.feat-title {
  font-family:'Space Grotesk',sans-serif; font-weight:700; font-size:.9rem;
  color:var(--text); margin-bottom:.35rem;
}
.feat-desc { font-size:.76rem; color:var(--text3); line-height:1.6; }

/* ─── STAT COUNTERS (Home) ─── */
.stat-row { display:grid; grid-template-columns:repeat(4,1fr); gap:.8rem; margin-bottom:1.4rem; }
.stat-box {
  background:linear-gradient(135deg,var(--accent),var(--purple));
  border-radius:12px; padding:1.1rem 1rem; text-align:center;
  box-shadow:0 4px 16px rgba(52,100,200,.25);
  animation:popIn .6s ease both;
}
.stat-box:nth-child(2) { background:linear-gradient(135deg,var(--purple),var(--teal)); animation-delay:.1s; }
.stat-box:nth-child(3) { background:linear-gradient(135deg,var(--teal),var(--green)); animation-delay:.2s; }
.stat-box:nth-child(4) { background:linear-gradient(135deg,var(--gold),var(--orange)); animation-delay:.3s; }
.stat-num {
  font-family:'Space Grotesk',sans-serif; font-size:1.6rem; font-weight:800;
  color:#fff; animation:countUp .8s cubic-bezier(.22,.68,0,1.2) .4s both;
}
.stat-lbl { font-size:.72rem; color:rgba(255,255,255,.82); font-weight:600; margin-top:.15rem; }

/* ─── STEP BAR ─── */
.step-row {
  display:flex; margin-bottom:1.8rem;
  background:var(--surf); border:1px solid var(--border);
  border-radius:var(--r); overflow:hidden; box-shadow:var(--sh);
  animation:fadeSlideUp .45s ease .05s both;
}
.step-item {
  flex:1; padding:.9rem; text-align:center;
  font-size:.73rem; font-weight:600; color:var(--text3);
  border-right:1px solid var(--border);
  transition:background .4s ease, color .3s ease;
}
.step-item:last-child { border-right:none; }
.step-item.active {
  background:linear-gradient(135deg,#eef2fc,#e8f0ff);
  color:var(--accent);
  animation:pulseRing 2.5s ease-in-out infinite;
}
.step-item.done { background:#e8f5ee; color:var(--green); }
.step-item.done .step-num { animation:starSpin .5s ease both; }
.step-num {
  display:block; font-size:1.15rem;
  font-family:'Space Grotesk',sans-serif; font-weight:800; margin-bottom:1px;
}

/* ─── FORM BOX ─── */
.form-box {
  background:var(--surf); border:1px solid var(--border);
  border-radius:var(--r); padding:1.8rem 2rem; margin-bottom:1.2rem;
  box-shadow:var(--sh);
  animation:fadeSlideUp .5s cubic-bezier(.22,.68,0,1.2) both;
  transition:border-color .3s ease, box-shadow .3s ease;
  position:relative; overflow:hidden;
}
.form-box::before {
  content:''; position:absolute; top:0; left:0; right:0; height:3px;
  background:linear-gradient(90deg,var(--accent),var(--purple));
  animation:borderTrail .8s ease .2s both;
}
.form-box:focus-within { border-color:var(--a2); box-shadow:0 4px 20px rgba(52,100,200,.12); }
.form-box h3 {
  font-family:'Space Grotesk',sans-serif; font-size:1rem; font-weight:700;
  color:var(--accent); margin:0 0 1.2rem;
  animation:fadeSlideLeft .5s ease both;
}

/* ─── SECTION TITLE ─── */
.sec {
  font-family:'Space Grotesk',sans-serif; font-size:.94rem; font-weight:700;
  color:var(--text); margin:1.6rem 0 .75rem;
  padding-bottom:.35rem; border-bottom:2px solid var(--border);
  animation:fadeSlideLeft .4s ease both;
  position:relative;
}
.sec::after {
  content:''; position:absolute; bottom:-2px; left:0;
  height:2px; background:linear-gradient(90deg,var(--accent),var(--a2));
  animation:typeBar .7s ease .2s both;
}

/* ─── CARDS ─── */
.card {
  background:var(--surf); border:1px solid var(--border);
  border-radius:var(--r); padding:1.2rem 1.4rem; box-shadow:var(--sh);
  transition:transform .28s ease, box-shadow .28s ease;
  animation:fadeSlideUp .5s ease both;
}
.card:hover { transform:translateY(-4px); box-shadow:var(--sh2); }
.kpi-lbl {
  font-size:.67rem; font-weight:700; text-transform:uppercase;
  letter-spacing:.1em; color:var(--text3); margin-bottom:.3rem;
}
.kpi-val {
  font-family:'Space Grotesk',sans-serif;
  font-size:1.9rem; font-weight:800; line-height:1;
  animation:countUp .6s cubic-bezier(.22,.68,0,1.2) .2s both;
}
.kpi-sub { font-size:.71rem; color:var(--text3); margin-top:.2rem; }

/* Color tokens */
.c-gold   { color:var(--gold)!important; }
.c-green  { color:var(--green)!important; }
.c-red    { color:var(--red)!important; }
.c-orange { color:var(--orange)!important; }
.c-blue   { color:var(--a2)!important; }
.c-purple { color:var(--purple)!important; }
.c-teal   { color:var(--teal)!important; }

/* ─── ALERTS ─── */
.al {
  border-radius:var(--r); padding:1rem 1.3rem; margin-bottom:.9rem;
  border-left:4px solid; font-size:.86rem; line-height:1.75; color:var(--text2);
  box-shadow:var(--sh);
  animation:fadeSlideRight .45s cubic-bezier(.22,.68,0,1.2) both;
  transition:transform .22s ease, box-shadow .22s ease;
}
.al:hover { transform:translateX(5px); box-shadow:var(--sh2); }
.al h4 { margin:0 0 .4rem; font-size:.9rem; font-weight:700; }
.al ul { margin:.35rem 0 0; padding-left:1.3rem; }
.al li { margin-bottom:.22rem; }
.al strong { color:var(--text); }
.al-s { background:#edfbf3; border-color:var(--green); } .al-s h4 { color:var(--green); }
.al-w { background:#fff7ee; border-color:var(--orange); } .al-w h4 { color:var(--orange); }
.al-d { background:#fff0f0; border-color:var(--red); }   .al-d h4 { color:var(--red); }
.al-i { background:#eef2fc; border-color:var(--accent); } .al-i h4 { color:var(--accent); }
.al-p { background:#f3eeff; border-color:var(--purple); } .al-p h4 { color:var(--purple); }

/* ─── PROGRESS BARS ─── */
.prog-wrap { margin-bottom:.75rem; }
.prog-lbl { display:flex; justify-content:space-between; font-size:.79rem; font-weight:600; color:var(--text2); margin-bottom:5px; }
.prog-bg { background:var(--surf2); border-radius:99px; height:10px; overflow:hidden; border:1px solid var(--border); }
.prog-fill {
  height:100%; border-radius:99px;
  animation:progressGrow .9s cubic-bezier(.22,.68,0,1.2) .3s both;
  position:relative; overflow:hidden;
}
.prog-fill::after {
  content:''; position:absolute; inset:0;
  background:linear-gradient(90deg,transparent 0%,rgba(255,255,255,.45) 50%,transparent 100%);
  background-size:200% 100%;
  animation:shimmer 2s ease 1.4s infinite;
}

/* ─── BOBOT CHIP ─── */
.bobot-chip {
  display:inline-flex; flex-direction:column; align-items:center;
  background:#eef2fc; border:1px solid #b8cff0;
  border-radius:8px; padding:.4rem .65rem; margin:.12rem;
  transition:transform .22s ease, background .22s ease;
  animation:popIn .5s ease both;
}
.bobot-chip:hover { transform:scale(1.12) translateY(-2px); background:#dde8f8; }
.bobot-chip .sk { font-size:.62rem; color:var(--text3); margin-bottom:2px; }
.bobot-chip .bv {
  font-size:.96rem; font-weight:800; color:var(--accent);
  font-family:'Space Grotesk',sans-serif;
}

/* ─── WEEK CARD ─── */
.week-card {
  background:var(--surf); border:1px solid var(--border);
  border-radius:12px; padding:1rem 1.2rem; margin-bottom:.65rem;
  box-shadow:var(--sh);
  transition:transform .25s ease, border-color .25s ease, box-shadow .25s ease;
  animation:fadeSlideUp .5s ease both;
  border-left:4px solid transparent;
}
.week-card:hover { transform:translateX(8px); border-left-color:var(--accent); box-shadow:var(--sh2); }
.week-num {
  font-family:'Space Grotesk',sans-serif; font-size:.72rem; font-weight:700;
  color:var(--accent); text-transform:uppercase; letter-spacing:.1em; margin-bottom:.28rem;
}
.week-target { font-size:.84rem; font-weight:700; color:var(--text); margin-bottom:.24rem; }
.week-tasks { font-size:.79rem; color:var(--text2); line-height:1.68; }

/* ─── STATUS BADGE ─── */
.status-badge {
  display:inline-flex; align-items:center; gap:.45rem;
  padding:.42rem 1.1rem; border-radius:99px;
  font-size:.78rem; font-weight:700;
  animation:popIn .6s ease both;
}
.sbg-sa { background:#e6f5ee; color:#148a42; border:1.5px solid #9adbb8; }
.sbg-a  { background:#edf6ff; color:#1a5fa0; border:1.5px solid #90c0f0; }
.sbg-k  { background:#fff4e6; color:#d4620a; border:1.5px solid #f4c08a; }
.sbg-r  { background:#fff0f0; color:#c0392b; border:1.5px solid #f4a0a0; }
.sb-dot {
  width:8px; height:8px; border-radius:50%; display:inline-block;
  animation:pulseRing 1.8s ease-in-out infinite;
}
.sbg-sa .sb-dot { background:#148a42; }
.sbg-a  .sb-dot { background:#1a5fa0; }
.sbg-k  .sb-dot { background:#d4620a; }
.sbg-r  .sb-dot { background:#c0392b; }

/* ─── SCORE RING ─── */
.score-ring-wrap { display:flex; justify-content:center; padding:1rem 0; }
.score-ring {
  width:148px; height:148px; border-radius:50%;
  background:conic-gradient(var(--accent) var(--pct,0%), #e8eef8 var(--pct,0%));
  display:flex; flex-direction:column; align-items:center; justify-content:center;
  position:relative; animation:popIn .8s cubic-bezier(.22,.68,0,1.2) .1s both;
  box-shadow:0 4px 24px rgba(52,100,200,.2);
}
.score-ring::before {
  content:''; position:absolute; inset:13px; border-radius:50%;
  background:var(--surf); box-shadow:inset 0 2px 10px rgba(52,100,200,.08);
}
.score-ring-val {
  position:relative; z-index:1;
  font-family:'Space Grotesk',sans-serif; font-size:1.65rem; font-weight:800;
  color:var(--accent); animation:countUp .9s ease .5s both;
}
.score-ring-sub { position:relative; z-index:1; font-size:.62rem; color:var(--text3); }

/* ─── STREAMLIT OVERRIDES ─── */
div[data-testid="stButton"] button[kind="primary"] {
  background:linear-gradient(135deg,var(--accent),#1a3470) !important;
  color:#fff !important; font-weight:700 !important;
  font-family:'Space Grotesk',sans-serif !important;
  border:none !important; border-radius:10px !important;
  font-size:.89rem !important; letter-spacing:.02em !important;
  transition:all .28s cubic-bezier(.22,.68,0,1.2) !important;
  position:relative !important; overflow:hidden !important;
}
div[data-testid="stButton"] button[kind="primary"]:hover {
  transform:translateY(-3px) scale(1.02) !important;
  box-shadow:0 8px 28px rgba(52,100,200,.4) !important;
}
div[data-testid="stButton"] button {
  background:var(--surf) !important; color:var(--text2) !important;
  border:1px solid var(--border) !important; border-radius:10px !important;
  font-weight:600 !important; transition:all .22s ease !important;
}
div[data-testid="stButton"] button:hover {
  border-color:var(--a2) !important; color:var(--accent) !important;
  transform:translateY(-2px) !important;
  box-shadow:0 4px 14px rgba(52,100,200,.15) !important;
}
div[data-testid="stTabs"] button[data-baseweb="tab"] {
  font-family:'Space Grotesk',sans-serif !important; font-weight:700 !important;
  font-size:.79rem !important; color:var(--text3) !important;
  transition:color .2s ease !important;
}
div[data-testid="stTabs"] button[aria-selected="true"] {
  color:var(--accent) !important; border-bottom-color:var(--accent) !important;
}
div[data-testid="stMetric"] {
  background:var(--surf) !important; border:1px solid var(--border) !important;
  border-radius:var(--r) !important; padding:1.1rem 1.3rem !important;
  box-shadow:var(--sh) !important; animation:fadeSlideUp .5s ease both !important;
  transition:transform .28s ease, box-shadow .28s ease !important;
}
div[data-testid="stMetric"]:hover {
  transform:translateY(-4px) !important; box-shadow:var(--sh2) !important;
}
div[data-testid="stMetric"] label {
  color:var(--text3) !important; font-size:.7rem !important;
  font-weight:700 !important; text-transform:uppercase !important; letter-spacing:.08em !important;
}
div[data-testid="stMetric"] [data-testid="stMetricValue"] {
  color:var(--text) !important; font-family:'Space Grotesk',sans-serif !important;
  animation:countUp .6s ease both !important;
}
div[data-testid="stExpander"] {
  background:var(--surf) !important; border:1px solid var(--border) !important;
  border-radius:var(--r) !important; box-shadow:var(--sh) !important;
  animation:fadeSlideUp .45s ease both !important;
  transition:border-color .3s ease !important;
}
div[data-testid="stExpander"]:hover { border-color:var(--a2) !important; }
div[data-testid="stExpander"] summary { color:var(--text2) !important; font-weight:700 !important; }
div[data-testid="stNumberInput"] label,div[data-testid="stSelectbox"] label,
div[data-testid="stTextInput"] label,div[data-testid="stRadio"] label {
  color:var(--text2) !important; font-weight:700 !important; font-size:.83rem !important;
}
div[data-testid="stNumberInput"] input,div[data-testid="stTextInput"] input {
  background:var(--surf) !important; color:var(--text) !important;
  border-color:var(--border) !important; font-size:.9rem !important;
  transition:border-color .25s ease, box-shadow .25s ease !important; border-radius:8px !important;
}
div[data-testid="stNumberInput"] input:focus,div[data-testid="stTextInput"] input:focus {
  border-color:var(--a2) !important; box-shadow:0 0 0 3px rgba(52,100,200,.14) !important;
}
.stCaption,[data-testid="stCaptionContainer"],.stCaption p { color:var(--text3) !important; font-size:.76rem !important; }
hr { border-color:var(--border) !important; margin:1.2rem 0 !important; }
div[data-testid="stDataFrame"] { border-radius:12px; overflow:hidden; box-shadow:var(--sh); animation:fadeSlideUp .5s ease both; }
div[data-baseweb="select"] { background:var(--surf) !important; }
div[data-baseweb="select"] * { color:var(--text) !important; }
div[data-testid="stSlider"] label { color:var(--text2) !important; font-weight:700 !important; font-size:.83rem !important; }
table { border-collapse:collapse; width:100%; font-size:.84rem; }
th { background:#eef2fc; color:var(--text); padding:.55rem .9rem; border:1px solid var(--border); font-weight:700; text-align:left; }
td { padding:.5rem .9rem; border:1px solid var(--border); color:var(--text2); transition:background .15s ease; }
tr:nth-child(even) td { background:#f8faff; }
tr:hover td { background:#eef2fc !important; }

/* stagger helpers */
.d1{animation-delay:.05s!important} .d2{animation-delay:.10s!important}
.d3{animation-delay:.15s!important} .d4{animation-delay:.20s!important}
.d5{animation-delay:.25s!important} .d6{animation-delay:.30s!important}
.d7{animation-delay:.35s!important} .d8{animation-delay:.40s!important}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# SESSION STATE
# ══════════════════════════════════════════════════════════
DEFAULTS = {
    'page': 'home', 'step': 1,
    'data': {}, 'result': None,
    '_cid': 0,
}
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

def ckey(prefix="c"):
    st.session_state._cid += 1
    return f"{prefix}_{st.session_state._cid}"


# ══════════════════════════════════════════════════════════
# KONSTANTA
# ══════════════════════════════════════════════════════════
SKOR_MIN_TPS = 200
SKOR_MAX_TPS = 1000

SUBTES = ["PU", "PPU", "PBM", "PK", "LBI", "LBE", "PM"]
SUBTES_FULL = {
    "PU":  "Penalaran Umum",
    "PPU": "Pem. & Pengetahuan Umum",
    "PBM": "Pemahaman Bacaan & Menulis",
    "PK":  "Pengetahuan Kuantitatif",
    "LBI": "Literasi Bahasa Indonesia",
    "LBE": "Literasi Bahasa Inggris",
    "PM":  "Penalaran Matematika",
}
SUBTES_CLR = {
    "PU": "#c8890a", "PPU": "#3b6cb7", "PBM": "#7048c8",
    "PK": "#c0392b", "LBI": "#1a8a4a", "LBE": "#0d8a80", "PM": "#d4620a",
}

DAFTAR_JENJANG = ["S1 (Sarjana)", "D3 (Diploma Tiga)"]

DAFTAR_JURUSAN_S1 = [
    "Kedokteran","Kedokteran Gigi",
    "Teknik Sipil","Teknik Mesin","Teknik Elektro","Teknik Industri","Teknik Kimia","Teknik Informatika",
    "Matematika","Fisika","Kimia","Biologi","Statistika","Aktuaria",
    "Farmasi","Gizi","Keperawatan","Kesehatan Masyarakat",
    "Ilmu Hukum","Ekonomi","Manajemen","Akuntansi","Bisnis",
    "Psikologi","Ilmu Komunikasi","Hubungan Internasional","Administrasi Publik",
    "Sastra Inggris","Pendidikan Bahasa Indonesia","Pendidikan Bahasa Inggris",
    "Sosiologi","Ilmu Politik","Sejarah","Geografi"
]

DAFTAR_JURUSAN_D3 = [
    "D3 Teknik Sipil","D3 Teknik Mesin","D3 Teknik Elektro","D3 Teknik Kimia",
    "D3 Teknik Komputer","D3 Teknologi Informasi","D3 Teknik Mekatronika",
    "D3 Manajemen","D3 Akuntansi","D3 Administrasi Bisnis","D3 Perbankan & Keuangan",
    "D3 Manajemen Pemasaran","D3 Perpajakan",
    "D3 Keperawatan","D3 Kebidanan","D3 Farmasi","D3 Gizi","D3 Analis Kesehatan",
    "D3 Rekam Medis","D3 Fisioterapi","D3 Radiologi",
    "D3 Komunikasi","D3 Hubungan Masyarakat","D3 Desain Grafis","D3 Animasi",
    "D3 Pariwisata","D3 Perhotelan","D3 Bahasa Inggris",
    "D3 Agribisnis","D3 Teknologi Pangan",
]

DAFTAR_JURUSAN = DAFTAR_JURUSAN_S1

def get_daftar_jurusan(jenjang):
    if "D3" in jenjang:
        return DAFTAR_JURUSAN_D3
    return DAFTAR_JURUSAN_S1

BOBOT_MAP = {
    "Kedokteran":             {"PU":.20,"PPU":.15,"PBM":.10,"PK":.15,"LBI":.10,"LBE":.10,"PM":.20},
    "Kedokteran Gigi":        {"PU":.20,"PPU":.15,"PBM":.10,"PK":.15,"LBI":.10,"LBE":.10,"PM":.20},
    "Teknik Informatika":     {"PU":.20,"PPU":.05,"PBM":.05,"PK":.20,"LBI":.05,"LBE":.10,"PM":.35},
    "Teknik Sipil":           {"PU":.20,"PPU":.05,"PBM":.05,"PK":.20,"LBI":.05,"LBE":.10,"PM":.35},
    "Teknik Mesin":           {"PU":.20,"PPU":.05,"PBM":.05,"PK":.20,"LBI":.05,"LBE":.10,"PM":.35},
    "Teknik Elektro":         {"PU":.20,"PPU":.05,"PBM":.05,"PK":.20,"LBI":.05,"LBE":.10,"PM":.35},
    "Teknik Industri":        {"PU":.20,"PPU":.05,"PBM":.05,"PK":.20,"LBI":.05,"LBE":.10,"PM":.35},
    "Teknik Kimia":           {"PU":.18,"PPU":.08,"PBM":.05,"PK":.20,"LBI":.05,"LBE":.07,"PM":.37},
    "Matematika":             {"PU":.15,"PPU":.05,"PBM":.05,"PK":.20,"LBI":.05,"LBE":.05,"PM":.45},
    "Fisika":                 {"PU":.18,"PPU":.07,"PBM":.05,"PK":.20,"LBI":.05,"LBE":.05,"PM":.40},
    "Kimia":                  {"PU":.18,"PPU":.10,"PBM":.07,"PK":.18,"LBI":.07,"LBE":.05,"PM":.35},
    "Biologi":                {"PU":.20,"PPU":.15,"PBM":.10,"PK":.15,"LBI":.10,"LBE":.08,"PM":.22},
    "Statistika":             {"PU":.15,"PPU":.07,"PBM":.05,"PK":.20,"LBI":.05,"LBE":.05,"PM":.43},
    "Aktuaria":               {"PU":.15,"PPU":.07,"PBM":.05,"PK":.20,"LBI":.05,"LBE":.05,"PM":.43},
    "Farmasi":                {"PU":.18,"PPU":.12,"PBM":.08,"PK":.18,"LBI":.08,"LBE":.08,"PM":.28},
    "Gizi":                   {"PU":.18,"PPU":.12,"PBM":.10,"PK":.15,"LBI":.12,"LBE":.08,"PM":.25},
    "Keperawatan":            {"PU":.18,"PPU":.12,"PBM":.12,"PK":.12,"LBI":.15,"LBE":.08,"PM":.23},
    "Kesehatan Masyarakat":   {"PU":.20,"PPU":.12,"PBM":.12,"PK":.12,"LBI":.15,"LBE":.08,"PM":.21},
    "Ilmu Hukum":             {"PU":.22,"PPU":.18,"PBM":.20,"PK":.08,"LBI":.18,"LBE":.10,"PM":.04},
    "Ekonomi":                {"PU":.20,"PPU":.15,"PBM":.10,"PK":.20,"LBI":.10,"LBE":.10,"PM":.15},
    "Manajemen":              {"PU":.20,"PPU":.15,"PBM":.12,"PK":.18,"LBI":.12,"LBE":.10,"PM":.13},
    "Akuntansi":              {"PU":.18,"PPU":.15,"PBM":.10,"PK":.22,"LBI":.10,"LBE":.10,"PM":.15},
    "Bisnis":                 {"PU":.20,"PPU":.15,"PBM":.12,"PK":.18,"LBI":.12,"LBE":.10,"PM":.13},
    "Psikologi":              {"PU":.22,"PPU":.15,"PBM":.18,"PK":.10,"LBI":.18,"LBE":.10,"PM":.07},
    "Ilmu Komunikasi":        {"PU":.20,"PPU":.15,"PBM":.22,"PK":.08,"LBI":.20,"LBE":.10,"PM":.05},
    "Hubungan Internasional": {"PU":.20,"PPU":.15,"PBM":.15,"PK":.08,"LBI":.17,"LBE":.20,"PM":.05},
    "Administrasi Publik":    {"PU":.22,"PPU":.15,"PBM":.18,"PK":.08,"LBI":.20,"LBE":.10,"PM":.07},
    "Sastra Inggris":         {"PU":.12,"PPU":.12,"PBM":.20,"PK":.05,"LBI":.15,"LBE":.31,"PM":.05},
    "Pendidikan Bahasa Indonesia": {"PU":.12,"PPU":.12,"PBM":.22,"PK":.05,"LBI":.32,"LBE":.12,"PM":.05},
    "Pendidikan Bahasa Inggris":   {"PU":.12,"PPU":.12,"PBM":.18,"PK":.05,"LBI":.12,"LBE":.33,"PM":.08},
    "Sosiologi":              {"PU":.22,"PPU":.17,"PBM":.18,"PK":.08,"LBI":.18,"LBE":.10,"PM":.07},
    "Ilmu Politik":           {"PU":.22,"PPU":.17,"PBM":.18,"PK":.08,"LBI":.18,"LBE":.10,"PM":.07},
    "Sejarah":                {"PU":.20,"PPU":.20,"PBM":.18,"PK":.05,"LBI":.22,"LBE":.10,"PM":.05},
    "Geografi":               {"PU":.20,"PPU":.15,"PBM":.15,"PK":.12,"LBI":.15,"LBE":.08,"PM":.15},
}
DEFAULT_BOBOT = {"PU":.15,"PPU":.15,"PBM":.15,"PK":.15,"LBI":.15,"LBE":.15,"PM":.10}

BOBOT_MAP_D3 = {
    "D3 Teknik Sipil":         {"PU":.18,"PPU":.05,"PBM":.05,"PK":.22,"LBI":.05,"LBE":.07,"PM":.38},
    "D3 Teknik Mesin":         {"PU":.18,"PPU":.05,"PBM":.05,"PK":.22,"LBI":.05,"LBE":.07,"PM":.38},
    "D3 Teknik Elektro":       {"PU":.18,"PPU":.05,"PBM":.05,"PK":.22,"LBI":.05,"LBE":.07,"PM":.38},
    "D3 Teknik Kimia":         {"PU":.17,"PPU":.08,"PBM":.05,"PK":.22,"LBI":.05,"LBE":.05,"PM":.38},
    "D3 Teknik Komputer":      {"PU":.18,"PPU":.05,"PBM":.05,"PK":.22,"LBI":.05,"LBE":.08,"PM":.37},
    "D3 Teknologi Informasi":  {"PU":.18,"PPU":.05,"PBM":.05,"PK":.22,"LBI":.05,"LBE":.08,"PM":.37},
    "D3 Teknik Mekatronika":   {"PU":.18,"PPU":.05,"PBM":.05,"PK":.22,"LBI":.05,"LBE":.07,"PM":.38},
    "D3 Manajemen":            {"PU":.20,"PPU":.15,"PBM":.15,"PK":.18,"LBI":.15,"LBE":.10,"PM":.07},
    "D3 Akuntansi":            {"PU":.18,"PPU":.13,"PBM":.12,"PK":.25,"LBI":.12,"LBE":.08,"PM":.12},
    "D3 Administrasi Bisnis":  {"PU":.20,"PPU":.15,"PBM":.18,"PK":.12,"LBI":.18,"LBE":.10,"PM":.07},
    "D3 Perbankan & Keuangan": {"PU":.18,"PPU":.13,"PBM":.12,"PK":.25,"LBI":.12,"LBE":.08,"PM":.12},
    "D3 Manajemen Pemasaran":  {"PU":.20,"PPU":.15,"PBM":.17,"PK":.12,"LBI":.18,"LBE":.12,"PM":.06},
    "D3 Perpajakan":           {"PU":.18,"PPU":.12,"PBM":.12,"PK":.25,"LBI":.13,"LBE":.08,"PM":.12},
    "D3 Keperawatan":          {"PU":.18,"PPU":.13,"PBM":.13,"PK":.12,"LBI":.17,"LBE":.08,"PM":.19},
    "D3 Kebidanan":            {"PU":.18,"PPU":.14,"PBM":.13,"PK":.12,"LBI":.17,"LBE":.08,"PM":.18},
    "D3 Farmasi":              {"PU":.17,"PPU":.13,"PBM":.08,"PK":.18,"LBI":.10,"LBE":.08,"PM":.26},
    "D3 Gizi":                 {"PU":.18,"PPU":.13,"PBM":.10,"PK":.15,"LBI":.13,"LBE":.08,"PM":.23},
    "D3 Analis Kesehatan":     {"PU":.18,"PPU":.13,"PBM":.08,"PK":.18,"LBI":.10,"LBE":.07,"PM":.26},
    "D3 Rekam Medis":          {"PU":.18,"PPU":.12,"PBM":.14,"PK":.15,"LBI":.16,"LBE":.08,"PM":.17},
    "D3 Fisioterapi":          {"PU":.19,"PPU":.13,"PBM":.12,"PK":.13,"LBI":.15,"LBE":.08,"PM":.20},
    "D3 Radiologi":            {"PU":.18,"PPU":.12,"PBM":.08,"PK":.20,"LBI":.10,"LBE":.07,"PM":.25},
    "D3 Komunikasi":           {"PU":.20,"PPU":.15,"PBM":.22,"PK":.08,"LBI":.20,"LBE":.10,"PM":.05},
    "D3 Hubungan Masyarakat":  {"PU":.20,"PPU":.15,"PBM":.22,"PK":.07,"LBI":.22,"LBE":.10,"PM":.04},
    "D3 Desain Grafis":        {"PU":.18,"PPU":.10,"PBM":.18,"PK":.12,"LBI":.18,"LBE":.12,"PM":.12},
    "D3 Animasi":              {"PU":.18,"PPU":.10,"PBM":.15,"PK":.15,"LBI":.17,"LBE":.12,"PM":.13},
    "D3 Pariwisata":           {"PU":.18,"PPU":.13,"PBM":.18,"PK":.08,"LBI":.18,"LBE":.18,"PM":.07},
    "D3 Perhotelan":           {"PU":.18,"PPU":.12,"PBM":.17,"PK":.08,"LBI":.18,"LBE":.20,"PM":.07},
    "D3 Bahasa Inggris":       {"PU":.13,"PPU":.12,"PBM":.18,"PK":.05,"LBI":.15,"LBE":.33,"PM":.04},
    "D3 Agribisnis":           {"PU":.20,"PPU":.15,"PBM":.12,"PK":.15,"LBI":.15,"LBE":.08,"PM":.15},
    "D3 Teknologi Pangan":     {"PU":.18,"PPU":.13,"PBM":.08,"PK":.18,"LBI":.10,"LBE":.07,"PM":.26},
}

DEFAULT_BOBOT_D3 = {"PU":.18,"PPU":.12,"PBM":.13,"PK":.15,"LBI":.15,"LBE":.10,"PM":.17}

def get_bobot(j):
    if j in BOBOT_MAP_D3:
        return BOBOT_MAP_D3[j]
    return BOBOT_MAP.get(j, DEFAULT_BOBOT)

# ══════════════════════════════════════════════════════════
# PTN DATA — 30 PTN | S1 Skor aman per jurusan
# Sumber: UTBK_SNBT_Estimasi_30PTN.xlsx (SNPMB/BPPP Kemdikbud 2025/2026)
# ══════════════════════════════════════════════════════════
PTN_JURUSAN_DATA = {
    "Universitas Indonesia (UI)": {
        "_klaster": 1,
        "_lbl": '⭐ Klaster 1 — Top Tier',
        "Kedokteran": {"mn": 805, "mx": 840},
        "Kedokteran Gigi": {"mn": 753, "mx": 788},
        "Teknik Sipil": {"mn": 755, "mx": 790},
        "Teknik Mesin": {"mn": 760, "mx": 795},
        "Teknik Elektro": {"mn": 775, "mx": 810},
        "Teknik Industri": {"mn": 743, "mx": 778},
        "Teknik Kimia": {"mn": 765, "mx": 800},
        "Teknik Informatika": {"mn": 795, "mx": 830},
        "Matematika": {"mn": 733, "mx": 768},
        "Fisika": {"mn": 727, "mx": 762},
        "Kimia": {"mn": 723, "mx": 758},
        "Biologi": {"mn": 720, "mx": 755},
        "Statistika": {"mn": 737, "mx": 772},
        "Aktuaria": {"mn": 740, "mx": 775},
        "Farmasi": {"mn": 780, "mx": 815},
        "Gizi": {"mn": 703, "mx": 738},
        "Keperawatan": {"mn": 697, "mx": 732},
        "Kesehatan Masyarakat": {"mn": 689, "mx": 724},
        "Ilmu Hukum": {"mn": 775, "mx": 810},
        "Ekonomi": {"mn": 753, "mx": 788},
        "Manajemen": {"mn": 763, "mx": 798},
        "Akuntansi": {"mn": 770, "mx": 805},
        "Bisnis": {"mn": 745, "mx": 780},
        "Psikologi": {"mn": 785, "mx": 820},
        "Ilmu Komunikasi": {"mn": 760, "mx": 795},
        "Hubungan Internasional": {"mn": 750, "mx": 785},
        "Administrasi Publik": {"mn": 667, "mx": 702},
        "Sastra Inggris": {"mn": 707, "mx": 742},
        "Pendidikan Bahasa Indonesia": {"mn": 700, "mx": 735},
        "Pendidikan Bahasa Inggris": {"mn": 697, "mx": 732},
        "Sosiologi": {"mn": 733, "mx": 768},
        "Ilmu Politik": {"mn": 740, "mx": 775},
        "Sejarah": {"mn": 710, "mx": 745},
        "Geografi": {"mn": 728, "mx": 763},
        "_default": {"mn": 740, "mx": 775},
    },
    "Universitas Gadjah Mada (UGM)": {
        "_klaster": 1,
        "_lbl": '⭐ Klaster 1 — Top Tier',
        "Kedokteran": {"mn": 805, "mx": 840},
        "Kedokteran Gigi": {"mn": 753, "mx": 788},
        "Teknik Sipil": {"mn": 755, "mx": 790},
        "Teknik Mesin": {"mn": 760, "mx": 795},
        "Teknik Elektro": {"mn": 775, "mx": 810},
        "Teknik Industri": {"mn": 743, "mx": 778},
        "Teknik Kimia": {"mn": 765, "mx": 800},
        "Teknik Informatika": {"mn": 795, "mx": 830},
        "Matematika": {"mn": 733, "mx": 768},
        "Fisika": {"mn": 727, "mx": 762},
        "Kimia": {"mn": 723, "mx": 758},
        "Biologi": {"mn": 720, "mx": 755},
        "Statistika": {"mn": 737, "mx": 772},
        "Aktuaria": {"mn": 740, "mx": 775},
        "Farmasi": {"mn": 780, "mx": 815},
        "Gizi": {"mn": 703, "mx": 738},
        "Keperawatan": {"mn": 697, "mx": 732},
        "Kesehatan Masyarakat": {"mn": 689, "mx": 724},
        "Ilmu Hukum": {"mn": 775, "mx": 810},
        "Ekonomi": {"mn": 753, "mx": 788},
        "Manajemen": {"mn": 763, "mx": 798},
        "Akuntansi": {"mn": 770, "mx": 805},
        "Bisnis": {"mn": 745, "mx": 780},
        "Psikologi": {"mn": 785, "mx": 820},
        "Ilmu Komunikasi": {"mn": 760, "mx": 795},
        "Hubungan Internasional": {"mn": 750, "mx": 785},
        "Administrasi Publik": {"mn": 667, "mx": 702},
        "Sastra Inggris": {"mn": 707, "mx": 742},
        "Pendidikan Bahasa Indonesia": {"mn": 700, "mx": 735},
        "Pendidikan Bahasa Inggris": {"mn": 697, "mx": 732},
        "Sosiologi": {"mn": 733, "mx": 768},
        "Ilmu Politik": {"mn": 740, "mx": 775},
        "Sejarah": {"mn": 710, "mx": 745},
        "Geografi": {"mn": 728, "mx": 763},
        "_default": {"mn": 740, "mx": 775},
    },
    "Universitas Airlangga (Unair)": {
        "_klaster": 2,
        "_lbl": '🔷 Klaster 2 — Menengah Atas',
        "Kedokteran": {"mn": 780, "mx": 815},
        "Kedokteran Gigi": {"mn": 730, "mx": 765},
        "Teknik Sipil": {"mn": 732, "mx": 767},
        "Teknik Mesin": {"mn": 737, "mx": 772},
        "Teknik Elektro": {"mn": 751, "mx": 786},
        "Teknik Industri": {"mn": 720, "mx": 755},
        "Teknik Kimia": {"mn": 742, "mx": 777},
        "Teknik Informatika": {"mn": 771, "mx": 806},
        "Matematika": {"mn": 711, "mx": 746},
        "Fisika": {"mn": 705, "mx": 740},
        "Kimia": {"mn": 701, "mx": 736},
        "Biologi": {"mn": 698, "mx": 733},
        "Statistika": {"mn": 714, "mx": 749},
        "Aktuaria": {"mn": 717, "mx": 752},
        "Farmasi": {"mn": 756, "mx": 791},
        "Gizi": {"mn": 681, "mx": 716},
        "Keperawatan": {"mn": 676, "mx": 711},
        "Kesehatan Masyarakat": {"mn": 668, "mx": 703},
        "Ilmu Hukum": {"mn": 751, "mx": 786},
        "Ekonomi": {"mn": 730, "mx": 765},
        "Manajemen": {"mn": 740, "mx": 775},
        "Akuntansi": {"mn": 746, "mx": 781},
        "Bisnis": {"mn": 722, "mx": 757},
        "Psikologi": {"mn": 761, "mx": 796},
        "Ilmu Komunikasi": {"mn": 737, "mx": 772},
        "Hubungan Internasional": {"mn": 727, "mx": 762},
        "Administrasi Publik": {"mn": 647, "mx": 682},
        "Sastra Inggris": {"mn": 685, "mx": 720},
        "Pendidikan Bahasa Indonesia": {"mn": 679, "mx": 714},
        "Pendidikan Bahasa Inggris": {"mn": 676, "mx": 711},
        "Sosiologi": {"mn": 711, "mx": 746},
        "Ilmu Politik": {"mn": 717, "mx": 752},
        "Sejarah": {"mn": 688, "mx": 723},
        "Geografi": {"mn": 706, "mx": 741},
        "_default": {"mn": 718, "mx": 753},
    },
    "Institut Teknologi Bandung (ITB)": {
        "_klaster": 1,
        "_lbl": '⭐ Klaster 1 — Top Tier',
        "Kedokteran": {"mn": 805, "mx": 840},
        "Kedokteran Gigi": {"mn": 753, "mx": 788},
        "Teknik Sipil": {"mn": 755, "mx": 790},
        "Teknik Mesin": {"mn": 760, "mx": 795},
        "Teknik Elektro": {"mn": 775, "mx": 810},
        "Teknik Industri": {"mn": 743, "mx": 778},
        "Teknik Kimia": {"mn": 765, "mx": 800},
        "Teknik Informatika": {"mn": 795, "mx": 830},
        "Matematika": {"mn": 733, "mx": 768},
        "Fisika": {"mn": 727, "mx": 762},
        "Kimia": {"mn": 723, "mx": 758},
        "Biologi": {"mn": 720, "mx": 755},
        "Statistika": {"mn": 737, "mx": 772},
        "Aktuaria": {"mn": 740, "mx": 775},
        "Farmasi": {"mn": 780, "mx": 815},
        "Gizi": {"mn": 703, "mx": 738},
        "Keperawatan": {"mn": 697, "mx": 732},
        "Kesehatan Masyarakat": {"mn": 689, "mx": 724},
        "Ilmu Hukum": {"mn": 775, "mx": 810},
        "Ekonomi": {"mn": 753, "mx": 788},
        "Manajemen": {"mn": 763, "mx": 798},
        "Akuntansi": {"mn": 770, "mx": 805},
        "Bisnis": {"mn": 745, "mx": 780},
        "Psikologi": {"mn": 785, "mx": 820},
        "Ilmu Komunikasi": {"mn": 760, "mx": 795},
        "Hubungan Internasional": {"mn": 750, "mx": 785},
        "Administrasi Publik": {"mn": 667, "mx": 702},
        "Sastra Inggris": {"mn": 707, "mx": 742},
        "Pendidikan Bahasa Indonesia": {"mn": 700, "mx": 735},
        "Pendidikan Bahasa Inggris": {"mn": 697, "mx": 732},
        "Sosiologi": {"mn": 733, "mx": 768},
        "Ilmu Politik": {"mn": 740, "mx": 775},
        "Sejarah": {"mn": 710, "mx": 745},
        "Geografi": {"mn": 728, "mx": 763},
        "_default": {"mn": 740, "mx": 775},
    },
    "Universitas Padjadjaran (Unpad)": {
        "_klaster": 1,
        "_lbl": '⭐ Klaster 1 — Top Tier',
        "Kedokteran": {"mn": 748, "mx": 783},
        "Kedokteran Gigi": {"mn": 699, "mx": 734},
        "Teknik Sipil": {"mn": 701, "mx": 736},
        "Teknik Mesin": {"mn": 706, "mx": 741},
        "Teknik Elektro": {"mn": 720, "mx": 755},
        "Teknik Industri": {"mn": 690, "mx": 725},
        "Teknik Kimia": {"mn": 710, "mx": 745},
        "Teknik Informatika": {"mn": 738, "mx": 773},
        "Matematika": {"mn": 681, "mx": 716},
        "Fisika": {"mn": 675, "mx": 710},
        "Kimia": {"mn": 671, "mx": 706},
        "Biologi": {"mn": 669, "mx": 704},
        "Statistika": {"mn": 684, "mx": 719},
        "Aktuaria": {"mn": 687, "mx": 722},
        "Farmasi": {"mn": 724, "mx": 759},
        "Gizi": {"mn": 653, "mx": 688},
        "Keperawatan": {"mn": 647, "mx": 682},
        "Kesehatan Masyarakat": {"mn": 639, "mx": 674},
        "Ilmu Hukum": {"mn": 720, "mx": 755},
        "Ekonomi": {"mn": 699, "mx": 734},
        "Manajemen": {"mn": 709, "mx": 744},
        "Akuntansi": {"mn": 715, "mx": 750},
        "Bisnis": {"mn": 692, "mx": 727},
        "Psikologi": {"mn": 729, "mx": 764},
        "Ilmu Komunikasi": {"mn": 706, "mx": 741},
        "Hubungan Internasional": {"mn": 696, "mx": 731},
        "Administrasi Publik": {"mn": 619, "mx": 654},
        "Sastra Inggris": {"mn": 656, "mx": 691},
        "Pendidikan Bahasa Indonesia": {"mn": 650, "mx": 685},
        "Pendidikan Bahasa Inggris": {"mn": 647, "mx": 682},
        "Sosiologi": {"mn": 681, "mx": 716},
        "Ilmu Politik": {"mn": 687, "mx": 722},
        "Sejarah": {"mn": 659, "mx": 694},
        "Geografi": {"mn": 676, "mx": 711},
        "_default": {"mn": 687, "mx": 722},
    },
    "Institut Pertanian Bogor (IPB)": {
        "_klaster": 1,
        "_lbl": '⭐ Klaster 1 — Top Tier',
        "Kedokteran": {"mn": 731, "mx": 766},
        "Kedokteran Gigi": {"mn": 684, "mx": 719},
        "Teknik Sipil": {"mn": 686, "mx": 721},
        "Teknik Mesin": {"mn": 690, "mx": 725},
        "Teknik Elektro": {"mn": 704, "mx": 739},
        "Teknik Industri": {"mn": 675, "mx": 710},
        "Teknik Kimia": {"mn": 695, "mx": 730},
        "Teknik Informatika": {"mn": 722, "mx": 757},
        "Matematika": {"mn": 666, "mx": 701},
        "Fisika": {"mn": 660, "mx": 695},
        "Kimia": {"mn": 657, "mx": 692},
        "Biologi": {"mn": 654, "mx": 689},
        "Statistika": {"mn": 669, "mx": 704},
        "Aktuaria": {"mn": 672, "mx": 707},
        "Farmasi": {"mn": 708, "mx": 743},
        "Gizi": {"mn": 638, "mx": 673},
        "Keperawatan": {"mn": 633, "mx": 668},
        "Kesehatan Masyarakat": {"mn": 625, "mx": 660},
        "Ilmu Hukum": {"mn": 704, "mx": 739},
        "Ekonomi": {"mn": 684, "mx": 719},
        "Manajemen": {"mn": 693, "mx": 728},
        "Akuntansi": {"mn": 699, "mx": 734},
        "Bisnis": {"mn": 677, "mx": 712},
        "Psikologi": {"mn": 713, "mx": 748},
        "Ilmu Komunikasi": {"mn": 690, "mx": 725},
        "Hubungan Internasional": {"mn": 681, "mx": 716},
        "Administrasi Publik": {"mn": 606, "mx": 641},
        "Sastra Inggris": {"mn": 642, "mx": 677},
        "Pendidikan Bahasa Indonesia": {"mn": 636, "mx": 671},
        "Pendidikan Bahasa Inggris": {"mn": 633, "mx": 668},
        "Sosiologi": {"mn": 666, "mx": 701},
        "Ilmu Politik": {"mn": 672, "mx": 707},
        "Sejarah": {"mn": 645, "mx": 680},
        "Geografi": {"mn": 661, "mx": 696},
        "_default": {"mn": 672, "mx": 707},
    },
    "Institut Teknologi Sepuluh Nopember (ITS)": {
        "_klaster": 2,
        "_lbl": '🔷 Klaster 2 — Menengah Atas',
        "Kedokteran": {"mn": 739, "mx": 774},
        "Kedokteran Gigi": {"mn": 692, "mx": 727},
        "Teknik Sipil": {"mn": 693, "mx": 728},
        "Teknik Mesin": {"mn": 698, "mx": 733},
        "Teknik Elektro": {"mn": 712, "mx": 747},
        "Teknik Industri": {"mn": 682, "mx": 717},
        "Teknik Kimia": {"mn": 703, "mx": 738},
        "Teknik Informatika": {"mn": 730, "mx": 765},
        "Matematika": {"mn": 673, "mx": 708},
        "Fisika": {"mn": 668, "mx": 703},
        "Kimia": {"mn": 664, "mx": 699},
        "Biologi": {"mn": 661, "mx": 696},
        "Statistika": {"mn": 677, "mx": 712},
        "Aktuaria": {"mn": 680, "mx": 715},
        "Farmasi": {"mn": 716, "mx": 751},
        "Gizi": {"mn": 646, "mx": 681},
        "Keperawatan": {"mn": 640, "mx": 675},
        "Kesehatan Masyarakat": {"mn": 632, "mx": 667},
        "Ilmu Hukum": {"mn": 712, "mx": 747},
        "Ekonomi": {"mn": 692, "mx": 727},
        "Manajemen": {"mn": 701, "mx": 736},
        "Akuntansi": {"mn": 707, "mx": 742},
        "Bisnis": {"mn": 684, "mx": 719},
        "Psikologi": {"mn": 721, "mx": 756},
        "Ilmu Komunikasi": {"mn": 698, "mx": 733},
        "Hubungan Internasional": {"mn": 689, "mx": 724},
        "Administrasi Publik": {"mn": 612, "mx": 647},
        "Sastra Inggris": {"mn": 649, "mx": 684},
        "Pendidikan Bahasa Indonesia": {"mn": 643, "mx": 678},
        "Pendidikan Bahasa Inggris": {"mn": 640, "mx": 675},
        "Sosiologi": {"mn": 673, "mx": 708},
        "Ilmu Politik": {"mn": 680, "mx": 715},
        "Sejarah": {"mn": 652, "mx": 687},
        "Geografi": {"mn": 668, "mx": 703},
        "_default": {"mn": 680, "mx": 715},
    },
    "Universitas Diponegoro (Undip)": {
        "_klaster": 2,
        "_lbl": '🔷 Klaster 2 — Menengah Atas',
        "Kedokteran": {"mn": 731, "mx": 766},
        "Kedokteran Gigi": {"mn": 684, "mx": 719},
        "Teknik Sipil": {"mn": 686, "mx": 721},
        "Teknik Mesin": {"mn": 690, "mx": 725},
        "Teknik Elektro": {"mn": 704, "mx": 739},
        "Teknik Industri": {"mn": 675, "mx": 710},
        "Teknik Kimia": {"mn": 695, "mx": 730},
        "Teknik Informatika": {"mn": 722, "mx": 757},
        "Matematika": {"mn": 666, "mx": 701},
        "Fisika": {"mn": 660, "mx": 695},
        "Kimia": {"mn": 657, "mx": 692},
        "Biologi": {"mn": 654, "mx": 689},
        "Statistika": {"mn": 669, "mx": 704},
        "Aktuaria": {"mn": 672, "mx": 707},
        "Farmasi": {"mn": 708, "mx": 743},
        "Gizi": {"mn": 638, "mx": 673},
        "Keperawatan": {"mn": 633, "mx": 668},
        "Kesehatan Masyarakat": {"mn": 625, "mx": 660},
        "Ilmu Hukum": {"mn": 704, "mx": 739},
        "Ekonomi": {"mn": 684, "mx": 719},
        "Manajemen": {"mn": 693, "mx": 728},
        "Akuntansi": {"mn": 699, "mx": 734},
        "Bisnis": {"mn": 677, "mx": 712},
        "Psikologi": {"mn": 713, "mx": 748},
        "Ilmu Komunikasi": {"mn": 690, "mx": 725},
        "Hubungan Internasional": {"mn": 681, "mx": 716},
        "Administrasi Publik": {"mn": 606, "mx": 641},
        "Sastra Inggris": {"mn": 642, "mx": 677},
        "Pendidikan Bahasa Indonesia": {"mn": 636, "mx": 671},
        "Pendidikan Bahasa Inggris": {"mn": 633, "mx": 668},
        "Sosiologi": {"mn": 666, "mx": 701},
        "Ilmu Politik": {"mn": 672, "mx": 707},
        "Sejarah": {"mn": 645, "mx": 680},
        "Geografi": {"mn": 661, "mx": 696},
        "_default": {"mn": 672, "mx": 707},
    },
    "Universitas Brawijaya (UB)": {
        "_klaster": 2,
        "_lbl": '🔷 Klaster 2 — Menengah Atas',
        "Kedokteran": {"mn": 707, "mx": 742},
        "Kedokteran Gigi": {"mn": 661, "mx": 696},
        "Teknik Sipil": {"mn": 663, "mx": 698},
        "Teknik Mesin": {"mn": 667, "mx": 702},
        "Teknik Elektro": {"mn": 680, "mx": 715},
        "Teknik Industri": {"mn": 652, "mx": 687},
        "Teknik Kimia": {"mn": 671, "mx": 706},
        "Teknik Informatika": {"mn": 698, "mx": 733},
        "Matematika": {"mn": 643, "mx": 678},
        "Fisika": {"mn": 638, "mx": 673},
        "Kimia": {"mn": 634, "mx": 669},
        "Biologi": {"mn": 632, "mx": 667},
        "Statistika": {"mn": 647, "mx": 682},
        "Aktuaria": {"mn": 650, "mx": 685},
        "Farmasi": {"mn": 685, "mx": 720},
        "Gizi": {"mn": 617, "mx": 652},
        "Keperawatan": {"mn": 612, "mx": 647},
        "Kesehatan Masyarakat": {"mn": 604, "mx": 639},
        "Ilmu Hukum": {"mn": 680, "mx": 715},
        "Ekonomi": {"mn": 661, "mx": 696},
        "Manajemen": {"mn": 670, "mx": 705},
        "Akuntansi": {"mn": 676, "mx": 711},
        "Bisnis": {"mn": 654, "mx": 689},
        "Psikologi": {"mn": 689, "mx": 724},
        "Ilmu Komunikasi": {"mn": 667, "mx": 702},
        "Hubungan Internasional": {"mn": 658, "mx": 693},
        "Administrasi Publik": {"mn": 585, "mx": 620},
        "Sastra Inggris": {"mn": 620, "mx": 655},
        "Pendidikan Bahasa Indonesia": {"mn": 614, "mx": 649},
        "Pendidikan Bahasa Inggris": {"mn": 612, "mx": 647},
        "Sosiologi": {"mn": 643, "mx": 678},
        "Ilmu Politik": {"mn": 649, "mx": 684},
        "Sejarah": {"mn": 623, "mx": 658},
        "Geografi": {"mn": 638, "mx": 673},
        "_default": {"mn": 650, "mx": 685},
    },
    "Universitas Sebelas Maret (UNS)": {
        "_klaster": 2,
        "_lbl": '🔷 Klaster 2 — Menengah Atas',
        "Kedokteran": {"mn": 698, "mx": 733},
        "Kedokteran Gigi": {"mn": 653, "mx": 688},
        "Teknik Sipil": {"mn": 655, "mx": 690},
        "Teknik Mesin": {"mn": 659, "mx": 694},
        "Teknik Elektro": {"mn": 672, "mx": 707},
        "Teknik Industri": {"mn": 644, "mx": 679},
        "Teknik Kimia": {"mn": 664, "mx": 699},
        "Teknik Informatika": {"mn": 690, "mx": 725},
        "Matematika": {"mn": 636, "mx": 671},
        "Fisika": {"mn": 631, "mx": 666},
        "Kimia": {"mn": 627, "mx": 662},
        "Biologi": {"mn": 624, "mx": 659},
        "Statistika": {"mn": 639, "mx": 674},
        "Aktuaria": {"mn": 642, "mx": 677},
        "Farmasi": {"mn": 677, "mx": 712},
        "Gizi": {"mn": 610, "mx": 645},
        "Keperawatan": {"mn": 604, "mx": 639},
        "Kesehatan Masyarakat": {"mn": 596, "mx": 631},
        "Ilmu Hukum": {"mn": 672, "mx": 707},
        "Ekonomi": {"mn": 653, "mx": 688},
        "Manajemen": {"mn": 662, "mx": 697},
        "Akuntansi": {"mn": 668, "mx": 703},
        "Bisnis": {"mn": 646, "mx": 681},
        "Psikologi": {"mn": 681, "mx": 716},
        "Ilmu Komunikasi": {"mn": 659, "mx": 694},
        "Hubungan Internasional": {"mn": 651, "mx": 686},
        "Administrasi Publik": {"mn": 578, "mx": 613},
        "Sastra Inggris": {"mn": 613, "mx": 648},
        "Pendidikan Bahasa Indonesia": {"mn": 607, "mx": 642},
        "Pendidikan Bahasa Inggris": {"mn": 604, "mx": 639},
        "Sosiologi": {"mn": 636, "mx": 671},
        "Ilmu Politik": {"mn": 642, "mx": 677},
        "Sejarah": {"mn": 616, "mx": 651},
        "Geografi": {"mn": 631, "mx": 666},
        "_default": {"mn": 642, "mx": 677},
    },
    "Universitas Hasanuddin (Unhas)": {
        "_klaster": 2,
        "_lbl": '🔷 Klaster 2 — Menengah Atas',
        "Kedokteran": {"mn": 690, "mx": 725},
        "Kedokteran Gigi": {"mn": 645, "mx": 680},
        "Teknik Sipil": {"mn": 647, "mx": 682},
        "Teknik Mesin": {"mn": 651, "mx": 686},
        "Teknik Elektro": {"mn": 664, "mx": 699},
        "Teknik Industri": {"mn": 637, "mx": 672},
        "Teknik Kimia": {"mn": 656, "mx": 691},
        "Teknik Informatika": {"mn": 682, "mx": 717},
        "Matematika": {"mn": 628, "mx": 663},
        "Fisika": {"mn": 623, "mx": 658},
        "Kimia": {"mn": 620, "mx": 655},
        "Biologi": {"mn": 617, "mx": 652},
        "Statistika": {"mn": 632, "mx": 667},
        "Aktuaria": {"mn": 635, "mx": 670},
        "Farmasi": {"mn": 669, "mx": 704},
        "Gizi": {"mn": 602, "mx": 637},
        "Keperawatan": {"mn": 597, "mx": 632},
        "Kesehatan Masyarakat": {"mn": 589, "mx": 624},
        "Ilmu Hukum": {"mn": 664, "mx": 699},
        "Ekonomi": {"mn": 645, "mx": 680},
        "Manajemen": {"mn": 654, "mx": 689},
        "Akuntansi": {"mn": 660, "mx": 695},
        "Bisnis": {"mn": 639, "mx": 674},
        "Psikologi": {"mn": 673, "mx": 708},
        "Ilmu Komunikasi": {"mn": 651, "mx": 686},
        "Hubungan Internasional": {"mn": 643, "mx": 678},
        "Administrasi Publik": {"mn": 572, "mx": 607},
        "Sastra Inggris": {"mn": 606, "mx": 641},
        "Pendidikan Bahasa Indonesia": {"mn": 600, "mx": 635},
        "Pendidikan Bahasa Inggris": {"mn": 597, "mx": 632},
        "Sosiologi": {"mn": 628, "mx": 663},
        "Ilmu Politik": {"mn": 634, "mx": 669},
        "Sejarah": {"mn": 609, "mx": 644},
        "Geografi": {"mn": 623, "mx": 658},
        "_default": {"mn": 634, "mx": 669},
    },
    "Universitas Pendidikan Indonesia (UPI)": {
        "_klaster": 3,
        "_lbl": '🔹 Klaster 3 — Menengah',
        "Kedokteran": {"mn": 657, "mx": 692},
        "Kedokteran Gigi": {"mn": 615, "mx": 650},
        "Teknik Sipil": {"mn": 616, "mx": 651},
        "Teknik Mesin": {"mn": 621, "mx": 656},
        "Teknik Elektro": {"mn": 633, "mx": 668},
        "Teknik Industri": {"mn": 607, "mx": 642},
        "Teknik Kimia": {"mn": 625, "mx": 660},
        "Teknik Informatika": {"mn": 649, "mx": 684},
        "Matematika": {"mn": 598, "mx": 633},
        "Fisika": {"mn": 593, "mx": 628},
        "Kimia": {"mn": 590, "mx": 625},
        "Biologi": {"mn": 588, "mx": 623},
        "Statistika": {"mn": 602, "mx": 637},
        "Aktuaria": {"mn": 605, "mx": 640},
        "Farmasi": {"mn": 637, "mx": 672},
        "Gizi": {"mn": 574, "mx": 609},
        "Keperawatan": {"mn": 569, "mx": 604},
        "Kesehatan Masyarakat": {"mn": 561, "mx": 596},
        "Ilmu Hukum": {"mn": 633, "mx": 668},
        "Ekonomi": {"mn": 615, "mx": 650},
        "Manajemen": {"mn": 623, "mx": 658},
        "Akuntansi": {"mn": 629, "mx": 664},
        "Bisnis": {"mn": 608, "mx": 643},
        "Psikologi": {"mn": 641, "mx": 676},
        "Ilmu Komunikasi": {"mn": 621, "mx": 656},
        "Hubungan Internasional": {"mn": 612, "mx": 647},
        "Administrasi Publik": {"mn": 544, "mx": 579},
        "Sastra Inggris": {"mn": 577, "mx": 612},
        "Pendidikan Bahasa Indonesia": {"mn": 571, "mx": 606},
        "Pendidikan Bahasa Inggris": {"mn": 569, "mx": 604},
        "Sosiologi": {"mn": 598, "mx": 633},
        "Ilmu Politik": {"mn": 604, "mx": 639},
        "Sejarah": {"mn": 579, "mx": 614},
        "Geografi": {"mn": 593, "mx": 628},
        "_default": {"mn": 604, "mx": 639},
    },
    "Universitas Sumatera Utara (USU)": {
        "_klaster": 3,
        "_lbl": '🔹 Klaster 3 — Menengah',
        "Kedokteran": {"mn": 657, "mx": 692},
        "Kedokteran Gigi": {"mn": 615, "mx": 650},
        "Teknik Sipil": {"mn": 616, "mx": 651},
        "Teknik Mesin": {"mn": 621, "mx": 656},
        "Teknik Elektro": {"mn": 633, "mx": 668},
        "Teknik Industri": {"mn": 607, "mx": 642},
        "Teknik Kimia": {"mn": 625, "mx": 660},
        "Teknik Informatika": {"mn": 649, "mx": 684},
        "Matematika": {"mn": 598, "mx": 633},
        "Fisika": {"mn": 593, "mx": 628},
        "Kimia": {"mn": 590, "mx": 625},
        "Biologi": {"mn": 588, "mx": 623},
        "Statistika": {"mn": 602, "mx": 637},
        "Aktuaria": {"mn": 605, "mx": 640},
        "Farmasi": {"mn": 637, "mx": 672},
        "Gizi": {"mn": 574, "mx": 609},
        "Keperawatan": {"mn": 569, "mx": 604},
        "Kesehatan Masyarakat": {"mn": 561, "mx": 596},
        "Ilmu Hukum": {"mn": 633, "mx": 668},
        "Ekonomi": {"mn": 615, "mx": 650},
        "Manajemen": {"mn": 623, "mx": 658},
        "Akuntansi": {"mn": 629, "mx": 664},
        "Bisnis": {"mn": 608, "mx": 643},
        "Psikologi": {"mn": 641, "mx": 676},
        "Ilmu Komunikasi": {"mn": 621, "mx": 656},
        "Hubungan Internasional": {"mn": 612, "mx": 647},
        "Administrasi Publik": {"mn": 544, "mx": 579},
        "Sastra Inggris": {"mn": 577, "mx": 612},
        "Pendidikan Bahasa Indonesia": {"mn": 571, "mx": 606},
        "Pendidikan Bahasa Inggris": {"mn": 569, "mx": 604},
        "Sosiologi": {"mn": 598, "mx": 633},
        "Ilmu Politik": {"mn": 604, "mx": 639},
        "Sejarah": {"mn": 579, "mx": 614},
        "Geografi": {"mn": 593, "mx": 628},
        "_default": {"mn": 604, "mx": 639},
    },
    "Universitas Negeri Yogyakarta (UNY)": {
        "_klaster": 3,
        "_lbl": '🔹 Klaster 3 — Menengah',
        "Kedokteran": {"mn": 657, "mx": 692},
        "Kedokteran Gigi": {"mn": 615, "mx": 650},
        "Teknik Sipil": {"mn": 616, "mx": 651},
        "Teknik Mesin": {"mn": 621, "mx": 656},
        "Teknik Elektro": {"mn": 633, "mx": 668},
        "Teknik Industri": {"mn": 607, "mx": 642},
        "Teknik Kimia": {"mn": 625, "mx": 660},
        "Teknik Informatika": {"mn": 649, "mx": 684},
        "Matematika": {"mn": 598, "mx": 633},
        "Fisika": {"mn": 593, "mx": 628},
        "Kimia": {"mn": 590, "mx": 625},
        "Biologi": {"mn": 588, "mx": 623},
        "Statistika": {"mn": 602, "mx": 637},
        "Aktuaria": {"mn": 605, "mx": 640},
        "Farmasi": {"mn": 637, "mx": 672},
        "Gizi": {"mn": 574, "mx": 609},
        "Keperawatan": {"mn": 569, "mx": 604},
        "Kesehatan Masyarakat": {"mn": 561, "mx": 596},
        "Ilmu Hukum": {"mn": 633, "mx": 668},
        "Ekonomi": {"mn": 615, "mx": 650},
        "Manajemen": {"mn": 623, "mx": 658},
        "Akuntansi": {"mn": 629, "mx": 664},
        "Bisnis": {"mn": 608, "mx": 643},
        "Psikologi": {"mn": 641, "mx": 676},
        "Ilmu Komunikasi": {"mn": 621, "mx": 656},
        "Hubungan Internasional": {"mn": 612, "mx": 647},
        "Administrasi Publik": {"mn": 544, "mx": 579},
        "Sastra Inggris": {"mn": 577, "mx": 612},
        "Pendidikan Bahasa Indonesia": {"mn": 571, "mx": 606},
        "Pendidikan Bahasa Inggris": {"mn": 569, "mx": 604},
        "Sosiologi": {"mn": 598, "mx": 633},
        "Ilmu Politik": {"mn": 604, "mx": 639},
        "Sejarah": {"mn": 579, "mx": 614},
        "Geografi": {"mn": 593, "mx": 628},
        "_default": {"mn": 604, "mx": 639},
    },
    "Universitas Negeri Malang (UM)": {
        "_klaster": 3,
        "_lbl": '🔹 Klaster 3 — Menengah',
        "Kedokteran": {"mn": 641, "mx": 676},
        "Kedokteran Gigi": {"mn": 599, "mx": 634},
        "Teknik Sipil": {"mn": 601, "mx": 636},
        "Teknik Mesin": {"mn": 605, "mx": 640},
        "Teknik Elektro": {"mn": 617, "mx": 652},
        "Teknik Industri": {"mn": 591, "mx": 626},
        "Teknik Kimia": {"mn": 609, "mx": 644},
        "Teknik Informatika": {"mn": 633, "mx": 668},
        "Matematika": {"mn": 583, "mx": 618},
        "Fisika": {"mn": 579, "mx": 614},
        "Kimia": {"mn": 575, "mx": 610},
        "Biologi": {"mn": 573, "mx": 608},
        "Statistika": {"mn": 587, "mx": 622},
        "Aktuaria": {"mn": 590, "mx": 625},
        "Farmasi": {"mn": 621, "mx": 656},
        "Gizi": {"mn": 559, "mx": 594},
        "Keperawatan": {"mn": 555, "mx": 590},
        "Kesehatan Masyarakat": {"mn": 547, "mx": 582},
        "Ilmu Hukum": {"mn": 617, "mx": 652},
        "Ekonomi": {"mn": 599, "mx": 634},
        "Manajemen": {"mn": 607, "mx": 642},
        "Akuntansi": {"mn": 613, "mx": 648},
        "Bisnis": {"mn": 593, "mx": 628},
        "Psikologi": {"mn": 625, "mx": 660},
        "Ilmu Komunikasi": {"mn": 605, "mx": 640},
        "Hubungan Internasional": {"mn": 597, "mx": 632},
        "Administrasi Publik": {"mn": 531, "mx": 566},
        "Sastra Inggris": {"mn": 563, "mx": 598},
        "Pendidikan Bahasa Indonesia": {"mn": 557, "mx": 592},
        "Pendidikan Bahasa Inggris": {"mn": 555, "mx": 590},
        "Sosiologi": {"mn": 583, "mx": 618},
        "Ilmu Politik": {"mn": 589, "mx": 624},
        "Sejarah": {"mn": 565, "mx": 600},
        "Geografi": {"mn": 578, "mx": 613},
        "_default": {"mn": 589, "mx": 624},
    },
    "Universitas Lampung (Unila)": {
        "_klaster": 3,
        "_lbl": '🔹 Klaster 3 — Menengah',
        "Kedokteran": {"mn": 633, "mx": 668},
        "Kedokteran Gigi": {"mn": 592, "mx": 627},
        "Teknik Sipil": {"mn": 593, "mx": 628},
        "Teknik Mesin": {"mn": 597, "mx": 632},
        "Teknik Elektro": {"mn": 609, "mx": 644},
        "Teknik Industri": {"mn": 584, "mx": 619},
        "Teknik Kimia": {"mn": 601, "mx": 636},
        "Teknik Informatika": {"mn": 625, "mx": 660},
        "Matematika": {"mn": 576, "mx": 611},
        "Fisika": {"mn": 571, "mx": 606},
        "Kimia": {"mn": 568, "mx": 603},
        "Biologi": {"mn": 566, "mx": 601},
        "Statistika": {"mn": 579, "mx": 614},
        "Aktuaria": {"mn": 582, "mx": 617},
        "Farmasi": {"mn": 613, "mx": 648},
        "Gizi": {"mn": 552, "mx": 587},
        "Keperawatan": {"mn": 547, "mx": 582},
        "Kesehatan Masyarakat": {"mn": 539, "mx": 574},
        "Ilmu Hukum": {"mn": 609, "mx": 644},
        "Ekonomi": {"mn": 592, "mx": 627},
        "Manajemen": {"mn": 600, "mx": 635},
        "Akuntansi": {"mn": 605, "mx": 640},
        "Bisnis": {"mn": 585, "mx": 620},
        "Psikologi": {"mn": 617, "mx": 652},
        "Ilmu Komunikasi": {"mn": 597, "mx": 632},
        "Hubungan Internasional": {"mn": 589, "mx": 624},
        "Administrasi Publik": {"mn": 524, "mx": 559},
        "Sastra Inggris": {"mn": 555, "mx": 590},
        "Pendidikan Bahasa Indonesia": {"mn": 550, "mx": 585},
        "Pendidikan Bahasa Inggris": {"mn": 547, "mx": 582},
        "Sosiologi": {"mn": 576, "mx": 611},
        "Ilmu Politik": {"mn": 581, "mx": 616},
        "Sejarah": {"mn": 558, "mx": 593},
        "Geografi": {"mn": 571, "mx": 606},
        "_default": {"mn": 581, "mx": 616},
    },
    "Universitas Andalas (Unand)": {
        "_klaster": 3,
        "_lbl": '🔹 Klaster 3 — Menengah',
        "Kedokteran": {"mn": 649, "mx": 684},
        "Kedokteran Gigi": {"mn": 607, "mx": 642},
        "Teknik Sipil": {"mn": 609, "mx": 644},
        "Teknik Mesin": {"mn": 613, "mx": 648},
        "Teknik Elektro": {"mn": 625, "mx": 660},
        "Teknik Industri": {"mn": 599, "mx": 634},
        "Teknik Kimia": {"mn": 617, "mx": 652},
        "Teknik Informatika": {"mn": 641, "mx": 676},
        "Matematika": {"mn": 591, "mx": 626},
        "Fisika": {"mn": 586, "mx": 621},
        "Kimia": {"mn": 583, "mx": 618},
        "Biologi": {"mn": 580, "mx": 615},
        "Statistika": {"mn": 594, "mx": 629},
        "Aktuaria": {"mn": 597, "mx": 632},
        "Farmasi": {"mn": 629, "mx": 664},
        "Gizi": {"mn": 567, "mx": 602},
        "Keperawatan": {"mn": 562, "mx": 597},
        "Kesehatan Masyarakat": {"mn": 554, "mx": 589},
        "Ilmu Hukum": {"mn": 625, "mx": 660},
        "Ekonomi": {"mn": 607, "mx": 642},
        "Manajemen": {"mn": 615, "mx": 650},
        "Akuntansi": {"mn": 621, "mx": 656},
        "Bisnis": {"mn": 601, "mx": 636},
        "Psikologi": {"mn": 633, "mx": 668},
        "Ilmu Komunikasi": {"mn": 613, "mx": 648},
        "Hubungan Internasional": {"mn": 605, "mx": 640},
        "Administrasi Publik": {"mn": 537, "mx": 572},
        "Sastra Inggris": {"mn": 570, "mx": 605},
        "Pendidikan Bahasa Indonesia": {"mn": 564, "mx": 599},
        "Pendidikan Bahasa Inggris": {"mn": 562, "mx": 597},
        "Sosiologi": {"mn": 591, "mx": 626},
        "Ilmu Politik": {"mn": 597, "mx": 632},
        "Sejarah": {"mn": 572, "mx": 607},
        "Geografi": {"mn": 586, "mx": 621},
        "_default": {"mn": 597, "mx": 632},
    },
    "Universitas Negeri Semarang (UNNES)": {
        "_klaster": 3,
        "_lbl": '🔹 Klaster 3 — Menengah',
        "Kedokteran": {"mn": 641, "mx": 676},
        "Kedokteran Gigi": {"mn": 599, "mx": 634},
        "Teknik Sipil": {"mn": 601, "mx": 636},
        "Teknik Mesin": {"mn": 605, "mx": 640},
        "Teknik Elektro": {"mn": 617, "mx": 652},
        "Teknik Industri": {"mn": 591, "mx": 626},
        "Teknik Kimia": {"mn": 609, "mx": 644},
        "Teknik Informatika": {"mn": 633, "mx": 668},
        "Matematika": {"mn": 583, "mx": 618},
        "Fisika": {"mn": 579, "mx": 614},
        "Kimia": {"mn": 575, "mx": 610},
        "Biologi": {"mn": 573, "mx": 608},
        "Statistika": {"mn": 587, "mx": 622},
        "Aktuaria": {"mn": 590, "mx": 625},
        "Farmasi": {"mn": 621, "mx": 656},
        "Gizi": {"mn": 559, "mx": 594},
        "Keperawatan": {"mn": 555, "mx": 590},
        "Kesehatan Masyarakat": {"mn": 547, "mx": 582},
        "Ilmu Hukum": {"mn": 617, "mx": 652},
        "Ekonomi": {"mn": 599, "mx": 634},
        "Manajemen": {"mn": 607, "mx": 642},
        "Akuntansi": {"mn": 613, "mx": 648},
        "Bisnis": {"mn": 593, "mx": 628},
        "Psikologi": {"mn": 625, "mx": 660},
        "Ilmu Komunikasi": {"mn": 605, "mx": 640},
        "Hubungan Internasional": {"mn": 597, "mx": 632},
        "Administrasi Publik": {"mn": 531, "mx": 566},
        "Sastra Inggris": {"mn": 563, "mx": 598},
        "Pendidikan Bahasa Indonesia": {"mn": 557, "mx": 592},
        "Pendidikan Bahasa Inggris": {"mn": 555, "mx": 590},
        "Sosiologi": {"mn": 583, "mx": 618},
        "Ilmu Politik": {"mn": 589, "mx": 624},
        "Sejarah": {"mn": 565, "mx": 600},
        "Geografi": {"mn": 578, "mx": 613},
        "_default": {"mn": 589, "mx": 624},
    },
    "Universitas Syiah Kuala (USK)": {
        "_klaster": 4,
        "_lbl": '🔸 Klaster 4 — Regional',
        "Kedokteran": {"mn": 633, "mx": 668},
        "Kedokteran Gigi": {"mn": 592, "mx": 627},
        "Teknik Sipil": {"mn": 593, "mx": 628},
        "Teknik Mesin": {"mn": 597, "mx": 632},
        "Teknik Elektro": {"mn": 609, "mx": 644},
        "Teknik Industri": {"mn": 584, "mx": 619},
        "Teknik Kimia": {"mn": 601, "mx": 636},
        "Teknik Informatika": {"mn": 625, "mx": 660},
        "Matematika": {"mn": 576, "mx": 611},
        "Fisika": {"mn": 571, "mx": 606},
        "Kimia": {"mn": 568, "mx": 603},
        "Biologi": {"mn": 566, "mx": 601},
        "Statistika": {"mn": 579, "mx": 614},
        "Aktuaria": {"mn": 582, "mx": 617},
        "Farmasi": {"mn": 613, "mx": 648},
        "Gizi": {"mn": 552, "mx": 587},
        "Keperawatan": {"mn": 547, "mx": 582},
        "Kesehatan Masyarakat": {"mn": 539, "mx": 574},
        "Ilmu Hukum": {"mn": 609, "mx": 644},
        "Ekonomi": {"mn": 592, "mx": 627},
        "Manajemen": {"mn": 600, "mx": 635},
        "Akuntansi": {"mn": 605, "mx": 640},
        "Bisnis": {"mn": 585, "mx": 620},
        "Psikologi": {"mn": 617, "mx": 652},
        "Ilmu Komunikasi": {"mn": 597, "mx": 632},
        "Hubungan Internasional": {"mn": 589, "mx": 624},
        "Administrasi Publik": {"mn": 524, "mx": 559},
        "Sastra Inggris": {"mn": 555, "mx": 590},
        "Pendidikan Bahasa Indonesia": {"mn": 550, "mx": 585},
        "Pendidikan Bahasa Inggris": {"mn": 547, "mx": 582},
        "Sosiologi": {"mn": 576, "mx": 611},
        "Ilmu Politik": {"mn": 581, "mx": 616},
        "Sejarah": {"mn": 558, "mx": 593},
        "Geografi": {"mn": 571, "mx": 606},
        "_default": {"mn": 581, "mx": 616},
    },
    "Universitas Mulawarman (Unmul)": {
        "_klaster": 4,
        "_lbl": '🔸 Klaster 4 — Regional',
        "Kedokteran": {"mn": 616, "mx": 651},
        "Kedokteran Gigi": {"mn": 576, "mx": 611},
        "Teknik Sipil": {"mn": 578, "mx": 613},
        "Teknik Mesin": {"mn": 582, "mx": 617},
        "Teknik Elektro": {"mn": 593, "mx": 628},
        "Teknik Industri": {"mn": 569, "mx": 604},
        "Teknik Kimia": {"mn": 586, "mx": 621},
        "Teknik Informatika": {"mn": 609, "mx": 644},
        "Matematika": {"mn": 561, "mx": 596},
        "Fisika": {"mn": 556, "mx": 591},
        "Kimia": {"mn": 553, "mx": 588},
        "Biologi": {"mn": 551, "mx": 586},
        "Statistika": {"mn": 564, "mx": 599},
        "Aktuaria": {"mn": 567, "mx": 602},
        "Farmasi": {"mn": 597, "mx": 632},
        "Gizi": {"mn": 538, "mx": 573},
        "Keperawatan": {"mn": 533, "mx": 568},
        "Kesehatan Masyarakat": {"mn": 525, "mx": 560},
        "Ilmu Hukum": {"mn": 593, "mx": 628},
        "Ekonomi": {"mn": 576, "mx": 611},
        "Manajemen": {"mn": 584, "mx": 619},
        "Akuntansi": {"mn": 589, "mx": 624},
        "Bisnis": {"mn": 570, "mx": 605},
        "Psikologi": {"mn": 601, "mx": 636},
        "Ilmu Komunikasi": {"mn": 582, "mx": 617},
        "Hubungan Internasional": {"mn": 574, "mx": 609},
        "Administrasi Publik": {"mn": 510, "mx": 545},
        "Sastra Inggris": {"mn": 541, "mx": 576},
        "Pendidikan Bahasa Indonesia": {"mn": 536, "mx": 571},
        "Pendidikan Bahasa Inggris": {"mn": 533, "mx": 568},
        "Sosiologi": {"mn": 561, "mx": 596},
        "Ilmu Politik": {"mn": 566, "mx": 601},
        "Sejarah": {"mn": 543, "mx": 578},
        "Geografi": {"mn": 556, "mx": 591},
        "_default": {"mn": 566, "mx": 601},
    },
    "Universitas Sriwijaya (Unsri)": {
        "_klaster": 4,
        "_lbl": '🔸 Klaster 4 — Regional',
        "Kedokteran": {"mn": 633, "mx": 668},
        "Kedokteran Gigi": {"mn": 592, "mx": 627},
        "Teknik Sipil": {"mn": 593, "mx": 628},
        "Teknik Mesin": {"mn": 597, "mx": 632},
        "Teknik Elektro": {"mn": 609, "mx": 644},
        "Teknik Industri": {"mn": 584, "mx": 619},
        "Teknik Kimia": {"mn": 601, "mx": 636},
        "Teknik Informatika": {"mn": 625, "mx": 660},
        "Matematika": {"mn": 576, "mx": 611},
        "Fisika": {"mn": 571, "mx": 606},
        "Kimia": {"mn": 568, "mx": 603},
        "Biologi": {"mn": 566, "mx": 601},
        "Statistika": {"mn": 579, "mx": 614},
        "Aktuaria": {"mn": 582, "mx": 617},
        "Farmasi": {"mn": 613, "mx": 648},
        "Gizi": {"mn": 552, "mx": 587},
        "Keperawatan": {"mn": 547, "mx": 582},
        "Kesehatan Masyarakat": {"mn": 539, "mx": 574},
        "Ilmu Hukum": {"mn": 609, "mx": 644},
        "Ekonomi": {"mn": 592, "mx": 627},
        "Manajemen": {"mn": 600, "mx": 635},
        "Akuntansi": {"mn": 605, "mx": 640},
        "Bisnis": {"mn": 585, "mx": 620},
        "Psikologi": {"mn": 617, "mx": 652},
        "Ilmu Komunikasi": {"mn": 597, "mx": 632},
        "Hubungan Internasional": {"mn": 589, "mx": 624},
        "Administrasi Publik": {"mn": 524, "mx": 559},
        "Sastra Inggris": {"mn": 555, "mx": 590},
        "Pendidikan Bahasa Indonesia": {"mn": 550, "mx": 585},
        "Pendidikan Bahasa Inggris": {"mn": 547, "mx": 582},
        "Sosiologi": {"mn": 576, "mx": 611},
        "Ilmu Politik": {"mn": 581, "mx": 616},
        "Sejarah": {"mn": 558, "mx": 593},
        "Geografi": {"mn": 571, "mx": 606},
        "_default": {"mn": 581, "mx": 616},
    },
    "Universitas Udayana (Unud)": {
        "_klaster": 4,
        "_lbl": '🔸 Klaster 4 — Regional',
        "Kedokteran": {"mn": 666, "mx": 701},
        "Kedokteran Gigi": {"mn": 622, "mx": 657},
        "Teknik Sipil": {"mn": 624, "mx": 659},
        "Teknik Mesin": {"mn": 628, "mx": 663},
        "Teknik Elektro": {"mn": 641, "mx": 676},
        "Teknik Industri": {"mn": 614, "mx": 649},
        "Teknik Kimia": {"mn": 632, "mx": 667},
        "Teknik Informatika": {"mn": 657, "mx": 692},
        "Matematika": {"mn": 606, "mx": 641},
        "Fisika": {"mn": 601, "mx": 636},
        "Kimia": {"mn": 598, "mx": 633},
        "Biologi": {"mn": 595, "mx": 630},
        "Statistika": {"mn": 609, "mx": 644},
        "Aktuaria": {"mn": 612, "mx": 647},
        "Farmasi": {"mn": 645, "mx": 680},
        "Gizi": {"mn": 581, "mx": 616},
        "Keperawatan": {"mn": 576, "mx": 611},
        "Kesehatan Masyarakat": {"mn": 568, "mx": 603},
        "Ilmu Hukum": {"mn": 641, "mx": 676},
        "Ekonomi": {"mn": 622, "mx": 657},
        "Manajemen": {"mn": 631, "mx": 666},
        "Akuntansi": {"mn": 637, "mx": 672},
        "Bisnis": {"mn": 616, "mx": 651},
        "Psikologi": {"mn": 649, "mx": 684},
        "Ilmu Komunikasi": {"mn": 628, "mx": 663},
        "Hubungan Internasional": {"mn": 620, "mx": 655},
        "Administrasi Publik": {"mn": 551, "mx": 586},
        "Sastra Inggris": {"mn": 584, "mx": 619},
        "Pendidikan Bahasa Indonesia": {"mn": 578, "mx": 613},
        "Pendidikan Bahasa Inggris": {"mn": 576, "mx": 611},
        "Sosiologi": {"mn": 606, "mx": 641},
        "Ilmu Politik": {"mn": 612, "mx": 647},
        "Sejarah": {"mn": 587, "mx": 622},
        "Geografi": {"mn": 601, "mx": 636},
        "_default": {"mn": 612, "mx": 647},
    },
    "Universitas Sam Ratulangi (Unsrat)": {
        "_klaster": 4,
        "_lbl": '🔸 Klaster 4 — Regional',
        "Kedokteran": {"mn": 616, "mx": 651},
        "Kedokteran Gigi": {"mn": 576, "mx": 611},
        "Teknik Sipil": {"mn": 578, "mx": 613},
        "Teknik Mesin": {"mn": 582, "mx": 617},
        "Teknik Elektro": {"mn": 593, "mx": 628},
        "Teknik Industri": {"mn": 569, "mx": 604},
        "Teknik Kimia": {"mn": 586, "mx": 621},
        "Teknik Informatika": {"mn": 609, "mx": 644},
        "Matematika": {"mn": 561, "mx": 596},
        "Fisika": {"mn": 556, "mx": 591},
        "Kimia": {"mn": 553, "mx": 588},
        "Biologi": {"mn": 551, "mx": 586},
        "Statistika": {"mn": 564, "mx": 599},
        "Aktuaria": {"mn": 567, "mx": 602},
        "Farmasi": {"mn": 597, "mx": 632},
        "Gizi": {"mn": 538, "mx": 573},
        "Keperawatan": {"mn": 533, "mx": 568},
        "Kesehatan Masyarakat": {"mn": 525, "mx": 560},
        "Ilmu Hukum": {"mn": 593, "mx": 628},
        "Ekonomi": {"mn": 576, "mx": 611},
        "Manajemen": {"mn": 584, "mx": 619},
        "Akuntansi": {"mn": 589, "mx": 624},
        "Bisnis": {"mn": 570, "mx": 605},
        "Psikologi": {"mn": 601, "mx": 636},
        "Ilmu Komunikasi": {"mn": 582, "mx": 617},
        "Hubungan Internasional": {"mn": 574, "mx": 609},
        "Administrasi Publik": {"mn": 510, "mx": 545},
        "Sastra Inggris": {"mn": 541, "mx": 576},
        "Pendidikan Bahasa Indonesia": {"mn": 536, "mx": 571},
        "Pendidikan Bahasa Inggris": {"mn": 533, "mx": 568},
        "Sosiologi": {"mn": 561, "mx": 596},
        "Ilmu Politik": {"mn": 566, "mx": 601},
        "Sejarah": {"mn": 543, "mx": 578},
        "Geografi": {"mn": 556, "mx": 591},
        "_default": {"mn": 566, "mx": 601},
    },
    "Universitas Riau (Unri)": {
        "_klaster": 4,
        "_lbl": '🔸 Klaster 4 — Regional',
        "Kedokteran": {"mn": 625, "mx": 660},
        "Kedokteran Gigi": {"mn": 584, "mx": 619},
        "Teknik Sipil": {"mn": 586, "mx": 621},
        "Teknik Mesin": {"mn": 589, "mx": 624},
        "Teknik Elektro": {"mn": 601, "mx": 636},
        "Teknik Industri": {"mn": 576, "mx": 611},
        "Teknik Kimia": {"mn": 593, "mx": 628},
        "Teknik Informatika": {"mn": 617, "mx": 652},
        "Matematika": {"mn": 568, "mx": 603},
        "Fisika": {"mn": 564, "mx": 599},
        "Kimia": {"mn": 561, "mx": 596},
        "Biologi": {"mn": 558, "mx": 593},
        "Statistika": {"mn": 572, "mx": 607},
        "Aktuaria": {"mn": 575, "mx": 610},
        "Farmasi": {"mn": 605, "mx": 640},
        "Gizi": {"mn": 545, "mx": 580},
        "Keperawatan": {"mn": 540, "mx": 575},
        "Kesehatan Masyarakat": {"mn": 532, "mx": 567},
        "Ilmu Hukum": {"mn": 601, "mx": 636},
        "Ekonomi": {"mn": 584, "mx": 619},
        "Manajemen": {"mn": 592, "mx": 627},
        "Akuntansi": {"mn": 597, "mx": 632},
        "Bisnis": {"mn": 578, "mx": 613},
        "Psikologi": {"mn": 609, "mx": 644},
        "Ilmu Komunikasi": {"mn": 589, "mx": 624},
        "Hubungan Internasional": {"mn": 582, "mx": 617},
        "Administrasi Publik": {"mn": 517, "mx": 552},
        "Sastra Inggris": {"mn": 548, "mx": 583},
        "Pendidikan Bahasa Indonesia": {"mn": 543, "mx": 578},
        "Pendidikan Bahasa Inggris": {"mn": 540, "mx": 575},
        "Sosiologi": {"mn": 568, "mx": 603},
        "Ilmu Politik": {"mn": 574, "mx": 609},
        "Sejarah": {"mn": 551, "mx": 586},
        "Geografi": {"mn": 563, "mx": 598},
        "_default": {"mn": 574, "mx": 609},
    },
    "Universitas Jember (Unej)": {
        "_klaster": 4,
        "_lbl": '🔸 Klaster 4 — Regional',
        "Kedokteran": {"mn": 641, "mx": 676},
        "Kedokteran Gigi": {"mn": 599, "mx": 634},
        "Teknik Sipil": {"mn": 601, "mx": 636},
        "Teknik Mesin": {"mn": 605, "mx": 640},
        "Teknik Elektro": {"mn": 617, "mx": 652},
        "Teknik Industri": {"mn": 591, "mx": 626},
        "Teknik Kimia": {"mn": 609, "mx": 644},
        "Teknik Informatika": {"mn": 633, "mx": 668},
        "Matematika": {"mn": 583, "mx": 618},
        "Fisika": {"mn": 579, "mx": 614},
        "Kimia": {"mn": 575, "mx": 610},
        "Biologi": {"mn": 573, "mx": 608},
        "Statistika": {"mn": 587, "mx": 622},
        "Aktuaria": {"mn": 590, "mx": 625},
        "Farmasi": {"mn": 621, "mx": 656},
        "Gizi": {"mn": 559, "mx": 594},
        "Keperawatan": {"mn": 555, "mx": 590},
        "Kesehatan Masyarakat": {"mn": 547, "mx": 582},
        "Ilmu Hukum": {"mn": 617, "mx": 652},
        "Ekonomi": {"mn": 599, "mx": 634},
        "Manajemen": {"mn": 607, "mx": 642},
        "Akuntansi": {"mn": 613, "mx": 648},
        "Bisnis": {"mn": 593, "mx": 628},
        "Psikologi": {"mn": 625, "mx": 660},
        "Ilmu Komunikasi": {"mn": 605, "mx": 640},
        "Hubungan Internasional": {"mn": 597, "mx": 632},
        "Administrasi Publik": {"mn": 531, "mx": 566},
        "Sastra Inggris": {"mn": 563, "mx": 598},
        "Pendidikan Bahasa Indonesia": {"mn": 557, "mx": 592},
        "Pendidikan Bahasa Inggris": {"mn": 555, "mx": 590},
        "Sosiologi": {"mn": 583, "mx": 618},
        "Ilmu Politik": {"mn": 589, "mx": 624},
        "Sejarah": {"mn": 565, "mx": 600},
        "Geografi": {"mn": 578, "mx": 613},
        "_default": {"mn": 589, "mx": 624},
    },
    "Telkom University": {
        "_klaster": 4,
        "_lbl": '🔸 Klaster 4 — Regional',
        "Kedokteran": {"mn": 633, "mx": 668},
        "Kedokteran Gigi": {"mn": 592, "mx": 627},
        "Teknik Sipil": {"mn": 593, "mx": 628},
        "Teknik Mesin": {"mn": 597, "mx": 632},
        "Teknik Elektro": {"mn": 609, "mx": 644},
        "Teknik Industri": {"mn": 584, "mx": 619},
        "Teknik Kimia": {"mn": 601, "mx": 636},
        "Teknik Informatika": {"mn": 625, "mx": 660},
        "Matematika": {"mn": 576, "mx": 611},
        "Fisika": {"mn": 571, "mx": 606},
        "Kimia": {"mn": 568, "mx": 603},
        "Biologi": {"mn": 566, "mx": 601},
        "Statistika": {"mn": 579, "mx": 614},
        "Aktuaria": {"mn": 582, "mx": 617},
        "Farmasi": {"mn": 613, "mx": 648},
        "Gizi": {"mn": 552, "mx": 587},
        "Keperawatan": {"mn": 547, "mx": 582},
        "Kesehatan Masyarakat": {"mn": 539, "mx": 574},
        "Ilmu Hukum": {"mn": 609, "mx": 644},
        "Ekonomi": {"mn": 592, "mx": 627},
        "Manajemen": {"mn": 600, "mx": 635},
        "Akuntansi": {"mn": 605, "mx": 640},
        "Bisnis": {"mn": 585, "mx": 620},
        "Psikologi": {"mn": 617, "mx": 652},
        "Ilmu Komunikasi": {"mn": 597, "mx": 632},
        "Hubungan Internasional": {"mn": 589, "mx": 624},
        "Administrasi Publik": {"mn": 524, "mx": 559},
        "Sastra Inggris": {"mn": 555, "mx": 590},
        "Pendidikan Bahasa Indonesia": {"mn": 550, "mx": 585},
        "Pendidikan Bahasa Inggris": {"mn": 547, "mx": 582},
        "Sosiologi": {"mn": 576, "mx": 611},
        "Ilmu Politik": {"mn": 581, "mx": 616},
        "Sejarah": {"mn": 558, "mx": 593},
        "Geografi": {"mn": 571, "mx": 606},
        "_default": {"mn": 581, "mx": 616},
    },
    "Universitas Islam Indonesia (UII)": {
        "_klaster": 4,
        "_lbl": '🔸 Klaster 4 — Regional',
        "Kedokteran": {"mn": 625, "mx": 660},
        "Kedokteran Gigi": {"mn": 584, "mx": 619},
        "Teknik Sipil": {"mn": 586, "mx": 621},
        "Teknik Mesin": {"mn": 589, "mx": 624},
        "Teknik Elektro": {"mn": 601, "mx": 636},
        "Teknik Industri": {"mn": 576, "mx": 611},
        "Teknik Kimia": {"mn": 593, "mx": 628},
        "Teknik Informatika": {"mn": 617, "mx": 652},
        "Matematika": {"mn": 568, "mx": 603},
        "Fisika": {"mn": 564, "mx": 599},
        "Kimia": {"mn": 561, "mx": 596},
        "Biologi": {"mn": 558, "mx": 593},
        "Statistika": {"mn": 572, "mx": 607},
        "Aktuaria": {"mn": 575, "mx": 610},
        "Farmasi": {"mn": 605, "mx": 640},
        "Gizi": {"mn": 545, "mx": 580},
        "Keperawatan": {"mn": 540, "mx": 575},
        "Kesehatan Masyarakat": {"mn": 532, "mx": 567},
        "Ilmu Hukum": {"mn": 601, "mx": 636},
        "Ekonomi": {"mn": 584, "mx": 619},
        "Manajemen": {"mn": 592, "mx": 627},
        "Akuntansi": {"mn": 597, "mx": 632},
        "Bisnis": {"mn": 578, "mx": 613},
        "Psikologi": {"mn": 609, "mx": 644},
        "Ilmu Komunikasi": {"mn": 589, "mx": 624},
        "Hubungan Internasional": {"mn": 582, "mx": 617},
        "Administrasi Publik": {"mn": 517, "mx": 552},
        "Sastra Inggris": {"mn": 548, "mx": 583},
        "Pendidikan Bahasa Indonesia": {"mn": 543, "mx": 578},
        "Pendidikan Bahasa Inggris": {"mn": 540, "mx": 575},
        "Sosiologi": {"mn": 568, "mx": 603},
        "Ilmu Politik": {"mn": 574, "mx": 609},
        "Sejarah": {"mn": 551, "mx": 586},
        "Geografi": {"mn": 563, "mx": 598},
        "_default": {"mn": 574, "mx": 609},
    },
    "Universitas Muhammadiyah Yogyakarta (UMY)": {
        "_klaster": 4,
        "_lbl": '🔸 Klaster 4 — Regional',
        "Kedokteran": {"mn": 608, "mx": 643},
        "Kedokteran Gigi": {"mn": 569, "mx": 604},
        "Teknik Sipil": {"mn": 570, "mx": 605},
        "Teknik Mesin": {"mn": 574, "mx": 609},
        "Teknik Elektro": {"mn": 585, "mx": 620},
        "Teknik Industri": {"mn": 561, "mx": 596},
        "Teknik Kimia": {"mn": 578, "mx": 613},
        "Teknik Informatika": {"mn": 601, "mx": 636},
        "Matematika": {"mn": 553, "mx": 588},
        "Fisika": {"mn": 549, "mx": 584},
        "Kimia": {"mn": 546, "mx": 581},
        "Biologi": {"mn": 544, "mx": 579},
        "Statistika": {"mn": 557, "mx": 592},
        "Aktuaria": {"mn": 560, "mx": 595},
        "Farmasi": {"mn": 589, "mx": 624},
        "Gizi": {"mn": 531, "mx": 566},
        "Keperawatan": {"mn": 526, "mx": 561},
        "Kesehatan Masyarakat": {"mn": 518, "mx": 553},
        "Ilmu Hukum": {"mn": 585, "mx": 620},
        "Ekonomi": {"mn": 569, "mx": 604},
        "Manajemen": {"mn": 576, "mx": 611},
        "Akuntansi": {"mn": 582, "mx": 617},
        "Bisnis": {"mn": 563, "mx": 598},
        "Psikologi": {"mn": 593, "mx": 628},
        "Ilmu Komunikasi": {"mn": 574, "mx": 609},
        "Hubungan Internasional": {"mn": 566, "mx": 601},
        "Administrasi Publik": {"mn": 503, "mx": 538},
        "Sastra Inggris": {"mn": 534, "mx": 569},
        "Pendidikan Bahasa Indonesia": {"mn": 528, "mx": 563},
        "Pendidikan Bahasa Inggris": {"mn": 526, "mx": 561},
        "Sosiologi": {"mn": 553, "mx": 588},
        "Ilmu Politik": {"mn": 559, "mx": 594},
        "Sejarah": {"mn": 536, "mx": 571},
        "Geografi": {"mn": 548, "mx": 583},
        "_default": {"mn": 559, "mx": 594},
    },
    "Bina Nusantara University (Binus)": {
        "_klaster": 4,
        "_lbl": '🔸 Klaster 4 — Regional',
        "Kedokteran": {"mn": 641, "mx": 676},
        "Kedokteran Gigi": {"mn": 599, "mx": 634},
        "Teknik Sipil": {"mn": 601, "mx": 636},
        "Teknik Mesin": {"mn": 605, "mx": 640},
        "Teknik Elektro": {"mn": 617, "mx": 652},
        "Teknik Industri": {"mn": 591, "mx": 626},
        "Teknik Kimia": {"mn": 609, "mx": 644},
        "Teknik Informatika": {"mn": 633, "mx": 668},
        "Matematika": {"mn": 583, "mx": 618},
        "Fisika": {"mn": 579, "mx": 614},
        "Kimia": {"mn": 575, "mx": 610},
        "Biologi": {"mn": 573, "mx": 608},
        "Statistika": {"mn": 587, "mx": 622},
        "Aktuaria": {"mn": 590, "mx": 625},
        "Farmasi": {"mn": 621, "mx": 656},
        "Gizi": {"mn": 559, "mx": 594},
        "Keperawatan": {"mn": 555, "mx": 590},
        "Kesehatan Masyarakat": {"mn": 547, "mx": 582},
        "Ilmu Hukum": {"mn": 617, "mx": 652},
        "Ekonomi": {"mn": 599, "mx": 634},
        "Manajemen": {"mn": 607, "mx": 642},
        "Akuntansi": {"mn": 613, "mx": 648},
        "Bisnis": {"mn": 593, "mx": 628},
        "Psikologi": {"mn": 625, "mx": 660},
        "Ilmu Komunikasi": {"mn": 605, "mx": 640},
        "Hubungan Internasional": {"mn": 597, "mx": 632},
        "Administrasi Publik": {"mn": 531, "mx": 566},
        "Sastra Inggris": {"mn": 563, "mx": 598},
        "Pendidikan Bahasa Indonesia": {"mn": 557, "mx": 592},
        "Pendidikan Bahasa Inggris": {"mn": 555, "mx": 590},
        "Sosiologi": {"mn": 583, "mx": 618},
        "Ilmu Politik": {"mn": 589, "mx": 624},
        "Sejarah": {"mn": 565, "mx": 600},
        "Geografi": {"mn": 578, "mx": 613},
        "_default": {"mn": 589, "mx": 624},
    },
    "Universitas Muhammadiyah Malang (UMM)": {
        "_klaster": 4,
        "_lbl": '🔸 Klaster 4 — Regional',
        "Kedokteran": {"mn": 600, "mx": 635},
        "Kedokteran Gigi": {"mn": 561, "mx": 596},
        "Teknik Sipil": {"mn": 563, "mx": 598},
        "Teknik Mesin": {"mn": 566, "mx": 601},
        "Teknik Elektro": {"mn": 577, "mx": 612},
        "Teknik Industri": {"mn": 553, "mx": 588},
        "Teknik Kimia": {"mn": 570, "mx": 605},
        "Teknik Informatika": {"mn": 593, "mx": 628},
        "Matematika": {"mn": 546, "mx": 581},
        "Fisika": {"mn": 541, "mx": 576},
        "Kimia": {"mn": 539, "mx": 574},
        "Biologi": {"mn": 536, "mx": 571},
        "Statistika": {"mn": 549, "mx": 584},
        "Aktuaria": {"mn": 552, "mx": 587},
        "Farmasi": {"mn": 581, "mx": 616},
        "Gizi": {"mn": 523, "mx": 558},
        "Keperawatan": {"mn": 519, "mx": 554},
        "Kesehatan Masyarakat": {"mn": 511, "mx": 546},
        "Ilmu Hukum": {"mn": 577, "mx": 612},
        "Ekonomi": {"mn": 561, "mx": 596},
        "Manajemen": {"mn": 569, "mx": 604},
        "Akuntansi": {"mn": 574, "mx": 609},
        "Bisnis": {"mn": 555, "mx": 590},
        "Psikologi": {"mn": 585, "mx": 620},
        "Ilmu Komunikasi": {"mn": 566, "mx": 601},
        "Hubungan Internasional": {"mn": 559, "mx": 594},
        "Administrasi Publik": {"mn": 497, "mx": 532},
        "Sastra Inggris": {"mn": 527, "mx": 562},
        "Pendidikan Bahasa Indonesia": {"mn": 521, "mx": 556},
        "Pendidikan Bahasa Inggris": {"mn": 519, "mx": 554},
        "Sosiologi": {"mn": 546, "mx": 581},
        "Ilmu Politik": {"mn": 551, "mx": 586},
        "Sejarah": {"mn": 529, "mx": 564},
        "Geografi": {"mn": 541, "mx": 576},
        "_default": {"mn": 551, "mx": 586},
    },
}

# ══════════════════════════════════════════════════════════
# D3 PTN DATA — 30 PTN | D3 Skor aman per prodi
# ══════════════════════════════════════════════════════════
PTN_D3_DATA = {
    "Universitas Indonesia (UI)": {
        "_klaster": 1,
        "_lbl": '⭐ Klaster 1 — Top Tier',
        "D3 Teknik Sipil": {"mn": 675, "mx": 710},
        "D3 Teknik Mesin": {"mn": 680, "mx": 715},
        "D3 Teknik Elektro": {"mn": 695, "mx": 730},
        "D3 Teknik Kimia": {"mn": 685, "mx": 720},
        "D3 Teknik Komputer": {"mn": 710, "mx": 745},
        "D3 Teknologi Informasi": {"mn": 712, "mx": 747},
        "D3 Teknik Mekatronika": {"mn": 678, "mx": 713},
        "D3 Manajemen": {"mn": 683, "mx": 718},
        "D3 Akuntansi": {"mn": 690, "mx": 725},
        "D3 Administrasi Bisnis": {"mn": 665, "mx": 700},
        "D3 Perbankan & Keuangan": {"mn": 687, "mx": 722},
        "D3 Manajemen Pemasaran": {"mn": 680, "mx": 715},
        "D3 Perpajakan": {"mn": 685, "mx": 720},
        "D3 Keperawatan": {"mn": 617, "mx": 652},
        "D3 Kebidanan": {"mn": 612, "mx": 647},
        "D3 Farmasi": {"mn": 700, "mx": 735},
        "D3 Gizi": {"mn": 623, "mx": 658},
        "D3 Analis Kesehatan": {"mn": 695, "mx": 730},
        "D3 Rekam Medis": {"mn": 601, "mx": 636},
        "D3 Fisioterapi": {"mn": 614, "mx": 649},
        "D3 Radiologi": {"mn": 692, "mx": 727},
        "D3 Komunikasi": {"mn": 680, "mx": 715},
        "D3 Hubungan Masyarakat": {"mn": 677, "mx": 712},
        "D3 Desain Grafis": {"mn": 670, "mx": 705},
        "D3 Animasi": {"mn": 707, "mx": 742},
        "D3 Pariwisata": {"mn": 657, "mx": 692},
        "D3 Perhotelan": {"mn": 655, "mx": 690},
        "D3 Bahasa Inggris": {"mn": 622, "mx": 657},
        "D3 Agribisnis": {"mn": 635, "mx": 670},
        "D3 Teknologi Pangan": {"mn": 618, "mx": 653},
        "_default": {"mn": 666, "mx": 701},
    },
    "Universitas Gadjah Mada (UGM)": {
        "_klaster": 1,
        "_lbl": '⭐ Klaster 1 — Top Tier',
        "D3 Teknik Sipil": {"mn": 675, "mx": 710},
        "D3 Teknik Mesin": {"mn": 680, "mx": 715},
        "D3 Teknik Elektro": {"mn": 695, "mx": 730},
        "D3 Teknik Kimia": {"mn": 685, "mx": 720},
        "D3 Teknik Komputer": {"mn": 710, "mx": 745},
        "D3 Teknologi Informasi": {"mn": 712, "mx": 747},
        "D3 Teknik Mekatronika": {"mn": 678, "mx": 713},
        "D3 Manajemen": {"mn": 683, "mx": 718},
        "D3 Akuntansi": {"mn": 690, "mx": 725},
        "D3 Administrasi Bisnis": {"mn": 665, "mx": 700},
        "D3 Perbankan & Keuangan": {"mn": 687, "mx": 722},
        "D3 Manajemen Pemasaran": {"mn": 680, "mx": 715},
        "D3 Perpajakan": {"mn": 685, "mx": 720},
        "D3 Keperawatan": {"mn": 617, "mx": 652},
        "D3 Kebidanan": {"mn": 612, "mx": 647},
        "D3 Farmasi": {"mn": 700, "mx": 735},
        "D3 Gizi": {"mn": 623, "mx": 658},
        "D3 Analis Kesehatan": {"mn": 695, "mx": 730},
        "D3 Rekam Medis": {"mn": 601, "mx": 636},
        "D3 Fisioterapi": {"mn": 614, "mx": 649},
        "D3 Radiologi": {"mn": 692, "mx": 727},
        "D3 Komunikasi": {"mn": 680, "mx": 715},
        "D3 Hubungan Masyarakat": {"mn": 677, "mx": 712},
        "D3 Desain Grafis": {"mn": 670, "mx": 705},
        "D3 Animasi": {"mn": 707, "mx": 742},
        "D3 Pariwisata": {"mn": 657, "mx": 692},
        "D3 Perhotelan": {"mn": 655, "mx": 690},
        "D3 Bahasa Inggris": {"mn": 622, "mx": 657},
        "D3 Agribisnis": {"mn": 635, "mx": 670},
        "D3 Teknologi Pangan": {"mn": 618, "mx": 653},
        "_default": {"mn": 666, "mx": 701},
    },
    "Universitas Airlangga (Unair)": {
        "_klaster": 2,
        "_lbl": '🔷 Klaster 2 — Menengah Atas',
        "D3 Teknik Sipil": {"mn": 667, "mx": 702},
        "D3 Teknik Mesin": {"mn": 672, "mx": 707},
        "D3 Teknik Elektro": {"mn": 686, "mx": 721},
        "D3 Teknik Kimia": {"mn": 677, "mx": 712},
        "D3 Teknik Komputer": {"mn": 701, "mx": 736},
        "D3 Teknologi Informasi": {"mn": 703, "mx": 738},
        "D3 Teknik Mekatronika": {"mn": 670, "mx": 705},
        "D3 Manajemen": {"mn": 675, "mx": 710},
        "D3 Akuntansi": {"mn": 681, "mx": 716},
        "D3 Administrasi Bisnis": {"mn": 657, "mx": 692},
        "D3 Perbankan & Keuangan": {"mn": 678, "mx": 713},
        "D3 Manajemen Pemasaran": {"mn": 672, "mx": 707},
        "D3 Perpajakan": {"mn": 676, "mx": 711},
        "D3 Keperawatan": {"mn": 611, "mx": 646},
        "D3 Kebidanan": {"mn": 606, "mx": 641},
        "D3 Farmasi": {"mn": 691, "mx": 726},
        "D3 Gizi": {"mn": 616, "mx": 651},
        "D3 Analis Kesehatan": {"mn": 686, "mx": 721},
        "D3 Rekam Medis": {"mn": 595, "mx": 630},
        "D3 Fisioterapi": {"mn": 608, "mx": 643},
        "D3 Radiologi": {"mn": 683, "mx": 718},
        "D3 Komunikasi": {"mn": 672, "mx": 707},
        "D3 Hubungan Masyarakat": {"mn": 669, "mx": 704},
        "D3 Desain Grafis": {"mn": 662, "mx": 697},
        "D3 Animasi": {"mn": 698, "mx": 733},
        "D3 Pariwisata": {"mn": 649, "mx": 684},
        "D3 Perhotelan": {"mn": 647, "mx": 682},
        "D3 Bahasa Inggris": {"mn": 615, "mx": 650},
        "D3 Agribisnis": {"mn": 628, "mx": 663},
        "D3 Teknologi Pangan": {"mn": 611, "mx": 646},
        "_default": {"mn": 658, "mx": 693},
    },
    "Institut Teknologi Bandung (ITB)": {
        "_klaster": 1,
        "_lbl": '⭐ Klaster 1 — Top Tier',
        "D3 Teknik Sipil": {"mn": 680, "mx": 715},
        "D3 Teknik Mesin": {"mn": 685, "mx": 720},
        "D3 Teknik Elektro": {"mn": 700, "mx": 735},
        "D3 Teknik Kimia": {"mn": 690, "mx": 725},
        "D3 Teknik Komputer": {"mn": 715, "mx": 750},
        "D3 Teknologi Informasi": {"mn": 717, "mx": 752},
        "D3 Teknik Mekatronika": {"mn": 683, "mx": 718},
        "D3 Manajemen": {"mn": 688, "mx": 723},
        "D3 Akuntansi": {"mn": 695, "mx": 730},
        "D3 Administrasi Bisnis": {"mn": 670, "mx": 705},
        "D3 Perbankan & Keuangan": {"mn": 692, "mx": 727},
        "D3 Manajemen Pemasaran": {"mn": 685, "mx": 720},
        "D3 Perpajakan": {"mn": 690, "mx": 725},
        "D3 Keperawatan": {"mn": 622, "mx": 657},
        "D3 Kebidanan": {"mn": 617, "mx": 652},
        "D3 Farmasi": {"mn": 705, "mx": 740},
        "D3 Gizi": {"mn": 628, "mx": 663},
        "D3 Analis Kesehatan": {"mn": 700, "mx": 735},
        "D3 Rekam Medis": {"mn": 606, "mx": 641},
        "D3 Fisioterapi": {"mn": 619, "mx": 654},
        "D3 Radiologi": {"mn": 697, "mx": 732},
        "D3 Komunikasi": {"mn": 685, "mx": 720},
        "D3 Hubungan Masyarakat": {"mn": 682, "mx": 717},
        "D3 Desain Grafis": {"mn": 675, "mx": 710},
        "D3 Animasi": {"mn": 712, "mx": 747},
        "D3 Pariwisata": {"mn": 662, "mx": 697},
        "D3 Perhotelan": {"mn": 660, "mx": 695},
        "D3 Bahasa Inggris": {"mn": 627, "mx": 662},
        "D3 Agribisnis": {"mn": 640, "mx": 675},
        "D3 Teknologi Pangan": {"mn": 623, "mx": 658},
        "_default": {"mn": 671, "mx": 706},
    },
    "Universitas Padjadjaran (Unpad)": {
        "_klaster": 1,
        "_lbl": '⭐ Klaster 1 — Top Tier',
        "D3 Teknik Sipil": {"mn": 636, "mx": 671},
        "D3 Teknik Mesin": {"mn": 641, "mx": 676},
        "D3 Teknik Elektro": {"mn": 655, "mx": 690},
        "D3 Teknik Kimia": {"mn": 645, "mx": 680},
        "D3 Teknik Komputer": {"mn": 668, "mx": 703},
        "D3 Teknologi Informasi": {"mn": 670, "mx": 705},
        "D3 Teknik Mekatronika": {"mn": 639, "mx": 674},
        "D3 Manajemen": {"mn": 644, "mx": 679},
        "D3 Akuntansi": {"mn": 650, "mx": 685},
        "D3 Administrasi Bisnis": {"mn": 627, "mx": 662},
        "D3 Perbankan & Keuangan": {"mn": 647, "mx": 682},
        "D3 Manajemen Pemasaran": {"mn": 641, "mx": 676},
        "D3 Perpajakan": {"mn": 645, "mx": 680},
        "D3 Keperawatan": {"mn": 582, "mx": 617},
        "D3 Kebidanan": {"mn": 577, "mx": 612},
        "D3 Farmasi": {"mn": 659, "mx": 694},
        "D3 Gizi": {"mn": 588, "mx": 623},
        "D3 Analis Kesehatan": {"mn": 654, "mx": 689},
        "D3 Rekam Medis": {"mn": 566, "mx": 601},
        "D3 Fisioterapi": {"mn": 579, "mx": 614},
        "D3 Radiologi": {"mn": 651, "mx": 686},
        "D3 Komunikasi": {"mn": 641, "mx": 676},
        "D3 Hubungan Masyarakat": {"mn": 638, "mx": 673},
        "D3 Desain Grafis": {"mn": 631, "mx": 666},
        "D3 Animasi": {"mn": 665, "mx": 700},
        "D3 Pariwisata": {"mn": 619, "mx": 654},
        "D3 Perhotelan": {"mn": 617, "mx": 652},
        "D3 Bahasa Inggris": {"mn": 586, "mx": 621},
        "D3 Agribisnis": {"mn": 599, "mx": 634},
        "D3 Teknologi Pangan": {"mn": 583, "mx": 618},
        "_default": {"mn": 628, "mx": 663},
    },
    "Institut Pertanian Bogor (IPB)": {
        "_klaster": 1,
        "_lbl": '⭐ Klaster 1 — Top Tier',
        "D3 Teknik Sipil": {"mn": 626, "mx": 661},
        "D3 Teknik Mesin": {"mn": 630, "mx": 665},
        "D3 Teknik Elektro": {"mn": 644, "mx": 679},
        "D3 Teknik Kimia": {"mn": 635, "mx": 670},
        "D3 Teknik Komputer": {"mn": 657, "mx": 692},
        "D3 Teknologi Informasi": {"mn": 659, "mx": 694},
        "D3 Teknik Mekatronika": {"mn": 628, "mx": 663},
        "D3 Manajemen": {"mn": 633, "mx": 668},
        "D3 Akuntansi": {"mn": 639, "mx": 674},
        "D3 Administrasi Bisnis": {"mn": 617, "mx": 652},
        "D3 Perbankan & Keuangan": {"mn": 636, "mx": 671},
        "D3 Manajemen Pemasaran": {"mn": 630, "mx": 665},
        "D3 Perpajakan": {"mn": 634, "mx": 669},
        "D3 Keperawatan": {"mn": 573, "mx": 608},
        "D3 Kebidanan": {"mn": 568, "mx": 603},
        "D3 Farmasi": {"mn": 648, "mx": 683},
        "D3 Gizi": {"mn": 578, "mx": 613},
        "D3 Analis Kesehatan": {"mn": 643, "mx": 678},
        "D3 Rekam Medis": {"mn": 557, "mx": 592},
        "D3 Fisioterapi": {"mn": 570, "mx": 605},
        "D3 Radiologi": {"mn": 640, "mx": 675},
        "D3 Komunikasi": {"mn": 630, "mx": 665},
        "D3 Hubungan Masyarakat": {"mn": 627, "mx": 662},
        "D3 Desain Grafis": {"mn": 620, "mx": 655},
        "D3 Animasi": {"mn": 654, "mx": 689},
        "D3 Pariwisata": {"mn": 609, "mx": 644},
        "D3 Perhotelan": {"mn": 607, "mx": 642},
        "D3 Bahasa Inggris": {"mn": 577, "mx": 612},
        "D3 Agribisnis": {"mn": 589, "mx": 624},
        "D3 Teknologi Pangan": {"mn": 573, "mx": 608},
        "_default": {"mn": 617, "mx": 652},
    },
    "Institut Teknologi Sepuluh Nopember (ITS)": {
        "_klaster": 2,
        "_lbl": '🔷 Klaster 2 — Menengah Atas',
        "D3 Teknik Sipil": {"mn": 628, "mx": 663},
        "D3 Teknik Mesin": {"mn": 633, "mx": 668},
        "D3 Teknik Elektro": {"mn": 647, "mx": 682},
        "D3 Teknik Kimia": {"mn": 638, "mx": 673},
        "D3 Teknik Komputer": {"mn": 660, "mx": 695},
        "D3 Teknologi Informasi": {"mn": 662, "mx": 697},
        "D3 Teknik Mekatronika": {"mn": 631, "mx": 666},
        "D3 Manajemen": {"mn": 636, "mx": 671},
        "D3 Akuntansi": {"mn": 642, "mx": 677},
        "D3 Administrasi Bisnis": {"mn": 619, "mx": 654},
        "D3 Perbankan & Keuangan": {"mn": 639, "mx": 674},
        "D3 Manajemen Pemasaran": {"mn": 633, "mx": 668},
        "D3 Perpajakan": {"mn": 637, "mx": 672},
        "D3 Keperawatan": {"mn": 575, "mx": 610},
        "D3 Kebidanan": {"mn": 570, "mx": 605},
        "D3 Farmasi": {"mn": 651, "mx": 686},
        "D3 Gizi": {"mn": 581, "mx": 616},
        "D3 Analis Kesehatan": {"mn": 646, "mx": 681},
        "D3 Rekam Medis": {"mn": 559, "mx": 594},
        "D3 Fisioterapi": {"mn": 572, "mx": 607},
        "D3 Radiologi": {"mn": 643, "mx": 678},
        "D3 Komunikasi": {"mn": 633, "mx": 668},
        "D3 Hubungan Masyarakat": {"mn": 630, "mx": 665},
        "D3 Desain Grafis": {"mn": 623, "mx": 658},
        "D3 Animasi": {"mn": 657, "mx": 692},
        "D3 Pariwisata": {"mn": 611, "mx": 646},
        "D3 Perhotelan": {"mn": 609, "mx": 644},
        "D3 Bahasa Inggris": {"mn": 579, "mx": 614},
        "D3 Agribisnis": {"mn": 591, "mx": 626},
        "D3 Teknologi Pangan": {"mn": 576, "mx": 611},
        "_default": {"mn": 620, "mx": 655},
    },
    "Universitas Diponegoro (Undip)": {
        "_klaster": 2,
        "_lbl": '🔷 Klaster 2 — Menengah Atas',
        "D3 Teknik Sipil": {"mn": 626, "mx": 661},
        "D3 Teknik Mesin": {"mn": 630, "mx": 665},
        "D3 Teknik Elektro": {"mn": 644, "mx": 679},
        "D3 Teknik Kimia": {"mn": 635, "mx": 670},
        "D3 Teknik Komputer": {"mn": 657, "mx": 692},
        "D3 Teknologi Informasi": {"mn": 659, "mx": 694},
        "D3 Teknik Mekatronika": {"mn": 628, "mx": 663},
        "D3 Manajemen": {"mn": 633, "mx": 668},
        "D3 Akuntansi": {"mn": 639, "mx": 674},
        "D3 Administrasi Bisnis": {"mn": 617, "mx": 652},
        "D3 Perbankan & Keuangan": {"mn": 636, "mx": 671},
        "D3 Manajemen Pemasaran": {"mn": 630, "mx": 665},
        "D3 Perpajakan": {"mn": 634, "mx": 669},
        "D3 Keperawatan": {"mn": 573, "mx": 608},
        "D3 Kebidanan": {"mn": 568, "mx": 603},
        "D3 Farmasi": {"mn": 648, "mx": 683},
        "D3 Gizi": {"mn": 578, "mx": 613},
        "D3 Analis Kesehatan": {"mn": 643, "mx": 678},
        "D3 Rekam Medis": {"mn": 557, "mx": 592},
        "D3 Fisioterapi": {"mn": 570, "mx": 605},
        "D3 Radiologi": {"mn": 640, "mx": 675},
        "D3 Komunikasi": {"mn": 630, "mx": 665},
        "D3 Hubungan Masyarakat": {"mn": 627, "mx": 662},
        "D3 Desain Grafis": {"mn": 620, "mx": 655},
        "D3 Animasi": {"mn": 654, "mx": 689},
        "D3 Pariwisata": {"mn": 609, "mx": 644},
        "D3 Perhotelan": {"mn": 607, "mx": 642},
        "D3 Bahasa Inggris": {"mn": 577, "mx": 612},
        "D3 Agribisnis": {"mn": 589, "mx": 624},
        "D3 Teknologi Pangan": {"mn": 573, "mx": 608},
        "_default": {"mn": 617, "mx": 652},
    },
    "Universitas Brawijaya (UB)": {
        "_klaster": 2,
        "_lbl": '🔷 Klaster 2 — Menengah Atas',
        "D3 Teknik Sipil": {"mn": 608, "mx": 643},
        "D3 Teknik Mesin": {"mn": 612, "mx": 647},
        "D3 Teknik Elektro": {"mn": 625, "mx": 660},
        "D3 Teknik Kimia": {"mn": 616, "mx": 651},
        "D3 Teknik Komputer": {"mn": 638, "mx": 673},
        "D3 Teknologi Informasi": {"mn": 640, "mx": 675},
        "D3 Teknik Mekatronika": {"mn": 610, "mx": 645},
        "D3 Manajemen": {"mn": 615, "mx": 650},
        "D3 Akuntansi": {"mn": 621, "mx": 656},
        "D3 Administrasi Bisnis": {"mn": 599, "mx": 634},
        "D3 Perbankan & Keuangan": {"mn": 618, "mx": 653},
        "D3 Manajemen Pemasaran": {"mn": 612, "mx": 647},
        "D3 Perpajakan": {"mn": 616, "mx": 651},
        "D3 Keperawatan": {"mn": 557, "mx": 592},
        "D3 Kebidanan": {"mn": 552, "mx": 587},
        "D3 Farmasi": {"mn": 630, "mx": 665},
        "D3 Gizi": {"mn": 562, "mx": 597},
        "D3 Analis Kesehatan": {"mn": 625, "mx": 660},
        "D3 Rekam Medis": {"mn": 541, "mx": 576},
        "D3 Fisioterapi": {"mn": 554, "mx": 589},
        "D3 Radiologi": {"mn": 622, "mx": 657},
        "D3 Komunikasi": {"mn": 612, "mx": 647},
        "D3 Hubungan Masyarakat": {"mn": 609, "mx": 644},
        "D3 Desain Grafis": {"mn": 602, "mx": 637},
        "D3 Animasi": {"mn": 635, "mx": 670},
        "D3 Pariwisata": {"mn": 591, "mx": 626},
        "D3 Perhotelan": {"mn": 589, "mx": 624},
        "D3 Bahasa Inggris": {"mn": 560, "mx": 595},
        "D3 Agribisnis": {"mn": 572, "mx": 607},
        "D3 Teknologi Pangan": {"mn": 557, "mx": 592},
        "_default": {"mn": 600, "mx": 635},
    },
    "Universitas Sebelas Maret (UNS)": {
        "_klaster": 2,
        "_lbl": '🔷 Klaster 2 — Menengah Atas',
        "D3 Teknik Sipil": {"mn": 600, "mx": 635},
        "D3 Teknik Mesin": {"mn": 604, "mx": 639},
        "D3 Teknik Elektro": {"mn": 617, "mx": 652},
        "D3 Teknik Kimia": {"mn": 609, "mx": 644},
        "D3 Teknik Komputer": {"mn": 630, "mx": 665},
        "D3 Teknologi Informasi": {"mn": 632, "mx": 667},
        "D3 Teknik Mekatronika": {"mn": 602, "mx": 637},
        "D3 Manajemen": {"mn": 607, "mx": 642},
        "D3 Akuntansi": {"mn": 613, "mx": 648},
        "D3 Administrasi Bisnis": {"mn": 591, "mx": 626},
        "D3 Perbankan & Keuangan": {"mn": 610, "mx": 645},
        "D3 Manajemen Pemasaran": {"mn": 604, "mx": 639},
        "D3 Perpajakan": {"mn": 608, "mx": 643},
        "D3 Keperawatan": {"mn": 549, "mx": 584},
        "D3 Kebidanan": {"mn": 544, "mx": 579},
        "D3 Farmasi": {"mn": 622, "mx": 657},
        "D3 Gizi": {"mn": 555, "mx": 590},
        "D3 Analis Kesehatan": {"mn": 617, "mx": 652},
        "D3 Rekam Medis": {"mn": 533, "mx": 568},
        "D3 Fisioterapi": {"mn": 546, "mx": 581},
        "D3 Radiologi": {"mn": 614, "mx": 649},
        "D3 Komunikasi": {"mn": 604, "mx": 639},
        "D3 Hubungan Masyarakat": {"mn": 601, "mx": 636},
        "D3 Desain Grafis": {"mn": 594, "mx": 629},
        "D3 Animasi": {"mn": 627, "mx": 662},
        "D3 Pariwisata": {"mn": 583, "mx": 618},
        "D3 Perhotelan": {"mn": 581, "mx": 616},
        "D3 Bahasa Inggris": {"mn": 553, "mx": 588},
        "D3 Agribisnis": {"mn": 564, "mx": 599},
        "D3 Teknologi Pangan": {"mn": 550, "mx": 585},
        "_default": {"mn": 592, "mx": 627},
    },
    "Universitas Hasanuddin (Unhas)": {
        "_klaster": 2,
        "_lbl": '🔷 Klaster 2 — Menengah Atas',
        "D3 Teknik Sipil": {"mn": 592, "mx": 627},
        "D3 Teknik Mesin": {"mn": 596, "mx": 631},
        "D3 Teknik Elektro": {"mn": 609, "mx": 644},
        "D3 Teknik Kimia": {"mn": 601, "mx": 636},
        "D3 Teknik Komputer": {"mn": 622, "mx": 657},
        "D3 Teknologi Informasi": {"mn": 624, "mx": 659},
        "D3 Teknik Mekatronika": {"mn": 594, "mx": 629},
        "D3 Manajemen": {"mn": 599, "mx": 634},
        "D3 Akuntansi": {"mn": 605, "mx": 640},
        "D3 Administrasi Bisnis": {"mn": 584, "mx": 619},
        "D3 Perbankan & Keuangan": {"mn": 602, "mx": 637},
        "D3 Manajemen Pemasaran": {"mn": 596, "mx": 631},
        "D3 Perpajakan": {"mn": 600, "mx": 635},
        "D3 Keperawatan": {"mn": 542, "mx": 577},
        "D3 Kebidanan": {"mn": 537, "mx": 572},
        "D3 Farmasi": {"mn": 614, "mx": 649},
        "D3 Gizi": {"mn": 547, "mx": 582},
        "D3 Analis Kesehatan": {"mn": 609, "mx": 644},
        "D3 Rekam Medis": {"mn": 526, "mx": 561},
        "D3 Fisioterapi": {"mn": 539, "mx": 574},
        "D3 Radiologi": {"mn": 606, "mx": 641},
        "D3 Komunikasi": {"mn": 596, "mx": 631},
        "D3 Hubungan Masyarakat": {"mn": 593, "mx": 628},
        "D3 Desain Grafis": {"mn": 586, "mx": 621},
        "D3 Animasi": {"mn": 619, "mx": 654},
        "D3 Pariwisata": {"mn": 576, "mx": 611},
        "D3 Perhotelan": {"mn": 574, "mx": 609},
        "D3 Bahasa Inggris": {"mn": 546, "mx": 581},
        "D3 Agribisnis": {"mn": 557, "mx": 592},
        "D3 Teknologi Pangan": {"mn": 542, "mx": 577},
        "_default": {"mn": 584, "mx": 619},
    },
    "Universitas Pendidikan Indonesia (UPI)": {
        "_klaster": 3,
        "_lbl": '🔹 Klaster 3 — Menengah',
        "D3 Teknik Sipil": {"mn": 566, "mx": 601},
        "D3 Teknik Mesin": {"mn": 571, "mx": 606},
        "D3 Teknik Elektro": {"mn": 583, "mx": 618},
        "D3 Teknik Kimia": {"mn": 575, "mx": 610},
        "D3 Teknik Komputer": {"mn": 594, "mx": 629},
        "D3 Teknologi Informasi": {"mn": 596, "mx": 631},
        "D3 Teknik Mekatronika": {"mn": 569, "mx": 604},
        "D3 Manajemen": {"mn": 573, "mx": 608},
        "D3 Akuntansi": {"mn": 579, "mx": 614},
        "D3 Administrasi Bisnis": {"mn": 558, "mx": 593},
        "D3 Perbankan & Keuangan": {"mn": 576, "mx": 611},
        "D3 Manajemen Pemasaran": {"mn": 570, "mx": 605},
        "D3 Perpajakan": {"mn": 574, "mx": 609},
        "D3 Keperawatan": {"mn": 519, "mx": 554},
        "D3 Kebidanan": {"mn": 514, "mx": 549},
        "D3 Farmasi": {"mn": 587, "mx": 622},
        "D3 Gizi": {"mn": 524, "mx": 559},
        "D3 Analis Kesehatan": {"mn": 582, "mx": 617},
        "D3 Rekam Medis": {"mn": 503, "mx": 538},
        "D3 Fisioterapi": {"mn": 516, "mx": 551},
        "D3 Radiologi": {"mn": 579, "mx": 614},
        "D3 Komunikasi": {"mn": 571, "mx": 606},
        "D3 Hubungan Masyarakat": {"mn": 568, "mx": 603},
        "D3 Desain Grafis": {"mn": 561, "mx": 596},
        "D3 Animasi": {"mn": 591, "mx": 626},
        "D3 Pariwisata": {"mn": 550, "mx": 585},
        "D3 Perhotelan": {"mn": 548, "mx": 583},
        "D3 Bahasa Inggris": {"mn": 522, "mx": 557},
        "D3 Agribisnis": {"mn": 533, "mx": 568},
        "D3 Teknologi Pangan": {"mn": 519, "mx": 554},
        "_default": {"mn": 559, "mx": 594},
    },
    "Universitas Sumatera Utara (USU)": {
        "_klaster": 3,
        "_lbl": '🔹 Klaster 3 — Menengah',
        "D3 Teknik Sipil": {"mn": 566, "mx": 601},
        "D3 Teknik Mesin": {"mn": 571, "mx": 606},
        "D3 Teknik Elektro": {"mn": 583, "mx": 618},
        "D3 Teknik Kimia": {"mn": 575, "mx": 610},
        "D3 Teknik Komputer": {"mn": 594, "mx": 629},
        "D3 Teknologi Informasi": {"mn": 596, "mx": 631},
        "D3 Teknik Mekatronika": {"mn": 569, "mx": 604},
        "D3 Manajemen": {"mn": 573, "mx": 608},
        "D3 Akuntansi": {"mn": 579, "mx": 614},
        "D3 Administrasi Bisnis": {"mn": 558, "mx": 593},
        "D3 Perbankan & Keuangan": {"mn": 576, "mx": 611},
        "D3 Manajemen Pemasaran": {"mn": 570, "mx": 605},
        "D3 Perpajakan": {"mn": 574, "mx": 609},
        "D3 Keperawatan": {"mn": 519, "mx": 554},
        "D3 Kebidanan": {"mn": 514, "mx": 549},
        "D3 Farmasi": {"mn": 587, "mx": 622},
        "D3 Gizi": {"mn": 524, "mx": 559},
        "D3 Analis Kesehatan": {"mn": 582, "mx": 617},
        "D3 Rekam Medis": {"mn": 503, "mx": 538},
        "D3 Fisioterapi": {"mn": 516, "mx": 551},
        "D3 Radiologi": {"mn": 579, "mx": 614},
        "D3 Komunikasi": {"mn": 571, "mx": 606},
        "D3 Hubungan Masyarakat": {"mn": 568, "mx": 603},
        "D3 Desain Grafis": {"mn": 561, "mx": 596},
        "D3 Animasi": {"mn": 591, "mx": 626},
        "D3 Pariwisata": {"mn": 550, "mx": 585},
        "D3 Perhotelan": {"mn": 548, "mx": 583},
        "D3 Bahasa Inggris": {"mn": 522, "mx": 557},
        "D3 Agribisnis": {"mn": 533, "mx": 568},
        "D3 Teknologi Pangan": {"mn": 519, "mx": 554},
        "_default": {"mn": 559, "mx": 594},
    },
    "Universitas Negeri Yogyakarta (UNY)": {
        "_klaster": 3,
        "_lbl": '🔹 Klaster 3 — Menengah',
        "D3 Teknik Sipil": {"mn": 566, "mx": 601},
        "D3 Teknik Mesin": {"mn": 571, "mx": 606},
        "D3 Teknik Elektro": {"mn": 583, "mx": 618},
        "D3 Teknik Kimia": {"mn": 575, "mx": 610},
        "D3 Teknik Komputer": {"mn": 594, "mx": 629},
        "D3 Teknologi Informasi": {"mn": 596, "mx": 631},
        "D3 Teknik Mekatronika": {"mn": 569, "mx": 604},
        "D3 Manajemen": {"mn": 573, "mx": 608},
        "D3 Akuntansi": {"mn": 579, "mx": 614},
        "D3 Administrasi Bisnis": {"mn": 558, "mx": 593},
        "D3 Perbankan & Keuangan": {"mn": 576, "mx": 611},
        "D3 Manajemen Pemasaran": {"mn": 570, "mx": 605},
        "D3 Perpajakan": {"mn": 574, "mx": 609},
        "D3 Keperawatan": {"mn": 519, "mx": 554},
        "D3 Kebidanan": {"mn": 514, "mx": 549},
        "D3 Farmasi": {"mn": 587, "mx": 622},
        "D3 Gizi": {"mn": 524, "mx": 559},
        "D3 Analis Kesehatan": {"mn": 582, "mx": 617},
        "D3 Rekam Medis": {"mn": 503, "mx": 538},
        "D3 Fisioterapi": {"mn": 516, "mx": 551},
        "D3 Radiologi": {"mn": 579, "mx": 614},
        "D3 Komunikasi": {"mn": 571, "mx": 606},
        "D3 Hubungan Masyarakat": {"mn": 568, "mx": 603},
        "D3 Desain Grafis": {"mn": 561, "mx": 596},
        "D3 Animasi": {"mn": 591, "mx": 626},
        "D3 Pariwisata": {"mn": 550, "mx": 585},
        "D3 Perhotelan": {"mn": 548, "mx": 583},
        "D3 Bahasa Inggris": {"mn": 522, "mx": 557},
        "D3 Agribisnis": {"mn": 533, "mx": 568},
        "D3 Teknologi Pangan": {"mn": 519, "mx": 554},
        "_default": {"mn": 559, "mx": 594},
    },
    "Universitas Negeri Malang (UM)": {
        "_klaster": 3,
        "_lbl": '🔹 Klaster 3 — Menengah',
        "D3 Teknik Sipil": {"mn": 551, "mx": 586},
        "D3 Teknik Mesin": {"mn": 555, "mx": 590},
        "D3 Teknik Elektro": {"mn": 567, "mx": 602},
        "D3 Teknik Kimia": {"mn": 559, "mx": 594},
        "D3 Teknik Komputer": {"mn": 578, "mx": 613},
        "D3 Teknologi Informasi": {"mn": 580, "mx": 615},
        "D3 Teknik Mekatronika": {"mn": 553, "mx": 588},
        "D3 Manajemen": {"mn": 557, "mx": 592},
        "D3 Akuntansi": {"mn": 563, "mx": 598},
        "D3 Administrasi Bisnis": {"mn": 543, "mx": 578},
        "D3 Perbankan & Keuangan": {"mn": 560, "mx": 595},
        "D3 Manajemen Pemasaran": {"mn": 554, "mx": 589},
        "D3 Perpajakan": {"mn": 558, "mx": 593},
        "D3 Keperawatan": {"mn": 505, "mx": 540},
        "D3 Kebidanan": {"mn": 500, "mx": 535},
        "D3 Farmasi": {"mn": 571, "mx": 606},
        "D3 Gizi": {"mn": 509, "mx": 544},
        "D3 Analis Kesehatan": {"mn": 566, "mx": 601},
        "D3 Rekam Medis": {"mn": 489, "mx": 524},
        "D3 Fisioterapi": {"mn": 502, "mx": 537},
        "D3 Radiologi": {"mn": 563, "mx": 598},
        "D3 Komunikasi": {"mn": 555, "mx": 590},
        "D3 Hubungan Masyarakat": {"mn": 552, "mx": 587},
        "D3 Desain Grafis": {"mn": 545, "mx": 580},
        "D3 Animasi": {"mn": 575, "mx": 610},
        "D3 Pariwisata": {"mn": 535, "mx": 570},
        "D3 Perhotelan": {"mn": 533, "mx": 568},
        "D3 Bahasa Inggris": {"mn": 508, "mx": 543},
        "D3 Agribisnis": {"mn": 518, "mx": 553},
        "D3 Teknologi Pangan": {"mn": 504, "mx": 539},
        "_default": {"mn": 543, "mx": 578},
    },
    "Universitas Lampung (Unila)": {
        "_klaster": 3,
        "_lbl": '🔹 Klaster 3 — Menengah',
        "D3 Teknik Sipil": {"mn": 548, "mx": 583},
        "D3 Teknik Mesin": {"mn": 552, "mx": 587},
        "D3 Teknik Elektro": {"mn": 564, "mx": 599},
        "D3 Teknik Kimia": {"mn": 556, "mx": 591},
        "D3 Teknik Komputer": {"mn": 575, "mx": 610},
        "D3 Teknologi Informasi": {"mn": 577, "mx": 612},
        "D3 Teknik Mekatronika": {"mn": 550, "mx": 585},
        "D3 Manajemen": {"mn": 555, "mx": 590},
        "D3 Akuntansi": {"mn": 560, "mx": 595},
        "D3 Administrasi Bisnis": {"mn": 540, "mx": 575},
        "D3 Perbankan & Keuangan": {"mn": 557, "mx": 592},
        "D3 Manajemen Pemasaran": {"mn": 552, "mx": 587},
        "D3 Perpajakan": {"mn": 555, "mx": 590},
        "D3 Keperawatan": {"mn": 502, "mx": 537},
        "D3 Kebidanan": {"mn": 497, "mx": 532},
        "D3 Farmasi": {"mn": 568, "mx": 603},
        "D3 Gizi": {"mn": 507, "mx": 542},
        "D3 Analis Kesehatan": {"mn": 563, "mx": 598},
        "D3 Rekam Medis": {"mn": 486, "mx": 521},
        "D3 Fisioterapi": {"mn": 499, "mx": 534},
        "D3 Radiologi": {"mn": 560, "mx": 595},
        "D3 Komunikasi": {"mn": 552, "mx": 587},
        "D3 Hubungan Masyarakat": {"mn": 549, "mx": 584},
        "D3 Desain Grafis": {"mn": 542, "mx": 577},
        "D3 Animasi": {"mn": 572, "mx": 607},
        "D3 Pariwisata": {"mn": 532, "mx": 567},
        "D3 Perhotelan": {"mn": 530, "mx": 565},
        "D3 Bahasa Inggris": {"mn": 505, "mx": 540},
        "D3 Agribisnis": {"mn": 516, "mx": 551},
        "D3 Teknologi Pangan": {"mn": 502, "mx": 537},
        "_default": {"mn": 540, "mx": 575},
    },
    "Universitas Andalas (Unand)": {
        "_klaster": 3,
        "_lbl": '🔹 Klaster 3 — Menengah',
        "D3 Teknik Sipil": {"mn": 559, "mx": 594},
        "D3 Teknik Mesin": {"mn": 563, "mx": 598},
        "D3 Teknik Elektro": {"mn": 575, "mx": 610},
        "D3 Teknik Kimia": {"mn": 567, "mx": 602},
        "D3 Teknik Komputer": {"mn": 586, "mx": 621},
        "D3 Teknologi Informasi": {"mn": 588, "mx": 623},
        "D3 Teknik Mekatronika": {"mn": 561, "mx": 596},
        "D3 Manajemen": {"mn": 565, "mx": 600},
        "D3 Akuntansi": {"mn": 571, "mx": 606},
        "D3 Administrasi Bisnis": {"mn": 551, "mx": 586},
        "D3 Perbankan & Keuangan": {"mn": 568, "mx": 603},
        "D3 Manajemen Pemasaran": {"mn": 562, "mx": 597},
        "D3 Perpajakan": {"mn": 566, "mx": 601},
        "D3 Keperawatan": {"mn": 512, "mx": 547},
        "D3 Kebidanan": {"mn": 507, "mx": 542},
        "D3 Farmasi": {"mn": 579, "mx": 614},
        "D3 Gizi": {"mn": 517, "mx": 552},
        "D3 Analis Kesehatan": {"mn": 574, "mx": 609},
        "D3 Rekam Medis": {"mn": 496, "mx": 531},
        "D3 Fisioterapi": {"mn": 509, "mx": 544},
        "D3 Radiologi": {"mn": 571, "mx": 606},
        "D3 Komunikasi": {"mn": 563, "mx": 598},
        "D3 Hubungan Masyarakat": {"mn": 560, "mx": 595},
        "D3 Desain Grafis": {"mn": 553, "mx": 588},
        "D3 Animasi": {"mn": 583, "mx": 618},
        "D3 Pariwisata": {"mn": 543, "mx": 578},
        "D3 Perhotelan": {"mn": 541, "mx": 576},
        "D3 Bahasa Inggris": {"mn": 515, "mx": 550},
        "D3 Agribisnis": {"mn": 525, "mx": 560},
        "D3 Teknologi Pangan": {"mn": 512, "mx": 547},
        "_default": {"mn": 551, "mx": 586},
    },
    "Universitas Negeri Semarang (UNNES)": {
        "_klaster": 3,
        "_lbl": '🔹 Klaster 3 — Menengah',
        "D3 Teknik Sipil": {"mn": 551, "mx": 586},
        "D3 Teknik Mesin": {"mn": 555, "mx": 590},
        "D3 Teknik Elektro": {"mn": 567, "mx": 602},
        "D3 Teknik Kimia": {"mn": 559, "mx": 594},
        "D3 Teknik Komputer": {"mn": 578, "mx": 613},
        "D3 Teknologi Informasi": {"mn": 580, "mx": 615},
        "D3 Teknik Mekatronika": {"mn": 553, "mx": 588},
        "D3 Manajemen": {"mn": 557, "mx": 592},
        "D3 Akuntansi": {"mn": 563, "mx": 598},
        "D3 Administrasi Bisnis": {"mn": 543, "mx": 578},
        "D3 Perbankan & Keuangan": {"mn": 560, "mx": 595},
        "D3 Manajemen Pemasaran": {"mn": 554, "mx": 589},
        "D3 Perpajakan": {"mn": 558, "mx": 593},
        "D3 Keperawatan": {"mn": 505, "mx": 540},
        "D3 Kebidanan": {"mn": 500, "mx": 535},
        "D3 Farmasi": {"mn": 571, "mx": 606},
        "D3 Gizi": {"mn": 509, "mx": 544},
        "D3 Analis Kesehatan": {"mn": 566, "mx": 601},
        "D3 Rekam Medis": {"mn": 489, "mx": 524},
        "D3 Fisioterapi": {"mn": 502, "mx": 537},
        "D3 Radiologi": {"mn": 563, "mx": 598},
        "D3 Komunikasi": {"mn": 555, "mx": 590},
        "D3 Hubungan Masyarakat": {"mn": 552, "mx": 587},
        "D3 Desain Grafis": {"mn": 545, "mx": 580},
        "D3 Animasi": {"mn": 575, "mx": 610},
        "D3 Pariwisata": {"mn": 535, "mx": 570},
        "D3 Perhotelan": {"mn": 533, "mx": 568},
        "D3 Bahasa Inggris": {"mn": 508, "mx": 543},
        "D3 Agribisnis": {"mn": 518, "mx": 553},
        "D3 Teknologi Pangan": {"mn": 504, "mx": 539},
        "_default": {"mn": 543, "mx": 578},
    },
    "Universitas Syiah Kuala (USK)": {
        "_klaster": 4,
        "_lbl": '🔸 Klaster 4 — Regional',
        "D3 Teknik Sipil": {"mn": 548, "mx": 583},
        "D3 Teknik Mesin": {"mn": 552, "mx": 587},
        "D3 Teknik Elektro": {"mn": 564, "mx": 599},
        "D3 Teknik Kimia": {"mn": 556, "mx": 591},
        "D3 Teknik Komputer": {"mn": 575, "mx": 610},
        "D3 Teknologi Informasi": {"mn": 577, "mx": 612},
        "D3 Teknik Mekatronika": {"mn": 550, "mx": 585},
        "D3 Manajemen": {"mn": 555, "mx": 590},
        "D3 Akuntansi": {"mn": 560, "mx": 595},
        "D3 Administrasi Bisnis": {"mn": 540, "mx": 575},
        "D3 Perbankan & Keuangan": {"mn": 557, "mx": 592},
        "D3 Manajemen Pemasaran": {"mn": 552, "mx": 587},
        "D3 Perpajakan": {"mn": 555, "mx": 590},
        "D3 Keperawatan": {"mn": 502, "mx": 537},
        "D3 Kebidanan": {"mn": 497, "mx": 532},
        "D3 Farmasi": {"mn": 568, "mx": 603},
        "D3 Gizi": {"mn": 507, "mx": 542},
        "D3 Analis Kesehatan": {"mn": 563, "mx": 598},
        "D3 Rekam Medis": {"mn": 486, "mx": 521},
        "D3 Fisioterapi": {"mn": 499, "mx": 534},
        "D3 Radiologi": {"mn": 560, "mx": 595},
        "D3 Komunikasi": {"mn": 552, "mx": 587},
        "D3 Hubungan Masyarakat": {"mn": 549, "mx": 584},
        "D3 Desain Grafis": {"mn": 542, "mx": 577},
        "D3 Animasi": {"mn": 572, "mx": 607},
        "D3 Pariwisata": {"mn": 532, "mx": 567},
        "D3 Perhotelan": {"mn": 530, "mx": 565},
        "D3 Bahasa Inggris": {"mn": 505, "mx": 540},
        "D3 Agribisnis": {"mn": 516, "mx": 551},
        "D3 Teknologi Pangan": {"mn": 502, "mx": 537},
        "_default": {"mn": 540, "mx": 575},
    },
    "Universitas Mulawarman (Unmul)": {
        "_klaster": 4,
        "_lbl": '🔸 Klaster 4 — Regional',
        "D3 Teknik Sipil": {"mn": 533, "mx": 568},
        "D3 Teknik Mesin": {"mn": 537, "mx": 572},
        "D3 Teknik Elektro": {"mn": 548, "mx": 583},
        "D3 Teknik Kimia": {"mn": 541, "mx": 576},
        "D3 Teknik Komputer": {"mn": 559, "mx": 594},
        "D3 Teknologi Informasi": {"mn": 561, "mx": 596},
        "D3 Teknik Mekatronika": {"mn": 535, "mx": 570},
        "D3 Manajemen": {"mn": 539, "mx": 574},
        "D3 Akuntansi": {"mn": 544, "mx": 579},
        "D3 Administrasi Bisnis": {"mn": 525, "mx": 560},
        "D3 Perbankan & Keuangan": {"mn": 541, "mx": 576},
        "D3 Manajemen Pemasaran": {"mn": 536, "mx": 571},
        "D3 Perpajakan": {"mn": 539, "mx": 574},
        "D3 Keperawatan": {"mn": 488, "mx": 523},
        "D3 Kebidanan": {"mn": 483, "mx": 518},
        "D3 Farmasi": {"mn": 552, "mx": 587},
        "D3 Gizi": {"mn": 493, "mx": 528},
        "D3 Analis Kesehatan": {"mn": 547, "mx": 582},
        "D3 Rekam Medis": {"mn": 472, "mx": 507},
        "D3 Fisioterapi": {"mn": 485, "mx": 520},
        "D3 Radiologi": {"mn": 544, "mx": 579},
        "D3 Komunikasi": {"mn": 537, "mx": 572},
        "D3 Hubungan Masyarakat": {"mn": 534, "mx": 569},
        "D3 Desain Grafis": {"mn": 527, "mx": 562},
        "D3 Animasi": {"mn": 556, "mx": 591},
        "D3 Pariwisata": {"mn": 517, "mx": 552},
        "D3 Perhotelan": {"mn": 515, "mx": 550},
        "D3 Bahasa Inggris": {"mn": 491, "mx": 526},
        "D3 Agribisnis": {"mn": 501, "mx": 536},
        "D3 Teknologi Pangan": {"mn": 488, "mx": 523},
        "_default": {"mn": 525, "mx": 560},
    },
    "Universitas Sriwijaya (Unsri)": {
        "_klaster": 4,
        "_lbl": '🔸 Klaster 4 — Regional',
        "D3 Teknik Sipil": {"mn": 548, "mx": 583},
        "D3 Teknik Mesin": {"mn": 552, "mx": 587},
        "D3 Teknik Elektro": {"mn": 564, "mx": 599},
        "D3 Teknik Kimia": {"mn": 556, "mx": 591},
        "D3 Teknik Komputer": {"mn": 575, "mx": 610},
        "D3 Teknologi Informasi": {"mn": 577, "mx": 612},
        "D3 Teknik Mekatronika": {"mn": 550, "mx": 585},
        "D3 Manajemen": {"mn": 555, "mx": 590},
        "D3 Akuntansi": {"mn": 560, "mx": 595},
        "D3 Administrasi Bisnis": {"mn": 540, "mx": 575},
        "D3 Perbankan & Keuangan": {"mn": 557, "mx": 592},
        "D3 Manajemen Pemasaran": {"mn": 552, "mx": 587},
        "D3 Perpajakan": {"mn": 555, "mx": 590},
        "D3 Keperawatan": {"mn": 502, "mx": 537},
        "D3 Kebidanan": {"mn": 497, "mx": 532},
        "D3 Farmasi": {"mn": 568, "mx": 603},
        "D3 Gizi": {"mn": 507, "mx": 542},
        "D3 Analis Kesehatan": {"mn": 563, "mx": 598},
        "D3 Rekam Medis": {"mn": 486, "mx": 521},
        "D3 Fisioterapi": {"mn": 499, "mx": 534},
        "D3 Radiologi": {"mn": 560, "mx": 595},
        "D3 Komunikasi": {"mn": 552, "mx": 587},
        "D3 Hubungan Masyarakat": {"mn": 549, "mx": 584},
        "D3 Desain Grafis": {"mn": 542, "mx": 577},
        "D3 Animasi": {"mn": 572, "mx": 607},
        "D3 Pariwisata": {"mn": 532, "mx": 567},
        "D3 Perhotelan": {"mn": 530, "mx": 565},
        "D3 Bahasa Inggris": {"mn": 505, "mx": 540},
        "D3 Agribisnis": {"mn": 516, "mx": 551},
        "D3 Teknologi Pangan": {"mn": 502, "mx": 537},
        "_default": {"mn": 540, "mx": 575},
    },
    "Universitas Udayana (Unud)": {
        "_klaster": 4,
        "_lbl": '🔸 Klaster 4 — Regional',
        "D3 Teknik Sipil": {"mn": 574, "mx": 609},
        "D3 Teknik Mesin": {"mn": 578, "mx": 613},
        "D3 Teknik Elektro": {"mn": 591, "mx": 626},
        "D3 Teknik Kimia": {"mn": 582, "mx": 617},
        "D3 Teknik Komputer": {"mn": 602, "mx": 637},
        "D3 Teknologi Informasi": {"mn": 604, "mx": 639},
        "D3 Teknik Mekatronika": {"mn": 576, "mx": 611},
        "D3 Manajemen": {"mn": 581, "mx": 616},
        "D3 Akuntansi": {"mn": 587, "mx": 622},
        "D3 Administrasi Bisnis": {"mn": 566, "mx": 601},
        "D3 Perbankan & Keuangan": {"mn": 584, "mx": 619},
        "D3 Manajemen Pemasaran": {"mn": 578, "mx": 613},
        "D3 Perpajakan": {"mn": 582, "mx": 617},
        "D3 Keperawatan": {"mn": 526, "mx": 561},
        "D3 Kebidanan": {"mn": 521, "mx": 556},
        "D3 Farmasi": {"mn": 595, "mx": 630},
        "D3 Gizi": {"mn": 531, "mx": 566},
        "D3 Analis Kesehatan": {"mn": 590, "mx": 625},
        "D3 Rekam Medis": {"mn": 510, "mx": 545},
        "D3 Fisioterapi": {"mn": 523, "mx": 558},
        "D3 Radiologi": {"mn": 587, "mx": 622},
        "D3 Komunikasi": {"mn": 578, "mx": 613},
        "D3 Hubungan Masyarakat": {"mn": 575, "mx": 610},
        "D3 Desain Grafis": {"mn": 568, "mx": 603},
        "D3 Animasi": {"mn": 599, "mx": 634},
        "D3 Pariwisata": {"mn": 558, "mx": 593},
        "D3 Perhotelan": {"mn": 556, "mx": 591},
        "D3 Bahasa Inggris": {"mn": 529, "mx": 564},
        "D3 Agribisnis": {"mn": 540, "mx": 575},
        "D3 Teknologi Pangan": {"mn": 526, "mx": 561},
        "_default": {"mn": 566, "mx": 601},
    },
    "Universitas Sam Ratulangi (Unsrat)": {
        "_klaster": 4,
        "_lbl": '🔸 Klaster 4 — Regional',
        "D3 Teknik Sipil": {"mn": 533, "mx": 568},
        "D3 Teknik Mesin": {"mn": 537, "mx": 572},
        "D3 Teknik Elektro": {"mn": 548, "mx": 583},
        "D3 Teknik Kimia": {"mn": 541, "mx": 576},
        "D3 Teknik Komputer": {"mn": 559, "mx": 594},
        "D3 Teknologi Informasi": {"mn": 561, "mx": 596},
        "D3 Teknik Mekatronika": {"mn": 535, "mx": 570},
        "D3 Manajemen": {"mn": 539, "mx": 574},
        "D3 Akuntansi": {"mn": 544, "mx": 579},
        "D3 Administrasi Bisnis": {"mn": 525, "mx": 560},
        "D3 Perbankan & Keuangan": {"mn": 541, "mx": 576},
        "D3 Manajemen Pemasaran": {"mn": 536, "mx": 571},
        "D3 Perpajakan": {"mn": 539, "mx": 574},
        "D3 Keperawatan": {"mn": 488, "mx": 523},
        "D3 Kebidanan": {"mn": 483, "mx": 518},
        "D3 Farmasi": {"mn": 552, "mx": 587},
        "D3 Gizi": {"mn": 493, "mx": 528},
        "D3 Analis Kesehatan": {"mn": 547, "mx": 582},
        "D3 Rekam Medis": {"mn": 472, "mx": 507},
        "D3 Fisioterapi": {"mn": 485, "mx": 520},
        "D3 Radiologi": {"mn": 544, "mx": 579},
        "D3 Komunikasi": {"mn": 537, "mx": 572},
        "D3 Hubungan Masyarakat": {"mn": 534, "mx": 569},
        "D3 Desain Grafis": {"mn": 527, "mx": 562},
        "D3 Animasi": {"mn": 556, "mx": 591},
        "D3 Pariwisata": {"mn": 517, "mx": 552},
        "D3 Perhotelan": {"mn": 515, "mx": 550},
        "D3 Bahasa Inggris": {"mn": 491, "mx": 526},
        "D3 Agribisnis": {"mn": 501, "mx": 536},
        "D3 Teknologi Pangan": {"mn": 488, "mx": 523},
        "_default": {"mn": 525, "mx": 560},
    },
    "Universitas Riau (Unri)": {
        "_klaster": 4,
        "_lbl": '🔸 Klaster 4 — Regional',
        "D3 Teknik Sipil": {"mn": 541, "mx": 576},
        "D3 Teknik Mesin": {"mn": 544, "mx": 579},
        "D3 Teknik Elektro": {"mn": 556, "mx": 591},
        "D3 Teknik Kimia": {"mn": 548, "mx": 583},
        "D3 Teknik Komputer": {"mn": 567, "mx": 602},
        "D3 Teknologi Informasi": {"mn": 569, "mx": 604},
        "D3 Teknik Mekatronika": {"mn": 542, "mx": 577},
        "D3 Manajemen": {"mn": 547, "mx": 582},
        "D3 Akuntansi": {"mn": 552, "mx": 587},
        "D3 Administrasi Bisnis": {"mn": 533, "mx": 568},
        "D3 Perbankan & Keuangan": {"mn": 549, "mx": 584},
        "D3 Manajemen Pemasaran": {"mn": 544, "mx": 579},
        "D3 Perpajakan": {"mn": 547, "mx": 582},
        "D3 Keperawatan": {"mn": 495, "mx": 530},
        "D3 Kebidanan": {"mn": 490, "mx": 525},
        "D3 Farmasi": {"mn": 560, "mx": 595},
        "D3 Gizi": {"mn": 500, "mx": 535},
        "D3 Analis Kesehatan": {"mn": 555, "mx": 590},
        "D3 Rekam Medis": {"mn": 479, "mx": 514},
        "D3 Fisioterapi": {"mn": 492, "mx": 527},
        "D3 Radiologi": {"mn": 552, "mx": 587},
        "D3 Komunikasi": {"mn": 544, "mx": 579},
        "D3 Hubungan Masyarakat": {"mn": 541, "mx": 576},
        "D3 Desain Grafis": {"mn": 534, "mx": 569},
        "D3 Animasi": {"mn": 564, "mx": 599},
        "D3 Pariwisata": {"mn": 525, "mx": 560},
        "D3 Perhotelan": {"mn": 523, "mx": 558},
        "D3 Bahasa Inggris": {"mn": 498, "mx": 533},
        "D3 Agribisnis": {"mn": 508, "mx": 543},
        "D3 Teknologi Pangan": {"mn": 495, "mx": 530},
        "_default": {"mn": 533, "mx": 568},
    },
    "Universitas Jember (Unej)": {
        "_klaster": 4,
        "_lbl": '🔸 Klaster 4 — Regional',
        "D3 Teknik Sipil": {"mn": 556, "mx": 591},
        "D3 Teknik Mesin": {"mn": 560, "mx": 595},
        "D3 Teknik Elektro": {"mn": 572, "mx": 607},
        "D3 Teknik Kimia": {"mn": 564, "mx": 599},
        "D3 Teknik Komputer": {"mn": 583, "mx": 618},
        "D3 Teknologi Informasi": {"mn": 585, "mx": 620},
        "D3 Teknik Mekatronika": {"mn": 558, "mx": 593},
        "D3 Manajemen": {"mn": 562, "mx": 597},
        "D3 Akuntansi": {"mn": 568, "mx": 603},
        "D3 Administrasi Bisnis": {"mn": 548, "mx": 583},
        "D3 Perbankan & Keuangan": {"mn": 565, "mx": 600},
        "D3 Manajemen Pemasaran": {"mn": 559, "mx": 594},
        "D3 Perpajakan": {"mn": 563, "mx": 598},
        "D3 Keperawatan": {"mn": 510, "mx": 545},
        "D3 Kebidanan": {"mn": 505, "mx": 540},
        "D3 Farmasi": {"mn": 576, "mx": 611},
        "D3 Gizi": {"mn": 514, "mx": 549},
        "D3 Analis Kesehatan": {"mn": 571, "mx": 606},
        "D3 Rekam Medis": {"mn": 494, "mx": 529},
        "D3 Fisioterapi": {"mn": 507, "mx": 542},
        "D3 Radiologi": {"mn": 568, "mx": 603},
        "D3 Komunikasi": {"mn": 560, "mx": 595},
        "D3 Hubungan Masyarakat": {"mn": 557, "mx": 592},
        "D3 Desain Grafis": {"mn": 550, "mx": 585},
        "D3 Animasi": {"mn": 580, "mx": 615},
        "D3 Pariwisata": {"mn": 540, "mx": 575},
        "D3 Perhotelan": {"mn": 538, "mx": 573},
        "D3 Bahasa Inggris": {"mn": 513, "mx": 548},
        "D3 Agribisnis": {"mn": 523, "mx": 558},
        "D3 Teknologi Pangan": {"mn": 509, "mx": 544},
        "_default": {"mn": 548, "mx": 583},
    },
    "Telkom University": {
        "_klaster": 4,
        "_lbl": '🔸 Klaster 4 — Regional',
        "D3 Teknik Sipil": {"mn": 548, "mx": 583},
        "D3 Teknik Mesin": {"mn": 552, "mx": 587},
        "D3 Teknik Elektro": {"mn": 564, "mx": 599},
        "D3 Teknik Kimia": {"mn": 556, "mx": 591},
        "D3 Teknik Komputer": {"mn": 575, "mx": 610},
        "D3 Teknologi Informasi": {"mn": 577, "mx": 612},
        "D3 Teknik Mekatronika": {"mn": 550, "mx": 585},
        "D3 Manajemen": {"mn": 555, "mx": 590},
        "D3 Akuntansi": {"mn": 560, "mx": 595},
        "D3 Administrasi Bisnis": {"mn": 540, "mx": 575},
        "D3 Perbankan & Keuangan": {"mn": 557, "mx": 592},
        "D3 Manajemen Pemasaran": {"mn": 552, "mx": 587},
        "D3 Perpajakan": {"mn": 555, "mx": 590},
        "D3 Keperawatan": {"mn": 502, "mx": 537},
        "D3 Kebidanan": {"mn": 497, "mx": 532},
        "D3 Farmasi": {"mn": 568, "mx": 603},
        "D3 Gizi": {"mn": 507, "mx": 542},
        "D3 Analis Kesehatan": {"mn": 563, "mx": 598},
        "D3 Rekam Medis": {"mn": 486, "mx": 521},
        "D3 Fisioterapi": {"mn": 499, "mx": 534},
        "D3 Radiologi": {"mn": 560, "mx": 595},
        "D3 Komunikasi": {"mn": 552, "mx": 587},
        "D3 Hubungan Masyarakat": {"mn": 549, "mx": 584},
        "D3 Desain Grafis": {"mn": 542, "mx": 577},
        "D3 Animasi": {"mn": 572, "mx": 607},
        "D3 Pariwisata": {"mn": 532, "mx": 567},
        "D3 Perhotelan": {"mn": 530, "mx": 565},
        "D3 Bahasa Inggris": {"mn": 505, "mx": 540},
        "D3 Agribisnis": {"mn": 516, "mx": 551},
        "D3 Teknologi Pangan": {"mn": 502, "mx": 537},
        "_default": {"mn": 540, "mx": 575},
    },
    "Universitas Islam Indonesia (UII)": {
        "_klaster": 4,
        "_lbl": '🔸 Klaster 4 — Regional',
        "D3 Teknik Sipil": {"mn": 541, "mx": 576},
        "D3 Teknik Mesin": {"mn": 544, "mx": 579},
        "D3 Teknik Elektro": {"mn": 556, "mx": 591},
        "D3 Teknik Kimia": {"mn": 548, "mx": 583},
        "D3 Teknik Komputer": {"mn": 567, "mx": 602},
        "D3 Teknologi Informasi": {"mn": 569, "mx": 604},
        "D3 Teknik Mekatronika": {"mn": 542, "mx": 577},
        "D3 Manajemen": {"mn": 547, "mx": 582},
        "D3 Akuntansi": {"mn": 552, "mx": 587},
        "D3 Administrasi Bisnis": {"mn": 533, "mx": 568},
        "D3 Perbankan & Keuangan": {"mn": 549, "mx": 584},
        "D3 Manajemen Pemasaran": {"mn": 544, "mx": 579},
        "D3 Perpajakan": {"mn": 547, "mx": 582},
        "D3 Keperawatan": {"mn": 495, "mx": 530},
        "D3 Kebidanan": {"mn": 490, "mx": 525},
        "D3 Farmasi": {"mn": 560, "mx": 595},
        "D3 Gizi": {"mn": 500, "mx": 535},
        "D3 Analis Kesehatan": {"mn": 555, "mx": 590},
        "D3 Rekam Medis": {"mn": 479, "mx": 514},
        "D3 Fisioterapi": {"mn": 492, "mx": 527},
        "D3 Radiologi": {"mn": 552, "mx": 587},
        "D3 Komunikasi": {"mn": 544, "mx": 579},
        "D3 Hubungan Masyarakat": {"mn": 541, "mx": 576},
        "D3 Desain Grafis": {"mn": 534, "mx": 569},
        "D3 Animasi": {"mn": 564, "mx": 599},
        "D3 Pariwisata": {"mn": 525, "mx": 560},
        "D3 Perhotelan": {"mn": 523, "mx": 558},
        "D3 Bahasa Inggris": {"mn": 498, "mx": 533},
        "D3 Agribisnis": {"mn": 508, "mx": 543},
        "D3 Teknologi Pangan": {"mn": 495, "mx": 530},
        "_default": {"mn": 533, "mx": 568},
    },
    "Universitas Muhammadiyah Yogyakarta (UMY)": {
        "_klaster": 4,
        "_lbl": '🔸 Klaster 4 — Regional',
        "D3 Teknik Sipil": {"mn": 530, "mx": 565},
        "D3 Teknik Mesin": {"mn": 534, "mx": 569},
        "D3 Teknik Elektro": {"mn": 545, "mx": 580},
        "D3 Teknik Kimia": {"mn": 538, "mx": 573},
        "D3 Teknik Komputer": {"mn": 556, "mx": 591},
        "D3 Teknologi Informasi": {"mn": 558, "mx": 593},
        "D3 Teknik Mekatronika": {"mn": 532, "mx": 567},
        "D3 Manajemen": {"mn": 536, "mx": 571},
        "D3 Akuntansi": {"mn": 542, "mx": 577},
        "D3 Administrasi Bisnis": {"mn": 523, "mx": 558},
        "D3 Perbankan & Keuangan": {"mn": 539, "mx": 574},
        "D3 Manajemen Pemasaran": {"mn": 533, "mx": 568},
        "D3 Perpajakan": {"mn": 537, "mx": 572},
        "D3 Keperawatan": {"mn": 486, "mx": 521},
        "D3 Kebidanan": {"mn": 481, "mx": 516},
        "D3 Farmasi": {"mn": 549, "mx": 584},
        "D3 Gizi": {"mn": 491, "mx": 526},
        "D3 Analis Kesehatan": {"mn": 544, "mx": 579},
        "D3 Rekam Medis": {"mn": 470, "mx": 505},
        "D3 Fisioterapi": {"mn": 483, "mx": 518},
        "D3 Radiologi": {"mn": 541, "mx": 576},
        "D3 Komunikasi": {"mn": 534, "mx": 569},
        "D3 Hubungan Masyarakat": {"mn": 531, "mx": 566},
        "D3 Desain Grafis": {"mn": 524, "mx": 559},
        "D3 Animasi": {"mn": 553, "mx": 588},
        "D3 Pariwisata": {"mn": 515, "mx": 550},
        "D3 Perhotelan": {"mn": 513, "mx": 548},
        "D3 Bahasa Inggris": {"mn": 489, "mx": 524},
        "D3 Agribisnis": {"mn": 499, "mx": 534},
        "D3 Teknologi Pangan": {"mn": 486, "mx": 521},
        "_default": {"mn": 523, "mx": 558},
    },
    "Bina Nusantara University (Binus)": {
        "_klaster": 4,
        "_lbl": '🔸 Klaster 4 — Regional',
        "D3 Teknik Sipil": {"mn": 556, "mx": 591},
        "D3 Teknik Mesin": {"mn": 560, "mx": 595},
        "D3 Teknik Elektro": {"mn": 572, "mx": 607},
        "D3 Teknik Kimia": {"mn": 564, "mx": 599},
        "D3 Teknik Komputer": {"mn": 583, "mx": 618},
        "D3 Teknologi Informasi": {"mn": 585, "mx": 620},
        "D3 Teknik Mekatronika": {"mn": 558, "mx": 593},
        "D3 Manajemen": {"mn": 562, "mx": 597},
        "D3 Akuntansi": {"mn": 568, "mx": 603},
        "D3 Administrasi Bisnis": {"mn": 548, "mx": 583},
        "D3 Perbankan & Keuangan": {"mn": 565, "mx": 600},
        "D3 Manajemen Pemasaran": {"mn": 559, "mx": 594},
        "D3 Perpajakan": {"mn": 563, "mx": 598},
        "D3 Keperawatan": {"mn": 510, "mx": 545},
        "D3 Kebidanan": {"mn": 505, "mx": 540},
        "D3 Farmasi": {"mn": 576, "mx": 611},
        "D3 Gizi": {"mn": 514, "mx": 549},
        "D3 Analis Kesehatan": {"mn": 571, "mx": 606},
        "D3 Rekam Medis": {"mn": 494, "mx": 529},
        "D3 Fisioterapi": {"mn": 507, "mx": 542},
        "D3 Radiologi": {"mn": 568, "mx": 603},
        "D3 Komunikasi": {"mn": 560, "mx": 595},
        "D3 Hubungan Masyarakat": {"mn": 557, "mx": 592},
        "D3 Desain Grafis": {"mn": 550, "mx": 585},
        "D3 Animasi": {"mn": 580, "mx": 615},
        "D3 Pariwisata": {"mn": 540, "mx": 575},
        "D3 Perhotelan": {"mn": 538, "mx": 573},
        "D3 Bahasa Inggris": {"mn": 513, "mx": 548},
        "D3 Agribisnis": {"mn": 523, "mx": 558},
        "D3 Teknologi Pangan": {"mn": 509, "mx": 544},
        "_default": {"mn": 548, "mx": 583},
    },
    "Universitas Muhammadiyah Malang (UMM)": {
        "_klaster": 4,
        "_lbl": '🔸 Klaster 4 — Regional',
        "D3 Teknik Sipil": {"mn": 523, "mx": 558},
        "D3 Teknik Mesin": {"mn": 526, "mx": 561},
        "D3 Teknik Elektro": {"mn": 537, "mx": 572},
        "D3 Teknik Kimia": {"mn": 530, "mx": 565},
        "D3 Teknik Komputer": {"mn": 548, "mx": 583},
        "D3 Teknologi Informasi": {"mn": 550, "mx": 585},
        "D3 Teknik Mekatronika": {"mn": 524, "mx": 559},
        "D3 Manajemen": {"mn": 529, "mx": 564},
        "D3 Akuntansi": {"mn": 534, "mx": 569},
        "D3 Administrasi Bisnis": {"mn": 515, "mx": 550},
        "D3 Perbankan & Keuangan": {"mn": 531, "mx": 566},
        "D3 Manajemen Pemasaran": {"mn": 526, "mx": 561},
        "D3 Perpajakan": {"mn": 529, "mx": 564},
        "D3 Keperawatan": {"mn": 479, "mx": 514},
        "D3 Kebidanan": {"mn": 474, "mx": 509},
        "D3 Farmasi": {"mn": 541, "mx": 576},
        "D3 Gizi": {"mn": 483, "mx": 518},
        "D3 Analis Kesehatan": {"mn": 536, "mx": 571},
        "D3 Rekam Medis": {"mn": 463, "mx": 498},
        "D3 Fisioterapi": {"mn": 476, "mx": 511},
        "D3 Radiologi": {"mn": 533, "mx": 568},
        "D3 Komunikasi": {"mn": 526, "mx": 561},
        "D3 Hubungan Masyarakat": {"mn": 523, "mx": 558},
        "D3 Desain Grafis": {"mn": 516, "mx": 551},
        "D3 Animasi": {"mn": 545, "mx": 580},
        "D3 Pariwisata": {"mn": 507, "mx": 542},
        "D3 Perhotelan": {"mn": 505, "mx": 540},
        "D3 Bahasa Inggris": {"mn": 482, "mx": 517},
        "D3 Agribisnis": {"mn": 491, "mx": 526},
        "D3 Teknologi Pangan": {"mn": 478, "mx": 513},
        "_default": {"mn": 515, "mx": 550},
    },
}

DAFTAR_PTN = [
    "Universitas Indonesia (UI)",
    "Universitas Gadjah Mada (UGM)",
    "Universitas Airlangga (Unair)",
    "Institut Teknologi Bandung (ITB)",
    "Universitas Padjadjaran (Unpad)",
    "Institut Pertanian Bogor (IPB)",
    "Institut Teknologi Sepuluh Nopember (ITS)",
    "Universitas Diponegoro (Undip)",
    "Universitas Brawijaya (UB)",
    "Universitas Sebelas Maret (UNS)",
    "Universitas Hasanuddin (Unhas)",
    "Universitas Pendidikan Indonesia (UPI)",
    "Universitas Sumatera Utara (USU)",
    "Universitas Negeri Yogyakarta (UNY)",
    "Universitas Negeri Malang (UM)",
    "Universitas Lampung (Unila)",
    "Universitas Andalas (Unand)",
    "Universitas Negeri Semarang (UNNES)",
    "Universitas Syiah Kuala (USK)",
    "Universitas Mulawarman (Unmul)",
    "Universitas Sriwijaya (Unsri)",
    "Universitas Udayana (Unud)",
    "Universitas Sam Ratulangi (Unsrat)",
    "Universitas Riau (Unri)",
    "Universitas Jember (Unej)",
    "Telkom University",
    "Universitas Islam Indonesia (UII)",
    "Universitas Muhammadiyah Yogyakarta (UMY)",
    "Bina Nusantara University (Binus)",
    "Universitas Muhammadiyah Malang (UMM)",
]


def get_ptn_info(kampus, jurusan, jenjang="S1 (Sarjana)"):
    """Ambil info skor PTN berdasarkan kampus, jurusan, dan jenjang"""
    if "D3" in jenjang or jurusan.startswith("D3"):
        ptn = PTN_D3_DATA.get(kampus, {})
        if not ptn:
            ptn_s1 = PTN_JURUSAN_DATA.get(kampus, {})
            base = ptn_s1.get(jurusan, ptn_s1.get("_default", {"mn":500,"mx":570}))
            return {
                "mn": max(380, base["mn"] - 80),
                "mx": max(450, base["mx"] - 80),
                "k": ptn_s1.get("_klaster", 4),
                "lbl": ptn_s1.get("_lbl", "🔸 Klaster 4 — Regional")
            }
        jurusan_data = ptn.get(jurusan, ptn.get("_default", {"mn":500,"mx":570}))
        return {
            "mn": jurusan_data["mn"],
            "mx": jurusan_data["mx"],
            "k": ptn.get("_klaster", 4),
            "lbl": ptn.get("_lbl", "🔸 Klaster 4 — Regional")
        }
    else:
        ptn = PTN_JURUSAN_DATA.get(kampus, {})
        if not ptn:
            return {"mn": 650, "mx": 720, "k": 4, "lbl": "🔸 Klaster 4 — Regional"}
        jurusan_data = ptn.get(jurusan, ptn.get("_default", {"mn": 650, "mx": 720}))
        return {
            "mn": jurusan_data["mn"],
            "mx": jurusan_data["mx"],
            "k": ptn.get("_klaster", 4),
            "lbl": ptn.get("_lbl", "🔸 Klaster 4 — Regional")
        }

def get_ptn(k):
    ptn = PTN_JURUSAN_DATA.get(k, {})
    default = ptn.get("_default", {"mn": 650, "mx": 720})
    return {
        "k": ptn.get("_klaster", 4),
        "mn": default["mn"],
        "mx": default["mx"],
        "lbl": ptn.get("_lbl", "🔸 Klaster 4")
    }

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

ALTERNATIF_MAP_D3 = {
    "D3 Teknik Sipil":         ["D3 Teknik Mesin","D3 Teknik Elektro","D3 Teknik Mekatronika"],
    "D3 Teknik Mesin":         ["D3 Teknik Sipil","D3 Teknik Elektro","D3 Teknik Mekatronika"],
    "D3 Teknik Elektro":       ["D3 Teknik Komputer","D3 Teknologi Informasi","D3 Teknik Mekatronika"],
    "D3 Teknik Kimia":         ["D3 Teknologi Pangan","D3 Teknik Sipil","D3 Teknik Mesin"],
    "D3 Teknik Komputer":      ["D3 Teknologi Informasi","D3 Teknik Elektro","D3 Animasi"],
    "D3 Teknologi Informasi":  ["D3 Teknik Komputer","D3 Animasi","D3 Desain Grafis"],
    "D3 Teknik Mekatronika":   ["D3 Teknik Mesin","D3 Teknik Elektro","D3 Teknik Komputer"],
    "D3 Manajemen":            ["D3 Administrasi Bisnis","D3 Manajemen Pemasaran","D3 Akuntansi"],
    "D3 Akuntansi":            ["D3 Perpajakan","D3 Perbankan & Keuangan","D3 Manajemen"],
    "D3 Administrasi Bisnis":  ["D3 Manajemen","D3 Manajemen Pemasaran","D3 Akuntansi"],
    "D3 Perbankan & Keuangan": ["D3 Akuntansi","D3 Perpajakan","D3 Manajemen"],
    "D3 Manajemen Pemasaran":  ["D3 Administrasi Bisnis","D3 Komunikasi","D3 Manajemen"],
    "D3 Perpajakan":           ["D3 Akuntansi","D3 Perbankan & Keuangan","D3 Manajemen"],
    "D3 Keperawatan":          ["D3 Kebidanan","D3 Gizi","D3 Farmasi"],
    "D3 Kebidanan":            ["D3 Keperawatan","D3 Gizi","D3 Analis Kesehatan"],
    "D3 Farmasi":              ["D3 Analis Kesehatan","D3 Keperawatan","D3 Gizi"],
    "D3 Gizi":                 ["D3 Keperawatan","D3 Farmasi","D3 Analis Kesehatan"],
    "D3 Analis Kesehatan":     ["D3 Farmasi","D3 Radiologi","D3 Rekam Medis"],
    "D3 Rekam Medis":          ["D3 Administrasi Bisnis","D3 Analis Kesehatan","D3 Keperawatan"],
    "D3 Fisioterapi":          ["D3 Keperawatan","D3 Gizi","D3 Kebidanan"],
    "D3 Radiologi":            ["D3 Analis Kesehatan","D3 Rekam Medis","D3 Farmasi"],
    "D3 Komunikasi":           ["D3 Hubungan Masyarakat","D3 Manajemen Pemasaran","D3 Pariwisata"],
    "D3 Hubungan Masyarakat":  ["D3 Komunikasi","D3 Manajemen Pemasaran","D3 Administrasi Bisnis"],
    "D3 Desain Grafis":        ["D3 Animasi","D3 Komunikasi","D3 Teknologi Informasi"],
    "D3 Animasi":              ["D3 Desain Grafis","D3 Teknologi Informasi","D3 Komunikasi"],
    "D3 Pariwisata":           ["D3 Perhotelan","D3 Komunikasi","D3 Manajemen"],
    "D3 Perhotelan":           ["D3 Pariwisata","D3 Manajemen","D3 Komunikasi"],
    "D3 Bahasa Inggris":       ["D3 Komunikasi","D3 Hubungan Masyarakat","D3 Pariwisata"],
    "D3 Agribisnis":           ["D3 Teknologi Pangan","D3 Manajemen","D3 Administrasi Bisnis"],
    "D3 Teknologi Pangan":     ["D3 Agribisnis","D3 Analis Kesehatan","D3 Gizi"],
}

LABEL_STRATEGI = ["Intensif & Terstruktur","Penguatan Mental","Optimasi & Review","Pertahankan & Tingkatkan"]
DESC_STRATEGI = {
    "Intensif & Terstruktur":{"icon":"🔴","desc":"Kebiasaan belajar dan kondisi psikologis perlu ditingkatkan secara bersamaan.",
        "tips":["Buat jadwal belajar harian yang ketat","Mulai 2 jam/hari, tingkatkan bertahap","Metode Pomodoro 25+5 menit","Cari kelompok belajar","Konsultasi guru/mentor"]},
    "Penguatan Mental":{"icon":"🟠","desc":"Kebiasaan belajar sudah baik, namun kondisi psikologis perlu diperkuat.",
        "tips":["Mindfulness 10 mnt sebelum belajar","Target kecil harian","Kurangi perbandingan diri","Rutinitas tidur teratur","Tryout rutin untuk adaptasi"]},
    "Optimasi & Review":{"icon":"🟡","desc":"Kebiasaan & mental sudah baik, tingkatkan kualitas review dan evaluasi.",
        "tips":["Review soal yang pernah salah","Analisis pola kesalahan per subtes","Tryout min. 2x/bulan","Catatan ringkasan materi","Fokus efisiensi waktu"]},
    "Pertahankan & Tingkatkan":{"icon":"🟢","desc":"Kebiasaan belajar dan kondisi psikologis sudah sangat baik!",
        "tips":["Pertahankan konsistensi","Tingkatkan target tryout bertahap","Manajemen waktu ujian","Bantu teman belajar","Jaga kesehatan fisik"]},
}


# ══════════════════════════════════════════════════════════
# LOAD MODEL
# ══════════════════════════════════════════════════════════
@st.cache_resource
def load_model():
    for f in ["lgbm_model_2_.pkl","lgbm_model.pkl","model_skor_utbk_asli.pkl"]:
        if os.path.exists(f):
            try:
                with open(f,"rb") as fp: return pickle.load(fp), f
            except: pass
    return None, None

lgbm_model, lgbm_fname = load_model()


# ══════════════════════════════════════════════════════════
# KALKULASI
# ══════════════════════════════════════════════════════════
def hitung_tw(skor, bobot): return sum(skor[k]*bobot[k] for k in SUBTES)

def hitung_peluang(sw, kampus, jurusan=None, jenjang="S1 (Sarjana)"):
    if jurusan:
        info = get_ptn_info(kampus, jurusan, jenjang)
    else:
        info = get_ptn(kampus)
    mn, mx = info["mn"], info["mx"]
    g = sw - mn
    if sw >= mx:      return "Sangat Aman","#1a8a4a", min(93.,76+(sw-mx)/max(mx,1)*12)
    elif sw >= mn:    return "Aman","#1a8a4a",        62+(sw-mn)/max(mx-mn,1)*13
    elif sw >= mn-70: return "Kompetitif","#d4620a",  32+(70+g)/70*25
    elif sw >= mn-140:return "Berisiko","#c0392b",    16.
    else:             return "Perlu Peningkatan","#c0392b", 8.

def predict_lgbm(model, inp):
    try:
        feat = pd.DataFrame([{
            "Jam_Belajar":inp["jam"],"Hari_Belajar":inp["hari"],
            "Latihan_Soal":inp["latihan"],"Frekuensi_Tryout":inp["tryout"],
            "Review_Soal":inp["review"],"Fokus":inp["fokus"],
            "Percaya_Diri":inp["pede"],
            "Kecemasan_Rev":6-inp["cemas"],"Distraksi_Rev":6-inp["distrak"],
        }])
        if hasattr(model,"feature_name_"):     feat = feat.reindex(columns=model.feature_name_,fill_value=0)
        elif hasattr(model,"feature_names_in_"):feat = feat.reindex(columns=model.feature_names_in_,fill_value=0)
        kode  = int(model.predict(feat)[0])
        label = LABEL_STRATEGI[kode] if kode < len(LABEL_STRATEGI) else LABEL_STRATEGI[-1]
        kpct  = None
        if hasattr(model,"predict_proba"): kpct = float(model.predict_proba(feat)[0][kode])*100
        return {"ok":True,"kode":kode,"strategi":label,"kpct":kpct,"detail":DESC_STRATEGI.get(label,{})}
    except Exception as e:
        return {"ok":False,"err":str(e)}

def compute(d):
    skor  = {k: d[k] for k in SUBTES}
    bobot = get_bobot(d["jurusan"])
    sw    = hitung_tw(skor, bobot)
    rata  = float(np.mean([skor[k] for k in SUBTES]))
    jenjang = d.get("jenjang", "S1 (Sarjana)")
    pl,pc,ppct = hitung_peluang(sw, d["kampus"], d["jurusan"], jenjang)
    info  = get_ptn_info(d["kampus"], d["jurusan"], jenjang)
    gap   = sw - info["mn"]

    psiko = (d["fokus"]*1.5 + d["pede"]*1.5 + (6-d["cemas"]) + (6-d["distrak"])) / 20 * 100
    konsist = min(100, (d["jam"]*2 + d["hari"]*2.2 + d["latihan"]*1.8 + d["tryout"]*1.5 + d["review"]*1.5)*2)
    pos = (d["fokus"]*1.5 + d["pede"]*1.5)*10
    neg = (d["cemas"]*1.2 + d["distrak"]*1.2)*8
    stab = max(0, min(100, pos - neg + 50))
    rgb  = stab*0.6 + konsist*0.4
    if rgb >= 75: risk=("Rendah","✅","Kemungkinan perform sesuai/di atas kemampuan")
    elif rgb >= 60: risk=("Sedang","⚠️","Ada potensi fluktuasi, jaga konsistensi")
    else: risk=("Tinggi","🔴","Risiko perform di bawah kemampuan, perlu perbaikan")

    lgbm_r = predict_lgbm(lgbm_model, d) if lgbm_model else None
    aman   = pl in ("Sangat Aman","Aman")
    jenjang = d.get("jenjang","S1 (Sarjana)")
    if "D3" in jenjang or d["jurusan"].startswith("D3"):
        alt = ALTERNATIF_MAP_D3.get(d["jurusan"],[])
    else:
        alt = ALTERNATIF_MAP.get(d["jurusan"],[])

    return {**d,"skor":skor,"bobot":bobot,"sw":sw,"rata":rata,
            "pl":pl,"pc":pc,"ppct":ppct,"info":info,"gap":gap,
            "psiko":psiko,"konsist":konsist,"stab":stab,"risk":risk,
            "lgbm_r":lgbm_r,"aman":aman,"jenjang":jenjang,
            "alternatif":alt}

# ══════════════════════════════════════════════════════════
# RENCANA BELAJAR MINGGUAN
# ══════════════════════════════════════════════════════════
def buat_rencana_mingguan(r, n_minggu=8):
    skor  = r["skor"]
    bobot = r["bobot"]
    gap   = r["gap"]
    sw    = r["sw"]
    mn    = r["info"]["mn"]
    mx    = r["info"]["mx"]

    ranked = sorted(SUBTES, key=lambda k: skor[k])
    terlemah3 = ranked[:3]
    sedang2   = ranked[3:5]
    terkuat2  = ranked[5:]

    if gap < 0:
        target_per_minggu = abs(gap) / n_minggu + 10
    else:
        target_per_minggu = (mx - sw) / n_minggu + 5 if sw < mx else 5

    rencana = []
    for w in range(1, n_minggu+1):
        fase = "Fondasi" if w <= 2 else "Intensif" if w <= 5 else "Pemantapan" if w <= 7 else "Final"
        target_sw = min(mx+20, sw + target_per_minggu * w)

        if fase == "Fondasi":
            tasks = [
                f"Review konsep dasar {SUBTES_FULL[terlemah3[0]]} (skor {skor[terlemah3[0]]} → target +30)",
                f"50 soal latihan {SUBTES_FULL[terlemah3[1]]} dengan timer",
                f"Pelajari pola soal {SUBTES_FULL[terlemah3[2]]}",
                "Buat catatan kesalahan (error log)",
                "Tryout mini: 30 soal campuran + analisis",
            ]
            jam = "2–3 jam/hari"
        elif fase == "Intensif":
            subtes_minggu = terlemah3 + sedang2
            subtes_ini = subtes_minggu[(w-3) % len(subtes_minggu)] if subtes_minggu else "PU"
            tasks = [
                f"100 soal latihan {SUBTES_FULL[subtes_ini]} + timer ketat",
                "Review error log minggu sebelumnya",
                f"Mini tryout {SUBTES_FULL[sedang2[0] if sedang2 else 'PU']} (50 soal, 45 mnt)",
                "Simulasi 1 paket soal lengkap (90 mnt)",
                "Analisis & rekap kesalahan pola berulang",
            ]
            jam = "3–4 jam/hari"
        elif fase == "Pemantapan":
            tasks = [
                "Full tryout 1 paket lengkap + evaluasi",
                f"Review intensif {SUBTES_FULL[terlemah3[0]]} (subtes fokus utama)",
                "Latihan manajemen waktu (simulasi kondisi ujian)",
                "Review catatan penting semua subtes",
                "Rest day: hanya review ringan 1 jam",
            ]
            jam = "3–4 jam/hari (1 hari libur)"
        else:
            tasks = [
                "Full tryout final + review mendalam",
                "Revisi soal-soal sulit yang pernah salah",
                "Persiapan mental: teknik relaksasi & tidur cukup",
                "Cek strategi manajemen waktu ujian",
                "Istirahat — jaga kondisi fisik & mental",
            ]
            jam = "2 jam/hari + istirahat cukup"

        rencana.append({
            "minggu": w, "fase": fase,
            "target_skor": f"{target_sw:.0f}",
            "jam": jam, "fokus": SUBTES_FULL.get(terlemah3[0],"TPS") if terlemah3 else "TPS",
            "tasks": tasks,
        })
    return rencana


# ══════════════════════════════════════════════════════════
# CHART THEME — Light
# ══════════════════════════════════════════════════════════
CTH = dict(
    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family='Inter', color='#3a4a65'),
    margin=dict(l=10, r=10, t=45, b=10)
)

def ch_radar(skor, bobot, jurusan, key=None):
    cats  = [SUBTES_FULL[k] for k in SUBTES] + [SUBTES_FULL[SUBTES[0]]]
    vals  = [skor[k] for k in SUBTES] + [skor[SUBTES[0]]]
    ideal = [min(SKOR_MAX_TPS, SKOR_MAX_TPS*bobot[k]*6) for k in SUBTES] + [min(SKOR_MAX_TPS, SKOR_MAX_TPS*bobot[SUBTES[0]]*6)]
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=ideal, theta=cats, fill='toself', name='Profil Ideal Jurusan',
        fillcolor='rgba(200,137,10,.08)', line=dict(color='#c8890a', dash='dot', width=2)))
    fig.add_trace(go.Scatterpolar(r=vals,  theta=cats, fill='toself', name='Skor Kamu',
        fillcolor='rgba(59,108,183,.12)', line=dict(color='#3b6cb7', width=2.5)))
    fig.update_layout(**CTH, polar=dict(
        bgcolor='rgba(240,244,248,.6)',
        radialaxis=dict(range=[0,SKOR_MAX_TPS], gridcolor='#dde3ec', linecolor='#dde3ec',
                        tickfont=dict(size=9, color='#6a7a95')),
        angularaxis=dict(gridcolor='#dde3ec', linecolor='#dde3ec', tickfont=dict(size=9.5, color='#3a4a65'))),
        legend=dict(bgcolor='rgba(255,255,255,.8)', orientation='h', x=.5, xanchor='center', y=-.15,
                    font=dict(color='#3a4a65')),
        title=dict(text=f"Radar TPS — {jurusan}", font=dict(size=13, color='#1a2540')), height=400)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False}, key=key or ckey("radar"))

def ch_bar_subtes(skor, bobot, info, key=None):
    lbl  = [SUBTES_FULL[k] for k in SUBTES]
    vals = [skor[k] for k in SUBTES]
    tgt  = [min(SKOR_MAX_TPS,(info["mn"]+info["mx"])/2*bobot[k]*7) for k in SUBTES]
    clrs = [SUBTES_CLR[k] for k in SUBTES]
    fig  = go.Figure()
    fig.add_trace(go.Bar(name='Skor Kamu', x=lbl, y=vals, marker_color=clrs, marker_line_width=0,
        text=[str(v) for v in vals], textposition='outside', textfont=dict(size=10, color='#1a2540')))
    fig.add_trace(go.Scatter(name='Target Kampus', x=lbl, y=tgt, mode='markers+lines',
        marker=dict(symbol='diamond', size=9, color='#c8890a'),
        line=dict(color='#c8890a', dash='dot', width=1.5)))
    fig.update_layout(**CTH, barmode='group',
        xaxis=dict(tickfont=dict(size=9, color='#3a4a65'), gridcolor='#dde3ec'),
        yaxis=dict(range=[0, SKOR_MAX_TPS*1.07], gridcolor='#eef1f5', tickfont=dict(size=9, color='#3a4a65')),
        legend=dict(bgcolor='rgba(255,255,255,.8)', orientation='h', x=.5, xanchor='center', y=-.2, font=dict(color='#3a4a65')),
        title=dict(text="Skor Per Subtes vs Target Kampus", font=dict(size=13, color='#1a2540')), height=370)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False}, key=key or ckey("bar"))

def ch_pipeline(skor, bobot, info, jurusan, key=None):
    lbl    = [SUBTES_FULL[k] for k in SUBTES]
    aktual = [skor[k]*bobot[k] for k in SUBTES]
    ideal  = [info["mn"]*bobot[k] for k in SUBTES]
    clrs   = [SUBTES_CLR[k] for k in SUBTES]
    fig    = go.Figure()
    fig.add_trace(go.Bar(name='Target Min Kampus', y=lbl, x=ideal, orientation='h',
        marker_color=['rgba(200,137,10,.12)']*7,
        marker_line_color='#c8890a', marker_line_width=1.5))
    fig.add_trace(go.Bar(name='Kontribusi Aktual', y=lbl, x=aktual, orientation='h',
        marker_color=clrs, text=[f"{v:.1f}" for v in aktual],
        textposition='inside', textfont=dict(size=10, color='#fff')))
    fig.update_layout(**CTH, barmode='overlay',
        xaxis=dict(title="Kontribusi ke Skor Total", gridcolor='#eef1f5',
                   title_font=dict(color='#6a7a95'), tickfont=dict(size=9, color='#3a4a65')),
        yaxis=dict(gridcolor='#dde3ec', tickfont=dict(size=10, color='#3a4a65')),
        legend=dict(bgcolor='rgba(255,255,255,.8)', orientation='h', x=.5, xanchor='center', y=-.13, font=dict(color='#3a4a65')),
        title=dict(text=f"Pipeline Kontribusi Subtes — {jurusan}", font=dict(size=13, color='#1a2540')), height=380)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False}, key=key or ckey("pipe"))

def ch_bobot(jurusan, key=None):
    bobot = get_bobot(jurusan)
    lbl   = [SUBTES_FULL[k] for k in SUBTES]
    vals  = [bobot[k]*100 for k in SUBTES]
    clrs  = [SUBTES_CLR[k] for k in SUBTES]
    fig   = go.Figure(go.Bar(x=lbl, y=vals, marker_color=clrs, marker_line_width=0,
        text=[f"{v:.0f}%" for v in vals], textposition='outside', textfont=dict(size=10, color='#1a2540')))
    fig.update_layout(**CTH,
        xaxis=dict(tickfont=dict(size=9, color='#3a4a65'), gridcolor='#dde3ec'),
        yaxis=dict(range=[0,55], ticksuffix="%", gridcolor='#eef1f5',
                   title="Bobot (%)", title_font=dict(color='#6a7a95'), tickfont=dict(size=9, color='#3a4a65')),
        title=dict(text=f"Distribusi Bobot Subtes — {jurusan}", font=dict(size=13, color='#1a2540')), height=300)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False}, key=key or ckey("bobot"))

def ch_klaster(sw, key=None):
    kl = [("Klaster 1\nTop Tier",880,970,"#c0392b"),
          ("Klaster 2\nMng Atas",730,870,"#d4620a"),
          ("Klaster 3\nMenengah",600,730,"#1a8a4a"),
          ("Klaster 4\nRegional",555,660,"#3b6cb7")]
    fig = go.Figure()
    for lbl,mn,mx,clr in kl:
        r_,g_,b_ = int(clr[1:3],16),int(clr[3:5],16),int(clr[5:7],16)
        fig.add_trace(go.Bar(x=[lbl], y=[mx-mn], base=[mn], showlegend=False,
            marker_color=f"rgba({r_},{g_},{b_},.12)", marker_line_color=clr, marker_line_width=2,
            text=[f"{mn}–{mx}"], textposition='inside', textfont=dict(size=10,color=clr)))
    fig.add_hline(y=sw, line_dash="dash", line_color="#7048c8", line_width=2.5,
        annotation_text=f"  Skor kamu: {sw:.0f}", annotation_font_color="#7048c8", annotation_font_size=11)
    fig.update_layout(**CTH, barmode='overlay',
        xaxis=dict(gridcolor='#dde3ec', tickfont=dict(size=10,color='#3a4a65')),
        yaxis=dict(range=[450,SKOR_MAX_TPS], gridcolor='#eef1f5',
                   title="Rentang Skor Aman", title_font=dict(color='#6a7a95'), tickfont=dict(size=9,color='#3a4a65')),
        title=dict(text="Posisi Skor vs Klaster PTN", font=dict(size=13,color='#1a2540')), height=370)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False}, key=key or ckey("klaster"))

def ch_ptn(sw, klaster_no, jurusan, jenjang="S1 (Sarjana)", key=None):
    if "D3" in jenjang:
        ptn_k = {k:v for k,v in PTN_D3_DATA.items() if v.get("_klaster")==klaster_no}
    else:
        ptn_k = {k:v for k,v in PTN_JURUSAN_DATA.items() if v.get("_klaster")==klaster_no}
    fig = go.Figure()
    for nm,d in ptn_k.items():
        short = nm.split("(")[0].strip()[:24]
        jd = d.get(jurusan, d.get("_default", {"mn":500,"mx":600}))
        mn_j, mx_j = jd["mn"], jd["mx"]
        fig.add_trace(go.Bar(x=[short], y=[mx_j-mn_j], base=[mn_j], showlegend=False,
            marker_color='rgba(59,108,183,.12)', marker_line_color='#3b6cb7', marker_line_width=1.5,
            text=[f"{mn_j}–{mx_j}"], textposition='inside', textfont=dict(size=9,color='#1a2540')))
    fig.add_hline(y=sw, line_dash="dash", line_color="#c8890a", line_width=2,
        annotation_text=f"  Skor kamu: {sw:.0f}", annotation_font_color="#c8890a", annotation_font_size=11)
    y_min = 350 if "D3" in jenjang else 450
    jenjang_lbl2 = "D3" if "D3" in jenjang else "S1"
    fig.update_layout(**CTH, barmode='overlay',
        yaxis=dict(range=[y_min,SKOR_MAX_TPS], gridcolor='#eef1f5',
                   title="Rentang Skor", title_font=dict(color='#6a7a95'), tickfont=dict(size=9,color='#3a4a65')),
        xaxis=dict(gridcolor='#dde3ec', tickfont=dict(size=9,color='#3a4a65')),
        title=dict(text=f"PTN Klaster {klaster_no} ({jenjang_lbl2}) — {jurusan}", font=dict(size=13,color='#1a2540')), height=320)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False}, key=key or ckey("ptn"))

def ch_psiko(psiko, konsist, stab, key=None):
    cats = ["Kesiapan Mental","Konsistensi Belajar","Stabilitas Mental"]
    fig  = go.Figure()
    fig.add_trace(go.Bar(x=cats, y=[psiko,konsist,stab],
        marker_color=["#3b6cb7","#1a8a4a","#7048c8"], marker_line_width=0,
        text=[f"{v:.0f}%" for v in [psiko,konsist,stab]],
        textposition='outside', textfont=dict(size=11,color='#1a2540')))
    fig.add_hline(y=80, line_dash="dot", line_color="#c8890a", line_width=1.5,
        annotation_text="  Target 80%", annotation_font_color="#c8890a", annotation_font_size=10)
    fig.update_layout(**CTH,
        yaxis=dict(range=[0,115], ticksuffix="%", gridcolor='#eef1f5', tickfont=dict(size=9,color='#3a4a65')),
        xaxis=dict(gridcolor='#dde3ec', tickfont=dict(size=10,color='#3a4a65')),
        title=dict(text="Indikator Psikologis & Konsistensi", font=dict(size=13,color='#1a2540')), height=300)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False}, key=key or ckey("psiko"))

def ch_progress(r, key=None):
    sw   = r["sw"]; mn = r["info"]["mn"]; mx = r["info"]["mx"]
    gap  = abs(r["gap"]) if r["gap"] < 0 else 0
    ppm  = gap/8 + 8
    weeks = list(range(0, 9))
    preds = [min(mx+30, sw + ppm*w) for w in weeks]
    fig = go.Figure()
    fig.add_hrect(y0=mn, y1=mx, fillcolor="rgba(26,138,74,.07)", layer="below",
                  line_width=0, annotation_text="  Zona Aman", annotation_position="top right",
                  annotation_font=dict(color="#1a8a4a", size=10))
    fig.add_trace(go.Scatter(x=weeks, y=preds, mode='lines+markers+text',
        line=dict(color='#3b6cb7', width=2.5),
        marker=dict(size=8, color='#3b6cb7', line=dict(color='#ffffff', width=1.5)),
        text=[f"{v:.0f}" for v in preds], textposition='top center',
        textfont=dict(size=9,color='#3a4a65'), name='Proyeksi Skor'))
    fig.add_trace(go.Scatter(x=[0], y=[sw], mode='markers',
        marker=dict(size=12, color='#c8890a', symbol='star'),
        name=f'Skor Sekarang ({sw:.0f})'))
    fig.add_hline(y=mn, line_dash="dash", line_color="#d4620a", line_width=1.5,
        annotation_text=f"  Minimum ({mn})", annotation_font_color="#d4620a", annotation_font_size=10)
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter', color='#3a4a65'),
        margin=dict(l=10, r=10, t=45, b=30),
        xaxis=dict(title="Minggu ke-", tickvals=weeks, gridcolor='#eef1f5',
                   title_font=dict(color='#6a7a95'), tickfont=dict(size=9,color='#3a4a65')),
        yaxis=dict(range=[max(400,sw-100), min(1000,mx+60)], gridcolor='#eef1f5',
                   title="Proyeksi Skor", title_font=dict(color='#6a7a95'), tickfont=dict(size=9,color='#3a4a65')),
        legend=dict(bgcolor='rgba(255,255,255,.8)', font=dict(color='#3a4a65')),
        title=dict(text="Proyeksi Skor 8 Minggu ke Depan", font=dict(size=13,color='#1a2540')),
        height=340
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False}, key=key or ckey("prog"))


# ══════════════════════════════════════════════════════════
# PDF EXPORT
# ══════════════════════════════════════════════════════════
def generate_pdf(r):
    now  = datetime.datetime.now().strftime("%d %B %Y, %H:%M")
    nama = r.get("nama","—")
    jenjang_lbl = r.get("jenjang","S1 (Sarjana)")
    bobot_rows = "".join(
        f"<tr><td>{SUBTES_FULL[k]}</td><td>{int(r['bobot'][k]*100)}%</td>"
        f"<td>{r['skor'][k]}</td><td>{r['skor'][k]*r['bobot'][k]:.1f}</td></tr>"
        for k in SUBTES)
    alt_list = ", ".join(r["alternatif"]) if r["alternatif"] else "—"
    lgbm_txt = ""
    if r.get("lgbm_r") and r["lgbm_r"].get("ok"):
        h = r["lgbm_r"]
        kp = f"{h['kpct']:.1f}%" if h.get("kpct") else "—"
        lgbm_txt = f"<p><strong>Rekomendasi Strategi SKORIA AI:</strong> {h['strategi']} (kepercayaan: {kp})</p>"
    rencana = buat_rencana_mingguan(r, 8)
    minggu_html = "".join(f"""
    <div style="margin-bottom:12px;padding:10px 14px;background:#f8fafc;border-radius:8px;border-left:3px solid #3b6cb7">
      <div style="font-size:9pt;color:#3b6cb7;font-weight:700;text-transform:uppercase;letter-spacing:.05em;margin-bottom:3px">
        Minggu {m['minggu']} — {m['fase']}
      </div>
      <div style="font-size:9.5pt;font-weight:600;color:#1e293b;margin-bottom:4px">
        Target skor: {m['target_skor']} | {m['jam']}
      </div>
      <ul style="margin:0;padding-left:1.1rem;font-size:9pt;color:#374151;line-height:1.7">
        {"".join(f"<li>{t}</li>" for t in m['tasks'])}
      </ul>
    </div>""" for m in rencana)
    gc = "green" if r["gap"]>=0 else "red"
    pc = "green" if r["ppct"]>=65 else "orange" if r["ppct"]>=35 else "red"
    return f"""<!DOCTYPE html><html lang="id"><head><meta charset="UTF-8">
<title>Laporan SKORIA — {nama}</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Sora:wght@700;800&display=swap');
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:'Inter',sans-serif;font-size:11pt;color:#1e293b;background:#fff;padding:1.2cm 1.8cm}}
h1{{font-family:'Sora',sans-serif;font-size:18pt;font-weight:800;color:#0f172a}}
h2{{font-family:'Sora',sans-serif;font-size:11pt;font-weight:700;color:#0f172a;margin:16px 0 7px;
    border-bottom:2px solid #3b6cb7;padding-bottom:3px}}
p{{font-size:10pt;line-height:1.65;color:#374151;margin-bottom:5px}}
.hdr{{background:linear-gradient(135deg,#2a4a8c,#3b6cb7);color:#fff;padding:1.1cm 1.4cm;
      border-radius:12px;margin-bottom:.9cm}}
.brand{{font-family:'Sora',sans-serif;font-size:12pt;font-weight:800;color:#ffd166;margin-bottom:3px}}
.hdr .sub{{color:rgba(255,255,255,.75);font-size:9pt;margin-top:3px}}
.kpi-row{{display:flex;gap:10px;margin-bottom:10px}}
.kpi{{flex:1;border:1px solid #e2e8f0;border-radius:8px;padding:10px;text-align:center}}
.kpi .val{{font-size:18pt;font-weight:800;font-family:'Sora',sans-serif}}
.kpi .lbl{{font-size:7.5pt;color:#64748b;text-transform:uppercase;letter-spacing:.05em}}
.green{{color:#16a34a}}.orange{{color:#ca8a04}}.red{{color:#dc2626}}.blue{{color:#1d4ed8}}
table{{width:100%;border-collapse:collapse;font-size:9.5pt;margin-bottom:9px}}
th{{background:#eef3fc;text-align:left;padding:5px 9px;font-weight:600;border:1px solid #dde3ec;color:#1e293b}}
td{{padding:5px 9px;border:1px solid #dde3ec;color:#374151}}
tr:nth-child(even) td{{background:#f7f9fc}}
.footer{{margin-top:.8cm;font-size:8pt;color:#94a3b8;text-align:center;border-top:1px solid #e2e8f0;padding-top:7px}}
@media print{{body{{padding:.8cm 1cm}}.no-print{{display:none}}}}
</style></head><body>
<div class="hdr">
  <div class="brand">🎯 SKORIA</div>
  <h1>AI UTBK Readiness Report</h1>
  <div class="sub">Laporan Kesiapan UTBK · {now}</div>
</div>
<h2>👤 Profil Siswa</h2>
<table><tr><th>Nama</th><td>{nama}</td><th>Jenjang</th><td>{jenjang_lbl}</td></tr>
<tr><th>Jurusan / Prodi</th><td>{r['jurusan']}</td><th>Kampus Target</th><td>{r['kampus']}</td></tr>
<tr><th>Klaster</th><td colspan="3">{r['info']['lbl']}</td></tr></table>
<h2>📊 Ringkasan Hasil (Skor skala 1000)</h2>
<div class="kpi-row">
<div class="kpi"><div class="lbl">Skor Tertimbang</div><div class="val {gc}">{r['sw']:.0f}</div><div class="lbl">dari 1000</div></div>
<div class="kpi"><div class="lbl">Rata-rata Subtes</div><div class="val blue">{r['rata']:.0f}</div></div>
<div class="kpi"><div class="lbl">Peluang Lolos</div><div class="val {pc}">{r['ppct']:.0f}%</div><div class="lbl">{r['pl']}</div></div>
<div class="kpi"><div class="lbl">Gap vs Minimum</div><div class="val {gc}">{r['gap']:+.0f}</div><div class="lbl">Min {r['info']['mn']}</div></div>
</div>
{lgbm_txt}
<h2>📋 Bobot & Skor Subtes</h2>
<table><tr><th>Subtes</th><th>Bobot ({r['jurusan']})</th><th>Skor (maks 1000)</th><th>Kontribusi</th></tr>
{bobot_rows}
<tr style="background:#eef3fc"><th colspan="2">Total Skor Tertimbang</th><th colspan="2"><strong>{r['sw']:.1f}</strong></th></tr></table>
<h2>🧠 Indikator Psikologis & Kebiasaan</h2>
<table>
<tr><th>Fokus</th><td>{r['fokus']}/5</td><th>Percaya Diri</th><td>{r['pede']}/5</td></tr>
<tr><th>Kecemasan</th><td>{r['cemas']}/5</td><th>Distraksi</th><td>{r['distrak']}/5</td></tr>
<tr><th>Kesiapan Mental</th><td>{r['psiko']:.0f}/100</td><th>Konsistensi</th><td>{r['konsist']:.0f}/100</td></tr>
<tr><th>Stabilitas Mental</th><td>{r['stab']:.0f}/100</td><th>Risiko Underperform</th><td>{r['risk'][0]} {r['risk'][1]}</td></tr></table>
<h2>🎓 Jurusan Alternatif</h2><p>{alt_list}</p>
<h2>📅 Rencana Belajar Mingguan (8 Minggu)</h2>
{minggu_html}
<div class="footer">🎯 SKORIA — AI UTBK Intelligence · Data SNPMB/BPPP Kemdikbud & media pendidikan 2025/2026 · Skor skala 200–1000 · 30 PTN</div>
<div class="no-print" style="margin-top:16px;text-align:center">
<button onclick="window.print()" style="padding:8px 20px;background:#3b6cb7;border:none;border-radius:8px;
  font-weight:700;cursor:pointer;font-size:11pt;font-family:'Sora',sans-serif;color:#ffffff">
  🖨️ Print / Save as PDF</button></div>
</body></html>"""


# ══════════════════════════════════════════════════════════
# NAV BAR
# ══════════════════════════════════════════════════════════
def render_nav():
    p = st.session_state.page
    s1 = "done" if p in ["survey","result"] else "active" if p=="home" else ""
    s2 = "done" if p=="result" else "active" if p=="survey" else ""
    s3 = "active" if p=="result" else ""
    st.markdown(f"""<div class="topbar">
      <div class="topbar-brand">🎯 SKORIA <span class="topbar-tag">AI UTBK Intelligence · S1 &amp; D3 · 30 PTN · 2025/2026</span></div>
      <div style="flex:1"></div>
      <div class="step-pill {s1}">{{'✓' if p in ['survey','result'] else '①'}} Beranda</div>
      <div class="step-pill {s2}">{{'✓' if p=='result' else '②'}} Input Data</div>
      <div class="step-pill {s3}">③ Hasil Analisis</div>
    </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════
def prog_bar(label, val, color):
    pct = max(0, min(100, val))
    st.markdown(f"""<div class="prog-wrap">
      <div class="prog-lbl"><span>{label}</span>
        <span style="color:{color};font-weight:800;font-family:'Space Grotesk',sans-serif">{pct:.0f}/100</span></div>
      <div class="prog-bg">
        <div class="prog-fill" style="width:{pct:.0f}%;background:linear-gradient(90deg,{color},{color}cc)"></div>
      </div>
    </div>""", unsafe_allow_html=True)

def bobot_chips(jurusan):
    b = get_bobot(jurusan)
    chips = "".join(
        f'<div class="bobot-chip"><span class="sk">{k}</span><span class="bv">{int(b[k]*100)}%</span></div>'
        for k in SUBTES)
    st.markdown(f'<div style="display:flex;flex-wrap:wrap;gap:3px;margin:.4rem 0">{chips}</div>',
                unsafe_allow_html=True)

def step_bar(cur):
    steps = ["👤 Profil, Jenjang & Target","📊 Skor TPS","🧠 Psikologis","📚 Kebiasaan Belajar"]
    html  = '<div class="step-row">'
    for i,s in enumerate(steps,1):
        cls = "active" if i==cur else "done" if i<cur else ""
        mk  = "✓" if i<cur else str(i)
        html += f'<div class="step-item {cls}"><span class="step-num">{mk}</span>{s}</div>'
    st.markdown(html+"</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════
# PAGE: HOME
# ══════════════════════════════════════════════════════════
def page_home():
    st.markdown("""
    <div class="ticker-wrap">
      <div class="ticker-inner">
        <span class="ticker-item">🎯 SKORIA v5.0 — AI UTBK Intelligence</span>
        <span class="ticker-item">📊 Data SNPMB/BPPP Kemdikbud <span>2025/2026</span></span>
        <span class="ticker-item">🎓 Jenjang <span>S1 Sarjana</span> &amp; <span>D3 Vokasi</span></span>
        <span class="ticker-item">🏛️ <span>30 PTN</span> — Klaster 1 hingga 4</span>
        <span class="ticker-item">📚 <span>34+</span> Jurusan S1 · <span>30+</span> Prodi D3</span>
        <span class="ticker-item">🤖 Powered by <span>LightGBM AI</span></span>
        <span class="ticker-item">📅 Rencana Belajar <span>8 Minggu</span> Personal</span>
        <span class="ticker-item">🎯 SKORIA v5.0 — AI UTBK Intelligence</span>
        <span class="ticker-item">📊 Data SNPMB/BPPP Kemdikbud <span>2025/2026</span></span>
        <span class="ticker-item">🎓 Jenjang <span>S1 Sarjana</span> &amp; <span>D3 Vokasi</span></span>
        <span class="ticker-item">🏛️ <span>30 PTN</span> — Klaster 1 hingga 4</span>
        <span class="ticker-item">📚 <span>34+</span> Jurusan S1 · <span>30+</span> Prodi D3</span>
        <span class="ticker-item">🤖 Powered by <span>LightGBM AI</span></span>
        <span class="ticker-item">📅 Rencana Belajar <span>8 Minggu</span> Personal</span>
      </div>
    </div>""", unsafe_allow_html=True)

    st.markdown("""<div class="hero">
      <div class="hero-badge">🚀 v5.0 · S1 &amp; D3 · 30 PTN · 64+ Program Studi</div>
      <h1>SKORIA — Analisis Kesiapan<br><span>UTBK</span> Berbasis AI</h1>
      <p>Platform kecerdasan buatan untuk memahami peluang, gap skor, dan strategi belajar<br>
         yang dipersonalisasi. Data skor S1 &amp; D3 berbasis SNPMB/BPPP Kemdikbud 2025/2026.</p>
    </div>""", unsafe_allow_html=True)

    st.markdown("""<div class="stat-row">
      <div class="stat-box">
        <div class="stat-num">30</div>
        <div class="stat-lbl">🏛️ PTN Terkover</div>
      </div>
      <div class="stat-box">
        <div class="stat-num">64+</div>
        <div class="stat-lbl">📚 Program Studi</div>
      </div>
      <div class="stat-box">
        <div class="stat-num">7</div>
        <div class="stat-lbl">📊 Subtes TPS</div>
      </div>
      <div class="stat-box">
        <div class="stat-num">8</div>
        <div class="stat-lbl">📅 Minggu Belajar</div>
      </div>
    </div>""", unsafe_allow_html=True)

    st.markdown("""<div class="feat-grid">
      <div class="feat-card d1">
        <span class="feat-icon">📡</span>
        <div class="feat-title">Radar Chart TPS</div>
        <div class="feat-desc">Visualisasi 7 subtes vs profil ideal jurusan yang dipilih</div>
      </div>
      <div class="feat-card d2">
        <span class="feat-icon">🎓</span>
        <div class="feat-title">S1 &amp; D3 Support</div>
        <div class="feat-desc">Skor aman per jenjang, jurusan &amp; 30 PTN berbasis SNPMB 2025/2026</div>
      </div>
      <div class="feat-card d3">
        <span class="feat-icon">🤖</span>
        <div class="feat-title">AI LightGBM</div>
        <div class="feat-desc">Prediksi strategi belajar otomatis dari model machine learning</div>
      </div>
      <div class="feat-card d4">
        <span class="feat-icon">📄</span>
        <div class="feat-title">Export PDF</div>
        <div class="feat-desc">Laporan lengkap 8 minggu terstruktur siap cetak</div>
      </div>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="anim-div"></div>', unsafe_allow_html=True)
    st.markdown('<div class="sec">🤖 Tentang SKORIA</div>', unsafe_allow_html=True)
    st.markdown("""<div class="al al-i">
      <h4>SKORIA — Score Intelligence for UTBK</h4>
      Platform SKORIA mengintegrasikan <strong>Model LightGBM</strong> dengan analisis holistik:
      <ul>
        <li>🎓 <strong>Support jenjang S1 (Sarjana) &amp; D3 (Diploma Tiga)</strong> — 30+ prodi D3 dari 30 PTN</li>
        <li>📊 Skor aman per jurusan, jenjang, &amp; PTN berbasis <strong>SNPMB/BPPP Kemdikbud 2025/2026</strong></li>
        <li>🏛️ <strong>30 PTN</strong>: UI, UGM, Unair, ITB, Unpad, IPB, ITS, Undip, UB, UNS, Unhas, UPI, USU, UNY, UM, Unila, Unand, UNNES, USK, Unmul, Unsri, Unud, Unsrat, Unri, Unej, Telkom, UII, UMY, Binus, UMM</li>
        <li>🧠 Evaluasi psikologis: fokus, percaya diri, kecemasan, distraksi</li>
        <li>📡 Radar Chart, Bar Chart, Pipeline Kontribusi, Klaster PTN</li>
        <li>📅 Rencana belajar mingguan 8 minggu dengan target terukur</li>
        <li>📄 Export PDF lengkap · 🎯 Gap analysis berbasis klaster PTN</li>
      </ul>
    </div>""", unsafe_allow_html=True)

    ai_status = f'<div class="al al-s"><h4>✅ Model AI Aktif</h4>File: <code>{lgbm_fname}</code> — Prediksi strategi belajar siap digunakan.</div>' if lgbm_model else '<div class="al al-w"><h4>⚠️ Model AI Tidak Ditemukan</h4>Letakkan <code>lgbm_model_2_.pkl</code> di folder yang sama. Kalkulasi manual tetap berjalan.</div>'
    st.markdown(ai_status, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col_cta, col_info = st.columns([2,3])
    with col_cta:
        if st.button("🚀  Mulai Analisis UTBK Sekarang", type="primary", use_container_width=True):
            st.session_state.page="survey"; st.session_state.step=1; st.rerun()
    with col_info:
        st.markdown("""<div style="padding:.7rem 0;font-size:.81rem;color:#6a7a9a;line-height:1.8">
          ⏱ Waktu pengisian: ~5 menit &nbsp;·&nbsp; 🔒 Data tidak tersimpan &nbsp;·&nbsp; 📱 Mobile friendly
        </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════
# PAGE: SURVEY (4 STEPS)
# ══════════════════════════════════════════════════════════
def step1():
    st.markdown("""<div class="al al-i d1" style="margin-bottom:1rem;padding:.8rem 1.2rem">
      <h4>👤 Langkah 1 dari 4 — Profil &amp; Target</h4>
      Pilih jenjang, jurusan, dan kampus yang kamu tuju. Skor aman akan ditampilkan secara langsung.
    </div>""", unsafe_allow_html=True)
    st.markdown('<div class="form-box">', unsafe_allow_html=True)
    st.markdown('<h3>👤 Profil &amp; Target</h3>', unsafe_allow_html=True)
    d = st.session_state.data
    nama    = st.text_input("Nama Lengkap", value=d.get("nama",""), placeholder="Nama kamu...")

    prev_jenjang = d.get("jenjang", DAFTAR_JENJANG[0])
    jenjang = st.radio(
        "🎓 Jenjang yang Dituju",
        DAFTAR_JENJANG,
        index=DAFTAR_JENJANG.index(prev_jenjang),
        horizontal=True,
        help="S1 = Sarjana (4 tahun) | D3 = Diploma Tiga (3 tahun, program vokasi)"
    )

    daftar_j = get_daftar_jurusan(jenjang)
    prev_jurusan = d.get("jurusan", daftar_j[0])
    if prev_jurusan not in daftar_j:
        prev_jurusan = daftar_j[0]
    jurusan = st.selectbox(
        "🏫 Target Jurusan / Program Studi",
        daftar_j,
        index=daftar_j.index(prev_jurusan),
        help="Pilih program studi yang kamu tuju"
    )

    kampus  = st.selectbox("🏛️ Target Kampus (PTN)", DAFTAR_PTN,
                           index=DAFTAR_PTN.index(d.get("kampus",DAFTAR_PTN[0])))

    if "D3" in jenjang:
        st.markdown("""<div class="al al-p" style="margin-top:.5rem;padding:.7rem 1rem">
          <h4>📋 Tentang Jenjang D3 (Diploma Tiga)</h4>
          Program vokasi 3 tahun yang menekankan keterampilan praktis & profesional.
          Skor aman D3 umumnya <strong>35–80 poin lebih rendah</strong> dari S1 sejenis,
          namun persaingan tetap ada karena kuota lebih kecil. Data berbasis SNPMB 2025/2026.
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown("""<div class="al al-i" style="margin-top:.5rem;padding:.7rem 1rem">
          <h4>📋 Tentang Jenjang S1 (Sarjana)</h4>
          Program akademik 4 tahun. Data skor aman berbasis SNPMB/BPPP Kemdikbud & media pendidikan 2025/2026.
        </div>""", unsafe_allow_html=True)

    st.markdown("---")
    bobot_chips(jurusan)
    info = get_ptn_info(kampus, jurusan, jenjang)
    jenjang_lbl = "D3" if "D3" in jenjang else "S1"
    st.markdown(f"""<div class="al al-i" style="margin-top:.7rem">
      <h4>{info['lbl']} — {kampus}</h4>
      Skor aman <strong>{jenjang_lbl} {jurusan}</strong>:
      <strong>{info['mn']} – {info['mx']}</strong>
      <br><small style="color:#6a7a95">Berdasarkan data SNPMB/BPPP Kemdikbud & referensi media pendidikan 2025/2026</small>
    </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    if st.button("Lanjut → Skor TPS ▶", type="primary"):
        if not nama.strip(): st.error("Nama harus diisi!"); return
        st.session_state.data.update({"nama":nama,"jenjang":jenjang,"jurusan":jurusan,"kampus":kampus})
        st.session_state.step=2; st.rerun()

def step2():
    st.markdown("""<div class="al al-p d1" style="margin-bottom:1rem;padding:.8rem 1.2rem">
      <h4>📊 Langkah 2 dari 4 — Skor TPS</h4>
      Masukkan skor tryout terbaru untuk 7 subtes TPS. Radar chart akan update secara live!
    </div>""", unsafe_allow_html=True)
    st.markdown('<div class="form-box">', unsafe_allow_html=True)
    st.markdown('<h3>📊 Skor TPS (Tes Potensi Skolastik)</h3>', unsafe_allow_html=True)
    st.caption(f"Masukkan skor tryout terbaru kamu. Skala: {SKOR_MIN_TPS} – {SKOR_MAX_TPS}")
    d = st.session_state.data
    skor = {}

    pairs = [("PU","PPU"),("PBM","PK"),("LBI","LBE"),("PM",None)]
    for pair in pairs:
        cols = st.columns(2)
        for col, k in zip(cols, pair):
            if k is None: continue
            with col:
                val = d.get(k, 550)
                skor[k] = st.number_input(
                    f"{SUBTES_FULL[k]} ({k})",
                    min_value=SKOR_MIN_TPS, max_value=SKOR_MAX_TPS,
                    value=int(val), step=5,
                    key=f"n_{k}",
                    help=f"Masukkan skor {SUBTES_FULL[k]} dari tryout terakhir (200–1000)"
                )

    jurusan = d.get("jurusan", DAFTAR_JURUSAN[0])
    bobot   = get_bobot(jurusan)

    cats  = [SUBTES_FULL[k] for k in SUBTES] + [SUBTES_FULL[SUBTES[0]]]
    vals  = [skor[k] for k in SUBTES] + [skor[SUBTES[0]]]
    ideal = [min(SKOR_MAX_TPS, SKOR_MAX_TPS*bobot[k]*6) for k in SUBTES]+[min(SKOR_MAX_TPS,SKOR_MAX_TPS*bobot[SUBTES[0]]*6)]
    fig   = go.Figure()
    fig.add_trace(go.Scatterpolar(r=ideal,theta=cats,fill='toself',name='Profil Ideal',
        fillcolor='rgba(200,137,10,.08)',line=dict(color='#c8890a',dash='dot',width=2)))
    fig.add_trace(go.Scatterpolar(r=vals, theta=cats,fill='toself',name='Skor Kamu',
        fillcolor='rgba(59,108,183,.12)',line=dict(color='#3b6cb7',width=2.5)))
    fig.update_layout(**CTH,polar=dict(
        bgcolor='rgba(240,244,248,.6)',
        radialaxis=dict(range=[0,SKOR_MAX_TPS],gridcolor='#dde3ec',linecolor='#dde3ec',tickfont=dict(size=9,color='#6a7a95')),
        angularaxis=dict(gridcolor='#dde3ec',linecolor='#dde3ec',tickfont=dict(size=9.5,color='#3a4a65'))),
        legend=dict(bgcolor='rgba(255,255,255,.8)',orientation='h',x=.5,xanchor='center',y=-.15,font=dict(color='#3a4a65')),
        title=dict(text=f"Preview Radar — {jurusan}",font=dict(size=13,color='#1a2540')),height=380)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False}, key="survey_radar")
    st.markdown('</div>', unsafe_allow_html=True)
    ca,cb = st.columns([1,5])
    with ca:
        if st.button("◀ Kembali"): st.session_state.step=1; st.rerun()
    with cb:
        if st.button("Lanjut → Psikologis ▶", type="primary"):
            st.session_state.data.update(skor); st.session_state.step=3; st.rerun()

def step3():
    st.markdown("""<div class="al al-w d1" style="margin-bottom:1rem;padding:.8rem 1.2rem">
      <h4>🧠 Langkah 3 dari 4 — Kondisi Psikologis</h4>
      Nilai kondisi mental dan emosional kamu saat belajar. Faktor ini mempengaruhi risiko underperform.
    </div>""", unsafe_allow_html=True)
    st.markdown('<div class="form-box">', unsafe_allow_html=True)
    st.markdown('<h3>🧠 Kondisi Psikologis</h3>', unsafe_allow_html=True)
    st.caption("1 = Sangat Rendah · 5 = Sangat Tinggi")
    d = st.session_state.data
    ca,cb = st.columns(2)
    with ca:
        fokus = st.slider("🎯 Kemampuan Fokus Belajar",1,5,d.get("fokus",3))
        pede  = st.slider("💪 Percaya Diri",1,5,d.get("pede",3))
    with cb:
        cemas  = st.slider("😰 Tingkat Kecemasan (1=tenang, 5=sangat cemas)",1,5,d.get("cemas",3))
        distrak= st.slider("📱 Mudah Terdistraksi (1=fokus, 5=sangat mudah)",1,5,d.get("distrak",3))
    psiko = (fokus*1.5+pede*1.5+(6-cemas)+(6-distrak))/20*100
    pc = "#148a42" if psiko>=65 else "#d4900a" if psiko>=45 else "#c0392b"
    pct_p = f"{psiko:.0f}%"
    st.markdown(f"""<div class="score-ring-wrap">
      <div class="score-ring" style="--pct:{pct_p};background:conic-gradient({pc} {pct_p},#e8eef8 {pct_p})">
        <div class="score-ring-val" style="color:{pc}">{psiko:.0f}</div>
        <div class="score-ring-sub">Mental Score</div>
      </div>
    </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    ca,cb = st.columns([1,5])
    with ca:
        if st.button("◀ Kembali"): st.session_state.step=2; st.rerun()
    with cb:
        if st.button("Lanjut → Kebiasaan Belajar ▶", type="primary"):
            st.session_state.data.update({"fokus":fokus,"pede":pede,"cemas":cemas,"distrak":distrak})
            st.session_state.step=4; st.rerun()

def step4():
    st.markdown("""<div class="al al-s d1" style="margin-bottom:1rem;padding:.8rem 1.2rem">
      <h4>📚 Langkah 4 dari 4 — Kebiasaan Belajar</h4>
      Langkah terakhir! Ceritakan pola belajarmu. Data ini digunakan oleh model AI untuk rekomendasi strategi.
    </div>""", unsafe_allow_html=True)
    st.markdown('<div class="form-box">', unsafe_allow_html=True)
    st.markdown('<h3>📚 Kebiasaan Belajar</h3>', unsafe_allow_html=True)
    d = st.session_state.data
    mj = {"< 1 jam":1,"1–2 jam":2,"3–4 jam":3,"5–6 jam":4,"> 6 jam":5}
    mh = {"≤ 1 hari":1,"2 hari":2,"3 hari":3,"4–5 hari":4,"≥ 6 hari":5}
    ca,cb = st.columns(2)
    with ca:
        js = st.selectbox("⏰ Jam belajar/hari",list(mj.keys()),index=d.get("jam",3)-1)
        hs = st.selectbox("📅 Hari belajar/minggu",list(mh.keys()),index=d.get("hari",3)-1)
        lat= st.slider("✏️ Intensitas latihan soal/minggu (1–5)",1,5,d.get("latihan",3))
    with cb:
        try_= st.slider("📝 Frekuensi tryout/bulan (1–5)",1,5,d.get("tryout",2))
        rev = st.slider("🔄 Intensitas review soal salah/minggu (1–5)",1,5,d.get("review",3))
    jb = mj[js]; hb = mh[hs]
    konsist = min(100,(jb*2+hb*2.2+lat*1.8+try_*1.5+rev*1.5)*2)
    kc = "#148a42" if konsist>=65 else "#d4900a" if konsist>=45 else "#c0392b"
    pct_deg = f"{konsist:.0f}%"
    st.markdown(f"""<div class="score-ring-wrap">
      <div class="score-ring" style="--pct:{pct_deg};background:conic-gradient({kc} {pct_deg},#e8eef8 {pct_deg})">
        <div class="score-ring-val" style="color:{kc}">{konsist:.0f}</div>
        <div class="score-ring-sub">Konsistensi</div>
      </div>
    </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    ca,cb = st.columns([1,5])
    with ca:
        if st.button("◀ Kembali"): st.session_state.step=3; st.rerun()
    with cb:
        if st.button("🎯  Lihat Hasil Analisis SKORIA", type="primary"):
            st.session_state.data.update({"jam":jb,"hari":hb,"latihan":lat,"tryout":try_,"review":rev})
            st.session_state.result = compute(st.session_state.data)
            st.session_state.page="result"; st.rerun()

def page_survey():
    step_bar(st.session_state.step)
    {1:step1,2:step2,3:step3,4:step4}[st.session_state.step]()


# ══════════════════════════════════════════════════════════
# PAGE: RESULT
# ══════════════════════════════════════════════════════════
def page_result():
    r = st.session_state.result
    if not r: st.session_state.page="home"; st.rerun()

    nama = r.get("nama","Pejuang UTBK")
    jam  = datetime.datetime.now().hour
    salam= "Selamat pagi" if jam<11 else "Selamat siang" if jam<15 else "Selamat sore" if jam<18 else "Selamat malam"
    jenjang_lbl = r.get("jenjang","S1 (Sarjana)")
    jenjang_badge = "🎓 D3 Vokasi" if "D3" in jenjang_lbl else "🎓 S1 Sarjana"

    if r["pl"] == "Sangat Aman":    sb_cls, sb_dot_c = "sbg-sa", "✅"
    elif r["pl"] == "Aman":         sb_cls, sb_dot_c = "sbg-a",  "✅"
    elif r["pl"] == "Kompetitif":   sb_cls, sb_dot_c = "sbg-k",  "⚡"
    else:                            sb_cls, sb_dot_c = "sbg-r",  "🔴"

    st.markdown(f"""<div class="hero">
      <div class="hero-badge">{jenjang_badge} · {r['jurusan']} · {r['kampus']}</div>
      <h1 style="font-size:1.65rem!important">{salam}, <span>{nama}!</span> 👋</h1>
      <p>Hasil analisis <strong style="color:#ffd166">SKORIA AI</strong> berdasarkan
         skor TPS, psikologis, dan kebiasaan belajarmu · Skor skala 1000 · 30 PTN</p>
      <div style="margin-top:1rem">
        <span class="status-badge {sb_cls}">{sb_dot_c} Status: {r['pl']} · Skor {r['sw']:.0f}</span>
        &nbsp;
        <span class="status-badge sbg-a">📊 Peluang ~{r['ppct']:.0f}%</span>
      </div>
    </div>""", unsafe_allow_html=True)

    gc = "c-green" if r["gap"]>=0 else "c-red"
    pc = "c-green" if r["ppct"]>=65 else "c-orange" if r["ppct"]>=35 else "c-red"
    kc = "c-green" if r["pl"] in ("Sangat Aman","Aman") else "c-orange" if r["pl"]=="Kompetitif" else "c-red"

    k1,k2,k3,k4,k5 = st.columns(5)
    for i,(col,lbl,val,cls,sub) in enumerate([
        (k1,"Skor Tertimbang",f"{r['sw']:.0f}",kc,"dari 1000"),
        (k2,"Rata-rata Subtes",f"{r['rata']:.0f}","c-blue","7 subtes"),
        (k3,"Peluang Lolos",f"{r['ppct']:.0f}%",pc,r["pl"]),
        (k4,"Gap vs Minimum",f"{r['gap']:+.0f}",gc,f"Min {r['info']['mn']}"),
        (k5,"Risiko Underperform",r["risk"][0],
             "c-green" if r["risk"][0]=="Rendah" else "c-orange" if r["risk"][0]=="Sedang" else "c-red",
             r["risk"][1]),
    ]):
        with col:
            st.markdown(f"""<div class="card d{i+1}">
              <div class="kpi-lbl">{lbl}</div>
              <div class="kpi-val {cls}">{val}</div>
              <div class="kpi-sub">{sub}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown('<div class="anim-div"></div>', unsafe_allow_html=True)

    if r.get("lgbm_r") and r["lgbm_r"].get("ok"):
        h=r["lgbm_r"]; det=h.get("detail",{})
        kpct = f"{h['kpct']:.1f}%" if h.get("kpct") else ""
        tips = "".join(f"<li>{t}</li>" for t in det.get("tips",[]))
        st.markdown(f"""<div class="al al-s">
          <h4>🤖 Rekomendasi Strategi SKORIA AI — {det.get('icon','')} {h['strategi']}
            <span style="font-size:.78rem;font-weight:500;color:#6a7a95"> · Kepercayaan: {kpct}</span></h4>
          <em>{det.get('desc','')}</em>
          <ul style="margin-top:.35rem">{tips}</ul>
        </div>""", unsafe_allow_html=True)

    if r["pl"]=="Sangat Aman":
        st.markdown(f"""<div class="al al-s"><h4>🎯 Status: SANGAT AMAN</h4>
          Skor tertimbang <strong>{r['sw']:.0f}</strong> melampaui batas aman maksimum {r['info']['mx']} untuk {r['jurusan']} di {r['kampus']}.
          Pertahankan performa & jaga kondisi mental.</div>""", unsafe_allow_html=True)
    elif r["pl"]=="Aman":
        st.markdown(f"""<div class="al al-s"><h4>✅ Status: AMAN</h4>
          Skor {r['sw']:.0f} dalam zona aman ({r['info']['mn']}–{r['info']['mx']}).
          Tambah <strong>{r['info']['mx']-r['sw']:.0f} poin</strong> lagi untuk zona sangat aman.</div>""", unsafe_allow_html=True)
    elif r["pl"]=="Kompetitif":
        st.markdown(f"""<div class="al al-w"><h4>⚡ Status: KOMPETITIF</h4>
          Butuh <strong>+{r['info']['mn']-r['sw']:.0f} poin</strong> untuk zona aman di {r['jurusan']} - {r['kampus']}. Intensifkan latihan.</div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""<div class="al al-d"><h4>🔴 Status: PERLU PENINGKATAN</h4>
          Gap <strong>{abs(r['gap']):.0f} poin</strong> dari minimum untuk {r['jurusan']} di {r['kampus']}. Pertimbangkan bimbingan intensif atau jurusan alternatif.</div>""", unsafe_allow_html=True)

    t1,t2,t3,t4,t5,t6,t7 = st.tabs([
        "📡 Radar & Skor TPS",
        "📊 Analisis Kampus",
        "🔀 Pipeline & Bobot",
        "🎓 Jurusan",
        "🚀 Strategi",
        "📅 Rencana Mingguan",
        "📄 Export PDF",
    ])

    with t1:
        st.markdown('<div class="sec">📡 Radar TPS vs Profil Ideal Jurusan</div>', unsafe_allow_html=True)
        ch_radar(r["skor"],r["bobot"],r["jurusan"], key="r_radar_t1")
        st.markdown('<div class="sec">📊 Skor Per Subtes vs Target Kampus</div>', unsafe_allow_html=True)
        ch_bar_subtes(r["skor"],r["bobot"],r["info"], key="r_bar_t1")
        st.markdown('<div class="sec">Detail Skor Subtes</div>', unsafe_allow_html=True)
        df_data = []
        for k in SUBTES:
            sv = r["skor"][k]
            status = "✅ Kuat" if sv>=750 else "⚡ Sedang" if sv>=550 else "🔴 Perlu Fokus"
            df_data.append({
                "Subtes": SUBTES_FULL[k],
                "Bobot (%)": f"{r['bobot'][k]*100:.0f}%",
                "Skor": sv,
                "Kontribusi": f"{sv*r['bobot'][k]:.1f}",
                "Status": status,
            })
        st.dataframe(
            pd.DataFrame(df_data),
            use_container_width=True, hide_index=True,
            column_config={
                "Skor": st.column_config.ProgressColumn("Skor", min_value=200, max_value=1000, format="%d"),
            }
        )

    with t2:
        st.markdown('<div class="sec">📊 Posisi Skor vs Klaster PTN</div>', unsafe_allow_html=True)
        ch_klaster(r["sw"], key="r_kl_t2")
        st.markdown(f'<div class="sec">🏛️ PTN Klaster {r["info"]["k"]} — Skor per {r["jurusan"]} ({r.get("jenjang","S1")})</div>', unsafe_allow_html=True)
        ch_ptn(r["sw"], r["info"]["k"], r["jurusan"], r.get("jenjang","S1 (Sarjana)"), key="r_ptn_t2")
        st.markdown('<div class="sec">Ringkasan Peluang per Klaster</div>', unsafe_allow_html=True)
        jenjang_r = r.get("jenjang","S1 (Sarjana)")
        kl_rows = []
        for kno,(mn_k,mx_k,knm) in [(1,(850,950,"⭐ Klaster 1 — Top Tier")),
                                      (2,(700,870,"🔷 Klaster 2 — Menengah Atas")),
                                      (3,(600,720,"🔹 Klaster 3 — Menengah")),
                                      (4,(555,660,"🔸 Klaster 4 — Regional"))]:
            if "D3" in jenjang_r:
                ptn_klaster = [k for k,v in PTN_D3_DATA.items() if v.get("_klaster")==kno]
            else:
                ptn_klaster = [k for k,v in PTN_JURUSAN_DATA.items() if v.get("_klaster")==kno]
            if ptn_klaster:
                info_k = get_ptn_info(ptn_klaster[0], r["jurusan"], jenjang_r)
                mn_k, mx_k = info_k["mn"], info_k["mx"]
            g = r["sw"] - mn_k
            if r["sw"]>=mx_k: st_k,p_k="🎯 Sangat Aman","~87%"
            elif r["sw"]>=mn_k: st_k,p_k="✅ Aman","~72%"
            elif r["sw"]>=mn_k-70: st_k,p_k="⚡ Kompetitif","~42%"
            else: st_k,p_k="🔴 Berisiko","~16%"
            kl_rows.append({
                "Klaster": knm,
                "Rentang Skor": f"{mn_k}–{mx_k}",
                "Skor Kamu": f"{r['sw']:.0f}",
                "Gap": f"{g:+.0f}",
                "Status": st_k,
                "Est. Peluang": p_k
            })
        st.dataframe(pd.DataFrame(kl_rows), use_container_width=True, hide_index=True)
        d1,d2,d3 = st.columns(3)
        with d1: st.metric("Skor Minimum Aman",r["info"]["mn"])
        with d2: st.metric("Skor Sangat Aman",r["info"]["mx"])
        with d3: st.metric("Skor Tertimbang Kamu",f"{r['sw']:.0f}",
                            delta=f"{r['gap']:+.0f} vs minimum",
                            delta_color="normal" if r["gap"]>=0 else "inverse")

    with t3:
        st.markdown('<div class="sec">🔀 Pipeline Kontribusi Subtes → Skor Total</div>', unsafe_allow_html=True)
        st.caption("Batang berwarna = kontribusi aktual. Batang transparan = target minimum kampus.")
        ch_pipeline(r["skor"],r["bobot"],r["info"],r["jurusan"], key="r_pipe_t3")
        st.markdown(f'<div class="sec">📐 Distribusi Bobot Subtes — {r["jurusan"]}</div>', unsafe_allow_html=True)
        ch_bobot(r["jurusan"], key="r_bobot_t3")
        st.markdown('<div class="sec">Tabel Bobot & Kontribusi Detail</div>', unsafe_allow_html=True)
        df_b_data = []
        for k in SUBTES:
            df_b_data.append({
                "Subtes": SUBTES_FULL[k],
                "Bobot": f"{r['bobot'][k]*100:.0f}%",
                "Skor": r["skor"][k],
                "Kontribusi Aktual": f"{r['skor'][k]*r['bobot'][k]:.1f}",
                "Target Minimum": f"{r['info']['mn']*r['bobot'][k]:.1f}",
                "Selisih": f"{(r['skor'][k]-r['info']['mn'])*r['bobot'][k]:+.1f}",
            })
        df_b_data.append({
            "Subtes": "TOTAL",
            "Bobot": "100%",
            "Skor": "—",
            "Kontribusi Aktual": f"{r['sw']:.1f}",
            "Target Minimum": f"{r['info']['mn']:.0f}",
            "Selisih": f"{r['gap']:+.1f}",
        })
        st.dataframe(pd.DataFrame(df_b_data), use_container_width=True, hide_index=True)
        with st.expander("📊 Lihat bobot semua jurusan"):
            rows_all = []
            for j,b in BOBOT_MAP.items():
                row={"Jurusan":j}; row.update({f"{k}(%)":f"{b[k]*100:.0f}" for k in SUBTES})
                rows_all.append(row)
            st.dataframe(pd.DataFrame(rows_all), use_container_width=True, hide_index=True)

    with t4:
        st.markdown(f'<div class="sec">🎓 Analisis Jurusan — {r["jurusan"]}</div>', unsafe_allow_html=True)
        if r["aman"]:
            st.markdown(f"""<div class="al al-s">
              <h4>🎯 FOKUS KE JURUSAN TARGET: {r['jurusan']}</h4>
              Peluang lolos <strong>{r['pl']}</strong> ({r['ppct']:.0f}%) — tidak perlu berpindah jurusan.
              Pertahankan dan tingkatkan skor menjelang UTBK.
            </div>""", unsafe_allow_html=True)
            bobot_chips(r["jurusan"])
            col_a, col_b = st.columns(2)
            with col_a:
                ch_bobot(r["jurusan"], key="r_bobot_t4_main")
            with col_b:
                st.markdown("<p style='color:#3a4a65;font-weight:600;margin-bottom:.8rem'>📈 Indikator Kesiapan:</p>", unsafe_allow_html=True)
                prog_bar("Kesiapan Mental",r["psiko"],"#3b6cb7")
                prog_bar("Konsistensi Belajar",r["konsist"],"#1a8a4a")
                prog_bar("Stabilitas Mental",r["stab"],"#7048c8")
            bs = sorted(r["bobot"].items(),key=lambda x:x[1],reverse=True)
            st.markdown('<div class="sec">🔑 Subtes Kunci (Bobot Tertinggi)</div>', unsafe_allow_html=True)
            sc = st.columns(3)
            for col,(k,bv) in zip(sc,bs[:3]):
                sv = r["skor"][k]
                kc2 = "c-green" if sv>=750 else "c-gold" if sv>=550 else "c-red"
                with col:
                    st.markdown(f"""<div class="card" style="text-align:center">
                      <div class="kpi-lbl">{SUBTES_FULL[k]}</div>
                      <div class="kpi-val {kc2}">{sv}</div>
                      <div class="kpi-sub">Bobot {int(bv*100)}% {'✅' if sv>=750 else '⚡' if sv>=550 else '🔴'}</div>
                    </div>""", unsafe_allow_html=True)
            st.markdown('<div class="sec">📋 Jurusan Alternatif (Cadangan)</div>', unsafe_allow_html=True)
            st.markdown('<div class="al al-i"><h4>ℹ️ Info</h4>Skor kamu sudah aman. Alternatif ini hanya cadangan formalitas.</div>', unsafe_allow_html=True)
            alt = r["alternatif"]
            if alt:
                ac = st.columns(len(alt))
                for col,j in zip(ac,alt):
                    with col:
                        bj=get_bobot(j); swj=hitung_tw(r["skor"],bj)
                        plj,_,pctj=hitung_peluang(swj,r["kampus"],j,r.get("jenjang","S1 (Sarjana)"))
                        st.markdown(f"""<div class="card" style="text-align:center;opacity:.75">
                          <div style="font-size:.7rem;color:#6a7a95">Alternatif</div>
                          <div style="font-weight:700;font-size:.87rem;margin:.2rem 0;color:#1a2540">{j}</div>
                          <div style="font-size:.75rem;color:#3a4a65">{plj} ({pctj:.0f}%)</div>
                        </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""<div class="al al-w">
              <h4>⚡ Skor Belum Zona Aman — {r['jurusan']}</h4>
              Butuh <strong>+{r['info']['mn']-r['sw']:.0f} poin</strong>. Pertimbangkan jurusan alternatif.
            </div>""", unsafe_allow_html=True)
            bobot_chips(r["jurusan"])
            ch_bobot(r["jurusan"], key="r_bobot_t4_alt")
            st.markdown('<div class="sec">🔄 Jurusan Alternatif yang Direkomendasikan</div>', unsafe_allow_html=True)
            for idx,j in enumerate(r["alternatif"]):
                bj = get_bobot(j); swj = hitung_tw(r["skor"],bj)
                plj,_,pctj = hitung_peluang(swj, r["kampus"], j, r.get("jenjang","S1 (Sarjana)"))
                info_j = get_ptn_info(r["kampus"], j, r.get("jenjang","S1 (Sarjana)"))
                with st.expander(f"📚 {j}  —  Skor: {swj:.0f}  |  {plj}  ({pctj:.0f}%)"):
                    ca2,cb2 = st.columns(2)
                    with ca2:
                        st.metric("Skor Tertimbang",f"{swj:.0f}")
                        st.metric("Peluang",f"{pctj:.0f}% ({plj})")
                        st.metric("Skor Aman",f"{info_j['mn']}–{info_j['mx']}")
                        bobot_chips(j)
                    with cb2:
                        ch_bobot(j, key=f"r_bobot_alt_{idx}")

    with t5:
        st.markdown('<div class="sec">🚀 Strategi Belajar Personal</div>', unsafe_allow_html=True)
        ch_psiko(r["psiko"],r["konsist"],r["stab"], key="r_psiko_t5")
        prog_bar("Kesiapan Mental",r["psiko"],"#3b6cb7")
        prog_bar("Konsistensi Belajar",r["konsist"],"#1a8a4a")
        prog_bar("Stabilitas Mental",r["stab"],"#7048c8")
        st.markdown('<div class="sec">📌 Prioritas Subtes</div>', unsafe_allow_html=True)
        ss = sorted(r["skor"].items(),key=lambda x:x[1])
        lemah3 = ss[:3]; kuat2 = ss[-2:]
        cp1,cp2 = st.columns(2)
        with cp1:
            il = "".join(f"<li><strong>{SUBTES_FULL[k]}</strong>: {v} → perlu +{max(0,750-v)} poin</li>" for k,v in lemah3)
            st.markdown(f'<div class="al al-d"><h4>🔴 3 Subtes Perlu Fokus</h4><ul>{il}</ul></div>',unsafe_allow_html=True)
        with cp2:
            ik = "".join(f"<li><strong>{SUBTES_FULL[k]}</strong>: {v} ✅</li>" for k,v in kuat2)
            st.markdown(f'<div class="al al-s"><h4>🟢 Kekuatan Akademik</h4><ul>{ik}</ul></div>',unsafe_allow_html=True)
        st.markdown('<div class="sec">📋 Rencana Aksi</div>', unsafe_allow_html=True)
        if r["sw"]>=r["info"]["mx"]:
            st.markdown("""<div class="al al-s"><h4>🏆 Maintenance Mode</h4><ul>
              <li>Tryout 1–2x/minggu untuk menjaga ketajaman</li>
              <li>Review kesalahan kecil yang masih berulang</li>
              <li>Fokus manajemen waktu dan kondisi mental</li>
              <li>Jaga pola tidur 7–8 jam/malam</li></ul></div>""",unsafe_allow_html=True)
        elif r["sw"]>=r["info"]["mn"]:
            st.markdown(f"""<div class="al al-i"><h4>✅ Penguatan & Konsistensi</h4><ul>
              <li>Target +{r['info']['mx']-r['sw']:.0f} poin untuk zona sangat aman</li>
              <li>60% waktu pada {SUBTES_FULL[ss[0][0]]} (terlemah)</li>
              <li>Tryout min. 2x/bulan + review mendalam</li>
              <li>Simulasi 150 soal dalam 2.5 jam/sesi</li></ul></div>""",unsafe_allow_html=True)
        else:
            st.markdown(f"""<div class="al al-w"><h4>⚡ Intensifikasi Penuh</h4><ul>
              <li>Target +{r['info']['mn']-r['sw']:.0f} poin — bertahap +{min(60,r['info']['mn']-r['sw']):.0f}/bulan</li>
              <li>Belajar 4–5 jam/hari terstruktur</li>
              <li>Tryout mingguan + analisis soal salah mendalam</li>
              <li>Konsultasi tutor untuk subtes berbobot tinggi</li></ul></div>""",unsafe_allow_html=True)
        st.markdown('<div class="sec">🧠 Tips Psikologis</div>', unsafe_allow_html=True)
        tp1,tp2 = st.columns(2)
        with tp1:
            if r.get("fokus",3)<=2:
                st.markdown('<div class="al al-d"><h4>🎯 Fokus Rendah</h4><ul><li>Pomodoro 25+5 mnt</li><li>Matikan notifikasi HP</li><li>Mulai sesi pendek 15 mnt</li></ul></div>',unsafe_allow_html=True)
            if r.get("cemas",3)>=4:
                st.markdown('<div class="al al-d"><h4>😰 Kecemasan Tinggi</h4><ul><li>Pernapasan 4-7-8 tiap pagi</li><li>Fokus proses bukan hasil</li><li>Tidur 7–8 jam/malam</li></ul></div>',unsafe_allow_html=True)
        with tp2:
            if r.get("distrak",3)>=4:
                st.markdown('<div class="al al-d"><h4>📱 Distraksi Tinggi</h4><ul><li>Cold Turkey / Forest app</li><li>HP di ruangan lain</li><li>Reward setelah selesai sesi</li></ul></div>',unsafe_allow_html=True)
            if r.get("review",3)<=2:
                st.markdown('<div class="al al-w"><h4>📝 Review Soal Kurang</h4><ul><li>Review SETIAP soal salah</li><li>Buku catatan soal sulit</li></ul></div>',unsafe_allow_html=True)

    with t6:
        st.markdown('<div class="sec">📅 Proyeksi Skor 8 Minggu ke Depan</div>', unsafe_allow_html=True)
        ch_progress(r, key="r_prog_t6")
        st.markdown('<div class="sec">📋 Detail Rencana Per Minggu</div>', unsafe_allow_html=True)
        rencana = buat_rencana_mingguan(r, 8)
        fase_clr = {"Fondasi":"#3b6cb7","Intensif":"#d4620a","Pemantapan":"#1a8a4a","Final":"#c8890a"}
        for m in rencana:
            clr = fase_clr.get(m["fase"],"#7048c8")
            tasks_html = "".join(f'<div style="padding:.1rem 0;color:#3a4a65">• {t}</div>' for t in m["tasks"])
            st.markdown(f"""<div class="week-card">
              <div class="week-num" style="color:{clr}">MINGGU {m['minggu']} — {m['fase'].upper()}</div>
              <div class="week-target">
                🎯 Target skor: <strong style="color:{clr}">{m['target_skor']}</strong> &nbsp;|&nbsp; ⏰ {m['jam']}
              </div>
              <div class="week-tasks">{tasks_html}</div>
            </div>""", unsafe_allow_html=True)
        st.markdown('<div class="sec">Ringkasan Rencana 8 Minggu</div>', unsafe_allow_html=True)
        df_r = pd.DataFrame([{
            "Minggu": f"Minggu {m['minggu']}",
            "Fase": m["fase"],
            "Target Skor": m["target_skor"],
            "Durasi Belajar": m["jam"],
            "Fokus Utama": m["fokus"]
        } for m in rencana])
        st.dataframe(df_r, use_container_width=True, hide_index=True)

    with t7:
        st.markdown('<div class="sec">📄 Export Laporan ke PDF</div>', unsafe_allow_html=True)
        st.markdown("""<div class="al al-i"><h4>Cara Menyimpan sebagai PDF</h4><ol>
          <li>Klik tombol <strong>Generate & Download Laporan HTML</strong> di bawah</li>
          <li>Buka file HTML yang terdownload di browser</li>
          <li>Tekan <strong>Ctrl+P</strong> (Win) atau <strong>Cmd+P</strong> (Mac)</li>
          <li>Pilih <strong>"Save as PDF"</strong> sebagai printer</li>
          <li>Klik <strong>Save</strong></li>
        </ol></div>""", unsafe_allow_html=True)
        if st.button("📄  Generate & Download Laporan HTML", type="primary"):
            html = generate_pdf(r)
            b64  = base64.b64encode(html.encode()).decode()
            fn   = f"skoria_{r.get('nama','').replace(' ','_')}.html"
            st.markdown(f"""<a href="data:text/html;base64,{b64}" download="{fn}"
              style="display:inline-block;background:linear-gradient(135deg,#3b6cb7,#2a4a8c);
                     color:#ffffff;font-weight:700;padding:.6rem 1.4rem;border-radius:8px;
                     text-decoration:none;font-family:'Sora',sans-serif;font-size:.9rem;margin-top:.5rem">
              ⬇️ Download {fn}</a>""", unsafe_allow_html=True)
        st.markdown('<div class="sec">Preview Ringkasan Laporan</div>', unsafe_allow_html=True)
        pp1,pp2 = st.columns(2)
        with pp1:
            st.dataframe(pd.DataFrame([
                {"Info": "Nama", "Detail": r.get("nama","—")},
                {"Info": "Jurusan", "Detail": r["jurusan"]},
                {"Info": "Kampus", "Detail": r["kampus"]},
                {"Info": "Klaster", "Detail": r["info"]["lbl"]},
                {"Info": "Skor Tertimbang", "Detail": f"{r['sw']:.0f} / 1000"},
                {"Info": "Gap vs Minimum", "Detail": f"{r['gap']:+.0f}"},
            ]), use_container_width=True, hide_index=True)
        with pp2:
            st.dataframe(pd.DataFrame([
                {"Indikator": "Peluang Lolos", "Nilai": f"{r['ppct']:.0f}% ({r['pl']})"},
                {"Indikator": "Kesiapan Mental", "Nilai": f"{r['psiko']:.0f}/100"},
                {"Indikator": "Konsistensi", "Nilai": f"{r['konsist']:.0f}/100"},
                {"Indikator": "Stabilitas", "Nilai": f"{r['stab']:.0f}/100"},
                {"Indikator": "Risiko Underperform", "Nilai": f"{r['risk'][0]} {r['risk'][1]}"},
            ]), use_container_width=True, hide_index=True)

    st.divider()
    nb1,nb2,_ = st.columns([1,1,4])
    with nb1:
        if st.button("◀ Ubah Data"): st.session_state.page="survey"; st.session_state.step=1; st.rerun()
    with nb2:
        if st.button("🏠 Beranda"): st.session_state.page="home"; st.rerun()

    st.markdown(f"""<div style="text-align:center;padding:1.4rem;background:var(--surf);
      border-radius:var(--r);border:1px solid var(--border);margin-top:.8rem;
      box-shadow:var(--shadow)">
      <div style="font-family:'Sora',sans-serif;font-size:1.05rem;font-weight:800;color:#1a2540">
        💪 {nama}, kamu pasti bisa!
      </div>
      <div style="color:#6a7a95;font-size:.82rem;margin-top:.3rem">
        Konsistensi + strategi tepat = PTN impianmu pasti bisa diraih 🚀
      </div>
      <div style="color:#b0b8c8;font-size:.7rem;margin-top:.3rem">
        🎯 SKORIA v5.0 — AI UTBK Intelligence · LightGBM + Data SNPMB 2025/2026 · S1 & D3 · 30 PTN · Skor skala 200–1000
      </div>
    </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════
def main():
    render_nav()
    {"home":page_home,"survey":page_survey,"result":page_result}[st.session_state.page]()

if __name__=="__main__":
    main()
