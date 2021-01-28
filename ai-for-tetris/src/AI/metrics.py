import numpy as np

def compute_holes(board):
    """
        Compute the number of holes in the board

        Note: a hole is defined as an empty cell with a block one or more 
        blocks above

        Parameters
        ----------
            board: 2d array_like
                The tetris board
    """
    holes = 0
    size = board.shape

    for j in range(0, board.shape[1]):
        is_one = False

        for e in board[:, j]:
            if is_one and e == 0:
                holes += 1
            elif e == 1:
                is_one = True

    return holes

def compute_height(board):
    """
        Compute the maximum height of the board

        Parameters
        ----------
            board: 2d array_like
                The tetris board
    """
    max_height = 0

    for j in range(0, board.shape[1]):
        column_j = board[:, j]

        if np.count_nonzero(column_j) == 0:
            min_index_j = 0
        else: 
            min_index_j = column_j.shape[0] - np.argmax(column_j)

        max_height = max(max_height, min_index_j)

    return max_height

def compute_bumpiness(board):
    """
        Compute bumpiness of a given board

        The bumpiness measure how flat is the last layer of 
        the board. 

        For two adjacent columns, the relative bumpiness is the absolute value
        of the difference between the height of the columns. The total 
        bumpiness is the sum of all relative bumpiness and is therefor a
        positive integer

        Parameters
        ----------
            board: 2d array_like
                The tetris board filled with 1 (for a block) or 0
                for empty space
    """
    bumpiness = 0
    
    for j in range(0, board.shape[1] - 1):
        col_j  = np.transpose(np.array([board[:, j]]))
        col_jp = np.transpose(np.array([board[:, j + 1]]))

        columnj_height  = compute_height(col_j)
        columnjp_height = compute_height(col_jp)

        bumpiness += abs(columnj_height - columnjp_height)

    return bumpiness

def compute_sum_height(board):
    """
        Compute the sum of all columns heights

        Parameters
        ----------
            board: 2d array_like
                The tetris board
    """
    sumH = 0

    for j in range(0, board.shape[1]):
        for i in range(0, board.shape[0]):
            if board[i, j] == 1:
                sumH += board.shape[0] - i
                break

    return sumH