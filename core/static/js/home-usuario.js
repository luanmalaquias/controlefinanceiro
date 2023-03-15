function copy(alerta) {
    let textarea = document.getElementById("copia-e-cola");
    textarea.select();
    document.execCommand("copy");          
    window.alert("Código copiado");
}

function abrirPicPay(){
    copy();
    window.location.assign('picpay://');
}