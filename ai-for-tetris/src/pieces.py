from src.tetris.base.Piece import Piece

I = Piece(
    [
        [0, 0, 0, 0],
        [1, 1, 1, 1],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ],
    [
        [0, 0, 1, 0],
        [0, 0, 1, 0],
        [0, 0, 1, 0],
        [0, 0, 1, 0]
    ],
    [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [1, 1, 1, 1],
        [0, 0, 0, 0]
    ],
    [
        [0, 1, 0, 0],
        [0, 1, 0, 0],
        [0, 1, 0, 0],
        [0, 1, 0, 0]
    ]
)
J = Piece(
    [
        [1, 0, 0],
        [1, 1, 1],
        [0, 0, 0],
    ],
    [
        [0, 1, 1],
        [0, 1, 0],
        [0, 1, 0]
    ],
    [
        [0, 0, 0],
        [1, 1, 1],
        [0, 0, 1]
    ],
    [
        [0, 1, 0],
        [0, 1, 0],
        [1, 1, 0]
    ]
)
L = Piece(
    [
        [0, 0, 1],
        [1, 1, 1],
        [0, 0, 0]
    ],
    [
        [0, 1, 0],
        [0, 1, 0],
        [0, 1, 1]
    ],
    [
        [0, 0, 0],
        [1, 1, 1],
        [1, 0, 0]
    ],
    [
        [1, 1, 0],
        [0, 1, 0],
        [0, 1, 0]
    ]
)
O = Piece(
    [
        [1, 1],
        [1, 1]
    ],
    [
        [1, 1],
        [1, 1]
    ],
    [
        [1, 1],
        [1, 1]
    ],
    [
        [1, 1],
        [1, 1]
    ]
)
S = Piece(
    [
        [0, 1, 1],
        [1, 1, 0],
        [0, 0, 0]
    ],
    [
        [0, 1, 0],
        [0, 1, 1],
        [0, 0, 1]
    ],
    [
        [0, 0, 0],
        [0, 1, 1],
        [1, 1, 0]
    ],
    [
        [1, 0, 0],
        [1, 1, 0],
        [0, 1, 0]
    ]
)
T = Piece(
    [
        [0, 1, 0],
        [1, 1, 1],
        [0, 0, 0]
    ],
    [
        [0, 1, 0],
        [0, 1, 1],
        [0, 1, 0]
    ],
    [
        [1, 1, 1],
        [0, 1, 0],
        [0, 0, 0]
    ],
    [
        [0, 1, 0],
        [1, 1, 0],
        [0, 1, 0]
    ]
)
Z = Piece(
    [
        [1, 1, 0],
        [0, 1, 1],
        [0, 0, 0]
    ],
    [
        [0, 0, 1],
        [0, 1, 1],
        [0, 1, 0]
    ],
    [
        [0, 0, 0],
        [1, 1, 0],
        [0, 1, 1]
    ],
    [
        [0, 1, 0],
        [1, 1, 0],
        [1, 0, 0]
    ]
)


DOT = Piece(
    [
        [0, 1], 
        [0, 0]
    ], 
    [
        [0, 0], 
        [0, 1]
    ],
    [
        [0, 0], 
        [1, 0]
    ],
    [
        [1, 0], 
        [0, 0]
    ]
)

DIAG = Piece(
    [
        [0, 1], 
        [1, 0]
    ], 
    [
        [1, 0], 
        [0, 1]
    ],
    [
        [0, 1], 
        [1, 0]
    ],
    [
        [1, 0], 
        [0, 1]
    ]
)

SMALL_L = Piece(
    [
        [0, 1], 
        [1, 1]
    ], 
    [
        [1, 0], 
        [1, 1]
    ],
    [
        [1, 1], 
        [1, 0]
    ],
    [
        [1, 1], 
        [0, 1]
    ]
)

SMALL_I = Piece(
    [
        [1, 1], 
        [0, 0]
    ], 
    [
        [0, 1], 
        [0, 1]
    ],
    [
        [0, 0], 
        [1, 1]
    ],
    [
        [1, 0], 
        [1, 0]
    ]
)

SMALL_O = Piece(
    [
        [1, 1], 
        [1, 1]
    ], 
    [
        [1, 1], 
        [1, 1]
    ],
    [
        [1, 1], 
        [1, 1]
    ],
    [
        [1, 1], 
        [1, 1]
    ]
)

CLASSICAL_PIECES = [I, J, L, O, S, T, Z]
PIECES = [DOT]