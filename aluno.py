class Aluno:
	def __init__(self, nome, usuario, senha,  curso):
		self.nome = nome
		self.usuario = usuario
		self.senha = senha
		self.curso = curso

	def getUsuario(self):
		return self.usuario

	def getSenha(self):
		return self.senha