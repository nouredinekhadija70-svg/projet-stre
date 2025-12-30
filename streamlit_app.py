import streamlit as st
import requests
from datetime import datetime
import json

# Configuration de la page avec thème sombre
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

# Traductions
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
        'error_server': '❌ Le serveur FastAPI a répondu avec une erreur. Veuillez réessayer.',
        'error_timeout': '⏱️ Délai d\'attente dépassé. Le serveur met trop de temps à répondre.',
        'error_connection': '🔌 Impossible de contacter l\'API. Assurez-vous que le serveur FastAPI est lancé sur http://127.0.0.1:8000',
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
        'error_server': '❌ The FastAPI server responded with an error. Please try again.',
        'error_timeout': '⏱️ Timeout exceeded. The server is taking too long to respond.',
        'error_connection': '🔌 Unable to contact the API. Make sure the FastAPI server is running on http://127.0.0.1:8000',
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
        'error_server': '❌ El servidor FastAPI respondió con un error. Por favor intente nuevamente.',
        'error_timeout': '⏱️ Tiempo de espera excedido. El servidor está tardando demasiado en responder.',
        'error_connection': '🔌 No se puede contactar con la API. Asegúrese de que el servidor FastAPI esté ejecutándose en http://127.0.0.1:8000',
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
        'error_server': '❌ استجاب خادم FastAPI بخطأ. يرجى المحاولة مرة أخرى.',
        'error_timeout': '⏱️ انتهت المهلة الزمنية. الخادم يستغرق وقتًا طويلاً للرد.',
        'error_connection': '🔌 تعذر الاتصال بواجهة برمجة التطبيقات. تأكد من تشغيل خادم FastAPI على http://127.0.0.1:8000',
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

# Dataset d'exemples de phrases
example_datasets = {
    'fr': [
        "J'adore cette application, elle est incroyable et très intuitive !",
        "Le service client est excellent, j'ai reçu une aide rapide et efficace.",
        "Quelle déception ! Le produit ne correspond pas du tout à la description.",
        "Je suis très satisfait de mon achat, la qualité est au rendez-vous.",
        "C'est horrible, je ne recommande absolument pas cette expérience.",
        "Une expérience formidable ! Je reviendrai certainement.",
    ],
    'en': [
        "I love this application, it's amazing and very intuitive!",
        "The customer service is excellent, I received quick and efficient help.",
        "What a disappointment! The product doesn't match the description at all.",
        "I'm very satisfied with my purchase, the quality is there.",
        "It's horrible, I absolutely don't recommend this experience.",
        "A wonderful experience! I will definitely come back.",
    ],
    'es': [
        "¡Me encanta esta aplicación, es increíble y muy intuitiva!",
        "El servicio al cliente es excelente, recibí ayuda rápida y eficiente.",
        "¡Qué decepción! El producto no coincide en absoluto con la descripción.",
        "Estoy muy satisfecho con mi compra, la calidad está presente.",
        "Es horrible, no recomiendo absolutamente esta experiencia.",
        "¡Una experiencia maravillosa! Definitivamente volveré.",
    ],
    'ar': [
        "أحب هذا التطبيق، إنه مذهل وسهل الاستخدام للغاية!",
        "خدمة العملاء ممتازة، تلقيت مساعدة سريعة وفعالة.",
        "يا للخيبة! المنتج لا يتطابق مع الوصف على الإطلاق.",
        "أنا راضٍ جدًا عن عملية الشراء، الجودة موجودة.",
        "إنه فظيع، لا أوصي بهذه التجربة على الإطلاق.",
        "تجربة رائعة! سأعود بالتأكيد.",
    ]
}

# Fonction pour obtenir la traduction
def t(key):
    return translations[st.session_state.language].get(key, key)

