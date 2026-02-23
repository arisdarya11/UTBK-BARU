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
# GLOBAL CSS — Animated Design System v4.2
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
@keyframes countUp {
  from { opacity:0; transform:translateY(14px) scale(.8); }
  to   { opacity:1; transform:translateY(0) scale(1); }
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
@keyframes typeBar { from { width:0; } }

html,body,[class*="css"],.stApp {
  background: var(--bg) !important;
  font-family: 'Plus Jakarta Sans', sans-serif !important;
  color: var(--text) !important;
}
#MainMenu, footer, header { visibility:hidden }
.stDeployButton { display:none }
.block-container { padding:1rem 1.5rem !important; max-width:100% !important; }
.main .block-container { animation: fadeSlideUp .5s cubic-bezier(.22,.68,0,1.2) both; }

.topbar {
  background:#fff; border-bottom:2px solid var(--border);
  padding:.6rem 2rem; display:flex; align-items:center; gap:1.2rem;
  margin:-1rem -1.5rem 1.5rem -1.5rem;
  position:sticky; top:0; z-index:999;
  box-shadow:0 2px 12px rgba(30,60,140,.07);
  animation:fadeSlideLeft .4s ease both;
}
.topbar-brand {
  font-family:'Space Grotesk',sans-serif;
  font-size:1.1rem; font-weight:800; color:var(--accent) !important;
  display:flex; align-items:center; gap:.5rem;
  animation:float 4s ease-in-out infinite;
}
.topbar-tag { font-size:.68rem; color:var(--text3); letter-spacing:.04em; }
.step-pill {
  font-size:.72rem; font-weight:600; padding:.26rem .8rem; border-radius:99px;
  color:var(--text3); background:var(--surf2); border:1px solid var(--border);
  transition:all .3s ease;
}
.step-pill.done  { background:#e6f5ee; color:var(--green); border-color:#9adbb8; animation:popIn .5s ease both; }
.step-pill.active{ background:#eef2fc; color:var(--accent); border-color:#aac0f0; animation:pulseRing 2.5s ease-in-out infinite; }

.hero {
  background:linear-gradient(135deg,#1a3470 0%,#3464c8 55%,#2a50a8 100%);
  border-radius:16px; padding:2.4rem 3rem; margin-bottom:1.8rem;
  position:relative; overflow:hidden;
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

.anim-div {
  height:2px; border-radius:99px; margin:1.2rem 0;
  background:linear-gradient(90deg,var(--accent),var(--purple),var(--teal),var(--gold),var(--accent));
  background-size:300% auto; animation:gradientFlow 4s linear infinite;
}

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

.feat-grid { display:grid; grid-template-columns:repeat(4,1fr); gap:1rem; margin-bottom:1.4rem; }
.feat-card {
  background:var(--surf); border:1px solid var(--border); border-radius:14px;
  padding:1.6rem 1.2rem; text-align:center; box-shadow:var(--sh);
  transition:all .32s cubic-bezier(.22,.68,0,1.2);
  position:relative; overflow:hidden; animation:fadeSlideUp .5s ease both;
}
.feat-card:hover { transform:translateY(-8px) scale(1.02); box-shadow:var(--sh2); }
.feat-icon { font-size:2.2rem; margin-bottom:.6rem; display:block; animation:float 3.2s ease-in-out infinite; }
.feat-card:nth-child(2) .feat-icon { animation-delay:.3s; }
.feat-card:nth-child(3) .feat-icon { animation-delay:.6s; }
.feat-card:nth-child(4) .feat-icon { animation-delay:.9s; }
.feat-title { font-family:'Space Grotesk',sans-serif; font-weight:700; font-size:.9rem; color:var(--text); margin-bottom:.35rem; }
.feat-desc { font-size:.76rem; color:var(--text3); line-height:1.6; }

.stat-row { display:grid; grid-template-columns:repeat(4,1fr); gap:.8rem; margin-bottom:1.4rem; }
.stat-box {
  background:linear-gradient(135deg,var(--accent),var(--purple));
  border-radius:12px; padding:1.1rem 1rem; text-align:center;
  box-shadow:0 4px 16px rgba(52,100,200,.25); animation:popIn .6s ease both;
}
.stat-box:nth-child(2) { background:linear-gradient(135deg,var(--purple),var(--teal)); animation-delay:.1s; }
.stat-box:nth-child(3) { background:linear-gradient(135deg,var(--teal),var(--green)); animation-delay:.2s; }
.stat-box:nth-child(4) { background:linear-gradient(135deg,var(--gold),var(--orange)); animation-delay:.3s; }
.stat-num { font-family:'Space Grotesk',sans-serif; font-size:1.6rem; font-weight:800; color:#fff; animation:countUp .8s cubic-bezier(.22,.68,0,1.2) .4s both; }
.stat-lbl { font-size:.72rem; color:rgba(255,255,255,.82); font-weight:600; margin-top:.15rem; }

.step-row {
  display:flex; margin-bottom:1.8rem; background:var(--surf); border:1px solid var(--border);
  border-radius:var(--r); overflow:hidden; box-shadow:var(--sh); animation:fadeSlideUp .45s ease .05s both;
}
.step-item {
  flex:1; padding:.9rem; text-align:center; font-size:.73rem; font-weight:600; color:var(--text3);
  border-right:1px solid var(--border); transition:background .4s ease, color .3s ease;
}
.step-item:last-child { border-right:none; }
.step-item.active { background:linear-gradient(135deg,#eef2fc,#e8f0ff); color:var(--accent); animation:pulseRing 2.5s ease-in-out infinite; }
.step-item.done { background:#e8f5ee; color:var(--green); }
.step-item.done .step-num { animation:starSpin .5s ease both; }
.step-num { display:block; font-size:1.15rem; font-family:'Space Grotesk',sans-serif; font-weight:800; margin-bottom:1px; }

.form-box {
  background:var(--surf); border:1px solid var(--border); border-radius:var(--r);
  padding:1.8rem 2rem; margin-bottom:1.2rem; box-shadow:var(--sh);
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
.form-box h3 { font-family:'Space Grotesk',sans-serif; font-size:1rem; font-weight:700; color:var(--accent); margin:0 0 1.2rem; animation:fadeSlideLeft .5s ease both; }

.sec {
  font-family:'Space Grotesk',sans-serif; font-size:.94rem; font-weight:700; color:var(--text);
  margin:1.6rem 0 .75rem; padding-bottom:.35rem; border-bottom:2px solid var(--border);
  animation:fadeSlideLeft .4s ease both; position:relative;
}
.sec::after {
  content:''; position:absolute; bottom:-2px; left:0; height:2px;
  background:linear-gradient(90deg,var(--accent),var(--a2)); animation:typeBar .7s ease .2s both;
}

.card {
  background:var(--surf); border:1px solid var(--border); border-radius:var(--r);
  padding:1.2rem 1.4rem; box-shadow:var(--sh);
  transition:transform .28s ease, box-shadow .28s ease; animation:fadeSlideUp .5s ease both;
}
.card:hover { transform:translateY(-4px); box-shadow:var(--sh2); }
.kpi-lbl { font-size:.67rem; font-weight:700; text-transform:uppercase; letter-spacing:.1em; color:var(--text3); margin-bottom:.3rem; }
.kpi-val { font-family:'Space Grotesk',sans-serif; font-size:1.9rem; font-weight:800; line-height:1; animation:countUp .6s cubic-bezier(.22,.68,0,1.2) .2s both; }
.kpi-sub { font-size:.71rem; color:var(--text3); margin-top:.2rem; }

.c-gold   { color:var(--gold)!important; }
.c-green  { color:var(--green)!important; }
.c-red    { color:var(--red)!important; }
.c-orange { color:var(--orange)!important; }
.c-blue   { color:var(--a2)!important; }
.c-purple { color:var(--purple)!important; }
.c-teal   { color:var(--teal)!important; }

.al {
  border-radius:var(--r); padding:1rem 1.3rem; margin-bottom:.9rem;
  border-left:4px solid; font-size:.86rem; line-height:1.75; color:var(--text2);
  box-shadow:var(--sh); animation:fadeSlideRight .45s cubic-bezier(.22,.68,0,1.2) both;
  transition:transform .22s ease, box-shadow .22s ease;
}
.al:hover { transform:translateX(5px); box-shadow:var(--sh2); }
.al h4 { margin:0 0 .4rem; font-size:.9rem; font-weight:700; }
.al ul { margin:.35rem 0 0; padding-left:1.3rem; }
.al li { margin-bottom:.22rem; }
.al strong { color:var(--text); }
.al-s  { background:#edfbf3; border-color:var(--green); }  .al-s h4 { color:var(--green); }
.al-w  { background:#fff7ee; border-color:var(--orange); } .al-w h4 { color:var(--orange); }
.al-d  { background:#fff0f0; border-color:var(--red); }    .al-d h4 { color:var(--red); }
.al-i  { background:#eef2fc; border-color:var(--accent); } .al-i h4 { color:var(--accent); }
.al-p  { background:#f3eeff; border-color:var(--purple); } .al-p h4 { color:var(--purple); }
.al-na { background:#ffe8e8; border-color:#c0392b; }       .al-na h4 { color:#c0392b; }
.al-br { background:#fff3e0; border-color:#e67e22; }       .al-br h4 { color:#e67e22; }

/* ── 4 STATUS KATEGORI BADGE ── */
.badge-sa  { background:#e6f5ee; color:#148a42; border:1.5px solid #9adbb8; }
.badge-a   { background:#edf6ff; color:#1a5fa0; border:1.5px solid #90c0f0; }
.badge-br  { background:#fff4e6; color:#d4620a; border:1.5px solid #f4c08a; }
.badge-na  { background:#fff0f0; color:#c0392b; border:1.5px solid #f4a0a0; }

.prog-wrap { margin-bottom:.75rem; }
.prog-lbl { display:flex; justify-content:space-between; font-size:.79rem; font-weight:600; color:var(--text2); margin-bottom:5px; }
.prog-bg { background:var(--surf2); border-radius:99px; height:10px; overflow:hidden; border:1px solid var(--border); }
.prog-fill { height:100%; border-radius:99px; animation:progressGrow .9s cubic-bezier(.22,.68,0,1.2) .3s both; position:relative; overflow:hidden; }
.prog-fill::after {
  content:''; position:absolute; inset:0;
  background:linear-gradient(90deg,transparent 0%,rgba(255,255,255,.45) 50%,transparent 100%);
  background-size:200% 100%; animation:shimmer 2s ease 1.4s infinite;
}

.bobot-chip {
  display:inline-flex; flex-direction:column; align-items:center;
  background:#eef2fc; border:1px solid #b8cff0; border-radius:8px; padding:.4rem .65rem; margin:.12rem;
  transition:transform .22s ease, background .22s ease; animation:popIn .5s ease both;
}
.bobot-chip:hover { transform:scale(1.12) translateY(-2px); background:#dde8f8; }
.bobot-chip .sk { font-size:.62rem; color:var(--text3); margin-bottom:2px; }
.bobot-chip .bv { font-size:.96rem; font-weight:800; color:var(--accent); font-family:'Space Grotesk',sans-serif; }

.week-card {
  background:var(--surf); border:1px solid var(--border); border-radius:12px;
  padding:1rem 1.2rem; margin-bottom:.65rem; box-shadow:var(--sh);
  transition:transform .25s ease, border-color .25s ease, box-shadow .25s ease;
  animation:fadeSlideUp .5s ease both; border-left:4px solid transparent;
}
.week-card:hover { transform:translateX(8px); border-left-color:var(--accent); box-shadow:var(--sh2); }
.week-num { font-family:'Space Grotesk',sans-serif; font-size:.72rem; font-weight:700; color:var(--accent); text-transform:uppercase; letter-spacing:.1em; margin-bottom:.28rem; }
.week-target { font-size:.84rem; font-weight:700; color:var(--text); margin-bottom:.24rem; }
.week-tasks { font-size:.79rem; color:var(--text2); line-height:1.68; }

.status-badge { display:inline-flex; align-items:center; gap:.45rem; padding:.42rem 1.1rem; border-radius:99px; font-size:.78rem; font-weight:700; animation:popIn .6s ease both; }

.score-ring-wrap { display:flex; justify-content:center; padding:1rem 0; }
.score-ring {
  width:148px; height:148px; border-radius:50%;
  background:conic-gradient(var(--accent) var(--pct,0%), #e8eef8 var(--pct,0%));
  display:flex; flex-direction:column; align-items:center; justify-content:center;
  position:relative; animation:popIn .8s cubic-bezier(.22,.68,0,1.2) .1s both;
  box-shadow:0 4px 24px rgba(52,100,200,.2);
}
.score-ring::before { content:''; position:absolute; inset:13px; border-radius:50%; background:var(--surf); box-shadow:inset 0 2px 10px rgba(52,100,200,.08); }
.score-ring-val { position:relative; z-index:1; font-family:'Space Grotesk',sans-serif; font-size:1.65rem; font-weight:800; color:var(--accent); animation:countUp .9s ease .5s both; }
.score-ring-sub { position:relative; z-index:1; font-size:.62rem; color:var(--text3); }

/* 4-level skor gauge */
.skor-legend {
  display:flex; gap:.5rem; flex-wrap:wrap; margin:.6rem 0;
}
.skor-legend-item {
  display:inline-flex; align-items:center; gap:.35rem;
  padding:.25rem .65rem; border-radius:99px; font-size:.72rem; font-weight:700;
}
.sl-na  { background:#fff0f0; color:#c0392b; border:1.5px solid #f4a0a0; }
.sl-br  { background:#fff4e6; color:#e67e22; border:1.5px solid #f4c08a; }
.sl-a   { background:#edf6ff; color:#1a5fa0; border:1.5px solid #90c0f0; }
.sl-sa  { background:#e6f5ee; color:#148a42; border:1.5px solid #9adbb8; }

/* ── FITUR PANEL ── */
.fitur-panel {
  background:var(--surf); border:1.5px solid var(--border); border-radius:16px;
  padding:1.8rem 2rem; margin-bottom:1.6rem; box-shadow:var(--sh);
  animation:fadeSlideUp .6s ease both;
  position:relative; overflow:hidden;
}
.fitur-panel::before {
  content:''; position:absolute; top:0; left:0; right:0; height:4px;
  background:linear-gradient(90deg,var(--accent),var(--purple),var(--teal));
  animation:gradientFlow 4s linear infinite; background-size:300% auto;
}
.fitur-panel-title {
  font-family:'Space Grotesk',sans-serif; font-size:1.05rem; font-weight:800;
  color:var(--text); margin-bottom:1.1rem; display:flex; align-items:center; gap:.5rem;
}
.fitur-grid-3 { display:grid; grid-template-columns:repeat(3,1fr); gap:.9rem; }
.fitur-item {
  background:var(--surf2); border:1px solid var(--border); border-radius:12px;
  padding:1rem 1.1rem; transition:all .25s ease; animation:fadeSlideUp .5s ease both;
}
.fitur-item:hover { background:#eef2fc; border-color:var(--a2); transform:translateY(-3px); box-shadow:var(--sh2); }
.fitur-item-icon { font-size:1.6rem; margin-bottom:.4rem; display:block; }
.fitur-item-title { font-family:'Space Grotesk',sans-serif; font-size:.82rem; font-weight:700; color:var(--text); margin-bottom:.3rem; }
.fitur-item-desc { font-size:.73rem; color:var(--text3); line-height:1.6; }

div[data-testid="stButton"] button[kind="primary"] {
  background:linear-gradient(135deg,var(--accent),#1a3470) !important;
  color:#fff !important; font-weight:700 !important; font-family:'Space Grotesk',sans-serif !important;
  border:none !important; border-radius:10px !important; font-size:.89rem !important;
  letter-spacing:.02em !important; transition:all .28s cubic-bezier(.22,.68,0,1.2) !important;
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
  transform:translateY(-2px) !important; box-shadow:0 4px 14px rgba(52,100,200,.15) !important;
}
div[data-testid="stTabs"] button[data-baseweb="tab"] { font-family:'Space Grotesk',sans-serif !important; font-weight:700 !important; font-size:.79rem !important; color:var(--text3) !important; }
div[data-testid="stTabs"] button[aria-selected="true"] { color:var(--accent) !important; border-bottom-color:var(--accent) !important; }
div[data-testid="stMetric"] { background:var(--surf) !important; border:1px solid var(--border) !important; border-radius:var(--r) !important; padding:1.1rem 1.3rem !important; box-shadow:var(--sh) !important; }
div[data-testid="stMetric"]:hover { transform:translateY(-4px) !important; box-shadow:var(--sh2) !important; }
div[data-testid="stMetric"] label { color:var(--text3) !important; font-size:.7rem !important; font-weight:700 !important; text-transform:uppercase !important; letter-spacing:.08em !important; }
div[data-testid="stMetric"] [data-testid="stMetricValue"] { color:var(--text) !important; font-family:'Space Grotesk',sans-serif !important; }
div[data-testid="stExpander"] { background:var(--surf) !important; border:1px solid var(--border) !important; border-radius:var(--r) !important; box-shadow:var(--sh) !important; }
div[data-testid="stExpander"]:hover { border-color:var(--a2) !important; }
div[data-testid="stExpander"] summary { color:var(--text2) !important; font-weight:700 !important; }
div[data-testid="stNumberInput"] label,div[data-testid="stSelectbox"] label,
div[data-testid="stTextInput"] label,div[data-testid="stRadio"] label { color:var(--text2) !important; font-weight:700 !important; font-size:.83rem !important; }
div[data-testid="stNumberInput"] input,div[data-testid="stTextInput"] input { background:var(--surf) !important; color:var(--text) !important; border-color:var(--border) !important; font-size:.9rem !important; border-radius:8px !important; }
div[data-testid="stNumberInput"] input:focus,div[data-testid="stTextInput"] input:focus { border-color:var(--a2) !important; box-shadow:0 0 0 3px rgba(52,100,200,.14) !important; }
div[data-baseweb="select"] { background:var(--surf) !important; }
div[data-baseweb="select"] * { color:var(--text) !important; }
hr { border-color:var(--border) !important; margin:1.2rem 0 !important; }
div[data-testid="stDataFrame"] { border-radius:12px; overflow:hidden; box-shadow:var(--sh); }
table { border-collapse:collapse; width:100%; font-size:.84rem; }
th { background:#eef2fc; color:var(--text); padding:.55rem .9rem; border:1px solid var(--border); font-weight:700; text-align:left; }
td { padding:.5rem .9rem; border:1px solid var(--border); color:var(--text2); }
tr:nth-child(even) td { background:#f8faff; }
tr:hover td { background:#eef2fc !important; }

.d1{animation-delay:.05s!important} .d2{animation-delay:.10s!important}
.d3{animation-delay:.15s!important} .d4{animation-delay:.20s!important}
.d5{animation-delay:.25s!important} .d6{animation-delay:.30s!important}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# SESSION STATE
# ══════════════════════════════════════════════════════════
DEFAULTS = {'page':'home','step':1,'data':{},'result':None,'_cid':0}
for k,v in DEFAULTS.items():
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

SUBTES = ["PU","PPU","PBM","PK","LBI","LBE","PM"]
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
    "PU":"#c8890a","PPU":"#3b6cb7","PBM":"#7048c8",
    "PK":"#c0392b","LBI":"#1a8a4a","LBE":"#0d8a80","PM":"#d4620a",
}

DAFTAR_JENJANG = ["S1 (Sarjana)", "D4 (Sarjana Terapan)", "D3 (Diploma Tiga)"]

# ══════════════════════════════════════════════════════════
# LOAD DATA DARI XLSX
# ══════════════════════════════════════════════════════════
URL_S1  = "https://raw.githubusercontent.com/Skoriaid/skoria-data/main/UTBK_SNBT_Estimasi_30PTN.xlsx"
URL_D34 = "https://raw.githubusercontent.com/Skoriaid/skoria-data/main/UTBK_SNBT_D3_D4_SaintekSoshum_30PTN.xlsx"
LOCAL_S1  = "UTBK_SNBT_Estimasi_30PTN.xlsx"
LOCAL_D34 = "UTBK_SNBT_D3_D4_SaintekSoshum_30PTN.xlsx"

def parse_rentang(r):
    for sep in ['–', '-']:
        try:
            parts = str(r).split(sep)
            if len(parts) == 2:
                mn = int(parts[0].strip())
                mx = int(parts[1].strip())
                return mn, mx
        except:
            pass
    return None, None

# ── FILTER: hanya PTN (Perguruan Tinggi Negeri) ──
_PTN_KEYWORDS_POSITIF = [
    "negeri", "institut teknologi", "institut pertanian",
    "universitas indonesia", "universitas gadjah mada",
    "universitas airlangga", "universitas padjadjaran",
    "universitas diponegoro", "universitas brawijaya",
    "universitas sebelas maret", "universitas hasanuddin",
    "universitas sumatera utara", "universitas andalas",
    "universitas sriwijaya", "universitas udayana",
    "universitas riau", "universitas jember",
    "universitas mulawarman", "universitas syiah kuala",
    "universitas sam ratulangi", "universitas lampung",
    "politeknik negeri", "politeknik elektronika negeri",
    "politeknik perkapalan negeri", "politeknik manufaktur negeri",
]
_PTS_KEYWORDS_NEGATIF = [
    "swasta", "amikom", "bina nusantara", "mercu buana",
    "trisakti", "pelita harapan", "atma jaya", "unika",
    "unpas", "untar", "unisba", "ums ", "umy ", "unissula",
    "uib ", "uii ", "umm ", "umsu", "prasetiya mulya",
    "ciputra", "widyatama", "stmik", "stikes", "sekolah tinggi",
    "akademi ", "itb-stei",
]

def is_ptn(nama: str) -> bool:
    """Kembalikan True jika nama kampus terindikasi PTN (bukan PTS)."""
    n = nama.lower().strip()
    # Jika ada kata kunci PTS → langsung tolak
    for kw in _PTS_KEYWORDS_NEGATIF:
        if kw in n:
            return False
    # Jika ada kata kunci PTN → terima
    for kw in _PTN_KEYWORDS_POSITIF:
        if kw in n:
            return True
    # Default: tolak jika tidak cocok keyword PTN
    return False

# ══════════════════════════════════════════════════════════
# DATABASE PRODI D3 DAN D4 AKURAT PER KAMPUS
# Sumber: website resmi masing-masing PTN & SNPMB 2022-2024
# ══════════════════════════════════════════════════════════

PTN_PRODI_D3 = {
    # ── POLITEKNIK ──
    "Politeknik Negeri Bandung": {
        "D3 Teknik Sipil": {"mn": 530, "mx": 600},
        "D3 Teknik Geodesi": {"mn": 520, "mx": 590},
        "D3 Teknik Mesin": {"mn": 520, "mx": 590},
        "D3 Teknik Refrigerasi dan Tata Udara": {"mn": 510, "mx": 580},
        "D3 Teknik Otomotif": {"mn": 510, "mx": 580},
        "D3 Teknik Elektronika": {"mn": 530, "mx": 600},
        "D3 Teknik Elektro": {"mn": 535, "mx": 605},
        "D3 Teknik Informatika": {"mn": 560, "mx": 630},
        "D3 Teknik Kimia": {"mn": 510, "mx": 580},
        "D3 Analisis Kimia": {"mn": 510, "mx": 580},
        "D3 Teknik Lingkungan": {"mn": 500, "mx": 570},
        "D3 Akuntansi": {"mn": 520, "mx": 590},
        "D3 Keuangan dan Perbankan": {"mn": 510, "mx": 580},
        "D3 Manajemen Pemasaran": {"mn": 500, "mx": 570},
        "D3 Administrasi Bisnis": {"mn": 500, "mx": 570},
        "D3 Manajemen Informatika": {"mn": 530, "mx": 600},
        "D3 Komputerisasi Akuntansi": {"mn": 520, "mx": 590},
        "D3 Usaha Perjalanan Wisata": {"mn": 490, "mx": 560},
        "D3 Manajemen Aset": {"mn": 490, "mx": 560},
    },
    "Politeknik Negeri Jakarta": {
        "D3 Teknik Sipil": {"mn": 520, "mx": 590},
        "D3 Teknik Mesin": {"mn": 515, "mx": 585},
        "D3 Teknik Elektro": {"mn": 530, "mx": 600},
        "D3 Teknik Elektronika": {"mn": 525, "mx": 595},
        "D3 Teknik Informatika": {"mn": 550, "mx": 620},
        "D3 Teknik Kimia": {"mn": 505, "mx": 575},
        "D3 Akuntansi": {"mn": 515, "mx": 585},
        "D3 Keuangan dan Perbankan": {"mn": 505, "mx": 575},
        "D3 Manajemen Pemasaran": {"mn": 495, "mx": 565},
        "D3 Administrasi Bisnis": {"mn": 495, "mx": 565},
        "D3 Manajemen Informatika": {"mn": 525, "mx": 595},
        "D3 Komputerisasi Akuntansi": {"mn": 515, "mx": 585},
        "D3 Perbankan Syariah": {"mn": 495, "mx": 565},
        "D3 Teknik Grafika dan Penerbitan": {"mn": 490, "mx": 560},
    },
    "Politeknik Negeri Semarang": {
        "D3 Teknik Sipil": {"mn": 510, "mx": 580},
        "D3 Teknik Mesin": {"mn": 505, "mx": 575},
        "D3 Teknik Elektro": {"mn": 520, "mx": 590},
        "D3 Teknik Elektronika": {"mn": 515, "mx": 585},
        "D3 Teknik Informatika": {"mn": 540, "mx": 610},
        "D3 Teknik Kimia": {"mn": 500, "mx": 570},
        "D3 Teknik Telekomunikasi": {"mn": 515, "mx": 585},
        "D3 Akuntansi": {"mn": 510, "mx": 580},
        "D3 Keuangan dan Perbankan": {"mn": 500, "mx": 570},
        "D3 Manajemen Pemasaran": {"mn": 490, "mx": 560},
        "D3 Administrasi Bisnis": {"mn": 490, "mx": 560},
        "D3 Manajemen Informatika": {"mn": 520, "mx": 590},
        "D3 Komputerisasi Akuntansi": {"mn": 510, "mx": 580},
        "D3 Teknik Konstruksi Gedung": {"mn": 495, "mx": 565},
    },
    "Politeknik Negeri Malang": {
        "D3 Teknik Sipil": {"mn": 505, "mx": 575},
        "D3 Teknik Mesin": {"mn": 500, "mx": 570},
        "D3 Teknik Elektro": {"mn": 515, "mx": 585},
        "D3 Teknik Elektronika": {"mn": 510, "mx": 580},
        "D3 Teknik Informatika": {"mn": 535, "mx": 605},
        "D3 Teknik Kimia": {"mn": 495, "mx": 565},
        "D3 Teknik Listrik": {"mn": 500, "mx": 570},
        "D3 Akuntansi": {"mn": 505, "mx": 575},
        "D3 Keuangan dan Perbankan": {"mn": 495, "mx": 565},
        "D3 Manajemen Pemasaran": {"mn": 485, "mx": 555},
        "D3 Administrasi Bisnis": {"mn": 485, "mx": 555},
        "D3 Manajemen Informatika": {"mn": 515, "mx": 585},
        "D3 Komputerisasi Akuntansi": {"mn": 505, "mx": 575},
        "D3 Teknik Otomotif Elektronik": {"mn": 495, "mx": 565},
    },
    "Politeknik Negeri Medan": {
        "D3 Teknik Sipil": {"mn": 490, "mx": 560},
        "D3 Teknik Mesin": {"mn": 485, "mx": 555},
        "D3 Teknik Elektro": {"mn": 500, "mx": 570},
        "D3 Teknik Elektronika": {"mn": 495, "mx": 565},
        "D3 Teknik Informatika": {"mn": 515, "mx": 585},
        "D3 Teknik Kimia": {"mn": 480, "mx": 550},
        "D3 Akuntansi": {"mn": 490, "mx": 560},
        "D3 Keuangan dan Perbankan": {"mn": 480, "mx": 550},
        "D3 Manajemen Pemasaran": {"mn": 470, "mx": 540},
        "D3 Administrasi Bisnis": {"mn": 470, "mx": 540},
        "D3 Manajemen Informatika": {"mn": 500, "mx": 570},
        "D3 Komputerisasi Akuntansi": {"mn": 490, "mx": 560},
        "D3 Teknik Konstruksi Gedung": {"mn": 475, "mx": 545},
    },
    "Politeknik Negeri Ujung Pandang": {
        "D3 Teknik Sipil": {"mn": 490, "mx": 560},
        "D3 Teknik Mesin": {"mn": 485, "mx": 555},
        "D3 Teknik Elektro": {"mn": 500, "mx": 570},
        "D3 Teknik Elektronika": {"mn": 495, "mx": 565},
        "D3 Teknik Informatika": {"mn": 515, "mx": 585},
        "D3 Teknik Kimia": {"mn": 480, "mx": 550},
        "D3 Teknik Refrigerasi dan Tata Udara": {"mn": 480, "mx": 550},
        "D3 Akuntansi": {"mn": 490, "mx": 560},
        "D3 Administrasi Bisnis": {"mn": 470, "mx": 540},
        "D3 Manajemen Informatika": {"mn": 500, "mx": 570},
        "D3 Pariwisata": {"mn": 460, "mx": 530},
        "D3 Teknik Konstruksi Gedung": {"mn": 475, "mx": 545},
        "D3 Teknik Pertambangan": {"mn": 470, "mx": 540},
    },
    "Politeknik Negeri Bali": {
        "D3 Teknik Sipil": {"mn": 490, "mx": 560},
        "D3 Teknik Mesin": {"mn": 485, "mx": 555},
        "D3 Teknik Elektro": {"mn": 495, "mx": 565},
        "D3 Teknik Elektronika": {"mn": 490, "mx": 560},
        "D3 Teknik Informatika": {"mn": 510, "mx": 580},
        "D3 Akuntansi": {"mn": 490, "mx": 560},
        "D3 Keuangan dan Perbankan": {"mn": 480, "mx": 550},
        "D3 Administrasi Bisnis": {"mn": 470, "mx": 540},
        "D3 Manajemen Informatika": {"mn": 500, "mx": 570},
        "D3 Pariwisata": {"mn": 490, "mx": 560},
        "D3 Usaha Perjalanan Wisata": {"mn": 480, "mx": 550},
        "D3 Perhotelan": {"mn": 475, "mx": 545},
        "D3 Manajemen Proyek": {"mn": 470, "mx": 540},
    },
    "Politeknik Elektronika Negeri Surabaya": {
        "D3 Teknik Elektronika": {"mn": 545, "mx": 615},
        "D3 Teknik Informatika": {"mn": 555, "mx": 625},
        "D3 Teknik Telekomunikasi": {"mn": 535, "mx": 605},
        "D3 Teknik Komputer": {"mn": 540, "mx": 610},
        "D3 Teknik Listrik": {"mn": 520, "mx": 590},
        "D3 Sistem Kelistrikan": {"mn": 515, "mx": 585},
        "D3 Manajemen Informatika": {"mn": 530, "mx": 600},
        "D3 Teknik Mekatronika": {"mn": 535, "mx": 605},
    },
    "Politeknik Manufaktur Negeri Bandung": {
        "D3 Teknik Mesin": {"mn": 530, "mx": 600},
        "D3 Teknik Manufaktur": {"mn": 525, "mx": 595},
        "D3 Teknik Otomasi Industri": {"mn": 530, "mx": 600},
        "D3 Teknik Perancangan dan Konstruksi Mesin": {"mn": 520, "mx": 590},
        "D3 Teknik Pemeliharaan Mesin": {"mn": 515, "mx": 585},
        "D3 Teknik Pengecoran Logam": {"mn": 505, "mx": 575},
    },
    "Politeknik Perkapalan Negeri Surabaya": {
        "D3 Teknik Perkapalan": {"mn": 530, "mx": 600},
        "D3 Teknik Permesinan Kapal": {"mn": 520, "mx": 590},
        "D3 Teknik Kelistrikan Kapal": {"mn": 515, "mx": 585},
        "D3 Teknik Bangunan Kapal": {"mn": 525, "mx": 595},
        "D3 Teknik Desain dan Manufaktur": {"mn": 515, "mx": 585},
        "D3 Teknik Keselamatan dan Kesehatan Kerja": {"mn": 510, "mx": 580},
    },

    # ── UNIVERSITAS (D3 yang benar-benar ada) ──
    "Universitas Indonesia": {
        "D3 Fisioterapi": {"mn": 560, "mx": 630},
        "D3 Okupasi Terapi": {"mn": 540, "mx": 610},
        "D3 Administrasi Perkantoran": {"mn": 510, "mx": 580},
        "D3 Akuntansi": {"mn": 540, "mx": 610},
        "D3 Perpajakan": {"mn": 530, "mx": 600},
        "D3 Manajemen Informasi": {"mn": 510, "mx": 580},
        "D3 Hubungan Masyarakat": {"mn": 510, "mx": 580},
        "D3 Rekam Medis dan Informasi Kesehatan": {"mn": 530, "mx": 600},
        "D3 Teknik Komputer": {"mn": 560, "mx": 630},
        "D3 Kebidanan": {"mn": 530, "mx": 600},
    },
    "Institut Teknologi Bandung": {
        "D3 Teknik Sipil": {"mn": 590, "mx": 660},
        "D3 Teknik Mesin": {"mn": 585, "mx": 655},
        "D3 Teknik Elektro": {"mn": 595, "mx": 665},
        "D3 Teknik Kimia": {"mn": 575, "mx": 645},
        "D3 Teknik Informatika": {"mn": 615, "mx": 685},
        "D3 Manajemen Informatika": {"mn": 580, "mx": 650},
        "D3 Analisis Kimia": {"mn": 560, "mx": 630},
        "D3 Teknik Geodesi": {"mn": 565, "mx": 635},
        "D3 Teknik Lingkungan": {"mn": 555, "mx": 625},
        "D3 Manajemen Pemasaran": {"mn": 545, "mx": 615},
        "D3 Akuntansi": {"mn": 555, "mx": 625},
    },
    "Institut Teknologi Sepuluh Nopember": {
        "D3 Teknik Sipil": {"mn": 560, "mx": 630},
        "D3 Teknik Mesin": {"mn": 555, "mx": 625},
        "D3 Teknik Elektro": {"mn": 570, "mx": 640},
        "D3 Teknik Kimia": {"mn": 545, "mx": 615},
        "D3 Teknik Informatika": {"mn": 590, "mx": 660},
        "D3 Teknik Perkapalan": {"mn": 545, "mx": 615},
        "D3 Teknik Permesinan Kapal": {"mn": 535, "mx": 605},
        "D3 Instrumentasi": {"mn": 540, "mx": 610},
        "D3 Statistika Bisnis": {"mn": 545, "mx": 615},
        "D3 Manajemen Bisnis": {"mn": 545, "mx": 615},
    },
    "Institut Pertanian Bogor": {
        "D3 Analisis Kimia": {"mn": 530, "mx": 600},
        "D3 Teknologi Pangan": {"mn": 540, "mx": 610},
        "D3 Ekowisata": {"mn": 490, "mx": 560},
        "D3 Manajemen Informatika": {"mn": 515, "mx": 585},
        "D3 Akuntansi": {"mn": 510, "mx": 580},
        "D3 Teknik Komputer": {"mn": 525, "mx": 595},
        "D3 Komunikasi": {"mn": 495, "mx": 565},
        "D3 Pengelolaan Perkebunan": {"mn": 465, "mx": 535},
        "D3 Manajemen Agribisnis": {"mn": 475, "mx": 545},
        "D3 Supervisor Jaminan Mutu Pangan": {"mn": 480, "mx": 550},
        "D3 Manajemen Sumber Daya Lahan": {"mn": 460, "mx": 530},
        "D3 Teknik dan Manajemen Lingkungan": {"mn": 470, "mx": 540},
    },
    "Universitas Gadjah Mada": {
        "D3 Bahasa Inggris": {"mn": 530, "mx": 600},
        "D3 Bahasa Jepang": {"mn": 510, "mx": 580},
        "D3 Bahasa Prancis": {"mn": 500, "mx": 570},
        "D3 Bahasa Korea": {"mn": 505, "mx": 575},
        "D3 Akuntansi": {"mn": 550, "mx": 620},
        "D3 Manajemen": {"mn": 545, "mx": 615},
        "D3 Perpajakan": {"mn": 530, "mx": 600},
        "D3 Keuangan dan Perbankan": {"mn": 520, "mx": 590},
        "D3 Ekonomika Terapan": {"mn": 520, "mx": 590},
        "D3 Rekam Medis": {"mn": 530, "mx": 600},
        "D3 Kesehatan Hewan": {"mn": 490, "mx": 560},
        "D3 Komputer dan Sistem Informasi": {"mn": 545, "mx": 615},
        "D3 Elektronika dan Instrumentasi": {"mn": 530, "mx": 600},
        "D3 Teknik Elektro": {"mn": 530, "mx": 600},
        "D3 Teknik Mesin": {"mn": 520, "mx": 590},
        "D3 Teknik Sipil": {"mn": 525, "mx": 595},
        "D3 Teknik Kimia": {"mn": 510, "mx": 580},
        "D3 Teknik Geomatika": {"mn": 510, "mx": 580},
        "D3 Pariwisata": {"mn": 510, "mx": 580},
        "D3 Manajemen dan Penilaian Properti": {"mn": 505, "mx": 575},
    },
    "Universitas Airlangga": {
        "D3 Analis Kesehatan / TLM": {"mn": 540, "mx": 610},
        "D3 Rekam Medis dan Informasi Kesehatan": {"mn": 520, "mx": 590},
        "D3 Fisioterapi": {"mn": 530, "mx": 600},
        "D3 Radiologi": {"mn": 525, "mx": 595},
        "D3 Gizi": {"mn": 520, "mx": 590},
        "D3 Keperawatan": {"mn": 515, "mx": 585},
        "D3 Kebidanan": {"mn": 510, "mx": 580},
        "D3 Farmasi": {"mn": 540, "mx": 610},
        "D3 Akuntansi": {"mn": 520, "mx": 590},
        "D3 Perpajakan": {"mn": 510, "mx": 580},
        "D3 Manajemen Pemasaran": {"mn": 500, "mx": 570},
        "D3 Keuangan dan Perbankan": {"mn": 505, "mx": 575},
        "D3 Administrasi Bisnis": {"mn": 495, "mx": 565},
        "D3 Bahasa Inggris": {"mn": 500, "mx": 570},
        "D3 Bahasa Jepang": {"mn": 480, "mx": 550},
        "D3 Teknik Informatika": {"mn": 530, "mx": 600},
        "D3 Manajemen Informasi Kesehatan": {"mn": 515, "mx": 585},
        "D3 Hubungan Masyarakat": {"mn": 490, "mx": 560},
    },
    "Universitas Padjadjaran": {
        "D3 Analis Kesehatan / TLM": {"mn": 530, "mx": 600},
        "D3 Rekam Medis dan Informasi Kesehatan": {"mn": 510, "mx": 580},
        "D3 Fisioterapi": {"mn": 520, "mx": 590},
        "D3 Radiologi": {"mn": 515, "mx": 585},
        "D3 Gizi": {"mn": 510, "mx": 580},
        "D3 Keperawatan": {"mn": 505, "mx": 575},
        "D3 Kebidanan": {"mn": 500, "mx": 570},
        "D3 Farmasi": {"mn": 525, "mx": 595},
        "D3 Akuntansi": {"mn": 515, "mx": 585},
        "D3 Perpajakan": {"mn": 505, "mx": 575},
        "D3 Manajemen Pemasaran": {"mn": 495, "mx": 565},
        "D3 Keuangan dan Perbankan": {"mn": 495, "mx": 565},
        "D3 Administrasi Bisnis": {"mn": 485, "mx": 555},
        "D3 Bahasa Inggris": {"mn": 490, "mx": 560},
        "D3 Bahasa Jepang": {"mn": 470, "mx": 540},
        "D3 Hubungan Masyarakat": {"mn": 485, "mx": 555},
        "D3 Kehumasan": {"mn": 480, "mx": 550},
    },
    "Universitas Diponegoro": {
        "D3 Analis Kesehatan / TLM": {"mn": 510, "mx": 580},
        "D3 Rekam Medis dan Informasi Kesehatan": {"mn": 490, "mx": 560},
        "D3 Gizi": {"mn": 495, "mx": 565},
        "D3 Keperawatan": {"mn": 485, "mx": 555},
        "D3 Farmasi": {"mn": 505, "mx": 575},
        "D3 Akuntansi": {"mn": 500, "mx": 570},
        "D3 Perpajakan": {"mn": 490, "mx": 560},
        "D3 Manajemen Pemasaran": {"mn": 475, "mx": 545},
        "D3 Keuangan dan Perbankan": {"mn": 480, "mx": 550},
        "D3 Administrasi Bisnis": {"mn": 470, "mx": 540},
        "D3 Bahasa Inggris": {"mn": 475, "mx": 545},
        "D3 Hubungan Masyarakat": {"mn": 470, "mx": 540},
        "D3 Teknik Informatika": {"mn": 510, "mx": 580},
        "D3 Teknik Sipil": {"mn": 490, "mx": 560},
        "D3 Teknik Elektro": {"mn": 490, "mx": 560},
        "D3 Teknik Kimia": {"mn": 480, "mx": 550},
        "D3 Teknik Geomatika": {"mn": 475, "mx": 545},
    },
    "Universitas Brawijaya": {
        "D3 Analis Kesehatan / TLM": {"mn": 500, "mx": 570},
        "D3 Keperawatan": {"mn": 475, "mx": 545},
        "D3 Kebidanan": {"mn": 470, "mx": 540},
        "D3 Gizi": {"mn": 480, "mx": 550},
        "D3 Farmasi": {"mn": 490, "mx": 560},
        "D3 Akuntansi": {"mn": 490, "mx": 560},
        "D3 Perpajakan": {"mn": 480, "mx": 550},
        "D3 Manajemen Pemasaran": {"mn": 465, "mx": 535},
        "D3 Keuangan dan Perbankan": {"mn": 470, "mx": 540},
        "D3 Administrasi Bisnis": {"mn": 460, "mx": 530},
        "D3 Bahasa Inggris": {"mn": 465, "mx": 535},
        "D3 Teknik Informatika": {"mn": 495, "mx": 565},
        "D3 Manajemen Informatika": {"mn": 480, "mx": 550},
        "D3 Teknik Sipil": {"mn": 470, "mx": 540},
        "D3 Teknik Pengairan": {"mn": 455, "mx": 525},
        "D3 Statistika": {"mn": 470, "mx": 540},
    },
    "Universitas Sebelas Maret": {
        "D3 Rekam Medis": {"mn": 490, "mx": 560},
        "D3 Analis Kesehatan / TLM": {"mn": 495, "mx": 565},
        "D3 Keperawatan": {"mn": 470, "mx": 540},
        "D3 Kebidanan": {"mn": 465, "mx": 535},
        "D3 Farmasi": {"mn": 480, "mx": 550},
        "D3 Akuntansi": {"mn": 480, "mx": 550},
        "D3 Perpajakan": {"mn": 470, "mx": 540},
        "D3 Keuangan dan Perbankan": {"mn": 460, "mx": 530},
        "D3 Manajemen Pemasaran": {"mn": 450, "mx": 520},
        "D3 Manajemen Administrasi": {"mn": 450, "mx": 520},
        "D3 Usaha Perjalanan Wisata": {"mn": 445, "mx": 515},
        "D3 Komunikasi Terapan": {"mn": 450, "mx": 520},
        "D3 Bahasa Inggris": {"mn": 455, "mx": 525},
        "D3 Bahasa Mandarin": {"mn": 445, "mx": 515},
        "D3 Bahasa Jepang": {"mn": 440, "mx": 510},
        "D3 Teknik Informatika": {"mn": 480, "mx": 550},
        "D3 Teknik Sipil": {"mn": 455, "mx": 525},
        "D3 Teknik Kimia": {"mn": 445, "mx": 515},
        "D3 Teknik Mesin": {"mn": 445, "mx": 515},
        "D3 Statistika": {"mn": 455, "mx": 525},
        "D3 Desain Komunikasi Visual": {"mn": 430, "mx": 500},
    },
    "Universitas Hasanuddin": {
        "D3 Rekam Medis": {"mn": 480, "mx": 550},
        "D3 Analis Kesehatan / TLM": {"mn": 480, "mx": 550},
        "D3 Keperawatan": {"mn": 455, "mx": 525},
        "D3 Kebidanan": {"mn": 450, "mx": 520},
        "D3 Farmasi": {"mn": 465, "mx": 535},
        "D3 Akuntansi": {"mn": 465, "mx": 535},
        "D3 Perpajakan": {"mn": 455, "mx": 525},
        "D3 Manajemen Pemasaran": {"mn": 445, "mx": 515},
        "D3 Administrasi Bisnis": {"mn": 440, "mx": 510},
        "D3 Teknik Informatika": {"mn": 470, "mx": 540},
        "D3 Manajemen Informatika": {"mn": 455, "mx": 525},
        "D3 Teknik Sipil": {"mn": 450, "mx": 520},
        "D3 Teknik Elektro": {"mn": 455, "mx": 525},
        "D3 Teknik Mesin": {"mn": 445, "mx": 515},
        "D3 Statistika": {"mn": 450, "mx": 520},
    },
    "Universitas Sumatera Utara": {
        "D3 Rekam Medis": {"mn": 460, "mx": 530},
        "D3 Analis Kesehatan / TLM": {"mn": 465, "mx": 535},
        "D3 Keperawatan": {"mn": 440, "mx": 510},
        "D3 Kebidanan": {"mn": 435, "mx": 505},
        "D3 Farmasi": {"mn": 450, "mx": 520},
        "D3 Fisioterapi": {"mn": 445, "mx": 515},
        "D3 Akuntansi": {"mn": 450, "mx": 520},
        "D3 Perpajakan": {"mn": 440, "mx": 510},
        "D3 Keuangan dan Perbankan": {"mn": 435, "mx": 505},
        "D3 Manajemen Pemasaran": {"mn": 425, "mx": 495},
        "D3 Administrasi Bisnis": {"mn": 420, "mx": 490},
        "D3 Bahasa Inggris": {"mn": 435, "mx": 505},
        "D3 Bahasa Jepang": {"mn": 420, "mx": 490},
        "D3 Bahasa Mandarin": {"mn": 415, "mx": 485},
        "D3 Teknik Informatika": {"mn": 460, "mx": 530},
        "D3 Manajemen Informatika": {"mn": 445, "mx": 515},
        "D3 Teknik Sipil": {"mn": 435, "mx": 505},
        "D3 Teknik Elektro": {"mn": 435, "mx": 505},
        "D3 Teknik Kimia": {"mn": 425, "mx": 495},
        "D3 Statistika": {"mn": 435, "mx": 505},
    },
    "Universitas Andalas": {
        "D3 Rekam Medis": {"mn": 450, "mx": 520},
        "D3 Analis Kesehatan / TLM": {"mn": 455, "mx": 525},
        "D3 Keperawatan": {"mn": 430, "mx": 500},
        "D3 Kebidanan": {"mn": 425, "mx": 495},
        "D3 Farmasi": {"mn": 445, "mx": 515},
        "D3 Akuntansi": {"mn": 445, "mx": 515},
        "D3 Perpajakan": {"mn": 435, "mx": 505},
        "D3 Keuangan dan Perbankan": {"mn": 430, "mx": 500},
        "D3 Manajemen Pemasaran": {"mn": 420, "mx": 490},
        "D3 Teknik Informatika": {"mn": 455, "mx": 525},
        "D3 Teknik Sipil": {"mn": 430, "mx": 500},
        "D3 Teknik Elektro": {"mn": 430, "mx": 500},
        "D3 Teknik Mesin": {"mn": 420, "mx": 490},
    },
    "Universitas Sriwijaya": {
        "D3 Keperawatan": {"mn": 415, "mx": 485},
        "D3 Kebidanan": {"mn": 410, "mx": 480},
        "D3 Akuntansi": {"mn": 430, "mx": 500},
        "D3 Perpajakan": {"mn": 420, "mx": 490},
        "D3 Keuangan dan Perbankan": {"mn": 415, "mx": 485},
        "D3 Manajemen Pemasaran": {"mn": 405, "mx": 475},
        "D3 Administrasi Bisnis": {"mn": 400, "mx": 470},
        "D3 Teknik Informatika": {"mn": 440, "mx": 510},
        "D3 Teknik Sipil": {"mn": 415, "mx": 485},
        "D3 Teknik Elektro": {"mn": 415, "mx": 485},
        "D3 Teknik Mesin": {"mn": 405, "mx": 475},
        "D3 Teknik Kimia": {"mn": 405, "mx": 475},
    },
    "Universitas Udayana": {
        "D3 Rekam Medis": {"mn": 450, "mx": 520},
        "D3 Analis Kesehatan / TLM": {"mn": 455, "mx": 525},
        "D3 Keperawatan": {"mn": 430, "mx": 500},
        "D3 Kebidanan": {"mn": 425, "mx": 495},
        "D3 Farmasi": {"mn": 445, "mx": 515},
        "D3 Fisioterapi": {"mn": 440, "mx": 510},
        "D3 Akuntansi": {"mn": 445, "mx": 515},
        "D3 Perpajakan": {"mn": 435, "mx": 505},
        "D3 Keuangan dan Perbankan": {"mn": 430, "mx": 500},
        "D3 Manajemen Pemasaran": {"mn": 420, "mx": 490},
        "D3 Administrasi Bisnis": {"mn": 415, "mx": 485},
        "D3 Teknik Informatika": {"mn": 455, "mx": 525},
        "D3 Teknik Sipil": {"mn": 430, "mx": 500},
        "D3 Pariwisata": {"mn": 450, "mx": 520},
        "D3 Bahasa Inggris": {"mn": 430, "mx": 500},
    },
    "Universitas Jember": {
        "D3 Rekam Medis": {"mn": 435, "mx": 505},
        "D3 Analis Kesehatan / TLM": {"mn": 440, "mx": 510},
        "D3 Keperawatan": {"mn": 415, "mx": 485},
        "D3 Kebidanan": {"mn": 410, "mx": 480},
        "D3 Farmasi": {"mn": 430, "mx": 500},
        "D3 Akuntansi": {"mn": 430, "mx": 500},
        "D3 Perpajakan": {"mn": 420, "mx": 490},
        "D3 Manajemen Pemasaran": {"mn": 405, "mx": 475},
        "D3 Manajemen Agribisnis": {"mn": 400, "mx": 470},
        "D3 Teknik Informatika": {"mn": 440, "mx": 510},
        "D3 Manajemen Perusahaan": {"mn": 405, "mx": 475},
        "D3 Usaha Perjalanan Wisata": {"mn": 400, "mx": 470},
    },
    "Universitas Lampung": {
        "D3 Keperawatan": {"mn": 405, "mx": 475},
        "D3 Kebidanan": {"mn": 400, "mx": 470},
        "D3 Akuntansi": {"mn": 415, "mx": 485},
        "D3 Perpajakan": {"mn": 405, "mx": 475},
        "D3 Manajemen Pemasaran": {"mn": 415, "mx": 485},
        "D3 Administrasi Bisnis": {"mn": 415, "mx": 485},
        "D3 Teknik Informatika": {"mn": 425, "mx": 495},
        "D3 Manajemen Informatika": {"mn": 410, "mx": 480},
        "D3 Teknik Sipil": {"mn": 400, "mx": 470},
        "D3 Teknik Elektro": {"mn": 400, "mx": 470},
    },
    "Universitas Negeri Yogyakarta": {
        "D3 Teknik Elektro": {"mn": 450, "mx": 520},
        "D3 Teknik Mesin": {"mn": 445, "mx": 515},
        "D3 Teknik Sipil dan Perencanaan": {"mn": 445, "mx": 515},
        "D3 Teknik Elektronika": {"mn": 445, "mx": 515},
        "D3 Tata Boga": {"mn": 415, "mx": 485},
        "D3 Tata Busana": {"mn": 405, "mx": 475},
        "D3 Tata Rias dan Kecantikan": {"mn": 405, "mx": 475},
        "D3 Manajemen Pemasaran": {"mn": 420, "mx": 490},
        "D3 Akuntansi": {"mn": 430, "mx": 500},
        "D3 Teknik Informatika": {"mn": 455, "mx": 525},
    },
    "Universitas Negeri Malang": {
        "D3 Teknik Elektro": {"mn": 440, "mx": 510},
        "D3 Teknik Mesin": {"mn": 435, "mx": 505},
        "D3 Teknik Sipil": {"mn": 435, "mx": 505},
        "D3 Manajemen Pemasaran": {"mn": 410, "mx": 480},
        "D3 Akuntansi": {"mn": 420, "mx": 490},
        "D3 Teknik Informatika": {"mn": 445, "mx": 515},
        "D3 Desain Komunikasi Visual": {"mn": 405, "mx": 475},
    },
    "Universitas Negeri Semarang": {
        "D3 Teknik Elektro": {"mn": 430, "mx": 500},
        "D3 Teknik Mesin": {"mn": 425, "mx": 495},
        "D3 Teknik Sipil": {"mn": 425, "mx": 495},
        "D3 Teknik Kimia": {"mn": 415, "mx": 485},
        "D3 Manajemen Pemasaran": {"mn": 400, "mx": 470},
        "D3 Akuntansi": {"mn": 410, "mx": 480},
        "D3 Teknik Informatika": {"mn": 435, "mx": 505},
        "D3 Desain Komunikasi Visual": {"mn": 400, "mx": 470},
        "D3 Tata Boga": {"mn": 400, "mx": 470},
    },
    "Universitas Pendidikan Indonesia": {
        "D3 Teknik Elektro": {"mn": 445, "mx": 515},
        "D3 Teknik Mesin": {"mn": 435, "mx": 505},
        "D3 Teknik Sipil": {"mn": 435, "mx": 505},
        "D3 Manajemen Pemasaran": {"mn": 410, "mx": 480},
        "D3 Akuntansi": {"mn": 420, "mx": 490},
        "D3 Teknik Informatika": {"mn": 450, "mx": 520},
        "D3 Bahasa Inggris": {"mn": 430, "mx": 500},
        "D3 Desain Komunikasi Visual": {"mn": 410, "mx": 480},
        "D3 Tata Boga": {"mn": 405, "mx": 475},
        "D3 Tata Busana": {"mn": 400, "mx": 470},
    },
}

PTN_PRODI_D4 = {
    # ── POLITEKNIK ──
    "Politeknik Negeri Bandung": {
        "D4 Teknik Informatika": {"mn": 580, "mx": 650},
        "D4 Teknik Komputer": {"mn": 565, "mx": 635},
        "D4 Teknik Telekomunikasi": {"mn": 555, "mx": 625},
        "D4 Teknik Elektro": {"mn": 555, "mx": 625},
        "D4 Teknik Mesin": {"mn": 545, "mx": 615},
        "D4 Teknik Otomasi": {"mn": 555, "mx": 625},
        "D4 Teknik Sipil": {"mn": 545, "mx": 615},
        "D4 Teknik Kimia": {"mn": 535, "mx": 605},
        "D4 Teknologi Rekayasa Lingkungan": {"mn": 530, "mx": 600},
        "D4 Akuntansi Sektor Publik": {"mn": 545, "mx": 615},
        "D4 Keuangan dan Perbankan": {"mn": 535, "mx": 605},
        "D4 Manajemen Pemasaran": {"mn": 525, "mx": 595},
        "D4 Administrasi Bisnis": {"mn": 525, "mx": 595},
        "D4 Manajemen Penilaian Properti": {"mn": 520, "mx": 590},
        "D4 Manajemen Pariwisata": {"mn": 510, "mx": 580},
        "D4 Logistik": {"mn": 525, "mx": 595},
        "D4 Teknologi Rekayasa Manufaktur": {"mn": 540, "mx": 610},
        "D4 Teknik Mekatronika": {"mn": 550, "mx": 620},
        "D4 Teknik Geomatika": {"mn": 530, "mx": 600},
        "D4 Bahasa Inggris Terapan": {"mn": 510, "mx": 580},
    },
    "Politeknik Negeri Jakarta": {
        "D4 Teknik Informatika": {"mn": 560, "mx": 630},
        "D4 Teknik Komputer": {"mn": 545, "mx": 615},
        "D4 Teknik Elektro": {"mn": 545, "mx": 615},
        "D4 Teknik Mesin": {"mn": 535, "mx": 605},
        "D4 Teknik Sipil": {"mn": 535, "mx": 605},
        "D4 Teknik Kimia": {"mn": 520, "mx": 590},
        "D4 Akuntansi Sektor Publik": {"mn": 525, "mx": 595},
        "D4 Keuangan dan Perbankan": {"mn": 515, "mx": 585},
        "D4 Manajemen Pemasaran": {"mn": 505, "mx": 575},
        "D4 Administrasi Bisnis": {"mn": 505, "mx": 575},
        "D4 Teknik Mekatronika": {"mn": 530, "mx": 600},
        "D4 Teknologi Rekayasa Manufaktur": {"mn": 520, "mx": 590},
        "D4 Manajemen Logistik": {"mn": 505, "mx": 575},
        "D4 Perbankan Syariah": {"mn": 500, "mx": 570},
        "D4 Teknologi Rekayasa Konstruksi Bangunan Gedung": {"mn": 510, "mx": 580},
    },
    "Politeknik Negeri Semarang": {
        "D4 Rekayasa Perangkat Lunak": {"mn": 555, "mx": 625},
        "D4 Teknik Informatika": {"mn": 560, "mx": 630},
        "D4 Teknik Elektro": {"mn": 540, "mx": 610},
        "D4 Teknik Telekomunikasi": {"mn": 535, "mx": 605},
        "D4 Teknik Mesin": {"mn": 530, "mx": 600},
        "D4 Teknik Sipil": {"mn": 530, "mx": 600},
        "D4 Teknik Kimia": {"mn": 520, "mx": 590},
        "D4 Akuntansi Sektor Publik": {"mn": 525, "mx": 595},
        "D4 Keuangan dan Perbankan": {"mn": 515, "mx": 585},
        "D4 Manajemen Pemasaran": {"mn": 505, "mx": 575},
        "D4 Administrasi Bisnis": {"mn": 500, "mx": 570},
        "D4 Teknik Otomasi": {"mn": 530, "mx": 600},
        "D4 Teknologi Rekayasa Manufaktur": {"mn": 520, "mx": 590},
        "D4 Logistik Bisnis": {"mn": 505, "mx": 575},
    },
    "Politeknik Negeri Malang": {
        "D4 Rekayasa Perangkat Lunak": {"mn": 545, "mx": 615},
        "D4 Teknik Informatika": {"mn": 550, "mx": 620},
        "D4 Teknik Elektro": {"mn": 530, "mx": 600},
        "D4 Teknik Mesin": {"mn": 520, "mx": 590},
        "D4 Teknik Sipil": {"mn": 520, "mx": 590},
        "D4 Teknik Kimia": {"mn": 510, "mx": 580},
        "D4 Akuntansi Sektor Publik": {"mn": 515, "mx": 585},
        "D4 Keuangan dan Perbankan": {"mn": 505, "mx": 575},
        "D4 Manajemen Pemasaran": {"mn": 495, "mx": 565},
        "D4 Administrasi Bisnis": {"mn": 490, "mx": 560},
        "D4 Teknik Otomasi": {"mn": 520, "mx": 590},
        "D4 Teknologi Rekayasa Manufaktur": {"mn": 510, "mx": 580},
        "D4 Manajemen Energi": {"mn": 495, "mx": 565},
        "D4 Teknologi Rekayasa Kimia": {"mn": 505, "mx": 575},
    },
    "Politeknik Negeri Medan": {
        "D4 Rekayasa Perangkat Lunak": {"mn": 520, "mx": 590},
        "D4 Teknik Informatika": {"mn": 525, "mx": 595},
        "D4 Teknik Elektro": {"mn": 510, "mx": 580},
        "D4 Teknik Mesin": {"mn": 500, "mx": 570},
        "D4 Teknik Sipil": {"mn": 500, "mx": 570},
        "D4 Teknik Kimia": {"mn": 490, "mx": 560},
        "D4 Akuntansi Sektor Publik": {"mn": 495, "mx": 565},
        "D4 Keuangan dan Perbankan": {"mn": 485, "mx": 555},
        "D4 Manajemen Pemasaran": {"mn": 475, "mx": 545},
        "D4 Administrasi Bisnis": {"mn": 470, "mx": 540},
        "D4 Teknik Otomasi": {"mn": 500, "mx": 570},
        "D4 Teknologi Rekayasa Manufaktur": {"mn": 490, "mx": 560},
        "D4 Teknologi Rekayasa Konstruksi Gedung": {"mn": 485, "mx": 555},
    },
    "Politeknik Negeri Ujung Pandang": {
        "D4 Rekayasa Perangkat Lunak": {"mn": 515, "mx": 585},
        "D4 Teknik Informatika": {"mn": 520, "mx": 590},
        "D4 Teknik Elektro": {"mn": 505, "mx": 575},
        "D4 Teknik Mesin": {"mn": 495, "mx": 565},
        "D4 Teknik Sipil": {"mn": 495, "mx": 565},
        "D4 Teknik Kimia": {"mn": 485, "mx": 555},
        "D4 Akuntansi Sektor Publik": {"mn": 490, "mx": 560},
        "D4 Administrasi Bisnis": {"mn": 465, "mx": 535},
        "D4 Teknologi Rekayasa Manufaktur": {"mn": 485, "mx": 555},
        "D4 Manajemen Pariwisata": {"mn": 465, "mx": 535},
        "D4 Teknologi Rekayasa Pertambangan": {"mn": 470, "mx": 540},
    },
    "Politeknik Negeri Bali": {
        "D4 Rekayasa Perangkat Lunak": {"mn": 510, "mx": 580},
        "D4 Teknik Informatika": {"mn": 515, "mx": 585},
        "D4 Teknik Elektro": {"mn": 500, "mx": 570},
        "D4 Teknik Mesin": {"mn": 490, "mx": 560},
        "D4 Teknik Sipil": {"mn": 490, "mx": 560},
        "D4 Akuntansi Sektor Publik": {"mn": 485, "mx": 555},
        "D4 Administrasi Bisnis": {"mn": 460, "mx": 530},
        "D4 Manajemen Pariwisata": {"mn": 480, "mx": 550},
        "D4 Perhotelan": {"mn": 470, "mx": 540},
        "D4 Teknologi Rekayasa Manufaktur": {"mn": 480, "mx": 550},
    },
    "Politeknik Elektronika Negeri Surabaya": {
        "D4 Rekayasa Perangkat Lunak": {"mn": 580, "mx": 650},
        "D4 Teknik Informatika": {"mn": 585, "mx": 655},
        "D4 Teknik Komputer": {"mn": 570, "mx": 640},
        "D4 Teknik Telekomunikasi": {"mn": 560, "mx": 630},
        "D4 Teknik Mekatronika": {"mn": 565, "mx": 635},
        "D4 Teknologi Informasi": {"mn": 575, "mx": 645},
        "D4 Teknik Elektro Industri": {"mn": 555, "mx": 625},
        "D4 Teknologi Rekayasa Komputer": {"mn": 570, "mx": 640},
    },
    "Politeknik Manufaktur Negeri Bandung": {
        "D4 Teknologi Rekayasa Manufaktur": {"mn": 560, "mx": 630},
        "D4 Teknik Otomasi Industri": {"mn": 555, "mx": 625},
        "D4 Teknik Perancangan dan Konstruksi Mesin": {"mn": 545, "mx": 615},
        "D4 Manajemen Produksi": {"mn": 530, "mx": 600},
        "D4 Teknik Kimia Polimer": {"mn": 530, "mx": 600},
    },
    "Politeknik Perkapalan Negeri Surabaya": {
        "D4 Teknik Perkapalan": {"mn": 555, "mx": 625},
        "D4 Teknik Permesinan Kapal": {"mn": 545, "mx": 615},
        "D4 Teknik Kelistrikan Kapal": {"mn": 540, "mx": 610},
        "D4 Teknik Desain dan Manufaktur": {"mn": 540, "mx": 610},
        "D4 Teknik Keselamatan dan Kesehatan Kerja": {"mn": 530, "mx": 600},
        "D4 Teknologi Pengelasan Kapal": {"mn": 530, "mx": 600},
    },

    # ── UNIVERSITAS (D4 yang benar-benar ada) ──
    "Universitas Indonesia": {
        "D4 Teknologi Laboratorium Medis": {"mn": 580, "mx": 650},
        "D4 Fisioterapi": {"mn": 575, "mx": 645},
        "D4 Gizi Klinik": {"mn": 570, "mx": 640},
        "D4 Keperawatan": {"mn": 555, "mx": 625},
        "D4 Kebidanan": {"mn": 545, "mx": 615},
        "D4 Teknik Geomatika": {"mn": 580, "mx": 650},
        "D4 Rekayasa Perangkat Lunak": {"mn": 640, "mx": 710},
        "D4 Teknologi Informasi": {"mn": 630, "mx": 700},
        "D4 Teknik Mekatronika": {"mn": 600, "mx": 670},
        "D4 Teknik Perkapalan": {"mn": 580, "mx": 650},
        "D4 Teknologi Pangan": {"mn": 575, "mx": 645},
        "D4 Keselamatan dan Kesehatan Kerja": {"mn": 565, "mx": 635},
        "D4 Akuntansi Sektor Publik": {"mn": 580, "mx": 650},
        "D4 Administrasi Bisnis": {"mn": 570, "mx": 640},
        "D4 Manajemen Pariwisata": {"mn": 555, "mx": 625},
        "D4 Bahasa Inggris Terapan": {"mn": 545, "mx": 615},
    },
    "Institut Teknologi Bandung": {
        "D4 Rekayasa Perangkat Lunak": {"mn": 660, "mx": 730},
        "D4 Teknologi Informasi": {"mn": 650, "mx": 720},
        "D4 Teknik Mekatronika": {"mn": 635, "mx": 705},
        "D4 Teknologi Rekayasa Kimia": {"mn": 615, "mx": 685},
        "D4 Teknologi Rekayasa Lingkungan": {"mn": 605, "mx": 675},
        "D4 Teknik Geomatika": {"mn": 610, "mx": 680},
        "D4 Teknik Perkapalan": {"mn": 610, "mx": 680},
        "D4 Teknologi Rekayasa Manufaktur": {"mn": 620, "mx": 690},
        "D4 Teknik Otomasi": {"mn": 630, "mx": 700},
        "D4 Keselamatan dan Kesehatan Kerja": {"mn": 595, "mx": 665},
        "D4 Teknologi Pangan": {"mn": 600, "mx": 670},
        "D4 Gizi Klinik": {"mn": 595, "mx": 665},
        "D4 Manajemen Bisnis": {"mn": 640, "mx": 710},
        "D4 Logistik dan Supply Chain": {"mn": 610, "mx": 680},
    },
    "Institut Teknologi Sepuluh Nopember": {
        "D4 Rekayasa Perangkat Lunak": {"mn": 625, "mx": 695},
        "D4 Teknologi Informasi": {"mn": 615, "mx": 685},
        "D4 Teknik Mekatronika": {"mn": 605, "mx": 675},
        "D4 Teknologi Rekayasa Kimia": {"mn": 585, "mx": 655},
        "D4 Teknologi Rekayasa Lingkungan": {"mn": 575, "mx": 645},
        "D4 Teknik Geomatika": {"mn": 580, "mx": 650},
        "D4 Teknik Perkapalan": {"mn": 580, "mx": 650},
        "D4 Teknik Kelautan Terapan": {"mn": 570, "mx": 640},
        "D4 Teknologi Rekayasa Manufaktur": {"mn": 585, "mx": 655},
        "D4 Teknik Otomasi": {"mn": 595, "mx": 665},
        "D4 Keselamatan dan Kesehatan Kerja": {"mn": 565, "mx": 635},
        "D4 Manajemen Bisnis": {"mn": 595, "mx": 665},
        "D4 Logistik dan Supply Chain": {"mn": 575, "mx": 645},
        "D4 Statistika Bisnis": {"mn": 580, "mx": 650},
    },
    "Institut Pertanian Bogor": {
        "D4 Teknologi Pangan": {"mn": 560, "mx": 630},
        "D4 Teknologi Rekayasa Pertanian": {"mn": 540, "mx": 610},
        "D4 Manajemen Agribisnis": {"mn": 530, "mx": 600},
        "D4 Teknologi Industri Benih": {"mn": 515, "mx": 585},
        "D4 Supervisor Jaminan Mutu Pangan": {"mn": 520, "mx": 590},
        "D4 Ekowisata": {"mn": 500, "mx": 570},
        "D4 Teknik dan Manajemen Lingkungan Hidup": {"mn": 510, "mx": 580},
        "D4 Manajemen Informatika": {"mn": 530, "mx": 600},
        "D4 Akuntansi Alih Program": {"mn": 510, "mx": 580},
    },
    "Universitas Gadjah Mada": {
        "D4 Rekayasa Perangkat Lunak": {"mn": 620, "mx": 690},
        "D4 Teknologi Informasi": {"mn": 610, "mx": 680},
        "D4 Teknik Mekatronika": {"mn": 595, "mx": 665},
        "D4 Teknologi Rekayasa Kimia": {"mn": 570, "mx": 640},
        "D4 Teknologi Rekayasa Lingkungan": {"mn": 560, "mx": 630},
        "D4 Teknik Geomatika": {"mn": 565, "mx": 635},
        "D4 Teknik Pengelolaan dan Pemeliharaan Infrastruktur Sipil": {"mn": 550, "mx": 620},
        "D4 Teknologi Rekayasa Manufaktur": {"mn": 565, "mx": 635},
        "D4 Teknik Otomasi": {"mn": 575, "mx": 645},
        "D4 Keselamatan dan Kesehatan Kerja": {"mn": 545, "mx": 615},
        "D4 Gizi Klinik": {"mn": 555, "mx": 625},
        "D4 Fisioterapi": {"mn": 555, "mx": 625},
        "D4 Teknologi Laboratorium Medis": {"mn": 560, "mx": 630},
        "D4 Teknologi Pangan": {"mn": 555, "mx": 625},
        "D4 Manajemen Bisnis": {"mn": 590, "mx": 660},
        "D4 Logistik dan Supply Chain": {"mn": 560, "mx": 630},
        "D4 Manajemen Penilaian Properti": {"mn": 545, "mx": 615},
        "D4 Manajemen Pariwisata": {"mn": 545, "mx": 615},
        "D4 Bahasa Inggris Terapan": {"mn": 530, "mx": 600},
        "D4 Akuntansi Sektor Publik": {"mn": 560, "mx": 630},
    },
    "Universitas Airlangga": {
        "D4 Teknologi Laboratorium Medis": {"mn": 560, "mx": 630},
        "D4 Fisioterapi": {"mn": 555, "mx": 625},
        "D4 Gizi Klinik": {"mn": 550, "mx": 620},
        "D4 Keperawatan": {"mn": 535, "mx": 605},
        "D4 Kebidanan": {"mn": 530, "mx": 600},
        "D4 Rekam Medis dan Informasi Kesehatan": {"mn": 540, "mx": 610},
        "D4 Keselamatan dan Kesehatan Kerja": {"mn": 530, "mx": 600},
        "D4 Teknologi Pangan": {"mn": 540, "mx": 610},
        "D4 Akuntansi Sektor Publik": {"mn": 540, "mx": 610},
        "D4 Manajemen Pemasaran": {"mn": 530, "mx": 600},
        "D4 Keuangan dan Perbankan": {"mn": 530, "mx": 600},
        "D4 Administrasi Bisnis": {"mn": 520, "mx": 590},
        "D4 Manajemen Pariwisata": {"mn": 515, "mx": 585},
        "D4 Bahasa Inggris Terapan": {"mn": 510, "mx": 580},
        "D4 Rekayasa Perangkat Lunak": {"mn": 565, "mx": 635},
    },
    "Universitas Padjadjaran": {
        "D4 Teknologi Laboratorium Medis": {"mn": 545, "mx": 615},
        "D4 Fisioterapi": {"mn": 540, "mx": 610},
        "D4 Gizi Klinik": {"mn": 535, "mx": 605},
        "D4 Keperawatan": {"mn": 520, "mx": 590},
        "D4 Kebidanan": {"mn": 515, "mx": 585},
        "D4 Keselamatan dan Kesehatan Kerja": {"mn": 515, "mx": 585},
        "D4 Teknologi Pangan": {"mn": 525, "mx": 595},
        "D4 Akuntansi Sektor Publik": {"mn": 525, "mx": 595},
        "D4 Manajemen Pemasaran": {"mn": 515, "mx": 585},
        "D4 Administrasi Bisnis": {"mn": 505, "mx": 575},
        "D4 Manajemen Pariwisata": {"mn": 505, "mx": 575},
        "D4 Bahasa Inggris Terapan": {"mn": 495, "mx": 565},
        "D4 Rekayasa Perangkat Lunak": {"mn": 550, "mx": 620},
        "D4 Teknologi Informasi": {"mn": 545, "mx": 615},
    },
    "Universitas Diponegoro": {
        "D4 Teknologi Laboratorium Medis": {"mn": 520, "mx": 590},
        "D4 Fisioterapi": {"mn": 515, "mx": 585},
        "D4 Gizi Klinik": {"mn": 510, "mx": 580},
        "D4 Keperawatan": {"mn": 495, "mx": 565},
        "D4 Kebidanan": {"mn": 490, "mx": 560},
        "D4 Keselamatan dan Kesehatan Kerja": {"mn": 490, "mx": 560},
        "D4 Teknologi Pangan": {"mn": 500, "mx": 570},
        "D4 Akuntansi Sektor Publik": {"mn": 500, "mx": 570},
        "D4 Manajemen Pemasaran": {"mn": 490, "mx": 560},
        "D4 Administrasi Bisnis": {"mn": 480, "mx": 550},
        "D4 Teknik Geomatika": {"mn": 495, "mx": 565},
        "D4 Rekayasa Perangkat Lunak": {"mn": 525, "mx": 595},
        "D4 Teknologi Informasi": {"mn": 515, "mx": 585},
        "D4 Teknik Mekatronika": {"mn": 505, "mx": 575},
        "D4 Teknologi Rekayasa Kimia": {"mn": 490, "mx": 560},
    },
    "Universitas Brawijaya": {
        "D4 Teknologi Laboratorium Medis": {"mn": 505, "mx": 575},
        "D4 Gizi Klinik": {"mn": 495, "mx": 565},
        "D4 Keperawatan": {"mn": 480, "mx": 550},
        "D4 Kebidanan": {"mn": 475, "mx": 545},
        "D4 Keselamatan dan Kesehatan Kerja": {"mn": 475, "mx": 545},
        "D4 Teknologi Pangan": {"mn": 490, "mx": 560},
        "D4 Akuntansi Sektor Publik": {"mn": 490, "mx": 560},
        "D4 Manajemen Pemasaran": {"mn": 475, "mx": 545},
        "D4 Administrasi Bisnis": {"mn": 465, "mx": 535},
        "D4 Rekayasa Perangkat Lunak": {"mn": 510, "mx": 580},
        "D4 Teknologi Informasi": {"mn": 500, "mx": 570},
        "D4 Teknik Pengairan Terapan": {"mn": 465, "mx": 535},
        "D4 Manajemen Agribisnis": {"mn": 465, "mx": 535},
    },
    "Universitas Sebelas Maret": {
        "D4 Teknologi Laboratorium Medis": {"mn": 495, "mx": 565},
        "D4 Fisioterapi": {"mn": 490, "mx": 560},
        "D4 Gizi Klinik": {"mn": 485, "mx": 555},
        "D4 Keperawatan": {"mn": 470, "mx": 540},
        "D4 Kebidanan": {"mn": 465, "mx": 535},
        "D4 Keselamatan dan Kesehatan Kerja": {"mn": 465, "mx": 535},
        "D4 Teknologi Pangan": {"mn": 480, "mx": 550},
        "D4 Akuntansi Sektor Publik": {"mn": 480, "mx": 550},
        "D4 Manajemen Pemasaran": {"mn": 465, "mx": 535},
        "D4 Manajemen Pariwisata": {"mn": 455, "mx": 525},
        "D4 Usaha Perjalanan Wisata": {"mn": 450, "mx": 520},
        "D4 Bahasa Inggris Terapan": {"mn": 455, "mx": 525},
        "D4 Rekayasa Perangkat Lunak": {"mn": 495, "mx": 565},
        "D4 Teknologi Informasi": {"mn": 485, "mx": 555},
        "D4 Desain Komunikasi Visual": {"mn": 445, "mx": 515},
    },
    "Universitas Hasanuddin": {
        "D4 Teknologi Laboratorium Medis": {"mn": 485, "mx": 555},
        "D4 Fisioterapi": {"mn": 480, "mx": 550},
        "D4 Gizi Klinik": {"mn": 475, "mx": 545},
        "D4 Keperawatan": {"mn": 460, "mx": 530},
        "D4 Kebidanan": {"mn": 455, "mx": 525},
        "D4 Teknologi Pangan": {"mn": 465, "mx": 535},
        "D4 Akuntansi Sektor Publik": {"mn": 465, "mx": 535},
        "D4 Manajemen Pemasaran": {"mn": 450, "mx": 520},
        "D4 Administrasi Bisnis": {"mn": 445, "mx": 515},
        "D4 Rekayasa Perangkat Lunak": {"mn": 480, "mx": 550},
        "D4 Teknologi Informasi": {"mn": 470, "mx": 540},
        "D4 Teknik Geomatika": {"mn": 455, "mx": 525},
    },
    "Universitas Sumatera Utara": {
        "D4 Teknologi Laboratorium Medis": {"mn": 470, "mx": 540},
        "D4 Fisioterapi": {"mn": 455, "mx": 525},
        "D4 Gizi Klinik": {"mn": 460, "mx": 530},
        "D4 Keperawatan": {"mn": 445, "mx": 515},
        "D4 Kebidanan": {"mn": 440, "mx": 510},
        "D4 Teknologi Pangan": {"mn": 450, "mx": 520},
        "D4 Akuntansi Sektor Publik": {"mn": 450, "mx": 520},
        "D4 Manajemen Pemasaran": {"mn": 435, "mx": 505},
        "D4 Administrasi Bisnis": {"mn": 430, "mx": 500},
        "D4 Rekayasa Perangkat Lunak": {"mn": 465, "mx": 535},
        "D4 Teknologi Informasi": {"mn": 455, "mx": 525},
        "D4 Bahasa Inggris Terapan": {"mn": 430, "mx": 500},
    },
    "Universitas Andalas": {
        "D4 Teknologi Laboratorium Medis": {"mn": 455, "mx": 525},
        "D4 Gizi Klinik": {"mn": 450, "mx": 520},
        "D4 Keperawatan": {"mn": 435, "mx": 505},
        "D4 Kebidanan": {"mn": 430, "mx": 500},
        "D4 Teknologi Pangan": {"mn": 440, "mx": 510},
        "D4 Akuntansi Sektor Publik": {"mn": 440, "mx": 510},
        "D4 Manajemen Pemasaran": {"mn": 425, "mx": 495},
        "D4 Rekayasa Perangkat Lunak": {"mn": 455, "mx": 525},
        "D4 Teknologi Informasi": {"mn": 445, "mx": 515},
    },
    "Universitas Sriwijaya": {
        "D4 Gizi Klinik": {"mn": 430, "mx": 500},
        "D4 Keperawatan": {"mn": 415, "mx": 485},
        "D4 Kebidanan": {"mn": 410, "mx": 480},
        "D4 Teknologi Pangan": {"mn": 420, "mx": 490},
        "D4 Akuntansi Sektor Publik": {"mn": 420, "mx": 490},
        "D4 Manajemen Pemasaran": {"mn": 405, "mx": 475},
        "D4 Rekayasa Perangkat Lunak": {"mn": 435, "mx": 505},
        "D4 Teknologi Informasi": {"mn": 425, "mx": 495},
    },
    "Universitas Udayana": {
        "D4 Teknologi Laboratorium Medis": {"mn": 455, "mx": 525},
        "D4 Fisioterapi": {"mn": 450, "mx": 520},
        "D4 Gizi Klinik": {"mn": 445, "mx": 515},
        "D4 Keperawatan": {"mn": 430, "mx": 500},
        "D4 Kebidanan": {"mn": 425, "mx": 495},
        "D4 Teknologi Pangan": {"mn": 435, "mx": 505},
        "D4 Akuntansi Sektor Publik": {"mn": 440, "mx": 510},
        "D4 Manajemen Pemasaran": {"mn": 420, "mx": 490},
        "D4 Administrasi Bisnis": {"mn": 415, "mx": 485},
        "D4 Manajemen Pariwisata": {"mn": 440, "mx": 510},
        "D4 Rekayasa Perangkat Lunak": {"mn": 450, "mx": 520},
        "D4 Teknologi Informasi": {"mn": 440, "mx": 510},
    },
    "Universitas Jember": {
        "D4 Gizi Klinik": {"mn": 430, "mx": 500},
        "D4 Keperawatan": {"mn": 415, "mx": 485},
        "D4 Kebidanan": {"mn": 410, "mx": 480},
        "D4 Teknologi Pangan": {"mn": 425, "mx": 495},
        "D4 Akuntansi Sektor Publik": {"mn": 420, "mx": 490},
        "D4 Manajemen Pemasaran": {"mn": 405, "mx": 475},
        "D4 Manajemen Agribisnis": {"mn": 400, "mx": 470},
        "D4 Rekayasa Perangkat Lunak": {"mn": 435, "mx": 505},
        "D4 Teknologi Informasi": {"mn": 425, "mx": 495},
    },
    "Universitas Lampung": {
        "D4 Keperawatan": {"mn": 405, "mx": 475},
        "D4 Kebidanan": {"mn": 400, "mx": 470},
        "D4 Akuntansi Sektor Publik": {"mn": 410, "mx": 480},
        "D4 Manajemen Pemasaran": {"mn": 415, "mx": 485},
        "D4 Rekayasa Perangkat Lunak": {"mn": 420, "mx": 490},
        "D4 Teknologi Informasi": {"mn": 410, "mx": 480},
    },
    "Universitas Negeri Yogyakarta": {
        "D4 Rekayasa Perangkat Lunak": {"mn": 490, "mx": 560},
        "D4 Teknologi Informasi": {"mn": 480, "mx": 550},
        "D4 Teknik Otomasi Industri": {"mn": 470, "mx": 540},
        "D4 Manajemen Pemasaran": {"mn": 440, "mx": 510},
        "D4 Akuntansi Manajerial": {"mn": 445, "mx": 515},
        "D4 Tata Boga": {"mn": 420, "mx": 490},
        "D4 Tata Busana": {"mn": 415, "mx": 485},
    },
    "Universitas Negeri Malang": {
        "D4 Rekayasa Perangkat Lunak": {"mn": 480, "mx": 550},
        "D4 Teknologi Informasi": {"mn": 470, "mx": 540},
        "D4 Teknik Otomasi Industri": {"mn": 460, "mx": 530},
        "D4 Manajemen Pemasaran": {"mn": 430, "mx": 500},
        "D4 Akuntansi Manajerial": {"mn": 435, "mx": 505},
    },
    "Universitas Negeri Semarang": {
        "D4 Rekayasa Perangkat Lunak": {"mn": 465, "mx": 535},
        "D4 Teknologi Informasi": {"mn": 455, "mx": 525},
        "D4 Akuntansi Manajerial": {"mn": 420, "mx": 490},
        "D4 Manajemen Pemasaran": {"mn": 415, "mx": 485},
        "D4 Tata Boga": {"mn": 405, "mx": 475},
    },
    "Universitas Pendidikan Indonesia": {
        "D4 Rekayasa Perangkat Lunak": {"mn": 470, "mx": 540},
        "D4 Teknologi Informasi": {"mn": 460, "mx": 530},
        "D4 Teknik Otomasi Industri": {"mn": 455, "mx": 525},
        "D4 Akuntansi Manajerial": {"mn": 430, "mx": 500},
        "D4 Manajemen Pemasaran": {"mn": 425, "mx": 495},
        "D4 Bahasa Inggris Terapan": {"mn": 435, "mx": 505},
        "D4 Tata Boga": {"mn": 410, "mx": 480},
        "D4 Tata Busana": {"mn": 405, "mx": 475},
    },
}


# ══════════════════════════════════════════════════════════
# DATABASE PRODI S1 AKURAT PER KAMPUS
# Sumber: website resmi masing-masing PTN & SNPMB 2022-2024
# ══════════════════════════════════════════════════════════
PTN_PRODI_S1 = {
    "Universitas Indonesia": {
        # FK / FKG / FF / FIK
        "Pendidikan Dokter": {"mn": 760, "mx": 830},
        "Kedokteran Gigi": {"mn": 710, "mx": 780},
        "Farmasi": {"mn": 680, "mx": 750},
        "Ilmu Keperawatan": {"mn": 620, "mx": 690},
        "Kesehatan Masyarakat": {"mn": 620, "mx": 690},
        "Gizi": {"mn": 620, "mx": 685},
        "Ilmu Keolahragaan": {"mn": 560, "mx": 630},
        # FTUI
        "Teknik Sipil": {"mn": 660, "mx": 730},
        "Teknik Mesin": {"mn": 660, "mx": 730},
        "Teknik Elektro": {"mn": 690, "mx": 760},
        "Teknik Kimia": {"mn": 660, "mx": 730},
        "Teknik Industri": {"mn": 700, "mx": 770},
        "Teknik Lingkungan": {"mn": 640, "mx": 710},
        "Teknik Metalurgi dan Material": {"mn": 630, "mx": 700},
        "Teknik Perkapalan": {"mn": 620, "mx": 690},
        "Arsitektur": {"mn": 670, "mx": 740},
        "Teknik Komputer": {"mn": 700, "mx": 770},
        # FMIPA
        "Matematika": {"mn": 640, "mx": 710},
        "Fisika": {"mn": 630, "mx": 700},
        "Kimia": {"mn": 640, "mx": 710},
        "Biologi": {"mn": 640, "mx": 710},
        "Ilmu Komputer": {"mn": 730, "mx": 800},
        "Statistika": {"mn": 660, "mx": 730},
        "Geografi": {"mn": 620, "mx": 690},
        # FH
        "Ilmu Hukum": {"mn": 680, "mx": 750},
        # FEB
        "Ilmu Ekonomi": {"mn": 670, "mx": 740},
        "Akuntansi": {"mn": 700, "mx": 770},
        "Manajemen": {"mn": 710, "mx": 780},
        # FISIP
        "Ilmu Komunikasi": {"mn": 680, "mx": 750},
        "Hubungan Internasional": {"mn": 700, "mx": 770},
        "Sosiologi": {"mn": 640, "mx": 710},
        "Ilmu Politik": {"mn": 650, "mx": 720},
        "Ilmu Administrasi Fiskal": {"mn": 650, "mx": 720},
        "Ilmu Administrasi Niaga": {"mn": 660, "mx": 730},
        "Administrasi Negara": {"mn": 650, "mx": 720},
        "Ilmu Perpustakaan": {"mn": 590, "mx": 660},
        "Ilmu Kesejahteraan Sosial": {"mn": 620, "mx": 690},
        "Kriminologi": {"mn": 640, "mx": 710},
        # FIB
        "Sastra Indonesia": {"mn": 600, "mx": 670},
        "Sastra Inggris": {"mn": 630, "mx": 700},
        "Sastra Arab": {"mn": 590, "mx": 660},
        "Sastra Jepang": {"mn": 620, "mx": 690},
        "Sastra Belanda": {"mn": 580, "mx": 650},
        "Sastra Prancis": {"mn": 580, "mx": 650},
        "Sastra Cina": {"mn": 590, "mx": 660},
        "Filsafat": {"mn": 600, "mx": 670},
        # FPsi
        "Psikologi": {"mn": 680, "mx": 750},
        # FIA
        "Administrasi Bisnis": {"mn": 640, "mx": 710},
    },
    "Institut Teknologi Bandung": {
        # FTSL
        "Teknik Sipil": {"mn": 720, "mx": 790},
        "Teknik Lingkungan": {"mn": 700, "mx": 770},
        "Teknik Kelautan": {"mn": 680, "mx": 750},
        # FTMD
        "Teknik Mesin": {"mn": 730, "mx": 800},
        "Teknik Material": {"mn": 700, "mx": 770},
        "Teknik Dirgantara": {"mn": 710, "mx": 780},
        # FTTM
        "Teknik Pertambangan": {"mn": 690, "mx": 760},
        "Teknik Perminyakan": {"mn": 720, "mx": 790},
        "Teknik Geologi": {"mn": 700, "mx": 770},
        "Teknik Geodesi dan Geomatika": {"mn": 690, "mx": 760},
        "Meteorologi": {"mn": 680, "mx": 750},
        "Oseanografi": {"mn": 680, "mx": 750},
        # FTIF
        "Teknik Informatika": {"mn": 800, "mx": 870},
        "Sistem dan Teknologi Informasi": {"mn": 790, "mx": 860},
        # FTEIC
        "Teknik Elektro": {"mn": 760, "mx": 830},
        "Teknik Fisika": {"mn": 720, "mx": 790},
        "Teknik Tenaga Listrik": {"mn": 720, "mx": 790},
        "Teknik Telekomunikasi": {"mn": 730, "mx": 800},
        "Teknik Biomedis": {"mn": 720, "mx": 790},
        # FTI
        "Teknik Kimia": {"mn": 730, "mx": 800},
        "Teknik Industri": {"mn": 770, "mx": 840},
        "Manajemen Rekayasa": {"mn": 750, "mx": 820},
        # FMIPA
        "Matematika": {"mn": 720, "mx": 790},
        "Fisika": {"mn": 710, "mx": 780},
        "Kimia": {"mn": 720, "mx": 790},
        "Biologi": {"mn": 700, "mx": 770},
        "Astronomi": {"mn": 700, "mx": 770},
        "Aktuaria": {"mn": 750, "mx": 820},
        # SAPPK
        "Arsitektur": {"mn": 750, "mx": 820},
        "Perencanaan Wilayah dan Kota": {"mn": 730, "mx": 800},
        # FSRD
        "Desain Produk": {"mn": 720, "mx": 790},
        "Desain Komunikasi Visual": {"mn": 730, "mx": 800},
        "Seni Rupa": {"mn": 680, "mx": 750},
        "Kriya": {"mn": 670, "mx": 740},
        # SBM
        "Manajemen": {"mn": 780, "mx": 850},
        "Kewirausahaan": {"mn": 750, "mx": 820},
        # SF
        "Farmasi": {"mn": 740, "mx": 810},
        # SITH
        "Bioteknologi": {"mn": 720, "mx": 790},
        "Rekayasa Hayati": {"mn": 710, "mx": 780},
        "Rekayasa Pertanian": {"mn": 680, "mx": 750},
    },
    "Institut Teknologi Sepuluh Nopember": {
        # FTK
        "Teknik Perkapalan": {"mn": 630, "mx": 700},
        "Teknik Sistem Perkapalan": {"mn": 610, "mx": 680},
        "Teknik Kelautan": {"mn": 620, "mx": 690},
        "Transportasi Laut": {"mn": 600, "mx": 670},
        # FTI
        "Teknik Industri": {"mn": 670, "mx": 740},
        "Teknik Kimia": {"mn": 660, "mx": 730},
        "Teknik Material dan Metalurgi": {"mn": 630, "mx": 700},
        "Teknik Fisika": {"mn": 630, "mx": 700},
        "Teknik Geofisika": {"mn": 620, "mx": 690},
        # FTEIC
        "Teknik Elektro": {"mn": 700, "mx": 770},
        "Teknik Komputer": {"mn": 690, "mx": 760},
        "Teknik Informatika": {"mn": 740, "mx": 810},
        "Sistem Informasi": {"mn": 690, "mx": 760},
        "Teknologi Informasi": {"mn": 700, "mx": 770},
        # FTSP
        "Teknik Sipil": {"mn": 640, "mx": 710},
        "Teknik Lingkungan": {"mn": 620, "mx": 690},
        "Arsitektur": {"mn": 670, "mx": 740},
        "Perencanaan Wilayah dan Kota": {"mn": 650, "mx": 720},
        "Desain Produk Industri": {"mn": 650, "mx": 720},
        "Desain Interior": {"mn": 640, "mx": 710},
        # FV (Teknik Mesin ada di ITS)
        "Teknik Mesin": {"mn": 640, "mx": 710},
        # FMKSD
        "Matematika": {"mn": 660, "mx": 730},
        "Fisika": {"mn": 630, "mx": 700},
        "Kimia": {"mn": 640, "mx": 710},
        "Biologi": {"mn": 610, "mx": 680},
        "Statistika": {"mn": 660, "mx": 730},
        "Aktuaria": {"mn": 670, "mx": 740},
        # SB
        "Manajemen Bisnis": {"mn": 680, "mx": 750},
        "Studi Pembangunan": {"mn": 610, "mx": 680},
    },
    "Institut Pertanian Bogor": {
        # FAPERTA
        "Agronomi dan Hortikultura": {"mn": 600, "mx": 670},
        "Ilmu Tanah": {"mn": 580, "mx": 650},
        "Proteksi Tanaman": {"mn": 590, "mx": 660},
        "Arsitektur Lanskap": {"mn": 620, "mx": 690},
        # FMIPA
        "Matematika": {"mn": 630, "mx": 700},
        "Statistika": {"mn": 650, "mx": 720},
        "Ilmu Komputer": {"mn": 680, "mx": 750},
        "Fisika": {"mn": 600, "mx": 670},
        "Kimia": {"mn": 605, "mx": 675},
        "Biologi": {"mn": 610, "mx": 680},
        "Biokimia": {"mn": 625, "mx": 695},
        "Meteorologi Terapan": {"mn": 590, "mx": 660},
        # FKH
        "Kedokteran Hewan": {"mn": 660, "mx": 730},
        # FPIK
        "Budidaya Perairan": {"mn": 590, "mx": 660},
        "Manajemen Sumber Daya Perairan": {"mn": 580, "mx": 650},
        "Ilmu Kelautan": {"mn": 600, "mx": 670},
        "Teknologi Hasil Perairan": {"mn": 580, "mx": 650},
        # FEM
        "Ekonomi Sumber Daya dan Lingkungan": {"mn": 610, "mx": 680},
        "Agribisnis": {"mn": 635, "mx": 705},
        "Ekonomi Syariah": {"mn": 590, "mx": 660},
        "Manajemen": {"mn": 650, "mx": 720},
        # FATETA / FTK
        "Teknologi Pangan": {"mn": 645, "mx": 715},
        "Ilmu Gizi": {"mn": 645, "mx": 715},
        "Teknik Pertanian dan Biosistem": {"mn": 610, "mx": 680},
        "Teknik Kimia": {"mn": 620, "mx": 690},
        # FAHUTAN
        "Manajemen Hutan": {"mn": 590, "mx": 660},
        "Teknologi Hasil Hutan": {"mn": 580, "mx": 650},
        "Konservasi Sumber Daya Hutan dan Ekowisata": {"mn": 590, "mx": 660},
        "Silvikultur": {"mn": 580, "mx": 650},
        # FAPET
        "Ilmu Nutrisi dan Teknologi Pakan": {"mn": 580, "mx": 650},
        "Teknologi Produksi Ternak": {"mn": 580, "mx": 650},
        # FEMA
        "Ilmu Keluarga dan Konsumen": {"mn": 600, "mx": 670},
        "Komunikasi dan Pengembangan Masyarakat": {"mn": 610, "mx": 680},
    },
    "Universitas Gadjah Mada": {
        # FK
        "Pendidikan Dokter": {"mn": 770, "mx": 840},
        "Ilmu Keperawatan": {"mn": 630, "mx": 700},
        "Gizi Kesehatan": {"mn": 650, "mx": 720},
        "Kedokteran Gigi": {"mn": 730, "mx": 800},
        "Kesehatan Masyarakat": {"mn": 635, "mx": 705},
        # FF
        "Farmasi": {"mn": 700, "mx": 770},
        # FT
        "Teknik Sipil": {"mn": 690, "mx": 760},
        "Teknik Mesin": {"mn": 690, "mx": 760},
        "Teknik Elektro": {"mn": 720, "mx": 790},
        "Teknik Kimia": {"mn": 700, "mx": 770},
        "Teknik Industri": {"mn": 730, "mx": 800},
        "Teknik Fisika": {"mn": 680, "mx": 750},
        "Teknik Nuklir dan Teknik Fisika": {"mn": 680, "mx": 750},
        "Teknik Geodesi": {"mn": 680, "mx": 750},
        "Teknik Geologi": {"mn": 685, "mx": 755},
        "Perencanaan Wilayah dan Kota": {"mn": 700, "mx": 770},
        "Arsitektur": {"mn": 720, "mx": 790},
        "Teknik Informatika": {"mn": 770, "mx": 840},
        "Ilmu Komputer": {"mn": 760, "mx": 830},
        "Teknologi Informasi": {"mn": 750, "mx": 820},
        # FMIPA
        "Matematika": {"mn": 660, "mx": 730},
        "Fisika": {"mn": 650, "mx": 720},
        "Kimia": {"mn": 660, "mx": 730},
        "Biologi": {"mn": 650, "mx": 720},
        "Statistika": {"mn": 680, "mx": 750},
        "Geofisika": {"mn": 640, "mx": 710},
        "Elektronika dan Instrumentasi": {"mn": 660, "mx": 730},
        # FH
        "Ilmu Hukum": {"mn": 700, "mx": 770},
        # FEB
        "Ilmu Ekonomi": {"mn": 690, "mx": 760},
        "Akuntansi": {"mn": 720, "mx": 790},
        "Manajemen": {"mn": 730, "mx": 800},
        # FISIPOL
        "Ilmu Komunikasi": {"mn": 690, "mx": 760},
        "Manajemen dan Kebijakan Publik": {"mn": 670, "mx": 740},
        "Sosiologi": {"mn": 650, "mx": 720},
        "Ilmu Politik": {"mn": 660, "mx": 730},
        "Pembangunan Sosial dan Kesejahteraan": {"mn": 640, "mx": 710},
        "Hubungan Internasional": {"mn": 710, "mx": 780},
        # FPN / Pertanian
        "Agronomi": {"mn": 610, "mx": 680},
        "Ilmu Tanah": {"mn": 590, "mx": 660},
        "Proteksi Tanaman": {"mn": 600, "mx": 670},
        "Teknologi Pangan dan Hasil Pertanian": {"mn": 625, "mx": 695},
        "Agribisnis": {"mn": 640, "mx": 710},
        "Penyuluhan dan Komunikasi Pertanian": {"mn": 590, "mx": 660},
        # FKH
        "Kedokteran Hewan": {"mn": 660, "mx": 730},
        # Kehutanan
        "Kehutanan": {"mn": 610, "mx": 680},
        # Peternakan
        "Peternakan": {"mn": 600, "mx": 670},
        # FIB
        "Sastra Indonesia": {"mn": 600, "mx": 670},
        "Sastra Inggris": {"mn": 640, "mx": 710},
        "Sastra Arab": {"mn": 590, "mx": 660},
        "Sastra Jawa": {"mn": 560, "mx": 630},
        "Arkeologi": {"mn": 590, "mx": 660},
        "Sejarah": {"mn": 590, "mx": 660},
        "Antropologi Budaya": {"mn": 600, "mx": 670},
        "Pariwisata": {"mn": 620, "mx": 690},
        "Bahasa Korea": {"mn": 610, "mx": 680},
        "Bahasa dan Sastra Prancis": {"mn": 600, "mx": 670},
        # Filsafat
        "Filsafat": {"mn": 595, "mx": 665},
        # FPsi
        "Psikologi": {"mn": 700, "mx": 770},
        # FGE
        "Geografi Lingkungan": {"mn": 620, "mx": 690},
        "Kartografi dan Penginderaan Jauh": {"mn": 610, "mx": 680},
        "Pembangunan Wilayah": {"mn": 620, "mx": 690},
    },
    "Universitas Airlangga": {
        # FK
        "Pendidikan Dokter": {"mn": 740, "mx": 810},
        "Ilmu Keperawatan": {"mn": 610, "mx": 680},
        "Ilmu Gizi": {"mn": 620, "mx": 690},
        "Kedokteran Gigi": {"mn": 700, "mx": 770},
        # FKM
        "Kesehatan Masyarakat": {"mn": 610, "mx": 680},
        # FF
        "Farmasi": {"mn": 680, "mx": 750},
        # FKH
        "Kedokteran Hewan": {"mn": 650, "mx": 720},
        # FST
        "Matematika": {"mn": 610, "mx": 680},
        "Fisika": {"mn": 590, "mx": 660},
        "Kimia": {"mn": 610, "mx": 680},
        "Biologi": {"mn": 610, "mx": 680},
        "Ilmu Komputer": {"mn": 670, "mx": 740},
        "Statistika": {"mn": 630, "mx": 700},
        "Teknik Lingkungan": {"mn": 605, "mx": 675},
        # FH
        "Ilmu Hukum": {"mn": 660, "mx": 730},
        # FEB
        "Ilmu Ekonomi": {"mn": 650, "mx": 720},
        "Akuntansi": {"mn": 680, "mx": 750},
        "Manajemen": {"mn": 690, "mx": 760},
        "Ekonomi Islam": {"mn": 625, "mx": 695},
        # FISIP
        "Ilmu Komunikasi": {"mn": 650, "mx": 720},
        "Hubungan Internasional": {"mn": 670, "mx": 740},
        "Sosiologi": {"mn": 610, "mx": 680},
        "Ilmu Politik": {"mn": 620, "mx": 690},
        "Ilmu Informasi dan Perpustakaan": {"mn": 570, "mx": 640},
        "Ilmu Kesejahteraan Sosial": {"mn": 590, "mx": 660},
        "Administrasi Publik": {"mn": 610, "mx": 680},
        "Administrasi Bisnis": {"mn": 620, "mx": 690},
        # FPsi
        "Psikologi": {"mn": 670, "mx": 740},
        # FIB
        "Sastra Indonesia": {"mn": 570, "mx": 640},
        "Sastra Inggris": {"mn": 610, "mx": 680},
        "Sastra Jepang": {"mn": 590, "mx": 660},
    },
    "Universitas Padjadjaran": {
        # FK
        "Pendidikan Dokter": {"mn": 730, "mx": 800},
        "Ilmu Keperawatan": {"mn": 600, "mx": 670},
        "Ilmu Gizi": {"mn": 610, "mx": 680},
        "Kedokteran Gigi": {"mn": 690, "mx": 760},
        # FKM
        "Kesehatan Masyarakat": {"mn": 600, "mx": 670},
        # FF
        "Farmasi": {"mn": 660, "mx": 730},
        # FKH
        "Kedokteran Hewan": {"mn": 630, "mx": 700},
        # FMIPA
        "Matematika": {"mn": 600, "mx": 670},
        "Fisika": {"mn": 580, "mx": 650},
        "Kimia": {"mn": 600, "mx": 670},
        "Biologi": {"mn": 600, "mx": 670},
        "Ilmu Komputer": {"mn": 660, "mx": 730},
        "Statistika": {"mn": 620, "mx": 690},
        "Geofisika": {"mn": 590, "mx": 660},
        # FT
        "Teknik Informatika": {"mn": 680, "mx": 750},
        "Teknik Elektro": {"mn": 650, "mx": 720},
        "Teknik Industri": {"mn": 650, "mx": 720},
        "Teknik Geologi": {"mn": 620, "mx": 690},
        "Teknik Pertambangan": {"mn": 610, "mx": 680},
        # FH
        "Ilmu Hukum": {"mn": 640, "mx": 710},
        # FEB
        "Ilmu Ekonomi": {"mn": 640, "mx": 710},
        "Akuntansi": {"mn": 660, "mx": 730},
        "Manajemen": {"mn": 670, "mx": 740},
        "Bisnis Digital": {"mn": 640, "mx": 710},
        # FISIP
        "Ilmu Komunikasi": {"mn": 650, "mx": 720},
        "Hubungan Internasional": {"mn": 660, "mx": 730},
        "Sosiologi": {"mn": 600, "mx": 670},
        "Ilmu Politik": {"mn": 610, "mx": 680},
        "Administrasi Publik": {"mn": 600, "mx": 670},
        "Kesejahteraan Sosial": {"mn": 580, "mx": 650},
        # FIB
        "Sastra Indonesia": {"mn": 570, "mx": 640},
        "Sastra Inggris": {"mn": 610, "mx": 680},
        "Sastra Arab": {"mn": 570, "mx": 640},
        "Sastra Jepang": {"mn": 590, "mx": 660},
        "Sastra Jerman": {"mn": 570, "mx": 640},
        "Sastra Prancis": {"mn": 570, "mx": 640},
        "Sejarah": {"mn": 560, "mx": 630},
        # FPsi
        "Psikologi": {"mn": 660, "mx": 730},
        # FPIK
        "Ilmu Kelautan": {"mn": 580, "mx": 650},
        "Perikanan": {"mn": 570, "mx": 640},
        # FAPERTA
        "Agribisnis": {"mn": 600, "mx": 670},
        "Agroteknologi": {"mn": 590, "mx": 660},
        # FAPET
        "Peternakan": {"mn": 570, "mx": 640},
    },
    "Universitas Diponegoro": {
        "Pendidikan Dokter": {"mn": 710, "mx": 780},
        "Ilmu Keperawatan": {"mn": 590, "mx": 660},
        "Kesehatan Masyarakat": {"mn": 590, "mx": 660},
        "Ilmu Gizi": {"mn": 590, "mx": 660},
        "Kedokteran Gigi": {"mn": 660, "mx": 730},
        "Farmasi": {"mn": 630, "mx": 700},
        "Teknik Sipil": {"mn": 640, "mx": 710},
        "Teknik Mesin": {"mn": 640, "mx": 710},
        "Teknik Elektro": {"mn": 660, "mx": 730},
        "Teknik Kimia": {"mn": 650, "mx": 720},
        "Teknik Industri": {"mn": 660, "mx": 730},
        "Teknik Lingkungan": {"mn": 620, "mx": 690},
        "Teknik Geologi": {"mn": 620, "mx": 690},
        "Teknik Perkapalan": {"mn": 610, "mx": 680},
        "Arsitektur": {"mn": 650, "mx": 720},
        "Perencanaan Wilayah dan Kota": {"mn": 640, "mx": 710},
        "Teknik Informatika": {"mn": 690, "mx": 760},
        "Sistem Komputer": {"mn": 655, "mx": 725},
        "Matematika": {"mn": 600, "mx": 670},
        "Fisika": {"mn": 580, "mx": 650},
        "Kimia": {"mn": 590, "mx": 660},
        "Biologi": {"mn": 580, "mx": 650},
        "Statistika": {"mn": 610, "mx": 680},
        "Ilmu Hukum": {"mn": 620, "mx": 690},
        "Ilmu Ekonomi": {"mn": 620, "mx": 690},
        "Akuntansi": {"mn": 640, "mx": 710},
        "Manajemen": {"mn": 650, "mx": 720},
        "Perpajakan": {"mn": 610, "mx": 680},
        "Ilmu Komunikasi": {"mn": 630, "mx": 700},
        "Hubungan Internasional": {"mn": 640, "mx": 710},
        "Administrasi Publik": {"mn": 590, "mx": 660},
        "Ilmu Politik": {"mn": 590, "mx": 660},
        "Ilmu Pemerintahan": {"mn": 590, "mx": 660},
        "Psikologi": {"mn": 640, "mx": 710},
        "Sastra Indonesia": {"mn": 555, "mx": 625},
        "Sastra Inggris": {"mn": 590, "mx": 660},
        "Ilmu Kelautan": {"mn": 570, "mx": 640},
        "Perikanan": {"mn": 560, "mx": 630},
        "Peternakan": {"mn": 550, "mx": 620},
        "Agribisnis": {"mn": 570, "mx": 640},
        "Teknologi Pangan": {"mn": 590, "mx": 660},
        "Ilmu Keolahragaan": {"mn": 530, "mx": 600},
    },
    "Universitas Brawijaya": {
        "Pendidikan Dokter": {"mn": 710, "mx": 780},
        "Ilmu Keperawatan": {"mn": 580, "mx": 650},
        "Ilmu Gizi": {"mn": 590, "mx": 660},
        "Kesehatan Masyarakat": {"mn": 580, "mx": 650},
        "Kedokteran Gigi": {"mn": 650, "mx": 720},
        "Farmasi": {"mn": 620, "mx": 690},
        "Kedokteran Hewan": {"mn": 620, "mx": 690},
        "Teknik Sipil": {"mn": 620, "mx": 690},
        "Teknik Mesin": {"mn": 620, "mx": 690},
        "Teknik Elektro": {"mn": 640, "mx": 710},
        "Teknik Kimia": {"mn": 630, "mx": 700},
        "Teknik Industri": {"mn": 640, "mx": 710},
        "Teknik Pengairan": {"mn": 590, "mx": 660},
        "Arsitektur": {"mn": 640, "mx": 710},
        "Teknik Informatika": {"mn": 680, "mx": 750},
        "Sistem Informasi": {"mn": 650, "mx": 720},
        "Teknologi Informasi": {"mn": 640, "mx": 710},
        "Teknik Komputer": {"mn": 640, "mx": 710},
        "Matematika": {"mn": 580, "mx": 650},
        "Fisika": {"mn": 560, "mx": 630},
        "Kimia": {"mn": 570, "mx": 640},
        "Biologi": {"mn": 570, "mx": 640},
        "Statistika": {"mn": 590, "mx": 660},
        "Ilmu Hukum": {"mn": 600, "mx": 670},
        "Ilmu Ekonomi": {"mn": 600, "mx": 670},
        "Akuntansi": {"mn": 620, "mx": 690},
        "Manajemen": {"mn": 630, "mx": 700},
        "Ilmu Komunikasi": {"mn": 610, "mx": 680},
        "Hubungan Internasional": {"mn": 620, "mx": 690},
        "Sosiologi": {"mn": 570, "mx": 640},
        "Ilmu Politik": {"mn": 570, "mx": 640},
        "Administrasi Bisnis": {"mn": 590, "mx": 660},
        "Administrasi Publik": {"mn": 575, "mx": 645},
        "Psikologi": {"mn": 630, "mx": 700},
        "Sastra Indonesia": {"mn": 540, "mx": 610},
        "Sastra Inggris": {"mn": 580, "mx": 650},
        "Sastra Jepang": {"mn": 560, "mx": 630},
        "Agribisnis": {"mn": 570, "mx": 640},
        "Agroekoteknologi": {"mn": 560, "mx": 630},
        "Kehutanan": {"mn": 560, "mx": 630},
        "Peternakan": {"mn": 550, "mx": 620},
        "Ilmu Kelautan": {"mn": 560, "mx": 630},
        "Budidaya Perairan": {"mn": 550, "mx": 620},
        "Teknologi Pangan": {"mn": 580, "mx": 650},
        "Ilmu Tanah": {"mn": 550, "mx": 620},
    },
    "Universitas Sebelas Maret": {
        "Pendidikan Dokter": {"mn": 700, "mx": 770},
        "Ilmu Keperawatan": {"mn": 570, "mx": 640},
        "Ilmu Gizi": {"mn": 580, "mx": 650},
        "Kesehatan Masyarakat": {"mn": 570, "mx": 640},
        "Kedokteran Gigi": {"mn": 640, "mx": 710},
        "Farmasi": {"mn": 610, "mx": 680},
        "Teknik Sipil": {"mn": 610, "mx": 680},
        "Teknik Mesin": {"mn": 610, "mx": 680},
        "Teknik Elektro": {"mn": 620, "mx": 690},
        "Teknik Kimia": {"mn": 610, "mx": 680},
        "Teknik Industri": {"mn": 620, "mx": 690},
        "Arsitektur": {"mn": 630, "mx": 700},
        "Teknik Informatika": {"mn": 660, "mx": 730},
        "Informatika": {"mn": 655, "mx": 725},
        "Matematika": {"mn": 570, "mx": 640},
        "Fisika": {"mn": 550, "mx": 620},
        "Kimia": {"mn": 560, "mx": 630},
        "Biologi": {"mn": 560, "mx": 630},
        "Statistika": {"mn": 580, "mx": 650},
        "Ilmu Hukum": {"mn": 590, "mx": 660},
        "Ilmu Ekonomi": {"mn": 590, "mx": 660},
        "Akuntansi": {"mn": 610, "mx": 680},
        "Manajemen": {"mn": 620, "mx": 690},
        "Ilmu Komunikasi": {"mn": 600, "mx": 670},
        "Hubungan Internasional": {"mn": 610, "mx": 680},
        "Sosiologi": {"mn": 560, "mx": 630},
        "Ilmu Politik": {"mn": 560, "mx": 630},
        "Administrasi Negara": {"mn": 565, "mx": 635},
        "Psikologi": {"mn": 620, "mx": 690},
        "Sastra Indonesia": {"mn": 530, "mx": 600},
        "Sastra Inggris": {"mn": 570, "mx": 640},
        "Sastra Jawa": {"mn": 510, "mx": 580},
        "Sastra Daerah (Jawa)": {"mn": 505, "mx": 575},
        "Sejarah": {"mn": 520, "mx": 590},
        "Seni Rupa Murni": {"mn": 500, "mx": 570},
        "Kriya Seni": {"mn": 490, "mx": 560},
        "Agribisnis": {"mn": 550, "mx": 620},
        "Agroteknologi": {"mn": 540, "mx": 610},
        "Peternakan": {"mn": 530, "mx": 600},
        "Ilmu Tanah": {"mn": 530, "mx": 600},
        "Kehutanan": {"mn": 535, "mx": 605},
        "Teknologi Pangan": {"mn": 560, "mx": 630},
        "Pendidikan Matematika": {"mn": 565, "mx": 635},
        "Pendidikan Biologi": {"mn": 545, "mx": 615},
        "Pendidikan Kimia": {"mn": 545, "mx": 615},
        "Pendidikan Fisika": {"mn": 545, "mx": 615},
        "Pendidikan Bahasa Inggris": {"mn": 570, "mx": 640},
        "Pendidikan Bahasa Indonesia": {"mn": 530, "mx": 600},
        "Pendidikan Ekonomi": {"mn": 540, "mx": 610},
        "Pendidikan Sejarah": {"mn": 510, "mx": 580},
        "Pendidikan Sosiologi Antropologi": {"mn": 510, "mx": 580},
        "Pendidikan Pancasila dan Kewarganegaraan": {"mn": 510, "mx": 580},
    },
    "Universitas Hasanuddin": {
        "Pendidikan Dokter": {"mn": 690, "mx": 760},
        "Ilmu Keperawatan": {"mn": 560, "mx": 630},
        "Ilmu Gizi": {"mn": 570, "mx": 640},
        "Kesehatan Masyarakat": {"mn": 560, "mx": 630},
        "Kedokteran Gigi": {"mn": 640, "mx": 710},
        "Farmasi": {"mn": 600, "mx": 670},
        "Kedokteran Hewan": {"mn": 590, "mx": 660},
        "Teknik Sipil": {"mn": 600, "mx": 670},
        "Teknik Mesin": {"mn": 600, "mx": 670},
        "Teknik Elektro": {"mn": 620, "mx": 690},
        "Teknik Kimia": {"mn": 600, "mx": 670},
        "Teknik Industri": {"mn": 610, "mx": 680},
        "Teknik Geologi": {"mn": 600, "mx": 670},
        "Teknik Perminyakan": {"mn": 620, "mx": 690},
        "Arsitektur": {"mn": 620, "mx": 690},
        "Perencanaan Wilayah dan Kota": {"mn": 600, "mx": 670},
        "Teknik Informatika": {"mn": 650, "mx": 720},
        "Sistem Informasi": {"mn": 620, "mx": 690},
        "Teknik Lingkungan": {"mn": 590, "mx": 660},
        "Teknik Kelautan": {"mn": 580, "mx": 650},
        "Matematika": {"mn": 560, "mx": 630},
        "Fisika": {"mn": 540, "mx": 610},
        "Kimia": {"mn": 550, "mx": 620},
        "Biologi": {"mn": 550, "mx": 620},
        "Statistika": {"mn": 570, "mx": 640},
        "Ilmu Hukum": {"mn": 580, "mx": 650},
        "Ilmu Ekonomi": {"mn": 580, "mx": 650},
        "Akuntansi": {"mn": 600, "mx": 670},
        "Manajemen": {"mn": 610, "mx": 680},
        "Ilmu Komunikasi": {"mn": 590, "mx": 660},
        "Hubungan Internasional": {"mn": 600, "mx": 670},
        "Sosiologi": {"mn": 550, "mx": 620},
        "Ilmu Politik": {"mn": 555, "mx": 625},
        "Administrasi Negara": {"mn": 560, "mx": 630},
        "Ilmu Pemerintahan": {"mn": 560, "mx": 630},
        "Psikologi": {"mn": 610, "mx": 680},
        "Sastra Indonesia": {"mn": 520, "mx": 590},
        "Sastra Inggris": {"mn": 560, "mx": 630},
        "Sejarah": {"mn": 510, "mx": 580},
        "Agribisnis": {"mn": 540, "mx": 610},
        "Agroteknologi": {"mn": 530, "mx": 600},
        "Kehutanan": {"mn": 530, "mx": 600},
        "Peternakan": {"mn": 520, "mx": 590},
        "Ilmu Kelautan": {"mn": 540, "mx": 610},
        "Budidaya Perairan": {"mn": 530, "mx": 600},
        "Teknologi Pangan": {"mn": 560, "mx": 630},
    },
    "Universitas Sumatera Utara": {
        "Pendidikan Dokter": {"mn": 680, "mx": 750},
        "Ilmu Keperawatan": {"mn": 550, "mx": 620},
        "Ilmu Gizi": {"mn": 560, "mx": 630},
        "Kesehatan Masyarakat": {"mn": 550, "mx": 620},
        "Kedokteran Gigi": {"mn": 630, "mx": 700},
        "Farmasi": {"mn": 590, "mx": 660},
        "Teknik Sipil": {"mn": 590, "mx": 660},
        "Teknik Mesin": {"mn": 590, "mx": 660},
        "Teknik Elektro": {"mn": 610, "mx": 680},
        "Teknik Kimia": {"mn": 590, "mx": 660},
        "Teknik Industri": {"mn": 600, "mx": 670},
        "Teknik Informatika": {"mn": 630, "mx": 700},
        "Arsitektur": {"mn": 600, "mx": 670},
        "Teknik Lingkungan": {"mn": 575, "mx": 645},
        "Matematika": {"mn": 540, "mx": 610},
        "Fisika": {"mn": 520, "mx": 590},
        "Kimia": {"mn": 530, "mx": 600},
        "Biologi": {"mn": 530, "mx": 600},
        "Statistika": {"mn": 550, "mx": 620},
        "Ilmu Komputer": {"mn": 600, "mx": 670},
        "Ilmu Hukum": {"mn": 560, "mx": 630},
        "Ilmu Ekonomi": {"mn": 560, "mx": 630},
        "Akuntansi": {"mn": 580, "mx": 650},
        "Manajemen": {"mn": 590, "mx": 660},
        "Ilmu Komunikasi": {"mn": 570, "mx": 640},
        "Hubungan Internasional": {"mn": 580, "mx": 650},
        "Sosiologi": {"mn": 530, "mx": 600},
        "Ilmu Politik": {"mn": 530, "mx": 600},
        "Administrasi Negara": {"mn": 540, "mx": 610},
        "Administrasi Bisnis": {"mn": 545, "mx": 615},
        "Ilmu Perpustakaan": {"mn": 500, "mx": 570},
        "Kesejahteraan Sosial": {"mn": 520, "mx": 590},
        "Psikologi": {"mn": 580, "mx": 650},
        "Sastra Indonesia": {"mn": 500, "mx": 570},
        "Sastra Inggris": {"mn": 540, "mx": 610},
        "Sastra Melayu": {"mn": 490, "mx": 560},
        "Sastra Arab": {"mn": 490, "mx": 560},
        "Sastra Jepang": {"mn": 510, "mx": 580},
        "Sastra Cina": {"mn": 510, "mx": 580},
        "Sejarah": {"mn": 490, "mx": 560},
        "Agribisnis": {"mn": 520, "mx": 590},
        "Agroekoteknologi": {"mn": 510, "mx": 580},
        "Kehutanan": {"mn": 510, "mx": 580},
        "Peternakan": {"mn": 500, "mx": 570},
        "Ilmu Kelautan": {"mn": 510, "mx": 580},
        "Budidaya Perairan": {"mn": 500, "mx": 570},
        "Teknologi Pangan": {"mn": 530, "mx": 600},
    },
    "Universitas Andalas": {
        "Pendidikan Dokter": {"mn": 680, "mx": 750},
        "Ilmu Keperawatan": {"mn": 550, "mx": 620},
        "Ilmu Gizi": {"mn": 560, "mx": 630},
        "Kesehatan Masyarakat": {"mn": 550, "mx": 620},
        "Kedokteran Gigi": {"mn": 620, "mx": 690},
        "Farmasi": {"mn": 590, "mx": 660},
        "Kedokteran Hewan": {"mn": 580, "mx": 650},
        "Teknik Sipil": {"mn": 580, "mx": 650},
        "Teknik Mesin": {"mn": 580, "mx": 650},
        "Teknik Elektro": {"mn": 600, "mx": 670},
        "Teknik Kimia": {"mn": 580, "mx": 650},
        "Teknik Industri": {"mn": 590, "mx": 660},
        "Teknik Lingkungan": {"mn": 570, "mx": 640},
        "Arsitektur": {"mn": 590, "mx": 660},
        "Teknik Informatika": {"mn": 620, "mx": 690},
        "Sistem Informasi": {"mn": 600, "mx": 670},
        "Matematika": {"mn": 530, "mx": 600},
        "Fisika": {"mn": 510, "mx": 580},
        "Kimia": {"mn": 520, "mx": 590},
        "Biologi": {"mn": 520, "mx": 590},
        "Statistika": {"mn": 540, "mx": 610},
        "Ilmu Hukum": {"mn": 550, "mx": 620},
        "Ilmu Ekonomi": {"mn": 550, "mx": 620},
        "Akuntansi": {"mn": 570, "mx": 640},
        "Manajemen": {"mn": 580, "mx": 650},
        "Ilmu Komunikasi": {"mn": 560, "mx": 630},
        "Sosiologi": {"mn": 520, "mx": 590},
        "Ilmu Politik": {"mn": 520, "mx": 590},
        "Administrasi Publik": {"mn": 525, "mx": 595},
        "Ilmu Pemerintahan": {"mn": 525, "mx": 595},
        "Hubungan Internasional": {"mn": 560, "mx": 630},
        "Psikologi": {"mn": 570, "mx": 640},
        "Sastra Indonesia": {"mn": 490, "mx": 560},
        "Sastra Inggris": {"mn": 530, "mx": 600},
        "Sastra Minangkabau": {"mn": 460, "mx": 530},
        "Sejarah": {"mn": 480, "mx": 550},
        "Agribisnis": {"mn": 510, "mx": 580},
        "Agroteknologi": {"mn": 500, "mx": 570},
        "Peternakan": {"mn": 490, "mx": 560},
        "Kehutanan": {"mn": 490, "mx": 560},
        "Teknologi Pangan": {"mn": 540, "mx": 610},
        "Ilmu Kelautan": {"mn": 500, "mx": 570},
        "Budidaya Perairan": {"mn": 490, "mx": 560},
        "Ilmu Tanah": {"mn": 490, "mx": 560},
    },
    "Universitas Sriwijaya": {
        "Pendidikan Dokter": {"mn": 650, "mx": 720},
        "Ilmu Keperawatan": {"mn": 530, "mx": 600},
        "Kesehatan Masyarakat": {"mn": 530, "mx": 600},
        "Kedokteran Gigi": {"mn": 600, "mx": 670},
        "Farmasi": {"mn": 570, "mx": 640},
        "Teknik Sipil": {"mn": 560, "mx": 630},
        "Teknik Mesin": {"mn": 560, "mx": 630},
        "Teknik Elektro": {"mn": 580, "mx": 650},
        "Teknik Kimia": {"mn": 570, "mx": 640},
        "Teknik Industri": {"mn": 575, "mx": 645},
        "Teknik Pertambangan": {"mn": 560, "mx": 630},
        "Teknik Geologi": {"mn": 560, "mx": 630},
        "Teknik Informatika": {"mn": 600, "mx": 670},
        "Sistem Informasi": {"mn": 580, "mx": 650},
        "Ilmu Komputer": {"mn": 580, "mx": 650},
        "Arsitektur": {"mn": 565, "mx": 635},
        "Teknik Kimia": {"mn": 570, "mx": 640},
        "Matematika": {"mn": 510, "mx": 580},
        "Fisika": {"mn": 490, "mx": 560},
        "Kimia": {"mn": 500, "mx": 570},
        "Biologi": {"mn": 500, "mx": 570},
        "Ilmu Hukum": {"mn": 530, "mx": 600},
        "Ilmu Ekonomi": {"mn": 530, "mx": 600},
        "Akuntansi": {"mn": 550, "mx": 620},
        "Manajemen": {"mn": 560, "mx": 630},
        "Ilmu Komunikasi": {"mn": 540, "mx": 610},
        "Sosiologi": {"mn": 500, "mx": 570},
        "Administrasi Negara": {"mn": 510, "mx": 580},
        "Hubungan Internasional": {"mn": 550, "mx": 620},
        "Ilmu Pemerintahan": {"mn": 510, "mx": 580},
        "Psikologi": {"mn": 550, "mx": 620},
        "Sastra Indonesia": {"mn": 470, "mx": 540},
        "Sastra Inggris": {"mn": 510, "mx": 580},
        "Sastra Arab": {"mn": 460, "mx": 530},
        "Agribisnis": {"mn": 490, "mx": 560},
        "Agroekoteknologi": {"mn": 480, "mx": 550},
        "Peternakan": {"mn": 470, "mx": 540},
        "Kehutanan": {"mn": 470, "mx": 540},
        "Ilmu Kelautan": {"mn": 480, "mx": 550},
        "Budidaya Perairan": {"mn": 470, "mx": 540},
        "Teknologi Pangan": {"mn": 510, "mx": 580},
    },
    "Universitas Udayana": {
        "Pendidikan Dokter": {"mn": 680, "mx": 750},
        "Ilmu Keperawatan": {"mn": 550, "mx": 620},
        "Ilmu Gizi": {"mn": 560, "mx": 630},
        "Kesehatan Masyarakat": {"mn": 550, "mx": 620},
        "Kedokteran Gigi": {"mn": 630, "mx": 700},
        "Farmasi": {"mn": 590, "mx": 660},
        "Kedokteran Hewan": {"mn": 600, "mx": 670},
        "Teknik Sipil": {"mn": 580, "mx": 650},
        "Teknik Mesin": {"mn": 575, "mx": 645},
        "Teknik Elektro": {"mn": 600, "mx": 670},
        "Teknik Kimia": {"mn": 575, "mx": 645},
        "Teknik Industri": {"mn": 580, "mx": 650},
        "Arsitektur": {"mn": 600, "mx": 670},
        "Teknik Informatika": {"mn": 630, "mx": 700},
        "Sistem Informasi": {"mn": 600, "mx": 670},
        "Teknologi Informasi": {"mn": 610, "mx": 680},
        "Teknik Lingkungan": {"mn": 570, "mx": 640},
        "Matematika": {"mn": 530, "mx": 600},
        "Fisika": {"mn": 510, "mx": 580},
        "Kimia": {"mn": 520, "mx": 590},
        "Biologi": {"mn": 520, "mx": 590},
        "Ilmu Komputer": {"mn": 600, "mx": 670},
        "Ilmu Hukum": {"mn": 550, "mx": 620},
        "Ilmu Ekonomi": {"mn": 550, "mx": 620},
        "Akuntansi": {"mn": 570, "mx": 640},
        "Manajemen": {"mn": 580, "mx": 650},
        "Ilmu Komunikasi": {"mn": 560, "mx": 630},
        "Sosiologi": {"mn": 520, "mx": 590},
        "Ilmu Politik": {"mn": 520, "mx": 590},
        "Administrasi Negara": {"mn": 530, "mx": 600},
        "Ilmu Pemerintahan": {"mn": 530, "mx": 600},
        "Hubungan Internasional": {"mn": 565, "mx": 635},
        "Psikologi": {"mn": 570, "mx": 640},
        "Sastra Indonesia": {"mn": 490, "mx": 560},
        "Sastra Inggris": {"mn": 530, "mx": 600},
        "Sastra Bali": {"mn": 450, "mx": 520},
        "Sejarah": {"mn": 480, "mx": 550},
        "Pariwisata": {"mn": 560, "mx": 630},
        "Destinasi Pariwisata": {"mn": 550, "mx": 620},
        "Agribisnis": {"mn": 510, "mx": 580},
        "Agroteknologi": {"mn": 500, "mx": 570},
        "Peternakan": {"mn": 490, "mx": 560},
        "Ilmu Kelautan": {"mn": 510, "mx": 580},
        "Budidaya Perairan": {"mn": 500, "mx": 570},
        "Teknologi Pangan": {"mn": 530, "mx": 600},
    },
    "Universitas Pendidikan Indonesia": {
        "Pendidikan Matematika": {"mn": 580, "mx": 650},
        "Pendidikan Biologi": {"mn": 560, "mx": 630},
        "Pendidikan Kimia": {"mn": 560, "mx": 630},
        "Pendidikan Fisika": {"mn": 560, "mx": 630},
        "Pendidikan Ilmu Komputer": {"mn": 600, "mx": 670},
        "Ilmu Komputer": {"mn": 610, "mx": 680},
        "Teknik Informatika": {"mn": 620, "mx": 690},
        "Teknik Elektro": {"mn": 580, "mx": 650},
        "Teknik Mesin": {"mn": 560, "mx": 630},
        "Pendidikan Teknik Arsitektur": {"mn": 560, "mx": 630},
        "Pendidikan Teknik Bangunan": {"mn": 545, "mx": 615},
        "Pendidikan Bahasa Inggris": {"mn": 590, "mx": 660},
        "Pendidikan Bahasa Indonesia": {"mn": 540, "mx": 610},
        "Pendidikan Bahasa Jepang": {"mn": 540, "mx": 610},
        "Pendidikan Bahasa Arab": {"mn": 520, "mx": 590},
        "Pendidikan Bahasa Perancis": {"mn": 520, "mx": 590},
        "Pendidikan Bahasa Jerman": {"mn": 515, "mx": 585},
        "Pendidikan Ekonomi": {"mn": 540, "mx": 610},
        "Manajemen": {"mn": 580, "mx": 650},
        "Akuntansi": {"mn": 580, "mx": 650},
        "Pendidikan Akuntansi": {"mn": 540, "mx": 610},
        "Pendidikan Sejarah": {"mn": 520, "mx": 590},
        "Pendidikan Sosiologi": {"mn": 520, "mx": 590},
        "Pendidikan Geografi": {"mn": 520, "mx": 590},
        "Bimbingan dan Konseling": {"mn": 500, "mx": 570},
        "Pendidikan Luar Biasa": {"mn": 500, "mx": 570},
        "Pendidikan Luar Sekolah": {"mn": 490, "mx": 560},
        "Psikologi": {"mn": 600, "mx": 670},
        "Ilmu Komunikasi": {"mn": 580, "mx": 650},
        "Pendidikan Jasmani Kesehatan dan Rekreasi": {"mn": 490, "mx": 560},
        "Pendidikan Kepelatihan Olahraga": {"mn": 480, "mx": 550},
        "Pendidikan Seni Rupa": {"mn": 460, "mx": 530},
        "Pendidikan Seni Musik": {"mn": 460, "mx": 530},
        "Perpustakaan dan Sains Informasi": {"mn": 490, "mx": 560},
        "Administrasi Pendidikan": {"mn": 490, "mx": 560},
        "Teknologi Pendidikan": {"mn": 490, "mx": 560},
        "Pendidikan Guru Sekolah Dasar": {"mn": 510, "mx": 580},
    },
    "Universitas Negeri Yogyakarta": {
        "Pendidikan Matematika": {"mn": 580, "mx": 650},
        "Pendidikan Biologi": {"mn": 560, "mx": 630},
        "Pendidikan Kimia": {"mn": 560, "mx": 630},
        "Pendidikan Fisika": {"mn": 560, "mx": 630},
        "Matematika": {"mn": 560, "mx": 630},
        "Biologi": {"mn": 540, "mx": 610},
        "Kimia": {"mn": 540, "mx": 610},
        "Fisika": {"mn": 540, "mx": 610},
        "Ilmu Komputer": {"mn": 590, "mx": 660},
        "Teknik Informatika": {"mn": 600, "mx": 670},
        "Teknik Elektro": {"mn": 560, "mx": 630},
        "Teknik Mesin": {"mn": 550, "mx": 620},
        "Pendidikan Teknik Sipil dan Perencanaan": {"mn": 545, "mx": 615},
        "Teknik Boga": {"mn": 490, "mx": 560},
        "Teknik Busana": {"mn": 470, "mx": 540},
        "Pendidikan Bahasa Inggris": {"mn": 580, "mx": 650},
        "Pendidikan Bahasa Indonesia": {"mn": 540, "mx": 610},
        "Pendidikan Bahasa Jerman": {"mn": 510, "mx": 580},
        "Pendidikan Bahasa Prancis": {"mn": 510, "mx": 580},
        "Pendidikan Ekonomi": {"mn": 540, "mx": 610},
        "Manajemen": {"mn": 570, "mx": 640},
        "Akuntansi": {"mn": 570, "mx": 640},
        "Pendidikan Akuntansi": {"mn": 530, "mx": 600},
        "Pendidikan Sejarah": {"mn": 510, "mx": 580},
        "Pendidikan Sosiologi": {"mn": 510, "mx": 580},
        "Pendidikan Geografi": {"mn": 510, "mx": 580},
        "Ilmu Keolahragaan": {"mn": 490, "mx": 560},
        "Pendidikan Jasmani Kesehatan dan Rekreasi": {"mn": 480, "mx": 550},
        "Psikologi": {"mn": 590, "mx": 660},
        "Pendidikan Luar Biasa": {"mn": 490, "mx": 560},
        "Pendidikan Seni Rupa": {"mn": 460, "mx": 530},
        "Pendidikan Seni Musik": {"mn": 460, "mx": 530},
        "Administrasi Pendidikan": {"mn": 490, "mx": 560},
        "Bimbingan dan Konseling": {"mn": 490, "mx": 560},
        "Pendidikan Guru Sekolah Dasar": {"mn": 510, "mx": 580},
        "Teknologi Pendidikan": {"mn": 490, "mx": 560},
    },
    "Universitas Negeri Malang": {
        "Pendidikan Matematika": {"mn": 560, "mx": 630},
        "Pendidikan Biologi": {"mn": 540, "mx": 610},
        "Pendidikan Kimia": {"mn": 540, "mx": 610},
        "Pendidikan Fisika": {"mn": 540, "mx": 610},
        "Matematika": {"mn": 540, "mx": 610},
        "Biologi": {"mn": 520, "mx": 590},
        "Kimia": {"mn": 520, "mx": 590},
        "Fisika": {"mn": 520, "mx": 590},
        "Ilmu Komputer": {"mn": 570, "mx": 640},
        "Teknik Informatika": {"mn": 580, "mx": 650},
        "Teknik Elektro": {"mn": 540, "mx": 610},
        "Teknik Mesin": {"mn": 530, "mx": 600},
        "Teknik Sipil": {"mn": 530, "mx": 600},
        "Arsitektur": {"mn": 550, "mx": 620},
        "Pendidikan Bahasa Inggris": {"mn": 560, "mx": 630},
        "Pendidikan Bahasa Indonesia": {"mn": 520, "mx": 590},
        "Pendidikan Bahasa Arab": {"mn": 500, "mx": 570},
        "Pendidikan Bahasa Jepang": {"mn": 500, "mx": 570},
        "Pendidikan Bahasa Mandarin": {"mn": 500, "mx": 570},
        "Pendidikan Ekonomi": {"mn": 520, "mx": 590},
        "Manajemen": {"mn": 550, "mx": 620},
        "Akuntansi": {"mn": 550, "mx": 620},
        "Pendidikan Akuntansi": {"mn": 510, "mx": 580},
        "Pendidikan Sejarah": {"mn": 490, "mx": 560},
        "Pendidikan Sosiologi": {"mn": 490, "mx": 560},
        "Pendidikan Geografi": {"mn": 490, "mx": 560},
        "Ilmu Keolahragaan": {"mn": 470, "mx": 540},
        "Pendidikan Jasmani Kesehatan dan Rekreasi": {"mn": 460, "mx": 530},
        "Psikologi": {"mn": 570, "mx": 640},
        "Bimbingan dan Konseling": {"mn": 470, "mx": 540},
        "Pendidikan Luar Biasa": {"mn": 460, "mx": 530},
        "Administrasi Pendidikan": {"mn": 470, "mx": 540},
        "Teknologi Pendidikan": {"mn": 470, "mx": 540},
        "Pendidikan Guru Sekolah Dasar": {"mn": 490, "mx": 560},
        "Seni dan Desain": {"mn": 460, "mx": 530},
    },
    "Universitas Negeri Semarang": {
        "Pendidikan Matematika": {"mn": 540, "mx": 610},
        "Pendidikan Biologi": {"mn": 520, "mx": 590},
        "Pendidikan Kimia": {"mn": 520, "mx": 590},
        "Pendidikan Fisika": {"mn": 520, "mx": 590},
        "Matematika": {"mn": 520, "mx": 590},
        "Biologi": {"mn": 500, "mx": 570},
        "Kimia": {"mn": 500, "mx": 570},
        "Fisika": {"mn": 500, "mx": 570},
        "Ilmu Komputer": {"mn": 550, "mx": 620},
        "Teknik Informatika": {"mn": 560, "mx": 630},
        "Teknik Elektro": {"mn": 520, "mx": 590},
        "Teknik Mesin": {"mn": 510, "mx": 580},
        "Teknik Sipil": {"mn": 510, "mx": 580},
        "Teknik Kimia": {"mn": 510, "mx": 580},
        "Arsitektur": {"mn": 530, "mx": 600},
        "Pendidikan Bahasa Inggris": {"mn": 540, "mx": 610},
        "Pendidikan Bahasa Indonesia": {"mn": 500, "mx": 570},
        "Pendidikan Bahasa Jawa": {"mn": 460, "mx": 530},
        "Pendidikan Ekonomi": {"mn": 500, "mx": 570},
        "Manajemen": {"mn": 530, "mx": 600},
        "Akuntansi": {"mn": 530, "mx": 600},
        "Ekonomi Pembangunan": {"mn": 510, "mx": 580},
        "Pendidikan Sejarah": {"mn": 470, "mx": 540},
        "Pendidikan Sosiologi dan Antropologi": {"mn": 470, "mx": 540},
        "Pendidikan Geografi": {"mn": 470, "mx": 540},
        "Ilmu Hukum": {"mn": 520, "mx": 590},
        "Ilmu Keolahragaan": {"mn": 450, "mx": 520},
        "Psikologi": {"mn": 550, "mx": 620},
        "Kesehatan Masyarakat": {"mn": 530, "mx": 600},
        "Bimbingan dan Konseling": {"mn": 450, "mx": 520},
        "Pendidikan Guru Sekolah Dasar": {"mn": 490, "mx": 560},
        "Teknologi Pendidikan": {"mn": 450, "mx": 520},
        "Pendidikan Luar Sekolah": {"mn": 440, "mx": 510},
        "Seni Rupa": {"mn": 440, "mx": 510},
    },
    "Universitas Lampung": {
        "Pendidikan Dokter": {"mn": 640, "mx": 710},
        "Ilmu Keperawatan": {"mn": 520, "mx": 590},
        "Kesehatan Masyarakat": {"mn": 510, "mx": 580},
        "Farmasi": {"mn": 545, "mx": 615},
        "Teknik Sipil": {"mn": 550, "mx": 620},
        "Teknik Mesin": {"mn": 540, "mx": 610},
        "Teknik Elektro": {"mn": 560, "mx": 630},
        "Teknik Kimia": {"mn": 550, "mx": 620},
        "Teknik Informatika": {"mn": 580, "mx": 650},
        "Ilmu Komputer": {"mn": 570, "mx": 640},
        "Arsitektur": {"mn": 550, "mx": 620},
        "Matematika": {"mn": 500, "mx": 570},
        "Fisika": {"mn": 480, "mx": 550},
        "Kimia": {"mn": 490, "mx": 560},
        "Biologi": {"mn": 490, "mx": 560},
        "Ilmu Hukum": {"mn": 510, "mx": 580},
        "Ilmu Ekonomi": {"mn": 510, "mx": 580},
        "Akuntansi": {"mn": 530, "mx": 600},
        "Manajemen": {"mn": 540, "mx": 610},
        "Ilmu Komunikasi": {"mn": 520, "mx": 590},
        "Sosiologi": {"mn": 480, "mx": 550},
        "Ilmu Pemerintahan": {"mn": 490, "mx": 560},
        "Administrasi Negara": {"mn": 490, "mx": 560},
        "Hubungan Internasional": {"mn": 530, "mx": 600},
        "Psikologi": {"mn": 540, "mx": 610},
        "Sastra Indonesia": {"mn": 450, "mx": 520},
        "Sastra Inggris": {"mn": 490, "mx": 560},
        "Agribisnis": {"mn": 480, "mx": 550},
        "Agroteknologi": {"mn": 470, "mx": 540},
        "Peternakan": {"mn": 460, "mx": 530},
        "Kehutanan": {"mn": 460, "mx": 530},
        "Teknologi Pangan": {"mn": 490, "mx": 560},
        "Ilmu Kelautan": {"mn": 465, "mx": 535},
        "Perikanan": {"mn": 455, "mx": 525},
        "Ilmu Tanah": {"mn": 455, "mx": 525},
    },
    "Universitas Riau": {
        "Pendidikan Dokter": {"mn": 620, "mx": 690},
        "Ilmu Keperawatan": {"mn": 500, "mx": 570},
        "Kesehatan Masyarakat": {"mn": 490, "mx": 560},
        "Farmasi": {"mn": 545, "mx": 615},
        "Teknik Sipil": {"mn": 530, "mx": 600},
        "Teknik Mesin": {"mn": 520, "mx": 590},
        "Teknik Elektro": {"mn": 540, "mx": 610},
        "Teknik Kimia": {"mn": 530, "mx": 600},
        "Teknik Informatika": {"mn": 560, "mx": 630},
        "Sistem Informasi": {"mn": 540, "mx": 610},
        "Ilmu Komputer": {"mn": 550, "mx": 620},
        "Teknik Lingkungan": {"mn": 510, "mx": 580},
        "Teknik Perminyakan": {"mn": 540, "mx": 610},
        "Matematika": {"mn": 480, "mx": 550},
        "Fisika": {"mn": 460, "mx": 530},
        "Kimia": {"mn": 470, "mx": 540},
        "Biologi": {"mn": 470, "mx": 540},
        "Ilmu Hukum": {"mn": 490, "mx": 560},
        "Ilmu Ekonomi": {"mn": 490, "mx": 560},
        "Akuntansi": {"mn": 510, "mx": 580},
        "Manajemen": {"mn": 520, "mx": 590},
        "Ilmu Komunikasi": {"mn": 500, "mx": 570},
        "Sosiologi": {"mn": 460, "mx": 530},
        "Ilmu Pemerintahan": {"mn": 470, "mx": 540},
        "Administrasi Negara": {"mn": 460, "mx": 530},
        "Hubungan Internasional": {"mn": 500, "mx": 570},
        "Ilmu Politik": {"mn": 460, "mx": 530},
        "Psikologi": {"mn": 510, "mx": 580},
        "Sastra Indonesia": {"mn": 430, "mx": 500},
        "Sastra Inggris": {"mn": 460, "mx": 530},
        "Sastra Melayu": {"mn": 410, "mx": 480},
        "Agribisnis": {"mn": 450, "mx": 520},
        "Agroteknologi": {"mn": 440, "mx": 510},
        "Peternakan": {"mn": 430, "mx": 500},
        "Kehutanan": {"mn": 440, "mx": 510},
        "Ilmu Kelautan": {"mn": 450, "mx": 520},
        "Budidaya Perairan": {"mn": 430, "mx": 500},
        "Teknologi Pangan": {"mn": 470, "mx": 540},
        "Ilmu Tanah": {"mn": 430, "mx": 500},
    },
    "Universitas Jember": {
        "Pendidikan Dokter": {"mn": 640, "mx": 710},
        "Ilmu Keperawatan": {"mn": 510, "mx": 580},
        "Kesehatan Masyarakat": {"mn": 500, "mx": 570},
        "Kedokteran Gigi": {"mn": 600, "mx": 670},
        "Farmasi": {"mn": 560, "mx": 630},
        "Teknik Sipil": {"mn": 540, "mx": 610},
        "Teknik Mesin": {"mn": 530, "mx": 600},
        "Teknik Elektro": {"mn": 550, "mx": 620},
        "Teknik Kimia": {"mn": 540, "mx": 610},
        "Teknik Informatika": {"mn": 570, "mx": 640},
        "Sistem Informasi": {"mn": 550, "mx": 620},
        "Ilmu Komputer": {"mn": 555, "mx": 625},
        "Matematika": {"mn": 490, "mx": 560},
        "Fisika": {"mn": 470, "mx": 540},
        "Kimia": {"mn": 480, "mx": 550},
        "Biologi": {"mn": 480, "mx": 550},
        "Ilmu Hukum": {"mn": 500, "mx": 570},
        "Ilmu Ekonomi": {"mn": 500, "mx": 570},
        "Akuntansi": {"mn": 520, "mx": 590},
        "Manajemen": {"mn": 530, "mx": 600},
        "Ilmu Komunikasi": {"mn": 510, "mx": 580},
        "Sosiologi": {"mn": 470, "mx": 540},
        "Ilmu Pemerintahan": {"mn": 470, "mx": 540},
        "Administrasi Bisnis": {"mn": 490, "mx": 560},
        "Hubungan Internasional": {"mn": 510, "mx": 580},
        "Ilmu Politik": {"mn": 470, "mx": 540},
        "Psikologi": {"mn": 520, "mx": 590},
        "Sastra Indonesia": {"mn": 440, "mx": 510},
        "Sastra Inggris": {"mn": 470, "mx": 540},
        "Sejarah": {"mn": 440, "mx": 510},
        "Agribisnis": {"mn": 460, "mx": 530},
        "Agroteknologi": {"mn": 450, "mx": 520},
        "Peternakan": {"mn": 440, "mx": 510},
        "Kehutanan": {"mn": 440, "mx": 510},
        "Teknologi Pangan": {"mn": 480, "mx": 550},
        "Ilmu Kelautan": {"mn": 460, "mx": 530},
        "Budidaya Perairan": {"mn": 450, "mx": 520},
        "Ilmu Tanah": {"mn": 440, "mx": 510},
    },
    "Universitas Mulawarman": {
        "Pendidikan Dokter": {"mn": 590, "mx": 660},
        "Ilmu Keperawatan": {"mn": 470, "mx": 540},
        "Kesehatan Masyarakat": {"mn": 460, "mx": 530},
        "Farmasi": {"mn": 520, "mx": 590},
        "Teknik Sipil": {"mn": 490, "mx": 560},
        "Teknik Mesin": {"mn": 480, "mx": 550},
        "Teknik Elektro": {"mn": 500, "mx": 570},
        "Teknik Kimia": {"mn": 490, "mx": 560},
        "Teknik Informatika": {"mn": 520, "mx": 590},
        "Ilmu Komputer": {"mn": 510, "mx": 580},
        "Teknik Pertambangan": {"mn": 490, "mx": 560},
        "Teknik Geologi": {"mn": 490, "mx": 560},
        "Teknik Perminyakan": {"mn": 510, "mx": 580},
        "Arsitektur": {"mn": 490, "mx": 560},
        "Teknik Lingkungan": {"mn": 470, "mx": 540},
        "Matematika": {"mn": 440, "mx": 510},
        "Fisika": {"mn": 420, "mx": 490},
        "Kimia": {"mn": 430, "mx": 500},
        "Biologi": {"mn": 430, "mx": 500},
        "Ilmu Hukum": {"mn": 450, "mx": 520},
        "Ilmu Ekonomi": {"mn": 450, "mx": 520},
        "Akuntansi": {"mn": 470, "mx": 540},
        "Manajemen": {"mn": 480, "mx": 550},
        "Ilmu Komunikasi": {"mn": 460, "mx": 530},
        "Sosiologi": {"mn": 420, "mx": 490},
        "Ilmu Pemerintahan": {"mn": 430, "mx": 500},
        "Administrasi Bisnis": {"mn": 440, "mx": 510},
        "Administrasi Negara": {"mn": 435, "mx": 505},
        "Sastra Indonesia": {"mn": 405, "mx": 475},
        "Sastra Inggris": {"mn": 430, "mx": 500},
        "Agribisnis": {"mn": 415, "mx": 485},
        "Agroteknologi": {"mn": 410, "mx": 480},
        "Peternakan": {"mn": 405, "mx": 475},
        "Kehutanan": {"mn": 415, "mx": 485},
        "Ilmu Kelautan": {"mn": 415, "mx": 485},
        "Budidaya Perairan": {"mn": 410, "mx": 480},
        "Teknologi Pangan": {"mn": 435, "mx": 505},
        "Ilmu Tanah": {"mn": 405, "mx": 475},
    },
    "Universitas Syiah Kuala": {
        "Pendidikan Dokter": {"mn": 650, "mx": 720},
        "Ilmu Keperawatan": {"mn": 530, "mx": 600},
        "Kesehatan Masyarakat": {"mn": 520, "mx": 590},
        "Kedokteran Gigi": {"mn": 600, "mx": 670},
        "Farmasi": {"mn": 560, "mx": 630},
        "Kedokteran Hewan": {"mn": 560, "mx": 630},
        "Teknik Sipil": {"mn": 550, "mx": 620},
        "Teknik Mesin": {"mn": 540, "mx": 610},
        "Teknik Elektro": {"mn": 560, "mx": 630},
        "Teknik Kimia": {"mn": 550, "mx": 620},
        "Teknik Informatika": {"mn": 580, "mx": 650},
        "Arsitektur": {"mn": 560, "mx": 630},
        "Teknik Geologi": {"mn": 540, "mx": 610},
        "Teknik Industri": {"mn": 545, "mx": 615},
        "Matematika": {"mn": 490, "mx": 560},
        "Fisika": {"mn": 470, "mx": 540},
        "Kimia": {"mn": 480, "mx": 550},
        "Biologi": {"mn": 480, "mx": 550},
        "Ilmu Hukum": {"mn": 500, "mx": 570},
        "Ilmu Ekonomi": {"mn": 500, "mx": 570},
        "Akuntansi": {"mn": 520, "mx": 590},
        "Manajemen": {"mn": 530, "mx": 600},
        "Ilmu Komunikasi": {"mn": 510, "mx": 580},
        "Sosiologi": {"mn": 470, "mx": 540},
        "Ilmu Pemerintahan": {"mn": 480, "mx": 550},
        "Administrasi Negara": {"mn": 480, "mx": 550},
        "Hubungan Internasional": {"mn": 510, "mx": 580},
        "Ilmu Politik": {"mn": 475, "mx": 545},
        "Psikologi": {"mn": 530, "mx": 600},
        "Sastra Indonesia": {"mn": 440, "mx": 510},
        "Sastra Inggris": {"mn": 470, "mx": 540},
        "Sastra Arab": {"mn": 450, "mx": 520},
        "Agribisnis": {"mn": 460, "mx": 530},
        "Agroteknologi": {"mn": 450, "mx": 520},
        "Peternakan": {"mn": 440, "mx": 510},
        "Kehutanan": {"mn": 440, "mx": 510},
        "Teknologi Pangan": {"mn": 470, "mx": 540},
        "Ilmu Kelautan": {"mn": 460, "mx": 530},
        "Budidaya Perairan": {"mn": 445, "mx": 515},
    },
    "Universitas Negeri Jakarta": {
        "Pendidikan Matematika": {"mn": 560, "mx": 630},
        "Pendidikan Biologi": {"mn": 540, "mx": 610},
        "Pendidikan Kimia": {"mn": 540, "mx": 610},
        "Pendidikan Fisika": {"mn": 540, "mx": 610},
        "Matematika": {"mn": 540, "mx": 610},
        "Biologi": {"mn": 520, "mx": 590},
        "Kimia": {"mn": 520, "mx": 590},
        "Fisika": {"mn": 520, "mx": 590},
        "Ilmu Komputer": {"mn": 570, "mx": 640},
        "Teknik Informatika": {"mn": 580, "mx": 650},
        "Teknik Elektro": {"mn": 540, "mx": 610},
        "Teknik Mesin": {"mn": 530, "mx": 600},
        "Teknik Sipil": {"mn": 530, "mx": 600},
        "Pendidikan Bahasa Inggris": {"mn": 570, "mx": 640},
        "Pendidikan Bahasa Indonesia": {"mn": 530, "mx": 600},
        "Pendidikan Bahasa Jerman": {"mn": 500, "mx": 570},
        "Pendidikan Bahasa Perancis": {"mn": 500, "mx": 570},
        "Pendidikan Bahasa Arab": {"mn": 495, "mx": 565},
        "Pendidikan Ekonomi": {"mn": 530, "mx": 600},
        "Manajemen": {"mn": 560, "mx": 630},
        "Akuntansi": {"mn": 560, "mx": 630},
        "Pendidikan Akuntansi": {"mn": 520, "mx": 590},
        "Pendidikan Sejarah": {"mn": 490, "mx": 560},
        "Pendidikan Sosiologi": {"mn": 490, "mx": 560},
        "Pendidikan Geografi": {"mn": 490, "mx": 560},
        "Sosiologi": {"mn": 500, "mx": 570},
        "Ilmu Komunikasi": {"mn": 560, "mx": 630},
        "Psikologi": {"mn": 575, "mx": 645},
        "Ilmu Keolahragaan": {"mn": 460, "mx": 530},
        "Pendidikan Jasmani Kesehatan dan Rekreasi": {"mn": 450, "mx": 520},
        "Pendidikan Kepelatihan Olahraga": {"mn": 445, "mx": 515},
        "Pendidikan Luar Biasa": {"mn": 470, "mx": 540},
        "Pendidikan Guru Sekolah Dasar": {"mn": 490, "mx": 560},
        "Bimbingan dan Konseling": {"mn": 470, "mx": 540},
        "Administrasi Pendidikan": {"mn": 470, "mx": 540},
        "Teknologi Pendidikan": {"mn": 470, "mx": 540},
        "Pendidikan Seni Rupa": {"mn": 445, "mx": 515},
        "Pendidikan Seni Musik": {"mn": 445, "mx": 515},
        "Desain Komunikasi Visual": {"mn": 555, "mx": 625},
        "Pendidikan Vokasional Teknik Elektronika": {"mn": 500, "mx": 570},
        "Pendidikan Vokasional Konstruksi Bangunan": {"mn": 490, "mx": 560},
    },
    "Universitas Negeri Makassar": {
        "Pendidikan Matematika": {"mn": 530, "mx": 600},
        "Pendidikan Biologi": {"mn": 510, "mx": 580},
        "Pendidikan Kimia": {"mn": 510, "mx": 580},
        "Pendidikan Fisika": {"mn": 510, "mx": 580},
        "Matematika": {"mn": 510, "mx": 580},
        "Biologi": {"mn": 490, "mx": 560},
        "Kimia": {"mn": 490, "mx": 560},
        "Fisika": {"mn": 490, "mx": 560},
        "Ilmu Komputer": {"mn": 540, "mx": 610},
        "Teknik Informatika": {"mn": 550, "mx": 620},
        "Teknik Elektro": {"mn": 510, "mx": 580},
        "Teknik Mesin": {"mn": 500, "mx": 570},
        "Teknik Sipil": {"mn": 510, "mx": 580},
        "Arsitektur": {"mn": 520, "mx": 590},
        "Pendidikan Bahasa Inggris": {"mn": 540, "mx": 610},
        "Pendidikan Bahasa Indonesia": {"mn": 500, "mx": 570},
        "Pendidikan Bahasa Arab": {"mn": 480, "mx": 550},
        "Pendidikan Ekonomi": {"mn": 500, "mx": 570},
        "Manajemen": {"mn": 530, "mx": 600},
        "Akuntansi": {"mn": 530, "mx": 600},
        "Pendidikan Akuntansi": {"mn": 490, "mx": 560},
        "Ilmu Ekonomi": {"mn": 510, "mx": 580},
        "Administrasi Bisnis": {"mn": 490, "mx": 560},
        "Administrasi Negara": {"mn": 485, "mx": 555},
        "Pendidikan Sejarah": {"mn": 460, "mx": 530},
        "Pendidikan Sosiologi": {"mn": 460, "mx": 530},
        "Pendidikan Geografi": {"mn": 460, "mx": 530},
        "Sosiologi": {"mn": 470, "mx": 540},
        "Ilmu Komunikasi": {"mn": 520, "mx": 590},
        "Psikologi": {"mn": 540, "mx": 610},
        "Ilmu Keolahragaan": {"mn": 440, "mx": 510},
        "Pendidikan Jasmani Kesehatan dan Rekreasi": {"mn": 430, "mx": 500},
        "Pendidikan Luar Biasa": {"mn": 440, "mx": 510},
        "Pendidikan Guru Sekolah Dasar": {"mn": 460, "mx": 530},
        "Bimbingan dan Konseling": {"mn": 440, "mx": 510},
        "Teknologi Pendidikan": {"mn": 440, "mx": 510},
        "Pendidikan Seni Rupa": {"mn": 420, "mx": 490},
        "Seni Rupa": {"mn": 420, "mx": 490},
        "Pendidikan Teknik Otomotif": {"mn": 460, "mx": 530},
        "Pendidikan Teknik Bangunan": {"mn": 455, "mx": 525},
    },
    "Universitas Tanjungpura": {
        "Pendidikan Dokter": {"mn": 610, "mx": 680},
        "Ilmu Keperawatan": {"mn": 490, "mx": 560},
        "Kesehatan Masyarakat": {"mn": 480, "mx": 550},
        "Farmasi": {"mn": 530, "mx": 600},
        "Teknik Sipil": {"mn": 510, "mx": 580},
        "Teknik Mesin": {"mn": 500, "mx": 570},
        "Teknik Elektro": {"mn": 520, "mx": 590},
        "Teknik Kimia": {"mn": 510, "mx": 580},
        "Teknik Informatika": {"mn": 540, "mx": 610},
        "Ilmu Komputer": {"mn": 530, "mx": 600},
        "Teknik Lingkungan": {"mn": 495, "mx": 565},
        "Arsitektur": {"mn": 510, "mx": 580},
        "Teknik Pertambangan": {"mn": 495, "mx": 565},
        "Matematika": {"mn": 460, "mx": 530},
        "Fisika": {"mn": 440, "mx": 510},
        "Kimia": {"mn": 450, "mx": 520},
        "Biologi": {"mn": 450, "mx": 520},
        "Statistika": {"mn": 470, "mx": 540},
        "Ilmu Hukum": {"mn": 470, "mx": 540},
        "Ilmu Ekonomi": {"mn": 470, "mx": 540},
        "Akuntansi": {"mn": 490, "mx": 560},
        "Manajemen": {"mn": 500, "mx": 570},
        "Ilmu Komunikasi": {"mn": 480, "mx": 550},
        "Sosiologi": {"mn": 440, "mx": 510},
        "Ilmu Pemerintahan": {"mn": 445, "mx": 515},
        "Administrasi Publik": {"mn": 445, "mx": 515},
        "Ilmu Politik": {"mn": 440, "mx": 510},
        "Hubungan Internasional": {"mn": 475, "mx": 545},
        "Psikologi": {"mn": 500, "mx": 570},
        "Sastra Indonesia": {"mn": 415, "mx": 485},
        "Sastra Inggris": {"mn": 445, "mx": 515},
        "Sejarah": {"mn": 415, "mx": 485},
        "Agribisnis": {"mn": 430, "mx": 500},
        "Agroteknologi": {"mn": 420, "mx": 490},
        "Peternakan": {"mn": 410, "mx": 480},
        "Kehutanan": {"mn": 420, "mx": 490},
        "Ilmu Kelautan": {"mn": 430, "mx": 500},
        "Budidaya Perairan": {"mn": 415, "mx": 485},
        "Teknologi Pangan": {"mn": 445, "mx": 515},
    },
    "Universitas Mataram": {
        "Pendidikan Dokter": {"mn": 630, "mx": 700},
        "Ilmu Keperawatan": {"mn": 500, "mx": 570},
        "Kesehatan Masyarakat": {"mn": 490, "mx": 560},
        "Kedokteran Gigi": {"mn": 580, "mx": 650},
        "Farmasi": {"mn": 540, "mx": 610},
        "Teknik Sipil": {"mn": 520, "mx": 590},
        "Teknik Mesin": {"mn": 510, "mx": 580},
        "Teknik Elektro": {"mn": 530, "mx": 600},
        "Teknik Informatika": {"mn": 550, "mx": 620},
        "Sistem Informasi": {"mn": 530, "mx": 600},
        "Teknik Pertambangan": {"mn": 500, "mx": 570},
        "Teknik Lingkungan": {"mn": 495, "mx": 565},
        "Arsitektur": {"mn": 515, "mx": 585},
        "Matematika": {"mn": 470, "mx": 540},
        "Fisika": {"mn": 450, "mx": 520},
        "Kimia": {"mn": 460, "mx": 530},
        "Biologi": {"mn": 460, "mx": 530},
        "Ilmu Hukum": {"mn": 480, "mx": 550},
        "Ilmu Ekonomi": {"mn": 480, "mx": 550},
        "Akuntansi": {"mn": 500, "mx": 570},
        "Manajemen": {"mn": 510, "mx": 580},
        "Ilmu Komunikasi": {"mn": 490, "mx": 560},
        "Sosiologi": {"mn": 450, "mx": 520},
        "Ilmu Pemerintahan": {"mn": 455, "mx": 525},
        "Administrasi Negara": {"mn": 455, "mx": 525},
        "Hubungan Internasional": {"mn": 480, "mx": 550},
        "Ilmu Politik": {"mn": 450, "mx": 520},
        "Psikologi": {"mn": 510, "mx": 580},
        "Sastra Indonesia": {"mn": 425, "mx": 495},
        "Sastra Inggris": {"mn": 455, "mx": 525},
        "Sastra Arab": {"mn": 430, "mx": 500},
        "Agribisnis": {"mn": 440, "mx": 510},
        "Agroteknologi": {"mn": 430, "mx": 500},
        "Peternakan": {"mn": 420, "mx": 490},
        "Kehutanan": {"mn": 425, "mx": 495},
        "Ilmu Kelautan": {"mn": 435, "mx": 505},
        "Budidaya Perairan": {"mn": 425, "mx": 495},
        "Teknologi Pangan": {"mn": 455, "mx": 525},
        "Ilmu Tanah": {"mn": 420, "mx": 490},
        "Pariwisata": {"mn": 480, "mx": 550},
    },
    "Universitas Bengkulu": {
        "Pendidikan Dokter": {"mn": 600, "mx": 670},
        "Ilmu Keperawatan": {"mn": 480, "mx": 550},
        "Kesehatan Masyarakat": {"mn": 470, "mx": 540},
        "Farmasi": {"mn": 510, "mx": 580},
        "Teknik Sipil": {"mn": 495, "mx": 565},
        "Teknik Mesin": {"mn": 485, "mx": 555},
        "Teknik Elektro": {"mn": 505, "mx": 575},
        "Teknik Informatika": {"mn": 525, "mx": 595},
        "Ilmu Komputer": {"mn": 515, "mx": 585},
        "Teknik Kimia": {"mn": 490, "mx": 560},
        "Teknik Lingkungan": {"mn": 475, "mx": 545},
        "Matematika": {"mn": 445, "mx": 515},
        "Fisika": {"mn": 425, "mx": 495},
        "Kimia": {"mn": 435, "mx": 505},
        "Biologi": {"mn": 435, "mx": 505},
        "Ilmu Hukum": {"mn": 455, "mx": 525},
        "Ilmu Ekonomi": {"mn": 455, "mx": 525},
        "Akuntansi": {"mn": 475, "mx": 545},
        "Manajemen": {"mn": 485, "mx": 555},
        "Ilmu Komunikasi": {"mn": 465, "mx": 535},
        "Sosiologi": {"mn": 425, "mx": 495},
        "Ilmu Pemerintahan": {"mn": 430, "mx": 500},
        "Administrasi Negara": {"mn": 430, "mx": 500},
        "Ilmu Politik": {"mn": 425, "mx": 495},
        "Hubungan Internasional": {"mn": 455, "mx": 525},
        "Psikologi": {"mn": 485, "mx": 555},
        "Sastra Indonesia": {"mn": 400, "mx": 470},
        "Sastra Inggris": {"mn": 430, "mx": 500},
        "Sejarah": {"mn": 400, "mx": 470},
        "Agribisnis": {"mn": 415, "mx": 485},
        "Agroteknologi": {"mn": 405, "mx": 475},
        "Peternakan": {"mn": 400, "mx": 470},
        "Kehutanan": {"mn": 410, "mx": 480},
        "Ilmu Kelautan": {"mn": 415, "mx": 485},
        "Budidaya Perairan": {"mn": 405, "mx": 475},
        "Teknologi Pangan": {"mn": 430, "mx": 500},
        "Ilmu Tanah": {"mn": 400, "mx": 470},
    },
    "Universitas Sam Ratulangi": {
        "Pendidikan Dokter": {"mn": 640, "mx": 710},
        "Ilmu Keperawatan": {"mn": 520, "mx": 590},
        "Kesehatan Masyarakat": {"mn": 510, "mx": 580},
        "Kedokteran Gigi": {"mn": 590, "mx": 660},
        "Farmasi": {"mn": 550, "mx": 620},
        "Kedokteran Hewan": {"mn": 545, "mx": 615},
        "Teknik Sipil": {"mn": 540, "mx": 610},
        "Teknik Mesin": {"mn": 530, "mx": 600},
        "Teknik Elektro": {"mn": 550, "mx": 620},
        "Teknik Informatika": {"mn": 570, "mx": 640},
        "Arsitektur": {"mn": 550, "mx": 620},
        "Teknik Lingkungan": {"mn": 520, "mx": 590},
        "Matematika": {"mn": 480, "mx": 550},
        "Fisika": {"mn": 460, "mx": 530},
        "Kimia": {"mn": 470, "mx": 540},
        "Biologi": {"mn": 470, "mx": 540},
        "Ilmu Hukum": {"mn": 490, "mx": 560},
        "Ilmu Ekonomi": {"mn": 490, "mx": 560},
        "Akuntansi": {"mn": 510, "mx": 580},
        "Manajemen": {"mn": 520, "mx": 590},
        "Ilmu Komunikasi": {"mn": 500, "mx": 570},
        "Sosiologi": {"mn": 460, "mx": 530},
        "Ilmu Pemerintahan": {"mn": 460, "mx": 530},
        "Administrasi Bisnis": {"mn": 470, "mx": 540},
        "Hubungan Internasional": {"mn": 490, "mx": 560},
        "Ilmu Politik": {"mn": 460, "mx": 530},
        "Psikologi": {"mn": 510, "mx": 580},
        "Sastra Indonesia": {"mn": 430, "mx": 500},
        "Sastra Inggris": {"mn": 460, "mx": 530},
        "Agribisnis": {"mn": 440, "mx": 510},
        "Agroteknologi": {"mn": 430, "mx": 500},
        "Peternakan": {"mn": 420, "mx": 490},
        "Ilmu Kelautan": {"mn": 440, "mx": 510},
        "Budidaya Perairan": {"mn": 430, "mx": 500},
        "Teknologi Pangan": {"mn": 450, "mx": 520},
        "Kehutanan": {"mn": 430, "mx": 500},
    },
}

@st.cache_data(ttl=3600)
def load_database():
    import io
    def read_xlsx(source):
        return pd.read_excel(source, sheet_name=None, engine="openpyxl")
    def load_file(local_path, url):
        if os.path.exists(local_path):
            try:
                return read_xlsx(local_path), None
            except:
                pass
        try:
            import urllib.request
            with urllib.request.urlopen(url, timeout=20) as resp:
                data = resp.read()
            return read_xlsx(io.BytesIO(data)), None
        except Exception as e:
            return None, str(e)

    # ── S1: gunakan database akurat per kampus (menggantikan Excel yg semua PTN sama) ──
    ptn_s1 = {k: {p: dict(v) for p, v in vv.items()} for k, vv in PTN_PRODI_S1.items()}

    # D3/D4: gunakan database akurat per kampus (Excel juga semua PTN sama persis)
    ptn_d3 = {k: {p: dict(v) for p, v in vv.items()} for k, vv in PTN_PRODI_D3.items()}
    ptn_d4 = {k: {p: dict(v) for p, v in vv.items()} for k, vv in PTN_PRODI_D4.items()}

    # df_s1 dummy agar kode lain yang referens df_s1 tidak error
    df_s1 = pd.DataFrame(
        [{"No": str(i+1), "Prodi": p, "Kelompok": "-", "PTN": ptn,
          "Rank": "-", "NilaiAman": str(v["mn"]), "Rentang": f"{v['mn']}-{v['mx']}", "Catatan": ""}
         for i, (ptn, pd_map) in enumerate(PTN_PRODI_S1.items())
         for p, v in pd_map.items()]
    )

    return ptn_s1, ptn_d3, ptn_d4, df_s1, None

_PTN_S1, _PTN_D3, _PTN_D4, _DF_S1, _DB_ERR = load_database()

def get_db(jenjang="S1 (Sarjana)"):
    if "D4" in jenjang:
        return _PTN_D4 or {}
    elif "D3" in jenjang:
        return _PTN_D3 or {}
    return _PTN_S1 or {}

def get_daftar_ptn(jenjang="S1 (Sarjana)"):
    db = get_db(jenjang)
    return sorted(db.keys())

def get_daftar_prodi(ptn, jenjang="S1 (Sarjana)"):
    db = get_db(jenjang)
    return sorted(db.get(ptn, {}).keys())

def get_skor_info(ptn, prodi, jenjang="S1 (Sarjana)"):
    db = get_db(jenjang)
    ptn_data = db.get(ptn, {})
    data = ptn_data.get(prodi, None)
    if data is None:
        return {"mn": 600, "mx": 670}
    return data

# ══════════════════════════════════════════════════════════
# KATEGORI SKOR — 4 Level
# ══════════════════════════════════════════════════════════
def get_kategori_skor(sw, mn, mx):
    if sw >= mx:
        return ("Sangat Aman",  "#148a42", "badge-sa", "🏆",
                min(95.0, 80 + (sw - mx) / max(mx, 1) * 15))
    elif sw >= mn:
        return ("Aman",         "#1a5fa0", "badge-a",  "✅",
                60 + (sw - mn) / max(mx - mn, 1) * 18)
    elif sw >= mn - 70:
        gap = sw - mn
        return ("Berisiko",     "#e67e22", "badge-br", "⚡",
                max(20, 35 + gap / 70 * 20))
    else:
        return ("Tidak Aman",   "#c0392b", "badge-na", "🔴",
                max(5, 18 + (sw - (mn - 140)) / 70 * 12))

# ══════════════════════════════════════════════════════════
# BOBOT PER JURUSAN
# ══════════════════════════════════════════════════════════
BOBOT_KEYWORD = {
    "Teknik Informatika":    {"PU":.20,"PPU":.05,"PBM":.05,"PK":.20,"LBI":.05,"LBE":.10,"PM":.35},
    "Rekayasa Perangkat Lunak":{"PU":.20,"PPU":.05,"PBM":.05,"PK":.20,"LBI":.05,"LBE":.10,"PM":.35},
    "Teknologi Informasi":   {"PU":.20,"PPU":.05,"PBM":.05,"PK":.20,"LBI":.05,"LBE":.10,"PM":.35},
    "Ilmu Komputer":         {"PU":.20,"PPU":.05,"PBM":.05,"PK":.20,"LBI":.05,"LBE":.10,"PM":.35},
    "Teknik Komputer":       {"PU":.20,"PPU":.05,"PBM":.05,"PK":.20,"LBI":.05,"LBE":.10,"PM":.35},
    "Teknik Sipil":          {"PU":.20,"PPU":.05,"PBM":.05,"PK":.20,"LBI":.05,"LBE":.10,"PM":.35},
    "Teknik Mesin":          {"PU":.20,"PPU":.05,"PBM":.05,"PK":.20,"LBI":.05,"LBE":.10,"PM":.35},
    "Teknik Elektro":        {"PU":.20,"PPU":.05,"PBM":.05,"PK":.20,"LBI":.05,"LBE":.10,"PM":.35},
    "Teknik Industri":       {"PU":.20,"PPU":.05,"PBM":.05,"PK":.20,"LBI":.05,"LBE":.10,"PM":.35},
    "Teknik Kimia":          {"PU":.18,"PPU":.08,"PBM":.05,"PK":.20,"LBI":.05,"LBE":.07,"PM":.37},
    "Mekatronika":           {"PU":.19,"PPU":.06,"PBM":.05,"PK":.20,"LBI":.05,"LBE":.08,"PM":.37},
    "Matematika":            {"PU":.15,"PPU":.05,"PBM":.05,"PK":.20,"LBI":.05,"LBE":.05,"PM":.45},
    "Fisika":                {"PU":.18,"PPU":.07,"PBM":.05,"PK":.20,"LBI":.05,"LBE":.05,"PM":.40},
    "Kimia":                 {"PU":.18,"PPU":.10,"PBM":.07,"PK":.18,"LBI":.07,"LBE":.05,"PM":.35},
    "Biologi":               {"PU":.20,"PPU":.15,"PBM":.10,"PK":.15,"LBI":.10,"LBE":.08,"PM":.22},
    "Statistika":            {"PU":.15,"PPU":.07,"PBM":.05,"PK":.20,"LBI":.05,"LBE":.05,"PM":.43},
    "Aktuaria":              {"PU":.15,"PPU":.07,"PBM":.05,"PK":.20,"LBI":.05,"LBE":.05,"PM":.43},
    "Bioteknologi":          {"PU":.20,"PPU":.15,"PBM":.10,"PK":.15,"LBI":.10,"LBE":.08,"PM":.22},
    "Arsitektur":            {"PU":.20,"PPU":.10,"PBM":.10,"PK":.18,"LBI":.10,"LBE":.10,"PM":.22},
    "Teknik Lingkungan":     {"PU":.20,"PPU":.10,"PBM":.07,"PK":.18,"LBI":.07,"LBE":.08,"PM":.30},
    "Teknik Geologi":        {"PU":.20,"PPU":.10,"PBM":.07,"PK":.18,"LBI":.07,"LBE":.08,"PM":.30},
    "Teknik Perminyakan":    {"PU":.20,"PPU":.10,"PBM":.07,"PK":.18,"LBI":.07,"LBE":.08,"PM":.30},
    "Teknik Perkapalan":     {"PU":.20,"PPU":.07,"PBM":.05,"PK":.20,"LBI":.05,"LBE":.08,"PM":.35},
    "Teknik Geodesi":        {"PU":.20,"PPU":.08,"PBM":.07,"PK":.18,"LBI":.07,"LBE":.08,"PM":.32},
    "Teknik Otomotif":       {"PU":.20,"PPU":.07,"PBM":.05,"PK":.20,"LBI":.05,"LBE":.08,"PM":.35},
    "Teknik Elektronika":    {"PU":.20,"PPU":.06,"PBM":.05,"PK":.20,"LBI":.05,"LBE":.08,"PM":.36},
    "Rekayasa Kimia":        {"PU":.18,"PPU":.08,"PBM":.05,"PK":.20,"LBI":.05,"LBE":.07,"PM":.37},
    "Teknologi Pangan":      {"PU":.18,"PPU":.12,"PBM":.08,"PK":.18,"LBI":.10,"LBE":.07,"PM":.27},
    "Analisis Kimia":        {"PU":.18,"PPU":.12,"PBM":.08,"PK":.18,"LBI":.08,"LBE":.07,"PM":.29},
    "Manufaktur":            {"PU":.20,"PPU":.07,"PBM":.05,"PK":.20,"LBI":.05,"LBE":.08,"PM":.35},
    "Geomatika":             {"PU":.20,"PPU":.08,"PBM":.07,"PK":.18,"LBI":.07,"LBE":.08,"PM":.32},
    "Geofisika":             {"PU":.18,"PPU":.08,"PBM":.06,"PK":.20,"LBI":.06,"LBE":.07,"PM":.35},
    "Penginderaan Jauh":     {"PU":.18,"PPU":.10,"PBM":.08,"PK":.18,"LBI":.08,"LBE":.08,"PM":.30},
    "Logistik":              {"PU":.20,"PPU":.12,"PBM":.14,"PK":.16,"LBI":.14,"LBE":.10,"PM":.14},
    "Supply Chain":          {"PU":.20,"PPU":.12,"PBM":.14,"PK":.16,"LBI":.14,"LBE":.10,"PM":.14},
    "Kedokteran":            {"PU":.20,"PPU":.15,"PBM":.10,"PK":.15,"LBI":.10,"LBE":.10,"PM":.20},
    "Kedokteran Gigi":       {"PU":.20,"PPU":.15,"PBM":.10,"PK":.15,"LBI":.10,"LBE":.10,"PM":.20},
    "Farmasi":               {"PU":.18,"PPU":.12,"PBM":.08,"PK":.18,"LBI":.08,"LBE":.08,"PM":.28},
    "Gizi":                  {"PU":.18,"PPU":.13,"PBM":.10,"PK":.15,"LBI":.13,"LBE":.08,"PM":.23},
    "Gizi Klinik":           {"PU":.18,"PPU":.13,"PBM":.10,"PK":.15,"LBI":.13,"LBE":.08,"PM":.23},
    "Keperawatan":           {"PU":.18,"PPU":.12,"PBM":.12,"PK":.12,"LBI":.15,"LBE":.08,"PM":.23},
    "Kesehatan Masyarakat":  {"PU":.20,"PPU":.12,"PBM":.12,"PK":.12,"LBI":.15,"LBE":.08,"PM":.21},
    "Fisioterapi":           {"PU":.19,"PPU":.13,"PBM":.12,"PK":.13,"LBI":.15,"LBE":.08,"PM":.20},
    "Kebidanan":             {"PU":.18,"PPU":.14,"PBM":.13,"PK":.12,"LBI":.17,"LBE":.08,"PM":.18},
    "Radiologi":             {"PU":.18,"PPU":.12,"PBM":.08,"PK":.20,"LBI":.10,"LBE":.07,"PM":.25},
    "Rekam Medis":           {"PU":.18,"PPU":.12,"PBM":.14,"PK":.15,"LBI":.16,"LBE":.08,"PM":.17},
    "Analis Kesehatan":      {"PU":.18,"PPU":.13,"PBM":.08,"PK":.18,"LBI":.10,"LBE":.07,"PM":.26},
    "Laboratorium Medis":    {"PU":.18,"PPU":.13,"PBM":.08,"PK":.18,"LBI":.10,"LBE":.07,"PM":.26},
    "Keselamatan Kesehatan": {"PU":.20,"PPU":.13,"PBM":.12,"PK":.12,"LBI":.14,"LBE":.10,"PM":.19},
    "Ekonomi":               {"PU":.20,"PPU":.15,"PBM":.10,"PK":.20,"LBI":.10,"LBE":.10,"PM":.15},
    "Manajemen":             {"PU":.20,"PPU":.15,"PBM":.12,"PK":.18,"LBI":.12,"LBE":.10,"PM":.13},
    "Akuntansi":             {"PU":.18,"PPU":.15,"PBM":.10,"PK":.22,"LBI":.10,"LBE":.10,"PM":.15},
    "Bisnis":                {"PU":.20,"PPU":.15,"PBM":.12,"PK":.18,"LBI":.12,"LBE":.10,"PM":.13},
    "Perpajakan":            {"PU":.18,"PPU":.14,"PBM":.12,"PK":.22,"LBI":.12,"LBE":.08,"PM":.14},
    "Keuangan":              {"PU":.18,"PPU":.13,"PBM":.12,"PK":.22,"LBI":.12,"LBE":.08,"PM":.15},
    "Perbankan":             {"PU":.18,"PPU":.13,"PBM":.12,"PK":.22,"LBI":.12,"LBE":.08,"PM":.15},
    "Manajemen Pemasaran":   {"PU":.20,"PPU":.14,"PBM":.17,"PK":.12,"LBI":.18,"LBE":.12,"PM":.07},
    "Administrasi Bisnis":   {"PU":.20,"PPU":.15,"PBM":.18,"PK":.12,"LBI":.18,"LBE":.10,"PM":.07},
    "Penilaian Properti":    {"PU":.20,"PPU":.13,"PBM":.12,"PK":.18,"LBI":.12,"LBE":.10,"PM":.15},
    "Pariwisata":            {"PU":.18,"PPU":.13,"PBM":.18,"PK":.08,"LBI":.18,"LBE":.18,"PM":.07},
    "Perhotelan":            {"PU":.18,"PPU":.12,"PBM":.17,"PK":.08,"LBI":.18,"LBE":.20,"PM":.07},
    "Perjalanan Wisata":     {"PU":.18,"PPU":.12,"PBM":.17,"PK":.08,"LBI":.18,"LBE":.20,"PM":.07},
    "Ilmu Hukum":            {"PU":.22,"PPU":.18,"PBM":.20,"PK":.08,"LBI":.18,"LBE":.10,"PM":.04},
    "Psikologi":             {"PU":.22,"PPU":.15,"PBM":.18,"PK":.10,"LBI":.18,"LBE":.10,"PM":.07},
    "Ilmu Komunikasi":       {"PU":.20,"PPU":.15,"PBM":.22,"PK":.08,"LBI":.20,"LBE":.10,"PM":.05},
    "Hubungan Masyarakat":   {"PU":.20,"PPU":.15,"PBM":.22,"PK":.07,"LBI":.22,"LBE":.10,"PM":.04},
    "Hubungan Internasional":{"PU":.20,"PPU":.15,"PBM":.15,"PK":.08,"LBI":.17,"LBE":.20,"PM":.05},
    "Administrasi Publik":   {"PU":.22,"PPU":.15,"PBM":.18,"PK":.08,"LBI":.20,"LBE":.10,"PM":.07},
    "Sosiologi":             {"PU":.22,"PPU":.17,"PBM":.18,"PK":.08,"LBI":.18,"LBE":.10,"PM":.07},
    "Ilmu Politik":          {"PU":.22,"PPU":.17,"PBM":.18,"PK":.08,"LBI":.18,"LBE":.10,"PM":.07},
    "Sejarah":               {"PU":.20,"PPU":.20,"PBM":.18,"PK":.05,"LBI":.22,"LBE":.10,"PM":.05},
    "Geografi":              {"PU":.20,"PPU":.15,"PBM":.15,"PK":.12,"LBI":.15,"LBE":.08,"PM":.15},
    "Komunikasi":            {"PU":.20,"PPU":.15,"PBM":.22,"PK":.08,"LBI":.20,"LBE":.10,"PM":.05},
    "Sastra Inggris":        {"PU":.12,"PPU":.12,"PBM":.20,"PK":.05,"LBI":.15,"LBE":.31,"PM":.05},
    "Bahasa Inggris":        {"PU":.12,"PPU":.12,"PBM":.18,"PK":.05,"LBI":.12,"LBE":.33,"PM":.08},
    "Bahasa Indonesia":      {"PU":.12,"PPU":.12,"PBM":.22,"PK":.05,"LBI":.32,"LBE":.12,"PM":.05},
    "Pendidikan Bahasa Inggris":{"PU":.12,"PPU":.12,"PBM":.18,"PK":.05,"LBI":.12,"LBE":.33,"PM":.08},
    "Pendidikan Bahasa Indonesia":{"PU":.12,"PPU":.12,"PBM":.22,"PK":.05,"LBI":.32,"LBE":.12,"PM":.05},
    "Desain Grafis":         {"PU":.18,"PPU":.10,"PBM":.18,"PK":.12,"LBI":.18,"LBE":.12,"PM":.12},
    "Animasi":               {"PU":.18,"PPU":.10,"PBM":.15,"PK":.15,"LBI":.17,"LBE":.12,"PM":.13},
    "Seni":                  {"PU":.18,"PPU":.12,"PBM":.20,"PK":.08,"LBI":.20,"LBE":.12,"PM":.10},
    "Agribisnis":            {"PU":.20,"PPU":.15,"PBM":.12,"PK":.15,"LBI":.15,"LBE":.08,"PM":.15},
    "Kehutanan":             {"PU":.20,"PPU":.15,"PBM":.12,"PK":.15,"LBI":.15,"LBE":.08,"PM":.15},
    "Peternakan":            {"PU":.20,"PPU":.15,"PBM":.12,"PK":.14,"LBI":.14,"LBE":.08,"PM":.17},
}
DEFAULT_BOBOT = {"PU":.16,"PPU":.14,"PBM":.14,"PK":.14,"LBI":.14,"LBE":.14,"PM":.14}

def get_bobot(prodi_name):
    if prodi_name in BOBOT_KEYWORD:
        return BOBOT_KEYWORD[prodi_name]
    prodi_lower = prodi_name.lower()
    best_match = None
    best_len = 0
    for keyword, bobot in BOBOT_KEYWORD.items():
        if keyword.lower() in prodi_lower and len(keyword) > best_len:
            best_match = bobot
            best_len = len(keyword)
    return best_match if best_match else DEFAULT_BOBOT

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
    bobot = get_bobot(d["prodi"])
    sw    = hitung_tw(skor, bobot)
    rata  = float(np.mean([skor[k] for k in SUBTES]))
    jenjang = d.get("jenjang","S1 (Sarjana)")
    info  = get_skor_info(d["kampus"], d["prodi"], jenjang)
    mn, mx = info["mn"], info["mx"]
    gap   = sw - mn
    kat, kat_clr, kat_badge, kat_icon, ppct = get_kategori_skor(sw, mn, mx)

    psiko   = (d["fokus"]*1.5 + d["pede"]*1.5 + (6-d["cemas"]) + (6-d["distrak"])) / 20 * 100
    konsist = min(100, (d["jam"]*2 + d["hari"]*2.2 + d["latihan"]*1.8 + d["tryout"]*1.5 + d["review"]*1.5)*2)
    pos  = (d["fokus"]*1.5 + d["pede"]*1.5)*10
    neg  = (d["cemas"]*1.2 + d["distrak"]*1.2)*8
    stab = max(0, min(100, pos - neg + 50))
    rgb  = stab*0.6 + konsist*0.4
    if rgb >= 75:   risk=("Rendah","✅","Kemungkinan perform sesuai/di atas kemampuan")
    elif rgb >= 60: risk=("Sedang","⚠️","Ada potensi fluktuasi, jaga konsistensi")
    else:           risk=("Tinggi","🔴","Risiko perform di bawah kemampuan, perlu perbaikan")

    lgbm_r = predict_lgbm(lgbm_model, d) if lgbm_model else None

    return {**d,"skor":skor,"bobot":bobot,"sw":sw,"rata":rata,
            "kat":kat,"kat_clr":kat_clr,"kat_badge":kat_badge,"kat_icon":kat_icon,
            "ppct":ppct,"info":info,"mn":mn,"mx":mx,"gap":gap,
            "psiko":psiko,"konsist":konsist,"stab":stab,"risk":risk,
            "lgbm_r":lgbm_r,"jenjang":jenjang}


# ══════════════════════════════════════════════════════════
# REKOMENDASI ALTERNATIF
# ══════════════════════════════════════════════════════════

def get_rekomendasi_alternatif(skor, sw, prodi_target, kampus_target, jenjang, top_n=10):
    db = get_db(jenjang)
    kat_order = {"Sangat Aman": 0, "Aman": 1, "Berisiko": 2, "Tidak Aman": 3}

    # ── 1. Prodi lain di kampus yang sama ──
    alt_kampus_sama = []
    prodi_di_kampus = db.get(kampus_target, {})
    for prodi, info in prodi_di_kampus.items():
        if prodi == prodi_target:
            continue
        bobot_p = get_bobot(prodi)
        sw_p    = hitung_tw(skor, bobot_p)
        kat_p, kat_clr_p, badge_p, icon_p, pct_p = get_kategori_skor(sw_p, info["mn"], info["mx"])
        alt_kampus_sama.append({
            "prodi": prodi, "kampus": kampus_target,
            "mn": info["mn"], "mx": info["mx"],
            "sw": round(sw_p, 1), "gap": round(sw_p - info["mn"], 1),
            "kat": kat_p, "kat_clr": kat_clr_p,
            "badge": badge_p, "icon": icon_p, "ppct": round(pct_p, 1),
        })
    alt_kampus_sama.sort(key=lambda x: (kat_order.get(x["kat"], 9), -x["gap"]))
    alt_kampus_sama = alt_kampus_sama[:top_n]

    # ── 2. Prodi sama / mirip di kampus lain ──
    prodi_lower = prodi_target.lower()
    prodi_clean = prodi_lower.replace("d3 ", "").replace("d4 ", "").strip()
    alt_prodi_sama = []
    for kampus, prodi_map in db.items():
        if kampus == kampus_target:
            continue
        for prodi, info in prodi_map.items():
            prodi_cmp = prodi.lower().replace("d3 ", "").replace("d4 ", "").strip()
            if prodi_cmp == prodi_clean or prodi_clean in prodi_cmp or prodi_cmp in prodi_clean:
                bobot_p = get_bobot(prodi)
                sw_p    = hitung_tw(skor, bobot_p)
                kat_p, kat_clr_p, badge_p, icon_p, pct_p = get_kategori_skor(sw_p, info["mn"], info["mx"])
                alt_prodi_sama.append({
                    "prodi": prodi, "kampus": kampus,
                    "mn": info["mn"], "mx": info["mx"],
                    "sw": round(sw_p, 1), "gap": round(sw_p - info["mn"], 1),
                    "kat": kat_p, "kat_clr": kat_clr_p,
                    "badge": badge_p, "icon": icon_p, "ppct": round(pct_p, 1),
                })
    alt_prodi_sama.sort(key=lambda x: (kat_order.get(x["kat"], 9), -x["gap"]))
    alt_prodi_sama = alt_prodi_sama[:top_n]

    return alt_kampus_sama, alt_prodi_sama


def render_alt_cards(items, show_kampus=False, show_prodi=False):
    if not items:
        st.info("Tidak ada data alternatif yang ditemukan.")
        return
    badge_bg = {
        "Sangat Aman": ("#e6f5ee", "#148a42", "#9adbb8"),
        "Aman":        ("#edf6ff", "#1a5fa0", "#90c0f0"),
        "Berisiko":    ("#fff4e6", "#e67e22", "#f4c08a"),
        "Tidak Aman":  ("#fff0f0", "#c0392b", "#f4a0a0"),
    }
    for item in items:
        bg, fc, bc = badge_bg.get(item["kat"], ("#f8faff","#334466","#ccd9f0"))
        gap_str  = f"+{item['gap']:.0f}" if item["gap"] >= 0 else f"{item['gap']:.0f}"
        gap_clr  = "#148a42" if item["gap"] >= 0 else "#c0392b"
        if show_kampus:
            nama_utama = item["kampus"]
            nama_sub   = item["prodi"]
        else:
            nama_utama = item["prodi"]
            nama_sub   = item["kampus"]
        st.markdown(f"""
        <div style="background:#fff;border:1.5px solid {bc};border-radius:12px;
                    padding:.9rem 1.2rem;margin-bottom:.55rem;
                    border-left:5px solid {fc};
                    box-shadow:0 2px 10px rgba(30,60,140,.07);">
          <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:.4rem">
            <div>
              <div style="font-family:'Space Grotesk',sans-serif;font-weight:700;font-size:.92rem;color:#12203f">{nama_utama}</div>
              <div style="font-size:.75rem;color:#6a7a9a;margin-top:2px">{nama_sub}</div>
            </div>
            <div style="display:flex;align-items:center;gap:.5rem;flex-wrap:wrap">
              <span style="background:{bg};color:{fc};border:1.5px solid {bc};padding:.22rem .75rem;border-radius:99px;font-size:.72rem;font-weight:700">{item['icon']} {item['kat']}</span>
              <span style="background:#f0f4fa;color:#334466;border:1px solid #dde8f4;padding:.22rem .75rem;border-radius:99px;font-size:.72rem;font-weight:600">~{item['ppct']:.0f}% peluang</span>
            </div>
          </div>
          <div style="display:flex;gap:1.5rem;margin-top:.55rem;font-size:.78rem;flex-wrap:wrap">
            <span>🎯 <strong>Skor kamu:</strong> <span style="font-family:'Space Grotesk',sans-serif;font-weight:700;color:#3464c8">{item['sw']:.0f}</span></span>
            <span>📏 <strong>Rentang aman:</strong> {item['mn']} – {item['mx']}</span>
            <span>📊 <strong>Gap:</strong> <span style="font-weight:700;color:{gap_clr}">{gap_str}</span></span>
          </div>
        </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# RENCANA BELAJAR MINGGUAN
# ══════════════════════════════════════════════════════════
def buat_rencana_mingguan(r, n_minggu=8):
    skor = r["skor"]; sw = r["sw"]; mn = r["mn"]; mx = r["mx"]
    ranked = sorted(SUBTES, key=lambda k: skor[k])
    terlemah3 = ranked[:3]; sedang2 = ranked[3:5]
    gap = r["gap"]
    target_pm = abs(gap)/n_minggu + 10 if gap < 0 else (mx-sw)/n_minggu + 5 if sw < mx else 5
    rencana = []
    for w in range(1, n_minggu+1):
        fase = "Fondasi" if w<=2 else "Intensif" if w<=5 else "Pemantapan" if w<=7 else "Final"
        target_sw = min(mx+20, sw + target_pm * w)
        if fase == "Fondasi":
            tasks = [
                f"Review konsep dasar {SUBTES_FULL[terlemah3[0]]} (skor {skor[terlemah3[0]]} → target +30)",
                f"50 soal latihan {SUBTES_FULL[terlemah3[1]]} dengan timer",
                f"Pelajari pola soal {SUBTES_FULL[terlemah3[2]]}",
                "Buat catatan kesalahan (error log)",
                "Tryout mini: 30 soal campuran + analisis",
            ]; jam = "2–3 jam/hari"
        elif fase == "Intensif":
            subtes_minggu = terlemah3 + sedang2
            subtes_ini = subtes_minggu[(w-3) % len(subtes_minggu)] if subtes_minggu else "PU"
            tasks = [
                f"100 soal latihan {SUBTES_FULL[subtes_ini]} + timer ketat",
                "Review error log minggu sebelumnya",
                f"Mini tryout {SUBTES_FULL[sedang2[0] if sedang2 else 'PU']} (50 soal, 45 mnt)",
                "Simulasi 1 paket soal lengkap (90 mnt)",
                "Analisis & rekap kesalahan pola berulang",
            ]; jam = "3–4 jam/hari"
        elif fase == "Pemantapan":
            tasks = [
                "Full tryout 1 paket lengkap + evaluasi",
                f"Review intensif {SUBTES_FULL[terlemah3[0]]} (subtes fokus utama)",
                "Latihan manajemen waktu (simulasi kondisi ujian)",
                "Review catatan penting semua subtes",
                "Rest day: hanya review ringan 1 jam",
            ]; jam = "3–4 jam/hari (1 hari libur)"
        else:
            tasks = [
                "Full tryout final + review mendalam",
                "Revisi soal-soal sulit yang pernah salah",
                "Persiapan mental: teknik relaksasi & tidur cukup",
                "Cek strategi manajemen waktu ujian",
                "Istirahat — jaga kondisi fisik & mental",
            ]; jam = "2 jam/hari + istirahat cukup"
        rencana.append({
            "minggu":w,"fase":fase,"target_skor":f"{target_sw:.0f}",
            "jam":jam,"fokus":SUBTES_FULL.get(terlemah3[0],"TPS"),"tasks":tasks,
        })
    return rencana

# ══════════════════════════════════════════════════════════
# CHART THEME
# ══════════════════════════════════════════════════════════
CTH = dict(
    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family='Inter', color='#3a4a65'),
    margin=dict(l=10,r=10,t=45,b=10)
)

def ch_radar(skor, bobot, prodi, key=None):
    cats  = [SUBTES_FULL[k] for k in SUBTES] + [SUBTES_FULL[SUBTES[0]]]
    vals  = [skor[k] for k in SUBTES] + [skor[SUBTES[0]]]
    ideal = [min(SKOR_MAX_TPS, SKOR_MAX_TPS*bobot[k]*6) for k in SUBTES] + [min(SKOR_MAX_TPS, SKOR_MAX_TPS*bobot[SUBTES[0]]*6)]
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=ideal,theta=cats,fill='toself',name='Profil Ideal Prodi',
        fillcolor='rgba(200,137,10,.08)',line=dict(color='#c8890a',dash='dot',width=2)))
    fig.add_trace(go.Scatterpolar(r=vals,theta=cats,fill='toself',name='Skor Kamu',
        fillcolor='rgba(59,108,183,.12)',line=dict(color='#3b6cb7',width=2.5)))
    fig.update_layout(**CTH,polar=dict(
        bgcolor='rgba(240,244,248,.6)',
        radialaxis=dict(range=[0,SKOR_MAX_TPS],gridcolor='#dde3ec',linecolor='#dde3ec',tickfont=dict(size=9,color='#6a7a95')),
        angularaxis=dict(gridcolor='#dde3ec',linecolor='#dde3ec',tickfont=dict(size=9.5,color='#3a4a65'))),
        legend=dict(bgcolor='rgba(255,255,255,.8)',orientation='h',x=.5,xanchor='center',y=-.15,font=dict(color='#3a4a65')),
        title=dict(text=f"Radar TPS — {prodi}",font=dict(size=13,color='#1a2540')),height=400)
    st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False},key=key or ckey("radar"))

def ch_bar_subtes(skor, bobot, info, key=None):
    lbl  = [SUBTES_FULL[k] for k in SUBTES]
    vals = [skor[k] for k in SUBTES]
    tgt  = [min(SKOR_MAX_TPS,(info["mn"]+info["mx"])/2*bobot[k]*7) for k in SUBTES]
    clrs = [SUBTES_CLR[k] for k in SUBTES]
    fig  = go.Figure()
    fig.add_trace(go.Bar(name='Skor Kamu',x=lbl,y=vals,marker_color=clrs,marker_line_width=0,
        text=[str(v) for v in vals],textposition='outside',textfont=dict(size=10,color='#1a2540')))
    fig.add_trace(go.Scatter(name='Target Kampus',x=lbl,y=tgt,mode='markers+lines',
        marker=dict(symbol='diamond',size=9,color='#c8890a'),
        line=dict(color='#c8890a',dash='dot',width=1.5)))
    fig.update_layout(**CTH,barmode='group',
        xaxis=dict(tickfont=dict(size=9,color='#3a4a65'),gridcolor='#dde3ec'),
        yaxis=dict(range=[0,SKOR_MAX_TPS*1.07],gridcolor='#eef1f5',tickfont=dict(size=9,color='#3a4a65')),
        legend=dict(bgcolor='rgba(255,255,255,.8)',orientation='h',x=.5,xanchor='center',y=-.2,font=dict(color='#3a4a65')),
        title=dict(text="Skor Per Subtes vs Target Kampus",font=dict(size=13,color='#1a2540')),height=370)
    st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False},key=key or ckey("bar"))

def ch_bobot(prodi, key=None):
    bobot = get_bobot(prodi)
    lbl   = [SUBTES_FULL[k] for k in SUBTES]
    vals  = [bobot[k]*100 for k in SUBTES]
    clrs  = [SUBTES_CLR[k] for k in SUBTES]
    fig   = go.Figure(go.Bar(x=lbl,y=vals,marker_color=clrs,marker_line_width=0,
        text=[f"{v:.0f}%" for v in vals],textposition='outside',textfont=dict(size=10,color='#1a2540')))
    fig.update_layout(**CTH,
        xaxis=dict(tickfont=dict(size=9,color='#3a4a65'),gridcolor='#dde3ec'),
        yaxis=dict(range=[0,55],ticksuffix="%",gridcolor='#eef1f5',tickfont=dict(size=9,color='#3a4a65')),
        title=dict(text=f"Distribusi Bobot Subtes — {prodi}",font=dict(size=13,color='#1a2540')),height=300)
    st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False},key=key or ckey("bobot"))

def ch_pipeline(skor, bobot, info, prodi, key=None):
    lbl    = [SUBTES_FULL[k] for k in SUBTES]
    aktual = [skor[k]*bobot[k] for k in SUBTES]
    ideal  = [info["mn"]*bobot[k] for k in SUBTES]
    clrs   = [SUBTES_CLR[k] for k in SUBTES]
    fig    = go.Figure()
    fig.add_trace(go.Bar(name='Target Min Kampus',y=lbl,x=ideal,orientation='h',
        marker_color=['rgba(200,137,10,.12)']*7,marker_line_color='#c8890a',marker_line_width=1.5))
    fig.add_trace(go.Bar(name='Kontribusi Aktual',y=lbl,x=aktual,orientation='h',
        marker_color=clrs,text=[f"{v:.1f}" for v in aktual],
        textposition='inside',textfont=dict(size=10,color='#fff')))
    fig.update_layout(**CTH,barmode='overlay',
        xaxis=dict(title="Kontribusi ke Skor Total",gridcolor='#eef1f5',title_font=dict(color='#6a7a95'),tickfont=dict(size=9,color='#3a4a65')),
        yaxis=dict(gridcolor='#dde3ec',tickfont=dict(size=10,color='#3a4a65')),
        legend=dict(bgcolor='rgba(255,255,255,.8)',orientation='h',x=.5,xanchor='center',y=-.13,font=dict(color='#3a4a65')),
        title=dict(text=f"Pipeline Kontribusi Subtes — {prodi}",font=dict(size=13,color='#1a2540')),height=380)
    st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False},key=key or ckey("pipe"))

def ch_skor_gauge(sw, mn, mx, key=None):
    na_end  = mn - 70
    br_end  = mn
    a_end   = mx
    sa_end  = min(mx + 80, 1000)
    fig = go.Figure()
    zones = [
        (200,   na_end, "rgba(255,0,0,.08)",   "Tidak Aman"),
        (na_end, br_end, "rgba(230,126,34,.10)", "Berisiko"),
        (br_end, a_end,  "rgba(26,95,160,.08)",  "Aman"),
        (a_end,  sa_end, "rgba(20,138,66,.10)",  "Sangat Aman"),
    ]
    for x0, x1, clr, lbl in zones:
        if x1 > x0:
            fig.add_vrect(x0=x0, x1=x1, fillcolor=clr, layer="below",
                          line_width=0, annotation_text=lbl,
                          annotation_position="top",
                          annotation_font=dict(size=9, color='#3a4a65'))
    fig.add_vline(x=sw, line_dash="dash", line_color="#7048c8", line_width=3,
                  annotation_text=f"  Skormu: {sw:.0f}", annotation_font_color="#7048c8", annotation_font_size=12)
    fig.add_vline(x=mn, line_dash="dot", line_color="#d4620a", line_width=1.5,
                  annotation_text=f"  Min ({mn})", annotation_font_color="#d4620a", annotation_font_size=10)
    fig.add_vline(x=mx, line_dash="dot", line_color="#148a42", line_width=1.5,
                  annotation_text=f"  Aman ({mx})", annotation_font_color="#148a42", annotation_font_size=10)
    fig.add_trace(go.Scatter(x=[sw], y=[0.5], mode='markers',
        marker=dict(size=18, color='#7048c8', symbol='diamond',
                    line=dict(color='#fff', width=2)),
        name=f'Skor {sw:.0f}', showlegend=False))
    fig.update_layout(**CTH,
        xaxis=dict(range=[max(200, mn-150), min(1000, mx+100)],
                   title="Skor Tertimbang", gridcolor='#eef1f5', tickfont=dict(size=9,color='#3a4a65')),
        yaxis=dict(visible=False),
        title=dict(text="📊 Posisi Skor — 4 Kategori Kesiapan", font=dict(size=13,color='#1a2540')),
        height=200)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False}, key=key or ckey("gauge"))

def ch_psiko(psiko, konsist, stab, key=None):
    cats = ["Kesiapan Mental","Konsistensi Belajar","Stabilitas Mental"]
    fig  = go.Figure()
    fig.add_trace(go.Bar(x=cats,y=[psiko,konsist,stab],
        marker_color=["#3b6cb7","#1a8a4a","#7048c8"],marker_line_width=0,
        text=[f"{v:.0f}%" for v in [psiko,konsist,stab]],
        textposition='outside',textfont=dict(size=11,color='#1a2540')))
    fig.add_hline(y=80,line_dash="dot",line_color="#c8890a",line_width=1.5,
        annotation_text="  Target 80%",annotation_font_color="#c8890a",annotation_font_size=10)
    fig.update_layout(**CTH,
        yaxis=dict(range=[0,115],ticksuffix="%",gridcolor='#eef1f5',tickfont=dict(size=9,color='#3a4a65')),
        xaxis=dict(gridcolor='#dde3ec',tickfont=dict(size=10,color='#3a4a65')),
        title=dict(text="Indikator Psikologis & Konsistensi",font=dict(size=13,color='#1a2540')),height=300)
    st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False},key=key or ckey("psiko"))

def ch_progress(r, key=None):
    sw=r["sw"]; mn=r["mn"]; mx=r["mx"]
    gap=abs(r["gap"]) if r["gap"]<0 else 0
    ppm = gap/8+8
    weeks = list(range(0,9))
    preds = [min(mx+30, sw+ppm*w) for w in weeks]
    fig = go.Figure()
    fig.add_hrect(y0=mn,y1=mx,fillcolor="rgba(26,138,74,.07)",layer="below",line_width=0,
                  annotation_text="  Zona Aman",annotation_position="top right",
                  annotation_font=dict(color="#1a8a4a",size=10))
    fig.add_trace(go.Scatter(x=weeks,y=preds,mode='lines+markers+text',
        line=dict(color='#3b6cb7',width=2.5),
        marker=dict(size=8,color='#3b6cb7',line=dict(color='#ffffff',width=1.5)),
        text=[f"{v:.0f}" for v in preds],textposition='top center',
        textfont=dict(size=9,color='#3a4a65'),name='Proyeksi Skor'))
    fig.add_trace(go.Scatter(x=[0],y=[sw],mode='markers',
        marker=dict(size=12,color='#c8890a',symbol='star'),
        name=f'Skor Sekarang ({sw:.0f})'))
    fig.add_hline(y=mn,line_dash="dash",line_color="#d4620a",line_width=1.5,
        annotation_text=f"  Minimum ({mn})",annotation_font_color="#d4620a",annotation_font_size=10)
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter',color='#3a4a65'),margin=dict(l=10,r=10,t=45,b=30),
        xaxis=dict(title="Minggu ke-",tickvals=weeks,gridcolor='#eef1f5',title_font=dict(color='#6a7a95'),tickfont=dict(size=9,color='#3a4a65')),
        yaxis=dict(range=[max(400,sw-100),min(1000,mx+60)],gridcolor='#eef1f5',title="Proyeksi Skor",title_font=dict(color='#6a7a95'),tickfont=dict(size=9,color='#3a4a65')),
        legend=dict(bgcolor='rgba(255,255,255,.8)',font=dict(color='#3a4a65')),
        title=dict(text="Proyeksi Skor 8 Minggu ke Depan",font=dict(size=13,color='#1a2540')),height=340)
    st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False},key=key or ckey("prog"))

# ══════════════════════════════════════════════════════════
# PDF EXPORT — CHANGE 1: rounded total skor + alt recommendations
# ══════════════════════════════════════════════════════════
def generate_pdf(r):
    now  = datetime.datetime.now().strftime("%d %B %Y, %H:%M")
    nama = r.get("nama","—")
    jenjang_lbl = r.get("jenjang","S1 (Sarjana)")
    bobot_rows = "".join(
        f"<tr><td>{SUBTES_FULL[k]}</td><td>{int(r['bobot'][k]*100)}%</td>"
        f"<td>{r['skor'][k]}</td><td>{r['skor'][k]*r['bobot'][k]:.1f}</td></tr>"
        for k in SUBTES)
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

    # ── Rekomendasi alternatif untuk PDF ──
    skor = r["skor"]
    sw   = r["sw"]
    alt_kampus, alt_ptn = get_rekomendasi_alternatif(
        skor, sw, r["prodi"], r["kampus"], r["jenjang"], top_n=5
    )
    def alt_rows(items, show_kampus=False):
        rows = ""
        for item in items:
            gap_str = f"+{item['gap']:.0f}" if item["gap"] >= 0 else f"{item['gap']:.0f}"
            if show_kampus:
                col1, col2 = item["kampus"], item["prodi"]
            else:
                col1, col2 = item["prodi"], item["kampus"]
            rows += f"<tr><td>{col1}</td><td>{col2}</td><td>{item['sw']:.0f}</td><td>{item['mn']}–{item['mx']}</td><td>{gap_str}</td><td>{item['icon']} {item['kat']}</td><td>{item['ppct']:.0f}%</td></tr>"
        return rows

    alt_kampus_html = ""
    if alt_kampus:
        alt_kampus_html = f"""
        <h2>🏛️ Rekomendasi Prodi Lain di {r['kampus']}</h2>
        <table>
          <tr><th>Program Studi</th><th>Kampus</th><th>Skor Kamu</th><th>Rentang Aman</th><th>Gap</th><th>Status</th><th>Peluang</th></tr>
          {alt_rows(alt_kampus, show_kampus=False)}
        </table>"""

    alt_ptn_html = ""
    if alt_ptn:
        alt_ptn_html = f"""
        <h2>🔄 {r['prodi']} di Kampus Lain</h2>
        <table>
          <tr><th>Kampus</th><th>Program Studi</th><th>Skor Kamu</th><th>Rentang Aman</th><th>Gap</th><th>Status</th><th>Peluang</th></tr>
          {alt_rows(alt_ptn, show_kampus=True)}
        </table>"""

    # CHANGE 1: round skor tertimbang to integer in PDF
    sw_rounded = round(r["sw"])

    return f"""<!DOCTYPE html><html lang="id"><head><meta charset="UTF-8">
<title>Laporan SKORIA — {nama}</title>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:'Segoe UI',sans-serif;font-size:11pt;color:#1e293b;background:#fff;padding:1.2cm 1.8cm}}
h1{{font-size:18pt;font-weight:800;color:#0f172a}}
h2{{font-size:11pt;font-weight:700;color:#0f172a;margin:16px 0 7px;border-bottom:2px solid #3b6cb7;padding-bottom:3px}}
p{{font-size:10pt;line-height:1.65;color:#374151;margin-bottom:5px}}
.hdr{{background:linear-gradient(135deg,#2a4a8c,#3b6cb7);color:#fff;padding:1.1cm 1.4cm;border-radius:12px;margin-bottom:.9cm}}
.brand{{font-size:12pt;font-weight:800;color:#ffd166;margin-bottom:3px}}
.hdr .sub{{color:rgba(255,255,255,.75);font-size:9pt;margin-top:3px}}
.kpi-row{{display:flex;gap:10px;margin-bottom:10px}}
.kpi{{flex:1;border:1px solid #e2e8f0;border-radius:8px;padding:10px;text-align:center}}
.kpi .val{{font-size:18pt;font-weight:800}}
.kpi .lbl{{font-size:7.5pt;color:#64748b;text-transform:uppercase;letter-spacing:.05em}}
.green{{color:#16a34a}}.orange{{color:#ca8a04}}.red{{color:#dc2626}}.blue{{color:#1d4ed8}}
table{{width:100%;border-collapse:collapse;font-size:9.5pt;margin-bottom:9px}}
th{{background:#eef3fc;text-align:left;padding:5px 9px;font-weight:600;border:1px solid #dde3ec}}
td{{padding:5px 9px;border:1px solid #dde3ec;color:#374151}}
tr:nth-child(even) td{{background:#f7f9fc}}
.footer{{margin-top:.8cm;font-size:8pt;color:#94a3b8;text-align:center;border-top:1px solid #e2e8f0;padding-top:7px}}
@media print{{body{{padding:.8cm 1cm}}}}
.badge-sa{{background:#e6f5ee;color:#148a42;padding:3px 10px;border-radius:99px;font-weight:700}}
.badge-a {{background:#edf6ff;color:#1a5fa0;padding:3px 10px;border-radius:99px;font-weight:700}}
.badge-br{{background:#fff4e6;color:#d4620a;padding:3px 10px;border-radius:99px;font-weight:700}}
.badge-na{{background:#fff0f0;color:#c0392b;padding:3px 10px;border-radius:99px;font-weight:700}}
</style></head><body>
<div class="hdr">
  <div class="brand">🎯 SKORIA</div>
  <h1>AI UTBK Readiness Report</h1>
  <div class="sub">Laporan Kesiapan UTBK · {now}</div>
</div>
<h2>👤 Profil Siswa</h2>
<table><tr><th>Nama</th><td>{nama}</td><th>Jenjang</th><td>{jenjang_lbl}</td></tr>
<tr><th>Program Studi</th><td>{r['prodi']}</td><th>Kampus Target</th><td>{r['kampus']}</td></tr></table>
<h2>📊 Ringkasan Hasil</h2>
<div class="kpi-row">
<div class="kpi"><div class="lbl">Skor Tertimbang</div><div class="val {gc}">{sw_rounded}</div><div class="lbl">dari 1000</div></div>
<div class="kpi"><div class="lbl">Rentang Aman</div><div class="val blue">{r['mn']} – {r['mx']}</div></div>
<div class="kpi"><div class="lbl">Peluang Lolos</div><div class="val {pc}">{r['ppct']:.0f}%</div></div>
<div class="kpi"><div class="lbl">Gap vs Minimum</div><div class="val {gc}">{r['gap']:+.0f}</div></div>
</div>
<p>Status: <span class="badge-{r['kat_badge'].replace('badge-','')}">{r['kat_icon']} {r['kat']}</span> | Skor Aman: {r['mn']}–{r['mx']}</p>
<p>Kategori: <strong>Tidak Aman</strong> = &lt;{r['mn']-70} | <strong>Berisiko</strong> = {r['mn']-70}–{r['mn']-1} | <strong>Aman</strong> = {r['mn']}–{r['mx']-1} | <strong>Sangat Aman</strong> = ≥{r['mx']}</p>
{lgbm_txt}
<h2>📋 Bobot & Skor Subtes</h2>
<table><tr><th>Subtes</th><th>Bobot</th><th>Skor</th><th>Kontribusi</th></tr>
{bobot_rows}
<tr style="background:#eef3fc"><th colspan="2">Total Skor Tertimbang</th><th colspan="2"><strong>{sw_rounded}</strong></th></tr></table>
<h2>🧠 Indikator Psikologis</h2>
<table>
<tr><th>Fokus</th><td>{r['fokus']}/5</td><th>Percaya Diri</th><td>{r['pede']}/5</td></tr>
<tr><th>Kecemasan</th><td>{r['cemas']}/5</td><th>Distraksi</th><td>{r['distrak']}/5</td></tr>
<tr><th>Kesiapan Mental</th><td>{r['psiko']:.0f}/100</td><th>Konsistensi</th><td>{r['konsist']:.0f}/100</td></tr>
<tr><th>Stabilitas</th><td>{r['stab']:.0f}/100</td><th>Risiko Underperform</th><td>{r['risk'][0]} {r['risk'][1]}</td></tr></table>
{alt_kampus_html}
{alt_ptn_html}
<h2>📅 Rencana Belajar Mingguan (8 Minggu)</h2>
{minggu_html}
<div class="footer">🎯 SKORIA — AI UTBK Intelligence · Data SNPMB/BPPP Kemdikbud 2025/2026 · Skor skala 200–1000</div>
<div style="margin-top:16px;text-align:center">
<button onclick="window.print()" style="padding:8px 20px;background:#3b6cb7;border:none;border-radius:8px;font-weight:700;cursor:pointer;font-size:11pt;color:#fff">
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
      <div class="topbar-brand">🎯 SKORIA <span class="topbar-tag">AI UTBK Intelligence · S1 · D4 · D3 · 2025/2026</span></div>
      <div style="flex:1"></div>
      <div class="step-pill {s1}">{'✓' if p in ['survey','result'] else '①'} Beranda</div>
      <div class="step-pill {s2}">{'✓' if p=='result' else '②'} Input Data</div>
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

def bobot_chips(prodi):
    b = get_bobot(prodi)
    chips = "".join(
        f'<div class="bobot-chip"><span class="sk">{k}</span><span class="bv">{int(b[k]*100)}%</span></div>'
        for k in SUBTES)
    st.markdown(f'<div style="display:flex;flex-wrap:wrap;gap:3px;margin:.4rem 0">{chips}</div>',
                unsafe_allow_html=True)

def step_bar(cur):
    steps = ["👤 Profil & Target","📊 Skor TPS","🧠 Psikologis","📚 Kebiasaan Belajar"]
    html  = '<div class="step-row">'
    for i,s in enumerate(steps,1):
        cls = "active" if i==cur else "done" if i<cur else ""
        mk  = "✓" if i<cur else str(i)
        html += f'<div class="step-item {cls}"><span class="step-num">{mk}</span>{s}</div>'
    st.markdown(html+"</div>", unsafe_allow_html=True)

def render_skor_legend(mn, mx):
    st.markdown(f"""<div class="skor-legend">
      <span class="skor-legend-item sl-na">🔴 Tidak Aman &lt;{mn-70}</span>
      <span class="skor-legend-item sl-br">⚡ Berisiko {mn-70}–{mn-1}</span>
      <span class="skor-legend-item sl-a">✅ Aman {mn}–{mx-1}</span>
      <span class="skor-legend-item sl-sa">🏆 Sangat Aman ≥{mx}</span>
    </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# PAGE: HOME — CHANGE 3: Feature explanation panel added
# ══════════════════════════════════════════════════════════
def page_home():
    st.markdown("""
    <div class="ticker-wrap">
      <div class="ticker-inner">
        <span class="ticker-item">🎯 SKORIA v5.0 — AI UTBK Intelligence</span>
        <span class="ticker-item">📊 Data SNPMB/BPPP Kemdikbud <span>2025/2026</span></span>
        <span class="ticker-item">🎓 Jenjang <span>S1</span> · <span>D4</span> · <span>D3 Vokasi</span></span>
        <span class="ticker-item">🏛️ <span>30 PTN</span> — Data Estimasi Historis 2022–2024</span>
        <span class="ticker-item">📚 <span>60+</span> Prodi S1 · <span>D3/D4</span> dari database xlsx</span>
        <span class="ticker-item">🤖 Powered by <span>LightGBM AI</span></span>
        <span class="ticker-item">📊 4 Kategori Skor: <span>Tidak Aman</span> · <span>Berisiko</span> · <span>Aman</span> · <span>Sangat Aman</span></span>
        <span class="ticker-item">📅 Rencana Belajar <span>8 Minggu</span> Personal</span>
        <span class="ticker-item">🎯 SKORIA v5.0 — AI UTBK Intelligence</span>
        <span class="ticker-item">📊 Data SNPMB/BPPP Kemdikbud <span>2025/2026</span></span>
        <span class="ticker-item">🎓 Jenjang <span>S1</span> · <span>D4</span> · <span>D3 Vokasi</span></span>
        <span class="ticker-item">🏛️ <span>30 PTN</span> — Data Estimasi Historis 2022–2024</span>
        <span class="ticker-item">📚 <span>60+</span> Prodi S1 · <span>D3/D4</span> dari database xlsx</span>
        <span class="ticker-item">🤖 Powered by <span>LightGBM AI</span></span>
        <span class="ticker-item">📊 4 Kategori Skor: <span>Tidak Aman</span> · <span>Berisiko</span> · <span>Aman</span> · <span>Sangat Aman</span></span>
        <span class="ticker-item">📅 Rencana Belajar <span>8 Minggu</span> Personal</span>
      </div>
    </div>""", unsafe_allow_html=True)

    st.markdown("""<div class="hero">
      <div class="hero-badge">🚀 v5.0 · S1 · D4 · D3 · 30 PTN · Database xlsx Real-time</div>
      <h1>SKORIA — Analisis Kesiapan<br><span>UTBK</span> Berbasis AI</h1>
      <p>Platform AI untuk memahami peluang, gap skor, dan strategi belajar personal.<br>
         Data skor estimasi S1/D4/D3 dari database SNPMB/BPPP Kemdikbud 2022–2024.</p>
    </div>""", unsafe_allow_html=True)

    st.markdown("""<div class="stat-row">
      <div class="stat-box"><div class="stat-num">30</div><div class="stat-lbl">🏛️ PTN</div></div>
      <div class="stat-box"><div class="stat-num">4</div><div class="stat-lbl">📊 Kategori Skor</div></div>
      <div class="stat-box"><div class="stat-num">7</div><div class="stat-lbl">📝 Subtes TPS</div></div>
      <div class="stat-box"><div class="stat-num">8</div><div class="stat-lbl">📅 Minggu Rencana</div></div>
    </div>""", unsafe_allow_html=True)

    # ── CHANGE 3: Penjelasan fitur / hasil yang bisa didapat ──
    fitur_items = [
        ("📊", "d1", "Skor Tertimbang (TW)",
         "Skor akhir yang dihitung berdasarkan 7 subtes TPS dengan bobot yang disesuaikan per program studi, persis seperti cara penilaian nyata UTBK."),
        ("🏆", "d2", "4 Kategori Kesiapan",
         "Status lolos dikelompokkan menjadi <b>Tidak Aman &middot; Berisiko &middot; Aman &middot; Sangat Aman</b> lengkap dengan estimasi persentase peluang lolos."),
        ("📏", "d3", "Gap vs Skor Minimum",
         "Selisih skor kamu dengan batas minimum dan batas aman kampus/prodi target &mdash; kamu tahu persis berapa poin yang perlu ditingkatkan."),
        ("🎯", "d4", "Rekomendasi Prodi Alternatif",
         "Jika peluang masih kurang, SKORIA menampilkan prodi lain di kampus yang sama dan prodi serupa di kampus berbeda yang lebih sesuai skormu."),
        ("🤖", "d5", "Strategi Belajar AI (LightGBM)",
         "Model machine learning menganalisis kebiasaan &amp; kondisi psikologismu lalu merekomendasikan strategi yang paling tepat dari 4 pendekatan berbeda."),
        ("📅", "d6", "Rencana Belajar 8 Minggu",
         "Jadwal belajar personal mingguan &mdash; Fondasi, Intensif, Pemantapan, hingga Final &mdash; dengan target skor per minggu dan tugas harian yang spesifik."),
        ("📡", "d1", "Radar TPS vs Profil Ideal",
         "Grafik radar interaktif membandingkan skormu dengan profil ideal prodi &mdash; langsung terlihat subtes mana yang perlu diperkuat lebih dulu."),
        ("🧠", "d2", "Analisis Psikologis",
         "Indikator Kesiapan Mental, Konsistensi Belajar, dan Stabilitas Mental yang membantumu memahami faktor non-akademik yang mempengaruhi performa UTBK."),
        ("📄", "d3", "Export Laporan PDF",
         "Seluruh hasil analisis &mdash; skor, gap, rekomendasi alternatif, dan rencana 8 minggu &mdash; bisa diunduh sebagai laporan HTML siap cetak menjadi PDF."),
    ]
    items_html = "".join(
        f'<div class="fitur-item {d}">'
        f'<span class="fitur-item-icon">{icon}</span>'
        f'<div class="fitur-item-title">{title}</div>'
        f'<div class="fitur-item-desc">{desc}</div>'
        f'</div>'
        for icon, d, title, desc in fitur_items
    )
    st.markdown(
        f'<div class="fitur-panel">'
        f'<div class="fitur-panel-title">&#128269; Apa Saja yang Bisa Kamu Dapatkan dari SKORIA AI?</div>'
        f'<div class="fitur-grid-3">{items_html}</div>'
        f'</div>',
        unsafe_allow_html=True
    )

    # Legenda 4 kategori
    st.markdown("""<div style="background:#fff;border:1px solid #e0e8f4;border-radius:12px;padding:1rem 1.4rem;margin-bottom:1.2rem;box-shadow:0 2px 12px rgba(30,60,140,.08)">
      <div style="font-family:'Space Grotesk',sans-serif;font-size:.9rem;font-weight:700;color:#12203f;margin-bottom:.7rem">📊 4 Kategori Rentang Skor SKORIA</div>
      <div style="display:flex;gap:.6rem;flex-wrap:wrap">
        <span style="background:#fff0f0;color:#c0392b;border:1.5px solid #f4a0a0;padding:.3rem .9rem;border-radius:99px;font-size:.78rem;font-weight:700">🔴 Tidak Aman — Butuh peningkatan signifikan</span>
        <span style="background:#fff4e6;color:#e67e22;border:1.5px solid #f4c08a;padding:.3rem .9rem;border-radius:99px;font-size:.78rem;font-weight:700">⚡ Berisiko — Mendekati zona aman</span>
        <span style="background:#edf6ff;color:#1a5fa0;border:1.5px solid #90c0f0;padding:.3rem .9rem;border-radius:99px;font-size:.78rem;font-weight:700">✅ Aman — Dalam zona aman</span>
        <span style="background:#e6f5ee;color:#148a42;border:1.5px solid #9adbb8;padding:.3rem .9rem;border-radius:99px;font-size:.78rem;font-weight:700">🏆 Sangat Aman — Melampaui batas aman</span>
      </div>
    </div>""", unsafe_allow_html=True)

    st.markdown("""<div class="feat-grid">
      <div class="feat-card d1"><span class="feat-icon">🗃️</span><div class="feat-title">Database xlsx Real</div><div class="feat-desc">Data dari file xlsx estimasi historis UTBK 2022–2024 langsung terhubung</div></div>
      <div class="feat-card d2"><span class="feat-icon">📊</span><div class="feat-title">4 Kategori Skor</div><div class="feat-desc">Tidak Aman · Berisiko · Aman · Sangat Aman dengan rentang skor visual</div></div>
      <div class="feat-card d3"><span class="feat-icon">🤖</span><div class="feat-title">AI LightGBM</div><div class="feat-desc">Prediksi strategi belajar otomatis dari model machine learning</div></div>
      <div class="feat-card d4"><span class="feat-icon">📄</span><div class="feat-title">Export PDF</div><div class="feat-desc">Laporan lengkap 8 minggu + rekomendasi alternatif siap cetak</div></div>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="anim-div"></div>', unsafe_allow_html=True)

    if _DB_ERR:
        st.markdown(f'<div class="al al-d"><h4>⚠️ Database Error</h4>{_DB_ERR}<br>Pastikan file xlsx tersedia atau URL GitHub benar.</div>', unsafe_allow_html=True)
    elif _PTN_S1:
        n_ptn_s1 = len(_PTN_S1)
        n_prodi_s1 = sum(len(v) for v in _PTN_S1.values())
        n_ptn_d3 = len(_PTN_D3) if _PTN_D3 else 0
        n_ptn_d4 = len(_PTN_D4) if _PTN_D4 else 0
        st.markdown(f'<div class="al al-s"><h4>✅ Database Berhasil Dimuat</h4>S1: <strong>{n_ptn_s1} PTN</strong>, {n_prodi_s1}+ prodi · D3: <strong>{n_ptn_d3} PTN</strong> · D4: <strong>{n_ptn_d4} PTN</strong><br><small style="color:#6a7a95">Estimasi historis UTBK 2022–2024 · Data resmi: snpmb.bppp.kemdikbud.go.id</small></div>', unsafe_allow_html=True)

    ai_status = f'<div class="al al-s"><h4>✅ Model AI Aktif</h4>File: <code>{lgbm_fname}</code></div>' if lgbm_model else '<div class="al al-w"><h4>⚠️ Model AI Tidak Ditemukan</h4>Letakkan <code>lgbm_model_2_.pkl</code> di folder yang sama. Kalkulasi manual tetap berjalan.</div>'
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
# PAGE: SURVEY — CHANGE 4: urutan Nama → Jenjang → Kampus → Jurusan (sudah benar, diperkuat)
# ══════════════════════════════════════════════════════════
def step1():
    st.markdown("""<div class="al al-i d1" style="margin-bottom:1rem;padding:.8rem 1.2rem">
      <h4>👤 Langkah 1 dari 4 — Profil &amp; Target</h4>
      Isi <strong>① Nama Lengkap</strong> → pilih <strong>② Jenjang Pendidikan</strong> → pilih <strong>③ Kampus</strong> → lalu <strong>④ Jurusan/Prodi</strong>.
    </div>""", unsafe_allow_html=True)
    st.markdown('<div class="form-box">', unsafe_allow_html=True)
    st.markdown('<h3>👤 Profil &amp; Target</h3>', unsafe_allow_html=True)
    d = st.session_state.data

    # ① Nama Lengkap — PERTAMA
    nama = st.text_input("① Nama Lengkap", value=d.get("nama",""), placeholder="Masukkan nama kamu...")

    # ② Jenjang Pendidikan — KEDUA
    prev_jenjang = d.get("jenjang", DAFTAR_JENJANG[0])
    if prev_jenjang not in DAFTAR_JENJANG:
        prev_jenjang = DAFTAR_JENJANG[0]
    jenjang = st.radio(
        "② Jenjang Pendidikan yang Dituju",
        DAFTAR_JENJANG,
        index=DAFTAR_JENJANG.index(prev_jenjang),
        horizontal=True,
        help="S1 = Sarjana (4 th) | D4 = Sarjana Terapan (4 th, vokasi) | D3 = Diploma Tiga (3 th, vokasi)"
    )

    # ③ Kampus — KETIGA (setelah jenjang dipilih)
    daftar_ptn = get_daftar_ptn(jenjang)
    if not daftar_ptn:
        st.warning(f"⚠️ Data PTN untuk jenjang {jenjang} belum tersedia. Cek koneksi atau file xlsx.")
        st.markdown('</div>', unsafe_allow_html=True)
        if st.button("◀ Kembali ke Beranda"):
            st.session_state.page = "home"; st.rerun()
        return

    prev_kampus = d.get("kampus", daftar_ptn[0])
    if prev_kampus not in daftar_ptn:
        prev_kampus = daftar_ptn[0]
    kampus = st.selectbox(
        "③ Kampus Target (PTN)",
        daftar_ptn,
        index=daftar_ptn.index(prev_kampus),
        help="Pilih PTN yang kamu tuju — daftar disesuaikan dengan jenjang yang dipilih"
    )

    # ④ Jurusan/Prodi — KEEMPAT (setelah kampus dipilih)
    daftar_prodi = get_daftar_prodi(kampus, jenjang)
    if not daftar_prodi:
        st.warning(f"⚠️ Tidak ada data prodi untuk {kampus} ({jenjang}).")
        st.markdown('</div>', unsafe_allow_html=True)
        return

    prev_prodi = d.get("prodi", daftar_prodi[0])
    if prev_prodi not in daftar_prodi:
        prev_prodi = daftar_prodi[0]
    prodi = st.selectbox(
        "④ Program Studi / Jurusan",
        daftar_prodi,
        index=daftar_prodi.index(prev_prodi),
        help="Pilih program studi setelah memilih kampus — daftar difilter otomatis"
    )

    # Info skor aman
    info = get_skor_info(kampus, prodi, jenjang)
    mn, mx = info["mn"], info["mx"]
    render_skor_legend(mn, mx)

    st.markdown(f"""<div class="al al-i" style="margin-top:.7rem">
      <h4>🏛️ {kampus}</h4>
      Rentang skor aman <strong>{jenjang}</strong> — <strong>{prodi}</strong>:
      <br>
      <span style="font-size:1.1rem;font-weight:800;color:#3464c8">{mn} – {mx}</span>
      <br><small style="color:#6a7a95">Estimasi historis UTBK 2022–2024 · Sumber: SNPMB/BPPP Kemdikbud & referensi media pendidikan</small>
    </div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(f"**Distribusi bobot subtes untuk _{prodi}_:**")
    bobot_chips(prodi)

    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("Lanjut → Skor TPS ▶", type="primary"):
        if not nama.strip():
            st.error("❌ Nama harus diisi!")
            return
        st.session_state.data.update({"nama":nama,"jenjang":jenjang,"kampus":kampus,"prodi":prodi})
        st.session_state.step=2; st.rerun()

def step2():
    st.markdown("""<div class="al al-p d1" style="margin-bottom:1rem;padding:.8rem 1.2rem">
      <h4>📊 Langkah 2 dari 4 — Skor TPS</h4>
      Masukkan skor tryout terbaru untuk 7 subtes TPS.
    </div>""", unsafe_allow_html=True)
    st.markdown('<div class="form-box">', unsafe_allow_html=True)
    st.markdown('<h3>📊 Skor TPS (Tes Potensi Skolastik)</h3>', unsafe_allow_html=True)
    st.caption(f"Masukkan skor tryout terbaru. Skala: {SKOR_MIN_TPS} – {SKOR_MAX_TPS}")
    d = st.session_state.data
    skor = {}
    pairs = [("PU","PPU"),("PBM","PK"),("LBI","LBE"),("PM",None)]
    for pair in pairs:
        cols = st.columns(2)
        for col, k in zip(cols, pair):
            if k is None: continue
            with col:
                skor[k] = st.number_input(
                    f"{SUBTES_FULL[k]} ({k})",
                    min_value=SKOR_MIN_TPS, max_value=SKOR_MAX_TPS,
                    value=int(d.get(k, 550)), step=5, key=f"n_{k}",
                )

    prodi  = d.get("prodi","")
    bobot  = get_bobot(prodi)
    cats   = [SUBTES_FULL[k] for k in SUBTES]+[SUBTES_FULL[SUBTES[0]]]
    vals   = [skor[k] for k in SUBTES]+[skor[SUBTES[0]]]
    ideal  = [min(SKOR_MAX_TPS,SKOR_MAX_TPS*bobot[k]*6) for k in SUBTES]+[min(SKOR_MAX_TPS,SKOR_MAX_TPS*bobot[SUBTES[0]]*6)]
    fig    = go.Figure()
    fig.add_trace(go.Scatterpolar(r=ideal,theta=cats,fill='toself',name='Profil Ideal',
        fillcolor='rgba(200,137,10,.08)',line=dict(color='#c8890a',dash='dot',width=2)))
    fig.add_trace(go.Scatterpolar(r=vals,theta=cats,fill='toself',name='Skor Kamu',
        fillcolor='rgba(59,108,183,.12)',line=dict(color='#3b6cb7',width=2.5)))
    fig.update_layout(**CTH,polar=dict(
        bgcolor='rgba(240,244,248,.6)',
        radialaxis=dict(range=[0,SKOR_MAX_TPS],gridcolor='#dde3ec',linecolor='#dde3ec',tickfont=dict(size=9,color='#6a7a95')),
        angularaxis=dict(gridcolor='#dde3ec',linecolor='#dde3ec',tickfont=dict(size=9.5,color='#3a4a65'))),
        legend=dict(bgcolor='rgba(255,255,255,.8)',orientation='h',x=.5,xanchor='center',y=-.15,font=dict(color='#3a4a65')),
        title=dict(text=f"Preview Radar — {prodi}",font=dict(size=13,color='#1a2540')),height=380)
    st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False},key="survey_radar")
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
      Nilai kondisi mental dan emosional kamu saat belajar.
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
      Langkah terakhir! Data ini digunakan oleh model AI untuk rekomendasi strategi.
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
    {1:step1, 2:step2, 3:step3, 4:step4}[st.session_state.step]()

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

    kat_cls_map = {
        "Sangat Aman":"badge-sa", "Aman":"badge-a",
        "Berisiko":"badge-br",    "Tidak Aman":"badge-na"
    }
    sb_cls = kat_cls_map.get(r["kat"], "badge-na")

    st.markdown(f"""<div class="hero">
      <div class="hero-badge">🎓 {jenjang_lbl} · {r['prodi']} · {r['kampus']}</div>
      <h1 style="font-size:1.65rem!important">{salam}, <span>{nama}!</span> 👋</h1>
      <p>Hasil analisis <strong style="color:#ffd166">SKORIA AI</strong> berdasarkan skor TPS, psikologis, dan kebiasaan belajarmu</p>
      <div style="margin-top:1rem">
        <span class="status-badge {sb_cls}">{r['kat_icon']} {r['kat']} · Skor {r['sw']:.0f}</span>
        &nbsp;
        <span class="status-badge badge-a">📊 Peluang ~{r['ppct']:.0f}%</span>
      </div>
    </div>""", unsafe_allow_html=True)

    mn, mx = r["mn"], r["mx"]
    gc = "c-green" if r["gap"]>=0 else "c-red"
    pc = "c-green" if r["ppct"]>=65 else "c-orange" if r["ppct"]>=35 else "c-red"
    kc_map = {"Sangat Aman":"c-green","Aman":"c-blue","Berisiko":"c-orange","Tidak Aman":"c-red"}
    kc = kc_map.get(r["kat"],"c-red")

    k1,k2,k3,k4,k5 = st.columns(5)
    kampus_short = r["kampus"].split("(")[0].strip()[:22]
    for i,(col,lbl,val,cls,sub) in enumerate([
        (k1,"Skor Tertimbang",f"{r['sw']:.0f}",kc,"dari 1000"),
        (k2,"Rentang Aman",f"{mn}–{mx}","c-blue",kampus_short),
        (k3,"Peluang Lolos",f"{r['ppct']:.0f}%",pc,r["kat"]),
        (k4,"Gap vs Minimum",f"{r['gap']:+.0f}",gc,f"Min {mn}"),
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
    render_skor_legend(mn, mx)

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

    if r["kat"] == "Sangat Aman":
        st.markdown(f"""<div class="al al-s"><h4>🏆 Status: SANGAT AMAN</h4>
          Skor tertimbang <strong>{r['sw']:.0f}</strong> melampaui batas aman atas {mx}.
          Pertahankan performa & jaga kondisi mental menjelang UTBK!</div>""", unsafe_allow_html=True)
    elif r["kat"] == "Aman":
        st.markdown(f"""<div class="al al-s"><h4>✅ Status: AMAN</h4>
          Skor {r['sw']:.0f} dalam zona aman ({mn}–{mx-1}).
          Tambah <strong>{mx-r['sw']:.0f} poin</strong> lagi untuk zona Sangat Aman.</div>""", unsafe_allow_html=True)
    elif r["kat"] == "Berisiko":
        st.markdown(f"""<div class="al al-br"><h4>⚡ Status: BERISIKO</h4>
          Kurang <strong>{mn-r['sw']:.0f} poin</strong> dari batas aman minimum {mn}.
          Intensifkan latihan — masih bisa dikejar!</div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""<div class="al al-na"><h4>🔴 Status: TIDAK AMAN</h4>
          Gap <strong>{abs(r['gap']):.0f} poin</strong> dari minimum {mn}.
          Butuh peningkatan signifikan atau pertimbangkan PTN/prodi alternatif.</div>""", unsafe_allow_html=True)

    t1,t2,t3,t4,t5,t6,t7 = st.tabs([
        "📡 Radar & Skor TPS",
        "📊 Posisi & Peluang",
        "🎯 Alternatif",
        "🔀 Pipeline & Bobot",
        "🚀 Strategi Belajar",
        "📅 Rencana Mingguan",
        "📄 Export PDF",
    ])

    with t1:
        st.markdown('<div class="sec">📡 Radar TPS vs Profil Ideal Prodi</div>', unsafe_allow_html=True)
        ch_radar(r["skor"],r["bobot"],r["prodi"], key="r_radar_t1")
        st.markdown('<div class="sec">📊 Skor Per Subtes vs Target</div>', unsafe_allow_html=True)
        ch_bar_subtes(r["skor"],r["bobot"],r["info"], key="r_bar_t1")
        st.markdown('<div class="sec">Detail Skor Subtes</div>', unsafe_allow_html=True)
        df_data = []
        for k in SUBTES:
            sv = r["skor"][k]
            status = "✅ Kuat" if sv>=750 else "⚡ Sedang" if sv>=550 else "🔴 Perlu Fokus"
            df_data.append({"Subtes":SUBTES_FULL[k],"Bobot (%)":f"{r['bobot'][k]*100:.0f}%",
                            "Skor":sv,"Kontribusi":f"{sv*r['bobot'][k]:.1f}","Status":status})
        st.dataframe(pd.DataFrame(df_data), use_container_width=True, hide_index=True,
            column_config={"Skor": st.column_config.ProgressColumn("Skor",min_value=200,max_value=1000,format="%d")})

    with t2:
        st.markdown('<div class="sec">📊 Posisi Skor — 4 Kategori</div>', unsafe_allow_html=True)
        ch_skor_gauge(r["sw"], mn, mx, key="r_gauge_t2")
        render_skor_legend(mn, mx)
        st.markdown('<div class="sec">📋 Ringkasan Peluang di Semua Prodi</div>', unsafe_allow_html=True)
        daftar_prodi_ptn = get_daftar_prodi(r["kampus"], r["jenjang"])
        rows = []
        for prodi_lain in daftar_prodi_ptn[:30]:
            info_l = get_skor_info(r["kampus"], prodi_lain, r["jenjang"])
            bobot_l = get_bobot(prodi_lain)
            sw_l = hitung_tw(r["skor"], bobot_l)
            kat_l, _, _, icon_l, pct_l = get_kategori_skor(sw_l, info_l["mn"], info_l["mx"])
            rows.append({
                "Program Studi": prodi_lain,
                "Skor Aman": f"{info_l['mn']}–{info_l['mx']}",
                "Skor Kamu": f"{sw_l:.0f}",
                "Status": f"{icon_l} {kat_l}",
                "Est. Peluang": f"{pct_l:.0f}%"
            })
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
        d1,d2,d3 = st.columns(3)
        with d1: st.metric("Skor Minimum",mn)
        with d2: st.metric("Skor Sangat Aman (atas)",mx)
        with d3: st.metric("Skor Kamu",f"{r['sw']:.0f}",delta=f"{r['gap']:+.0f}",delta_color="normal" if r["gap"]>=0 else "inverse")

    with t3:
        sw   = r["sw"]
        skor = r["skor"]
        alt_kampus, alt_ptn = get_rekomendasi_alternatif(
            skor, sw, r["prodi"], r["kampus"], r["jenjang"]
        )
        kat_cls_info = {"Sangat Aman":"al-s","Aman":"al-i","Berisiko":"al-w","Tidak Aman":"al-d"}
        info_cls = kat_cls_info.get(r["kat"], "al-i")
        st.markdown(f'''<div class="al {info_cls}" style="padding:.75rem 1.1rem;margin-bottom:1rem">
          <h4>{r["kat_icon"]} Skor Tertimbang Kamu: <strong>{sw:.0f}</strong> &nbsp;·&nbsp; Status: {r["kat"]}</h4>
          Rekomendasi di bawah dihitung menggunakan <strong>skor TPS kamu yang sama</strong>
          dengan bobot masing-masing program studi — skor kamu mungkin berbeda tiap prodi.
        </div>''', unsafe_allow_html=True)

        st.markdown('<div class="sec">🏛️ Prodi Lain di Kampus yang Sama</div>', unsafe_allow_html=True)
        st.caption(f"Prodi lain di {r['kampus']} — diurutkan dari peluang terbaik")
        if alt_kampus:
            fa1, fa2, fa3 = st.tabs(["Semua Prodi", "✅ Aman & Sangat Aman", "⚡ Berisiko & Tidak Aman"])
            with fa1:
                render_alt_cards(alt_kampus, show_kampus=False)
            with fa2:
                aman_list = [x for x in alt_kampus if x["kat"] in ("Sangat Aman","Aman")]
                if aman_list: render_alt_cards(aman_list, show_kampus=False)
                else: st.info("Tidak ada prodi dengan kategori Aman/Sangat Aman.")
            with fa3:
                risiko_list = [x for x in alt_kampus if x["kat"] in ("Berisiko","Tidak Aman")]
                if risiko_list: render_alt_cards(risiko_list, show_kampus=False)
                else: st.info("Semua prodi masuk kategori Aman atau Sangat Aman! 🎉")
        else:
            st.info("Data prodi untuk kampus ini tidak tersedia.")

        st.markdown('<div class="anim-div"></div>', unsafe_allow_html=True)

        st.markdown('<div class="sec">🔄 Prodi Serupa di Kampus Berbeda</div>', unsafe_allow_html=True)
        st.caption(f"Mencari \"{r['prodi']}\" atau prodi serupa di PTN lain")
        if alt_ptn:
            fb1, fb2, fb3 = st.tabs(["Semua PTN", "✅ Aman & Sangat Aman", "⚡ Berisiko & Tidak Aman"])
            with fb1:
                render_alt_cards(alt_ptn, show_kampus=True)
            with fb2:
                aman_ptn = [x for x in alt_ptn if x["kat"] in ("Sangat Aman","Aman")]
                if aman_ptn: render_alt_cards(aman_ptn, show_kampus=True)
                else: st.info("Tidak ada PTN dengan kategori Aman/Sangat Aman untuk prodi ini.")
            with fb3:
                risiko_ptn = [x for x in alt_ptn if x["kat"] in ("Berisiko","Tidak Aman")]
                if risiko_ptn: render_alt_cards(risiko_ptn, show_kampus=True)
                else: st.info("Semua PTN masuk kategori Aman atau Sangat Aman! 🎉")
        else:
            st.info(f"Tidak ditemukan prodi serupa di PTN lain dengan data yang tersedia.")

        st.markdown('<div class="sec">📋 Tabel Ringkasan Semua Alternatif</div>', unsafe_allow_html=True)
        all_alt = []
        for item in alt_kampus[:5]:
            all_alt.append({"Tipe":"Kampus Sama","Program Studi":item["prodi"],"Kampus":item["kampus"],
                "Skor Kamu":f"{item['sw']:.0f}","Rentang Aman":f"{item['mn']}–{item['mx']}",
                "Gap":f"{item['gap']:+.0f}","Status":f"{item['icon']} {item['kat']}","Peluang":f"{item['ppct']:.0f}%"})
        for item in alt_ptn[:5]:
            all_alt.append({"Tipe":"Prodi Serupa","Program Studi":item["prodi"],"Kampus":item["kampus"],
                "Skor Kamu":f"{item['sw']:.0f}","Rentang Aman":f"{item['mn']}–{item['mx']}",
                "Gap":f"{item['gap']:+.0f}","Status":f"{item['icon']} {item['kat']}","Peluang":f"{item['ppct']:.0f}%"})
        if all_alt:
            st.dataframe(pd.DataFrame(all_alt), use_container_width=True, hide_index=True)

    with t4:
        st.markdown('<div class="sec">🔀 Pipeline Kontribusi Subtes</div>', unsafe_allow_html=True)
        ch_pipeline(r["skor"],r["bobot"],r["info"],r["prodi"], key="r_pipe_t3")
        st.markdown(f'<div class="sec">📐 Distribusi Bobot — {r["prodi"]}</div>', unsafe_allow_html=True)
        ch_bobot(r["prodi"], key="r_bobot_t3")
        st.markdown('<div class="sec">Tabel Bobot & Kontribusi</div>', unsafe_allow_html=True)
        df_b = []
        for k in SUBTES:
            df_b.append({"Subtes":SUBTES_FULL[k],"Bobot":f"{r['bobot'][k]*100:.0f}%","Skor":r["skor"][k],
                         "Kontribusi Aktual":f"{r['skor'][k]*r['bobot'][k]:.1f}",
                         "Target Minimum":f"{mn*r['bobot'][k]:.1f}",
                         "Selisih":f"{(r['skor'][k]-mn)*r['bobot'][k]:+.1f}"})
        df_b.append({"Subtes":"TOTAL","Bobot":"100%","Skor":"—",
                     "Kontribusi Aktual":f"{r['sw']:.1f}","Target Minimum":f"{mn:.0f}","Selisih":f"{r['gap']:+.1f}"})
        st.dataframe(pd.DataFrame(df_b), use_container_width=True, hide_index=True)

    with t5:
        st.markdown('<div class="sec">🚀 Strategi Belajar Personal</div>', unsafe_allow_html=True)
        ch_psiko(r["psiko"],r["konsist"],r["stab"], key="r_psiko_t4")
        prog_bar("Kesiapan Mental",r["psiko"],"#3b6cb7")
        prog_bar("Konsistensi Belajar",r["konsist"],"#1a8a4a")
        prog_bar("Stabilitas Mental",r["stab"],"#7048c8")
        st.markdown('<div class="sec">📌 Prioritas Subtes</div>', unsafe_allow_html=True)
        ss = sorted(r["skor"].items(),key=lambda x:x[1])
        lemah3=ss[:3]; kuat2=ss[-2:]
        cp1,cp2 = st.columns(2)
        with cp1:
            il="".join(f"<li><strong>{SUBTES_FULL[k]}</strong>: {v} → perlu +{max(0,750-v)} poin</li>" for k,v in lemah3)
            st.markdown(f'<div class="al al-d"><h4>🔴 3 Subtes Perlu Fokus</h4><ul>{il}</ul></div>',unsafe_allow_html=True)
        with cp2:
            ik="".join(f"<li><strong>{SUBTES_FULL[k]}</strong>: {v} ✅</li>" for k,v in kuat2)
            st.markdown(f'<div class="al al-s"><h4>🟢 Kekuatan Akademik</h4><ul>{ik}</ul></div>',unsafe_allow_html=True)
        st.markdown('<div class="sec">📋 Rencana Aksi</div>', unsafe_allow_html=True)
        if r["kat"]=="Sangat Aman":
            st.markdown("""<div class="al al-s"><h4>🏆 Maintenance Mode</h4><ul>
              <li>Tryout 1–2x/minggu menjaga ketajaman</li>
              <li>Review kesalahan kecil yang masih berulang</li>
              <li>Fokus manajemen waktu & kondisi mental</li>
              <li>Jaga pola tidur 7–8 jam/malam</li></ul></div>""",unsafe_allow_html=True)
        elif r["kat"]=="Aman":
            st.markdown(f"""<div class="al al-i"><h4>✅ Penguatan & Konsistensi</h4><ul>
              <li>Target +{mx-r['sw']:.0f} poin untuk zona Sangat Aman</li>
              <li>60% waktu pada {SUBTES_FULL[ss[0][0]]} (terlemah)</li>
              <li>Tryout min. 2x/bulan + review mendalam</li>
              <li>Simulasi 150 soal dalam 2.5 jam/sesi</li></ul></div>""",unsafe_allow_html=True)
        elif r["kat"]=="Berisiko":
            st.markdown(f"""<div class="al al-w"><h4>⚡ Intensifikasi Bertarget</h4><ul>
              <li>Target +{mn-r['sw']:.0f} poin untuk zona Aman</li>
              <li>Belajar 3–4 jam/hari terstruktur</li>
              <li>Tryout mingguan + analisis soal salah mendalam</li>
              <li>Fokus subtes berbobot tinggi untuk prodimu</li></ul></div>""",unsafe_allow_html=True)
        else:
            st.markdown(f"""<div class="al al-d"><h4>🔴 Intensifikasi Penuh</h4><ul>
              <li>Target +{abs(r['gap']):.0f} poin — bertahap setiap bulan</li>
              <li>Belajar 4–5 jam/hari terstruktur</li>
              <li>Tryout mingguan + analisis soal salah mendalam</li>
              <li>Konsultasi tutor untuk subtes berbobot tinggi</li>
              <li>Pertimbangkan prodi/PTN yang lebih sesuai</li></ul></div>""",unsafe_allow_html=True)

    with t6:
        st.markdown('<div class="sec">📅 Proyeksi Skor 8 Minggu</div>', unsafe_allow_html=True)
        ch_progress(r, key="r_prog_t5")
        st.markdown('<div class="sec">📋 Detail Rencana Per Minggu</div>', unsafe_allow_html=True)
        rencana = buat_rencana_mingguan(r, 8)
        fase_clr = {"Fondasi":"#3b6cb7","Intensif":"#d4620a","Pemantapan":"#1a8a4a","Final":"#c8890a"}
        for m in rencana:
            clr = fase_clr.get(m["fase"],"#7048c8")
            tasks_html = "".join(f'<div style="padding:.1rem 0;color:#3a4a65">• {t}</div>' for t in m["tasks"])
            st.markdown(f"""<div class="week-card">
              <div class="week-num" style="color:{clr}">MINGGU {m['minggu']} — {m['fase'].upper()}</div>
              <div class="week-target">🎯 Target: <strong style="color:{clr}">{m['target_skor']}</strong> &nbsp;|&nbsp; ⏰ {m['jam']}</div>
              <div class="week-tasks">{tasks_html}</div>
            </div>""", unsafe_allow_html=True)

    with t7:
        st.markdown('<div class="sec">📄 Export Laporan ke PDF</div>', unsafe_allow_html=True)
        st.markdown("""<div class="al al-i"><h4>📋 Laporan PDF Mencakup:</h4><ul>
          <li>Profil siswa & target kampus/prodi</li>
          <li>Skor tertimbang (dibulatkan) & status kategori kesiapan</li>
          <li>Tabel bobot & kontribusi per subtes</li>
          <li>Indikator psikologis & konsistensi belajar</li>
          <li><strong>Rekomendasi prodi alternatif</strong> di kampus yang sama & prodi serupa di kampus lain</li>
          <li>Rencana belajar 8 minggu personal (Fondasi → Intensif → Pemantapan → Final)</li>
        </ul></div>""", unsafe_allow_html=True)
        st.markdown("""<div class="al al-s"><h4>Cara Menyimpan sebagai PDF</h4><ol>
          <li>Klik tombol <strong>Generate & Download Laporan HTML</strong></li>
          <li>Buka file HTML di browser</li>
          <li>Tekan <strong>Ctrl+P</strong> (Win) atau <strong>Cmd+P</strong> (Mac)</li>
          <li>Pilih <strong>"Save as PDF"</strong> → klik Save</li>
        </ol></div>""", unsafe_allow_html=True)
        if st.button("📄  Generate & Download Laporan HTML", type="primary"):
            html = generate_pdf(r)
            b64  = base64.b64encode(html.encode()).decode()
            fn   = f"skoria_{r.get('nama','').replace(' ','_')}.html"
            st.markdown(f"""<a href="data:text/html;base64,{b64}" download="{fn}"
              style="display:inline-block;background:linear-gradient(135deg,#3b6cb7,#2a4a8c);
                     color:#ffffff;font-weight:700;padding:.6rem 1.4rem;border-radius:8px;
                     text-decoration:none;font-size:.9rem;margin-top:.5rem">
              ⬇️ Download {fn}</a>""", unsafe_allow_html=True)
        pp1,pp2 = st.columns(2)
        with pp1:
            st.dataframe(pd.DataFrame([
                {"Info":"Nama","Detail":r.get("nama","—")},
                {"Info":"Jenjang","Detail":r.get("jenjang","—")},
                {"Info":"Program Studi","Detail":r["prodi"]},
                {"Info":"Kampus","Detail":r["kampus"]},
                {"Info":"Skor Tertimbang","Detail":f"{round(r['sw'])} / 1000"},
                {"Info":"Gap vs Minimum","Detail":f"{r['gap']:+.0f}"},
            ]), use_container_width=True, hide_index=True)
        with pp2:
            st.dataframe(pd.DataFrame([
                {"Indikator":"Kategori Skor","Nilai":f"{r['kat_icon']} {r['kat']}"},
                {"Indikator":"Peluang Lolos","Nilai":f"{r['ppct']:.0f}%"},
                {"Indikator":"Kesiapan Mental","Nilai":f"{r['psiko']:.0f}/100"},
                {"Indikator":"Konsistensi","Nilai":f"{r['konsist']:.0f}/100"},
                {"Indikator":"Stabilitas","Nilai":f"{r['stab']:.0f}/100"},
                {"Indikator":"Risiko Underperform","Nilai":f"{r['risk'][0]} {r['risk'][1]}"},
            ]), use_container_width=True, hide_index=True)

    st.divider()
    nb1,nb2,_ = st.columns([1,1,4])
    with nb1:
        if st.button("◀ Ubah Data"): st.session_state.page="survey"; st.session_state.step=1; st.rerun()
    with nb2:
        if st.button("🏠 Beranda"): st.session_state.page="home"; st.rerun()

    st.markdown(f"""<div style="text-align:center;padding:1.4rem;background:var(--surf);
      border-radius:var(--r);border:1px solid var(--border);margin-top:.8rem">
      <div style="font-family:'Space Grotesk',sans-serif;font-size:1.05rem;font-weight:800;color:#1a2540">
        💪 {nama}, kamu pasti bisa!
      </div>
      <div style="color:#6a7a95;font-size:.82rem;margin-top:.3rem">
        Konsistensi + strategi tepat = PTN impianmu pasti bisa diraih 🚀
      </div>
      <div style="color:#b0b8c8;font-size:.7rem;margin-top:.3rem">
        🎯 SKORIA v5.0 — AI UTBK Intelligence · Data xlsx SNPMB 2022–2024 · S1/D4/D3 · 4 Kategori Skor
      </div>
    </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════
def main():
    render_nav()
    {"home":page_home, "survey":page_survey, "result":page_result}[st.session_state.page]()

if __name__ == "__main__":
    main()
