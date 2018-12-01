import numpy as np
import math

class Position(object):
  """docstring for Position"""
  def __init__(self, x, y, z):
    super(Position, self).__init__()
    self.x = x
    self.y = y
    self.z = z

  def __add__(self, other):
    if type(other) is Position:
      result = Position(self.x + other.x,
        self.y + other.y,
        self.z + other.z)
      return result
    raise ValueError("This is not a Position")

  def __sub__(self, other):
    if type(other) is Position:
      result = Position(self.x - other.x,
        self.y - other.y,
        self.z - other.z)
      return result
    raise ValueError("This is not a valid operation")

  def getMatrix(self):
    result = np.matrix([
      [self.x],
      [self.y],
      [self.z]])
    return result

class Rotation(object):
  """docstring for Rotation"""
  def __init__(self, w ,x ,y ,z):
    super(Rotation, self).__init__()
    norm = x**2 + y**2 + z**2 + w**2
    self.w = w/norm
    self.x = x/norm
    self.y = y/norm
    self.z = z/norm

  def getMatrix(self):
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
    if type is Position:
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
    elif type is Rotation:
      result = Rotation(
        self.w*other.w - self.x*other.x - self.y*other.y - self.z*other.z,
        self.w*other.x + self.x*other.w - self.y*other.z + self.z*other.y,
        self.w*other.y + self.x*other.z + self.y*other.w - self.z*other.x,
        self.w*other.z - self.x*other.y + self.y*other.x + self.z*other.w)
      return result
    raise ValueError("This is not a valid operation")

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

  def getRotation(self):
    return self.rotation

  def getTranslation(self):
    return self.translation

  def getMatrix(self):
    result = np.matrix([
      [1,0,0,0],
      [0,1,0,0],
      [0,0,1,0],
      [0,0,0,1]])
    result[0:3,0:3] = self.orientation.getMatrix()
    result[0:3,3] = self.translation.getMatrix()
    return result