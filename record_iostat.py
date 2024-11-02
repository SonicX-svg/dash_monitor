import subprocess
import csv
import time

# Запуск команды iostat
process = subprocess.Popen(['iostat', '-x', '1'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

with open('iostat_output.csv', 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(['Device', 'tps', 'kB_read/s', 'kB_wrtn/s', 'kB_read', 'kB_wrtn'])  # Заголовки

    for _ in range(10):  # Собирать данные 10 раз
        time.sleep(1)  # Задержка в 1 секунду
        output = process.stdout.readline().decode('utf-8').strip()
        if output and 'Device' not in output and 'tps' not in output:
            # Пропускаем строки заголовков
            data = output.split()
            csv_writer.writerow(data[:6])  # Пишем первые 6 значений в файл

process.terminate()

