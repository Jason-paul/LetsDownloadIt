#!/bin/bash
# Muhammad Momin
# Jason

# this script gets the input for the url and the choice (video, audio, or history)
# calls the downloadfile.py with information provided.

echo "      ********** LetsDownloadIt **********"
echo "Current user: `whoami`       Current time: `date`"
currentPath=`pwd`

askForClose() {
  read -p "You wanna continue y/n: " c
    if [[ $c =~ [yYnN] ]]; then
        if [[ $c =~ [nN] ]]; then
            start=false
        fi
    else
        echo "Please usee only y or n"
        askForClose
    fi
}

getChoice(){
    echo "What do you want to do? "
    choices=("video" "audio" "history" "SeeDownloads")
    select choice in ${choices[@]}
    do
        if [[ "$choice" ]]; then 
            if [[ $choice = "history" ]]; then
                python downloadfile.py " " ${choice:0:1}
                break
            elif [[ $choice = "SeeDownloads" ]]; then
                cd ./downloads
                ls
                break
            else
                read -p "Please enter a video url: " url
                python downloadfile.py $url ${choice:0:1}
                break
            fi
        else
            echo "Invalid choice"
            getChoice
            break
        fi
    done
}

start = true
while $start; do
    # get the user input
    getChoice
    # go back to prev path if path changed *needed for database
    newPath=`pwd`
    if [[ $newPath != $currentPath ]]; then
        echo "Going back to previous directory"
        cd -
    fi
    database="DownloadHistory.db"
    # check if there exists a database
    if [ -f "$database" ]
    then
    # give the ownership of DownloadHistory.db to current user
    chown `whoami` $database
    # Change the permissions of DownloadHistory.db
    chmod u=rw,g=r,o=r $database
    fi 
    # ask if the user wants to exit the program
    askForClose
done