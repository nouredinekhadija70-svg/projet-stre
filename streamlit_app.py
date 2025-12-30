import streamlit as st
from transformers import pipeline
from datetime import datetime
import re
import string

# --- 1. FONCTION DE NETTOYAGE (Preprocessing) ---
def clean_text(text):
    """
    Nettoie le texte avant l'analyse pour améliorer la précision.
    """
    # Mise en minuscule
    text = text.lower()
    # Suppression des URLs
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    # Suppression de la ponctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    # Suppression des espaces superflus
    text = text.strip()
    return text

# --- 2. CONFIGURATION DE L'IA ---
@st.cache_resource
def load_model():
    try:
        # Modèle BERT Multilingue
        model = pipeline(
            "sentiment-analysis", 
            model="nlptown/bert-base-multilingual-uncased-sentiment"
        )
        return model, True
    except Exception as e:
        return None, False

classifier, model_ready = load_model()

# --- 3. CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="IA Sentiment", page_icon="🎯", layout="wide")

# Initialisation des variables de session
if 'history' not in st.session_state:
    st.session_state.history = []
if 'language' not in st.session_state:
    st.session_state.language = 'fr'
if 'current_text' not in st.session_state:
    st.session_state.current_text = ''

# [Dictionnaires de traductions et CSS - Gardés de votre code original]
translations = {
    'fr': {
        'title': '🎯 Analyseur de Sentiment IA',
        'subtitle': '✨ Analyse avec Nettoyage de Données ✨',
        'input_label': '💬 Partagez votre texte :',
        'analyze_btn': '🚀 Analyser maintenant',
        'positive': 'Sentiment Positif',
        'negative': 'Sentiment Négatif',
        'confidence': 'Confiance de l\'IA',
        'history': '📜 Historique des Analyses',
        'clear_history': '🗑️ Effacer tout',
        'no_history': 'Aucun historique.',
        'language': '🌍 Langue',
        'raw_text': 'Texte brut',
        'cleaned_text': 'Texte nettoyé'
    },
    'en': {
        'title': '🎯 AI Sentiment Analyzer',
        'subtitle': '✨ Analysis with Data Cleaning ✨',
        'input_label': '💬 Share your text:',
        'analyze_btn': '🚀 Analyze now',
        'positive': 'Positive Sentiment',
        'negative': 'Negative Sentiment',
        'confidence': 'AI Confidence',
        'history': '📜 Analysis History',
        'clear_history': '🗑️ Clear all',
        'no_history': 'No history yet.',
        'language': '🌍 Language',
        'raw_text': 'Raw text',
        'cleaned_text': 'Cleaned text'
    }
}
# (Note: Vous pouvez rajouter vos versions AR et ES ici)

def t(key):
    return translations.get(st.session_state.language, translations['fr']).get(key, key)

# --- 4. SIDEBAR ET HISTORIQUE ---
with st.sidebar:
    st.header(f"⚙️ {t('language')}")
    st.session_state.language = st.selectbox("Select Language", ['fr', 'en'], index=0)
    
    st.divider()
    st.header(t('history'))
    
    if st.session_state.history:
        if st.button(t('clear_history')):
            st.session_state.history = []
            st.rerun()
        
        # Affichage de l'historique de manière propre
        for item in reversed(st.session_state.history):
            with st.expander(f"{item['emoji']} {item['timestamp']}"):
                st.write(f"**Texte:** {item['text']}")
                st.write(f"**Score:** {item['score']:.1%}")
    else:
        st.info(t('no_history'))

# --- 5. INTERFACE PRINCIPALE ---
st.markdown(f"<h1 style='text-align: center;'>{t('title')}</h1>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    user_input = st.text_area(t('input_label'), height=150)
    
    if st.button(t('analyze_btn'), use_container_width=True):
        if user_input.strip():
            # ÉTAPE DE NETTOYAGE
            cleaned = clean_text(user_input)
            
            with st.spinner("Analyse en cours..."):
                # ANALYSE IA
                result = classifier(cleaned)[0]
                star_value = int(result['label'].split()[0])
                label = "POSITIVE" if star_value >= 4 else "NEGATIVE"
                score = result['score']
                
                # ENREGISTREMENT DANS L'HISTORIQUE
                new_entry = {
                    'text': user_input,
                    'cleaned': cleaned,
                    'label': label,
                    'score': score,
                    'timestamp': datetime.now().strftime("%H:%M:%S"),
                    'emoji': '😊' if label == "POSITIVE" else '😔'
                }
                st.session_state.history.append(new_entry)
                
                # AFFICHAGE DU RÉSULTAT
                st.subheader(f"{new_entry['emoji']} {t('positive') if label == 'POSITIVE' else t('negative')}")
                st.progress(score)
                st.write(f"**{t('confidence')}:** {score:.1%}")
                
                # Affichage du nettoyage pour le Master
                with st.expander("🛠️ Détails du prétraitement (Preprocessing)"):
                    st.write(f"**{t('raw_text')}:** `{user_input}`")
                    st.write(f"**{t('cleaned_text')}:** `{cleaned}`")
                
                st.balloons()

# CSS pour le fond dégradé (VOTRE DESIGN)
st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }
    .stTextArea textarea { border-radius: 15px; }
</style>
""", unsafe_allow_html=True)
