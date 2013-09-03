import copy


class SudokuBoard(object):

  def __init__(self, square_size):
    self.square_size = square_size
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
    for i in xrange(0, self.board_size):
      print self.board[i]


class SudokuBoardHelper(object):

  def __init__(self, board):
    self.board = board.copy()
    self.board_size = board.get_size()
    self.empty_cells = self.board_size * self.board_size
    self.helements = [{k for k in xrange(1, self.board_size + 1)} for i in xrange(0, self.board_size)]
    self.velements = [{k for k in xrange(1, self.board_size + 1)} for i in xrange(0, self.board_size)]
    self.selements = [{k for k in xrange(1, self.board_size + 1)} for i in xrange(0, self.board_size)]
    self._fill_available_elements()

  def _fill_available_elements(self):
    for row in xrange(0, self.board_size):
      for col in xrange(0, self.board_size):
        if not self.board.is_empty(row, col):
          value = self.board.get_cell(row, col)
          self.set_cell(row, col, value, initialization=True)

  def _get_square_index(self, row, col):
    row, col = row // 3, col // 3
    return row * 3 + col

  def set_cell(self, row, col, value, initialization=False):
    if not self.board.is_empty(row, col) and not initialization:
      return False
    self.board.set_cell(row, col, value)
    self.helements[row].discard(value)
    self.velements[col].discard(value)
    self.selements[self._get_square_index(row, col)].discard(value)
    self.empty_cells -= 1
    return True

  def unset_cell(self, row, col, value):
    if self.board.is_empty(row, col):
      return False
    self.board.unset_cell(row, col)
    self.helements[row].add(value)
    self.velements[col].add(value)
    self.selements[self._get_square_index(row, col)].add(value)
    self.empty_cells += 1
    return True

  def get_next_cell(self):
    row, col, cnt = -1, -1, -1
    for r in xrange(0, self.board_size):
      for c in xrange(0, self.board_size):
        if not self.board.is_empty(r, c):
          continue
        elements = self.get_cell_available_elements(r, c)
        if cnt == -1 or len(elements) < cnt:
          row, col, cnt = r, c, len(elements)
    return row, col

  def get_cell_available_elements(self, row, col):
    hset = self.helements[row]
    vset = self.velements[col]
    sset = self.selements[self._get_square_index(row, col)]
    return hset & vset & sset

  def is_complete(self):
    return self.empty_cells == 0

  def get_board(self):
    return self.board.copy()


class SudokuSolver(object):

  def __init__(self, board):
    self.helper = SudokuBoardHelper(board)

  def solve(self):
    if self.helper.is_complete():
      return self.helper.get_board()
    row, col = self.helper.get_next_cell()
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
