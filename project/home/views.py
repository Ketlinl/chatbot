from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from ..questions.models import Question
from ..captures.models import Capture
from validate_docbr import CPF, CNPJ
from unidecode import unidecode
import buscacep
import re as regex

User = get_user_model()


def home(request):
    """
    View de capturas de dados.
    """

    return render(request, template_name="home.html")


def chatbot(request, protocol):
    """
    Abre a página do chatbot.
    """

    return render(
        request,
        template_name="chatbot.html",
        context={"protocol": protocol}
    )


def nlk_process(request, protocol, code_before, question):
    """
    Realiza o processamento de linguagem natural extraindo as
    informações importantes.
    """

    results = []

    try:
        user = User.objects.get(protocol=protocol)
    except User.DoesNotExist:
        return [
            {
                "current_code": 0,
                "protocol": protocol,
                "code_before": code_before,
                "question": question,
                "input": question,
                "output": "Ocorreu um problema na requisição."
            }
        ]

    # Substitui o caractere de espaço vindo da url pelo próprio caractere de espaço
    question = question.replace('%20', ' ')
    lower_question = question.lower()

    # Realiza o filtro das questões cadastradas
    if code_before > 0:
        queryset = Question.objects.filter(
            user__protocol=protocol,
            code_relation=code_before,
            is_active=True
        )

        if len(queryset) <= 0:
            queryset = Question.objects.filter(
                user__protocol=protocol,
                is_active=True
            )
    else:
        queryset = Question.objects.filter(
            user__protocol=protocol,
            is_active=True
        )

    # Captura da informação de idade
    age = 0
    if 'anos' in lower_question:
        # Pega 8 caracteres antes da palavra anos para encapsular a idade
        age = lower_question[lower_question.index('anos')-8:lower_question.index('anos')]
        # Por regex extrai os número da frase encapsulada acima.
        age = int(regex.sub('[^0-9]', '', age))
    else:
        # Caso não tenha passado o anos na resposta vamos quebrar a resposta em pedaços
        tokens = lower_question.split(' ')
        # Percorrer esses pedaços
        for token in tokes:
            # Por regex extrai o que tiver número
            parts = regex.sub('[^0-9]', '', token)
            # Se o número estiver entre 0 e 99 então armazene
            if len(parts) >= 1 and len(parts) <= 3:
                age = int(parts)

    # Captura da informação de sexo
    sex = ""
    temp = lower_question.replace(",", "").replace(".", "").replace(";", "").replace("!", "")
    if temp in [" m ", "masculino"]:
        sex = "M"
    elif temp in [" f ", "feminino"]:
        sex = "F"

    # Captura de informações
    email = ""
    name = ""
    document = ""
    phone = ""
    zip_code = ""
    state = ""
    city = ""
    neighborhood = ""
    address = ""
    number = ""
    tokens = lower_question.split(" ")
    for token in tokens:
        # Captura da informação do nome e email
        if "@" in token and "." in token:
            email = token.strip()
            # Verifica se o usuário encerrou a centensa com um ponto final
            if email[-1] == '.':
                email = email[0:-1]
            # Limpa o email de possíveis caracteres indesejados.
            email = email.replace(',', '').replace(';', '').replace('!', '')
            # Pega o nome da pessoa a partir do email cadastrado
            name = email.split("@")[0]

        # Captura da informação de CPF
        parts = regex.sub('[0-9]', '', token)
        if len(parts) == 11:
            objCPF = CPF()
            if objCPF.validade(parts):
                document = parts.strip()

        # Captura da informação de CNPJ
        if len(parts) == 14:
            objCNPJ = CNPJ()
            if objCNPJ.validade(parts):
                document = parts.strip()

        # Captura do telefone, como CPF e número tem a mesma
        # quantidade de digitos (11) é bom diferencia-las.
        if parts != cpf:
            # Todo número de telefone deve possuir o digito 9
            if '9' in parts:
                # 13 - Telefone com o código brasileiro 55
                # 11 - Telefone com o DDD e sem o código
                # 9 - Telefone sem ambos
                if len(parts) in [13, 11, 9]:
                    phone = parts.strip()

        # Captura do CEP e pegar o endereço pelos correios
        if len(parts) == 8:
            try:
                response = buscacep.busca_cep_correios(parts)
            except:
                response = None

            print(response)
            if response:
                zip_code = parts.strip()
                state = response.localidade[response.localidade.index("/"):].replace("/", "").strip()
                city = response.localidade[:response.localidade.index("/")].strip()
                neighborhood = response.bairro.strip()
                address = response.logradouro.strip()
                number = regex.sub('[0-9/]', '', response.logradouro)

    # Armazenar os resultados da captura
    if any([age, sex, email, name, document, phone, zip_code]):
        capture = Capture.objects.create(
            user=user,
            age=age,
            sex=sex,
            email=email,
            name=name,
            document=document,
            phone=phone,
            zip_code=zip_code,
            state=state.upper(),
            city=city,
            neighborhood=neighborhood,
            address=address,
            number=number,
        )

        results.append({
            "current_code": 0,
            "protocol": protocol,
            "code_before": code_before,
            "question": question,
            "input": question,
            "output": "Ok, entendi"
        })
    # Controle de abreviações
    else:
        temp = lower_question.replace("vc", "voce")
        temp = temp.replace("vcs", "voces")
        temp = temp.replace("eh", "e")
        temp = temp.replace("tb", "tambem")
        temp = temp.replace("tbm", "tambem")
        temp = temp.replace("oq", "o que")
        temp = temp.replace("dq", "de que")
        temp = temp.replace("td", "tudo")
        temp = temp.replace("pq", "porque")

        # Cria uma lista com query da consulta
        if len(queryset) <= 0:
            results.append({
                "current_code": 0,
                "protocol": protocol,
                "code_before": code_before,
                "question": question,
                "input": question,
                "output": "Desculpe, mas não sei informar."
            })
        else:
            for query in queryset:
                results.append({
                    "current_code": query.id,
                    "protocol": protocol,
                    "code_before": code_before,
                    "question": query.question,
                    "input": question,
                    "output": query.answer
                })

        # Remove acentuação e espaços
        question_received = unidecode(question)
        question_received.replace("?", "")
        question_received = question_received.strip()
        # Coloca em minúscula
        question_received = question_received.lower()
        # Elimina as 3 ultimas letras de cada palavra com tokenização
        temp = question_received.split(" ")
        temp_list = []
        for x in temp:
            if len(x) > 3:
                temp_list.append(x[0:len(x)-3])
            else:
                temp_list.append(x)
        question_received = ' '.join(temp_list)
        # Percorrer a lista de registros encontrados
        equals = 0
        code = ""
        for x in results:
            # Removor acentuação e espaços
            question_found = unidecode(x['question'])
            question_found.replace("?", "")
            question_found = question_found.strip()
            # Coloca em minuscula
            question_found = question_found.lower()
            # Elimina as 3 ultimas letras de cada palavra com tokenização
            temp = question_found.split(" ")
            temp_list = []
            for y in temp:
                if len(y) > 3:
                    temp_list.append(y[0:len(y)-3])
                else:
                    temp_list.append(y)
            question_found = ' '.join(temp_list)
            # Criar uma lista para a questão recebida e uma para a questão encontrada
            question_received_list = question_received.split(" ")
            question_found_list = question_found.split(" ")
            # Conta as palavras recebidas que coincidem com as palavras de cada questão encontrada
            qtd = 0
            for y in question_received_list:
                if y in question_found_list:
                    qtd += 1

            if qtd >= equals:
                equals = qtd
                code = x['current_code']

        # Deixa na lista somente a resposta correspondente
        corresponding = []
        for x in results:
            if code == x['current_code']:
                corresponding.append(x)
                break

        results = corresponding

    return JsonResponse(results, safe=False)
