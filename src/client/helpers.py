import sys

from src.client.savefile import Savefile
from src.log import log, warn
from src.client.ui.text import Text

from direct.gui.DirectGui import DirectScrolledFrame, DGG

def mainmenu_worldcreate_screen_001(name, instance):
    import limeade; limeade.refresh()

    instance.workspace.get_component('ui', 'world_name_input').hide()
    # input sanitisation or else the game will crash :D
    if len(name) < 1 or '/' in name:
        instance.workspace.get_component('ui', 'status_text').node().setText('Invalid world name!')
        return
            
    if sys.platform == 'linux':
        if len(name) > 4096 or name.startswith('..'): # .. is a trailing backslash, makes sense.
            instance.workspace.get_component('ui', 'status_text').node().setText('Invalid world name!')
            return


    # i either love microsoft, or i despise microsoft sometimes. CAN YOU LEAVE LEGACIES OF THE PAST AWAY? SERIOUSLY? CON IS A REAL NAME, BILLY WILLY THE 3RD!
    if sys.platform in ('win32', 'win64'):
        if len(name) > 256 or name.lower() in ('CON', 'PRN', 'AUX', 'NUL', 'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9', 'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9', 'NUL', 'NULL'):
            instance.workspace.get_component('ui', 'status_text').node().setText('Invalid world name!')
            return

    instance.workspace.get_component('ui', 'status_text').node().setText(instance.translator.translate('singleplayer_menu_createworld', 'create_savefile'))
    instance.workspace.get_component('ui', 'connecting_screen_backbtn').hide()

    savefile = Savefile(instance, name)
    savefile.add_new_file('game')
    savefile.add_new_file('player')

    instance.workspace.get_component('ui', 'status_text').node().setText(instance.translator.translate('singleplayer_menu_createworld', 'gamedata_savefile'))
    savefile.write_data('game', 'entities', {})
    savefile.write_data('game', 'time', 0.0)
    savefile.write_data('game', 'advancements', [])
            
    instance.workspace.get_component('ui', 'status_text').node().setText(instance.translator.translate('singleplayer_menu_createworld', 'playerdata_savefile'))
    savefile.write_data('player', 'health', 20.0),
    savefile.write_data('player', 'potion_effects', [])
    savefile.write_data('player', 'position', [0, 0, 0])
    savefile.write_data('player', 'progression_stage', 0)
    savefile.write_data('player', 'name', name)

    instance.workspace.get_component('ui', 'status_text').node().setText(instance.translator.translate('singleplayer_menu_createworld', 'firstsave_savefile'))

    savefile.write_data_to_disk()

    instance.workspace.get_component('ui', 'status_text').node().setText(instance.translator.translate('singleplayer_menu_createworld', 'simulation_savefile'))

def mainmenu_worldlist(tuo, wlist):
    font001 = tuo.fontLoader.load('gentium_basic')

    tuo.set_title(f'The Untold Odyssey {tuo.version} | Savefile Menu')

    header_text = Text(tuo, font001, 'World List', 0.1, (0, 0, 1))
    world_frame = DirectScrolledFrame(canvasSize=(-8, 8, -8, 8), frameSize=(-1, 1, -1, 1))

    world_frame.addoptions('hi', {'name': 'turi', 'default': None, 'function': None})

    tuo.workspace.add_ui('header_text_world_select', header_text)
    tuo.workspace.add_ui('world_list_frame', world_frame)
