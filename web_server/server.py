'''from http.server import SimpleHTTPRequestHandler, HTTPServer

# definindo a porta
port = 8000

# definindo o gerenciador/manipulador de requisições
handler = SimpleHTTPRequestHandler

# criando a instancia do servidor
server = HTTPServer(("localhost", port), handler)

# imprimindo mensagem de ok
print(f"Server Running in http://localhost:{port}")

server.serve_forever()'''


import os
from http.server import SimpleHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
import json 

# classe para personalizar a resposta do servidor
class MyHandle(SimpleHTTPRequestHandler):
    # tenta abrir o arquivo index em vez da listagem de diretório padrão
    def list_directory(self, path):
        try:
            f = open(os.path.join(path, "index.html"), encoding="utf-8")
            # resposta HTTP
            self.send_response(200)
            # informa o tipo do conteúdo
            self.send_header("Content-type", "text/html")
            # finaliza o cabeçalho
            self.end_headers()
            # lê e envia o arquivo
            self.wfile.write(f.read().encode("utf-8"))
            # fecha o arquivo
            f.close()
            # evita executar o método padrão
            return None
        except FileNotFoundError:
            # se não encontrar o arquivo, executa a listagem de diretório padrão
            pass
        return super().list_directory(self, path)

    # valida o login
    def account_user(self, login, senha):
        # define login válido
        log = "ray@gmail.com"
        password = "1234"

        # valida o que foi passado no form
        if login == log and senha == password:
            return "Usuário logado"
        else:
            return "Usuário não existe"
    
    # sobrescreve o método GET para acessar URLs específicas
    def do_GET(self):
        # tenta abrir o login
        if self.path == "/login":
            try:
                with open(os.path.join(os.getcwd(), "login.html"), encoding="utf-8") as login:
                    content = login.read() # lê o conteúdo do arquivo
                # resposta HTTP
                self.send_response(200) 
                # informa o tipo do conteúdo
                self.send_header("Content-type", "text/html")
                # finaliza o cabeçalho
                self.end_headers()
                # lê e envia o arquivo
                self.wfile.write(content.encode("utf-8"))
            # se não encontrar o arquivo, retorna erro 404
            except FileNotFoundError:
                self.send_error(404, "File Not Found")

        # tenta abrir o cadastro    
        elif self.path == "/cadastro":
            try:
                with open(os.path.join(os.getcwd(), "cadastro.html"), encoding="utf-8") as cadastro:
                    content = cadastro.read() # lê o conteúdo do arquivo
                # resposta HTTP
                self.send_response(200) 
                # informa o tipo do conteúdo
                self.send_header("Content-type", "text/html")
                # finaliza o cabeçalho
                self.end_headers()
                # lê e envia o arquivo
                self.wfile.write(content.encode("utf-8"))
            # se não encontrar o arquivo, retorna erro 404
            except FileNotFoundError:
                self.send_error(404, "File Not Found")
        
        # tenta abrir a listagem
        elif self.path == "/listagem":
            try:
                with open(os.path.join(os.getcwd(), "lista_filmes.html"), encoding="utf-8") as listagem:
                    content = listagem.read() # lê o conteúdo do arquivo
                # resposta HTTP
                self.send_response(200) 
                # informa o tipo do conteúdo
                self.send_header("Content-type", "text/html")
                # finaliza o cabeçalho
                self.end_headers()
                # lê e envia o arquivo
                self.wfile.write(content.encode("utf-8"))
            # se não encontrar o arquivo, retorna erro 404
            except FileNotFoundError:
                self.send_error(404, "File Not Found")
        
        # para outras rotas, chama o método padrão da classe base        
        else:
            super().do_GET()

    # guardar valores enviados nos forms
    def do_POST(self):
        # form de login
        if self.path == '/send_login':
            # pega o tamanho do corpo da requisição
            content_length = int(self.headers['Content-length'])
            # transforma o corpo em um string com decodificação UTF-8 (legível)
            body = self.rfile.read(content_length).decode('utf-8')
            # converte a string em dicionario (chaves: nomes dos campos, valores: valores enviados para cada campo)
            form_data = parse_qs(body)

            # pega o que foi digitado nos inputs
            login = form_data.get('user', [""])[0]
            senha = form_data.get('password', [""])[0]

            # chama a validação
            logou = self.account_user(login, senha)

            # imprime dados passados nos inputs
            print("Data Form:")
            print("Usuario: ", login)        
            print("Senha: ", senha)    

            # resposta HTTP
            self.send_response(200)
            # informa o tipo do conteúdo
            self.send_header("Content-type", "text/html")
            # finaliza o cabeçalho
            self.end_headers()
            # escreve o resultado da validação no arquivo
            self.wfile.write(logou.encode("utf-8"))

        # form de cadastro de filmes
        elif self.path == '/send_cadastro':
            # pega o tamanho do corpo da requisição
            content_length = int(self.headers['Content-length'])
            # transforma o corpo em um string com decodificação UTF-8 (legível)
            body = self.rfile.read(content_length).decode('utf-8')
            # converte a string em dicionario (chaves: nomes dos campos, valores: valores enviados para cada campo)
            form_data = parse_qs(body)

            # pega o que foi digitado nos inputs
            nome = form_data.get('nome', [""])[0]
            atores = form_data.get('atores', [""])[0]
            diretor = form_data.get('diretor', [""])[0]
            ano = int(form_data.get('ano', ["0"])[0])
            generos = form_data.get('generos', []) # checkboxes
            produtora = form_data.get('produtora', [""])[0]
            sinopse = form_data.get('sinopse', [""])[0]
            capa = form_data.get('capa', [""])[0]

            # criar dicionário para guardar o filme cadastrado
            novo_filme = {
                "nome": nome,
                "atores": atores,
                "diretor": diretor,
                "ano": ano,
                "generos": generos,
                "produtora": produtora,
                "sinopse": sinopse,
                "capa": capa
            }

            # verificar se existe JSON dos filmes
            arquivo = "filmes.json"
            if os.path.exists(arquivo):
                with open(arquivo,  "r", encoding="utf-8") as lista:
                    # tentar carregar o arquivo
                    try:
                        filmes = json.load(lista)
                    except json.JSONDecodeError:
                        filmes = []
                        
                # adicionar o novo filme
                filmes.append(novo_filme)
                
                # salvar de volta no JSON
                with open(arquivo, "w", encoding="utf-8") as lista:
                    json.dumb(filmes, lista, indent=4, ensure_ascii=False)
                    # imprime dados passados nos inputs
                    print("Data Form:")
                    print("Filme: ", nome)        
                    print("Atores: ", atores)    
                    print("Diretor: ", diretor)        
                    print("Ano de lançamento: ", ano)    
                    print("Gêneros: ", generos)        
                    print("Produtora: ", produtora)    
                    print("Sinopse: ", sinopse)  
                    print("URL da capa: ", capa)
            
                    # resposta HTTP
                    self.send_response(200)
                    # informa o tipo do conteúdo
                    self.send_header("Content-type", "text/html")
                    # finaliza o cabeçalho
                    self.end_headers()
                    # escreve o resultado da validação no arquivo
                    self.wfile.write("Filme cadastrado com sucesso!".encode("utf-8"))
        
        # listagem de filmes           
        elif self.path=='/lista_filmes':
            # verifica se JSON existe
            arquivo = filmes.json
            if os.path.exists(arquivo):
                with open(arquivo, "r", encoding="utf-8") as lista:
                    # tenta carregar o arquivo 
                    try:
                        filmes = json.load(lista)
                    except json.JSONDecodeError:
                        filmes = []

                # gerar html para cada filme
                filmes_html = ""
                for filme in filmes:
                    filmes_html += "<article class='containerFilme>"
                    filmes_html += f"<img src='{filme[capa]} alt='Capa do filme'/>"
                    filmes_html += "<div class='infosFilme'>"
                    filmes_html += f"<h2>{filme[nome]}</h2>"
                    filmes_html += f"<p>Atores: {filme[atores]}</p>"
                    filmes_html += f"<p>Diretor: {filme[diretor]}</p>"
                    filmes_html += f"<p>Ano: {filme[ano]}</p>"
                    filmes_html += f"<p>Gêneros: {','.join(filme[generos])}</p>"
                    filmes_html += f"<p>Produtora: {filme[produtora]}</p>"
                    filmes_html += "</div>"
                    filmes_html += "<p>Sinopse:</p>"
                    filmes_html += f"<p>{filmes[sinopse]}</p>"
                    filmes_html += "</article>"

                # ler o arquivo html
                with open("lista_filmes.html", "r", encoding="utf-8") as template:
                    html = template.read()

                # subistituir a marca dos filmes pelo conteúdo
                html = html.replace("<!-- Exibir filmes dinâmicamente aqui -->", filmes_html)

                # resposta HTTP
                self.send_response(200)
                # informa o tipo do conteúdo
                self.send_header("Content-type", "text/html")
                # finaliza o cabeçalho
                self.end_headers()
                # escreve o resultado da validação no arquivo
                self.wfile.write(html.encode("utf-8"))
        
        # chama o método padrão da classe base   
        else:
            super(MyHandle, self).do_POST()
            

# função principal para iniciar o servidor  
def main():
    server_adress = ("", 8000)  # define endereço e porta do servidor
    httpd = HTTPServer(server_adress, MyHandle)  # cria o servidor HTTP usando a classe MyHandle
    print("Server Running in http://localhost:8000")  # exibe mensagem informando que o servidor está rodando
    httpd.serve_forever()  # inicia o servidor e mantém rodando
    

main()