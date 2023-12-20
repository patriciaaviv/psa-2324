users=("schoe" "steph" "pahll" "frisc" "zette" "klaku" "dietr" "tongu" "haugs" "prinz" "stoec" "wittm" "grote" "deike" "meuse" "schub" "wothg" "songl" "horva" "kastl")
# fallen: "chris" "yesse"

# this includes fallen users, in case their accounts still remain on current machine
# apparently bash passes by value so og users is safe?
users_to_delete=${users[@]}
users_to_delete+=("chris" "yesse")
