// alterar ordem dos labels
$('p label').each(function() {
    $(this).insertAfter( $(this).next('input') );
    $(this).insertAfter( $(this).next('select') );
});

// trocar os elementos P por DIVS
$("p").each(function() {
    $(this).replaceWith("<div class=\"form-floating mb-3\">" + $(this).html() + "</div>");
});

// configurações dos inputs
$('input').addClass('form-control')
$('input').each(function(){
    $(this).attr('placeholder', 'placeholder');
})

// configurações dos selects
$('select').addClass('form-select')

$('.errorlist').children().each(function(){
    $(this).addClass('badge text-danger')
})