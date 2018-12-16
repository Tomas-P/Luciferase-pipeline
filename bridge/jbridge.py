import os
import subprocess
import glob
import jnius_config
os.environ['JAVA_HOME'] = subprocess.run(['/home/tomas/Fiji.app/ImageJ-linux64',
                                          "--print-java-home"],
                                         stdout=subprocess.PIPE).stdout.decode(
                                             ).strip()

jars = glob.glob("/home/tomas/Fiji.app/**/*.jar",recursive=True)
jnius_config.add_classpath(*jars)
import jnius
