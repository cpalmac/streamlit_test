from concurrent.futures.process import _threads_wakeups
from enum import auto
from pickle import TRUE
from unittest.util import sorted_list_difference
from warnings import catch_warnings
import pandas as pd
import pandas as pd
import streamlit as st
import requests
import io


def cargarDataSet():
    """
    Funcion cargarDataSet\n
    Carga archivo csv en dataset de Pandas\n
    Retorna: dataset df"""
    st.set_page_config(page_title="Taller_4", page_icon="", layout="centered")
    columna_encabezado = st.columns((4,1))
    columna_encabezado[0].title("Buscador peliculas NETFLIX")
    columna_encabezado[1].image(image='https://raw.githubusercontent.com/cpalmac/streamlit_test/master/netflix.png',width=80)


    url="https://raw.githubusercontent.com/cpalmac/streamlit_test/master/Netflix.csv"
    s=requests.get(url).content
    df=pd.read_csv(io.StringIO(s.decode('utf-8')), on_bad_lines="skip",sep=";")

    return df

def generarApp():
    """
    Funcion generarApp\n
    Genera el formulario de busqueda para las peliculas\n
    Retorna: \n
    dataset = data \n
    genero= opcion seleccionada como filtro genero \n
    pais= opcion seleccionada como filtro pais"""
    df = cargarDataSet()
    df.columns = ["ID",	"TITULO",	"DESCRIPCION",	"GENERO",	"REPARTO",	"DIRECTOR",	"PAIS"	,"AGREGADA_NETFILX"	,"ANIO",	"CATEGORIA",	"DURACION_MM",	"TEMPORADA",	"RATING"]


    data = df

    data = data.sort_values("GENERO")

    genero_list = data["GENERO"].unique()
    genero_list = genero_list
    genero_list[0] = "Seleccione"
    data = data.sort_values("PAIS")
    pais_list = data["PAIS"].unique()
    pais_list[0] = "Seleccione"
    columna = st.columns((3,1))

    genero = columna[0].selectbox("Genero",options=genero_list,index=0)
    pais = columna[1].selectbox("Pais",options=pais_list)

    buscarPelicula(data,genero,pais)

def buscarPelicula(data=None,genero=None,pais=None):
    """
    Funcion buscarPelicula\n
    Ejecuta los filtros de busqueda para las peliculas\n
    Entrada: \n
    data = dataset \n
    genero= opcion seleccionada como filtro genero \n
    pais= opcion seleccionada como filtro pais"""
    if st.button("Buscar"):
        data_filtro = data
        filtro = 0
        if  genero != "Seleccione":
            data_filtro = data_filtro[data_filtro.GENERO == genero][["TITULO","DESCRIPCION","ANIO","PAIS","RATING","DIRECTOR","REPARTO"]]
            filtro = 1

        if pais != "Seleccione":
            data_filtro = data_filtro[data_filtro.PAIS == pais][["TITULO","DESCRIPCION","ANIO","PAIS","RATING","DIRECTOR","REPARTO"]]
            filtro = 1

        if filtro == 1:
            
            if data_filtro["ANIO"].count()> 0:
                st.write(data_filtro)
                genero = ""
                pais = ""
                filtro = 0
            else:
                st.error("No se encuentran registros")
                filtro = 0
                genero = ""
                pais = ""
            

        elif filtro == 0:
            st.error("Debe ingresar Titulo o Genero")
        

            


generarApp()
