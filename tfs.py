import numpy as np
import math

class Position(object):
  """docstring for Position"""
  def __init__(self):
    super(Position, self).__init__()

  def setCoordinates(self,x,y,z):
    self.x = x
    self.y = y
    self.z = z

  def __add__(self, other):
    if type(other) is Position:
      result = Position(self.x + other.x,
        self.y + other.y,
        self.z + other.z)
      return result
    raise ValueError("This is not a valid operation - Position")

  def __sub__(self, other):
    if type(other) is Position:
      result = Position(self.x - other.x,
        self.y - other.y,
        self.z - other.z)
      return result
    raise ValueError("This is not a valid operation - Position")

  def toMatrix(self):
    result = np.matrix([
      [self.x],
      [self.y],
      [self.z]])
    return result

  def __str__(self):
    return "[" + "x=" + str(self.x) + "," + "y=" + str(self.y) + "," + "z=" + str(self.z) + "]"

class Vector(Position):
  """docstring for Vector"""
  def __init__(self):
    super(Vector, self).__init__()

class Rotation(object):
  """docstring for Rotation"""
  def __init__(self):
    super(Rotation, self).__init__()

  def fromQuaternion(self, w, x, y ,z):
    norm = x**2 + y**2 + z**2 + w**2
    self.w = w/norm
    self.x = x/norm
    self.y = y/norm
    self.z = z/norm

  def fromRotMatrix(self, matrix):
    self.w= math.sqrt(1 + matrix[0,0] + matrix[1,1] + matrix[2,2]) /2
    self.x = (matrix[2,1] - matrix[1,2])/(4 *self.w)
    self.y = (matrix[0,2] - matrix[2,0])/(4 *self.w)
    self.z = (matrix[1,0] - matrix[0,1])/(4 *self.w)

  def toRotMatrix(self):
    result = np.matrix([
      [1 - 2*self.y**2 - 2*self.z**2,
        2*self.x*self.y - 2*self.z*self.w,
        2*self.x*self.z + 2*self.y*self.w],
      [2*self.x*self.y + 2*self.z*self.w,
        1 - 2*self.x**2 - 2*self.z**2,
        2*self.y*self.z - 2*self.x*self.w],
      [2*self.x*self.z - 2*self.y*self.w,
      2*self.y*self.z + 2*self.x*self.w,
      1 - 2*self.x**2 - 2*self.y**2]])
    return result

  def __mul__(self, other):
    if type(other) is Position:
      result = Position(
        (1 - 2*self.y**2 - 2*self.z**2)*other.x +
          (2*self.x*self.y - 2*self.z*self.w)*other.y +
          (2*self.x*self.z + 2*self.y*self.w)*other.z,
        (2*self.x*self.y + 2*self.z*self.w)*other.x +
          (1 - 2*self.x**2 - 2*self.z**2)*other.y +
          (2*self.y*self.z - 2*self.x*self.w)*other.z,
        (2*self.x*self.z - 2*self.y*self.w)*other.x +
          (2*self.y*self.z + 2*self.x*self.w)*other.y +
          (1 - 2*self.x**2 - 2*self.y**2)*other.z)
      return result
    elif type(other) is Rotation:
      result = Rotation(
        self.w*other.w - self.x*other.x - self.y*other.y - self.z*other.z,
        self.w*other.x + self.x*other.w - self.y*other.z + self.z*other.y,
        self.w*other.y + self.x*other.z + self.y*other.w - self.z*other.x,
        self.w*other.z - self.x*other.y + self.y*other.x + self.z*other.w)
      return result
    raise ValueError("This is not a valid operation - Rotation")

  def __str__(self):
    return "[" + "w=" + str(self.w) + "," + "x=" + str(self.x) + "," + "y=" + str(self.y) + "," + "z=" + str(self.z) + "]"

class Transform(object):
  """docstring for Transform"""
  def __init__(self, rotation, translation):
    super(Transform, self).__init__()
    self.translation = translation
    self.rotation = rotation

  def __mul__(self, other):
    if other is Transform:
      result = Transform(
        self.orientation * other.orientation,
        self.orientation * other.translation + self.translation)
      return result
    raise ValueError("This is not a valid operation")

  def toRotation(self):
    return self.rotation

  def toTranslation(self):
    return self.translation

  def toMatrix(self):
    result = np.matrix([
      [1,0,0,0],
      [0,1,0,0],
      [0,0,1,0],
      [0,0,0,1]])
    result[0:3,0:3] = self.orientation.getMatrix()
    result[0:3,3] = self.translation.getMatrix()
    return result