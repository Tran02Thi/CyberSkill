#!/bin/bash

set -e

VERSION_APP=1.0
STACK_NAME=lemp

# FOLDER_NAME="$1"

# if [ $# -eq 0 ]; then
# 	echo "Vui lòng cho biết tên folder"
# else
# 	if [ ! -d "$FOLDER_NAME" ]; then
# 	echo "Không tồn tại thư mục"
# 	fi
# fi


# if ls "$FOLDER_NAME"/*.pdf 1> /dev/null 2>&1; then
# 	for pdf_file in "$FOLDER_NAME"/*.pdf;
# 	     do
# 		folder="${pdf_file%.pdf}"

# 		mkdir -p "$folder"
# 		pdftotext "$pdf_file" temp.txt

# 		tr -c '[:alpha:]' '[\n*]' < temp.txt | grep '^[a-zA-Z]\+$' | sort -u | while read -r word;
# 			do
# 				echo "$word" > "$folder/$word.txt"
# 			done
# 		rm temp.txt
#              done
# else
# 	echo "Không có file PDF nào trong thư mục '$FOLDER_NAME'."
# fi

# Build NodeJs 
sudo docker build --rm -t app:$VERSION_APP ./monitoring/backend/ || exit 1

docker stack rm $STACK_NAME

echo "Build docker stack ..."

cd monitoring

sudo docker stack deploy -c docker-compose.yml $STACK_NAME

sudo docker ps

echo "Docker containers are up and running!"



