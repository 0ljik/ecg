import wfdb

record = wfdb.rdsamp('./zapisi/x34') # В папке "zapisi" лежат 2 файла "aami3a.dat" и "aami3a.hea". Если одного нет, выполнение метода даст ошибку.
points = record[0] # Точки сигнала
properties = record[1] # Информация о сигнале (частота дискредитизации, длина сигнала, единица измерения)

print(record)
