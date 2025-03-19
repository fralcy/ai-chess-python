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
  
  def __add__(self, other):
    return Direction(self.row_delta + other.row_delta,
                      self.column_delta + other.column_delta)
  
  def __mul__(self, scalar):
    return Direction(self.row_delta * scalar,
                      self.column_delta * scalar)
  
  def __rmul__(self, scalar):
    return self.__mul__(scalar)
  
Direction.North = Direction(-1, 0)
Direction.South = Direction(1, 0)
Direction.West = Direction(0, -1)
Direction.East = Direction(0, 1)
Direction.NorthWest = Direction.North + Direction.West
Direction.NorthEast = Direction.North + Direction.East
Direction.SouthWest = Direction.South + Direction.West
Direction.SouthEast = Direction.South + Direction.East