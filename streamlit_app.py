import streamlit as st
from transformers import pipeline
from datetime import datetime
import torch

# --- 1. CONFIGURATION DE L'IA (Ancien code main.py intégré) ---
@st.cache_resource # Charge le modèle une seule fois pour économiser la mémoire
def load_model():
    try:
        # Modèle Multilingue BERT (FR, EN, ES, AR)
        model = pipeline(
            "sentiment-analysis", 
            model="nlptown/bert-base-multilingual-uncased-sentiment"
        )
        return model, True
    except Exception as e:
        return None, False

classifier, model_ready = load_model()

# --- 2. CONFIGURATION DE LA PAGE STREAMLIT ---
st.set_page_config(
    page_title="Analyseur de Sentiment IA",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialisation de l'état de session
if 'history' not in st.session_state:
    st.session_state.history = []
if 'language' not in st.session_state:
    st.session_state.language = 'fr'
if 'current_text' not in st.session_state:
    st.session_state.current_text = ''

# --- 3. DICTIONNAIRES DE TRADUCTIONS (VOS TRADUCTIONS) ---
translations = {
    'fr': {
        'title': '🎯 Analyseur de Sentiment IA',
        'subtitle': '✨ Analyse instantanée alimentée par l\'Intelligence Artificielle ✨',
        'input_label': '💬 Partagez votre texte :',
        'placeholder': 'Ex: Cette application est absolument géniale ! J\'adore l\'interface moderne et intuitive...',
        'analyze_btn': '🚀 Analyser maintenant',
        'warning_empty': '⚠️ Veuillez entrer du texte pour l\'analyser.',
        'analyzing': '🔮 L\'IA analyse votre texte en profondeur...',
        'positive': 'Sentiment Positif',
        'negative': 'Sentiment Négatif',
        'confidence': 'Confiance de l\'IA',
        'sentiment': 'Sentiment',
        'words_analyzed': 'Mots analysés',
        'error_server': '❌ Erreur lors du traitement IA.',
        'how_it_works': 'ℹ️ Comment ça fonctionne ?',
        'examples': '📚 Exemples de phrases',
        'history': '📜 Historique',
        'clear_history': '🗑️ Effacer l\'historique',
        'no_history': 'Aucune analyse effectuée pour le moment.',
        'language': '🌍 Langue',
        'footer': 'Projet Master - Framework AI',
        'powered_by': 'Propulsé par ❤️ et Intelligence Artificielle',
    },
    'en': {
        'title': '🎯 AI Sentiment Analyzer',
        'subtitle': '✨ Instant Analysis Powered by Artificial Intelligence ✨',
        'input_label': '💬 Share your text:',
        'placeholder': 'Ex: This application is absolutely amazing! I love the modern and intuitive interface...',
        'analyze_btn': '🚀 Analyze now',
        'warning_empty': '⚠️ Please enter text to analyze.',
        'analyzing': '🔮 AI is analyzing your text in depth...',
        'positive': 'Positive Sentiment',
        'negative': 'Negative Sentiment',
        'confidence': 'AI Confidence',
        'sentiment': 'Sentiment',
        'words_analyzed': 'Words analyzed',
        'error_server': '❌ AI processing error.',
        'how_it_works': 'ℹ️ How does it work?',
        'examples': '📚 Sample sentences',
        'history': '📜 History',
        'clear_history': '🗑️ Clear history',
        'no_history': 'No analysis performed yet.',
        'language': '🌍 Language',
        'footer': 'Master Project - AI Framework',
        'powered_by': 'Powered by ❤️ and Artificial Intelligence',
    },
    'es': {
        'title': '🎯 Analizador de Sentimientos IA',
        'subtitle': '✨ Análisis instantáneo impulsado por Inteligencia Artificial ✨',
        'input_label': '💬 Comparte tu texto:',
        'placeholder': 'Ej: ¡Esta aplicación es absolutamente genial! Me encanta la interfaz moderna e intuitiva...',
        'analyze_btn': '🚀 Analizar ahora',
        'warning_empty': '⚠️ Por favor ingrese texto para analizar.',
        'analyzing': '🔮 La IA está analizando tu texto en profundidad...',
        'positive': 'Sentimiento Positivo',
        'negative': 'Sentimiento Negativo',
        'confidence': 'Confianza de la IA',
        'sentiment': 'Sentimiento',
        'words_analyzed': 'Palabras analizadas',
        'error_server': '❌ Error en el procesamiento de IA.',
        'how_it_works': 'ℹ️ ¿Cómo funciona?',
        'examples': '📚 Frases de ejemplo',
        'history': '📜 Historial',
        'clear_history': '🗑️ Borrar historial',
        'no_history': 'No se ha realizado ningún análisis aún.',
        'language': '🌍 Idioma',
        'footer': 'Proyecto Máster - Framework IA',
        'powered_by': 'Impulsado por ❤️ e Inteligencia Artificial',
    },
    'ar': {
        'title': '🎯 محلل المشاعر بالذكاء الاصطناعي',
        'subtitle': '✨ تحليل فوري مدعوم بالذكاء الاصطناعي ✨',
        'input_label': '💬 شارك نصك:',
        'placeholder': 'مثال: هذا التطبيق رائع للغاية! أحب الواجهة الحديثة والبديهية...',
        'analyze_btn': '🚀 تحليل الآن',
        'warning_empty': '⚠️ يرجى إدخال نص للتحليل.',
        'analyzing': '🔮 الذكاء الاصطناعي يحلل نصك بعمق...',
        'positive': 'مشاعر إيجابية',
        'negative': 'مشاعر سلبية',
        'confidence': 'ثقة الذكاء الاصطناعي',
        'sentiment': 'المشاعر',
        'words_analyzed': 'الكلمات المحللة',
        'error_server': '❌ خطأ في معالجة الذكاء الاصطناعي.',
        'how_it_works': 'ℹ️ كيف يعمل؟',
        'examples': '📚 أمثلة على الجمل',
        'history': '📜 السجل',
        'clear_history': '🗑️ مسح السجل',
        'no_history': 'لم يتم إجراء أي تحليل حتى الآن.',
        'language': '🌍 اللغة',
        'footer': 'مشروع الماجستير - إطار الذكاء الاصطناعي',
        'powered_by': 'مدعوم بـ ❤️ والذكاء الاصطناعي',
    }
}

# --- 4. EXEMPLES ---
example_datasets = {
    'fr': ["J'adore cette application, elle est incroyable et très intuitive !", "Le service client est excellent.", "Quelle déception ! Produit nul."],
    'en': ["I love this application, it's amazing!", "Excellent customer service.", "What a disappointment! Bad product."],
    'es': ["¡Me encanta esta aplicación!", "El servicio al cliente es excelente.", "¡Qué decepción! Producto malo."],
    'ar': ["أحب هذا التطبيق، إنه مذهل!", "خدمة العملاء ممتازة.", "يا للخيبة! منتج سيء."]
}

def t(key):
    return translations[st.session_state.language].get(key, key)

# --- 5. STYLE CSS (VOTRE DESIGN) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;800&family=Inter:wght@300;400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #4facfe 75%, #00f2fe 100%);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
    }
    @keyframes gradient { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }
    .title { font-size: 3.5rem; font-weight: 800; text-align: center; color: white; margin-bottom: 1rem; }
    .subtitle { text-align: center; color: white; font-size: 1.2rem; margin-bottom: 2rem; }
    .stTextArea textarea { background: rgba(255, 255, 255, 0.9) !important; border-radius: 15px !important; }
    .stButton button { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important; color: white !important; border-radius: 50px !important; }
    .result-box { background: rgba(255, 255, 255, 0.95); border-radius: 20px; padding: 2rem; margin-top: 2rem; }
    .positive-result { border-left: 6px solid #10b981; }
    .negative-result { border-left: 6px solid #ef4444; }
    .footer { text-align: center; color: white; margin-top: 3rem; }
</style>
""", unsafe_allow_html=True)

# --- 6. SIDEBAR ---
with st.sidebar:
    st.markdown("## ⚙️ Options")
    lang_options = {'fr': '🇫🇷 Français', 'en': '🇬🇧 English', 'es': '🇪🇸 Español', 'ar': '🇸🇦 العربية'}
    selected_lang = st.selectbox(t('language'), options=list(lang_options.keys()), format_func=lambda x: lang_options[x], index=list(lang_options.keys()).index(st.session_state.language))
    if selected_lang != st.session_state.language:
        st.session_state.language = selected_lang
        st.rerun()
    
    st.markdown(f"### {t('examples')}")
    for i, example in enumerate(example_datasets[st.session_state.language][:3]):
        if st.button(f"📝 Exemple {i+1}", key=f"ex_{i}", use_container_width=True):
            st.session_state.current_text = example
            st.rerun()
    
    st.markdown("### 📜 Historique")
    if st.session_state.history:
        if st.button(t('clear_history'), use_container_width=True):
            st.session_state.history = []
            st.rerun()

# --- 7. CONTENU PRINCIPAL ---
st.markdown(f'<h1 class="title">{t("title")}</h1>', unsafe_allow_html=True)
st.markdown(f'<p class="subtitle">{t("subtitle")}</p>', unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 3, 1])

with col2:
    user_text = st.text_area(t('input_label'), value=st.session_state.current_text, placeholder=t('placeholder'), height=200)
    
    if st.button(t('analyze_btn'), use_container_width=True):
        if user_text.strip() == "":
            st.warning(t('warning_empty'))
        elif not model_ready:
            st.error("Désolé, le modèle IA n'est pas disponible pour le moment.")
        else:
            with st.spinner(t('analyzing')):
                try:
                    # ANALYSE IA DIRECTE (Remplaçant l'appel API)
                    result = classifier(user_text)[0]
                    star_value = int(result['label'].split()[0])
                    label = "POSITIVE" if star_value >= 4 else "NEGATIVE"
                    score = result['score']

                    # Historique
                    history_item = {
                        'text': user_text, 'label': label, 'score': score,
                        'timestamp': datetime.now().strftime("%H:%M:%S"),
                        'emoji': '😊' if label == "POSITIVE" else '😔'
                    }
                    st.session_state.history.append(history_item)

                    # Affichage
                    result_class = "positive-result" if label == "POSITIVE" else "negative-result"
                    st.markdown(f"""
                    <div class="result-box {result_class}">
                        <h2 style="margin: 0;">{'😊' if label == "POSITIVE" else '😔'} {t('positive') if label == "POSITIVE" else t('negative')}</h2>
                        <p>{t('confidence')} : <strong>{score:.1%}</strong></p>
                    </div>
                    """, unsafe_allow_html=True)
                    st.progress(score)
                    st.balloons()
                    
                except Exception as e:
                    st.error(f"Erreur : {str(e)}")

# --- 8. FOOTER ---
st.markdown(f'<div class="footer"><p>🎓 {t("footer")} | {datetime.now().year}</p></div>', unsafe_allow_html=True)
