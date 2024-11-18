import socket as sock
import threading

HOST = '26.193.67.37' #IP DO SERVIDOR
PORTA = 9999 #PORTA DO SERVIDOR

#criamos o socket do cliente
cliente = sock.socket(sock.AF_INET, sock.SOCK_STREAM)

exec = True

def msg():
    while True:
        try:
            mensagem = input('')
            #encode: faz a conversão str->bytes
            cliente.sendall(mensagem.encode())
        except:
            break
    

def chat(cliente):
    global exec
    while True:
        try:
            mensagem_recebida = cliente.recv(1024).decode()
            if mensagem_recebida.startswith("Você foi kickado"):  # Verifica se é mensagem de kick
                print(mensagem_recebida)  # Mostra o motivo do kick
                exec = False
                cliente.close()  # Fecha o socket
                break
            print(mensagem_recebida)
        except:
            print("Conexão com o servidor perdida.")
            cliente.close()
            break

def notificacao_login(cliente):
    while True:
        try:
            if exec == True:
                notif_login = cliente.recv(1024).decode()
                print(notif_login)
            else:
                break
        except:
            print('oi')

def notificacao_logout(cliente):
    while True:
        try:
            if exec == True:
                notif_logout = cliente.recv(1024).decode()
                print(notif_logout)
            else:
                break
        except:
            print('erro')
            

def lista_online(cliente):
    while True:
        try:
            if exec == True:
                clienteson = cliente.recv(1024).decode()
                print(clienteson)
            else:
                break
        except:
            print('erro')


def lista_cmd(cliente):
    while True:
        try:
            if exec == True:
                cmd = cliente.recv(1024).decode()
                print(cmd)
            else:
                break
        except:
            print('erro')


#Solicita conexão ao servidor (HOST,PORTA)
cliente.connect((HOST,PORTA))
#Criamos um loop para envio de dados
print(5*"*" + "INICIANDO CHAT" + 5*"*")
print('Digite "/cmd" para ver os comandos disponíveis')
nome = input("Informe seu nome para entrar no chat:\n")
#Antes de entrar no loop enviamos o nome
cliente.sendall(nome.encode())

thread_mensagem = threading.Thread(target=msg, args=[])
thread_mensagem.start()

thread_chat = threading.Thread(target=chat, args=[cliente])
thread_chat.start()

thread_notificacaologin = threading.Thread(target=notificacao_login, args=[cliente])
thread_notificacaologin.start()

thread_notificacaologout = threading.Thread(target=notificacao_logout, args=[cliente])
thread_notificacaologout.start()

thread_listaonline = threading.Thread(target=lista_online, args=[cliente])
thread_listaonline.start()

thread_listacmd = threading.Thread(target=lista_cmd, args=[cliente])
thread_listacmd.start()