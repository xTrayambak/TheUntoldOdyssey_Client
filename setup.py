from setuptools import setup

setup(
    name='theuntoldodyssey',
    options={
        'build_apps': {
            # Build asteroids.exe as a GUI application
            'gui_apps': {
                'theuntoldodyssey': 'main.py',
            },

            # Set up output logging, important for GUI apps!
            'log_filename': f'$USER_APPDATA/SyntaxStudios/TheUntoldOdyssey/debug.log',
            'log_append': False,

            # Specify which files are included with the distribution
            'include_patterns': [
                '**/*.png',
                '**/*.jpg',
                '**/*.egg',
                "**/*.flac",
                "**/*.json",
                "**/*.glsl",
                "**/*.obj",
                "**/*.gltf",
                "**/*.mp3",
                "**/*.glb",
                "**/*.ttf",
                "**/*.otf",
                "**/*.wav"
            ],

            # Include the OpenGL renderer and OpenAL audio plug-in
            'plugins': [
                'pandagl',
                'p3openal_audio',
            ],
        }
    }
)
