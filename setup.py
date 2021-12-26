from setuptools import setup

VER = open("VER", "r").readlines()[0]

setup(
    name=f'The Untold Odyssey {VER}',
    options={
        'build_apps': {
            'gui_apps': {
                'asteroids': 'main.py',
            },

            # Set up output logging, important for GUI apps!
            'log_filename': '$USER_APPDATA/Asteroids/output.log',
            'log_append': False,

            # Specify which files are included with the distribution
            'include_patterns': [
                '**/*.png',
                '**/*.jpg',
                '**/*.egg',
                '**/*.flac',
                '**/*.mp3',
                '**/*.obj',
                '**/*.ttf',
                '**/*.rtf',
                '**/*',
                '**/*.prc',
                '**/*.json',
                '**/*.glsl',
                '**/*.wav'
            ],

            # Include the OpenGL renderer and OpenAL audio plug-in
            # Includes p3assimp to load more than just .bam models.
            'plugins': [
                'pandagl',
                'p3openal_audio',
                'pandagles',
                'pandagles2',
                'pandadx9',
                'p3assimp'
            ]
        }
    }
)