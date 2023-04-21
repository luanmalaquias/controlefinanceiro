import secrets
import string
import re


def generatePassword(safety: int) -> str:
    """Retorna uma senha gerada automaticamente de acordo com o nível de segurança"""

    alphabet = string.ascii_letters + string.digits

    if safety <= 1:
        for tentativa in range(500):
            password = ''
            for _ in range(4):
                choice = secrets.choice(alphabet)
                password += choice + choice
            if safety == 0:
                if verifyPasswordIntergity(password, upper=False):
                    break
            elif safety == 1:
                if verifyPasswordIntergity(password):
                    break

    elif safety == 2:
        password = ''
        for tentativa in range(500):
            alphabet = string.ascii_letters + string.digits
            password = ''.join(secrets.choice(alphabet) for i in range(8))
            if verifyPasswordIntergity(password):
                break
            

    return password

def verifyPasswordIntergity(password: str, numeric=True, lower=True, upper=True) -> bool:
    """Verifica se a senha contém numeros e caracteres em lower case"""
    passwordIntergity = False

    passwordNumeric = False
    passwordLower = False
    passwordUpper = False

    for letter in password:
        if letter.isnumeric():
            passwordNumeric = True if not passwordNumeric else True
        if letter.islower():
            passwordLower = True if not passwordLower else True
        if letter.isupper():
            passwordUpper = True if not passwordUpper else True

    if passwordNumeric == numeric and passwordLower == lower and passwordUpper == upper:
        passwordIntergity = True

    return passwordIntergity

def unmask(target) -> str:
    """Remove todos os caracteres especiais"""
    return re.sub(r'[^a-zA-Z0-9]', '', str(target))

def unmaskMoney(target: str) -> int:
    """Retira a máscara money \nEx: 1.234,99 -> 1234"""
    if target == '':
        return 0
    if ',' in target:
        target = target.split(',')[0]
    target = unmask(target)
    return int(target)

def gerarDados(quantidade:int) -> None:
    from django.contrib.auth.models import User
    from usuario.models import Perfil
    from imobiliaria.models import Imovel
    from pagamento.models import Pagamento
    from notificacao.models import Notificacao
    from random import randint
    from datetime import datetime

    # limpar banco
    User.objects.all().filter(is_staff=False).delete()
    Imovel.objects.all().delete()
    Pagamento.objects.all().delete()
    Notificacao.objects.all().delete()

    nomes = ["Miguel","Arthur","Gael","Théo","Heitor","Ravi","Davi","Bernardo","Noah","Gabriel","Helena","Alice","Laura","Maria Alice","Sophia","Manuela","Maitê","Liz","Cecília","Isabella"]
    sobrenomes = ['Silva','Santos','Oliveira','Sousa','Rodrigues','Ferreira','Alves','Pereira','Lima','Gomes','Costa','Ribeiro','Martins','Carvalho','Almeira','Lopes','Soares','Fernandes','Vieira','Barbosa','Rocha','Dias','Nascimento','Andrade','Moreira','Nunes','Marques','Machado','Mendes','Freitas','Cardoso','Ramos','Gonçalves','Santana','Teixeira']

    for x in range(quantidade):
        username = [str(randint(0, 9)) for i in range(11)]
        usuario = User.objects.create_user(username="".join(username), password="senhausuario!@")

        imovel = Imovel.objects.create()
        imovel.nome = f'imovel teste {x}'
        imovel.cep = "".join([str(randint(0, 9)) for i in range(7)])
        imovel.endereco = f'endereco teste {x}'
        imovel.numero = f'{randint(0,100)}'
        imovel.bairro = f'bairro teste {x}'
        imovel.cidade = f'cidade teste {x}'
        imovel.uf = "".join([secrets.choice(string.ascii_uppercase) for i in range(2)])
        imovel.mensalidade = f'{randint(500, 1000)}'
        imovel.disponivel = False

        perfil = Perfil.objects.create(usuario = usuario)
        perfil.cpf = usuario.username
        perfil.nome_completo = f'{secrets.choice(nomes)} {secrets.choice(sobrenomes)}'
        perfil.telefone = "".join([str(randint(0, 9)) for i in range(11)])
        perfil.imovel = imovel

        pagamento = Pagamento.objects.create(perfil = perfil, data = datetime.now())
        pagamento.status = "P"
        pagamento.valor = imovel.mensalidade

        usuario.save()
        imovel.save()
        perfil.save()
        pagamento.save()

