import socket as sock
import threading

#------- lista do q falta --------
#enviar mensagem pra todos os clitens OK
#criar sistema de mensagem particular OK
#criar sistema de kick do chat
#cliente listar usuários online OK
#notificar ao cliente quando alguem entra OK
#notificar ao cliente quando alguem sai OK
#lista de comandos cliente OK
#lista de comandos servidor OK
#toggle do chat servidor OK



clientes = [] #lista de informações dos clientes online
clientes_online = [] #lista de nomes dos clientes online
comandos = '----- COMANDOS DO CLIENTE -----\n\n/pv - mensagens particulares\n Exemplo: /pv "nome" "mensagem"\n\n/lista - lista de usuários online'
comandos_serv = '----- COMANDOS DO SERVIDOR -----\n\n/cmd - comandos do servidor\n /chat - alternar visão do chat'
chat = False #variável para visualização do chat pelo servidor, valor padrão "False", para não ver oq está sendo enviado








def serv(): #função para entrada de dados de texto do servidor
    global chat #chamar variável "chat" para utilização na alternância de visão do chat
    while True:
        try:
            serv_cmd = input('') #input de texto do servidor
            if serv_cmd == '/cmd': #se for digitado "/cmd", vai aparecer a lista de comandos
                try:
                    print(comandos_serv)
                except:
                    return
                
            elif serv_cmd == '/chat': #se for digitado "/chat", vai alternar entre ver e esconder o que está sendo enviado pelos clientes
                chat = not chat #valor padrão é alterado, para poder ver oq está sendo enviado


            #FINALIZAR FUNÇÃO KICK
            elif serv_cmd.startswith('/kick '):
                partes_cmd = serv_cmd.split(' ', 2) #separa a mensagem em duas partes, usando o espaço como separação
                nome_kickado = partes_cmd[1].strip('"')  #nome de quem vai ser kickado, retira as aspas do texto transformando a escrita de quem vai receber em uma variavel pra lista
                motivo = partes_cmd[2]  #motivo do kick
                kick(nome_kickado, motivo)
                

        
        except:
            return


def kick(nome_kick, motivo):
    global clientes
    for nome, cliente_socket in clientes: #percorre toda a lista de clientes
            if nome == nome_kick: #se o nome da lista for igual ao nome do destinatario
                try:
                    cliente_socket.sendall(f'Você foi kickado >> Motivo: {motivo}'.encode()) #envia a mensagem privada ao destinatário
                    cliente_socket.shutdown(sock.SHUT_RDWR)
                    cliente_socket.close()
                    print(f'{nome_kick} foi kickado')
                except:
                    print('erro') #senão da erro




def notificacao_login(nome, socket): #função para notificar os clientes online quando alguem entra
        notif_login = f'Cliente conectado: {nome}' #formato da mensagem
        for nome, cliente in clientes: #loop para enviar para todos os clientes
            try: #try para tratamento de dados, e não ocorrer o erro de só um poder mandar mensagem por vez
                cliente.sendall(notif_login.encode()) #enviar a mensagem
            except: #else obrigatório do try, para erros
                return


def notificacao_logout(nome, socket): #função para notificar os clientes online quando alguem sai
        notif_logout = f'Cliente desconectado: {nome}' #formato da mensagem
        for nome, cliente in clientes: #loop para enviar para todos os clientes
            try: #try para tratamento de dados, e não ocorrer o erro de só um poder mandar mensagem por vez
                cliente.sendall(notif_logout.encode()) #enviar a mensagem
            except: #else obrigatório do try, para erros
                return
            

def lista_online(socket):
    clon = '\n- '.join(clientes_online)
    clienteson = f'Clientes online:\n- {clon}'
    try: #try para tratamento de dados, e não ocorrer o erro de só um poder mandar mensagem por vez
        socket.sendall(clienteson.encode()) #enviar a mensagem
    except: #else obrigatório do try, para erros
        return
    

def lista_cmd(socket):
    cmd = comandos
    try: #try para tratamento de dados, e não ocorrer o erro de só um poder mandar mensagem por vez
        socket.sendall(cmd.encode()) #enviar a mensagem
    except: #else obrigatório do try, para erros
        return


