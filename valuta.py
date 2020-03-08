import requests
import pyodbc
import datetime
from tkinter import *
import copy

# Доллар США используем в качестве базовой валюты
# и конвертируем валюту из списка

print('\n')

conn = pyodbc.connect(
        "DRIVER={SQL Server Native Client 11.0};"
        "Server=PASHOK-ПК\SQLEXPRESS;"
        "Database=Primer;"
        "Trusted_Connection=yes;"
    )
# Создание новой локальной базы (rates), куда закидываем валюту, курс, отметку времени

cursor = conn.cursor()
cursor.execute('drop table rates')
cursor.execute('create table rates (val varchar(7), znach float(2), date datetime)')
conn.commit()


# Вытаскиваем из http - запроса данные типа byteб перводим их в тип словарь
#и сохраняем в локалбную базу rates

CurrenyCode = []
response = requests.get('https://api.exchangeratesapi.io/latest?base=USD')
rates = response.json()
for key in rates['rates']:
    print (key, "{0:.2f}" .format(rates['rates'][key]))
    CurrenyCode.append(key)
    cursor.execute('insert into rates(val,znach,date) values(?,?,?);', (key, rates['rates'][key], datetime.datetime.now().strftime("%d-%m-%Y %H:%M")))
    conn.commit()


# Графическая часть. Отрисовка форм ввода

root = Tk()
root.configure(background='lavender')
root.geometry("400x250")


def clear_all() :
    Amount1_field.delete(0, END)

    Amount2_field.delete(0, END)

# Процедура в которой происходит вывод конвертирования относительно USD валюты по
#условию (если временная отметка меньше 600 сек(10 мин), то значение берем из базы,
# если больше 10 мин, то значение берем с сайта и сохранем его в базе rates)

def CurrencyConversion():
    valuta = variable2.get()
    cursor = conn.cursor()
    cursor.execute("select * from rates where val = ?", valuta)
    for row in cursor:
        print(datetime.datetime.now())
        print(row.date)
        s = datetime.datetime.now() - row.date
        if s.seconds <= 50:
            print('Kruto ' + str(s.seconds))
            print(Amount1_field.get())
            print(row.znach)
            raschet = row.znach * int(Amount1_field.get())
            z =("{0:.2f}".format(raschet))
            Amount2_field.delete(0, END)
            Amount2_field.insert(0, str(z))
        else:
            print(valuta)
            response = requests.get('https://api.exchangeratesapi.io/latest?base=USD&symbols=' + valuta)
            rates = response.json()
            print(rates)
            for key in rates['rates']:
                print(key, "{0:.2f}".format(rates['rates'][key]))
                znach = "{0:.2f}".format(rates['rates'][key])
                print(response.json())
                cursor = conn.cursor()
                cursor.execute('update rates set znach = ?, date = ? where val= ?;',(znach, datetime.datetime.now().strftime("%d-%m-%Y %H:%M"), valuta))
                conn.commit()
                raschet = row.znach * int(Amount1_field.get())
                z = ("{0:.2f}".format(raschet))
                Amount2_field.delete(0, END)
                Amount2_field.insert(0, str(z))

variable1 = StringVar(root)

variable2 = StringVar(root)

# инициализировать переменные

variable1.set("currency")

variable2.set("currency")


headlabel = Label(root, text='Currency Convertor', fg='black', bg="dodgerblue")

label1 = Label(root, text="Amount :", fg='black', bg='slategrey')

# Создайте ярлык "Из валюты:"

label2 = Label(root, text="From Currency", fg='black', bg='slategrey')

# Создать ярлык «To Currency:»

label3 = Label(root, text="To Currency :", fg='black', bg='slategrey')

# Создайте ярлык "Конвертированная сумма:"

label4 = Label(root, text="Converted Amount :", fg='black', bg='slategrey')

headlabel.grid(row=0, column=1)

label1.grid(row=1, column=0)

label2.grid(row=2, column=0)

label3.grid(row=3, column=0)

label4.grid(row=5, column=0)

Amount1_field = Entry(root)

Amount2_field = Entry(root)

# ipadx Аргумент ключевого слова устанавливает ширину пространства ввода.

Amount2_field.insert(0, str(''))

Amount1_field.grid(row=1, column=1, ipadx="25")

Amount2_field.grid(row=5, column=1, ipadx="25")


CurrenyCode_list = copy.deepcopy(CurrenyCode)

# создать выпадающее меню с помощью функции OptionMenu

# который принимает имя окна, переменную и выбор как

# Аргумент. используйте * перед названием списка,

# распаковать значения

FromCurrency_option = OptionMenu(root, variable1, 'USD')

ToCurrency_option = OptionMenu(root, variable2, *CurrenyCode_list)



FromCurrency_option.grid(row=2, column=1, ipadx=10)

ToCurrency_option.grid(row=3, column=1, ipadx=10)



# Создайте кнопку конвертации и прикрепите



button1 = Button(root, text="Convert", bg="darkkhaki", fg="black", command = CurrencyConversion)

button1.grid(row=4, column=1)

# Создайте кнопку Очистить и прикрепите

# с функцией удаления

button2 = Button(root, text="Clear", bg="darkkhaki", fg="black", command=clear_all)

button2.grid(row=6, column=1)

#list()

root.mainloop()
conn.close()

