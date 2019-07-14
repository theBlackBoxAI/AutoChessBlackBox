import sys

class Logger(object):
    def __init__(self, file_name):
        self.terminal = sys.stdout
        self.file_name = file_name

    def write(self, message):
        self.terminal.write(message)
        self.log = open(self.file_name, 'a')
        self.log.write(message)
        self.log.close()

    def flush(self):
        #this flush method is needed for python 3 compatibility.
        #this handles the flush command by doing nothing.
        #you might want to specify some extra behavior here.
        pass
