from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas as c
from reportlab.lib.units import inch
from reportlab.rl_config import defaultPageSize
from flask import json

class PDF:
	def __init__(self, nome):
		self.nome = nome

	def gerarPDF(self,listaDisciplinas):
		PAGE_HEIGHT=defaultPageSize[1]; 
		PAGE_WIDTH=defaultPageSize[0]
		xFinal = PAGE_HEIGHT - 36
		Inicio = 36
		yFinal = PAGE_WIDTH - 36
		#print("H: "+str(PAGE_HEIGHT))
		#print("W: "+str(PAGE_WIDTH))
		#print(str(inch))
		canvas = c.Canvas(self.nome, pagesize=A4)
		canvas.setLineWidth(.3)
		canvas.setFont('Helvetica', 12)
		
		self.geraTabela(canvas)

		# make text go straight up
		canvas.rotate(90)

		x = 0
		for i in listaDisciplinas:
			canvas.drawString((200),-10,i.upper())
			x+=10

		canvas.showPage()
		canvas.drawString((200),10,"i.upper()")
		canvas.save()

	def geraTabela(self, canvas):
		with open('tabelaPrograma.json') as f:
			data = json.load(f)
		#print(data)
		#print("Tipo: "+str(type(data)))
		somaH = 0
		somaW = 0
		xInicio = 36
		yInicio = 36
		flag = 0
		for i in data:
			linha = data[i]
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