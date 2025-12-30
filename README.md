🎯 Analyseur de Sentiment IA Multilingue (BERT)
📝 Présentation du Projet
Ce projet, réalisé dans le cadre d'un Master, est une application web capable de détecter la tonalité émotionnelle (positive ou négative) d'un texte. L'application utilise l'état de l'art du Traitement du Langage Naturel (NLP) pour offrir une analyse précise dans plusieurs langues (Français, Anglais, Espagnol, Arabe).

🚀 [Lien vers l'application en direct (Hugging Face)]
(Remplacez ce texte par votre lien Hugging Face une fois qu'il est "Running")

🛠️ Architecture Technique
L'application repose sur une architecture moderne intégrant :

IA Engine : BERT Multilingual (Hugging Face Transformers).

Interface : Streamlit pour une UX moderne et réactive.

Preprocessing : Pipeline de nettoyage personnalisé (Regex/Python).

Déploiement : CI/CD via GitHub et Hugging Face Spaces.

🧬 Pipeline de Données
Le projet suit une chaîne de traitement rigoureuse pour garantir la fiabilité des résultats :

Input : Récupération du texte brut utilisateur.

Preprocessing (Nettoyage) :

Conversion en minuscules.

Suppression des URLs et liens.

Retrait de la ponctuation (bruit numérique).

Normalisation des espaces.

Inférence IA : Passage du texte nettoyé dans le modèle BERT.

Post-processing : Conversion des scores (stars) en labels binaires (Positif/Négatif).

Visualisation : Affichage du score de confiance et mise à jour de l'historique de session.

🌍 Fonctionnalités Clés
Multilingue : Supporte nativement les nuances linguistiques de plusieurs langues.

Historique de Session : Suivi des analyses effectuées durant la session utilisateur.

Design Adaptatif : Interface optimisée pour Desktop et Mobile.

Transparence : Un module permet de visualiser le texte après nettoyage (Preprocessing).

💻 Installation Locale
Pour tester le projet sur votre machine :

Cloner le projet :

Bash

git clone https://github.com/votre-utilisateur/votre-projet.git
Installer les dépendances :

Bash

pip install -r requirements.txt
Lancer l'application :

Bash

streamlit run app.py
🎓 Cadre Académique
Diplôme : Master

Domaine : Intelligence Artificielle / Data Science

Technologies : Python, PyTorch, Transformers, Streamlit.
