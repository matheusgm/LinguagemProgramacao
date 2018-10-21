'''
 cd C:\\Users\\Matheus\\AppData\\Local\\Programs\\Python\\Python37-32\\Scripts\\venv\\Scripts
 activate
 cd C:\\Users\\Matheus\\Desktop\\UFRJ\\LinguagemProgramacao\\MicroSiga
 main.py
 '''

from flask import Flask, request, render_template, redirect, url_for, json, session, send_file
import requests
from aluno import *
from pdf import *

app = Flask(__name__)

@app.route('/')
def index(): # Pagina Inicial
	if request.method=='GET':
		if "usuario" in session:  # verifica se o usuario está logado
			return redirect(url_for("home"))  # se sim, redireciona para a home
		return render_template('login.html')  # se não, abre pagina de login

@app.route('/logout',methods=['POST','GET'])
def logout():  # Rota para realizar o logout
	session.pop("usuario",None)  # Retira o usuario da sessão
	session.pop("admin",None)  # Retira o admin da sessão, caso seja admin
	return redirect(url_for("login"))  # Redireciona para a pagina de login

@app.route('/cadastro')  
def cadastro():  # Rota para realizar o cadastro
	return render_template('cadastro.html', status=None)  # Pagina do cadastro

@app.route('/cadastrar',methods=['POST'])
def cadastrar():  # Cadastrar

	nome = request.form['nome']
	usuario = request.form['usuario']
	senha = request.form['senha']
	email = request.form['email']
	curso = request.form['curso']
	dataNasci = request.form['dataNasci']
	disciplinas = request.form['disciplinas']
	if disciplinas == None or disciplinas == "":
		disciplinas = "[]"
	else:
		disciplinas = disciplinas.split(",")

	existeCampoVazio = verificarCampoVazio([nome,usuario,senha,email,curso,dataNasci]) # verifica a existencia de campo vazio
	usuarioExiste = buscarAluno(usuario) != None  # verifica se o usuario já foi criado

	if existeCampoVazio == False: 
		if usuarioExiste: # Usuario já cadastrado
			return render_template('cadastro.html',status = "Usuario já cadastrado!")  
		elif len(senha) < 6: # Senha muito curto (menor que 6 caracteres)
			return render_template('cadastro.html',status = "Senha muito curta!")
		elif "@" not in email: # Nao possui o "@", logo não pode ser um email
			return render_template('cadastro.html',status = "Email incorreto!")
		else:  # Tudo correto
			aluno = Aluno(nome,usuario,senha,dataNasci,email,curso,str(disciplinas).replace("'",'"')) # Cria o Aluno
			status = aluno.cadastrarAluno()  # Cadastra ele no banco
			print(status)
			return redirect(url_for('login')) # Ao fim do cadastro, redireciona ele para a pagina de login
	return render_template('cadastro.html',status = "Algum campo não foi preenchido corretamente!")  # Exibe mensagem na pagina de cadastro, caso exista campos em branco

def verificarCampoVazio(listaCampos): # Função que verifica a existencia de campo vazio
	for i in listaCampos:
		if i == None or i.strip(" ") == "": # Se tiver pelo menos 1 campo vazio, ele já retorna verdadeiro
			return True
	return False

def buscarAluno(usuario):  # Função para buscar um Aluno no Banco
	try: # Tenta abrir o arquivo, se nao conseguir, ele criar e abre
		arq = open("Registro.txt","r")
	except(Exception):
		arq = open("Registro.txt","w")
		arq.close()
		arq = open("Registro.txt","r")
	a = None
	# Leitura do arquivo 
	linha = arq.readline()
	while(linha):
		linha = linha.strip("\n")
		json_aluno = json.loads(linha)
		if json_aluno["usuario"] == usuario.lower():
			a = Aluno(json_aluno["nome"],json_aluno["usuario"],json_aluno["senha"],json_aluno["dataNascimento"],json_aluno["email"],json_aluno["curso"], json_aluno["disciplinas"])
			break
		linha = arq.readline()
	arq.close()
	return a	# Se o aluno existir, retorna o Aluno. Caso contrario, retorna Null

@app.route("/home")
def home(): # Rota da Pagina de home
	if 'usuario' in session: # Verifica se existe usuario logado na sessão
		usuario=session['usuario']
		#print(usuario)
		aluno = buscarAluno(usuario) # busca o Aluno no Banco
		with open('disciplinasJSON.json') as f:
			data = json.load(f) # Pega todas as disciplinas já cadastradas
		#print(disciplinas)
		#print(type(disciplinas))
		#print("Todas Disciplinas: "+str(data))
		#print(aluno)
		#print(aluno.getDisciplinas())
		
		return render_template('home.html',aluno = aluno, data = data)	# Exibe a pagina home do usuario
	return redirect(url_for("index")) # Caso não exista usuario logado, o cliente será redireciona para a pagina inicial

@app.route("/home/cadastroDisciplina")
def cadastroDisciplina(): # Rota para realizar o cadastro de disciplinas
	if "usuario" in session:
		return render_template('cadastrarDisciplina.html')
	return redirect(url_for('index'))

