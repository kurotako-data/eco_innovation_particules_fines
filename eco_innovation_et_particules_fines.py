#!/usr/bin/env python
# coding: utf-8

# In[1]:


#1. Chargement et Préparation des Données
#Nous allons charger les fichiers CSV et vérifier la cohérence des périodes et des pays 
#dans les deux ensembles de données.


# In[2]:


import pandas as pd

# Chemins des fichiers (à ajuster selon votre environnement)
file_path_deces = '/Users/Patrice/Documents/GitHub/eco_innovation_et_particules_fines/data/deces_pm25_2005_2023.csv'
file_path_eco_index = '/Users/Patrice/Documents/GitHub/eco_innovation_et_particules_fines/data/eco_innovation_2013_2022.csv'

# Chargement des données avec le bon séparateur
deces_data = pd.read_csv(file_path_deces, sep=';')
eco_index_data = pd.read_csv(file_path_eco_index, sep=';')

# Renommer la colonne 'Unnamed: 0' en 'Pays'
deces_data.rename(columns={'Unnamed: 0': 'Pays'}, inplace=True)
eco_index_data.rename(columns={'Unnamed: 0': 'Pays'}, inplace=True)

# Vérification des colonnes après renommage
print("Colonnes de deces_pm25_2005_2023.csv après renommage :", deces_data.columns)
print("Colonnes de eco_innovation_2013_2022.csv après renommage :", eco_index_data.columns)

# Transformation du fichier de décès dus au PM2.5 en format long
deces_data_long = deces_data.melt(id_vars=['Pays'], var_name='Année', value_name='deces_pm25')
deces_data_long['Année'] = deces_data_long['Année'].astype(int)  # Convertir la colonne année en entier

# Transformation du fichier d’indice d’éco-innovation en format long
eco_index_data_long = eco_index_data.melt(id_vars=['Pays'], var_name='Année', value_name='eco_index')
eco_index_data_long['Année'] = eco_index_data_long['Année'].astype(int)  # Convertir la colonne année en entier

# Fusion des deux jeux de données sur les colonnes 'Pays' et 'Année'
merged_data = pd.merge(deces_data_long, eco_index_data_long, on=['Pays', 'Année'], how='inner')

# Affichage des premières lignes pour vérifier le résultat
print("Données fusionnées :\n", merged_data.head())

# Sauvegarde du fichier fusionné pour analyse future
merged_data.to_csv('/Users/Patrice/Documents/GitHub/eco_innovation_et_particules_fines/data/merged_data.csv', index=False, sep=';')


# In[3]:


# Suppression des lignes qui contiennent "Pays" dans la colonne 'Pays'
merged_data = merged_data[merged_data['Pays'] != 'Pays']

# Nettoyage des valeurs numériques
# Remplacer les espaces insécables par des chaînes vides et les virgules par des points pour les nombres décimaux
merged_data['deces_pm25'] = merged_data['deces_pm25'].replace({'\u202f': '', ',': '.'}, regex=True).astype(float)
merged_data['eco_index'] = merged_data['eco_index'].replace({'\u202f': '', ',': '.'}, regex=True).astype(float)

# Vérification des premières lignes pour s'assurer que le nettoyage a été effectué
print("Données fusionnées après nettoyage :\n", merged_data.head())

# Sauvegarde du fichier nettoyé
merged_data.to_csv('/Users/Patrice/Documents/GitHub/eco_innovation_et_particules_fines/data/merged_data_cleaned.csv', index=False, sep=';')


# In[4]:


#1. Analyse Exploratoire des Données (EDA)
#Nous allons explorer la distribution des données, examiner les tendances par pays et par année 
#et vérifier les corrélations initiales entre l'indice d’éco-innovation et les décès dus au PM2.5.


# In[5]:


import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Distribution des décès dus au PM2.5
plt.figure(figsize=(10, 5))
sns.histplot(merged_data['deces_pm25'], bins=20, kde=True)
plt.title("Distribution des Décès Prematurés dus au PM2.5")
plt.xlabel("Décès dus au PM2.5")
plt.ylabel("Fréquence")
plt.show()

# Distribution de l'indice d'éco-innovation
plt.figure(figsize=(10, 5))
sns.histplot(merged_data['eco_index'], bins=20, kde=True, color="green")
plt.title("Distribution de l'Indice d'Éco-Innovation")
plt.xlabel("Indice d'Éco-Innovation")
plt.ylabel("Fréquence")
plt.show()




import plotly.express as px

