from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import  TA_LEFT
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch,mm
from reportlab.lib import colors
from reportlab.platypus.flowables import Image, ImageAndFlowables
from Mantenimiento.settings import MEDIA_ROOT
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

    def imprimir_reporte(self,usuario,fechaIni,fechaFin):
        buffer = self.buffer
        doc = SimpleDocTemplate(buffer,
                                rightMargin = 15*mm,
                                leftMargin = 15*mm,
                                topMargin = 15*mm,
                                bottomMargin = 15*mm,
                                pagesize = self.pagesize)
        elements = []
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='logo',alignment=TA_LEFT,leftIndent=1*mm,
                                  fontSize=14))
        
        logo = MEDIA_ROOT + "/logo.jpg"
        elements.append(ImageAndFlowables(Image(logo,width=75*mm,height=25*mm),
                                          [Paragraph("<b>Departamento de Mantenimiento</b>",styles['logo']),
                                           Paragraph("Reporte de ingresos y solicitudes",styles['Heading2'])],
                                          imageSide = 'left'))
        
        tablaHeader = [["Nombre: "+usuario.first_name, "Apellido: "+usuario.last_name], 
                  ["Fecha inicial: "+str(fechaIni), "Fecha final: "+str(fechaFin)]]
        
        header = Table(tablaHeader, colWidths=[doc.width/2.0]*2)
        header.setStyle(TableStyle([('INNERGRID', (0, 0), (-1, -1), 0.25, colors.white),
                                    ('BOX', (0, 0), (-1, -1), 0.25, colors.white)]))
        elements.append(header)

        elements.append(Paragraph('Ingresos',styles['Heading2']))
        
        auxIngresos = [["Nombre", "Categoría", "Cantidad", "Ingresado por","Fecha"]]
        ingresos = Ingresa.objects.all()
        for item in ingresos:
            if (fechaIni <= item.fecha.date() <= fechaFin):
                auxIngresos.append([item.id_item.nombre,item.id_item.id_categoria,item.cantidad,
                          item.id_usuario.get_full_name(),item.fecha.date()])
        
        if (len(auxIngresos)==1):
            elements.append(Paragraph('No hay nuevos ingresos de material en este período de tiempo.',styles['df']))
        else:
            tablaIngresos = Table(auxIngresos, colWidths=[doc.width/5.0]*5)
            tablaIngresos.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor(0xD8D8D8)),
                                            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                                            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                                            ('FONTSIZE',(0,0),(-1,-1),9.5)]))
            elements.append(tablaIngresos)
        
        elements.append(Paragraph('Solicitudes',styles['Heading2']))
        
        auxSolicitud = [["CI Solicitante", "Departamento","Ítem","Cantidad","Aprobado por", 
                         "Fecha solicitud","Fecha aprobado"]]
        solicitudes = Aprueba.objects.all()
        for elem in solicitudes:
            if (fechaIni <= elem.fecha.date() <= fechaFin):
                autor = Crea.objects.get(pk=elem.id_solicitud.id)
                auxSolicitud.append([autor.id_usuario.username,elem.id_solicitud.dpto,autor.id_item.nombre,
                              elem.id_solicitud.cantidad, elem.id_usuario.username,autor.fecha.date(),
                              elem.fecha.date()])
        if (len(auxSolicitud)==1):
            elements.append(Paragraph('No se realizaron ni aprobaron solicitudes en este período de tiempo.',
                                      styles['df']))
        else:
            tablaSolicitud = Table(auxSolicitud, colWidths=[doc.width/7.0]*7)
            tablaSolicitud.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor(0xD8D8D8)),
                                            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                                            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                                            ('FONTSIZE',(0,0),(-1,-1),9.5)]))
            elements.append(tablaSolicitud)
        
        doc.build(elements, canvasmaker=CanvasNumerado)
        pdf = buffer.getvalue()
        buffer.close()
        return pdf    
    
              
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