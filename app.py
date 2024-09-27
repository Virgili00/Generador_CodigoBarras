from codigo_barras import *
import streamlit as st

 
st.title("Generador de codigo de barras ")

uploaded_file = st.file_uploader(
    label="Agrega tu archivo excel o sheet",
    accept_multiple_files=False,
    type=['xlsx','xls']
)


if uploaded_file is not None:
    # Mostrar el botón que generará y descargará el PDF
    generar = st.button("Generar PDFs")

    # Solo proceder si se ha presionado el botón
    if generar:
        # Generar el PDF en memoria
        pdf_data =GeneradorPDF(uploaded_file)
        # Mostrar el botón de descarga inmediatamente después de generar el PDF
        st.download_button(
            label="Descargar PDF",
            data=pdf_data.generarZip(),
            file_name="codigo_barras.zip",
            mime="application/zip"
        )
    generar_png = st.button("Generar PNGs")
    if generar_png:
        # Generar el PDF en memoria
        pdf_data =GeneradorPDF(uploaded_file)
        # Mostrar el botón de descarga inmediatamente después de generar el PDF
        st.download_button(
            label="Descargar PNG",
            data=pdf_data.generarPng(),
            file_name="codigo_barras.zip",
            mime="application/zip"
        )
        
else:
    st.warning("Por favor, sube un archivo para generar el PDF.")

