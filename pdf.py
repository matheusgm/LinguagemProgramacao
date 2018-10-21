from reportlab.lib.pagesizes import A4,landscape,letter
from reportlab.pdfgen import canvas as c
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.rl_config import defaultPageSize
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from flask import json
import textwrap

class PDF:
	def __init__(self, nome):
		self.nome = nome

	def gerarPDF(self,Disciplinas):
		#PAGE_HEIGHT=defaultPageSize[1]; 
		#PAGE_WIDTH=defaultPageSize[0]
		#xFinal = PAGE_HEIGHT - 36
		#Inicio = 36
		#yFinal = PAGE_WIDTH - 36
		#print("H: "+str(PAGE_HEIGHT))
		#print("W: "+str(PAGE_WIDTH))
		#print(str(inch))
		'''
		canvas = c.Canvas(self.nome, pagesize=A4)
		canvas.setLineWidth(.8)
		canvas.setFont('Helvetica', 12)

		with open('tabelaPrograma.json') as f:
			self.data = json.load(f)
		'''
		#self.geraTabela(canvas)
		# make text go straight up
		#canvas.rotate(90)
		'''
		for i in Disciplinas:
			self.geraTabela(canvas)
			canvas.rotate(90)
			canvas.drawString((200),-10,i.upper())
			canvas.drawString((200),-10,Disciplinas[i]["codigo"])
			
			canvas.showPage()
		'''
		doc = SimpleDocTemplate(self.nome, pagesize = landscape(A4), rightMargin=0, leftMargin=0, topMargin=30, bottomMargin=0)
		elements = []
		styles=getSampleStyleSheet()

		P = Paragraph('''
      		<para align=center spaceb=3>The <b>ReportLab Left
       		<font color=red>Logo</font></b>
       		Image</para>''',
       styles["BodyText"])

		for i in Disciplinas:
			CHT = str(Disciplinas[i]["cargaHoraria"]["T"])
			CHP = str(Disciplinas[i]["cargaHoraria"]["P"])
			creditos = str(Disciplinas[i]["creditos"])
			objetivo = str(Disciplinas[i]["objetivo"])
			#ParagrafoCH = Paragraph('<para align=center spaceb=3> <p>CARGA HÓRARIA POR PERÍODO:</p>T:'+CHT+'P:'+CHP+'T+P:'+str(int(CHT)+int(CHP))+'@@@@@@@@@@@@@@@@</para>', styles["BodyText"])
			cursos = ", ".join(Disciplinas[i]["cursos"])
			bibliografias = ""
			for j in Disciplinas[i]["bibliografias"]:
				bibliografias+=(j+"\n")
			ementa = str(Disciplinas[i]["ementa"])

			data=  [['UFRJ\n\nSR-1 - CEG', 'FORMULARIO CEG/03\n\nDISCIPLINA', '','CENTRO: de Tecnologia\nUNIDADE: COPPE\nPROGRAMA: ECI', '',"FOLHA N:\n\nDATA:"],
			        ['1 - NOME:\n\n'+str(i), '', '', '', '2 - CÓDIGO:\n\n'+str(Disciplinas[i]["codigo"]),'3 - IDENTIFICAÇÃO:\n\n'],
			        ['4 - CARGA HÓRARIA POR PERÍODO:\n\nT: '+CHT+'                P: '+CHP+'                T+P: '+str(int(CHT)+int(CHP)), '', '5 - CREDITOS:\n\n                '+creditos, '6 - REQUISITOS: (P): pré-requisito/ (C): co-requisito\n\n', '', ''],
			        ['7 - CARACTERÍSTICA(S) DA(S) AULA(S) PRÁTICA(S):\n\n', '', '','', '', ''],
			        ['8 - CURSOS PARA OS QUAIS É OFERECIDA:\n\n'+cursos, '', '','', '', ''],
			        ['9 - OBJETIVOS GERAIS DA DISCIPLINA:\n\n'+self.wrap(objetivo,150), '', '','', '', ''],
			        ['10 - EMENTA:\n\n'+self.wrap(ementa,150), '', '','', '', ''],
			        ['11 - BIBLIOGRAFIA BÁSICA PARA O ALUNO:\n\n'+bibliografias, '', '','', '', '']]
			t=Table(data,120,rowHeights = (55,50,50,55,60,70,90,95),style=[
	                ('GRID',(0,0),(-1,-1),2,colors.black),
	                #('BACKGROUND',(0,0),(1,1),colors.palegreen),
	                ('SPAN',(1,0),(2,0)),
	                ('SPAN',(3,0),(4,0)),
	                ('SPAN',(0,1),(3,1)),
	                ('SPAN',(0,2),(1,2)),
	                ('SPAN',(3,2),(-1,2)),
	                ('SPAN',(0,3),(-1,3)),
	                ('SPAN',(0,4),(-1,4)),
	                ('SPAN',(0,5),(-1,5)),
	                ('SPAN',(0,6),(-1,6)),
	                ('SPAN',(0,7),(-1,7)),
                    ('VALIGN',(0,0),(-1,-1),'TOP'),
                    ('ALIGN',(0,0),(2,0),'CENTER'),
                    ('ALIGN',(0,1),(-1,-1),'LEFT'),
                    ('ALIGN',(3,0),(-1,0),'LEFT'),
	                #('BACKGROUND',(-2,-2),(-1,-1), colors.pink),
	                ])

			elements.append(t)
		# write the document to disk
		doc.build(elements)

		#canvas.drawString((200),10,"i.upper()")
		#canvas.save()

	def wrap(self,s,width):
		return "\n".join(textwrap.wrap(s, width=width))
	'''
	def geraTabela(self, canvas):
		
		#print(self.data)
		#print("Tipo: "+str(type(self.data)))
		somaH = 0
		somaW = 0
		xInicio = 36
		yInicio = 36
		flag = 0
		for i in self.data:
			linha = self.data[i]
			coluna = linha["coluna"]
			h = int(coluna["h"])
			w = coluna["w"]
			somaW=0
			if(flag > 1):
				somaH+=5
			for j in w:
				canvas.rect(xInicio+somaH,yInicio+somaW,h,j,stroke=1, fill=0)
				somaW+=j
			somaH+=h

			
			flag+=1
			#print(coluna)
	'''