# Graphique interactif pour les décès dus au PM2.5 par pays et par année
fig_deces = px.line(
    merged_data, 
    x='Année', 
    y='deces_pm25', 
    color='Pays', 
    title="Décès Prematurés dus au PM2.5 par Pays et par Année",
    labels={'deces_pm25': 'Décès dus au PM2.5', 'Année': 'Année'}
)
fig_deces.update_layout(
    height=800,  # Ajuster la hauteur du graphique
    legend_title_text='Pays'
)
fig_deces.show()

# Graphique interactif pour l'indice d'éco-innovation par pays et par année
fig_eco_index = px.line(
    merged_data, 
    x='Année', 
    y='eco_index', 
    color='Pays', 
    title="Indice d'Éco-Innovation par Pays et par Année",
    labels={'eco_index': "Indice d'Éco-Innovation", 'Année': 'Année'}
)
fig_eco_index.update_layout(
    height=800,  # Ajuster la hauteur du graphique
    legend_title_text='Pays'
)
fig_eco_index.show()


# In[6]:


#2. Analyse des Corrélations
#Calculons la corrélation globale entre les deux variables et les corrélations spécifiques par pays. 
#Cela nous permettra de voir si une relation existe globalement ou si elle est spécifique à certains pays.


# In[7]:


# Corrélation globale
global_correlation = merged_data[['deces_pm25', 'eco_index']].corr().iloc[0, 1]
print("Corrélation globale entre l'indice d'éco-innovation et les décès dus au PM2.5 :", global_correlation)



# Calcul des corrélations par pays (déjà effectué dans votre code)
country_correlations = merged_data.groupby('Pays')[['deces_pm25', 'eco_index']].corr().iloc[0::2, -1].reset_index()
country_correlations.columns = ['Pays', 'index', 'correlation_eco_deces']

# Création du graphique interactif avec Plotly
fig_corr = px.bar(
    country_correlations, 
    x='Pays', 
    y='correlation_eco_deces', 
    title="Corrélation entre l'Indice d'Éco-Innovation et les Décès dus au PM2.5 par Pays",
    labels={'correlation_eco_deces': 'Coefficient de Corrélation'},
    hover_data={'correlation_eco_deces': ':.2f'}  # Format pour afficher deux décimales dans l'infobulle
)

# Personnalisation du graphique
fig_corr.update_layout(
    height=600,  # Ajuster la hauteur pour plus de lisibilité
    xaxis_tickangle=-90,  # Rotation des labels des pays pour lisibilité
    xaxis_title="Pays",
    yaxis_title="Coefficient de Corrélation"
)

# Affichage du graphique
fig_corr.show()


# In[8]:


#3. Modélisation Statistique (Régression Linéaire)
#Nous utiliserons une régression linéaire pour évaluer l'impact de l'indice d’éco-innovation sur les 
#décès dus au PM2.5. Nous ferons cette analyse pour l'ensemble des pays, ainsi que pour chaque pays individuellement.


# In[9]:


# Vérifier les valeurs manquantes dans les colonnes importantes
print("Valeurs manquantes par colonne :\n", merged_data[['deces_pm25', 'eco_index']].isna().sum())

# Supprimer les lignes avec des valeurs manquantes ou infinies dans les colonnes deces_pm25 et eco_index
merged_data_cleaned = merged_data.dropna(subset=['deces_pm25', 'eco_index'])

# Vérification après nettoyage
print("Données après suppression des valeurs manquantes :")
print(merged_data_cleaned[['deces_pm25', 'eco_index']].isna().sum())


# In[10]:


get_ipython().system('pip install plotly')

# Régression linéaire globale et par pays

#Étape 1 : Calcul des Résultats de Régression et Organisation en Tableau
#Nous allons d'abord collecter les résultats de régression pour chaque pays dans un DataFrame 
#afin de pouvoir les afficher dans un tableau interactif.


import pandas as pd
import statsmodels.api as sm
import plotly.graph_objects as go
import plotly.io as pio

# Configurer le renderer pour Jupyter Notebook
pio.renderers.default = "notebook"

# Calcul des résultats de régression
results = []

# Régression linéaire globale
X_global = sm.add_constant(merged_data_cleaned['eco_index'])
y_global = merged_data_cleaned['deces_pm25']
model_global = sm.OLS(y_global, X_global).fit()

# Ajouter les résultats globaux
results.append({
    'Pays': 'Global',
    'Coefficient': model_global.params['eco_index'],
    'Intercept': model_global.params['const'],
    'R_squared': model_global.rsquared,
    'p_value': model_global.pvalues['eco_index']
})

# Régression linéaire par pays
for country in merged_data_cleaned['Pays'].unique():
    country_data = merged_data_cleaned[merged_data_cleaned['Pays'] == country]
    X = sm.add_constant(country_data['eco_index'])
    y = country_data['deces_pm25']
    model = sm.OLS(y, X).fit()
    
    # Ajouter les résultats pour chaque pays
    results.append({
        'Pays': country,
        'Coefficient': model.params['eco_index'],
        'Intercept': model.params['const'],
        'R_squared': model.rsquared,
        'p_value': model.pvalues['eco_index']
    })

