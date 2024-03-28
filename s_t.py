from textblob import TextBlob
import pandas as pd
import streamlit as st
from googletrans import Translator
from gtts import gTTS
import os
import time
import glob

st.title('CocinaFacil - Análisis de Sentimientos')

translator = Translator()

def remove_files(n):
    mp3_files = glob.glob("temp/*mp3")
    if len(mp3_files) != 0:
        now = time.time()
        n_days = n * 86400
        for f in mp3_files:
            if os.stat(f).st_mtime < now - n_days:
                os.remove(f)
                print("Deleted ", f)

def text_to_speech(input_language, output_language, text, tld):
    translation = translator.translate(text, src=input_language, dest=output_language)
    trans_text = translation.text
    tts = gTTS(trans_text, lang=output_language, tld=tld, slow=False)
    try:
        my_file_name = text[0:20]
    except:
        my_file_name = "audio"
    tts.save(f"temp/{my_file_name}.mp3")
    return my_file_name, trans_text

recipe_options = ["Nueva receta", "Receta anterior"]

with st.expander('Analizar frase'):
    text = st.selectbox('Elige una opción:', recipe_options)
    
    if text == "Nueva receta":
        text_input = st.text_input('Escribe por favor tu receta: ')
    else:
        # Use the recipe from the previous selection
        text_input = trans_text if 'trans_text' in locals() else ""
        st.write(f"Receta anterior: {text_input}")

    if text_input:
        translation = translator.translate(text_input, src="es", dest="en")
        trans_text = translation.text
        blob = TextBlob(trans_text)
        st.write('Polarity: ', round(blob.sentiment.polarity,2))
        st.write('Subjectivity: ', round(blob.sentiment.subjectivity,2))
        x = round(blob.sentiment.polarity,2)
        if x >= 0.5:
            st.write('Es un sentimiento Positivo 😊')
            st.subheader("¡Te recomendamos probar esta receta positiva!")
            st.write("Nombre: Ensalada de quinoa con aguacate, tomate y aderezo de limón")
            st.write("Ingredientes:")
            st.write("- 1 taza de quinoa cocida")
            st.write("- 1 aguacate maduro, cortado en cubitos")
            st.write("- 1 tomate grande, cortado en cubitos")
            st.write("- Zumo de 1 limón")
            st.write("- Sal y pimienta al gusto")
            st.write("- Hojas de lechuga (opcional)")
            st.write("Preparación:")
            st.write("1. En un tazón grande, mezcla la quinoa cocida, el aguacate y el tomate.")
            st.write("2. Exprime el zumo de limón sobre la ensalada y sazona con sal y pimienta al gusto.")
            st.write("3. Opcionalmente, sirve sobre hojas de lechuga.")
        elif x <= -0.5:
            st.write('Es un sentimiento Negativo 😔')
            st.subheader("¡Te recomendamos probar esta receta reconfortante!")
            st.write("Nombre: Sopa de verduras reconfortante")
            st.write("Ingredientes:")
            st.write("- 2 zanahorias, cortadas en rodajas")
            st.write("- 2 ramas de apio, picadas")
            st.write("- 1 cebolla, picada")
            st.write("- 2 dientes de ajo, picados")
            st.write("- 1 papa grande, pelada y cortada en cubos")
            st.write("- 4 tazas de caldo de verduras")
            st.write("- Sal y pimienta al gusto")
            st.write("- Perejil fresco picado (opcional, para decorar)")
            st.write("Preparación:")
            st.write("1. En una olla grande, saltea la cebolla y el ajo en un poco de aceite hasta que estén dorados.")
            st.write("2. Agrega las zanahorias, el apio y la papa, y cocina por unos minutos.")
            st.write("3. Vierte el caldo de verduras, lleva a ebullición y luego reduce el fuego. Cocina a fuego lento hasta que las verduras estén tiernas.")
            st.write("4. Sazona con sal y pimienta al gusto.")
            st.write("5. Sirve caliente, decorado con perejil fresco si lo deseas.")
        else:
            st.write('Es un sentimiento Neutral 😐')
            st.subheader("¡Te recomendamos probar esta receta!")
            st.write("Nombre: Pasta con salsa de tomate y albahaca")
            st.write("Ingredientes:")
            st.write("- 250g de pasta de tu elección")
            st.write("- 2 tazas de salsa de tomate")
            st.write("- Un puñado de hojas de albahaca fresca")
            st.write("- Sal y pimienta al gusto")
            st.write("- Queso parmesano rallado (opcional, para servir)")
            st.write("Preparación:")
            st.write("1. Cocina la pasta según las instrucciones del paquete hasta que esté al dente. Escurre y reserva.")
            st.write("2. Calienta la salsa de tomate en una sartén grande.")
            st.write("3. Agrega las hojas de albahaca picadas y sazona con sal y pimienta al gusto.")
            st.write("4. Incorpora la pasta cocida a la salsa y mezcla bien.")
            st.write("5. Sirve caliente, con queso parmesano rallado si lo deseas.") 

text = st.text_input("Ingrese el texto que se utilizará para generar el audio")
display_output_text = st.checkbox("Mostrar el texto")

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

if st.button("Aceptar"):
    result, output_text = text_to_speech(input_language, output_language, text, tld)
    audio_file = open(f"temp/{result}.mp3", "rb")
    audio_bytes = audio_file.read()
    st.markdown(f"## Tu audio:")
    st.audio(audio_bytes, format="audio/mp3", start_time=0)

    if display_output_text:
        st.write(f"### Ahora puedes compartir tu receta con más personas")
        st.write(f" {output_text}")

remove_files(7)

   



