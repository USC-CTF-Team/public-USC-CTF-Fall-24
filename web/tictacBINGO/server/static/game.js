(function(){
var game_id = null
var socket = io();

function setStatusMessage(message)
{
    document.getElementById("status").innerText = message;
}

function onSquareClick(square)
{
    if (game_id == null) return;
    socket.emit('client_check_square_valid', {"game_id": game_id, "square": square});
}

function rcv_server_check_square_valid(json)
{
    if (game_id == null) return;
    if (json.is_valid)
        socket.emit('client_place_square', {"game_id": game_id, "square": json.square});
    else
        setStatusMessage("Cannot place square there");
}

function rcv_server_board_update(json)
{
    if (game_id == null) return;
    if (!json.is_valid) {
        setStatusMessage("Game doesn't exist; try refresh the page");
        return;
    }

    for (var i = 0; i < 9; i++)
    {
        boardVal = json.board[i] == 0 ? "X" : (json.board[i] == 1 ? "O" : "")
        document.getElementById("ttt" + i).innerText = boardVal
    }

    if (json.turn == 0)
        setStatusMessage("Your turn");
    else if (json.turn == 1)
        setStatusMessage("Computer is thinking...")

    if (json.winner == 0) {
        setStatusMessage(json.flag)
        game_id = null
        return;
    }
    if (json.winner == 1) {
        setStatusMessage("You lose...")
        game_id = null
        return;
    }  
    if (json.winner == 3) {
        setStatusMessage("Tie.")
        game_id = null
        return;
    }  
}

// Program begins here

function attachListeners()
{
    for (var i = 0; i < 9; i++)
    {
        document.getElementById("ttt" + i).addEventListener('click', function(x){onSquareClick(x)}.bind(null, i));
    }
}

function main()
{
    socket.on('connect', function() {
        socket.emit('client_new_game');
    });

    socket.on('server_new_game', function (json) {
        game_id = json.game_id;
    });

    socket.on('server_check_square_valid', rcv_server_check_square_valid);

    socket.on('server_board_update', rcv_server_board_update)
}
window.onload = attachListeners;
main()
})();