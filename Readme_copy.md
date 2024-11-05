# PROYECTO INDIVIDUAL UNO

Proyecto individual del curso de data science part-time de Henry

## Índice

1. Objetivo
2. Descripción del proyecto
3. Data Engineering
   1. ETL
   2. EDA
4. Levanamiento en FastAPI
5. Deploying
6. Video de presentación

## Objetivos

El objetivo del proyecto es aplicar los conocimiento adquiridos durante los módulos teóricos para armar un sistema de recomendación de películas en el que el usuario pueda conocer alternativas a películas que le hayan gustado

## Descripción del proyecto

Cumpliremos el rol de un data engineer que provee servicio de agregación de plataformas de streaming donde tendremos que crear un sistema de recomendación que aún no ha sido puesto en marcha. Para esto debemos tomar una base de datos cruda con nula madurez de los mismos (datos anidados, sin transformar, nulos, etc) y aplicar un **ETL** que nos permita trabajar con ellos.

Una vez normalizados los datos debemos proceder a trabajar con ellos para hacer un **EDA** y construir a partir de ahí nuestro sistema de recomendación.

## Data Engineering

### ETL

En ciencia de datos, un **ETL** (Extract, Transform, Load) es un proceso de tres pasos que permite recopilar, transformar y cargar datos desde diversas fuentes hacia una base de datos o un sistema de almacenamiento. Este proceso es fundamental para preparar los datos antes de que puedan analizarse, ya que garantiza que estén en el formato y la calidad adecuados. Veamos cada paso en detalle para asociarlos con el proyecto:

* **Extract (Extracción):** En esta fase, recopilamos los datos desde 2 datasets en formato .csv proporcionados por los repositorios de Henry, uno llamado dataset_movies.csv y el otro credits.csv. La información recibida venía cruda, por lo que nos topamos con información mal ingresada, en formato no corespondientes, valores nulos entre otros.
* **Transform (Transformación):** Una vez que se cargaron los datos se procedio a:
  * Hacer la limpieza de datos (remover duplicados, tratar valores nulos o inconsistentes).
  * Normalizar los datos, vale decir, transformarlos a sus tipos correspondientes, verificar que los strings tengan el mismo formato, etc.
  * Filtrado y selección de de los datos que serán usados para el modelo. Se elimina información del dataset que no es necesaria para nuestro objetivo.
  * Enriquecimos los datos creando o agregando información que nos será de utilidad.
* **Load (Carga):** Una vez transformado el dataset lo guardamos para poder cargarlo a los repositorios con el fin de ser usados para nuestros modelos.

### EDA

La segunda etapa en la manipulación de los datos es el **EDA** (Exploratory Data Analysis) o Análisis Exploratorio de Datos por sus siglas en inglés. en esta etapa hacemos la investigación y tratamos de entender el conjunto de datos antes de aplicar modelos o técnicas analíticas. Con los datasets generados en el **ETL** buscamos relaciones basadas en el resumen , el género y el título de cada película a fin de identificar patrones que se puedan usar para la recomendación.

Para este proyecto usamos la librería de scikit-learn con lo módulos de TfidfVectorizer que transforma el texto a una matriz numérica hecha con los principios de TF, que entre más aparece una palabra específica en un texto específico más importante es, y IDF, que entre mas aparece una palabra en diferentes textos menos importante es, para luego con el modulo de cosine_similarity encontrar las distancias más cercanas que representarían las películas con mayor similitud y que serán usadas para recomendación

## Levantamiento en FastAPI

Para ejecutar y alojar nuestra aplicación creada para un entorno de producción usaremos **FastAPI**. En ella haremos el levantamiento de todas las funciones creadas para nuestro programa:

1. **cantidad_filmaciones_mes()** --> podremos ver la cantidad de filmaciones hecha en determinado mes del año
2. **cantidad_filmaciones_dia()** --> podemos ver la cantidad de filmaciones hechas según el día de la semana
3. **score_titulo()** --> podemos ver la puntuación obtenida por determinado título segun valoraciones de la gente
4. **votos_titulo()** --> podemos ver la cantidad de votos y el promedio de esos votos por título
5. **get_actor()** --> podemos ver la cantidad de películas filamdas por actor y sus ganancias
6. **get_director()** --> obtenemos un listado con todas las películas del director en orden de relevancia según ganancias
7. **recomendacion()** --> Esta película nos recomienda 5 películas similares ordenadas de mayor a menor puntuación de similaridad

## Deploying

Para hacer el deploying del proyecto para que pueda ser visto por cualquier persona a través de un servidor web se ha usado RENDER RENDER nos permite cargar toda nuestra documentación (dataset, requirements, etc) y levantar el proyecto a través de un servicio web para que pueda ser consumido por la empresa y lo usuarios que lo necesiten.

Se debe acceder al proyecto a través del siguiente link:

[https://proy-uno.onrender.com](https://proy-uno.onrender.com "https://proy-uno.onrender.com")

## Video de presentación
