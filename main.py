import os
from http.server import SimpleHTTPRequestHandler
import socketserver
from urllib.parse import parse_qs, urlparse
import hashlib
 
# Class MyHandler = Try to open 'login.html' file

class MyMandler(SimpleHTTPRequestHandler):
    def list_directory(self, path):
        
        try:
            f = open(os.path.join(path, 'index.html'), 'r')
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(f.read().encode('utf-8'))
            f.close
            return None

        except FileNotFoundError:
            pass
 
        return super().list_directory(path)

# GET = Try to open and read 'login.html' file
      
    def do_GET(self):
        if self.path =='/login':

            try:
                with open(os.path.join(os.getcwd(), 'login.html'), 'r') as login_file:
                    content = login_file.read()
                self.send_response(200)
                self.send_header("content-type","text/html")
                self.end_headers()
                self.wfile.write(content.encode('utf-8'))          

            except FileNotFoundError:
                pass

# Path if the login or password be incorrect 
                     
        elif self.path == '/login_failed':

            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
           

            with open(os.path.join(os.getcwd(), 'login.html'), 'r', encoding='utf-8') as login_file:
                content = login_file.read()
               

            mensagem = "Login e/ou senha incorreta. Tente novamente"
            content = content.replace('<!-- Mensagem de erro será inserida aqui -->',
                                      f'<div class="error-message">{mensagem}</div>')
           
     
            self.wfile.write(content.encode('utf-8')) 

# Path if the class/activity is already registered
            
        elif self.path == '/turma_failed':

            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
           

            with open(os.path.join(os.getcwd(), 'cadastro_turma.html'), 'r', encoding='utf-8') as login_file:
                content = login_file.read()
               

            mensagem = " Turma já cadastrada. Tente novamente!"
            content = content.replace('<!-- Mensagem de erro será inserida aqui -->',
                                      f'<div class="error-message">{mensagem}</div>')
           
     
            self.wfile.write(content.encode('utf-8')) 
        
        elif self.path == '/atividade_failed':

            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
           

            with open(os.path.join(os.getcwd(), 'cadastro_atividade.html'), 'r', encoding='utf-8') as login_file:
                content = login_file.read()

            mensagem = " Atividade já cadastrada. Tente novamente!"
            content = content.replace('<!-- Mensagem de erro será inserida aqui -->',
                                      f'<div class="error-message">{mensagem}</div>')
           
     
            self.wfile.write(content.encode('utf-8')) 

# New user register 
       
        elif self.path.startswith('/novo_cadastro'):
 

            query_params = parse_qs(urlparse(self.path).query)
            login = query_params.get('login',[''])[0]
            senha = query_params.get('senha',[''])[0]
 
            welcome_message = f"Olá {login}, seja bem-vindo! Percebemos que você é novo por aqui.Complete seu cadastro"
 
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
 
            with open(os.path.join(os.getcwd(), 'cadastro.html'),'r', encoding='utf-8') as novo_cadastro_file:
                content = novo_cadastro_file.read()
 
            content = content.replace('{login}', login)
            content = content.replace('{senha}', senha)
            content = content.replace('{welcome_message}',welcome_message)
 
            self.wfile.write(content.encode('utf-8'))
 
            return

# open and read 'cadastro_turma.html' file
              
        elif self.path == '/turma':
            
            self.send_response(200)
            self.send_header("content-type","text/html; charset=utf-8")
            self.end_headers()
            with open(os.path.join(os.getcwd(), 'cadastro_turma.html'), 'r', encoding='utf-8') as file:
                content = file.read()
            self.wfile.write(content.encode('utf-8')) 

        elif self.path == '/atividade':
            
            self.send_response(200)
            self.send_header("content-type","text/html; charset=utf-8")
            self.end_headers()
            with open(os.path.join(os.getcwd(), 'cadastro_atividade.html'), 'r', encoding='utf-8') as file:
                content = file.read()
            self.wfile.write(content.encode('utf-8'))          
        

        else:

            super().do_GET()

