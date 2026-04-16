import streamlit as st
from supabase import create_client

# Supabase Daten
SUPABASE_URL = "DEINE_URL_HIER"
SUPABASE_KEY = "DEIN_KEY_HIER"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

st.title("Fundsachen App")

# Kategorien laden
kategorien = supabase.table("kategorien").select("*").execute().data

kategorie_namen = [k["name"] for k in kategorien]

# Eingabeformular
name = st.text_input("Name des Gegenstands")
beschreibung = st.text_area("Beschreibung")
fundort = st.text_input("Fundort")
kategorie = st.selectbox("Kategorie", kategorie_namen)

if st.button("Speichern"):
    # passende Kategorie-ID finden
    kategorie_id = next(k["id"] for k in kategorien if k["name"] == kategorie)

    # in Datenbank speichern
    supabase.table("fundsachen").insert({
        "name": name,
        "beschreibung": beschreibung,
        "fundort": fundort,
        "kategorie_id": kategorie_id
    }).execute()

    st.success("Gespeichert!")

# Anzeige der Fundsachen
st.subheader("Gespeicherte Fundsachen")

data = supabase.table("fundsachen").select("*").execute().data

for item in data:
    st.write(item)
