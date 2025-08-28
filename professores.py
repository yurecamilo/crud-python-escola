from prettytable import PrettyTable
import mysql.connector
def abrebanco():
    try:
        global conexao
        conexao = mysql.connector.Connect(host='127.0.0.1',port = 3307, database='univap',
        user='root', password='')
        #Na escola remover port = 3307
        if conexao.is_connected():
            informacaobanco = conexao.server_info
            print(f'Conectado ao servidor banco de dados - Versão {informacaobanco}')
            print('Conexão ok')
            global comandosql
            comandosql = conexao.cursor()
            comandosql.execute('select database();')
            nomebanco = comandosql.fetchone()
            print(f'Banco de dados acessado = {nomebanco}')
            print('='*80)
            return 1
        else:
            print("Conexão não realizada com banco")
        return 0
    except Exception as erro:
        print(f'Ocorreu erro ao tentar abrir o banco de dados: Erro===>>> {erro}')
    return 0

def mostratodos():
    grid = PrettyTable(['Registro do Professor', "Nome do Professor", "Telefone do Professor", "Idade do Professor", "Salário do Professor",])
    try:
        comandosql = conexao.cursor()
        comandosql.execute(f'select * from professores;')
        tabela = comandosql.fetchall()
        if comandosql.rowcount > 0:
            for registro in tabela:
                grid.add_row([registro[0], registro[1], registro[2], registro[3], registro[4]])
            print(grid)
        else:
            print('Não existem professores cadastrados!!!')
    except Exception as erro:
        print(f'Ocorreu erro: {erro}')

def consultarprofessor(rp=0):
    try:
        comandosql = conexao.cursor()
        comandosql.execute(f'select * from professores where registro = {rp};')
        tabela = comandosql.fetchall()
        if comandosql.rowcount > 0:
            for registro in tabela:
                print(f'Nome do Professor: {registro[1]}, Telefone do Professor: {registro[2]}, Idade do Professor: {registro[3]}, Salário do Professor: {registro[4]}')
                return 'c'
        else:
            return 'nc'
    except Exception as erro:
        print(f'Ocorreu erro ao tentar consultar esta disciplina: Erro===>>> {erro}')

def cadastrarprofessor(rp = 0, np = '', tfp = '', ip = 0, sp = 0):
    try:
        comandosql = conexao.cursor()
        comandosql.execute(f'insert into professores(registro, nomeprof, telefoneprof, idadeprof, salarioprof) values({rp}, "{np}", "{tfp}", {ip}, {sp});')
        conexao.commit()
        return 'Professor cadastrado com sucesso !!!'
    except Exception as erro:
        print(f'Ocorreu erro ao tentar cadastrar este professor: Erro===>>> {erro}')
        return 'Não foi possível cadastrar este professor !!!'

def atualizarprofessor(rp = 0, np = '', tfp = '', ip = 0, sp = 0):
    try:
        comandosql = conexao.cursor()
        comandosql.execute(f'update professores set nomeprof = "{np}", telefoneprof = "{tfp}", idadeprof = {ip}, salarioprof = {sp} where registro = {rp};')
        conexao.commit()
        return 'Professor atualizado com sucesso !!!'
    except Exception as erro:
        print(f'Ocorreu erro ao tentar atualizar este professor: Erro===>>> {erro}')
        return 'Não foi possível atualizar este professor !!!'

def excluirprofessor(rp=0):
    try:
        comandosql = conexao.cursor()
        comandosql.execute(f'SELECT * FROM disciplinasxprofessores WHERE codprofessor = {rp};')
        resultados = comandosql.fetchall()  # consome todos os resultados
        if len(resultados) > 0:
            return 'Não foi possível excluir este professor pois já existe uma disciplina associada a ele!!!'
        else:
            comandosql.execute(f'DELETE FROM professores WHERE registro = {rp};')
            conexao.commit()
            return 'Professor excluído com sucesso !!!'
    except Exception as erro:
        print(f'Ocorreu erro ao tentar excluir este professor: Erro===>>> {erro}')
        return 'Não foi possível excluir este professor !!!'