# CSS personnalisé pour un design moderne et attractif
st.markdown("""
<style>
    /* Import Google Fonts - Polices élégantes */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;800&family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Application de la police globale */
    html, body, [class*="css"] {
        font-family: 'Inter', 'Poppins', sans-serif;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Poppins', sans-serif;
        font-weight: 700;
    }
    
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #4facfe 75%, #00f2fe 100%);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .main-container {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 30px;
        padding: 3rem;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        border: 1px solid rgba(255, 255, 255, 0.18);
        margin: 2rem auto;
        max-width: 900px;
    }
    
    .title {
        font-size: 3.5rem;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(120deg, #ffffff, #e0e7ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        font-family: 'Poppins', sans-serif;
    }
    
    .subtitle {
        text-align: center;
        color: #ffffff;
        font-size: 1.2rem;
        margin-bottom: 2rem;
        font-weight: 300;
        font-family: 'Inter', sans-serif;
    }
    
    .stTextArea textarea {
        background: rgba(255, 255, 255, 0.9) !important;
        border-radius: 15px !important;
        border: 2px solid rgba(255, 255, 255, 0.3) !important;
        font-size: 1.1rem !important;
        padding: 1rem !important;
        transition: all 0.3s ease !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    .stTextArea textarea:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 20px rgba(102, 126, 234, 0.4) !important;
        transform: scale(1.02);
    }
    
    .stButton button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 50px !important;
        padding: 0.8rem 3rem !important;
        font-size: 1.2rem !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4) !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
        font-family: 'Poppins', sans-serif !important;
    }
    
    .stButton button:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 25px rgba(102, 126, 234, 0.6) !important;
    }
    
    .result-box {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 2rem;
        margin-top: 2rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        animation: slideIn 0.5s ease-out;
        font-family: 'Inter', sans-serif;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .positive-result {
        border-left: 6px solid #10b981;
    }
    
    .negative-result {
        border-left: 6px solid #ef4444;
    }
    
    .history-item {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 15px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        border-left: 4px solid #667eea;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s ease;
        font-family: 'Inter', sans-serif;
    }
    
    .history-item:hover {
        transform: translateX(5px);
    }
    
    .example-chip {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 20px;
        padding: 0.8rem 1.5rem;
        margin: 0.5rem;
        display: inline-block;
        cursor: pointer;
        transition: all 0.3s ease;
        border: 2px solid transparent;
        font-family: 'Inter', sans-serif;
    }
    
    .example-chip:hover {
        background: rgba(102, 126, 234, 0.2);
        border-color: #667eea;
        transform: scale(1.05);
    }
    
    .footer {
        text-align: center;
        color: rgba(255, 255, 255, 0.8);
        margin-top: 3rem;
        font-size: 0.9rem;
        font-family: 'Inter', sans-serif;
    }
    
    [data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        font-family: 'Inter', sans-serif;
    }
    
    /* Style pour les sélecteurs */
    .stSelectbox {
        font-family: 'Inter', sans-serif;
    }
    
    /* Style pour les expanders */
    .streamlit-expanderHeader {
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar pour les options
with st.sidebar:
    st.markdown("## ⚙️ Options")
    
    # Sélecteur de langue
    lang_options = {
        'fr': '🇫🇷 Français',
        'en': '🇬🇧 English',
        'es': '🇪🇸 Español',
        'ar': '🇸🇦 العربية'
    }
    
    selected_lang = st.selectbox(
        t('language'),
        options=list(lang_options.keys()),
        format_func=lambda x: lang_options[x],
        index=list(lang_options.keys()).index(st.session_state.language)
    )
    
    if selected_lang != st.session_state.language:
        st.session_state.language = selected_lang
        st.rerun()
    
    st.markdown("---")
    
    # Section des exemples
    st.markdown(f"### {t('examples')}")
    st.markdown("Cliquez sur un exemple pour l'utiliser :")
    
    # Affichage du dataset complet
    st.info(f"📊 **Dataset** : {len(example_datasets[st.session_state.language])} phrases d'exemple disponibles")
    
    for i, example in enumerate(example_datasets[st.session_state.language]):
        if st.button(f"📝 Exemple {i+1}", key=f"example_{i}", use_container_width=True):
            st.session_state.current_text = example
            st.rerun()
    
    st.markdown("---")
    
    # Historique
    st.markdown(f"### {t('history')}")
    
    if st.session_state.history:
        if st.button(t('clear_history'), use_container_width=True, type="secondary"):
            st.session_state.history = []
            st.rerun()
        
        st.markdown(f"**{len(st.session_state.history)} analyse(s)**")
        
        for idx, item in enumerate(reversed(st.session_state.history[-10:])):
            with st.expander(f"{item['emoji']} {item['text'][:30]}...", expanded=False):
                st.markdown(f"**Texte:** {item['text']}")
                st.markdown(f"**Résultat:** {item['label']}")
                st.markdown(f"**Confiance:** {item['score']:.1%}")
                st.markdown(f"**Date:** {item['timestamp']}")
                if st.button(f"🗑️ Supprimer", key=f"delete_{idx}"):
                    st.session_state.history.remove(item)
                    st.rerun()
    else:
        st.info(t('no_history'))

# En-tête
st.markdown(f'<h1 class="title">{t("title")}</h1>', unsafe_allow_html=True)
st.markdown(f'<p class="subtitle">{t("subtitle")}</p>', unsafe_allow_html=True)

# Alerte importante sur le modèle backend


# Conteneur principal
col1, col2, col3 = st.columns([1, 3, 1])

with col2:
    # Zone de saisie avec placeholder personnalisé
    user_text = st.text_area(
        t('input_label'),
        value=st.session_state.current_text,
        placeholder=t('placeholder'),
        height=200,
        key="text_input",
        help="Entrez n'importe quel texte pour analyser son sentiment"
    )
    
    # Mettre à jour current_text avec la valeur actuelle
    if user_text != st.session_state.current_text:
        st.session_state.current_text = user_text
    
    # Bouton d'analyse centré
    if st.button(t('analyze_btn'), use_container_width=True):
        if user_text.strip() == "":
            st.warning(t('warning_empty'))
        else:
            with st.spinner(t('analyzing')):
                try:
                    response = requests.post(
                        "http://127.0.0.1:8000/predict",
                        json={"text": user_text},
                        timeout=10
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        label = data['label']
                        score = data['score']
                        
                        # Ajouter à l'historique
                        history_item = {
                            'text': user_text,
                            'label': label,
                            'score': score,
                            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            'emoji': '😊' if label == "POSITIVE" else '😔'
                        }
                        st.session_state.history.append(history_item)
                        
                        # Affichage des résultats
                        result_class = "positive-result" if label == "POSITIVE" else "negative-result"
                        sentiment_text = t('positive') if label == "POSITIVE" else t('negative')
                        
                        st.markdown(f"""
                        <div class="result-box {result_class}">
                            <h2 style="margin: 0; color: #1f2937;">
                                {'😊' if label == "POSITIVE" else '😔'} {sentiment_text}
                            </h2>
                            <p style="font-size: 1.1rem; color: #6b7280; margin-top: 0.5rem;">
                                {t('confidence')} : <strong>{score:.1%}</strong>
                            </p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.progress(score)
                        
                        # Métriques
                        metric_col1, metric_col2, metric_col3 = st.columns(3)
                        
                        with metric_col1:
                            st.metric(
                                label=f"📊 {t('sentiment')}",
                                value=label,
                                delta="Positif" if label == "POSITIVE" else "Négatif"
                            )
                        
                        with metric_col2:
                            st.metric(
                                label=f"🎯 {t('confidence')}",
                                value=f"{score:.1%}",
                                delta=f"+{(score-0.5)*100:.0f}%" if score > 0.5 else f"{(score-0.5)*100:.0f}%"
                            )
                        
                        with metric_col3:
                            st.metric(
                                label=f"📝 {t('words_analyzed')}",
                                value=len(user_text.split())
                            )
                        
                        st.balloons()
                        
                    else:
                        st.error(t('error_server'))
                        
                except requests.exceptions.Timeout:
                    st.error(t('error_timeout'))
                    
                except requests.exceptions.ConnectionError:
                    st.error(t('error_connection'))
                    
                except Exception as e:
                    st.error(f"❌ {str(e)}")

# Informations supplémentaires
with st.expander(t('how_it_works')):
    st.markdown("""
    ### 🧠 Technologie
    Cette application utilise un modèle d'IA avancé pour analyser le sentiment de votre texte :
    
    - **Backend** : FastAPI pour des performances optimales
    - **Frontend** : Streamlit avec design moderne
    - **IA** : Modèle de traitement du langage naturel
    
    ### 🎨 Fonctionnalités
    - ✅ Analyse en temps réel
    - ✅ Interface multilingue (FR, EN, AR)
    - ✅ Exemples de phrases prédéfinis
    - ✅ Historique complet des analyses
    - ✅ Visualisation claire des résultats
    
    ### ⚠️ Note importante
    - **Phrases courtes** : Les phrases très courtes (1-2 mots) peuvent donner des résultats imprécis car le modèle IA a besoin de contexte pour analyser correctement le sentiment.
    - **Recommandation** : Utilisez des phrases complètes avec au moins 4-5 mots pour obtenir les meilleurs résultats (ex: "J'aime beaucoup cette application" au lieu de "j'aime").
    - **Contexte** : Le modèle analyse le sentiment global en tenant compte du contexte, de la syntaxe et de la sémantique de la phrase complète.
    """)

# Footer
st.markdown("---")
st.markdown(f"""
<div class="footer">
    <p>🎓 <strong>{t('footer')}</strong> | {datetime.now().year}</p>
    <p>{t('powered_by')}</p>
</div>
""", unsafe_allow_html=True)