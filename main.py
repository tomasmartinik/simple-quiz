import streamlit as st
import random
import os
import json

st.set_page_config(page_title="Flashcards Quizlet", page_icon="🧠")

# Flashcards data
default_flashcards = {
    "Co je hlavní město ČR?": "Praha",
    "Kolik je 7 * 8?": "56",
    "Kdo napsal Babičku?": "Božena Němcová",
    "Hlavní město Slovenska?": "Bratislava",
    "Největší oceán světa?": "Tichý oceán",
    "Kolik má člověk zubů?": "32"
}

# Function to load sets from the 'sets' folder
def load_sets():
    sets_path = "sets"
    sets = {}
    if os.path.exists(sets_path):
        for file_name in os.listdir(sets_path):
            if file_name.endswith(".json"):
                with open(os.path.join(sets_path, file_name), "r") as f:
                    sets[file_name[:-5]] = json.load(f)
    return sets

# Function to load configuration for each set
def load_set_config(set_name):
    config_path = os.path.join("conf", f"{set_name}.json")
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            return json.load(f)
    return {"title": f"Flashcards Quizlet - {set_name}", "background_color": "#007BFF"}  # Default title and blue color

# Load available sets
available_sets = load_sets()

# Inicializace
if "original_cards" not in st.session_state:
    st.session_state.original_cards = list(default_flashcards.items())
    st.session_state.cards = st.session_state.original_cards.copy()
    st.session_state.index = 0
    st.session_state.show_answer = False
    st.session_state.viewed = 0
    st.session_state.mode = "all"  # "all" nebo "review"
    st.session_state.known_status = {
        q: "unseen" for q, _ in st.session_state.original_cards
    }

def flip():
    st.session_state.show_answer = not st.session_state.show_answer

def next_card():
    st.session_state.index = (st.session_state.index + 1) % len(st.session_state.cards)
    st.session_state.show_answer = False
    st.session_state.viewed += 1

def mark(status):
    question, _ = st.session_state.cards[st.session_state.index]
    st.session_state.known_status[question] = status
    next_card()

def reshuffle():
    st.session_state.cards = st.session_state.original_cards.copy()
    random.shuffle(st.session_state.cards)
    reset_progress()
    st.session_state.mode = "all"
    st.success("Kartičky byly zamíchány.")

def reset_order():
    st.session_state.cards = st.session_state.original_cards.copy()
    reset_progress()
    st.session_state.mode = "all"
    st.success("Pořadí bylo resetováno.")

def reset_progress():
    st.session_state.index = 0
    st.session_state.viewed = 0
    st.session_state.show_answer = False

def review_unknown():
    # Filtruj kartičky, které jsou stále označené jako "unknown"
    unknown_cards = [item for item in st.session_state.original_cards if st.session_state.known_status[item[0]] == "unknown"]
    if not unknown_cards:
        st.warning("Žádné aktuálně neznámé kartičky.")
        return
    st.session_state.cards = unknown_cards
    random.shuffle(st.session_state.cards)
    reset_progress()
    st.session_state.mode = "review"
    st.success("Zobrazuji aktuálně neznámé kartičky.")

def back_to_all():
    st.session_state.cards = st.session_state.original_cards.copy()
    reset_progress()
    st.session_state.mode = "all"
    st.success("Zpět ke všem kartám.")

# Load configuration for the selected set
if 'set_title' in st.session_state:
    set_config = load_set_config(st.session_state.set_title)
else:
    set_config = {"title": "Flashcards Quizlet", "background_color": "#007BFF"}

# Title with set name and background color
st.markdown(f"<div style='background-color: {set_config['background_color']}; padding: 10px; border-radius: 5px;'>", unsafe_allow_html=True)
st.title(set_config['title'])
st.markdown("</div>", unsafe_allow_html=True)

# Sidebar for navigation
with st.sidebar:
    st.header("Navigace")
    st.button("Zamíchat", on_click=reshuffle)
    st.button("Původní pořadí", on_click=reset_order)
    st.button("Opakovat neznámé", on_click=review_unknown)
    if st.session_state.mode == "review":
        st.button("Zpět ke všem kartám", on_click=back_to_all)

# Sidebar for selecting a set
with st.sidebar:
    st.header("Vyberte sadu")
    selected_set = st.selectbox("Dostupné sady", options=list(available_sets.keys()))
    if st.button("Načíst sadu"):
        st.session_state.original_cards = list(available_sets[selected_set].items())
        st.session_state.cards = st.session_state.original_cards.copy()
        reset_progress()
        st.success(f"Sada '{selected_set}' byla načtena.")

# Main content with improved layout
if 'cards' in st.session_state and st.session_state.cards:
    total = len(st.session_state.cards)
    known_count = sum(1 for status in st.session_state.known_status.values() if status == "known")
    unknown_count = sum(1 for status in st.session_state.known_status.values() if status == "unknown")

    st.markdown(f"""
    - 👁️ Viděno: **{st.session_state.viewed}**
    - ✅ Známé: **{known_count}**
    - ❌ Neznámé: **{unknown_count}**
    """)

    st.markdown(f"**Kartička {st.session_state.index + 1} z {total}**")
    st.progress((st.session_state.index + 1) / total, text=f"{st.session_state.index + 1}/{total}")

    # Flashcard display
    question, answer = st.session_state.cards[st.session_state.index]

    st.markdown("### Otázka:")
    st.markdown(f"<div style='background-color: {set_config['background_color']}; padding: 10px; border-radius: 5px;'>", unsafe_allow_html=True)
    st.info(question)
    st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.show_answer:
        st.markdown("### Odpověď:")
        st.success(answer)

        # Action buttons styled as horizontal layout
        col1, col2 = st.columns(2, gap="large")
        with col1:
            st.button("✅ Znám", on_click=lambda: mark("known"), help="Označte tuto otázku jako známou.")
        with col2:
            st.button("❌ Neznám", on_click=lambda: mark("unknown"), help="Označte tuto otázku jako neznámou.")
    else:
        st.button("Zobrazit odpověď", on_click=flip, help="Zobrazí odpověď na aktuální otázku.")
