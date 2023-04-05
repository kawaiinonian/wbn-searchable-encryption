import ctypes as c

class c_user:
    def __init__(self, sopath) -> None:
        self.lib = c.cdll.LoadLibrary(sopath)

    def updateData_generate(self, skey, DOC):
        pass
