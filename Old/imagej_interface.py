import lucbase
from subprocess import run, PIPE
import re

def shell(prog):
    return run(prog,stdout=PIPE,shell=True)

def ijline(imagej:lucbase.Folder,commands,headless=False)->str:
    "create an imagej command-line macro based on the information provided."
    if headless:
        return ' '.join([imagej.locate_filetype('.exe')[0].replace('/','\\'),
                 '--headless','-eval "{0}"'.format(' '.join(commands))])
    else:
        return ' '.join([imagej.locate_filetype('.exe')[0].replace('/','\\'),
                 '-eval "{0}"'.format(' '.join(commands))])

def to_newlines(imagej_line):
    '''Convert a command-line macro created by ijline to a normal one
with the intent to write it to a file.'''
    macro = re.findall('".*"',imagej_line)[0] # get the imagej macro commands
    macro = macro.replace('; ',';\n')
    macro = macro.strip('"')
    return macro

def write_macro(macro, filename):
    "Write macro to filename."
    with open(filename, 'w') as file:
        file.write(macro)

def run_macro(filename, imagej_folder):
    "Run the file as an imagej macro"
    com = "cd {0} && {1} -macro {2}".format(
        imagej_folder.foldername,
        imagej_folder.locate_filetype('.exe')[0],
        filename
        )
    shell(com)

if __name__ == '__main__':
    # checking to make sure the file works
    # spoiler: it does
    config = lucbase.Config()
    imagej = lucbase.Folder(config[lucbase.IMAGEJ])
    line_1 = ijline(imagej,["print('hello world!');"])
    print(line_1)
    shell(line_1)
    for file in imagej.files:
        if file.endswith('/macros'):
            break
    line2 = to_newlines(line_1)
    write_macro(line2, file + '/hello.ijm')
    run_macro(file+'/hello.ijm',imagej)
