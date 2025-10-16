import streamlit as st
import pandas as pd

st.set_page_config(page_title="Bundesliga Tipprunde", page_icon="⚽")

# --- Einstellungen ---
spiele = [
    ("Union Berlin", "Borussia Mönchengladbach"),
    ("Mainz", "Bayer Leverkusen"),
    ("RB Leipzig", "HSV"),
    ("Wolfsburg", "VFB Stuttgart"),
    ("1. FC Heidenheim", "Werder Bremen"),
    ("Köln", "Augsburg"),
    ("Bayern München", "Borussia Dortmund"),
    ("SC Freiburg", "Frankfurt"),
    ("St. Pauli", "TSG Hoffenheim")
]

team1 = "Ninje & Mina"
team2 = "Lenny & MJ"
einsatz = "Ninje & Mina gewinnen = 5 blackBIKE classes Lenny & MJ gewinnen = 5 Gänge Menü gekocht von Ninje & Mina"

st.title("⚽ Bundesliga Tipprunde")
st.subheader(f"Wetteinsatz: {einsatz}")
st.divider()

# --- Tipp-Auswahl ---
optionen = ["🏠 Heimsieg", "🤝 Unentschieden", "🚗 Auswärtssieg"]
data = []

for i, (home, away) in enumerate(spiele, start=1):
    st.markdown(f"### Spiel {i}: {home} vs {away}")
    c1, c2, c3 = st.columns([3, 3, 3])

    with c2:
        tipp_team1 = st.radio(
            f"{team1} Tipp",
            optionen,
            key=f"t1_{i}",
            horizontal=True
        )
    with c3:
        tipp_team2 = st.radio(
            f"{team2} Tipp",
            optionen,
            key=f"t2_{i}",
            horizontal=True
        )

    data.append({
        "Spiel": f"{home} vs {away}",
        team1: tipp_team1,
        team2: tipp_team2
    })
    st.divider()

# --- Anzeige als Tabelle ---
df = pd.DataFrame(data)
st.subheader("📝 Übersicht eurer Tipps")
st.dataframe(df, hide_index=True)

# --- Optional speichern ---
if st.button("💾 Tipps speichern"):
    df.to_csv("tipps.csv", index=False, encoding="utf-8-sig")
    st.success("Tipps gespeichert! (Datei: tipps.csv)")
