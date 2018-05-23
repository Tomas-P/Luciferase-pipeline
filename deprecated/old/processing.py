import config
import folder
import imagej
import register

def process(folder_tag :str)->str:
    name = register.register(folder_tag)
    imagej.run('--run jython')