# Conversion des résultats en DataFrame
results_df = pd.DataFrame(results)

# Sauvegarde des résultats de régression dans un fichier CSV
results_df.to_csv("regression_results.csv", index=False)


# Création du tableau interactif avec Plotly
fig = go.Figure(data=[go.Table(
    header=dict(values=['Pays', 'Coefficient', 'Intercept', 'R_squared', 'p_value'],
                fill_color='paleturquoise',
                align='left'),
    cells=dict(values=[results_df.Pays, 
                       results_df.Coefficient.round(3), 
                       results_df.Intercept.round(3), 
                       results_df.R_squared.round(3), 
                       results_df.p_value.round(3)],
               fill_color='lavender',
               align='left'))
])

fig.update_layout(title="Résultats de la Régression Linéaire par Pays")

# Affichage du tableau
fig.show()


# In[11]:


#4. Visualisation des Résultats (Comparaison par Pays et par Année)
#Pour visualiser l’évolution des décès dus au PM2.5 et de l’indice d’éco-innovation, 
#nous allons créer un graphique avec deux échelles verticales, une pour les décès dus au PM2.5 
#et une autre pour l'indice d’éco-innovation, permettant ainsi de 
#visualiser clairement les deux séries de données sans problème d’échelle. 


# In[12]:


# Sélection de quelques pays pour visualiser les tendances
selected_countries = ['France', 'Germany', 'Italy', 'Spain', 'Belgium']

plt.figure(figsize=(14, 8))

# Parcourir chaque pays sélectionné et tracer les courbes
for country in selected_countries:
    country_data = merged_data[merged_data['Pays'] == country]
    
    # Tracer les décès dus au PM2.5 (axe gauche)
    plt.plot(country_data['Année'], country_data['deces_pm25'], label=f'Décès dus au PM2.5 - {country}')
    
# Création d'un deuxième axe y
ax2 = plt.gca().twinx()

# Tracer les courbes pour l'indice d'éco-innovation (axe droit)
for country in selected_countries:
    country_data = merged_data[merged_data['Pays'] == country]
    
    # Tracer l'éco-innovation avec un style en pointillés (axe droit)
    ax2.plot(country_data['Année'], country_data['eco_index'], linestyle='--', label=f'Éco-Innovation - {country}')

# Ajuster la légende et les titres
plt.title("Tendances de l'Éco-Innovation et des Décès dus au PM2.5 dans le Temps")
plt.xlabel("Année")
plt.ylabel("Décès dus au PM2.5")
ax2.set_ylabel("Indice d'Éco-Innovation")

# Création d'une légende combinée
lines, labels = plt.gca().get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
plt.legend(lines + lines2, labels + labels2, loc='upper right')

plt.show()



# In[ ]:


#Heatmap des Décès dus aux PM2.5 par Pays
#Une carte choroplèthe (carte en couleur) pourrait être utile pour visualiser les différences 
#de niveaux de décès dus au PM2.5 entre les pays européens pour une année donnée.
#Cette carte permettrait de voir rapidement quels pays sont les plus touchés.


# In[20]:


# Filtrer les données pour les années disponibles dans le DataFrame
data_for_map = merged_data[['Pays', 'Année', 'deces_pm25']].dropna()

# Création de la carte choroplèthe avec un curseur temporel et une échelle de couleurs plus riche
fig = px.choropleth(
    data_for_map,
    locations="Pays",
    locationmode="country names",
    color="deces_pm25",
    hover_name="Pays",
    animation_frame="Année",  # Curseur temporel basé sur l'année
    color_continuous_scale="Reds",  # Échelle de couleur plus riche
    title="Évolution des Décès dus au PM2.5 en Europe"
)

# Configuration de l'affichage de la carte pour se concentrer sur l'Europe
fig.update_geos(scope="europe", projection_type="natural earth")

# Ajustement de la légende de l'échelle de couleur
fig.update_coloraxes(colorbar_title="Décès PM2.5", colorbar_ticksuffix=" décès")

# Affichage de la carte
fig.show()


# In[21]:


#Évolution des Décès dus au PM2.5 et de l'Indice d'Éco-Innovation par Pays
#Un graphique à deux axes pourrait montrer l'évolution simultanée des décès dus aux PM2.5 
#et de l'indice d’éco-innovation pour chaque pays, ce qui permet de visualiser les tendances.
#Cela pourrait révéler des tendances communes ou des pays où une amélioration de 
#l'indice d'éco-innovation correspond à une baisse des décès.


# In[24]:


