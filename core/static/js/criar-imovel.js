// Máscaras
$('#id_cep').mask('00000-000');
$('#id_dueDate').mask('00')
$('#id_dueDate').attr('max', 29)
$('#id_mensalidade').mask('#.000,00', {reverse: true})

// Padrão em tudo?
$('form input').addClass('form-control rounded-pill');
$('form select').addClass('form-control');
$('form label').addClass('badge text-primary text-start')
$('form ul').addClass('mb-0 text-center')
$('form li').addClass('badge text-danger')

$("#id_cep").blur(function(){
    pesquisacep(this.value)
});

function limpa_formulário_cep() {
    //Limpa valores do formulário de cep.
    document.getElementById('id_address').value = ("");
    document.getElementById('id_neighborhood').value = ("");
    document.getElementById('id_city').value = ("");
    document.getElementById('id_uf').value = ("");
}

function meu_callback(conteudo) {
    if (!("erro" in conteudo)) {
        //Atualiza os campos com os valores.
        document.getElementById('id_address').value = (conteudo.logradouro);
        document.getElementById('id_neighborhood').value = (conteudo.bairro);
        document.getElementById('id_city').value = (conteudo.localidade);
        document.getElementById('id_uf').value = (conteudo.uf);
    } //end if.
    else {
        //CEP não Encontrado.
        limpa_formulário_cep();
        alert("CEP não encontrado.");
    }
}

function pesquisacep(valor) {

    //Nova variável "cep" somente com dígitos.
    var cep = valor.replace(/\D/g, '');

    //Verifica se campo cep possui valor informado.
    if (cep != "") {

        //Expressão regular para validar o CEP.
        var validacep = /^[0-9]{8}$/;

        //Valida o formato do CEP.
        if (validacep.test(cep)) {

            //Preenche os campos com "..." enquanto consulta webservice.
            document.getElementById('id_address').value = "...";
            document.getElementById('id_neighborhood').value = "...";
            document.getElementById('id_city').value = "...";
            document.getElementById('id_uf').value = "...";

            //Cria um elemento javascript.
            var script = document.createElement('script');

            //Sincroniza com o callback.
            script.src = 'https://viacep.com.br/ws/' + cep + '/json/?callback=meu_callback';

            //Insere script no documento e carrega o conteúdo.
            document.body.appendChild(script);

        } //end if.
        else {
            //cep é inválido.
            limpa_formulário_cep();
            alert("Formato de CEP inválido.");
        }
    } //end if.
    else {
        //cep sem valor, limpa formulário.
        limpa_formulário_cep();
    }
};