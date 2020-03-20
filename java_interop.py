
import glob
import platform
from pathlib import Path
import os
import jnius_config as jconf

def prep_env():
    # set JAVA_HOME and PATH so that jnius can be used
    system = platform.system()
    if system == "Linux":
        os.environ["JAVA_HOME"] = "/usr/lib/jvm/default-java"
    elif system == "Windows":
        jhome = glob.glob(r"C:\Program Files\Java\jdk-*")[0]
        os.environ["JAVA_HOME"] = jhome
        os.environ["PATH"] += jhome + r"\bin;" + jhome + r"\bin\server;"
        os.environ["PATH"] += jhome + r"\lib;"
    elif system == "Darwin":
        raise Exception("MacOS support is not currently included")
    elif system == "Java":
        raise Exception("This program is not suitable for use in Jython")
    else:
        raise Exception(f"{system} is not supported by this program")

def locate_jars() -> list:
    # find the jar files of Fiji/ImageJ. They will let us give ImageJ commands.
    home = Path("~").expanduser()
    ijfolder = next(home.glob("**/Fiji.app"))
    alljars = [str(p) for p in ijfolder.glob("**/*.jar")]
    return alljars

def setup():
    prep_env()
    jars = locate_jars()
    jconf.add_classpath(*locate_jars())
