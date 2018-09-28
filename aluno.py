class Aluno:
	def __init__(self, nome, usuario, senha, dataNascimento, email, curso, disciplinas):
		self.nome = nome
		self.usuario = usuario
		self.senha = senha
		self.curso = curso
		self.disciplinas = disciplinas
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

	def getCurso(self):
		return self.curso

	def getDisciplinas(self):
		return self.disciplinas



	def cadastrarAluno(self):
		try:
			
			print(self.email)
			registro = '{\
"usuario":"'+self.usuario.lower()+'\
","senha":"'+self.senha+'\
","nome":"'+self.nome+'\
","curso":"'+self.curso+'\
","email":"'+self.email+'\
","dataNascimento":"'+self.dataNascimento+'\
","disciplinas":'+str(self.disciplinas)+'\
}'

			print(registro)
			arq = open("Registro.txt","a")
			arq.write(registro+"\n")
			arq.close()
		except(Exception):
			raise
			return "Erro ao cadastrar aluno"

		return "Aluno cadastrado com sucesso"

	

	def verificarLogin(self, usuario, senha):
		if usuario.lower() == self.usuario and senha == self.senha:
			return True
		return False

