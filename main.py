from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger

import psutil
import os
import time

@register("Start_NapCat", "AstralGuardian", "automatically start NapCat", "1.0.0", "repo url")
class MyPlugin(Star):
    def __init__(self, context: Context, config:dict):
        super().__init__(context)
        self.config = config
        self.bat_path = config.get("bat_path","")
        self.bat_name = self.bat_path
        self.file_path = os.path.dirname(self.bat_name)
        if not self.bat_path:
            logger.error("input Absolute path of NapCat 'launcher.bat' first")
        else:
            self.Run_NapCat()
    
    def is_NapCat_running(self):
        for process in psutil.process_iter(["pid", "name", "cmdline"]):
            try:
                if isinstance(process.info["cmdline"], list):
                    if self.bat_name in process.info["cmdline"]:
                        return True
            except(psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return False
    
    def Run_NapCat(self):
        if not self.is_NapCat_running():
            os.system(f'start cmd /c "cd {self.file_path} && {self.bat_path}"')
            time.sleep(2)
            for i in range(10):
                if self.is_NapCat_running():
                    logger.debug("successfully run NapCat")
                    return
                time.sleep(1)
            logger.error("fail to run NapCat")
        else:
            logger.debug("has already run NapCat")



