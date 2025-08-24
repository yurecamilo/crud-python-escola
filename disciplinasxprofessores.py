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

def mostratoadas():
    grid = PrettyTable(['Código da Disciplina X Professor', 'Código da Disciplina', 'Código do Professor', 'Curso', 'Carga horária', 'Ano letivo'])
    try:
        comandosql = conexao.cursor()
        comandosql.execute(f'select * from disciplinasxprofessores;')
        tabela = comandosql.fetchall()
        if comandosql.rowcount > 0:
            for registro in tabela:
                grid.add_row([registro[0], registro[1], registro[2], registro[3], registro[4], registro[5]])
            print (grid)
        else:
            print('Não existem disciplinas cadastradas!!!')
    except Exception as erro:
        print(f'Ocorreu erro: {erro}')

