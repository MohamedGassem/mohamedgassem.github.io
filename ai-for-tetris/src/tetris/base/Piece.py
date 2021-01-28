import numpy as np


class Piece:
    """
        Class that handles Tetris pieces logic

        A 'piece' is a collection of two dimensional array. The rotation is
        emulated by changing an index within that array. This construction
        allows very flexible mechanics.
    """

    def __init__(self, *states):
        """
            Constructor

            Parameters
            ----------
                states: list of 2D array_like
                    List of the piece states
        """
        assert (len(states) > 0)
        self._states = []

        for state_data in states:
            self._states.append(np.asarray(state_data))

        self._current_state = 0

    def get_current_state(self):
        """
            Return the current state data of the piece

            Returns
            -------
                array_like
                    The current state data of the piece
        """
        return self._states[self._current_state]

    def rotate(self, direction, perform):
        """
            Return the rotated piece state data

            See also
            --------
                rotate_left
                rotate_right

            Parameters
            ----------
                direction: int
                    The direction (positive / negative) and the magnitude
                    (absolute value) of the rotation
                perform: bool
                    When true, perform the rotation on the calling piece.

            Returns
            -------
                array_like
                    The rotated state data of the piece
        """
        next_state = self._current_state + direction
        next_state %= len(self._states)

        if perform:
            self._current_state = next_state

        return self._states[next_state]

    def rotate_left(self, perform=False):
        """
            Return the left-rotated piece state data

            See also
            --------
                rotate
                rotate_right

            Parameters
            ----------
                perform: bool
                    When true, perform the rotation on the calling piece.

            Returns
            -------
                The rotated state data of the piece
        """
        return self.rotate(-1, perform)

    def rotate_right(self, perform=False):
        """
            Return the right-rotated piece state data

            See also
            --------
                rotate
                rotate_left

            Parameters
            ----------
                perform: bool
                    When true, perform the rotation on the calling piece.

            Returns
            -------
                array_like
                    The rotated state data of the piece
        """
        return self.rotate(+1, perform)

    def compute_current_bounds(self):
        """
            Returns the smallest array that contains all non zero elements

            This piece construction allows flexible mechanisms one of which is
            moving rotation axis. For positions to remain coherent the bounding
            box must be known.

            Returns
            -------
                tuple of 4 int, 2D-array_like
                    The first element is the bounding box of the smallest matrix
                    containing all elements, the second is the matrix itself
        """
        # Create variable so they can be used outside their loops
        i, j, k, l = 0, 0, 0, 0

        array = self._states[self._current_state]
        shape = array.shape

        for i in range(shape[1]):
            non_zero = np.count_nonzero(array[:, i])

            if non_zero != 0:
                break

        for j in reversed(range(shape[1])):
            non_zero = np.count_nonzero(array[:, j])

            if non_zero != 0:
                break

        for k in range(shape[0]):
            non_zero = np.count_nonzero(array[k, :])

            if non_zero != 0:
                break

        for l in reversed(range(shape[0])):
            non_zero = np.count_nonzero(array[l, :])

            if non_zero != 0:
                break

        return (k, l, i, j), array[k:(l + 1), i:(j + 1)]
