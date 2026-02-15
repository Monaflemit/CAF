# cd "C:\Users\quewa\Documents\pyzo\Raccoucis clavier"
# streamlit run "Prestations CAF - Analyse.py"
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Configuration de la page
st.set_page_config(
    page_title="Prestations CAF - Analyse",
    page_icon="📊",
    layout="wide"
)

# Titre principal
st.title("📊 Bénéficiaires des prestations CAF")
st.markdown("""
Bénéficiaires mensuels d'au moins une prestation légale (hors ARS, ADE et AVVC)
par type de prestations à l'échelle nationale depuis 2016.
""")

# Définitions du glossaire (adaptées à la légende)
glossaire_enfance_jeunesse = {
    "NDUR": "Allocataire bénéficiant d'au moins une prestation.",
    "NDURPAJE": "Allocation de base de la PAJE (Prestation d'Accueil du Jeune Enfant).",
    "PN": "Prime de Naissance ou d'Adoption.",
    "AB": "Allocation de Base (PAJE).",
    "CMG": "Complément de libre choix du Mode de Garde (PAJE).",
    "PreParE": "Prestation Partagée d'Éducation de l'Enfant (PAJE).",
    "NDUREJ": "Complément Éducation de la PAJE.",
}

glossaire_toutes_prestations = {
    **glossaire_enfance_jeunesse,
    "AAH": "Allocation aux Adultes Handicapés.",
    "APL": "Aide Personnalisée au Logement.",
    "RSA": "Revenu de Solidarité Active.",
    "CDI": "Complément Différentiel.",
}

# Cache pour charger les données
@st.cache
def load_data():
    url = "https://data.caf.fr/api/explore/v2.1/catalog/datasets/s_ben_nat/exports/csv?lang=fr&timezone=Europe%2FBerlin&use_labels=true&delimiter=%3B"
    df = pd.read_csv(url, delimiter=';')
    df['Date référence'] = pd.to_datetime(df['Date référence'], format='%Y-%m')
    df = df.sort_values(by='Date référence')
    return df

# Chargement des données
with st.spinner('Chargement des données...'):
    df = load_data()
st.success(f"✅ Données chargées : {len(df)} périodes de {df['Date référence'].min().strftime('%Y-%m')} à {df['Date référence'].max().strftime('%Y-%m')}")

# Sidebar pour les options
st.sidebar.header("Options d'affichage")
scope = st.sidebar.radio(
    "Périmètre des prestations",
    ["Prestations Enfance/Jeunesse", "Toutes les prestations"]
)

# Définition des colonnes selon le périmètre
if scope == "Prestations Enfance/Jeunesse":
    columns_foyers = [
        'Nombre foyers NDURPAJE', 'Nombre foyers PN',
        'Nombre foyers AB', 'Nombre foyers CMG', 'Nombre foyers PREPARE',
        'Nombre foyers NDUREJ'
    ]
    columns_personnes = [
        'Nombre personnes NDURPAJE', 'Nombre personnes PN',
        'Nombre personnes AB', 'Nombre personnes CMG', 'Nombre personnes PREPARE',
        'Nombre personnes NDUREJ'
    ]
    columns_montants = [
        'Montant total NDURPAJE', 'Montant total PN',
        'Montant total AB', 'Montant total CMG', 'Montant total PREPARE',
        'Montant total NDUREJ'
    ]
    legend_y = -0.3
    annotation_x = 1.3
    annotation_y = -0.5
    glossaire = glossaire_enfance_jeunesse
else:
    columns_foyers = [
        'Nombre foyers NDUR', 'Nombre foyers NDURPAJE', 'Nombre foyers PN',
        'Nombre foyers AB', 'Nombre foyers CMG', 'Nombre foyers PREPARE',
        'Nombre foyers NDUREJ', 'Nombre foyers AAH', 'Nombre foyers APL',
        'Nombre foyers RSA', 'Nombre foyers CDI'
    ]
    columns_personnes = [
        'Nombre personnes NDUR', 'Nombre personnes NDURPAJE', 'Nombre personnes PN',
        'Nombre personnes AB', 'Nombre personnes CMG', 'Nombre personnes PREPARE',
        'Nombre personnes NDUREJ', 'Nombre personnes AAH', 'Nombre personnes APL',
        'Nombre personnes RSA', 'Nombre personnes CDI'
    ]
    columns_montants = [
        'Montant total NDUR', 'Montant total NDURPAJE', 'Montant total PN',
        'Montant total AB', 'Montant total CMG', 'Montant total PREPARE',
        'Montant total NDUREJ', 'Montant total AAH', 'Montant total APL',
        'Montant total RSA', 'Montant total CDI'
    ]
    legend_y = -0.3
    annotation_x = 1.3
    annotation_y = -0.5
    glossaire = glossaire_toutes_prestations

# Affichage du glossaire
with st.expander("📚 Glossaire"):
    st.markdown("**Définitions des prestations affichées :**")
    for acronyme, definition in glossaire.items():
        st.markdown(f"**{acronyme}** : {definition}")

# Onglets pour les vues
tab_choice = st.radio(
    "Choisissez la vue :",
    ["👨‍👩‍👧‍👦 Foyers", "👥 Personnes", "💰 Montants"],
)

if tab_choice == "👨‍👩‍👧‍👦 Foyers":
    st.subheader("Évolution du nombre de foyers")
    fig_foyers = go.Figure()
    for column in columns_foyers:
        fig_foyers.add_trace(go.Scatter(
            x=df['Date référence'],
            y=df[column],
            mode='lines',
            name=column
        ))
    fig_foyers.update_layout(
        title='Évolution du nombre de foyers au fil du temps',
        xaxis_title='',
        yaxis_title='Nombre de foyers',
        legend_title='',
        height=600,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=legend_y,
            xanchor="center",
            x=0.5
        )
    )
    st.plotly_chart(fig_foyers, use_container_width=True)
elif tab_choice == "👥 Personnes":
    st.subheader("Évolution du nombre de personnes")
    fig_personnes = go.Figure()
    for column in columns_personnes:
        fig_personnes.add_trace(go.Scatter(
            x=df['Date référence'],
            y=df[column],
            mode='lines',
            name=column
        ))
    fig_personnes.update_layout(
        title='Évolution du nombre de personnes au fil du temps',
        xaxis_title='',
        yaxis_title='Nombre de personnes',
        legend_title='',
        height=600,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=legend_y,
            xanchor="center",
            x=0.5
        )
    )
    st.plotly_chart(fig_personnes, use_container_width=True)
elif tab_choice == "💰 Montants":
    st.subheader("Évolution des montants totaux")
    fig_montants = go.Figure()
    for column in columns_montants:
        fig_montants.add_trace(go.Scatter(
            x=df['Date référence'],
            y=df[column],
            mode='lines',
            name=column
        ))
    fig_montants.update_layout(
        title='Évolution des montants totaux au fil du temps',
        xaxis_title='',
        yaxis_title='Montant total (€)',
        legend_title='',
        height=600,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=legend_y,
            xanchor="center",
            x=0.5
        )
    )
    st.plotly_chart(fig_montants, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
**Source des données** : [data.caf.fr](https://data.caf.fr/explore/dataset/s_ben_nat/information/)
Les données sont mises à jour automatiquement depuis l'API de la CAF.
""")
