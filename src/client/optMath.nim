import nimpy
import std/math

# Optimized math functions for Python. Yay.
proc vector2DLength(x: float32, y: float32): float32 {.exportpy.} =
  sqrt(x ^ 2 + y ^ 2)

proc vector3DLength(x: float32, y: float32, z: float32): float32 {.exportpy.} =
  sqrt(x ^ 2 + y ^ 2 + z ^ 2)

proc vector3DMagnitude(vectorX1: float32, vectorY1: float32, vectorZ1: float32,
                       vectorX2: float32, vectorY2: float32, vectorZ2: float32): float32 {.exportpy.} =
  sqrt(
    (vectorX1 - vectorX2) ^ 2 +
    (vectorY1 - vectorY2) ^ 2 +
    (vectorZ1 - vectorZ2) ^ 2
  )

proc vector2DMagnitude(vectorX1: float32, vectorY1: float32,
                       vectorX2: float32, vectorY2: float32): float32 {.exportpy.} =
  sqrt(
    (vectorX1 - vectorX2) ^ 2 +
    (vectorY1 - vectorY2) ^ 2
  )

proc lcm(x: int, y: int): int {.exportpy.} =
  var greater = 0
  var lcmValue = 0

  if x > y:
    greater = x
  else:
    greater = y

  while (true):
    if ((greater mod x == 0) and (greater mod y == 0)):
      lcmValue = greater
      break

    inc greater

  lcmValue
