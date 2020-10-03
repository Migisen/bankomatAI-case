$(document).ready(function(){
    $(".btn").click(function () {
        $.ajax({
            url: '',
            type: 'get',
            data: {
                utility_input: $(".form-utility").val()
            },
            success: function (response) {
                $(".card-text").first().replaceWith("<p class='card-text'>  Прогнозируемая привлекательность " +
                    '<b>' + response.result + "</b></p>")
            }
        });
    });

    $(".atm-list-button").click(function (){
        $.ajax({
            url: '',
            type: 'get',
            data: {
                atm_id: $(this).find(".atm-id").text()
            },
            success: function (response) {
                $(".map-container").append("<h1>"  + "</h1>")
            }
        });
        $(".atm-list-button").removeClass("active")
        $(this).toggleClass("active");
        $(this).find("small").removeClass("text-muted")
    });
});