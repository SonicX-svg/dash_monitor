#!/bin/bash

# Указываем имя входного файла и выходного файла
INPUT_FILE="iostat_output.csv"
OUTPUT_FILE="iostat_cleaned.csv"

# Записываем заголовок в выходной файл
head -n 1 "$INPUT_FILE" > "$OUTPUT_FILE"

# Удаляем строки, где поле kB_wrtn пустое и добавляем их в выходной файл
awk -F, 'NR > 1 { if ($8 != "") print }' "$INPUT_FILE" >> "$OUTPUT_FILE"

