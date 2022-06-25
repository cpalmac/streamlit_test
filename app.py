from re import X
import pandas as pd
import streamlit as st
import requests
import io



def cargarDataSet():
    """
    Funcion cargarDataSet\n
    Carga archivo csv en dataset de Pandas\n
    Retorna: dataset df"""
    
    url="https://raw.githubusercontent.com/cpalmac/streamlit_test/master/Netflix2.csv"
    s=requests.get(url).content
    
    df=pd.read_csv(io.StringIO(s.decode('UTF-8')), on_bad_lines="skip",sep=";")

    return df

def generarApp():
    """
    Funcion generarApp\n
    Genera el formulario de busqueda para las peliculas\n
    Retorna: \n
    dataset = data \n
    genero= opcion seleccionada como filtro genero \n
    pais= opcion seleccionada como filtro pais"""

    
    st.set_page_config(page_title="Taller_4", page_icon="", layout="centered")
    columna_encabezado = st.columns((4,1))
    columna_encabezado[0].title("Buscador peliculas NETFLIX")
    columna_encabezado[1].image(image='https://raw.githubusercontent.com/cpalmac/streamlit_test/master/netflix.png',width=80)


    df = cargarDataSet()
    df.columns = ["ID",	"TITULO",	"DESCRIPCION",	"GENERO",	"REPARTO",	"DIRECTOR",	"PAIS"	,"AGREGADA_NETFILX"	,"ANIO",	"CATEGORIA",	"DURACION_MM",	"TEMPORADA",	"RATING"]
    data = df
    
    columna = st.columns((3,1))
    genero = columna[0].selectbox("Genero",options=listaGenero(data))
    
    pais = columna[1].selectbox("Pais",options=listaPais(data))
   
    botones = st.columns((1,1))
    if botones[0].button("Buscar"):
        buscarPelicula(data,genero,pais)

    if botones[1].button("Limpiar"):
        pass

def buscarPelicula(data=None,genero=None,pais=None):
    """
    Funcion buscarPelicula\n
    Ejecuta los filtros de busqueda para las peliculas\n
    Entrada: \n
    data = dataset \n
    genero= opcion seleccionada como filtro genero \n
    pais= opcion seleccionada como filtro pais"""
 
    data_filtro = data
    filtro = 0
    if  genero != "Seleccione":
        data_filtro = data_filtro[data_filtro.GENERO == genero][["TITULO","DESCRIPCION","ANIO","PAIS","RATING","DIRECTOR","REPARTO","GENERO"]]
        filtro = 1

    if pais != "Seleccione":
        data_filtro = data_filtro[data_filtro.PAIS == pais][["TITULO","DESCRIPCION","ANIO","PAIS","RATING","DIRECTOR","REPARTO","GENERO"]]
        filtro = 1

    if filtro == 1:
        
        if data_filtro["ANIO"].count()> 0:
            st.write(data_filtro)
            genero = ""
            pais = ""
            filtro = 0
        else:
            st.warning("No se encuentran registros")
            filtro = 0
            genero = ""
            pais = ""
        

    elif filtro == 0:
        st.error("Debe ingresar Titulo o Genero")

    
        
def listaGenero(data=None):
    """
    Funcion listaGenero\n
    Genera la lista de generos para cargar en filtro genero\n
    Retorna: genero_list"""
    data = data.sort_values("GENERO")

    genero_list = data["GENERO"].unique()
    genero_list[0] = "Seleccione"

    return genero_list

def listaPais(data=None):
    """
    Funcion listaPais\n
    Genera la lista de paises para cargar en filtro pais\n
    Retorna: pais_list"""
    data = data.sort_values("PAIS")
    pais_list = data["PAIS"].unique()
    pais_list[0] = "Seleccione"

    return pais_list
            


generarApp()
