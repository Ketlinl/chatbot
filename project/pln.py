from django.contrib.auth import get_user_model
from .questions.models import Question
from .captures.models import Capture
from .utils import zip_code_request
from validate_docbr import CPF, CNPJ
from unidecode import unidecode
import re as regex
import nltk
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
        self.email = ""
        self.name = ""
        self.phone = ""
        self.document = ""
        self.sex = ""
        self.age = 0
        self.address = {}
        # Usado para extrair o radical das palavras
        self.stemmer = nltk.stem.RSLPStemmer()
        # Stop words são palavras que não tem significado dentro de uma frase
        # por exemplo, (e, do, o, com, ...)
        self.stopwords = nltk.corpus.stopwords.words("portuguese")

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

        self.formated_input = self.input.lower().replace('%20', ' ')

    def __get_stored_sentences(self):
        """
        Realiza o filtro das questões cadastradas
        """

        question = None
        if self.input_before_id > 0:
            question = Question.objects.filter(id=self.input_before_id).last()

        print(f"Pergunta anterior: {self.input_before_id} - {question}")
        # Se existir uma pergunta anterior relacionada
        if question:
            # Pegue a questão que esteja relacionado a entrada anterior, caso exista.
            queryset = Question.objects.filter(
                user__protocol=self.protocol,
                input_before=question,
                is_active=True
            )
            print(f"Lista de perguntas encontradas: {queryset}")

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

    def __capture_age(self):
        """
        Captura da informação de idade
        """

        if 'anos' in self.formated_input:
            # Pega 8 caracteres antes da palavra anos para encapsular a idade
            self.age = self.formated_input[self.formated_input.index('anos')-8:self.formated_input.index('anos')]
            # Por regex extrai os número da frase encapsulada acima.
            self.age = int(regex.sub('[^0-9]', '', self.age))
        else:
            # Caso não tenha passado o anos na resposta vamos quebrar a resposta em pedaços
            tokens = self.formated_input.split(' ')
            # Percorrer esses pedaços
            for token in tokens:
                # Por regex extrai o que tiver número
                parts = regex.sub('[^0-9]', '', token)
                # Se o número estiver entre 1 e 3 digitos então armazene
                if len(parts) >= 1 and len(parts) <= 3:
                    self.age = int(parts)

    def __capture_sex(self):
        """
        Captura da informação de sexo
        """

        temp = self.formated_input.replace(",", "").replace(".", "").replace(";", "").replace("!", "")
        if " m " in temp or "masculino" in temp:
            self.sex = "M"
        elif " f " in temp or "feminino" in temp:
            self.sex = "F"

    def __capture_email_and_name(self, token):
        """
        Se for passado, captura a informação de email
        e a partir do email o nome.
        """

        if "@" in token and "." in token:
            email = token.strip()
            # Verifica se o usuário encerrou a sentença com um ponto final
            if email[-1] == '.':
                email = email[0:-1]
            # Limpa o email de possíveis caracteres indesejados.
            self.email = email.replace(',', '').replace(';', '').replace('!', '')
            # Pega o nome da pessoa a partir do email cadastrado
            self.name = self.email.split("@")[0]

    def __capture_document(self, token):
        """
        Se for passado, captura a informação do documento
        do usuárion, CPF ou CNPJ.
        """

        # Captura da informação de CPF
        if len(token) == 11 and token.isnumeric():
            objCPF = CPF()
            if objCPF.validate(token):
                self.document = token.strip()

        # Captura da informação de CNPJ
        if len(token) == 14 and token.isnumeric():
            objCNPJ = CNPJ()
            if objCNPJ.validate(token):
                self.document = token.strip()

    def __capture_phone(self, token):
        """
        Captura as informações do telefone celular.
        """

        # Como CPF e número tem a mesma quantidade de digitos (11)
        # é bom diferencia-las.
        if len(token) == 11 and token != self.document and token.isnumeric():
            # Todo número de telefone deve possuir o digito 9
            if '9' in token:
                # 13 - Telefone com o código brasileiro 55
                # 11 - Telefone com o DDD e sem o código
                # 9 - Telefone sem ambos
                if len(token) in [13, 11, 9]:
                    self.phone = token.strip()

    def __capture_address(self, token):
        """
        Captura o CEP e apartir dele pega os outros dados.
        """

        if len(token) == 8 and token.isnumeric():
            self.address = zip_code_request(token)

    def __abbreviation_control(self):
        """
        Controle de abreviações.
        chatbot
        """

        temp = self.formated_input.replace("vc", "voce")
        temp = temp.replace("vcs", "voces")
        temp = temp.replace(" eh ", "e")
        temp = temp.replace(" tb", "tambem")
        temp = temp.replace("tbm", "tambem")
        temp = temp.replace("oq ", "o que")
        temp = temp.replace("dq ", "de que")
        temp = temp.replace(" td", "tudo")
        temp = temp.replace("pq ", "porque")
        temp = temp.replace("flw", "tchau")
        temp = temp.replace("plv", "palavra")
        temp = temp.replace("smp", "sempre")
        temp = temp.replace("msm", "mesmo")
        temp = temp.replace("obg", "obrigado")
        self.formated_input = temp

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

    def __input_treatment(self):
        """
        Aqui será realizado um tratamento da pergunta que o usuário enviou.
        """

        # Remove acentuação e espaços, ponto de interrogação e coloca em minusculo.
        input_received = unidecode(self.formated_input)
        input_received = input_received.replace("?", "").replace(",", "").replace(".", "").replace(";", "").replace("!", "")
        input_received = input_received.strip()
        input_received = input_received.lower()

        # Extrai o radical das palavras eliminando tempos verbais
        return [str(self.stemmer.stem(word)) for word in input_received.split(" ") if word not in self.stopwords]

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

        # Extrai o radical das palavras eliminando tempos verbais
        return [str(self.stemmer.stem(word)) for word in question_found.split(" ") if word not in self.stopwords]

    def get_result(self):
        """
        Pega o resultado do processamento.
        """

        print("#############################################################################")

        user = self.__get_user_by_chatbot_protocol()
        if not user:
            return {
                "question_id": 0,
                "output": "Chatbot desativado, contate o administrador dele."
            }

        print(f"Protocolo: {self.protocol}, Pergunta: {self.input}, ID da pergunta relacionada: {self.input_before_id}")

        self.__format_input()
        queryset = self.__get_stored_sentences()
        self.__capture_age()
        self.__capture_sex()
        tokens = self.formated_input.split(" ")
        for token in tokens:
            self.__capture_email_and_name(token)
            self.__capture_document(token)
            self.__capture_phone(token)
            self.__capture_address(token)

        if any([self.age, self.sex, self.email, self.name, self.document, self.phone, self.address]):
            capture, created = Capture.objects.get_or_create(
                user=user,
                email=self.email,
                defaults={
                    "document": self.document,
                    "age": self.age,
                    "sex": self.sex,
                    "name": self.name,
                    "document": self.document,
                    "phone": self.phone,
                    **self.address
                }
            )

            if not created:
                capture.email = self.email
                capture.document = self.document
                capture.age = self.age
                capture.sex = self.sex
                capture.name = self.name
                capture.document = self.document
                capture.phone = self.phone
                capture.zip_code = self.address.get("zip_code", "")
                capture.state = self.address.get("state", "")
                capture.city = self.address.get("city", "")
                capture.neighborhood = self.address.get("neighborhood", "")
                capture.address = self.address.get("address", "")
                capture.complement = self.address.get("complement", "")
                capture.save()

            return {
                "question_id": 0,
                "output": "Anotado, muito obrigado."
            }
        else:
            self.__abbreviation_control()
            questions = self.__populate_question_found(queryset)
            if type(questions) == dict:
                return questions

            input_received = self.__input_treatment()

            equals = 0
            result = {
                "question_id": 0,
                "output": "Desculpe, essa informação eu não sei te responder ainda."
            }

            for question in questions:
                question_found = self.__answer_treatment(question)
                print(f"Questão: {question_found}, Questão recebida {input_received}")
                # Conta as palavras recebidas que coincidem com as palavras de cada questão encontrada
                # E armazenar o id da resposta com a maior quantidade de tokens semelhantes
                qtd = 0
                for _ in input_received:
                    if _ in question_found:
                        qtd += 1

                print(f"qtd: {qtd}, equals: {equals}")

                if qtd > 0 and qtd >= equals:
                    print(f"ENTREI: {question}")
                    equals = qtd
                    result['question_id'] = question['question_id']
                    result['output'] = question['output']

                print(f"Resultado: {result}")

            print("#############################################################################")

            return result
