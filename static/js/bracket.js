let preferences = ["Oscars", "Golden Globes"]

let makeMatch = (matchA, matchB, edgeType) => {
    nameA = matchA.name
    nameB = matchB.name

    awardsA = matchA.awards
    awardsB = matchB.awards
    
    return '<div class="match ' + edgeType + '">' + 
        '<h4>' + nameA + '</h4>' + 
        '<div class="awards">' + awardsA.reduce((a, v) => (
            a + ('<span class="' + v.entity + '"></span>')), '') +
        '</div><hr/>' + 
        '<h4>' + nameB + '</h4>' + 
        '<div class="awards">' + awardsB.reduce((a, v) => (
            a + ('<span class="' + v.entity + '"></span>')), '') +
        '</div></div>'
}

let winner = (movieA, movieB) => {
    return movieA.awards.length > movieB.awards.length ? movieA : movieB
}

let makeBracket = (round) => {
    console.log('make bracket', round)

    $(".col.left").empty()

    let winners = []

    for (i = 0; i < round.length; i += 2) {
        movieA = round[i]
        movieB = round[i+1]
    
        next = winner(movieA, movieB)
        
        winners.push(next)

        edge = (i%4 == 2) ? "up right" : "down right";

        $('.col.left').append(makeMatch(movieA, movieB, edge)) 
    }

    let helper = (round, carry) => {
        for (i = 0; i < round.length; i += 2) {
            movieA = round[i]
            movieB = round[i+1]
        
            next = winner(movieA, movieB)
            
            winners.push(next)

            edge = (i%4 == 2) ? "up right" : "down right";

            $('.col.right').append(makeMatch(movieA, movieB, edge)) 
        }
    }
    return helper(winners, [])
}

let getData = (round, success, error) => {
    $.post('/db/compare/', {round})
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

            getData(round, makeBracket, alert)
        }
    });
});
