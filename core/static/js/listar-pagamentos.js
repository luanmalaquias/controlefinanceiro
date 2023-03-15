function criar_pagamento(id){
    data = document.getElementById("id_data").value
    window.location.href = `/pagamento/editar-pagamento/${id}/listar-todos-os-pagamentos/${data}`
}
function pagamento_rapido(id){
    data = document.getElementById("id_data").value
    window.location.href = `/pagamento/adicionarpagamentorapido/${id}/${data}`
}
function deletar_rapido(id){
    data = document.getElementById("id_data").value
    window.location.href = `/pagamento/deletarpagamentorapido/${id}/${data}`
}