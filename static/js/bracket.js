let preferences = ["Oscars", "Golden Globes"]

let insertBracket = (payload) => {
    $(".col.left").html(payload.input)
    $(".col.right").html(payload.results)
}

let getData = (round, success, error) => {
    $.post('/results/', {round})
    .done((data) => {
        if (data.type == "SUCCESS") {
            success(data.payload)
        } else {
            error(data.payload) 
        }
    });
}

$(document).ready(() => {
    $("input").keydown((e) => {
        if (e.keyCode == 13) {

            let round = $("input").toArray().map(i => i.value);

            getData(round, insertBracket, alert)
        }
    });
});
