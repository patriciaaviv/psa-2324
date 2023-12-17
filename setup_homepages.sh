#!/bin/bash

filepath="/home/patricia/create_user_homepages"
template="$filepath/template"



users=("schoe" "steph" "pahll" "frisc" "zette" "klaku" "dietr" "tongu" "haugs" "stoec" "wittm" "grote" "deike" "meuse" "schub" "wothg" "songl" "horva" "kastl")

for user in "${users[@]}"; do

    # directories need to be accessible by the webserver
    sudo chmod +rx "/home/$user"
    sudo mkdir "/home/$user/.html-data"
    sudo mkdir "/home/$user/.cgi-bin"
    sudo chmod +rx "/home/$user/.html-data"
    sudo chmod +rx "/home/$user/.cgi-bin"

    # create html for user homepage
    # sed subtitutes USERNAME in the html file with actual name
    user_html="/home/$user/.html-data/index.html"
    sudo sed "s/USERNAME/$user/g" "$template" | sudo tee "$user_html" > /dev/null

    # create dynamic content
    user_script="/home/$user/.cgi-bin/print_time.py"
    sudo cp "$filepath/print_time.py" "$user_script"

    # permissions. Scripts will be executed by the owner set here!
    sudo chown $user:$user "/home/$user/.cgi-bin/"
    sudo chown $user:$user "/home/$user/.html-data/"
    sudo chown $user:$user $user_html
    sudo chown $user:$user $user_script
    sudo chmod 755 "$user_script"

done