def porcentagem(opcao: int, valor: float|int, porcentagem: float|int) -> float:
    """Calculo de porcentagem
    1: aumentar porcentagem em cima de um valor
    """
    if type(valor) != float or type(valor) != int:
        valor = float(valor)

    if opcao == 1:
        valor += valor*(porcentagem/100)
        return valor

def cpfIsValid(cpf: str|int) -> bool:
    """Verifica se o CPF é valido"""
    if type(cpf) == int:
        cpf = str(cpf)

    cpf = unmask(cpf)

    if len(cpf) != 11:
        return False
    
    primeiros9 = cpf[:9]
    verificadores = cpf[9:]
    
    def _calcPrimeiroDigito(primeiros9):
        result = 0
        primeiros9Invert = primeiros9[::-1]
        for index,number in enumerate(primeiros9Invert):
            result += (index+2) * int(number)
    
        resto = result % 11
        if resto < 2:
            primeiroDigito = 0
        else:
            primeiroDigito = 11 - resto
        
        return primeiroDigito
    
    def _calcSegundoDigito(primeiros9, primeiroDigito):
        result = 0
        primeiros9 = primeiros9 + str(primeiroDigito)
        primeiros9Invert = primeiros9[::-1]
        for index,number in enumerate(primeiros9Invert):
            result += (index+2) * int(number)
        
        resto = result % 11
        if resto < 2:
            segundoDigito = 0
        else:
            segundoDigito = 11 - resto
        
        return segundoDigito

    primeiroDigito = _calcPrimeiroDigito(primeiros9)
    segundoDigito = _calcSegundoDigito(primeiros9, primeiroDigito)
    
    if primeiroDigito == int(verificadores[0]) and segundoDigito == int(verificadores[1]):
        return True
    
    return False

def validar_cpf_cnpj(doc):
    """
    Função para validar um CPF ou CNPJ.
    Retorna True se for válido e False se for inválido.
    """
    # Remove caracteres não numéricos
    doc = re.sub('[^0-9]', '', str(doc))
    
    # Verifica se é CPF (11 dígitos) ou CNPJ (14 dígitos)
    if len(doc) == 11:
        # Verifica se todos os dígitos são iguais
        if len(set(doc)) == 1:
            return False
        
        # Calcula o primeiro dígito verificador
        soma = sum([int(doc[i]) * (10-i) for i in range(9)])
        dv1 = 11 - (soma % 11)
        if dv1 > 9:
            dv1 = 0
        
        # Calcula o segundo dígito verificador
        soma = sum([int(doc[i]) * (11-i) for i in range(10)])
        dv2 = 11 - (soma % 11)
        if dv2 > 9:
            dv2 = 0
        
        # Verifica se os dígitos verificadores são iguais aos do documento
        return dv1 == int(doc[9]) and dv2 == int(doc[10])
    
    elif len(doc) == 14:
        # Verifica se todos os dígitos são iguais
        if len(set(doc)) == 1:
            return False
        
        # Calcula o primeiro dígito verificador
        soma = sum([int(doc[i]) * (5+i) for i in range(4)]) + \
               sum([int(doc[i]) * (9-i) for i in range(8,12)])
        dv1 = 11 - (soma % 11)
        if dv1 > 9:
            dv1 = 0
        
        # Calcula o segundo dígito verificador
        soma = sum([int(doc[i]) * (6+i) for i in range(5)]) + \
               sum([int(doc[i]) * (9-i) for i in range(8,13)])
        dv2 = 11 - (soma % 11)
        if dv2 > 9:
            dv2 = 0
        
        # Verifica se os dígitos verificadores são iguais aos do documento
        return dv1 == int(doc[12]) and dv2 == int(doc[13])
    
    else:
        return False

def maskCpf(target: str|int) -> str:
    target = str(target)

    if len(target) != 11:
        raise IndexError("Quantidade de numeros no cpf deve ser igual a 11")
    
    target = target[:3] + '.' + target[3:6] + '.' + target[6:9] + '-' + target[9:]
    return target

def maskPhone(target: str|int) -> str:
    target = str(target)

    if len(target) != 11:
        raise IndexError("Número incorreto, verifique se faltou o DDD ou o numero 9")
    
    target = f'({target[:2]}) {target[2]} {target[3:7]}-{target[7:]}'
    return target

def brDateToHtmlDate(date: str):
    d = date.split('/')
    return f'{d[2]}-{d[1]}-{d[0]}'

def htmlDateToBrDate(date: str):
    d = date.split('-')
    return f'{d[2]}/{d[1]}/{d[0]}'
