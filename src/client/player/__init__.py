from panda3d.core import Vec3
from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from direct.showbase.DirectObject import *
from direct.task import Task

def limit( val, minVal, maxVal ):
  return max( minVal, min( val, maxVal ) )

from direct.interval.IntervalGlobal import *

from pandac.PandaModules import Trackball

globalClock = None

# a 3th person camera, which looks at the self.cameraLookatNode
class Player(DirectObject):
  def __init__(self, instance):
    camera = instance.camera
    # disable default mouse movements
    instance.disableMouse()
    
    # create a fixed 45 degree view angle
    camera.setP(-60)
    camera.setPos(-25,-25,50)
    
    self.camTask = instance.spawnNewTask("camLoop", self.camLoop)
    self.instance = instance
    
    self.cameraLookatNode = instance.render.attachNewNode('cameraLookatNode')
    self.cameraLookatNode.setH(-45)
    self.cameraPositionNode = self.cameraLookatNode.attachNewNode('cameraPositionNode')
    self.cameraPositionNode.setPos(Vec3( 0, -15, 0 ))

    # update task of view angle
    instance.spawnNewTask("cameraRotationTask", self.cameraRotationTask, -1)
    
    
    self.keyMap = dict()
    keybindings = { "arrow_left"  : "rotate_left"
                  , "arrow_right" : "rotate_right"
                  , "arrow_up"    : "move_forward"
                  , "arrow_down"  : "move_backward" }
    
    for key, bind in keybindings.items():
      self.accept( key, self.setKey, [bind,1])
      self.accept( key+"-up", self.setKey, [bind,0])
      self.keyMap[bind] = 0
    
    self.keyCalls = { "rotate_left"   : self.turn_left
                    , "rotate_right"  : self.turn_right
                    , "move_forward"  : self.move_forward
                    , "move_backward" : self.move_backward }
    
    instance.spawnNewTask("camera_key_handler", self.handleKey)
  
  #Records the state of the arrow keys
  def setKey( self, key, value ):
    self.keyMap[key] = value
  
  def handleKey( self, task ):
    for key, value in self.keyCalls.items():
      if self.keyMap[key]:
        value()
    return Task.again
  
  def cameraRotationTask(self, task):
    lookAtPos = self.cameraLookatNode.getPos(self.instance.render)
    relPos = self.cameraPositionNode.getPos()
    v = relPos.getY()
    self.cameraLookatNode.setP( v * 1.3 )
    pos = self.cameraPositionNode.getPos(self.instance.render)
    # look at the positition
    self.instance.cam.setPos(pos)
    self.instance.cam.lookAt(lookAtPos)
    return Task.cont
  
  def camLoop(self, task):
    """ move the camera if the mouse touches the edges of the screen
    """
    if not self.instance.mouseWatcherNode.hasMouse():
        return Task.cont
    
    timer = globalClock.getDt()
    
    mpos = base.mouseWatcherNode.getMouse()
    mousePosX = mpos.getX()
    mousePosY = mpos.getY()
    
    if mousePosX > 0.9:
      self.move_left( timer )
      
    if mousePosX < -0.9:
      self.move_right( timer )
    
    if mousePosY > 0.9:
      self.move_forward( timer )
    
    if mousePosY < -0.9:
      self.move_backward( timer )
    
    return Task.cont
  
  def turn_left(self):
    self.cameraLookatNode.setH( self.cameraLookatNode.getH() - 5 )

  def turn_right(self):
    self.cameraLookatNode.setH( self.cameraLookatNode.getH() + 5 )
  
  def move_forward( self, timer=1.0/30 ):
    multiplier = self.cameraPositionNode.getPos().getY() * timer / 2.0
    diffPos = camera.getPos( render ) - self.cameraLookatNode.getPos( render )
    diffPos.normalize()
    self.cameraLookatNode.setX( self.cameraLookatNode.getX() + diffPos.getX() * multiplier )
    self.cameraLookatNode.setY( self.cameraLookatNode.getY() + diffPos.getY() * multiplier )
    self.limit_movement()
  
  def move_backward( self, timer=1.0/30 ):
    multiplier = self.cameraPositionNode.getPos().getY() * timer / 2.0
    diffPos = camera.getPos( render ) - self.cameraLookatNode.getPos( render )
    diffPos.normalize()
    self.cameraLookatNode.setX( self.cameraLookatNode.getX() - diffPos.getX() * multiplier )
    self.cameraLookatNode.setY( self.cameraLookatNode.getY() - diffPos.getY() * multiplier )
    self.limit_movement()
  
  def move_left( self, timer=1.0/30 ):
    multiplier = self.cameraPositionNode.getPos().getY() * timer / 2.0
    diffPos = camera.getPos( render ) - self.cameraLookatNode.getPos( render )
    diffPos.normalize()
    self.cameraLookatNode.setX( self.cameraLookatNode.getX() + diffPos.getY() * multiplier )
    self.cameraLookatNode.setY( self.cameraLookatNode.getY() - diffPos.getX() * multiplier )
    self.limit_movement()
  
  def move_right( self, timer=1.0/30 ):
    multiplier = self.cameraPositionNode.getPos().getY() * timer / 2.0
    diffPos = camera.getPos( render ) - self.cameraLookatNode.getPos( render )
    diffPos.normalize()
    self.cameraLookatNode.setX( self.cameraLookatNode.getX() - diffPos.getY() * multiplier )
    self.cameraLookatNode.setY( self.cameraLookatNode.getY() + diffPos.getX() * multiplier )
    self.limit_movement()
  
  def limit_movement( self ):
    # limit position of camera look-at position
    self.cameraLookatNode.setX( limit( self.cameraLookatNode.getX(), 0, 86 ) )
    self.cameraLookatNode.setY( limit( self.cameraLookatNode.getY(), 0, 86 ) )
    pos = self.cameraLookatNode.getPos(render)
    pos = [pos[0], pos[1], pos[2]]