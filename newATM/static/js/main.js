$(document).ready(function(){
    $(".btn-single").click(function () {
        $.ajax({
            url: '',
            type: 'get',
            data: {
                utility_input: $(".form-utility").val()
            },
            success: function (response) {
                console.log(response.result)
                $(".card-text").first().replaceWith("<p class='card-text'>  Прогнозируемая привлекательность " +
                    '<b>' + response.result + "</b></p>")
            }
        });
    });

    $(".btn-multi").click(function (){
        $.ajax({
        url: '',
        type: 'get',
        data: {
            utility_multi_input: $(".form-utility-multi").val()
        },
            success: function (response){
                $('.map-pred-img').attr("src", "/static/maps/mappred.png?random"+new Date().getTime());
            }
    });
    });

    $('select').on('change', function () {
        let a = this.value
        let d = new Date()
        $.ajax({
            url: '',
            type: 'get',
            data: {
                city: a
            },
            success: function (response) {
                $('.map-img').attr("src", "/static/maps/maps.png?random"+new Date().getTime())
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
                $(".img-dashboard").attr("src", "/static/maps/atm_map.png?random"+new Date().getTime())
            }
        });
        $(".atm-list-button").removeClass("active");
        $(this).toggleClass("active");
        $(this).find("small").removeClass("text-muted");
    });
});

