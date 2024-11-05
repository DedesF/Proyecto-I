import pandas as pd
from fastapi import FastAPI, HTTPException

app = FastAPI(debug=True)

#Cargamos los datasets


df = pd.read_csv('Datasets/joined_dataset.csv')
df_dir = pd.read_csv('Datasets/directores.csv')
df_for_analisys = pd.read_pickle('Analisis/peliculas.pkl')
similaridad = pd.read_pickle('Analisis/similaridad.pkl')

#df = pd.read_csv('C:\Python\HENRY-Data-Science\Proyecto_1\Datasets\joined_dataset.csv')
#df_dir = pd.read_csv('C:\Python\HENRY-Data-Science\Proyecto_1\Datasets\directores.csv')
#df_for_analisys = pd.read_pickle('C:\Python\HENRY-Data-Science\Proyecto_1\Analisis\peliculas.pkl')
#similaridad = pd.read_pickle('C:\Python\HENRY-Data-Science\Proyecto_1\Analisis\similaridad.pkl')


df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce') #nomralizamos la columna de fechas


#Función que debe devolver la cantidad de películas que fueron estrenadas en el mes consultado en la totalidad del dataset.

@app.get('/cantidad_filmaciones_mes/{mes}')
def cantidad_filmaciones_mes(mes:str):

    mes = mes.lower().strip()
    meses_anio = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 
                'junio', 'julio', 'agosto', 'septiembre', 'octubre', 
                'noviembre', 'diciembre']
    
    # Validamos si el día es correcto
    if mes not in meses_anio:
        raise HTTPException(status_code=404, detail="Mes no válido")
    
    # Mapeamos cada mes del año a su valor numérico (0 = enero, ..., 12 = diciembre)
    mes_numero = {'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4,
                    'mayo': 5, 'junio': 6, 'julio': 7, 'agosto': 8,
                    'septiembre': 9, 'octubre': 10, 'noviembre': 11, 'diciembre': 12}
    
    # Convertimos los meses a números de mes del año y contamos ocurrencias
    matriz = df['release_date'].dt.month.value_counts()
    cantidad = matriz.get(mes_numero[mes], 0)
    
    return {f"{cantidad} cantidad de películas fueron estrenadas en el mes de {mes}"}


#Función que devolve la cantidad de películas que fueron estrenadas en el día consultado en la totalidad del dataset.

@app.get('/cantidad_filmaciones_dia/{dia}')
def cantidad_filmaciones_dia(dia:str):
    dia = dia.lower().strip() #Normalizamos el string
    dias_semana = ['lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado', 'domingo']
    
    # Validamos si el día es correcto
    if dia not in dias_semana:
        raise HTTPException(status_code=404, detail="Día no válido")
    
    # Mapeamos cada día de la semana a su valor numérico (0 = lunes, ..., 6 = domingo)
    dia_numero = {'lunes': 0, 'martes': 1, 'miercoles': 2, 'jueves': 3,
                    'viernes': 4, 'sabado': 5, 'domingo': 6}
    
    # Convertimos las fechas a números de día de la semana y contamos ocurrencias
    matriz = df['release_date'].dt.dayofweek.value_counts()
    cantidad = matriz.get(dia_numero[dia], 0)
    
    # Devolvemos el mensaje con el valor de cantidad
    return {f"{cantidad} películas fueron estrenadas durante los días {dia}"}


#Funcion que pide el título de una filmación esperando como respuesta el título, el año de estreno y el score.

@app.get('/score_titulo/{titulo_de_la_filmacion}')
def score_titulo(titulo_de_la_filmacion:str):

    titulo_de_la_filmacion = titulo_de_la_filmacion.title().strip() #Normalizamos el string

    try:# Verificamos si el título existe en el DataFrame
        # Filtramos el DataFrame y obtenemos la primera coincidencia
        film_data = df[df['title'] == titulo_de_la_filmacion].iloc[0]
    except IndexError:
        # Lanzamos una excepción si el título no existe
        raise HTTPException(status_code=404, detail="Película no encontrada")

    row_number = df.index.get_loc(df[df['title'] == titulo_de_la_filmacion].index[0])
    anio = int(df['year'][row_number])
    score = float(df['popularity'][row_number])    

    return {f'La película {titulo_de_la_filmacion} fue estrenada en el año {anio} con un score/popularidad de {score}'}


#Función que pide el título de una filmación esperando como respuesta el título, la cantidad de votos y el valor promedio de 
# las votaciones. La misma variable deberá de contar con al menos 2000 valoraciones, caso contrario, debemos contar 
# con un mensaje avisando que no cumple esta condición y que por ende, no se devuelve ningun valor.

