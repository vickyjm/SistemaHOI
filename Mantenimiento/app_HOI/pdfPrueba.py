from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.pdfgen import canvas
from django.contrib.auth.models import User
from reportlab.lib.units import inch,mm
from reportlab.lib import colors
from reportlab.platypus.flowables import Image
from Mantenimiento.settings import MEDIA_URL, MEDIA_ROOT
from reportlab.platypus.tables import Table, TableStyle
from app_HOI.models import Ingresa, Aprueba, Crea

class MiPDF:
    def __init__(self, buffer, pagesize):
        self.buffer = buffer
        if pagesize == 'A4':
            self.pagesize = A4
        elif pagesize == 'Letter':
            self.pagesize = letter
        self.width,self.heighht = self.pagesize

    def print_reporte(self):
        buffer = self.buffer
        doc = SimpleDocTemplate(buffer,
                                rightMargin = inch/4,
                                leftMargin = inch/4,
                                topMargin = inch/2,
                                bottomMargin = inch/4,
                                pagesize = self.pagesize)
        elements = []
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='centered',alignment=TA_CENTER))

        elements.append(Paragraph('Ingresos',styles['Heading2']))
        
        table = [["Nombre", "Categoría", "Cantidad", "Ingresado por"]]
        ingresos = Ingresa.objects.all()
        for item in ingresos:
            table.append([item.id_item.nombre,item.id_item.id_categoria,item.cantidad,item.id_usuario.get_full_name()])
        #table.append(["Total ingresos: "+str(len(table)-1)])
        user_table = Table(table, colWidths=[doc.width/4.0]*4)
        user_table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor(0xD8D8D8)),
                                        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                                        ('BOX', (0, 0), (-1, -1), 0.25, colors.black)]))
        elements.append(user_table)
        
        elements.append(Paragraph('Solicitudes',styles['Heading2']))
        
        table = [["Solicitante", "Departamento","Item","Cantidad","Aprobado por", "Fecha solicitud","Fecha aprobado"]]
        solicitudes = Aprueba.objects.all()
        for elem in solicitudes:
            autor = Crea.objects.get(pk=elem.id_solicitud)
            table.append([autor.id_usuario.get_short_name(),elem.id_solicitud.dpto,autor.id_item.nombre,
                          elem.id_solicitud.cantidad, elem.id_usuario.get_short_name(),autor.fecha,elem.fecha])
        #table.append(["Total ingresos: "+str(len(table)-1)])
        user_table = Table(table, colWidths=[doc.width/7.0]*7)
        user_table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor(0xD8D8D8)),
                                        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                                        ('BOX', (0, 0), (-1, -1), 0.25, colors.black)]))
        elements.append(user_table)
        doc.build(elements,onFirstPage=self._header_footer,onLaterPages=self._header_footer, canvasmaker=CanvasNumerado)
        pdf = buffer.getvalue()
        buffer.close()
        return pdf    
    
    @staticmethod
    def _header_footer(canvas,doc):
        canvas.saveState()
        styles = getSampleStyleSheet()
        
        logo = MEDIA_ROOT + "logo.jpg"
        header = Paragraph("",styles['Title'])
        w, h = header.wrap(doc.width, doc.topMargin)
        header.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin - h)
        canvas.restoreState()
              
class CanvasNumerado(canvas.Canvas):
    def __init__(self,*args,**kwargs):
        canvas.Canvas.__init__(self,*args,**kwargs)
        self._saved_page_states = []
        
    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()
        
    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)
        
    def draw_page_number(self,page_count):
        self.drawString(95*mm, 15*mm+(0.2*inch),"Página %d de %d" % (self._pageNumber, page_count))