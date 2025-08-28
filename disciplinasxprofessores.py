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

def mostradisciplinas():
    grid = PrettyTable(['Código da Disciplina', 'Nome da Disciplina'])
    try:
        comandosql = conexao.cursor()
        comandosql.execute(f'select * from disciplinas;')
        tabela = comandosql.fetchall()
        if comandosql.rowcount > 0:
            for registro in tabela:
                grid.add_row([registro[0], registro[1]])
            print (grid)
        else:
            print('Não existem disciplinas cadastradas!!!')
    except Exception as erro:
        print(f'Ocorreu erro: {erro}')


def mostraprofessores():
    grid = PrettyTable(['Código do Professor', 'Nome do Professor'])
    try:
        comandosql = conexao.cursor()
        comandosql.execute(f'select * from professores;')
        tabela = comandosql.fetchall()
        if comandosql.rowcount > 0:
            for registro in tabela:
                grid.add_row([registro[0], registro[1]])
            print (grid)
        else:
            print('Não existem professores cadastrados!!!')
    except Exception as erro:
        print(f'Ocorreu erro: {erro}')

def mostradisciplinasxprofessores():
    grid = PrettyTable(['Código da Disciplina no Curso', 'Código da Disciplina', 'Código do Professor', 'Curso', 'Carga horária', 'Ano letivo'])
    try:
        comandosql = conexao.cursor()
        comandosql.execute(f'select * from disciplinasxprofessores;')
        tabela = comandosql.fetchall()
        if comandosql.rowcount > 0:
            for registro in tabela:
                grid.add_row([registro[0], registro[1], registro[2], registro[3], registro[4], registro[5]])
            print (grid)
        else:
            print('Não existem dados cadastrados!!!')
    except Exception as erro:
        print(f'Ocorreu erro: {erro}')

def consultardisciplinaxprofessor(cdc=0):
    try:
        comandosql = conexao.cursor()
        comandosql.execute(f'select * from disciplinasxprofessores where codigodisciplinacurso = {cdc};')
        tabela = comandosql.fetchall()
        if comandosql.rowcount > 0:
            for registro in tabela:
                print (f'Código da Disciplina no Curso: {registro[0]} , Código da Disciplina: {registro[1]} , Código do Professor: {registro[2]} , Curso: {registro[3]} , Carga horária: {registro[4]} , Ano letivo: {registro[5]}')
                return 'c'
        else:
            return 'nc'
    except Exception as erro:
        print(f'Ocorreu erro: {erro}')

def atualizardisciplinaxprofessor(cdc=0, cd=0, cp=0, c=0, ch=0, al=0):
    try:
        comandosql = conexao.cursor()
        comandosql.execute(f'SELECT * FROM disciplinasxprofessores WHERE codigodisciplinacurso = {cdc}')
        if len(comandosql.fetchall()) == 0:
            return 'Registro não encontrado!'
        comandosql.execute(f'''
                            UPDATE disciplinasxprofessores
                            SET coddisciplina = {cd}, codprofessor = {cp}, curso = {c}, cargahoraria = {ch}, anoletivo = {al}
                            WHERE codigodisciplinacurso = {cdc};
                        ''')
        conexao.commit()
        return 'Disciplina atualizada com sucesso !!!'
    except Exception as erro:
        print(f'Ocorreu erro ao tentar atualizar esta disciplina: Erro===>>> {erro}')
        return 'Não foi possível atualizar esta disciplina !!!'


def verificar_disciplina_existe(codigo_disciplina):
    try:
        comandosql = conexao.cursor()
        comandosql.execute(f'SELECT codigodisc FROM disciplinas WHERE codigodisc = {codigo_disciplina};')
        resultado = comandosql.fetchone()
        if resultado:
            return True
        else:
            return False
    except Exception as erro:
        print(f'Erro ao verificar disciplina: {erro}')
        return False

def verificar_professor_existe(codigo_professor):
    try:
        comandosql = conexao.cursor()
        comandosql.execute(f'SELECT registro FROM professores WHERE registro = {codigo_professor};')
        resultado = comandosql.fetchone()
        if resultado:
            return True
        else:
            return False
    except Exception as erro:
        print(f'Erro ao verificar professor: {erro}')
        return False

def cadastrardisciplinaxprofessor(cdc=0, cd=0, cp=0, c=0, ch=0, al=0):
    try:
        # Verifica se a disciplina existe
        if not verificar_disciplina_existe(cd):
            return 'Erro: A disciplina informada não está cadastrada no sistema.'
            
        # Verifica se o professor existe
        if not verificar_professor_existe(cp):
            return 'Erro: O professor informado não está cadastrado no sistema.'
            
        comandosql = conexao.cursor()
        comandosql.execute(f'insert into disciplinasxprofessores(codigodisciplinacurso, coddisciplina, codprofessor, curso, cargahoraria, anoletivo) values ("{cdc}", {cd}, {cp}, {c}, {ch}, {al});')
        conexao.commit()
        return 'Disciplina cadastrada com sucesso!'
    except Exception as erro:
        print(f'Ocorreu erro ao tentar cadastrar esta disciplina: Erro===>>> {erro}')
        return 'Não foi possível cadastrar esta disciplina!'

def excluirdisciplinaxprofessor(cdc=0):
    try:
        comandosql = conexao.cursor()
        comandosql.execute(f'delete from disciplinasxprofessores where codigodisciplinacurso = {cdc};')
        conexao.commit()
        return 'Disciplina excluida com sucesso!'
    except Exception as erro:
        print(f'Ocorreu erro ao tentar excluir esta disciplina: Erro===>>> {erro}')
        return 'Não foi possível excluir esta disciplina!'