@app.get('/votos_titulo/{titulo_de_la_filmacion}')
def votos_titulo(titulo_de_la_filmacion: str):
    
    titulo_de_la_filmacion = titulo_de_la_filmacion.title().strip() # Normalizamos el título    
    
    try:# Verificamos si el título existe en el DataFrame
        # Filtramos el DataFrame y obtenemos la primera coincidencia
        film_data = df[df['title'] == titulo_de_la_filmacion].iloc[0]
    except IndexError:
        # Lanzamos una excepción si el título no existe
        raise HTTPException(status_code=404, detail="Película no encontrada")

    # Extraemos los valores necesarios
    anio = int(film_data['year'])
    promedio = float(film_data['vote_average'])
    val = int(film_data['vote_count'])
    
    # Devolvemos el resultado con base en el número de valoraciones
    if val >= 2000:
        return {
            f"La película {titulo_de_la_filmacion} fue estrenada en el año {anio}. "
            f"La misma cuenta con un total de {val} valoraciones, con un promedio de {promedio}."}
    else:
        return {"mensaje": "La película tiene menos de 2000 valoraciones"}


#Función que pide el nombre de un actor que se encuentre dentro de un dataset debiendo devolver el éxito 
#del mismo medido a través del retorno. Además, la cantidad de películas que en las que ha participado 
#y el promedio de retorno. La definición no deberá considerar directores.

@app.get('/get_actor/{nombre_actor}')
def get_actor(nombre_actor: str):
    # Normalizamos el nombre del actor
    nombre_actor = nombre_actor.title().strip()
    
    # Verificamos si el actor existe en el DataFrame
    try:
        actores = df[df['cast'] == nombre_actor].iloc[0]
    except IndexError:
        raise HTTPException(status_code=404, detail="El actor no fue encontrado")

    # Comprobamos si el actor ha trabajado como director
    if nombre_actor in df_dir['name'].values:
        return {"mensaje": "El actor ha trabajado como director"}

    # Filtramos el DataFrame para obtener películas del actor
    matriz = df[df['cast'] == nombre_actor]
    peliculas = matriz['id'].count()
    retorno = matriz['return'].sum()
    promedio = matriz['return'].mean()

    # Devolvemos los datos sobre la participación del actor en filmaciones
    return {f"El actor {nombre_actor} ha participado de {peliculas} filmaciones. "
            f"Ha conseguido un retorno total de {retorno} con un promedio de {promedio} por filmación."}

#La funcion pide el nombre de un director que se encuentre dentro de un dataset debiendo devolver el 
# éxito del mismo medido a través del retorno. Además, deberá devolver el nombre de cada película 
# con la fecha de lanzamiento, retorno individual, costo y ganancia de la misma.
@app.get('/get_director/{nombre_director}')
def get_director(nombre_director: str):
    # Normalizamos el nombre del director
    nombre_director = nombre_director.title().strip()
    
    # Filtramos el DataFrame para obtener solo las películas del director
    director_films = df[df['crew'].str.contains(nombre_director, case=False, na=False)]
    director_films = director_films.sort_values(by='return', ascending=False) #ordenamos el dataset para que devuelva en la película de
                                                                              #mayor éxito primero
    
    # Verificamos si el director tiene películas en el DataFrame
    if director_films.empty:
        raise HTTPException(status_code=404, detail="El director no fue encontrado o no tiene películas registradas.")
    
    # Calculamos el éxito total (retorno total) del director
    total_return = director_films['return'].sum()
    
    # Creamos la lista de detalles de cada película
    films_detail = []
    for _, row in director_films.iterrows():
        
        film_info = {"title": row['title'],
                    "release_date": row['release_date'],
                    "return": row['return'],
                    "budget": row['budget'],
                    "revenue": row['revenue']}
        films_detail.append(film_info)
    
    # Devolvemos la respuesta
    return {"director": nombre_director,
            "total_return": total_return,
            "films": films_detail}


@app.get('/recomendacion/{pelicula}')
def recomendacion(pelicula:str):
    pelicula = pelicula.title().strip()

    #try:
        #pelicula = df_for_analisys[df_for_analisys['title'] == pelicula].iloc[0]
    #except IndexError:
        #raise HTTPException(status_code=404, detail="La película no fue encontrada")

    recomendaciones = []

    indice = df_for_analisys[df_for_analisys['title'] == pelicula].index[0]

    distancia = sorted(list(enumerate(similaridad[indice])), reverse=True, key=lambda x: x[1])

    for i in distancia[1:6]:
        recomendaciones.append(df_for_analisys.iloc[i[0]].title)
    return recomendaciones