# check if the user already exists 
            
    def usuario_existente(self, login, senha):
            with open('dados.login.txt', 'r', encoding='utf-8') as file:
                for line in file:
                    if line.strip():
                        stored_login, stored_senha_hash, stored_nome = line.strip().split(';')
                    if login == stored_login:
                        # criptography the password
                        senha_hash = hashlib.sha256(senha.encode('UTF-8')).hexdigest()
                        return senha_hash == stored_senha_hash
            return False

# check if the class already exists
    
    def turma_existente(self, codigo, descricao):
            with open('dados_turmas.txt', 'r', encoding='utf-8') as file:
                for line in file:
                    if line.strip():
                        cod, desc = line.strip().split(';')
                    if codigo == cod:
                        return True
            return False
    
    def atividade_existente(self, codigo, descricao):
            with open('dados_atividade.txt', 'r', encoding='utf-8') as file:
                for line in file:
                    if line.strip():
                        disciplina, desc = line.strip().split(';')
                    if codigo == disciplina:
                        return True
            return False

# function to add an user
    
    def adicionar_usuario(self,login,senha,nome):
        senha_hash = hashlib.sha256(senha.encode("UTF-8")).hexdigest()
        with open('dados.login.txt', 'a', encoding='UTF-8') as file:
            file.write(f'{login};{senha_hash};{nome}\n')

# function to add a class
              
    def adicionar_turmas(self, codigo, descricao):
        with open('dados_turmas.txt', 'a', encoding='utf-8') as files:
            files.write(f'{codigo};{descricao}\n')
    
    def adicionar_atividade(self, codigo, descricao):
        with open('dados_atividade.txt', 'a', encoding='utf-8') as files:
            files.write(f'{codigo};{descricao}\n')
 
 
