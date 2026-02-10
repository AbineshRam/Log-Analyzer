import time
from typing import Callable
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class ErrorLogHandler(FileSystemEventHandler):
    """
    Handles filesystem events.
    Triggers callback when an error log file is created.
    """

    def __init__(self, callback: Callable[[str], None]):
        self.callback = callback

    def on_created(self, event):
        if event.is_directory:
            return

        file_path = event.src_path.lower()

        # Only react to error logs
        if "error" in file_path or "stderr" in file_path:
            self.callback(event.src_path)


class FileWatcher:
    """
    Watches a directory for error log creation.
    """

    def __init__(self, path: str, on_error_log: Callable[[str], None]):
        self.path = path
        self.on_error_log = on_error_log
        self.observer = Observer()

    def start(self):
        event_handler = ErrorLogHandler(self.on_error_log)
        self.observer.schedule(event_handler, self.path, recursive=True)
        self.observer.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        self.observer.stop()
        self.observer.join()
