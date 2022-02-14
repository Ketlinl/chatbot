function Send(event) {
  const Enter = 13;
  if (event.keyCode === Enter) {
    makeQuestion();
    return false;
  }
}

function makeQuestion() {
  const $input = document.getElementById("input");
  const question = $input.value.toString().trim();

  // Remover os acentos
  let questionSended = question.normalize('NFD').replace(/[\u0300-\u036f]/g, '');
  // Remover caracteres não alfanumericos
  questionSended = questionSended.replace(/[^a-zA-Z0-9@,.;:!-\s]/g, '');

  const $msg = document.getElementById("msg");
  const $protocol = document.getElementById("protocol");
  const $inputBefore = document.getElementById("input_before_id");
  const protocol = $protocol.value;
  const inputBeforeId = Number($inputBefore.value);
  console.log(inputBeforeId);

  // Remove o link para rolar o scroll para o final de forma automática
  let msgLines = $msg.innerHTML;
  msgLines = msgLines.replace('<a href="#" id="end">', '');

  // Abre uma conexão HTTP
  const http = new XMLHttpRequest();
  const request_async = true;
  http.open('GET', `/questao/${protocol}/answer/${inputBeforeId}/${questionSended}/`, request_async);
  http.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
  // Executa na conclusão do envio da requisição.
  http.onreadystatechange = function() {
    // Verificar se a operação foi concluida com sucesso.
    if (this.readyState == XMLHttpRequest.DONE && this.status === 200) {
      // Pega o objeto json da nossa view python
      let objJSON = JSON.parse(http.responseText);
      console.log(objJSON);
      // Se existir conteudo pegue a pergunta (input) e a resposta (output) e insira no html do chatbot.
      if (objJSON) {
        const input = question;
        $inputBefore.value = objJSON.question_id;
        const output = objJSON.output.toString().trim();
        msgLines += `
          <div class="talk-bubble tri-right right-top" style="width: 90%; background-color: #8000FF;">
            <div class="talktext">
              <p>${input}</p>
            </div>
          </div>

          <div class="talk-bubble tri-right left-top" style="width: 90%; background-color: #00AABB;">
            <div class="talktext">
              <p>${output}</p>
            </div>
          </div>

          <a href="#" id="end">
        `;
        // Limpar o input, insere o novo html na página e da um scroll para a última msg.
        document.getElementById("input").value = '';
        $msg.innerHTML = msgLines;
        window.location.href = '#end';
        // Retorna o foco para o input de digitação de perguntas
        document.getElementById("input").focus();
      }
    }
  }
  // Envia a requisição
  http.send();
}
// No carregamento da página de um scroll até a última msg com foco no input.
window.location.href = '#end';
document.getElementById("input").focus();
