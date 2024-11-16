# Installer les bibliothèques nécessaires
# !pip install streamlit plotly pandas

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Chargement des données
@st.cache_data
def load_data():
    data = pd.read_csv('data/merged_data_cleaned.csv', sep=';')
    regression_results = pd.read_csv("regression_results.csv", sep=';')  
    return data, regression_results

data, regression_results = load_data()

# Titre et Introduction
st.title("Indices d'éco-innovation et particules fines PM 2.5")
st.markdown("""
Ce projet analyse l’efficacité de l’indice d’éco-innovation en Europe et sa relation avec les décès prématurés dus aux particules fines (PM2.5) dans différents pays européens. 
L'objectif est de déterminer si les pays ayant un score élevé d’éco-innovation présentent des taux de mortalité plus faibles liés à la pollution par les particules fines.
""")

# Graphiques interactifs
st.header("Évolution des Décès dus au PM2.5 en Europe")
year = st.slider("Sélectionner l'année", 2013, 2021, 2013)
fig_map = px.choropleth(
    data[data['Année'] == year],
    locations="Pays",
    locationmode="country names",
    color="deces_pm25",
    color_continuous_scale="Reds",
    title=f"Décès dus au PM2.5 en {year}",
    labels={'deces_pm25': 'Décès PM2.5'}
)
st.plotly_chart(fig_map)

# Graphique de corrélation
st.header("Corrélation entre l'Indice d'Éco-Innovation et les Décès dus au PM2.5")
# Calcul des corrélations par pays
correlation_results = []
for country in data['Pays'].unique():
    country_data = data[data['Pays'] == country]
    correlation = country_data['eco_index'].corr(country_data['deces_pm25'])
    correlation_results.append({'Pays': country, 'correlation_coefficient': correlation})

# Conversion en DataFrame
corr_data = pd.DataFrame(correlation_results)

# Création du graphique de corrélation avec Plotly
fig_corr = px.bar(
    corr_data, 
    x="Pays", 
    y="correlation_coefficient", 
    title="Corrélation entre l'Indice d'Éco-Innovation et les Décès dus au PM2.5 par Pays",
    labels={'correlation_coefficient': 'Coefficient de Corrélation'},
    hover_data={'correlation_coefficient': ':.2f'}  # Format pour afficher deux décimales dans l'infobulle
)
st.plotly_chart(fig_corr)

# Comparaison annuelle par pays
st.header("Comparaison de l'Évolution par Pays")
country = st.selectbox("Sélectionner un pays", data["Pays"].unique())
country_data = data[data["Pays"] == country]
fig_country = go.Figure()
fig_country.add_trace(go.Scatter(x=country_data["Année"], y=country_data["deces_pm25"], name="Décès PM2.5", mode="lines+markers"))
fig_country.add_trace(go.Scatter(x=country_data["Année"], y=country_data["eco_index"], name="Indice d'Éco-Innovation", mode="lines+markers"))
fig_country.update_layout(title=f"Évolution des Décès et Éco-Innovation pour {country}", yaxis_title="Valeurs", xaxis_title="Année")
st.plotly_chart(fig_country)

# Tendance moyenne annuelle
st.header("Tendance Moyenne Annuelle des Décès dus au PM2.5 et de l'Éco-Innovation")

# Code temporaire pour vérifier les types et les premières lignes des données
st.write("Types des colonnes :", data.dtypes)
st.write("Exemple de données :", data.head())

# Nettoyage de la colonne Année pour s'assurer qu'elle est bien en format entier
data['Année'] = data['Année'].astype(str).str.replace(',', '').astype(int)

# Filtrer pour n'utiliser que les colonnes numériques sans inclure "Année" dans la moyenne
numeric_columns = [col for col in data.select_dtypes(include=['float64', 'int64']).columns if col != "Année"]
st.write("Colonnes numériques pour le calcul de la moyenne :", numeric_columns)

# Calcul de la tendance moyenne annuelle en utilisant uniquement les colonnes numériques
avg_data = data.groupby("Année")[numeric_columns].mean()  # Ne pas utiliser reset_index() pour éviter le conflit de colonne

# Afficher les données de tendance moyenne annuelle pour vérification
st.write("Données de tendance moyenne annuelle :", avg_data.head())

# Création du graphique
fig_avg = go.Figure()
fig_avg.add_trace(go.Scatter(x=avg_data.index, y=avg_data["deces_pm25"], name="Décès PM2.5 (Moyenne)", mode="lines+markers", line=dict(color='blue')))
fig_avg.add_trace(go.Scatter(x=avg_data.index, y=avg_data["eco_index"], name="Indice d'Éco-Innovation (Moyenne)", mode="lines+markers", line=dict(color='red')))
fig_avg.update_layout(title="Tendance Moyenne Annuelle", yaxis_title="Valeurs Moyennes", xaxis_title="Année")
st.plotly_chart(fig_avg)


# Résultats de la régression linéaire
st.header("Résultats de la Régression Linéaire par Pays")
st.table(regression_results)

# Liens vers les fichiers
st.header("Téléchargements")
st.markdown("[Télécharger le Code Python](./eco_innovation_et_particules_fines.py)")
st.markdown("[Télécharger le Rapport Final](./final_report)")

# Conclusion et Recommandations
st.header("Conclusion et Recommandations")
st.markdown("""
Les résultats montrent que l'éco-innovation semble avoir un effet significatif dans certains pays, et cette étude pourrait servir de base pour de futures recherches intégrant des facteurs additionnels, 
tels que des données économiques, des taux de croissance démographique, ou des informations sur les politiques environnementales.
""")
