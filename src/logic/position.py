class Position():
  def __init__(self, row, column):
    self.row = row
    self.column = column

  @property
  def row(self):
    return self._row
  
  @property
  def column(self):
    return self._column
  
  def square_color(self):
    """Return the color of the square."""
    from logic.player import Player
    if (self.row + self.column) % 2 == 0:
      return Player.WHITE
    else:
      return Player.BLACK
  
  def __eq__(self, other):
    return self.row == other.row and self.column == other.column
  
  def __hash__(self):
    """Return the hash of the position."""
    return hash((self.row, self.column))
  
  def __ne__(self, value):
    return not self == value
  
  def __add__(self, direction):
    return Position(self.row + direction.row_delta,
                    self.column + direction.column_delta)