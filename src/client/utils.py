from panda3d.core import Vec4, Texture, CardMaker, NodePath, LVecBase3

def tuple_conv_vec3(value: tuple):
    if len(value) > 2: return None
    if isinstance(value, LVecBase3f): return value 

    return LVecBase3f(value[0], value[1])

def load_image_as_plane(tuo, path: str, yres: int = 64):
    """
    Load up an image as a 3D plane.

    (Adapted from here: https://discourse.panda3d.org/t/loadimageasplane/10557)

    :: args ::
    path: str -- the path to the image
    yres: int -- the vertical resolution of the image (defaults to 64)
    """
    texture = tuo.texture_loader.load_texture(path)
    texture.setBorderColor(Vec4(0, 0, 0, 0))
    texture.setWrapU(Texture.WMBorderColor)
    texture.setWrapV(Texture.WMBorderColor)

    cm = CardMaker(path + '--card')
    cm.setFrame(-texture.getOrigFileXSize(), texture.getOrigFileXSize(), -texture.getOrigFileYSize(), texture.getOrigFileYSize())

    card_node = NodePath(cm.generate())
    card_node.setTexture(texture)
    card_node.setScale(card_node.getScale() / yres)
    card_node.flattenLight()

    return card_node
