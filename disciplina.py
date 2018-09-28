class Disciplina:
	def __init__(self, nome, credito, nota):
		self.nome = nome
		self.credito = credito
		self.nota = nota

	def situacao(self):
		if self.nota != -1:
			if self.nota >= 5:
				return "Aprovado"
			else:
				return "Reprovado"
		else:
			return "Cursando"