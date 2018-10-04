let preferences = ["Oscars", "Golden Globes"]

let getResults = (round) => {

    $.post('/db/compare/', {round, preferences})
    .done((data) => {
        console.log(data);
    });
}

$(document).ready(() => {
    $("input").keydown((e) => {
        if (e.keyCode == 13) {
            let round = $("input").toArray().map(i => i.value);
            getResults(round)
        }
    });
});
