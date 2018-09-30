'''
 cd C:\\Users\\Matheus\\AppData\\Local\\Programs\\Python\\Python37-32\\Scripts\\venv\\Scripts
 activate
 cd C:\\Users\\Matheus\\Desktop\\MicroSiga
 login.py
 '''

from flask import Flask, request, render_template, redirect, url_for, json, session
import requests
from aluno import *
from pdf import *

app = Flask(__name__)

@app.route('/')
def index():
	if request.method=='GET':
		if "usuario" in session:
			return redirect(url_for("home"))
		return render_template('login.html')

@app.route('/logout',methods=['POST','GET'])
def logout():
	session.pop("usuario",None)
	session.pop("admin",None)
	return redirect(url_for("login"))

@app.route('/cadastro')
def cadastro():
	return render_template('cadastro.html', status=None)

@app.route('/cadastrar',methods=['POST'])
def cadastrar():
	dictPreenchido = dict()

	nome = request.form['nome']
	usuario = request.form['usuario']
	senha = request.form['senha']
	email = request.form['email']
	curso = request.form['curso']
	dataNasci = request.form['dataNasci']

	existeCampoVazio = verificarCampoVazio([nome,usuario,senha,email,curso,dataNasci])
	usuarioExiste = buscarAluno(usuario) != None

	if existeCampoVazio == False:
		if usuarioExiste:
			return render_template('cadastro.html',status = "Usuario já cadastrado!")
		elif len(senha) < 6:
			return render_template('cadastro.html',status = "Senha muito curta!")
		elif "@" not in email:
			return render_template('cadastro.html',status = "Email incorreto!")
		else:
			aluno = Aluno(nome,usuario,senha,dataNasci,email,curso,"[]")
			status = aluno.cadastrarAluno()
			print(status)
			return redirect(url_for('login'))
	return render_template('cadastro.html',status = "Algum campo não foi preenchido corretamente!")

def verificarCampoVazio(listaCampos):
	for i in listaCampos:
		if i == None or i.strip(" ") == "":
			return True
	return False

def buscarAluno(usuario):
	# Tenta abrir o arquivo, se nao conseguir, ele criar e abre
	try:
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
	return a	

@app.route("/home")
def home():
	if 'usuario' in session:
		usuario=session['usuario']
		print(usuario)
		aluno = buscarAluno(usuario)
		with open('disciplinasJSON.json') as f:
			data = json.load(f)
		#print(disciplinas)
		#print(type(disciplinas))
		print(data)
		print(aluno)
		print(aluno.getDisciplinas())
		
		return render_template('loginValido.html',aluno = aluno, data = data)	
	return redirect(url_for("index"))

@app.route("/home/dashboard",methods=['POST','GET'])
def dashboard():
	if 'usuario' in session:
		if 'admin' in session and session['admin']:
			alunos = buscarListaAlunos()
			return render_template('dashboard.html',alunos = alunos)
		return redirect(url_for("home"))
	return redirect(url_for("index"))

def buscarListaAlunos():
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
def excluirUsuario():
	
	usuario = request.form["btnExcluir"]
	excluirAluno(usuario)


	return redirect(url_for("dashboard"))

def excluirAluno(usuario):
	alunos = buscarListaAlunos()
	print(alunos[0].getUsuario())
	#Limpar o arquivo
	open('Registro.txt', 'w').close()
	for i in alunos:
		if i.getUsuario() == usuario:
			print(i.getUsuario())
			continue
		status = i.cadastrarAluno()
		print(status)
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

@app.route("/downloadPDF", methods=['POST'])
def downloadPDF():
	if request.method == 'POST':
		lista = request.form.getlist("disciplinas")
		#print(lista)
		pdf = PDF("teste.pdf")
		pdf.gerarPDF(lista)
		return redirect(url_for("home"))

if __name__ == "__main__":
	app.secret_key = "session_key"
	app.run(debug=True)
