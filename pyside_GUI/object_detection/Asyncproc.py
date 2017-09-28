import os, fcntl, subprocess, threading, time
from PySide.QtGui import *
from PySide.QtCore import *

class AsyncProcessMonitor(QWidget):
    stdout = Signal(str)
    stderr = Signal(str)
    finished = Signal()
    def __init__(self, parent = None):
        super(AsyncProcessMonitor, self).__init__(parent = parent)
        self.thread = None
        self.process = None

    def closeEvent(self, e):
        if self.thread is not None: self.thread._Thread__stop()
        if self.process is not None: self.process.kill()
        e.accept()

    def Pstop(self):
        if self.thread is not None: 
            self.thread._Thread__stop()
            self.thread = None
        if self.process is not None:
            self.process.kill()
            self.process = None

    def Popen(self, args, bufsize=0, executable=None, stdin=None, stdout=None, stderr=None, preexec_fn=None, close_fds=False, shell=False, cwd=None, env=None, universal_newlines=False, startupinfo=None, creationflags=0, sleep = None):
        def runInThread():
            def monitor(stdout,stderr):
                while True:
                    if stdout:
                        output = non_block_read(stdout).strip()
                        if output: self.stdout.emit(output)
                    if stderr:
                        output = non_block_read(stderr).strip()
                        if output: self.stderr.emit(output)
                    if sleep is not None:
                        time.sleep(sleep)
                    if self.process.poll() is not None: 
                        self.finished.emit()
                        break
            def non_block_read(output):
                fd = output.fileno()
                fl = fcntl.fcntl(fd, fcntl.F_GETFL)
                fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)
                try:
                    return output.read()
                except:
                    return ''     
            self.process = subprocess.Popen(args, bufsize=bufsize, executable=executable, stdin=stdin, stdout=stdout, stderr=stderr, preexec_fn=preexec_fn, close_fds=close_fds, shell=shell, cwd=cwd, env=env, universal_newlines=universal_newlines, startupinfo=startupinfo, creationflags=creationflags)
            thread = threading.Thread(target = monitor, args = [self.process.stdout, self.process.stderr])
            thread.daemon = True
            thread.start()        
            self.process.wait()
            thread.join(timeout = 1)
        self.thread = threading.Thread(target = runInThread)
        self.thread.start()
