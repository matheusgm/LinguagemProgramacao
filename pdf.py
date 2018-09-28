from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas as c

class PDF:
	def __init__(self, nome):
		self.nome = nome

	def gerarPDF(self,listaDisciplinas):
		canvas = c.Canvas(self.nome, pagesize=letter)
		canvas.setLineWidth(.3)
		canvas.setFont('Helvetica', 12)

		canvas.drawString(30,750,'COMUNICADO OFICIAL')
		canvas.drawString(30,735,'EMPRESAS ACME')
		canvas.drawString(500,750,"12/12/2011")
		canvas.line(480,747,580,747)

		canvas.drawString(275,725,'SALDO DEVEDOR:')
		canvas.drawString(500,725,"R$ 1.000,00")
		canvas.line(378,723,580,723)

		canvas.drawString(30,703,'RECEBIDO POR:')
		canvas.line(130,700,580,700)
		canvas.drawString(130,703,"JOHN DOE")
		x = 0
		for i in listaDisciplinas:
			canvas.drawString(30,100-x,i.upper())
			x+=10


		canvas.save()