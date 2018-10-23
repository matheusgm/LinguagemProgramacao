from pessoa import *
class Aluno(Pessoa):
	def __init__(self, nome, usuario, senha, dataNascimento, email, curso, disciplinas):
		self.curso = curso
		self.disciplinas = disciplinas
		Pessoa.__init__(self,nome, usuario, senha, dataNascimento, email)


	def getUsuario(self):
		return self.usuario.title()

	def getCurso(self):
		return self.curso

	def getDisciplinas(self):
		return self.disciplinas


	def cadastrarAluno(self):
		try:
			
			registro = '{"usuario":"'+self.usuario.lower()+'","senha":"'+self.senha+'","nome":"'+self.nome+'\
","curso":"'+self.curso+'","email":"'+self.email+'","dataNascimento":"'+self.dataNascimento+'","disciplinas":'+str(self.disciplinas).replace("'",'"')+'\
}'

			#print(registro)
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

