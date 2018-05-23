REM skip the header
GOTO script
REM This script is supposed to make installing the dependencies earlier.
REM I have not tested it.
REM So run it with care.
:script
pip install numpy
pip install pandas
pip install matplotlib
GOTO end
REM goto end skips the footer.
REM numpy is a dependency of pandas, so it has to be installed firsth.
REM The installs are listed in the way I installed them on my machine.
:end