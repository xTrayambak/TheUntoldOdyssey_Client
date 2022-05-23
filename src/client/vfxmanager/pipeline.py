"""
VFXPipeline

Executes the instruction given by the parser to Panda3D.
"""
import uuid

from src.log import log, warn
from src.client.vfxmanager.lang import COMMANDS

from direct.task import Task

class Pipeline:
    """
    The TUOFX execution pipeline.
    """
    def __init__(self, instance):
        self.call_history = []
        self.tuo = instance

    def pipeline_activity_task(self, args):
        """
        The activity task for a TUOFX file.

        :: params ::
        args@tuple - The entirity of the raw arguments (including functions and WAIT/NO_WAIT state)
        """
        args = list(args)
        cmd_name = args[0]
        args.pop(0)
        wait_condition = args[0]
        args.pop(0)
        task_id = args[-1]
        args.pop(-1)

        if wait_condition.lower() == 'wait' and len(self.call_history) > 0:
            return Task.cont
      
        for order in args:
            real_args = order
            cmd_name_to_func = COMMANDS[cmd_name.lower()]
            cmd_name_to_func['command'](self.tuo, *real_args)

        self.call_history.remove({'task_id': task_id})
        return Task.done
    
    def execute(self, command_list: list):
        """
        Execute a list of commands the TUOFX parser provided us.
        """
        task_id = str(uuid.uuid4())
        history_call_report = {'task_id': task_id}
        command_list.append(task_id)

        log(command_list, 'cmd_list')
        self.tuo.spawnNewTask(task_id, self.pipeline_activity_task, args=command_list)

        self.call_history.append(history_call_report)