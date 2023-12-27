from manager import HistoTreeManager

debug = False
save_crash = False
manager = HistoTreeManager()

try:
    manager.start()
    manager.save_auto_save()
except:
    if debug:
        pass  # Debug Checkpoint
    if save_crash:
        manager.save_crash()
    raise