def receber_dados(cliente, endereco): #função para receber todos os dados vindo do cliente  
    nome = cliente.recv(50).decode() #Receber o nome antes de entrar no loop
    clientes_online.append(nome) #adicionar nome à lista de clientes online
    clienteid = (nome, cliente) #modelo de como os dados dos clientes serão inseridos
    clientes.append(clienteid) #adicionar dados do cliente numa lista para uso de funções
    print(f'clientes online : {clientes_online}') #printar clientes online
    print(f'Conexão com sucesso com {nome} : {endereco}') #printar o nome e o ip do cliente q conectou
    if len(clientes_online) != 0: #se tiver alguem online no chat, chamar função de notificação de login
        notificacao_login(nome, cliente)


    def broad(nome, socket, mensagem): #função para todos os clientes receberem as mensagens
        for nome, cliente in clientes: #loop para enviar para todos
            if cliente != socket: #if para o cliente q enviou a mensagem não receber ela de volta
                try: #try para tratamento de dados, e não ocorrer o erro de só um poder mandar mensagem por vez
                    cliente.sendall(mensagem.encode()) #enviar a mensagem
                except: #else obrigatório do try, para erros
                    print(f'Erro ao enviar mensagem para {cliente}.') #erro

    def mensagem_privada(nome_destino, mensagem, remetente): #função para mensagem privada
        for nome, cliente in clientes: #percorre toda a lista de clientes
            if nome == nome_destino: #se o nome da lista for igual ao nome do destinatario
                try:
                    cliente.sendall(f'[PV de {remetente}] >> {mensagem}'.encode()) #envia a mensagem privada ao destinatário
                    if chat == True:
                        try:
                            print(f'PV de <{remetente}> para <{nome_destino}> >> {mensagem}')
                        except:
                            return
                except:
                    print('erro') #senão da erro

    while True:
        try:
            mensagem = cliente.recv(1024).decode() #receber mensagem do cliente
            if mensagem.startswith('/pv '): #mesagem pv se começar com /pv
                partes = mensagem.split(' ', 2) #separa a mensagem em duas partes, usando o espaço como separação
                nome_destino = partes[1].strip('"')  #nome de quem vai receber, retira as aspas do texto transformando a escrita de quem vai receber em uma variavel pra lista
                mensagem_pv = partes[2]  #mensagem
                mensagem_privada(nome_destino, mensagem_pv, nome) #chama a função de pv


            elif mensagem == '/lista':
                lista_online(cliente)

            elif mensagem == '/cmd':
                lista_cmd(cliente)

            else: #mensagem pra todo mundo
                mensage_text = f'{nome} >> {mensagem}' #formato da mensagem
                broad(nome, cliente, mensage_text) #chama função pra enviar mensagem pra todo mundo
                if chat == True:
                    try:
                        print(mensage_text) #printa a mensagem pro servidor
                    except:
                        return
        except: #desconectar para caso de erro
            print(f'{nome} se desconectou')
            if len(clientes_online) != 0: #se tiver alguem online no chat, chamar função de notificação de login
                notificacao_logout(nome, cliente)
            clientes.remove((nome, cliente))
            clientes_online.remove(nome)
            cliente.close()
            print(f'clientes online : {clientes_online}')
            return
        


        
    

HOST = '26.193.67.37' #Endereço IP do servidor
PORTA = 9999

#Criamos o socket do servidor
socket_server = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
#Fazemos o BIND
socket_server.bind((HOST,PORTA))
#Entramos no modo escuta (LISTEN)
socket_server.listen()
print(f"O servidor {HOST}:{PORTA} está aguardando conexões...")
#Loop principal para recebimento de clientes

thread_serv = threading.Thread(target=serv, args=[])
thread_serv.start()


while True:
    cliente, ender = socket_server.accept()
    #Nesse ponto temos uma conexão com um cliente
    #Vamos fazer um loop para recebimento de dados
    #Agora vamos criar Threads para os loops
    thread_cliente = threading.Thread(target=receber_dados, args=[cliente, ender])
    thread_cliente.start()

