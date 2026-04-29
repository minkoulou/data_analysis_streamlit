import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ─────────────────────────────────────────
# Configuration de la page
# ─────────────────────────────────────────
st.set_page_config(
    page_title="Analyse de Données",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Data analysis")
st.markdown("Importe ton fichier CSV ou Excel pour obtenir des statistiques et graphiques automatiquement.")

# ─────────────────────────────────────────
# 1. UPLOAD DU FICHIER
# ─────────────────────────────────────────
uploaded_file = st.file_uploader("Importe ton fichier", type=["csv", "xlsx"])

@st.cache_data
def load_data(file):
    if file.name.endswith(".csv"):
        return pd.read_csv(file)
    else:
        return pd.read_excel(file)

if uploaded_file is not None:
    df = load_data(uploaded_file)

    # ─────────────────────────────────────────
    # 2. APERÇU DES DONNÉES
    # ─────────────────────────────────────────
    st.header("🔍 Aperçu des données")
    col1, col2, col3 = st.columns(3)
    col1.metric("Lignes", df.shape[0])
    col2.metric("Colonnes", df.shape[1])
    col3.metric("Valeurs manquantes", df.isnull().sum().sum())

    st.dataframe(df.head(10), use_container_width=True)

    # ─────────────────────────────────────────
    # 3. STATISTIQUES DESCRIPTIVES
    # ─────────────────────────────────────────
    st.header("📈 Statistiques descriptives")
    numeric_cols = df.select_dtypes(include="number")

    if not numeric_cols.empty:
        st.dataframe(numeric_cols.describe().round(2), use_container_width=True)
    else:
        st.warning("Aucune colonne numérique détectée.")

    # ─────────────────────────────────────────
    # 4. GRAPHIQUES
    # ─────────────────────────────────────────
    st.header("🎨 Visualisations")

    if not numeric_cols.empty:
        col_choisie = st.selectbox("Choisis une colonne à visualiser :", numeric_cols.columns)

        tab1, tab2, tab3 = st.tabs(["Histogramme", "Boxplot", "Heatmap de corrélation"])

        with tab1:
            fig, ax = plt.subplots()
            sns.histplot(df[col_choisie].dropna(), kde=True, ax=ax, color="#4C72B0")
            ax.set_title(f"Distribution de {col_choisie}")
            st.pyplot(fig)

        with tab2:
            fig, ax = plt.subplots()
            sns.boxplot(y=df[col_choisie].dropna(), ax=ax, color="#55A868")
            ax.set_title(f"Boxplot de {col_choisie}")
            st.pyplot(fig)

        with tab3:
            if numeric_cols.shape[1] >= 2:
                fig, ax = plt.subplots(figsize=(8, 6))
                sns.heatmap(numeric_cols.corr().round(2), annot=True, cmap="coolwarm", ax=ax)
                ax.set_title("Matrice de corrélation")
                st.pyplot(fig)
            else:
                st.info("Il faut au moins 2 colonnes numériques pour afficher la heatmap.")

    # ─────────────────────────────────────────
    # 5. EXPORT DES STATS
    # ─────────────────────────────────────────
    st.header("💾 Exporter les statistiques")
    if not numeric_cols.empty:
        csv_export = numeric_cols.describe().round(2).to_csv().encode("utf-8")
        st.download_button(
            label="📥 Télécharger les stats (CSV)",
            data=csv_export,
            file_name="statistiques.csv",
            mime="text/csv"
        )

else:
    st.info("👆 Commence par importer un fichier CSV ou Excel.")