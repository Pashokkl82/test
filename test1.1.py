# Сортируем имена и сохраняем их в списке sep_str_file. Выгружаем в файл -
# sortedfile.txt (для наглядности)

infile = open('D:\Test\\names.txt', 'r')
outfile = open('sortedfile.txt', 'w')
str_file = infile.read()
sep_str_file = str_file.split(',')
sep_str_file.sort()
outfile.write(str(sep_str_file))

# Подсчитываем сумму порядковых букв имен и сохраняем их в первом значении словаря dict

dict = {}
for elem in sep_str_file:
    dict[elem] = ['','']
for key in dict:
    sum = 0
    for i in key:
        if i != '"':
            sum = sum + (ord(i) - 64)
            dict[key][0] = sum
    print(key + ' ' + str(dict[key][0]))

print('\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n')

# Записываем в словарь dict вторым значением произвидение порядкового номера(который находится
# в первом значении словаря dict) на алфавитную сумму имени.

for i in range(len(sep_str_file)):
    dict[sep_str_file[i]][1] = dict[sep_str_file[i]][0] * (i+1)
    print(sep_str_file[i] + ' ' + str(dict[sep_str_file[i]][1]))

# Суммируем произведения из пункта 3, которые сохранены во втором значении словаря dict
SUMMA = 0
for key in dict:
    SUMMA += dict[key][1]
print('SUMMA = ' + str(SUMMA))

infile.close()
outfile.close()
