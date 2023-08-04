# Install HPCC & NLP Plugin

## Windows & WSL

These are instructions on how to install the HPCC Platform with the NLP Plugin on WSL and use it with the NLP++ Language Extension for VSCode.

### Clone dehilster-analyzers

- Open up Powershell
- connect to the folder where you want to clone the de Hilster analyzers
- Type: "`git clone https://github.com/visualtext/dehilster-analyzers`"
- Open the "HPCC" folder in VSCode

### Create and Launch HPCC Server 

- Open up Powershell
- Type: "`wsl --install -d Ubuntu`" (if you want to reset your WSL to start fresh, type in "`wsl --unregister Ubuntu`")
- Enter in your username and password
- Type: "`sudo su -`" and enter your password
- Type: "`wget http://visualtext.org/downloads/hpccnlp.sh`"
- Type: "`sh hpccnlp.sh`" and wait until complete (it can take in between 1 and 2 minutes)

### Add Data File to Server

- Open in a brower: "`127.0.0.1:8010`"
- Click on the "Files" icon on the left icons panel
- Click on "Landing Zones"
- Click on "Upload" and find the file DOJArticles.xml under the directory "dehilster-analyzers/HPCC/analyzers/Entities/input"
- Click on "Upload"
- Select the file "DOJArticles.xml" in the Landing Zones area that has now appeared
- Click on "Import: ... XML"
- Type "doj::articles" in the "Target Scope" field and choose "UTF-8" in the Format field
- Click on "Import"

### Run the ECL Code

- Open VSCode
- Install the ECL and NLP++ Extensions by searching for ECL and NLP
- Open the folder "dehilster-analyzers/HPCC/" in VSCode
- Clock on the "NLP++" Icon in the left-hand vertical bar
- Click on the file "entities.ecl" file in the ANALZYERS list under
- Right click on "entities.ecl" and choose "Generate HPCC Manifest File"
- Click on the "entities.ecl" and click on the run button in the top right corner of the editing window
- Wait for the processing to finish to see the results in the HPCC vertical panel at the bottom
