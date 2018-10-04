$(document).ready(function() {
    let state = {
        rounds: $(".round.input").length 
    }
    console.log(state.rounds)
    $("input").keydown(function(e) {
        switch(e.keyCode) {
            case 13:
                $.ajax({
                    url: '/db/compare',
                    type: 'POST',
                    dataType: 'json',
                    contentType: 'application/json',
                    data: JSON.stringify(person)
                });
                break;
            default:
                break;
        
        }
    });
});