# function to remove a line
            
    def remover_ultima_linha(self,arquivo):
        print("Vou excluir ultima linha")
        with open(arquivo, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            with open(arquivo, 'w', encoding='utf-8') as file:
                file.writelines(lines[:-1])
 
# POST function
                
    def do_POST(self):

        # Rota para enviar o login

        if self.path == '/enviar_login':
 
            content_length = int(self.headers['content-Length'])

            body = self.rfile.read(content_length).decode('utf-8')
          
            form_data = parse_qs(body)

            # Acessa os dados do login
 
            login = form_data.get('email', [''])[0]
            senha = form_data.get('senha', [''])[0]

            # Caso o usuário já exista, a página 'tela_professor.html' é carregada
           
            if self.usuario_existente(login, senha):
                with open(os.path.join(os.getcwd(), 'tela_professor.html'), 'r', encoding='utf-8') as existe:
                    content_file = existe.read()
                mensagem = f"Olá professor {login}"
                content = content_file.replace('<!-- Mensagem de autenticacao será inserida aqui -->',
                                      f'<p>{mensagem}</p>')

                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
            
                self.wfile.write(content.encode('utf-8'))
           
            else:

                # Lógica para a rota '/login_failed' caso email/senha esteja incorreto

                if any(line.startswith(f"{login};") for line in open("dados.login.txt", "r", encoding="UTF-8")):
                    self.send_response(302)
                    self.send_header('Location', '/login_failed')
                    self.end_headers()
                    return
               
                else:

                # Adiciona um novo usuário no txt
                    
                    self.adicionar_usuario(login,senha, nome='None')
                    self.send_response(302)
                    self.send_header('Location', f'novo_cadastro?login={login}&senha={senha}')
                    self.end_headers()
                return
            
        # Lógica quando há novo usuário
 
        elif   self.path.startswith('/confirmar_cadastro'):
            
            content_length = int(self.headers['Content-Length'])
            
            body= self.rfile.read(content_length).decode('utf-8')
            
            from_data = parse_qs(body, keep_blank_values=True)
 
            login = from_data.get('email', [''])[0]
            senha = from_data.get('senha', [''])[0]
            nome = from_data.get('nome', [''])[0]

            # Criptografar a senha
 
            senha_hash = hashlib.sha256(senha.encode('UTF-8')).hexdigest()
 
            if self.usuario_existente(login,senha):
 
                with open('dados.login.txt','r', encoding='utf-8') as file:
                    lines = file.readlines()
 
                with open('dados.login.txt','w', encoding='utf-8') as file:
                    for line in lines:
                        stored_login, stored_senha,stored_nome = line.strip().split(';')
                        if login == stored_login and senha_hash == stored_senha:
                            line = f"{login};{senha_hash};{nome}\n"
                        file.write(line)
                    
                    with open(os.path.join(os.getcwd(), 'tela_professor.html'),'r', encoding='utf-8') as file:
                        content = file.read()
 
                    self.send_response(302)
                    self.send_header("Content-type", "text/html; charset=utf-8")
                    self.end_headers()
                    self.wfile.write(content.encode('utf-8')) 
 
            else:
                    self.remover_ultima_linha('dados.login.txt')
                    self.send_response(302)
                    self.send_header("Content-type", "text/html; charset=utf-8")
                    self.end_headers()
                    self.wfile.write("A senha não confere.Retome o procedimento!". encode('utf-8'))
        
        # Lógica para cadastrar um turma

        elif self.path == '/cad_turma':           
                 
            content_length = int(self.headers['content-Length'])

            body = self.rfile.read(content_length).decode('utf-8')
          
            form_data = parse_qs(body)
 
            codigo = form_data.get('codigo', [''])[0]
            descricao = form_data.get('descricao', [''])[0]
           
            if self.usuario_existente(codigo, descricao):
                with open(os.path.join(os.getcwd(), 'cadastro_turma.html'), 'r', encoding='utf-8') as existe:
                    content_file = existe.read()
                mensagem = f"Turma já cadastrada. Tente novamente!"
                content = content_file.replace('<!-- Mensagem de autenticacao será inserida aqui -->',
                                      f'<p>{mensagem}</p>')

                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
            
                self.wfile.write(content.encode('utf-8'))
           
            else:

                if any(line.startswith(f"{codigo};") for line in open("dados_turmas.txt", "r", encoding="UTF-8")):
                    self.send_response(302)
                    self.send_header('Location', '/turma_failed')
                    self.end_headers()
                    return 
               
                else:
                    self.adicionar_turmas(codigo,descricao)
                    self.send_response(302)
                    self.send_header('Location', '/login')
                    self.end_headers()
        
        elif self.path == '/cad_atividade':           
                 
            content_length = int(self.headers['content-Length'])

            body = self.rfile.read(content_length).decode('utf-8')
          
            form_data = parse_qs(body)
 
            disciplina = form_data.get('disciplina', [''])[0]
            descricao = form_data.get('descricao', [''])[0]
           
            if self.usuario_existente(disciplina, descricao):
                with open(os.path.join(os.getcwd(), 'cadastro_atividade.html'), 'r', encoding='utf-8') as existe:
                    content_file = existe.read()
                mensagem = f"Atividade já cadastrada. Tente novamente!"
                content = content_file.replace('<!-- Mensagem de autenticacao será inserida aqui -->',
                                      f'<p>{mensagem}</p>')

                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
            
                self.wfile.write(content.encode('utf-8'))
           
            else:

                if any(line.startswith(f"{disciplina};") for line in open("dados_atividade.txt", "r", encoding="UTF-8")):
                    self.send_response(302)
                    self.send_header('Location', '/atividade_failed')
                    self.end_headers()
                    return 
               
                else:
                    self.adicionar_atividade(disciplina,descricao)
                    self.send_response(302)
                    self.send_header('Location', '/login')
                    self.end_headers()
               
        else:
            super(MyMandler,self).do_POST()

# Criação do Servidor

endereco_ip = "0.0.0.0"
porta = 8000
 

with socketserver.TCPServer((endereco_ip, porta), MyMandler) as httpd:
    print(f"Servidor iniciando em {endereco_ip}:{porta}")
    httpd.serve_forever()
 