import plotly.graph_objects as go

# Création de la figure de base
fig = go.Figure()

# Ajout des courbes pour chaque pays mais invisibles au départ
for country in merged_data['Pays'].unique():
    country_data = merged_data[merged_data['Pays'] == country]
    
    # Ajout de la courbe pour les décès dus au PM2.5 (invisible par défaut)
    fig.add_trace(go.Scatter(
        x=country_data['Année'],
        y=country_data['deces_pm25'],
        mode='lines+markers',
        name=f'Décès dus au PM2.5 - {country}',
        visible=False
    ))
    
    # Ajout de la courbe pour l'indice d'éco-innovation (invisible par défaut)
    fig.add_trace(go.Scatter(
        x=country_data['Année'],
        y=country_data['eco_index'],
        mode='lines+markers',
        name=f'Éco-Innovation - {country}',
        line=dict(dash='dash'),  # Style en pointillés
        visible=False,
        yaxis="y2"
    ))

# Activation de la première série de données par défaut (ex: premier pays de la liste)
fig.data[0].visible = True  # Décès dus au PM2.5
fig.data[1].visible = True  # Éco-Innovation

# Création du menu déroulant pour sélectionner le pays
buttons = []
for i, country in enumerate(merged_data['Pays'].unique()):
    button = dict(
        label=country,
        method="update",
        args=[{"visible": [False] * len(fig.data)}]  # Masquer toutes les traces
    )
    button["args"][0]["visible"][2 * i] = True  # Montrer les décès dus au PM2.5 pour le pays sélectionné
    button["args"][0]["visible"][2 * i + 1] = True  # Montrer l'éco-innovation pour le pays sélectionné
    buttons.append(button)

# Ajout du menu déroulant
fig.update_layout(
    updatemenus=[
        dict(
            active=0,
            buttons=buttons,
            x=0.17,
            xanchor="left",
            y=1.15,
            yanchor="top",
            direction="down",
            showactive=True
        )
    ]
)

# Ajout des titres et personnalisation des axes
fig.update_layout(
    title="Évolution des Décès dus au PM2.5 et de l'Indice d'Éco-Innovation par Pays",
    xaxis_title="Année",
    yaxis=dict(title="Décès dus au PM2.5"),
    yaxis2=dict(title="Indice d'Éco-Innovation", overlaying="y", side="right")
)

# Affichage du graphique
fig.show()


# In[ ]:


#Tendance Moyenne Annuelle des Décès dus au PM2.5 et de l'Éco-Innovation
#Un graphique en ligne avec la moyenne annuelle des décès dus au PM2.5 
#et de l’indice d’éco-innovation pour tous les pays permettrait de visualiser une tendance globale.
#Cela aiderait à voir si, en moyenne, l'amélioration de l'éco-innovation coïncide 
#avec une baisse des décès dus aux PM2.5.


# In[26]:


import plotly.graph_objects as go
import pandas as pd

# Calculer la moyenne annuelle pour les deux variables
annual_avg = merged_data.groupby('Année').agg({'deces_pm25': 'mean', 'eco_index': 'mean'}).reset_index()

# Création du graphique avec deux axes y
fig = go.Figure()

# Ajout de la courbe pour la moyenne des décès dus au PM2.5
fig.add_trace(go.Scatter(
    x=annual_avg['Année'],
    y=annual_avg['deces_pm25'],
    mode='lines+markers',
    name="Décès dus au PM2.5 (Moyenne)",
    line=dict(color='blue')
))

# Ajout de la courbe pour la moyenne de l'indice d'éco-innovation sur l'axe y2
fig.add_trace(go.Scatter(
    x=annual_avg['Année'],
    y=annual_avg['eco_index'],
    mode='lines+markers',
    name="Indice d'Éco-Innovation (Moyenne)",
    line=dict(color='red'),
    yaxis="y2"  # Spécifier l'axe y2 pour cette courbe
))

# Configuration de la mise en page pour les deux axes y
fig.update_layout(
    title="Tendance Moyenne Annuelle des Décès dus au PM2.5 et de l'Éco-Innovation",
    xaxis=dict(title="Année"),
    yaxis=dict(title="Décès dus au PM2.5 (Moyenne)", titlefont=dict(color="blue")),
    yaxis2=dict(title="Indice d'Éco-Innovation (Moyenne)", titlefont=dict(color="red"),
                overlaying="y", side="right"),  # Configuration de l'axe y2 à droite
    legend=dict(x=0.5, y=1.1, orientation="h")  # Légende positionnée au-dessus
)

# Affichage du graphique
fig.show()


# In[ ]:





# In[13]:


#5. Conclusion et Interprétation des Résultats


# In[ ]:


#voir rapport final


# In[ ]:




