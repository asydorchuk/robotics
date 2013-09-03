import unittest

from sudoku_solver import SudokuBoard
from sudoku_solver import SudokuBoardHelper
from sudoku_solver import SudokuSolver

class TestSudokuBoard(unittest.TestCase):

  def setUp(self):
    self.board = SudokuBoard(3);

  def testOperations(self):
    self.assertEqual(9, self.board.get_size())

    self.board.set_cell(8, 8, 1)
    self.assertEqual(1, self.board.get_cell(8, 8))
    self.assertFalse(self.board.is_empty(8, 8))

    self.board.unset_cell(8, 8)
    self.assertEqual(0, self.board.get_cell(8, 8))
    self.assertTrue(self.board.is_empty(8, 8))

    board = self.board.copy();
    board.set_cell(0, 0, 1)
    self.assertEqual(1, board.get_cell(0, 0))
    self.assertEqual(0, self.board.get_cell(0, 0))


class TestSudokuBoardHelper(unittest.TestCase):
  VALID_BOARD = (
      (1, 2, 3, 4, 5, 6, 7, 8, 9),
      (4, 5, 6, 7, 8, 9, 1, 2, 3),
      (7, 8, 9, 1, 2, 3, 4, 5, 6),
      (2, 3, 4, 5, 6, 7, 8, 9, 1),
      (5, 6, 7, 8, 9, 1, 2, 3, 4),
      (8, 9, 1, 2, 3, 4, 5, 6, 7),
      (3, 4, 5, 6, 7, 8, 9, 1, 2),
      (6, 7, 8, 9, 1, 2, 3, 4, 5),
      (9, 1, 2, 3, 4, 5, 6, 7, 8),
    )

  def setUp(self):
    board = SudokuBoard(3)
    self.helper = SudokuBoardHelper(board)

  def test_operation(self):
    self.assertEqual({e for e in xrange(1, 10)}, self.helper.get_cell_available_elements(0, 0))

    self.helper.set_cell(0, 0, 1)
    self.assertEqual({e for e in xrange(2, 10)}, self.helper.get_cell_available_elements(0, 0))
    self.assertEqual({e for e in xrange(2, 10)}, self.helper.get_cell_available_elements(0, 8))
    self.assertEqual({e for e in xrange(2, 10)}, self.helper.get_cell_available_elements(8, 0))
    self.assertEqual({e for e in xrange(2, 10)}, self.helper.get_cell_available_elements(2, 2))
    self.assertEqual({e for e in xrange(1, 10)}, self.helper.get_cell_available_elements(8, 8))

    row, col = self.helper.get_next_cell()
    self.assertEqual(0, row)
    self.assertEqual(1, col)

    self.helper.unset_cell(0, 0, 1)
    self.assertEqual({e for e in xrange(1, 10)}, self.helper.get_cell_available_elements(0, 0))
    self.assertEqual({e for e in xrange(1, 10)}, self.helper.get_cell_available_elements(0, 8))
    self.assertEqual({e for e in xrange(1, 10)}, self.helper.get_cell_available_elements(8, 0))
    self.assertEqual({e for e in xrange(1, 10)}, self.helper.get_cell_available_elements(2, 2))
    self.assertEqual({e for e in xrange(1, 10)}, self.helper.get_cell_available_elements(8, 8))

  def test_sequential_coverage(self):
    for r in xrange(0, 9):
      for c in xrange(0, 9):
        self.helper.set_cell(r, c, self.VALID_BOARD[r][c])

  def test_best_cell_coverage(self):
    for i in xrange(0, 81):
      r, c = self.helper.get_next_cell()
      self.helper.set_cell(r, c, self.VALID_BOARD[r][c])


