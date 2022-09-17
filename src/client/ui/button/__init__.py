from direct.gui import DirectGuiGlobals as DGG
from direct.gui.DirectButton import DirectButton

from src.client.utils import load_image_as_plane, tuple_conv_vec3

class Button:
    def __init__(self, instance, text: str, scale: float = 0.1, text_scale: float = 0.1, pos = (0, 0, 0), command = None, text_font = None, parent = None, hover_text: str = "button.play.hover", click_text: str = "button.play.click", overlay_img: str = None, geom = None) -> None:
        import limeade; limeade.refresh()
        self.text = text
        def command_extra():
            if len(click_text) >= 1:
                instance.narrator.say(click_text)

            if command != None: command()

        if geom == None and overlay_img == None:
            # I for the love of God, cannot make this stupid text either fit into the box properly or resize the box. Gosh I would rather be working a minimum wage job at McDonalds than this.

            div_factor = (256 + len(text) / 1.1) + len(text) / 4
            geom = load_image_as_plane(instance, 'assets/img/button_template.png', div_factor)

        self.click_text = click_text
        self.hover_text = hover_text

        self.direct = DirectButton(
            text = text,
            text_scale = text_scale,
            pos = pos,
            command = command_extra,
            text_font = text_font,
            parent = parent,
            image = overlay_img,
            relief = None,
            geom = geom
        )
        self.instance = instance

        self.direct.bind(DGG.ENTER, self.on_hover)

    def destroy(self):
        """
        Destroy this UI object.
        """
        self.direct.destroy()

    def set_text(self, text: str):
        """
        Set the text of this UI object.
        """
        self.text = text
        self.direct.setText(text)

    def setText(self, text: str):
        """
        This is to be deprecated soon as per the refactoring.
        """
        return self.set_text(text=text)

    def hide(self):
        self.direct.hide()

    def show(self):
        self.direct.show()

    def on_hover(self, args) -> None:
        if len(self.hover_text) == 0: return
        self.instance.narrator.say(self.hover_text)
