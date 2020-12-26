
import platform
from pathlib import Path
import os
import jnius_config

def prep_env():

    system = platform.system()

    if system == "Linux":
        path = Path(".") / "javadevkit" / "linux" / "jdk-15.0.1"
    elif system == "Windows":
        path = Path(".") / 'javadevkit' / 'windows' / 'jdk-15.0.1'
        os.environ['PATH'] += str(path / 'bin') + ';'
        os.environ['PATH'] += str(path / 'bin' / 'server') + ';'
        os.environ['PATH'] += str(path / 'lib') + ';'
    elif system == 'Darwin':
        raise Warning("This program has not been tested in MacOS")
        path = Path('.') / 'javadevkit' / 'osx' / 'jdk-15.0.1.jdk'
        path = path / 'Contents' / 'Home'
    else:
        raise Exception(f"{system} is not supported by this program")

    os.environ['JAVA_HOME'] = str(path.absolute())

def locate_jars():
    system = platform.system()
    if system == "Linux":
        subdir = "linux"
    elif system == "Windows":
        subdir = "windows"
    elif system == "Darwin":
        subdir = "mac"
    else:
        raise Exception(f"{system} is not supported by this program")
    ijfolder = Path('.').absolute() / 'imagej' / subdir / "Fiji.app"
    return [str(p) for p in ijfolder.glob("**/*.jar")]

def setup():
    prep_env()
    jars = locate_jars()
    jnius_config.add_classpath(*jars)


