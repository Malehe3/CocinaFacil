# Importar las bibliotecas necesarias
from textblob import TextBlob
import pandas as pd
import streamlit as st
from googletrans import Translator
from gtts import gTTS
import os
import time
import glob

# Título de la aplicación
st.title('CocinaFacil - Análisis de Sentimientos')

# Inicializar el traductor de Google
translator = Translator()

# Función para eliminar archivos antiguos
def remove_files(n):
    mp3_files = glob.glob("temp/*mp3")
    if len(mp3_files) != 0:
        now = time.time()
        n_days = n * 86400
        for f in mp3_files:
            if os.stat(f).st_mtime < now - n_days:
                os.remove(f)
                print("Deleted ", f)

# Función para convertir texto a voz
def text_to_speech(input_language, output_language, text, tld):
    translation = translator.translate(text, src=input_language, dest=output_language)
    trans_text = translation.text
    tts = gTTS(trans_text, lang=output_language, tld=tld, slow=False)
    try:
        my_file_name = text[0:20]
    except:
        my_file_name = "audio"
    
    # Verificar si el directorio existe, si no, crearlo
    if not os.path.exists("temp/"):
        os.makedirs("temp/")
    
    tts.save(f"temp/{my_file_name}.mp3")
    return my_file_name, trans_text

# Sección para analizar una frase ingresada por el usuario
with st.expander('Analizar frase'):
    text = st.text_input('Escribe por favor: ')
    if text:
        translation = translator.translate(text, src="es", dest="en")
        trans_text = translation.text
        blob = TextBlob(trans_text)
        st.write('Polarity: ', round(blob.sentiment.polarity,2))
        st.write('Subjectivity: ', round(blob.sentiment.subjectivity,2))
        x = round(blob.sentiment.polarity,2)
        if x >= 0.5:
            st.write('Es un sentimiento Positivo 😊')
            st.subheader("¡Te recomendamos probar esta receta positiva!")
            st.write("Nombre: Ensalada de quinoa con aguacate, tomate y aderezo de limón")
            # Resto de la receta positiva
        elif x <= -0.5:
            st.write('Es un sentimiento Negativo 😔')
            st.subheader("¡Te recomendamos probar esta receta reconfortante!")
            st.write("Nombre: Sopa de verduras reconfortante")
            # Resto de la receta negativa
        else:
            st.write('Es un sentimiento Neutral 😐')
            st.subheader("¡Te recomendamos probar esta receta!")
            st.write("Nombre: Pasta con salsa de tomate y albahaca")
            # Resto de la receta neutral

# Sección para generar audio a partir de texto
text = st.text_input("Ingrese el texto que se utilizará para generar el audio")

# Selector de idioma de entrada
in_lang = st.selectbox(
    "Elige el idioma en el que compartiste tu receta",
    ("Inglés", "Español", "Alemán", "Francés", "Bengalí", "Coreano", "Mandarín", "Japonés"),
)

if in_lang == "Inglés":
    input_language = "en"
elif in_lang == "Español":
    input_language = "es"
elif in_lang == "Alemán":
    input_language = "de"
elif in_lang == "Francés":
    input_language = "fr"
elif in_lang == "Bengalí":
    input_language = "bn"
elif in_lang == "Coreano":
    input_language = "ko"
elif in_lang == "Mandarín":
    input_language = "zh-cn"
elif in_lang == "Japonés":
    input_language = "ja"

# Selector de idioma de salida
out_lang = st.selectbox(
    "Elige el idioma en el que quieres compartir tu receta",
    ("Inglés", "Español", "Alemán", "Francés", "Bengalí", "Coreano", "Mandarín", "Japonés"),
)

if out_lang == "Inglés":
    output_language = "en"
elif out_lang == "Español":
    output_language = "es"
elif out_lang == "Alemán":
    output_language = "de"
elif out_lang == "Francés":
    output_language = "fr"
elif out_lang == "Bengalí":
    output_language = "bn"
elif out_lang == "Coreano":
    output_language = "ko"
elif out_lang == "Mandarín":
    output_language = "zh-cn"
elif out_lang == "Japonés":
    output_language = "ja"

# Selector de acento para el idioma inglés
english_accent = st.selectbox(
    "Elige un acento",
    (
        "Defecto",
        "Español",
        "Reino Unido",
        "Estados Unidos",
        "Canada",
        "Australia",
        "Irlanda",
        "Sudáfrica",
    ),
)

if english_accent == "Defecto":
    tld = "com"
elif english_accent == "Español":
    tld = "com.mx"
elif english_accent == "Reino Unido":
    tld = "co.uk"
elif english_accent == "Estados Unidos":
    tld = "com"
elif english_accent == "Canada":
    tld = "ca"
elif english_accent == "Australia":
    tld = "com.au"
elif english_accent == "Irlanda":
    tld = "ie"
elif english_accent == "Sudáfrica":
    tld = "co.za"

# Botón para generar audio
if st.button("Aceptar"):
    result, output_text = text_to_speech(input_language, output_language, text, tld)
    audio_file = open(f"temp/{result}.mp3", "rb")
    audio_bytes = audio_file.read()
    st.markdown(f"## Tu audio:")
    st.audio(audio_bytes, format="audio/mp3", start_time=0)

    if display_output_text:
        st.write(f"### Ahora puedes compartir tu receta con más personas")
        st.write(f" {output_text}")

# Eliminar archivos antiguos
remove_files(7)
