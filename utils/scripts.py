import secrets
import string

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

def unmaskCpf(cpf: str) -> str:
    """Retorna a string cpf sem pontos e traços"""
    cpf = cpf.replace('.', '').replace('-','')
    return cpf
    
def unmaskPhone(phone: str) -> str:
    """Retorna a string telefone sem espaços, traços e parênteses"""
    phone = phone.replace(' ','').replace('-','').replace('(','').replace(')','')
    return phone

def unmaskCep(cep: str) -> str:
    return cep.replace('-','').replace('.','')

def gerarDados(quantidade:int) -> None:
    from django.contrib.auth.models import User
    from usuario.models import Perfil
    from imobiliaria.models import Imovel
    from random import randint

    for x in range(quantidade):
        try:
            username = [str(randint(0, 9)) for i in range(11)]
            usuario = User.objects.create_user(username="".join(username), password=generatePassword(0))

            imovel = Imovel.objects.create()
            imovel.nome = f'imovel teste {x}'
            imovel.cep = "".join([str(randint(0, 9)) for i in range(7)])
            imovel.endereco = f'endereco teste {x}'
            imovel.numero = f'{randint(0,100)}'
            imovel.bairro = f'bairro teste {x}'
            imovel.cidade = f'cidade teste {x}'
            imovel.uf = f'uf teste {x}'
            imovel.mensalidade = f'{randint(500, 1000)}'
            imovel.vencimento = randint(1,29)
            imovel.disponibilidade = False

            perfil = Perfil.objects.create(usuario = usuario)
            perfil.cpf = usuario.username
            perfil.nome_completo = f'usuario teste {x}'
            perfil.telefone = "".join([str(randint(0, 9)) for i in range(11)])
            perfil.imovel = imovel

            usuario.save()
            imovel.save()
            perfil.save()
        except: pass