if abrebanco() == 1:
    print("\nMOSTRANDO TABELAS DE DISCIPLINAS E PROFESSORES PARA FACILITAR A CONSULTA\n")
    mostradisciplinas()
    mostraprofessores()
    resp = input("Deseja entrar no módulo de disciplinas x professores? (1- Sim ou qualquer tecla para sair): ")
    while resp == '1':
        print("="*80)
        print('{:^80}'.format('SISTEMA UNIVAP - DISCIPLINAS X PROFESSORES'))
        print('=' * 80)

        while True:
            codigodisciplinaxcurso = input('Digite o código da disciplina no curso (0 - mostrar todos): ')
            if codigodisciplinaxcurso.isnumeric():
                codigodisciplinaxcurso = int(codigodisciplinaxcurso)
                break
        if codigodisciplinaxcurso == 0:
            mostradisciplinasxprofessores()
            continue

        if consultardisciplinaxprofessor(codigodisciplinaxcurso) == 'nc':

            codigodisciplina = int(input('Digite o código da disciplina: '))
            while codigodisciplina <= 0:
                print("ERRO !!! Código da disciplina deve ser maior que zero!")
                codigodisciplina = int(input('Digite o código da disciplina: '))
            while not verificar_disciplina_existe(codigodisciplina):
                codigodisciplina = int(input('Erro: A disciplina informada não está cadastrada no sistema. Digite Novamente: '))

            codigoprofessor = int(input('Digite o código do professor: '))
            while codigoprofessor <= 0:
                print("ERRO !!! Código do professor deve ser maior que zero!")
            while not verificar_professor_existe(codigoprofessor):
                codigoprofessor = int(input('Erro: O professor informado não está cadastrado no sistema. Digite novamente: '))

            curso = int(input('Digite o curso: '))
            while curso <= 0:
                print("ERRO !!! Curso deve ser maior que zero!")
                curso = int(input('Digite o curso: '))

            cargahoraria = int(input('Digite a carga horária: '))
            while cargahoraria <= 0:
                print("ERRO !!! Carga horária deve ser maior que zero!")
                cargahoraria = int(input('Digite a carga horária: '))

            anoletivo = int(input('Digite o ano letivo: '))
            while anoletivo <= 0 or anoletivo < 2000:
                print("ERRO !!! Ano letivo deve ser maior que zero e maior que 2000!")
                anoletivo = int(input('Digite o ano letivo: '))

            msg = cadastrardisciplinaxprofessor(codigodisciplinaxcurso, codigodisciplina, codigoprofessor, curso, cargahoraria, anoletivo)
            print(msg)
        else:
            op = input("Escolha: [A]-Alterar [E]-Excluir [C]-Cancelar Operações ==> ")
            while op != 'A' and op != 'E' and op != 'C':
                op = input("ERRO !!! Escolha CORRETAMENTE : [A]-Alterar [E]-Excluir [C]- Cancelar Operações ==> ")
            if op == 'A':

                codigodisciplina = int(input('Digite o código da disciplina: '))
                while codigodisciplina <= 0:
                    print("ERRO !!! Código da disciplina deve ser maior que zero!")
                    codigodisciplina = int(input('Digite o código da disciplina: '))
                while not verificar_disciplina_existe(codigodisciplina):
                    codigodisciplina = int(input('Erro: A disciplina informada não está cadastrada no sistema. Digite novamente: '))


                codigoprofessor = int(input('Digite o código do professor: '))
                while codigoprofessor <= 0:
                    print("ERRO !!! Código do professor deve ser maior que zero!")
                while not verificar_professor_existe(codigoprofessor):
                    codigoprofessor= int(input('Erro: O professor informado não está cadastrado no sistema. Digite novamente:'))

                curso = int(input('Digite o curso: '))
                while curso <= 0:
                    print("ERRO !!! Curso deve ser maior que zero!")
                    curso = int(input('Digite o curso: '))

                cargahoraria = int(input('Digite a carga horária: '))
                while cargahoraria <= 0:
                    print("ERRO !!! Carga horária deve ser maior que zero!")
                    cargahoraria = int(input('Digite a carga horária: '))

                anoletivo = int(input('Digite o ano letivo: '))
                while anoletivo <= 0 or anoletivo < 2000:
                    print("ERRO !!! Ano letivo deve ser maior que zero e maior que 2000!")
                    anoletivo = int(input('Digite o ano letivo: '))

                msg = atualizardisciplinaxprofessor(codigodisciplinaxcurso, codigodisciplina, codigoprofessor, curso, cargahoraria, anoletivo)
                print(msg)
            elif op == 'E':
                confirma = input('ATENÇÃO !!!! TEM CERTEZA, CONFIRMA EXCLUSÃO? S-SIM OU N-NÃO: ')
                while confirma != 'S' and confirma != 'N':
                    confirma = input('RESPOSTA INEXISTENTE !!!! TEM CERTEZA, CONFIRMA EXCLUSÃO? S-SIM OU N-NÃO: ')
                msg = excluirdisciplinaxprofessor(codigodisciplinaxcurso)
                print(msg)
        print("\n\n")
        print("="*80)
        if input("Deseja continuar usando o programa? (1- Sim ou qualquer tecla para sair): ") == '1':
            continue
        else:
            break
            comandosql.close()
            conexao.close()
else:
    print('FIM DO PROGRAMA!!! Algum problema existente na conexão com banco de dados.')



