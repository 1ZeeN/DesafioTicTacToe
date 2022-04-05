from flask import Flask, Response, jsonify, request
import re

def tela(): 
    global jogo
    board = []
    for i in range(3):
        linha = []
        # Coverte 0, 1, -1 para as formas do jogo.
        for j in range(3):
            if quadro[i][j] == 0:
                x = " - "
            elif quadro[i][j] == 1:
                x = " X "
            elif quadro[i][j] == -1:
                x = " O "
            linha.append(x)
        # Cria a tabela com base nas formas X, 0, -.
        board.append(linha)
    jogo = "Jogo da Velha"
    for i in range(3):
        jogo = jogo + "\n"
        for j in range(3):
            jogo = jogo + (f" {board[i][j]}") + "\t"
    return print(jogo)

def checkwin():
    '''
    Condição de Vitória com base no variavel quadro, realiza-se a soma pra verificar qual estágio do jogo está:
    Andamento, Encerrado ou Vitoria X/O!
    '''
    global winner,run
    for i in range(3): #checagem de Linha
        soma = quadro[i][0]+quadro[i][1]+quadro[i][2]
        if soma == 3:
            winner = 'X'
            run = False
            return jsonify({'status':'OK','jogadas':jogadas,'message':f'O vencedor foi o {winner}!'})
        elif soma == -3:
            winner = 'O'
            run = False
            return jsonify({'status':'OK','jogadas':jogadas,'message':f'O vencedor foi o {winner}!'})
        

    for i in range(3): #checagem de coluna
        soma = quadro[0][i]+quadro[1][i]+quadro[2][i]
        if soma == 3:
            winner = 'X'
            run = False
            return jsonify({'status':'OK','jogadas':jogadas,'message':f'O vencedor foi o {winner}!'})
        elif soma == -3:
            winner = 'O'
            run = False
            return jsonify({'status':'OK','jogadas':jogadas,'message':f'O vencedor foi o {winner}!'})

    d1 = quadro[0][0]+quadro[1][1]+quadro[2][2] #checagem de diagonais
    d2 = quadro[0][2]+quadro[1][1]+quadro[2][0]
    if d1 == 3 or  d2 == 3:
        winner = 'X'
        run = False
        return jsonify({'status':'OK','jogadas':jogadas,'message':f'O vencedor foi o {winner}!'})
    
    elif d2 == -3 or d1 == -3:
        winner = 'O'
        run = False
        return jsonify({'status':'OK','jogadas':jogadas,'message':f'O vencedor foi o {winner}!'})

    if winner == None: # Jogo em andamento
        if any(0 in sublist for sublist in quadro): # Verifica se alguma posição não foi preenchida.
            run = True
            return jsonify({'status':'OK','jogadas':jogadas,'message':'Jogo em Andamento'})

        else:
            run = False # Encerra o jogo
            return jsonify({'status':'OK','jogadas':jogadas,'message':'Jogo Empatado'})

def game(pos, player):
    '''
    Faz a verificação do input dado pela função jogada(), caso esteja tudo certo a jogada é realizada!
    '''
    global index, y, run
    try: #validação dos inputs: se respeitam as regras do jogo.
        if len(pos) != 3 or (pos[0] != 'P') or re.match(r"([^OX])",player):
            raise Exception()
        coluna = int(pos[2])
        linha = int(pos[1])
        if (linha > 3 or coluna > 3 or linha < 1 or coluna < 1):
            raise Exception
    except:
        return jsonify({'status':'ERROR','jogada':pos,'jogador':player,'message':'Jogada Invalida: Posição invalida!'}),400

    checkwin() #Chama a função para saber se o jogo está encerrado ou não.
    if (run == False):
        return jsonify({'status':'ERROR','jogada':pos,'jogador':player,'message':'Jogada Invalida: Jogo encerrado!'}),400
    else:
        if player == 'X': #Conversão da variavel jogador para 1, -1. Utilizado na soma para a condição da vitória.
            y = 1
        elif player == 'O':
            y = -1
        else:
            return jsonify({'status':'ERROR','jogada':pos,'jogador':player,'message':'Jogada Invalida: Sem Jogador Definido'}),400

        if quadro[linha-1][coluna-1] == 0: #Preenchimento da variavel QUADRO com base na posição dada pelo usuário.
            quadro[linha-1][coluna-1] = y
            jogadas.append(f"{pos} => {player}") #Salva a posição e o jogador para exibir em status().
            tela()
            return jsonify({'status':'OK','jogada':pos,'jogador':player,'message':'Movimento executado!'})
        else:
            return jsonify({'status':'ERROR','jogada':pos,'jogador':player,'message':'Jogada Invalida: Posição já preenchida'}),400

app = Flask(__name__)

index = 1
jogadas = []
stats = x = z = jogo = ""
run = True
winner = None
quadro = [[0, 0, 0],
          [0, 0, 0],
          [0, 0, 0]]


@app.route("/jogada", methods=['POST'])
# Request da posição e jogador.
def jogada():
    if ("pos" not in request.form) or ("player" not in request.form):
        return jsonify({'status':'ERROR','message':'Parametro Invalido!'}),400
    else:   
        pos = request.form.get('pos').upper()
        player = request.form.get('player').upper()
        retorno = game(pos, player)
        return retorno


@app.route("/status")
# Exibe o estado que o jogo se encontra.
def status():
    tela()
    return checkwin()

@app.route("/reiniciar")
# Limpa todas as variaveis pra reiniciar o jogo.
def reiniciar():
    global index, jogadas, stats, x , z, jogo, run, winner , quadro
    index = 1
    jogadas = []
    stats = x = z = jogo = ""
    run = True
    winner = None
    quadro = [[0, 0, 0],[0, 0, 0],[0, 0, 0]]
    return jsonify({'status':'OK','jogadas':jogadas,'message':'Jogo Reiniciado'})


app.run(host="0.0.0.0",port=80)
