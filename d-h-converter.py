import wfdb
import sys
import numpy
# numpy.set_printoptions(threshold=1500)

record = wfdb.rdsamp('./zapisi/x34') # В папке "zapisi" лежат 2 файла "aami3a.dat" и "aami3a.hea". Если одного нет, выполнение метода даст ошибку.
points = record[0] # Точки сигнала
properties = record[1] # Информация о сигнале (частота дискредитизации, длина сигнала, единица измерения)

print(points.tolist())