if abrebanco() == 1:
    resp = input('Deseja entrar no módulo de professores? (1-sim ou qualquer tecla para sair): ')
    while resp == '1':
        print('=' * 80)
        print('{:^80}'.format('SISTEMA UNIVAP - PROFESSORES'))
        print('=' * 80)
        while True:
            codigoprof = input('Digite o código do professor (0 - mostra todos): ')
            if codigoprof.isnumeric():
                codigoprof = int(codigoprof)
                break
        if codigoprof == 0:
            mostratodos()
            continue

        if consultarprofessor(codigoprof) == 'nc':

            nomeprof = input('Digite o nome do professor: ')
            while len(nomeprof) < 0 or not nomeprof.isalpha():
                nomeprof = input('ERRO !!! Nome do professor deve ter pelo menos 1 caractere e não pode conter números. Digite novamente: ')

            telefoneprof = input('Digite o telefone do professor: ')
            while len(telefoneprof) < 0 or not telefoneprof.isnumeric():
                telefoneprof = input('ERRO !!! Telefone do professor deve ter pelo menos 1 caractere e não pode conter letras. Digite novamente: ')

            idadeprof = int(input('Digite a idade do professor: '))
            while idadeprof < 0 or idadeprof >= 150:
                idadeprof = int(input('ERRO !!! Idade do professor deve ser maior que 0 e menor que 150. Digite novamente: '))

            salarioprof = float(input('Digite o salário do professor: '))
            while salarioprof < 0:
                salarioprof = float(input('ERRO !!! Salário do professor deve ser maior que 0. Digite novamente: '))

            msg = cadastrarprofessor(codigoprof, nomeprof, telefoneprof, idadeprof, salarioprof)
            print(msg)
        else:
            op = input("Escolha: [A]-Alterar [E]-Excluir [C]-Cancelar Operações ==> ")
            while op != 'A' and op != 'E' and op != 'C':
                op = input("ERRO !!! Escolha CORRETAMENTE : [A]-Alterar [E]-Excluir [C]- Cancelar Operações ==> ")
            if op == 'A':
                print('Atenção: Código do professor não pode ser alterado!!!')

                nomeprof = input('Digite o nome do professor: ')
                while len(nomeprof) < 0 or not nomeprof.isalpha():
                    nomeprof = input(
                        'ERRO !!! Nome do professor deve ter pelo menos 1 caractere e não pode conter números. Digite novamente: ')

                telefoneprof = input('Digite o telefone do professor: ')
                while len(telefoneprof) < 0 or not telefoneprof.isnumeric():
                    telefoneprof = input(
                        'ERRO !!! Telefone do professor deve ter pelo menos 1 caractere e não pode conter letras. Digite novamente: ')

                idadeprof = int(input('Digite a idade do professor: '))
                while idadeprof < 0 or idadeprof >= 150:
                    idadeprof = int(
                        input('ERRO !!! Idade do professor deve ser maior que 0 e menor que 150. Digite novamente: '))

                salarioprof = float(input('Digite o salário do professor: '))
                while salarioprof < 0:
                    salarioprof = float(input('ERRO !!! Salário do professor deve ser maior que 0. Digite novamente: '))

                msg = atualizarprofessor(codigoprof, nomeprof, telefoneprof, idadeprof, salarioprof)
                print(msg)
            elif op == 'E':
                confirma = input('ATENÇÃO !!!! TEM CERTEZA, CONFIRMA EXCLUSÃO? S-SIM OU N-NÃO: ')
                while confirma != 'S' and confirma != 'N':
                    confirma = input('RESPOSTA INEXISTENTE !!!! TEM CERTEZA, CONFIRMA EXCLUSÃO? S-SIM OU N-NÃO: ')
                msg = excluirprofessor(codigoprof)
                print(msg)
        print('\n\n')
        print('=' * 80)
        if input('Deseja continuar usando o programa? 1- Sim OU qualquer tecla para sair: ') == '1':

            # o COMANDO CONTIUE ABAIXO, RETORNA PARA O WHILE QUE ESTÁ SENDO EXECUTADO
            continue
        else:
            break
        comandosql.close()
        conexao.close()
else:
    print('FIM DO PROGRAMA!!! Algum problema existente na conexão com banco de dados.')





