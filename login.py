'''
 cd C:\\Users\\Matheus\\AppData\\Local\\Programs\\Python\\Python37-32\\Scripts\\venv\\Scripts
 activate
 cd C:\\Users\\Matheus\\Desktop\\MicroSiga
 login.py
 '''

from flask import Flask, request, render_template, redirect, url_for, json
import requests
from aluno import *

app = Flask(__name__)

@app.route('/')
def index():
	try:
		status = request.args['msg']
		#print("Status: "+status)
	except(Exception):
		#print("Erro")
		return render_template('login.html', status = "")
	return render_template('login.html',msg=status)

@app.route('/cadastro')
def cadastro():
	return render_template('cadastro.html')

@app.route('/cadastroSitu',methods=['POST'])
def cadastroSitu():
	usuario = request.form['usuario']
	senha = request.form['senha']
	nota = request.form['nota']

	registro = usuario.lower()+"-"+senha+"-"+nota

	arq = open("Registro.txt","a")
	arq.write(registro+"\n")
	arq.close()
	status = 'Cadastradooo com Sucessooo'
	return redirect(url_for('index',msg = status))

def pegaListaAlunos():
	try:
		arq = open("Registro.txt","r")
	except(Exception):
		arq = open("Registro.txt","w")
		arq.close()
		arq = open("Registro.txt","r")
		
	listaAlunos = []
	linha = arq.readline()
	while(linha):
		linha = linha.strip("\n")
		linha = linha.split("-")
		a = Aluno("Nome",linha[0],linha[1],linha[2])
		listaAlunos.append(a)
		linha = arq.readline()
	arq.close()
	return listaAlunos

@app.route("/echo", methods=['POST'])
def echo():

	if request.method == 'POST':
		if request.form['submit_button'] ==  'Login':
			# Dados do Formulario
			usuario = request.form['usuario']
			senha = request.form['senha']

			listaAlunos = pegaListaAlunos()
			#print(listaAlunos)
			flagValido = False
			for i,el in enumerate(listaAlunos):
				if el.getUsuario() == usuario.lower() and el.getSenha() == senha:
					flagValido = True
					break

			if flagValido:
				return render_template('loginValido.html',usuario = usuario)
			else:
				status = 'Usuario/Senha Invalido'
				return redirect(url_for('index',msg = status))

			
		else:
			return redirect(url_for('cadastro'))	
			
if __name__ == "__main__":
    app.run(debug=True)
