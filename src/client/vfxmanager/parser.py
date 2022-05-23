from src.log import log, warn
from ast import literal_eval # eval is dangerous, little timmy. do not use eval, never, ever.

def parse(file):
    """
    Parse the entire file, and return the commands needed to go to the execution pipeline along
    the arguments.

    :: params ::

    file: SupportsRead - The file to read from

    :: returns ::
    commands: dict - The list of commands to give to the execution pipeline.
    """
    commands = []

    try:
        for line in file.readlines():
            if not line.startswith('!') and not line.isspace(): # ignore comments and emptylines.
                # what in the world? please god, forgive me.
                split_t1 = line.split('[')
                func_name = split_t1[0]
                args = split_t1[-1].split(']')[0].split(',')

                # refining args to remove left-over impurities like spaces and evaluate them into proper types.
                for arg in args:
                    if arg.startswith(' '):
                        args[args.index(arg)] = arg.split(' ')[1]
                    
                    if arg.isnumeric():
                        args[args.index(arg)] = int(arg)

                if args[0] != '\n': # ignore newline literal. 
                    commands.append(
                        (func_name, args)
                    )

    except Exception as exc:
        warn("An error occured whilst parsing the TUOFX file.", "Worker/TUOFXParser", exc)

    return commands