@app.route("/home/cadastrarDisciplina", methods=['POST'])
def cadastrarDisciplina(): # Cadastrar Disciplinas
	
	nome = request.form['nome']
	codigo = request.form['codigo']
	creditos = request.form['creditos']
	cargaHorariaTeoria = request.form['cargaHorariaTeoria']
	cargaHorariaPratica = request.form['cargaHorariaPratica']
	cursos = request.form['cursos']
	objetivo = request.form['objetivo']
	ementa = request.form['ementa']
	bibliografia = request.form['bibliografia']

	existeCampoVazio = verificarCampoVazio([nome,codigo,creditos,cargaHorariaPratica,cargaHorariaTeoria,cursos,objetivo,ementa,bibliografia]) # verifica a existencia de campo vazio
	if existeCampoVazio == False:

		dic= dict()
		dic["codigo"] = codigo
		dic["cargaHoraria"] = dict()
		dic["cargaHoraria"]["T"] = cargaHorariaTeoria
		dic["cargaHoraria"]["P"] = cargaHorariaPratica
		dic["creditos"] = creditos
		dic["cursos"] = cursos.split(",")
		dic["objetivo"] =objetivo
		dic["ementa"] = ementa
		dic["bibliografias"] = bibliografia.split("\r\n")

		#print(dic)

		with open('disciplinasJSON.json', encoding='utf-8') as f:
				data = json.load(f) 
		data[nome] = dic
		with open('disciplinasJSON.json','w') as f:
				res = json.dumps(data) 
				f.write(res)

		return redirect(url_for("home"))
	return redirect(url_for("cadastroDisciplina"))

@app.route("/home/dashboard",methods=['POST','GET'])
def dashboard(): # Rota do dashboard
	if 'usuario' in session: # verifica se o usuario está logado
		if 'admin' in session and session['admin']: # verifica se o usuario é admin
			alunos = buscarListaAlunos() # Busca todos os alunos do Banco
			return render_template('dashboard.html',alunos = alunos) # Exibe a dashboard com todos os alunos
		return redirect(url_for("home")) # Caso não seja admin, será redirecionado para home
	return redirect(url_for("index")) # Caso não esteja logado, será redirecionado para a pagina inicial

def buscarListaAlunos():  # Função para buscar todos os alunos do banco
	alunos = []
	arq = open("Registro.txt","r")
	linha = arq.readline()
	while(linha):
		linha = linha.strip("\n")
		json_aluno = json.loads(linha)
		a = Aluno(json_aluno["nome"],json_aluno["usuario"],json_aluno["senha"],json_aluno["dataNascimento"],json_aluno["email"],json_aluno["curso"], json_aluno["disciplinas"])
		alunos.append(a)
		linha = arq.readline()
	arq.close()
	return alunos

@app.route("/salvarEdicaoUsuario",methods=['POST'])
def salvarEdicaoUsuario():



	return redirect(url_for("dashboard"))

@app.route("/editarUsuario",methods=['POST'])
def editarUsuario():
	
	usuario = request.form["btnEditar"]
	aluno = buscarAluno(usuario)


	return render_template("editarUsuario.html", aluno = aluno)

@app.route("/excluirUsuario",methods=['POST'])
def excluirUsuario(): # Rota para excluir o usuario do Banco, através da dashboard
	
	usuario = request.form["btnExcluir"] #pega o usuario a ser excluido
	excluirAluno(usuario) #exclui o usuario


	return redirect(url_for("dashboard")) #redireciona para a pagina dashboard

def excluirAluno(usuario): # Função para excluir o Aluno
	alunos = buscarListaAlunos()
	#print(alunos[0].getUsuario())
	#Limpar o arquivo
	open('Registro.txt', 'w').close()
	for i in alunos:
		if i.getUsuario() == usuario:
			print(i.getUsuario())
			continue
		status = i.cadastrarAluno()
		#print(status)
	return

@app.route("/login", methods=['POST','GET'])
def login():

	if request.method == 'POST':
		if request.form['submit_button'] ==  'Login':
			# Dados do Formulario
			usuario = request.form['usuario']
			senha = request.form['senha']

			flagValido = False
			aluno = buscarAluno(usuario)
			if aluno is not None:
				flagValido = aluno.verificarLogin(usuario,senha)


			if flagValido:
				#session['logged_in'] = True
				session['usuario'] = usuario.lower()
				if usuario.lower() == "matheus":
					session['admin'] = True
				else:
					session['admin'] = False
				return redirect(url_for('home'))
			else:
				status = 'Usuario/Senha Invalido'
				return render_template("login.html",status=status)
			
		else:
			return redirect(url_for('cadastro'))
	return render_template("login.html")

@app.route("/formHome",methods=['POST'])
def formHome():
	if request.method == 'POST':
		if request.form['submit_button'] == 'Gerar PDF':
			return downloadPDF()
		else:
			return redirect(url_for('cadastroDisciplina'))

		

@app.route("/downloadPDF",methods=['POST'])
def downloadPDF(): # Rota para realizar a criação e o download do PDF
	if request.method == 'POST':
		if "usuario" in session:
			lista = request.form.getlist("disciplinas")
			print("Lista: "+str(lista))

			if len(lista) > 0:
				with open('disciplinasJSON.json', encoding='utf-8') as f:
					disci = json.load(f)
				materia = dict()
				for i in disci:
					if disci[i]["codigo"] in lista:
						materia[i] = disci[i]

				pdf = PDF("teste.pdf") # Cria o PDF
				pdf.gerarPDF(materia) #Gera o PDF das disciplinas

				return send_file('teste.pdf', as_attachment=True)
			return redirect(url_for("home")) # Redireciona para home
		return redirect(url_for('index'))

if __name__ == "__main__":
	app.secret_key = "session_key"
	app.run(debug=True)
