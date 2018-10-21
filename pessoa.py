class Pessoa:
	def __init__(self,nome, usuario, senha,dataNascimento, email):
		self.nome = nome
		self.usuario = usuario
		self.senha = senha
		self.dataNascimento = dataNascimento
		self.email = email

	def getUsuario(self):
		return self.usuario

	def getSenha(self):
		return self.senha

	def getNome(self):
		return self.nome

	def getDataNascimento(self):
		return self.dataNascimento

	def getEmail(self):
		return self.email