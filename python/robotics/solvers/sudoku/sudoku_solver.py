import copy


class SudokuBoard(object):

  def __init__(self, square_size):
    self.board_size = square_size * square_size
    self.board = [[0 for j in xrange(0, self.board_size)] for i in xrange(0, self.board_size)]

  def get_size(self):
    return self.board_size

  def set_cell(self, row, col, value):
    self.board[row][col] = value

  def unset_cell(self, row, col):
    self.board[row][col] = 0

  def get_cell(self, row, col):
    return self.board[row][col]

  def is_empty(self, row, col):
    return self.board[row][col] == 0

  def copy(self):
    return copy.deepcopy(self)

  def output(self):
    for row in self.board:
      print row


class SudokuBoardHelper(object):

  def __init__(self, board):
    self.board = board.copy()
    self.helements = [{k for k in xrange(1, board.get_size() + 1)} for i in xrange(0, board.get_size())]
    self.velements = [{k for k in xrange(1, board.get_size() + 1)} for i in xrange(0, board.get_size())]
    self.selements = [{k for k in xrange(1, board.get_size() + 1)} for i in xrange(0, board.get_size())]
    for row in xrange(0, board.get_size()):
      for col in xrange(0, board.get_size()):
        if not self.board.is_empty(row, col):
          value = self.board.get_cell(row, col)
          self.set_cell(row, col, value, initialization=True)

  def set_cell(self, row, col, value, initialization=False):
    assert (self.board.is_empty(row, col) or initialization)
    self.board.set_cell(row, col, value)
    self.helements[row].discard(value)
    self.velements[col].discard(value)
    self.selements[row // 3 * 3 + col // 3].discard(value)

  def unset_cell(self, row, col, value):
    assert not self.board.is_empty(row, col)
    self.board.unset_cell(row, col)
    self.helements[row].add(value)
    self.velements[col].add(value)
    self.selements[row // 3 * 3 + col // 3].add(value)

  def get_next_cell(self):
    row, col, cnt = -1, -1, -1
    for r in xrange(0, self.board.get_size()):
      for c in xrange(0, self.board.get_size()):
        if self.board.is_empty(r, c):
          elements = self.get_cell_available_elements(r, c)
          if cnt == -1 or len(elements) < cnt:
            row, col, cnt = r, c, len(elements)
    return row, col

  def get_cell_available_elements(self, row, col):
    return self.helements[row] & self.velements[col] & self.selements[row // 3 * 3 + col // 3]

  def get_board(self):
    return self.board.copy()


class SudokuSolver(object):

  def __init__(self, board):
    self.helper = SudokuBoardHelper(board)

  def solve(self):
    row, col = self.helper.get_next_cell()
    if row == -1 and col == -1:
      return self.helper.get_board()
    elements = self.helper.get_cell_available_elements(row, col)
    if len(elements) == 0:
      return None
    for element in elements:
      self.helper.set_cell(row, col, element)
      solution_board = self.solve()
      if solution_board is not None:
        return solution_board
      self.helper.unset_cell(row, col, element)
    return None
