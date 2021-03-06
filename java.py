
import platform
from pathlib import Path
import os
import jnius_config

def prep_env():

    system = platform.system()

    if system == "Linux":
        path = Path(".") / "jdk-15.0.1"
    elif system == "Windows":
        path = Path(".") / 'jdk-15.0.1'
        os.environ['PATH'] += str(path / 'bin') + ';'
        os.environ['PATH'] += str(path / 'bin' / 'server') + ';'
        os.environ['PATH'] += str(path / 'lib') + ';'
    elif system == 'Darwin':
        raise Warning("This program has not been tested in MacOS")
        path = Path('.') / 'jdk-15.0.1.jdk'
        path = path / 'Contents' / 'Home'
    else:
        raise Exception(f"{system} is not supported by this program")

    os.environ['JAVA_HOME'] = str(path.absolute())

def locate_jars():
    ijfolder = Path('.').absolute() / "Fiji.app"
    return [str(p) for p in ijfolder.glob("**/*.jar")]

def setup():
    prep_env()
    jars = locate_jars()
    jnius_config.add_classpath(*jars)


