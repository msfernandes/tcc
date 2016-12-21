import sys
import os
import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
DEVNULL = open(os.devnull, 'wb')


class MyHandler(PatternMatchingEventHandler):
    patterns = ["*.tex", "*.bib"]

    def process(self, event):
        """
        event.event_type
            'modified' | 'created' | 'moved' | 'deleted'
        event.is_directory
            True | False
        event.src_path
            path/to/observed/file
        """
        # the file will be processed there
        print event.src_path, event.event_type  # print now only for degug

    def compile_tex(self):
        subprocess.call(['make', 'pre-build'])
        subprocess.call(['make'])
        subprocess.call(['make', 'clean'])

    def on_modified(self, event):
        self.process(event)
        self.compile_tex()

    def on_created(self, event):
        self.process(event)
        self.compile_tex()

if __name__ == '__main__':
    args = sys.argv[1:]
    observer = Observer()
    observer.schedule(MyHandler(), path=args[0] if args else '.',
                      recursive=True)
    observer.start()

    print("Watching .tex and .bib files...")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
