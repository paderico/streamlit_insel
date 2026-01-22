# -*- coding: utf-8 -*-
"""
Created on Mon Jan 12 23:50:17 2026

@author: Patrick Werz
"""

import streamlit as st
import insel
import time

st.set_page_config(layout="wide", page_title="Simulation der Wirtschaftlichkeit von unterschiedlichen Batteriespeicher-Größen")
st.markdown("<h1 style='text-align: center'>Simulation der Wirtschaftlichkeit von unterschiedlichen Batteriespeicher-Größen</h1>", unsafe_allow_html=True)
st.markdown(
    """
    <style>
    /* 1) Globale Standard-Schriftgröße (Body & viele Widgets) */
    html, body, [class*="st-"] {
        font-size: 20px;
    }

    /* 2) Buttons (Hauptbereich) */
    div.stButton > button {
        padding: 0.7rem 1.2rem;
        font-size: 18px !important;
    }
    div.stButton > button > div > p {
        font-size: 22px !important;
    }

    /* 3) Sidebar-Text (alles in der Sidebar) */
    [data-testid="stSidebar"] * {
        font-size: 20px !important;
    }

    /* 4) Slider-Beschriftung (Label über dem Slider) */
    div.stSlider > label > div {
        font-size: 20px !important;
    }

    /* 5) Slider-Werte / Ticks */
    div.stSlider [data-testid="stTickBar"] p {
        font-size: 18px !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

left, right = st.columns([2, 2])


with left:

    st.header("2024")
    verbrauch = st.slider("🔌 Verbrauch [MWh/a]", 0.0, 10.0, 5.5, format="%g MWh / a")
    pvleistung = st.slider("🌞 PV Leistung [kWp]", 0.0, 25.0, 13.6, format="%g kWp")
    wirkungsgrad = st.select_slider("🦾 Batteriewirkungsgrad [%]", 
                                   options=[85.0, 86.0, 87.0, 88.0, 89.0, 90.0, 90.5, 91, 91.5, 92, 92.5, 93, 93.5, 94, 94.5, 95.0, 95.5, 96.0, 96.5, 97.0, 97.5, 98.0, 98.5, 99.0, 99.5, 100.0],
                                   value=98.5, 
                                   format_func=lambda x:f"{x:g} %", 
                                   )
    
    # Batteriekapazität über Buttons auswählen 
    # Session-State initialisieren, damit die Wahl stabil bleibt
    if "batkap" not in st.session_state:
        st.session_state.batkap = 0.0  # Default-Wert in kWh
    
    st.write("🔋 Batteriekapazität [kWh] auswählen:")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        if st.button("0 kWh"):
            st.session_state.batkap = 0.0
    with col2:
        if st.button("6.3 kWh"):
            st.session_state.batkap = 6.3
    with col3:
        if st.button("9.5 kWh"):
            st.session_state.batkap = 9.5
    with col4:
        if st.button("12.6 kWh"):
            st.session_state.batkap = 12.6
    with col5:
        if st.button("15.8 kWh"):
            st.session_state.batkap = 15.8        
    
    batkap = st.session_state.batkap
    st.write(f"🔋 Aktuell gewählte Batteriekapazität: {batkap} kWh")
    
    # --- Insel-Berechnung ---
    einspeisung, netzbezug, eigenverbrauchsquote, autarkiequote = insel.template(
        "Hybridwechselrichter.vseit",
        Verbrauch_MWh=verbrauch,
        kWp_PV=pvleistung,
        Kapazitaet_Batterie=batkap * 1000,
        Wirkungsgrad_Batterie_DC=wirkungsgrad / 100,
    )
    
    st.write(f"⚡ Einspeisung = {round(einspeisung)} kWh", f"sowie 🔌 Netzbezug = {round(netzbezug)} kWh")
    st.progress(
            eigenverbrauchsquote,
            text=f"## 🏠 Eigenverbrauchsquote = {eigenverbrauchsquote * 100:.0f} %",
        )
    
    st.progress(
            autarkiequote,
            text=f"🏝️ Autarkiequote = {autarkiequote * 100:.0f} %",
        )
    
    # Investitionsrechnung NUR, WENN eine Batterie > 0
    
    if batkap > 0:
        # ------------------------------
        # 1. Beschreibung + Zinssatz
        # ------------------------------
        st.write('---')
        st.subheader("💰 Dynamische Investitionsrechnung")

        zinssatz_prozent = st.slider(
            "Zinssatz (Diskontierungszins) in %",
            min_value=0.0,
            max_value=5.0,
            value=2.3,
            step=0.1,
            key="zins_2024",
        )

        zinssatz = zinssatz_prozent / 100.0

        # 2. Varianten passend zur batkap
        # Eric hier musst du ganz tapfer sein!
        # ToDo: Eliminate hardcoded values with variables: ersparnis muss aus einnahmen und ausgaben gg Referenz berechnet werden.
        if batkap == 6.3:
            varianten = {
                "Variante 6,3 kWh": {
                    "invest": 3750,
                    "einnahmen": 356,
                    "ausgaben": 1,
                },
            }
        elif batkap == 9.5:
            varianten = {
                "Variante 9,5 kWh": {
                    "invest": 4900,
                    "einnahmen": 394,
                    "ausgaben": 1,
                },
            }
        elif batkap == 12.6:
            varianten = {
                "Variante 12,6 kWh": {
                    "invest": 6050,
                    "einnahmen": 405,
                    "ausgaben": 1,
                },
            }
        elif batkap == 15.8:
            varianten = {
                "Variante 15,8 kWh": {
                    "invest": 7200,
                    "einnahmen": 410,
                    "ausgaben": 1,
                },
            }
        else:
            varianten = {
                f"Variante {batkap:g} kWh (Default)": {
                    "invest": 20000,
                    "einnahmen": 3000,
                    "ausgaben": 300,
                },
            }

        MAX_JAHRE = 30

        def berechne_amortisationsdauer(invest, einnahmen, ausgaben, zinssatz, max_jahre=30):
            
            kapitalwert = -invest  # Jahr 0: Auszahlung
            verlauf = [(0, kapitalwert)]

            for jahr in range(1, max_jahre + 1):
                netto_cf = einnahmen - ausgaben
                if zinssatz > 0:
                    diskontfaktor = (1 + zinssatz) ** jahr
                    kapitalwert += netto_cf / diskontfaktor
                else:
                    kapitalwert += netto_cf

                verlauf.append((jahr, kapitalwert))

                if kapitalwert >= 0:
                    return float(jahr), verlauf

            return None, verlauf

        max_anzeigejahre = MAX_JAHRE

        for name, daten in varianten.items():
            st.markdown(f"### {name}")

            invest = daten["invest"]
            einnahmen = daten["einnahmen"]
            ausgaben = daten["ausgaben"]

            st.write(f"- **Investitionskosten**: {invest:,.0f} €")

            jahre_bis_amort, verlauf = berechne_amortisationsdauer(
                invest=invest,
                einnahmen=einnahmen,
                ausgaben=ausgaben,
                zinssatz=zinssatz,
                max_jahre=MAX_JAHRE,
            )

            if jahre_bis_amort is None:
                st.error(
                    f"Die Investition amortisiert sich innerhalb von {MAX_JAHRE} Jahren "
                    f"bei einem Zinssatz von {zinssatz_prozent:.1f} % nicht."
                )
                st.progress(100)
            else:
                st.success(
                    f"Amortisationsdauer: ca. {jahre_bis_amort:.0f} Jahre "
                    f"bei einem Zinssatz von {zinssatz_prozent:.1f} %."
                )

                with st.expander("Kapitalwert-Verlauf anzeigen"):
                    import pandas as pd

                    df = pd.DataFrame(verlauf, columns=["Jahr", "Kapitalwert (€)"])
                    st.dataframe(df.style.format({"Kapitalwert (€)": "{:,.0f}"}))

    time.sleep(1.0)
    st.image("templates/Hybridwechselrichter.png")


with right:
    st.header("2025")
    verbrauch_2025 = st.slider("🔌 Verbrauch [MWh/a]", 0.0, 10.0, 6.17, format="%g MWh / a", key=1001)
    pvleistung_2025 = st.slider("🌞 PV Leistung [kWp]", 0.0, 25.0, 13.6, format="%g kWp", key=1002)
    wirkungsgrad_2025 = st.select_slider("🦾 Batteriewirkungsgrad [%]", 
                                         options=[85.0, 86.0, 87.0, 88.0, 89.0, 90.0, 90.5, 91, 91.5, 92, 92.5, 93, 93.5, 94, 94.5, 95.0, 95.5, 96.0, 96.5, 97.0, 97.5, 98.0, 98.5, 99.0, 99.5, 100.0],
                                         value=98.5, 
                                         format_func=lambda x:f"{x:g} %", 
                                         key=1003,
                                         )
    
    # --- Batteriekapazität über Buttons auswählen ---
    
    if "batkap_2025" not in st.session_state:
        st.session_state.batkap_2025 = 0.0  # Default-Wert in kWh
    
    st.write("🔋 Batteriekapazität [kWh] auswählen:")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        if st.button("0 kWh", key=2001):
            st.session_state.batkap_2025 = 0.0
    with col2:
        if st.button("6.3 kWh", key=2002):
            st.session_state.batkap_2025 = 6.3
    with col3:
        if st.button("9.5 kWh", key=2003):
            st.session_state.batkap_2025 = 9.5
    with col4:
        if st.button("12.6 kWh", key=2004):
            st.session_state.batkap_2025 = 12.6
    with col5:
        if st.button("15.8 kWh", key=2005):
            st.session_state.batkap_2025 = 15.8        
    
    batkap_2025 = st.session_state.batkap_2025
    st.write(f"🔋 Aktuell gewählte Batteriekapazität: {batkap_2025} kWh")
    
    # --- Insel-Berechnung ---
    einspeisung_2025, netzbezug_2025, eigenverbrauchsquote_2025, autarkiequote_2025 = insel.template(
        "Hybridwechselrichter2025.vseit",
        Verbrauch_MWh_2025=verbrauch_2025,
        kWp_PV_2025=pvleistung_2025,
        Kapazitaet_Batterie_2025=batkap_2025 * 1000,
        Wirkungsgrad_Batterie_DC_2025=wirkungsgrad_2025 / 100,
    )
    
    st.write(f"⚡ Einspeisung = {round(einspeisung_2025)} kWh", f"sowie 🔌 Netzbezug = {round(netzbezug_2025)} kWh")
    st.progress(
            eigenverbrauchsquote_2025,
            text=f"## 🏠 Eigenverbrauchsquote = {eigenverbrauchsquote_2025 * 100:.0f} %",
        )
    
    st.progress(
            autarkiequote_2025,
            text=f"🏝️ Autarkiequote = {autarkiequote_2025 * 100:.0f} %",
        )

    # Investitionsrechnung rechts: NUR, WENN batkap_2025 > 0
    if batkap_2025 > 0:
        st.write('---')
        st.subheader("💰 Dynamische Investitionsrechnung")

        zinssatz_prozent_2025 = st.slider(
            "Zinssatz (Diskontierungszins) in %",
            min_value=0.0,
            max_value=5.0,
            value=2.3,
            step=0.1,
            key="zins_2025",
        )

        zinssatz_2025 = zinssatz_prozent_2025 / 100.0

        #ToDo siehe 'with left'
        if batkap_2025 == 6.3:
            varianten_2025 = {
                "Variante 6,3 kWh": {
                    "invest": 3750,
                    "einnahmen": 332,
                    "ausgaben": 1,
                },
            }
        elif batkap_2025 == 9.5:
            varianten_2025 = {
                "Variante 9,5 kWh": {
                    "invest": 4900,
                    "einnahmen": 381,
                    "ausgaben": 1,
                },
            }
        elif batkap_2025 == 12.6:
            varianten_2025 = {
                "Variante 12,6 kWh": {
                    "invest": 6050,
                    "einnahmen": 403,
                    "ausgaben": 1,
                },
            }
        elif batkap_2025 == 15.8:
            varianten_2025 = {
                "Variante 15,8 kWh": {
                    "invest": 7200,
                    "einnahmen": 415,
                    "ausgaben": 1,
                },
            }
        else:
            varianten_2025 = {
                f"Variante {batkap_2025:g} kWh (Default)": {
                    "invest": 20000,
                    "einnahmen": 3000,
                    "ausgaben": 300,
                },
            }

        MAX_JAHRE_2025 = 30

        def berechne_amortisationsdauer_2025(invest, einnahmen, ausgaben, zinssatz, max_jahre=30):
            kapitalwert = -invest
            verlauf = [(0, kapitalwert)]

            for jahr in range(1, max_jahre + 1):
                netto_cf = einnahmen - ausgaben
                if zinssatz > 0:
                    diskontfaktor = (1 + zinssatz) ** jahr
                    kapitalwert += netto_cf / diskontfaktor
                else:
                    kapitalwert += netto_cf

                verlauf.append((jahr, kapitalwert))

                if kapitalwert >= 0:
                    return float(jahr), verlauf

            return None, verlauf

        max_anzeigejahre_2025 = MAX_JAHRE_2025

        for name, daten in varianten_2025.items():
            st.markdown(f"### {name}")

            invest = daten["invest"]
            einnahmen = daten["einnahmen"]
            ausgaben = daten["ausgaben"]

            st.write(f"- **Investitionskosten**: {invest:,.0f} €")

            jahre_bis_amort, verlauf = berechne_amortisationsdauer_2025(
                invest=invest,
                einnahmen=einnahmen,
                ausgaben=ausgaben,
                zinssatz=zinssatz_2025,
                max_jahre=MAX_JAHRE_2025,
            )

            if jahre_bis_amort is None:
                st.error(
                    f"Die Investition amortisiert sich innerhalb von {MAX_JAHRE_2025} Jahren "
                    f"bei einem Zinssatz von {zinssatz_prozent_2025:.1f} % nicht."
                )
                st.progress(100)
            else:
                st.success(
                    f"Amortisationsdauer: ca. {jahre_bis_amort:.0f} Jahre "
                    f"bei einem Zinssatz von {zinssatz_prozent_2025:.1f} %."
                )

                with st.expander("Kapitalwert-Verlauf anzeigen"):
                    import pandas as pd

                    df = pd.DataFrame(verlauf, columns=["Jahr", "Kapitalwert (€)"])
                    st.dataframe(df.style.format({"Kapitalwert (€)": "{:,.0f}"}))

    time.sleep(1.0)
    st.image("templates/Hybridwechselrichter2025.png")
