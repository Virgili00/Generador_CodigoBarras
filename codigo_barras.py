import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.graphics.barcode import createBarcodeDrawing
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.shapes import Group
from io import BytesIO  # Para crear el archivo en memoria
import zipfile as zip

# Leer el archivo Excel
class GeneradorPDF:
    def __init__(self,archivo):
        self.archivo=archivo

    def generarDataFrame(self):
        df = pd.read_excel(self.archivo, sheet_name=0, engine='openpyxl')
        return df
    
    def generarZip(self):
        zip_memoria=BytesIO()
        with zip.ZipFile(zip_memoria,'w') as zip_file: 
            for indice,row in self.generarDataFrame().iterrows():
                try:
                    pdf=Pdf(row)
                    zip_file.writestr(f"{pdf.getNombre()}_{indice}.pdf",pdf.getPdf())
                except:pass
        zip_memoria.seek(0)
        print("se concreto la generacion")
        return zip_memoria.getvalue()

class Pdf:
    def __init__(self,row):
        self.row=row
        
    def getNombre(self):
        nombre=f"{self.row['DESCRIPCION']}_{self.row['TALLE']}_{self.row['SKU']}"
        return nombre
    def generarPdf(self):
            buffer=BytesIO()
            c = canvas.Canvas(buffer, pagesize=A4)
            # Dimensiones de la página
            ancho_pagina, alto_pagina = A4
            # Margen
            margen_x = 50
            codigo_barras = createBarcodeDrawing('EAN13', value=str(self.row['EANS']), barHeight=30, humanReadable=True)
            
            # Ajustar la escala del código de barras
            factor_escala = 3  # Cambiar este valor para escalar el código de barras
            ancho_codigo = codigo_barras.width * factor_escala
            alto_codigo = codigo_barras.height * factor_escala

            # Crear un dibujo con la escala ajustada
            d = Drawing(ancho_codigo, alto_codigo)
            d.add(Group(codigo_barras, transform=[factor_escala, 0, 0, factor_escala, 0, 0]))

            # Dibujar el código de barras centrado
            x_position = (ancho_pagina - ancho_codigo) / 2
            d.drawOn(c, x_position, alto_pagina - alto_codigo - 200)  # Ajustar la posición vertical del código de barras

            # Datos adicionales debajo del código de barras
            c.setFont("Helvetica", 12)
            texto_y = alto_pagina - alto_codigo - 200 - 15  # Reducir aún más el margen vertical para acercar el texto al código de barras

            # Ajustar el texto para que coincida con el ancho del código de barras
            c.drawString(x_position + margen_x, texto_y, f"Ref: {self.row['SKU']}")
            c.drawString(x_position + ancho_codigo - margen_x , texto_y, f"Talle: {self.row['TALLE']}")

            # Descripción centrada con tamaño de fuente más pequeño
            c.setFont("Helvetica-Bold", 9)  # Tamaño de fuente reducido
            c.drawCentredString(ancho_pagina / 2.0, alto_pagina - alto_codigo - 200 -30, self.row['DESCRIPCION'])  # Ajustar la posición vertical de la descripción

            # Añadir una nueva página para el siguiente código de barras
            c.showPage()
            # Crear el pdf
            c.save()
            buffer.seek(0)
            return buffer.getvalue()
    def getPdf(self):
        pdfBuffer=self.generarPdf()
        return pdfBuffer
    

     
        
        
           
        
           
    


