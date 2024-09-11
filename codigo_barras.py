import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.graphics.barcode import createBarcodeDrawing
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.shapes import Group
from reportlab.lib.units import cm
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
    def __init__(self, row):
        self.row = row

    def getNombre(self):
        nombre = f"{self.row['DESCRIPCION']}_{self.row['TALLE']}_{self.row['SKU']}"
        return nombre

    def generarPdf(self):
        # Crear el buffer en memoria
        buffer = BytesIO()

        # Establecer el tamaño del PDF a 6x3 cm
        c = canvas.Canvas(buffer, pagesize=(6*cm, 3*cm))

        # Dimensiones de la página en puntos (6x3 cm)
        ancho_pagina, alto_pagina = 6 * cm, 3 * cm

        # Margen en puntos (ajusta esto si lo necesitas)
        margen_x = 5

        # Crear el código de barras (EAN13 por ejemplo)
        codigo_barras = createBarcodeDrawing('EAN13', value=str(self.row['EANS']), barHeight=1.1*cm, humanReadable=True)

        # Ajustar la escala del código de barras
        factor_escala = 1.5  # Cambia este valor para ajustar el tamaño del código de barras
        ancho_codigo = codigo_barras.width * factor_escala
        alto_codigo = codigo_barras.height * factor_escala

        # Crear un dibujo con la escala ajustada
        d = Drawing(ancho_codigo, alto_codigo)
        d.add(Group(codigo_barras, transform=[factor_escala, 0, 0, factor_escala, 0, 0]))

        # Dibujar el código de barras centrado en la página
        x_position = (ancho_pagina - ancho_codigo) / 2
        d.drawOn(c, x_position, alto_pagina - alto_codigo - margen_x)

        # Añadir datos adicionales debajo del código de barras
        c.setFont("Helvetica", 6)
        texto_y = alto_pagina - alto_codigo - margen_x - 10  # Ajustar la posición del texto

        # Texto adicional en la parte inferior
        c.drawString(margen_x, texto_y, f"Ref: {self.row['SKU']}-{self.row['CODE COLOR']}")
        c.drawString(ancho_pagina - margen_x - 40, texto_y, f"Talle: {self.row['TALLE']}")

        # Descripción en el centro de la parte inferior
        c.setFont("Helvetica-Bold", 5)
        c.drawCentredString(ancho_pagina / 2.0, texto_y - 10, self.row['DESCRIPCION'])

        # Finalizar el PDF
        c.showPage()
        c.save()

        # Retornar el contenido del PDF
        buffer.seek(0)
        return buffer.getvalue()

    def getPdf(self):
        return self.generarPdf()

     
        
        
           
        
           
    


