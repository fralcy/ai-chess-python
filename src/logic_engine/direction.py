class Direction():
  def __init__(self, row_delta, column_delta):
    self.row_delta = row_delta
    self.column_delta = column_delta

  @property
  def row_delta(self):
    return self._row_delta
  
  @property
  def column_delta(self):
    return self._column_delta
  
  @row_delta.setter
  def row_delta(self, value):
    self._row_delta = value

  @column_delta.setter
  def column_delta(self, value):
    self._column_delta = value

  def __add__(self, other):
    return Direction(self.row_delta + other.row_delta,
                      self.column_delta + other.column_delta)
  
  def __mul__(self, scalar):
    return Direction(self.row_delta * scalar,
                      self.column_delta * scalar)
  
  def __rmul__(self, scalar):
    return self.__mul__(scalar)
  
Direction.NORTH = Direction(-1, 0)
Direction.SOUTH = Direction(1, 0)
Direction.WEST = Direction(0, -1)
Direction.EAST = Direction(0, 1)
Direction.NORTH_WEST = Direction.NORTH + Direction.WEST
Direction.NORTH_EAST = Direction.NORTH + Direction.EAST
Direction.SOUTH_WEST = Direction.SOUTH + Direction.WEST
Direction.SOUTH_EAST = Direction.SOUTH + Direction.EAST