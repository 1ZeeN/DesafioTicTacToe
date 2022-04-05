# Exercício de Nivelamento - Fernando Camargo

## Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Usage](#usage)
- [Author](#author)

## About <a name = "about"></a>

Code for Tic Tac Toe that utilizes Python and Flask for play with HTTP request.

## Getting Started <a name = "getting_started"></a>

### Prerequisites

What things you need to install the software and how to install them.

```
Flask
Client HTTP, thats suports GET and POST requests.
```

### Installing

This code only needs Flask to run, so:

```
pip install Flask
```

## Usage <a name = "usage"></a>

### Endpoints:
`http://localhost/jogada` = receive the player and the desired position.

POST parameters example:
```
pos = P11
player = O
```

Output:
```
{
	"jogada": "P11",
	"jogador": "O",
	"message": "Movimento executado!",
	"status": "OK"
}
```

`http://localhost/status` = shows the status of the game in json.

Output:
```
{
	"jogadas": [
		"P22 => O",
		"P11 => X",
		"P31 => O",
		"P13 => X",
		"P12 => O",
		"P32 => X",
		"P21 => O",
		"P23 => X",
		"P33 => O"
	],
	"message": "Jogo Empatado",
	"status": "OK"
}
```
`http://localhost/reiniciar` = clean all the variables to restart the game.


## Author:
Fernando Camargo - <fernando.fox.camargo@gmail.com>