class TestSudokuSolver(unittest.TestCase):

  def get_board_from_grid(self, grid):
    board = SudokuBoard(3)
    for r in xrange(0, 9):
      for c in xrange(0, 9):
        board.set_cell(r, c, grid[r][c])
    return board

  def get_grid_from_board(self, board):
    return tuple(tuple(board.get_cell(r, c) for c in xrange(0, 9)) for r in xrange(0, 9))

  def is_valid_board(self, board):
    return True

  def test_solver_empty_board(self):
    board = SudokuBoard(3)
    solver = SudokuSolver(board)
    solution_board = solver.solve()

  def test_solver_example_easy1(self):
    grid = (
      (0, 2, 3, 4, 5, 6, 7, 8, 9),
      (4, 0, 6, 7, 8, 9, 1, 2, 3),
      (7, 8, 0, 1, 2, 3, 4, 5, 6),
      (2, 3, 4, 0, 6, 7, 8, 9, 1),
      (5, 6, 7, 8, 0, 1, 2, 3, 4),
      (8, 9, 1, 2, 3, 0, 5, 6, 7),
      (3, 4, 5, 6, 7, 8, 0, 1, 2),
      (6, 7, 8, 9, 1, 2, 3, 0, 5),
      (9, 1, 2, 3, 4, 5, 6, 7, 0),
    )
    board = self.get_board_from_grid(grid)
    solver = SudokuSolver(board)
    solution_board = solver.solve()
    self.assertTrue(1, solution_board.get_cell(0, 0))
    self.assertTrue(5, solution_board.get_cell(1, 1))
    self.assertTrue(9, solution_board.get_cell(2, 2))
    self.assertTrue(5, solution_board.get_cell(3, 3))
    self.assertTrue(9, solution_board.get_cell(4, 4))
    self.assertTrue(4, solution_board.get_cell(5, 5))
    self.assertTrue(9, solution_board.get_cell(6, 6))
    self.assertTrue(4, solution_board.get_cell(7, 7))
    self.assertTrue(8, solution_board.get_cell(8, 8))

  def test_solver_example_easy2(self):
    grid = (
      (0, 0, 3, 0, 2, 0, 6, 0, 0),
      (9, 0, 0, 3, 0, 5, 0, 0, 1),
      (0, 0, 1, 8, 0, 6, 4, 0, 0),
      (0, 0, 8, 1, 0, 2, 9, 0, 0),
      (7, 0, 0, 0, 0, 0, 0, 0, 8),
      (0, 0, 6, 7, 0, 8, 2, 0, 0),
      (0, 0, 2, 6, 0, 9, 5, 0, 0),
      (8, 0, 0, 2, 0, 3, 0, 0, 9),
      (0, 0, 5, 0, 1, 0, 3, 0, 0),
    )
    solution_grid = (
      (4, 8, 3, 9, 2, 1, 6, 5, 7),
      (9, 6, 7, 3, 4, 5, 8, 2, 1),
      (2, 5, 1, 8, 7, 6, 4, 9, 3),
      (5, 4, 8, 1, 3, 2, 9, 7, 6),
      (7, 2, 9, 5, 6, 4, 1, 3, 8),
      (1, 3, 6, 7, 9, 8, 2, 4, 5),
      (3, 7, 2, 6, 8, 9, 5, 1, 4),
      (8, 1, 4, 2, 5, 3, 7, 6, 9),
      (6, 9, 5, 4, 1, 7, 3, 8, 2),
    )
    board = self.get_board_from_grid(grid)
    solver = SudokuSolver(board)
    solution_board = solver.solve()
    self.assertEqual(solution_grid, self.get_grid_from_board(solution_board))

  def test_solver_example_hard1(self):
    grid = (
      (8, 5, 0, 0, 0, 2, 4, 0, 0),
      (7, 2, 0, 0, 0, 0, 0, 0, 9),
      (0, 0, 4, 0, 0, 0, 0, 0, 0),
      (0, 0, 0, 1, 0, 7, 0, 0, 2),
      (3, 0, 5, 0, 0, 0, 9, 0, 0),
      (0, 4, 0, 0, 0, 0, 0, 0, 0),
      (0, 0, 0, 0, 8, 0, 0, 7, 0),
      (0, 1, 7, 0, 0, 0, 0, 0, 0),
      (0, 0, 0, 0, 3, 6, 0, 4, 0),
    )
    solution_grid = (
      (8, 5, 9, 6, 1, 2, 4, 3, 7),
      (7, 2, 3, 8, 5, 4, 1, 6, 9),
      (1, 6, 4, 3, 7, 9, 5, 2, 8),
      (9, 8, 6, 1, 4, 7, 3, 5, 2),
      (3, 7, 5, 2, 6, 8, 9, 1, 4),
      (2, 4, 1, 5, 9, 3, 7, 8, 6),
      (4, 3, 2, 9, 8, 1, 6, 7, 5),
      (6, 1, 7, 4, 2, 5, 8, 9, 3),
      (5, 9, 8, 7, 3, 6, 2, 4, 1),
    )
    board = self.get_board_from_grid(grid)
    solver = SudokuSolver(board)
    solution_board = solver.solve()
    self.assertEqual(solution_grid, self.get_grid_from_board(solution_board))

  def test_solver_example_hard2(self):
    grid = (
      (0, 0, 5, 3, 0, 0, 0, 0, 0),
      (8, 0, 0, 0, 0, 0, 0, 2, 0),
      (0, 7, 0, 0, 1, 0, 5, 0, 0),
      (4, 0, 0, 0, 0, 5, 3, 0, 0),
      (0, 1, 0, 0, 7, 0, 0, 0, 6),
      (0, 0, 3, 2, 0, 0, 0, 8, 0),
      (0, 6, 0, 5, 0, 0, 0, 0, 9),
      (0, 0, 4, 0, 0, 0, 0, 3, 0),
      (0, 0, 0, 0, 0, 9, 7, 0, 0),
    )
    solution_grid = (
      (1, 4, 5, 3, 2, 7, 6, 9, 8),
      (8, 3, 9, 6, 5, 4, 1, 2, 7),
      (6, 7, 2, 9, 1, 8, 5, 4, 3),
      (4, 9, 6, 1, 8, 5, 3, 7, 2),
      (2, 1, 8, 4, 7, 3, 9, 5, 6),
      (7, 5, 3, 2, 9, 6, 4, 8, 1),
      (3, 6, 7, 5, 4, 2, 8, 1, 9),
      (9, 8, 4, 7, 6, 1, 2, 3, 5),
      (5, 2, 1, 8, 3, 9, 7, 6, 4),
    )
    board = self.get_board_from_grid(grid)
    solver = SudokuSolver(board)
    solution_board = solver.solve()
    self.assertEqual(solution_grid, self.get_grid_from_board(solution_board))

  def test_solver_example_hard3(self):
    grid = (
      (0, 0, 0, 0, 0, 5, 0, 8, 0),
      (0, 0, 0, 6, 0, 1, 0, 4, 3),
      (0, 0, 0, 0, 0, 0, 0, 0, 0),
      (0, 1, 0, 5, 0, 0, 0, 0, 0),
      (0, 0, 0, 1, 0, 6, 0, 0, 0),
      (3, 0, 0, 0, 0, 0, 0, 0, 5),
      (5, 3, 0, 0, 0, 0, 0, 6, 1),
      (0, 0, 0, 0, 0, 0, 0, 0, 4),
      (0, 0, 0, 0, 0, 0, 0, 0, 0),
    )
    # solution_grid = (
    #   (1, 4, 5, 3, 2, 7, 6, 9, 8),
    #   (8, 3, 9, 6, 5, 4, 1, 2, 7),
    #   (6, 7, 2, 9, 1, 8, 5, 4, 3),
    #   (4, 9, 6, 1, 8, 5, 3, 7, 2),
    #   (2, 1, 8, 4, 7, 3, 9, 5, 6),
    #   (7, 5, 3, 2, 9, 6, 4, 8, 1),
    #   (3, 6, 7, 5, 4, 2, 8, 1, 9),
    #   (9, 8, 4, 7, 6, 1, 2, 3, 5),
    #   (5, 2, 1, 8, 3, 9, 7, 6, 4),
    # )
    #board = self.get_board_from_grid(grid)
    #solver = SudokuSolver(board)
    #solution_board = solver.solve()
    #self.assertEqual(solution_grid, self.get_grid_from_board(solution_board))

if __name__ == '__main__':
  unittest.main()
