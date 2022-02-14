from django.contrib.auth import get_user_model
from .questions.models import Question
from .captures.models import Capture
from .utils import zip_code_request
from validate_docbr import CPF, CNPJ
from unidecode import unidecode
import re as regex
import os

User = get_user_model()


class PLN:
    """
    Classe responsável pelo processamento de linguagem natural.
    """

    def __init__(self, protocol, input_before_id, current_input):
        """
        Construtor
        """

        self.input = current_input
        self.input_before_id = input_before_id
        self.protocol = protocol

    def __get_user_by_chatbot_protocol(self):
        """
        Pega o usuário dono do chatbot pelo seu protocolo.
        """

        try:
            user = User.objects.get(protocol=self.protocol)
        except User.DoesNotExist:
            return None

        return user

    def __format_input(self):
        """
        Formata a entrada do usuário no chatbot.
        Substitui o caractere de espaço vindo da url
        pelo próprio caractere de espaço
        """

        self.input = self.input.replace('%20', ' ')
        return self.input.lower()

    def __get_stored_sentences(self):
        """
        Realiza o filtro das questões cadastradas
        """

        question = None
        if self.input_before_id > 0:
            question = Question.objects.filter(id=self.input_before_id).last()

        print(self.input_before_id, question)
        # Se existir uma pergunta anterior relacionada
        if question:
            # Pegue a questão que esteja relacionado a entrada anterior, caso exista.
            queryset = Question.objects.filter(
                user__protocol=self.protocol,
                input_before=question,
                is_active=True
            )
            print(queryset)

            # Caso não ache provavelmente é uma pergunta que não tem relação com as outras.
            if len(queryset) <= 0:
                queryset = Question.objects.filter(
                    user__protocol=self.protocol,
                    is_active=True
                )
        # Caso seja uma nova pergunta
        else:
            queryset = Question.objects.filter(
                user__protocol=self.protocol,
                is_active=True
            )

        return queryset

    def __capture_age(self, current_input):
        """
        Captura da informação de idade
        """

        age = 0
        if 'anos' in current_input:
            # Pega 8 caracteres antes da palavra anos para encapsular a idade
            age = current_input[current_input.index('anos')-8:current_input.index('anos')]
            # Por regex extrai os número da frase encapsulada acima.
            age = int(regex.sub('[^0-9]', '', age))
        else:
            # Caso não tenha passado o anos na resposta vamos quebrar a resposta em pedaços
            tokens = current_input.split(' ')
            # Percorrer esses pedaços
            for token in tokens:
                # Por regex extrai o que tiver número
                parts = regex.sub('[^0-9]', '', token)
                # Se o número estiver entre 1 e 3 digitos então armazene
                if len(parts) >= 1 and len(parts) <= 3:
                    age = int(parts)

        return age

    def __capture_sex(self, current_input):
        """
        Captura da informação de sexo
        """

        sex = ""
        temp = current_input.replace(",", "").replace(".", "").replace(";", "").replace("!", "")
        if " m " in temp or "masculino" in temp:
            sex = "M"
        elif " f " in temp or "feminino" in temp:
            sex = "F"

        return sex

    def __capture_email_and_name(self, token):
        """
        Se for passado, captura a informação de email
        e a partir do email o nome.
        """

        email, name = "", ""
        if "@" in token and "." in token:
            email = token.strip()
            # Verifica se o usuário encerrou a sentença com um ponto final
            if email[-1] == '.':
                email = email[0:-1]
            # Limpa o email de possíveis caracteres indesejados.
            email = email.replace(',', '').replace(';', '').replace('!', '')
            # Pega o nome da pessoa a partir do email cadastrado
            name = email.split("@")[0]

        return email, name

    def __capture_document(self, number, token):
        """
        Se for passado, captura a informação do documento
        do usuárion, CPF ou CNPJ.
        """

        document = ""
        # Captura da informação de CPF
        if len(number) == 11:
            objCPF = CPF()
            if objCPF.validade(number):
                document = number.strip()

        # Captura da informação de CNPJ
        if len(number) == 14:
            objCNPJ = CNPJ()
            if objCNPJ.validade(number):
                document = number.strip()

        return document

    def __capture_phone(self, document, number, token):
        """
        Captura as informações do telefone celular.
        """

        phone = ""
        # Como CPF e número tem a mesma quantidade de digitos (11)
        # é bom diferencia-las.
        number = regex.sub('[0-9]', '', token)
        if len(document) == 11 and number != document:
            # Todo número de telefone deve possuir o digito 9
            if '9' in number:
                # 13 - Telefone com o código brasileiro 55
                # 11 - Telefone com o DDD e sem o código
                # 9 - Telefone sem ambos
                if len(number) in [13, 11, 9]:
                    phone = number.strip()

        return phone

    def __capture_address(self, number, token):
        """
        Captura o CEP e apartir dele pega os outros dados.
        """

        address = {}
        if len(number) == 8:
            address = zip_code_request(number)

        return address

    def __abbreviation_control(self, current_input):
        """
        Controle de abreviações.
        """

        temp = current_input.replace("vc", "voce")
        temp = temp.replace("vcs", "voces")
        temp = temp.replace("eh", "e")
        temp = temp.replace("tb", "tambem")
        temp = temp.replace("tbm", "tambem")
        temp = temp.replace("oq", "o que")
        temp = temp.replace("dq", "de que")
        temp = temp.replace("td", "tudo")
        temp = temp.replace("pq", "porque")

        return temp

    def __remove_commom_expression(self, current_input):
        """
        Remove as expressões comuns que tem em quase todas as perguntas.
        """

        temp = current_input.replace(" que ", "")
        temp = temp.replace("quem ", "")
        return temp

    def __populate_question_found(self, queryset):
        """
        Pega todas as perguntas encontradas para realizar a
        inteligencia do algoritmo.
        """

        results = []
        if len(queryset) > 0:
            for query in queryset:
                results.append({
                    "question_id": query.id,
                    "input": query.body,
                    "output": query.answer
                })

            return results

        return {
            "question_id": 0,
            "output": "Desculpe, essa informação eu não sei te responder ainda."
        }

    def __input_treatment(self, current_input):
        """
        Aqui será realizado um tratamento da pergunta que o usuário enviou.
        """

        # Remove acentuação e espaços, ponto de interrogação e coloca em minusculo.
        input_received = unidecode(current_input)
        input_received = input_received.replace("?", "")
        input_received = input_received.strip()
        input_received = input_received.lower()

        # Elimina as 3 ultimas letras de cada palavra com tokenização
        # para desconsiderar o tempo verbal de cada palavra
        temp = input_received.split(" ")
        temp_list = []
        for x in temp:
            if len(x) > 3:
                temp_list.append(x[0:len(x)-3])
            else:
                temp_list.append(x)

        input_received = ' '.join(temp_list)
        return input_received

    def __answer_treatment(self, question):
        """
        Percorrer a lista de registros encontrados, no caso as perguntas cadastradas
        no banco de dados e realiza seu tratamento.
        """

        # Remove acentuação e espaços, tira a ? e coloca em minusculo
        question_found = unidecode(question['input'])
        question_found = question_found.replace("?", "")
        question_found = question_found.strip()
        question_found = question_found.lower()

        # Elimina as 3 ultimas letras de cada palavra com tokenização
        # para desconsiderar o tempo verbal de cada palavra
        temp = question_found.split(" ")
        temp_list = []
        for y in temp:
            if len(y) > 3:
                temp_list.append(y[0:len(y)-3])
            else:
                temp_list.append(y)

        question_found = ' '.join(temp_list)
        return question_found

    def get_result(self):
        """
        Pega o resultado do processamento.
        """

        print("############################")

        user = self.__get_user_by_chatbot_protocol()
        if not user:
            return {
                "question_id": 0,
                "output": "Chatbot desativado, contate o administrador dele."
            }

        print(self.input, self.input_before_id, self.protocol)

        current_input = self.__format_input()
        queryset = self.__get_stored_sentences()
        age = self.__capture_age(current_input)
        sex = self.__capture_sex(current_input)
        tokens = current_input.split(" ")
        for token in tokens:
            email, name = self.__capture_email_and_name(token)
            number = regex.sub('[0-9]', '', token)
            document = self.__capture_document(number, token)
            phone = self.__capture_phone(document, number, token)
            address = self.__capture_address(number, token)

        # print(age, sex, email, name, document, phone, number, address)

        if any([age, sex, email, name, document, phone, address]):
            print("ENTREIII CAPTURA")
            capture = Capture.objects.create(
                user=user,
                age=age,
                sex=sex,
                email=email,
                name=name.upper(),
                document=document,
                phone=phone,
                **address
            )

            return {
                "question_id": 0,
                "output": "Anotado, muito obrigado."
            }
        else:
            current_input = self.__abbreviation_control(current_input)
            # current_input = self.__remove_commom_expression(current_input)
            questions = self.__populate_question_found(queryset)
            if type(questions) == dict:
                return questions

            input_received = self.__input_treatment(current_input)

            equals = 0
            result = {
                "question_id": 0,
                "output": "Desculpe, essa informação eu não sei te responder ainda."
            }

            for question in questions:
                question_found = self.__answer_treatment(question)
                print(f"Questão: {question_found}, Questão recebida {input_received}")
                # Criar uma lista para a questão recebida e uma para a questão encontrada
                question_received_list = input_received.split(" ")
                print(question_received_list)
                question_found_list = question_found.split(" ")
                print(question_found_list)
                # Conta as palavras recebidas que coincidem com as palavras de cada questão encontrada
                # E armazenar o id da resposta com a maior quantidade de tokens semelhantes
                qtd = 0
                for _ in question_received_list:
                    if _ in question_found_list:
                        qtd += 1

                print(f"qtd: {qtd}, equals: {equals}")

                if qtd > 0 and qtd >= equals:
                    print(f"ENTREI: {question}")
                    equals = qtd
                    result['question_id'] = question['question_id']
                    result['output'] = question['output']

                print(f"Resultado: {result}")
            print("############################")

            return result
