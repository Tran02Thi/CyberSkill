#!/bin/bash
for pdf_file in *.pdf;
	do
                folder="${pdf_file%.pdf}"

		mkdir -p "$folder" 

		pdftotext "$pdf_path" temp.txt

		tr -c '[:alpha:]' '[\n*]' < temp.txt | grep '^[a-zA-Z]\+$' | sort -u | while read -r word; 
			do
				echo "$word" > "$folder/$word.txt"
			done

		rm temp.txt
	done


