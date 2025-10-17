import streamlit as st
import pandas as pd
from supabase import create_client, Client

# ---------------------------------------------------------
#  APP-GRUNDEINSTELLUNGEN
# ---------------------------------------------------------
st.set_page_config(page_title="Bundesliga Tipprunde", page_icon="⚽")

# ---------------------------------------------------------
#  SUPABASE-VERBINDUNG (aus Secrets)
# ---------------------------------------------------------
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase: create_client(url, key)

# ---------------------------------------------------------
#  LOGIN-BEREICH
# ---------------------------------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.team = None

if not st.session_state.logged_in:
    st.title("⚽ Bundesliga Tipprunde – Login")

    email = st.text_input("E-Mail")
    password = st.text_input("Passwort", type="password")

    if st.button("Login"):
        result = (
            supabase.table("users")
            .select("*")
            .eq("email", email)
            .eq("password", password)
            .execute()
        )

        if result.data:
            st.session_state.logged_in = True
            st.session_state.team = result.data[0]["team"]
            st.success(f"Willkommen, {st.session_state.team}! 👋")
            st.rerun()
        else:
            st.error("❌ Falsche E-Mail oder Passwort.")
    st.stop()

# ---------------------------------------------------------
#  SPIELELISTE & OPTIONEN
# ---------------------------------------------------------
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

optionen = ["🏠 Heimsieg", "🤝 Unentschieden", "🚗 Auswärtssieg"]

# ---------------------------------------------------------
#  SEITENKOPF MIT WETTEINSATZ
# ---------------------------------------------------------
st.title("⚽ Bundesliga Tipprunde")
st.subheader(f"Eingeloggt als: {st.session_state.team}")

# 🍕 Wetteinsatz-Anzeige
einsatz_text = "🍕 **Wetteinsatz:** Ninje & Mina gewinnen = 5 blackBIKE classes Lenny & MJ gewinnen = 5 Gänge Menü gekocht von Ninje&Mina"
st.markdown(einsatz_text)
st.divider()

# ---------------------------------------------------------
#  TIPPABGABE
# ---------------------------------------------------------
data = []

for i, (home, away) in enumerate(spiele, start=1):
    spiel = f"{home} vs {away}"

    # vorhandene Tipps des Teams laden
    existing = (
        supabase.table("tipps")
        .select("tipp")
        .eq("spiel", spiel)
        .eq("team", st.session_state.team)
        .execute()
    )

    default_idx = 0
    if existing.data:
        try:
            default_idx = optionen.index(existing.data[0]["tipp"])
        except ValueError:
            default_idx = 0

    tipp = st.radio(
        f"Spiel {i}: {spiel}",
        optionen,
        index=default_idx,
        key=f"radio_{i}",
    )

    data.append({"spiel": spiel, "team": st.session_state.team, "tipp": tipp})
    st.markdown("---")

# ---------------------------------------------------------
#  TIPPS SPEICHERN
# ---------------------------------------------------------
if st.button("💾 Tipps speichern"):
    for row in data:
        supabase.table("tipps").upsert(row, on_conflict=["spiel", "team"]).execute()
    st.success("✅ Tipps erfolgreich gespeichert!")

# ---------------------------------------------------------
#  ÜBERSICHT ALLER TIPPS
# ---------------------------------------------------------
st.subheader("📊 Übersicht aller Tipps")

all_tipps = supabase.table("tipps").select("*").execute()
if all_tipps.data:
    df = pd.DataFrame(all_tipps.data)

    # Teamanzeige schöner machen
    df["team"] = df["team"].replace({
        "Team1": "Ninje & Mina",
        "Team2": "Lenny & MJ"
    })

    st.dataframe(df, hide_index=True, use_container_width=True)
else:
    st.info("Noch keine Tipps vorhanden.")

# ---------------------------------------------------------
#  LOGOUT-BUTTON
# ---------------------------------------------------------
st.divider()
if st.button("🚪 Logout"):
    st.session_state.logged_in = False
    st.session_state.team = None
    st.rerun()
