# -*- coding: utf-8 -*-

import streamlit as st
import pandas as pd
import numpy as np
from numerize.numerize import numerize

import plotly.graph_objs as go
import plotly.express as px
import plotly.figure_factory as ff


st.set_page_config(page_title=":bar_chart: Tableau de bord Projet DataViz",
                   layout = 'wide',
                   initial_sidebar_state= 'expanded'
                   )



df = pd.read_excel('/content/PRODUCTION_Detail_Contrats_Janvier_Septembre_2023_NonAuto.xlsx')


df_apres_nettoyage = df[df['PRIMENETTE'] > 0]

header_left,header_mid,header_right = st.columns([1,2,1],gap='large')

with header_mid:
    st.title(':bar_chart: Tableau de bord agences')


with st.sidebar:
    agence_filter = st.multiselect(label= 'Choisissez une agence',
                                options=df['CRMA'].unique(),
                                default=df['CRMA'].unique())

    groupe_filter = st.multiselect(label='Choisissez un type de contract',
                            options=df['GROUPE'].unique(),
                            default=df['GROUPE'].unique())

    grappe_filter = st.multiselect(label='Choisissez un type de produits',
                            options=df['GRAPPE'].unique(),
                            default=df['GRAPPE'].unique())

df = df.query('CRMA == @agence_filter & GROUPE == @groupe_filter & GRAPPE == @grappe_filter')






nombre_agences = len(df_apres_nettoyage['CRMA'].unique())
Nombre_clients = len(df_apres_nettoyage['ASSURE'].unique())
Nombre_Produits =  len(df['GRAPPE'].value_counts())
Nombre_Transactions = len(df.index.value_counts())/nombre_agences
Revenu_moy = df_apres_nettoyage['PRIMENETTE'].sum()/nombre_agences



total1,total2,total3,total4,total5 = st.columns(5,gap='large')

with total1:
    #st.image('images/impression.png',use_column_width='Auto')
    st.metric(label = "Nombre d'agences", value= numerize(nombre_agences))
    
with total2:
    #st.image('images/tap.png',use_column_width='Auto')
    st.metric(label="Nombres de clients", value=numerize(Nombre_clients))

with total3:
    #st.image('images/hand.png',use_column_width='Auto')
    st.metric(label= 'Total produits',value=numerize(Nombre_Produits))

with total4:
    #st.image('images/conversion.png',use_column_width='Auto')
    st.metric(label='Tansactions par agence',value= numerize(Nombre_Transactions))

with total5:
    #st.image('images/app_conversion.png',use_column_width='Auto')
    st.metric(label="Revenu moyen par agence",value= numerize(Revenu_moy))



Q1,Q2 = st.columns(2)
with Q1:
    fig1 = px.box(df, y="PRIMENETTE", notched=True)


    fig2 = px.box(df_apres_nettoyage, y="PRIMENETTE", notched=True)

    tab1, tab2 = st.tabs(["Avant nettoyage", "Aprés nettoyage"])
    with tab1:
        # Use the Streamlit theme.
        # This is the default. So you can also omit the theme argument.
        st.plotly_chart(fig1, theme=None, use_container_width=True)
    with tab2:
        # Use the native Plotly theme.
        st.plotly_chart(fig2, theme=None, use_container_width=True)
with Q2:
    fig1 = px.scatter(df, x="JOURNEE", y="PRIMENETTE", color='GROUPE')
    fig2 = px.scatter(df_apres_nettoyage, x="JOURNEE", y="PRIMENETTE", color='GROUPE')

    tab1, tab2 = st.tabs(["Avant nettoyage", "Aprés nettoyage"])
    with tab1:
        # Use the Streamlit theme.
        # This is the default. So you can also omit the theme argument.
        st.plotly_chart(fig1, theme=None, use_container_width=True)
    with tab2:
        # Use the native Plotly theme.
        st.plotly_chart(fig2, theme=None, use_container_width=True)

    
Q3,Q4 = st.columns(2)

with Q3:
    fig = px.pie(df, values=df['GROUPE'], names='GROUPE', title='Groupes distribution')
    st.plotly_chart(fig, theme=None, use_container_width=True)
with Q4:
    ig = px.scatter(df_apres_nettoyage[df_apres_nettoyage['CRMA']=='CE02'], x="JOURNEE", y="GRAPPE",color="GROUPE",size='PRIMENETTE',
                     hover_name="GRAPPE", log_x=False, size_max=60)


    st.plotly_chart(fig, theme=None, use_container_width=True)

    








