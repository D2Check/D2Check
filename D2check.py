from os import listdir
from os.path import isfile, join
import psutil
import hashlib
import sys

# Get a process list
psutil.process_iter(attrs=None, ad_value=None)

# for each process in the process list
found = 0
for proc in psutil.process_iter():

    # Try to do the following things
    try:
        # Get process name & pid from process object.
        processName = proc.name()
        processID = proc.pid
        print("Searching for d2 process")
        # If the process name is "Game.exe" we have found diablo 2 running
        if processName == "Game.exe":
            print("D2 process found")
            found += 1
            if found >= 2:

                # Protect against previously opening 2 or more d2 games
                fout = open("log.txt", "w")
                fout.close()
                sys.exit()
            # Open a log file
            fout = open("log.txt", "w")

            # Set the attributes of the running process in order to get the path of the game currently running
            path = proc.__dict__
            # make it readable
            path = str(path['_proc'].exe())[0:-8]
            # print(path)
            # print(processName, ' ::: ', processID)

            #get the files in the path of the running process
            onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]

            # print(onlyfiles)

            # for each of the files in the directory
            for file in onlyfiles:
                # we only want USEFUL files
                if file.endswith("mpq") or file.endswith("dll") or file.endswith("exe"):
                    # make a new sha256 hash object
                    hasher = hashlib.sha256()
                    with open(path + file, 'rb') as afile:
                        buf = afile.read()

                        #update the hash object with the binary representation of the file
                        hasher.update(buf)
                    # prepare a line of content to exfil to the logfile
                    line = "{}\t\t{}\n".format(hasher.hexdigest(),file[0:-4])

                    # write that line
                    fout.write(line)
                # close the output file
            fout.close()
        else:
            continue

    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        pass
print("Done! Show log.txt")