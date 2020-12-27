
$pyurl = "https://www.python.org/ftp/python/3.8.7/python-3.8.7-amd64.exe"
$installer = "$HOME\Downloads\python-3.8.7-amd64.exe"

$wc = New-Object System.Net.WebClient
$wc.DownloadFile($pyurl, $installer)

cd $HOME\Downloads
.\python-3.8.7-amd64.exe /quiet InstallAllUsers=1 PrependPath=1

cd $HOME

if (!(Test-Path $HOME\Luciferase-Pipeline)) {
	mkdir $HOME\Luciferase-Pipeline
}

cd $HOME\Luciferase-Pipeline

$pipelineurl = "https://github.com/Tomas-P/Luciferase-pipeline/archive/master.zip"
$source = "$(pwd)\master.zip"
$wc.DownloadFile($pipelineurl, $source)
Expand-Archive -LiteralPath $source -DestinationPath $(pwd) 

$javaurl = "https://download.java.net/java/GA/jdk15.0.1/51f4f36ad4ef43e39d0dfdbaf6549e32/9/GPL/openjdk-15.0.1_windows-x64_bin.zip"
$java = "$(pwd)\openjdk.zip"
$wc.DownloadFile($javaurl, $java)
Expand-Archive $java -DestinationPath $(pwd)

$fijiurl = "https://downloads.imagej.net/fiji/latest/fiji-win64.zip"
$fiji = "$(pwd)\fiji-win64.zip"
$wc.DownloadFile($fijiurl, $fiji)
Expand-Archive $fiji -DestinationPath $(pwd)

Move-Item .\Luciferase-pipeline-master\* .
Remove-Item Luciferase-pipeline-master

py -3 -m venv .

.\Scripts\Activate.ps1

pip3 install -r requirements.txt

deactivate