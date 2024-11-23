# tictacBINGO

challenge authors: neonlian and RJCyber

category: web

writeup author: neonlian

## Revenge

There was an unintended solution in tictactocket where you could win the tictactoe game by clicking on one square, and then quickly spam clicking the square where the computer is going to place a piece in response. No coding or cyber skills required! We fixed that for tictacBINGO >:)

## Solution

The solution for tictacBINGO is similar to the intended solution for tictactocket. Read the solution writeup for tictactocket first before this one.

These are the main changes from tictactocket:
* To win, you must place your piece on all 9 squares of the board (not just 3 in a row)
* You can no longer overwrite the opponent's pieces with your own, because the server now checks if there is a piece already at where you are trying to place yours.
* However, the server now does not correctly check whose turn it is when you request to place a piece.

To win tictacBINGO, you must send 9 piece place requests simultaneously. You will win if all of your pieces get placed before the computer makes its move. 

You can replace the function `e()` with this code in the javascript file to achieve this:
```js
function e(i) {
    for (var x = 0; x < 9; x++) {
        b['emit']('client_place_square', {
            'game_id': a,
            'square': x
        });
    }
}
```

You may need to refresh the page and attempt this multiple times if some but not all pieces get placed before
the computer.
