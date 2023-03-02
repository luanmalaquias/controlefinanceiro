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

def unmask(target: any, chars: str) -> str:
    """Remove todos os caracteres que forem passados no parametro chars"""
    if type(target) != str:
        target = str(target)
    for char in chars:
        target = target.replace(char, '')
    return target

def gerarDados(quantidade:int) -> None:
    from django.contrib.auth.models import User
    from usuario.models import Perfil
    from imobiliaria.models import Imovel
    from pagamento.models import Pagamento
    from random import randint
    from datetime import datetime

    usuarios = User.objects.all().filter(is_staff=False).delete()
    imoveis = Imovel.objects.all().delete()
    pagamentos = Pagamento.objects.all().delete()

    nomes = ["Miguel","Arthur","Gael","Théo","Heitor","Ravi","Davi","Bernardo","Noah","Gabriel","Helena","Alice","Laura","Maria Alice","Sophia","Manuela","Maitê","Liz","Cecília","Isabella"]
    sobrenomes = ['Silva','Santos','Oliveira','Sousa','Rodrigues','Ferreira','Alves','Pereira','Lima','Gomes','Costa','Ribeiro','Martins','Carvalho','Almeira','Lopes','Soares','Fernandes','Vieira','Barbosa','Rocha','Dias','Nascimento','Andrade','Moreira','Nunes','Marques','Machado','Mendes','Freitas','Cardoso','Ramos','Gonçalves','Santana','Teixeira']

    for x in range(quantidade):
        username = [str(randint(0, 9)) for i in range(11)]
        usuario = User.objects.create_user(username="".join(username), password=generatePassword(0))

        imovel = Imovel.objects.create()
        imovel.nome = f'imovel teste {x}'
        imovel.cep = "".join([str(randint(0, 9)) for i in range(7)])
        imovel.endereco = f'endereco teste {x}'
        imovel.numero = f'{randint(0,100)}'
        imovel.bairro = f'bairro teste {x}'
        imovel.cidade = f'cidade teste {x}'
        imovel.uf = "".join([secrets.choice(string.ascii_uppercase) for i in range(2)])
        imovel.mensalidade = f'{randint(500, 1000)}'
        imovel.vencimento = randint(1,29)
        imovel.disponibilidade = False

        perfil = Perfil.objects.create(usuario = usuario)
        perfil.cpf = usuario.username
        perfil.nome_completo = f'{secrets.choice(nomes)} {secrets.choice(sobrenomes)}'
        perfil.telefone = "".join([str(randint(0, 9)) for i in range(11)])
        perfil.imovel = imovel

        pagamento = Pagamento.objects.create(perfil = perfil)
        pagamento.status = "Concluido"
        pagamento.valor_pago = imovel.mensalidade
        pagamento.data = datetime.now()

        usuario.save()
        imovel.save()
        perfil.save()
        pagamento.save()