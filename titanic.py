import pandas as pd
from scipy import stats as st
import numpy as np

def percentage(perc, whole):
  """
  рассчет доли
  """
  return str(round((perc * 100) / whole))+'%'

def get_number_of_pass(sex, data = None):
  """
  Какое количество мужчин и женщин ехало на параходе? 
  Приведите два числа через пробел
  """
  sexratio = data.value_counts() #data['название поля'].value_counts - возвращает количество вхождений 

  if sex == 'male':
    return sexratio['male']
  else:
    return sexratio['female']
    
def get_number_of_ports(port, data = None):
  """
  Подсчитайте сколько пассажиров загрузилось на борт в различных портах?
  """
  port_int = data.value_counts()

  if port == 'C':
    return port_int['C']
  if port == 'Q':
    return port_int['Q']
  if port == 'S':
    return port_int['S']


def get_number_of_died(data = None):
  """
  Посчитайте долю погибших на параходе (число и процент)
  """
  survived = data.value_counts()
  died_int = survived[0]
  surv_int = survived[1]
  return str(died_int) +' ,доля которых = '+ percentage(died_int, died_int+surv_int)

def get_pass_classes(data = None):
  """
  Какие доли составляли пассажиры первого, второго, третьего класса?
  """
  Pclass = data.value_counts()
  class_1 = Pclass[1]
  class_2 = Pclass[2]
  class_3 = Pclass[3]
  return '\n1-' + percentage(class_1, class_1+class_2+class_3) + '\n2-' + percentage(class_2, class_1+class_2+class_3) + '\n3-'+ percentage(class_3, class_1+class_2+class_3)

def get_cor_coef(data, data1):
  """
  Вычисление коэффициента корреляции Пирсона
  """
  cor_coef = st.pearsonr(data, data1)
  return cor_coef[0] #функция выдает 2 значения: коэффициент Пирсона и p-показатель

def get_average_and_median(data = None):
  """
  функция высчитывает среднее значение и медиану
  """
  lst = data.value_counts().index.tolist()
  print("Среднее: ", np.average(lst))
  print("Медиана: ", np.median(lst))
  return str(np.average(lst)) + str(np.median(lst))

def get_name(name):
  """
  Функция для фильтрации ячеек Name
  """
  import re
  # Первое слово до запятой - фамилия
  fam = re.search('^[^,]+, (.*)', name)
  if fam:
    name = fam.group(1)
    # Если есть скобки - то имя пассажира в них
  fam = re.search('\(([^)]+)\)', name)
  if fam:
    name = fam.group(1)
    # Удаляем обращения
  name = re.sub('(Master\. |Mr\. |Mrs\. |Miss\. )', '', name)
    # Берем первое оставшееся слово и удаляем кавычки
  name = name.split(' ')[0].replace('"', '')
  return name

def get_popular_male_name(data):
  """
  возвращает самое популярное мужское имя
  """
  names = data[data['Sex'] == 'male']['Name'].map(get_name)
  name_counts = names.value_counts()
  if(name_counts.count()>0):
    return name_counts.head(1).index.values[0]
  return ''

def get_popular_name(data,sex,age):
  """
  Функция возвращает самое популярное имя того пола и возраста(старше чем), которое указывает пользователь
  """
  if (data is None):
    return ''
  if (sex=='male' or sex=='female'):
    names = data[data['Sex'] == sex][data['Age'] > age]['Name'].map(get_name)
  name_counts = names.value_counts()
  if(name_counts.count()>0):
    return name_counts.head(1).index.values[0] #head(n)-возвращает первые n строк, index(n)-возвращает положение n в списке ,values-оставляет только значение ключа
  return ''


data = pd.read_csv('train.csv', index_col='PassengerId') #чтение файла

male_int = get_number_of_pass('male', data['Sex'] ) 
female_int = get_number_of_pass('female', data['Sex'])
print("Количество людей:\nМужчины =", male_int,", Женщины =", female_int)
print('\n')

C_port_int = get_number_of_ports('C', data['Embarked']) 
Q_port_int = get_number_of_ports('Q', data['Embarked'])
S_port_int = get_number_of_ports('S', data['Embarked'])
print("Количество людей, загруженных на борт:\nПорт C =", C_port_int,", Порт Q =", Q_port_int, "Порт S =", S_port_int )
print('\n')

died_int = get_number_of_died(data['Survived'])
print('Количество погибших людей\n', died_int)
print('\n')

Pclass = get_pass_classes(data['Pclass'])
print('Доля пассажиров в классах:', Pclass)
print('\n')

cor_coef_SibSp_Parch = get_cor_coef(data['SibSp'], data['Parch'])
print("Коэффициент корреляции Пирсона между количеством супругов и количеством детей равен \n", cor_coef_SibSp_Parch)
print('\n')

cor_coef_Age_Surv = get_cor_coef(data['Age'], data['Survived'])
print("Коэффициент корреляции Пирсона между возрастом и выживанием \n", cor_coef_Age_Surv)
print('\n')

#cor_coef_Sex_Surv = get_cor_coef(data['Sex'], data['Survived'])
#print("Коэффициент корреляции Пирсона между полом человека и выживанием \n", cor_coef_Sex_Surv)
#print('\n')

cor_coef_Class_Surv = get_cor_coef(data['Pclass'], data['Survived'])
print("Коэффициент корреляции Пирсона между классом, в котором пассажир ехал, и выживанием \n", cor_coef_Class_Surv)
print('\n')

print('Среднее и медиана возраста пассажиров:')
get_average_and_median(data['Age'])
print('\n')

print('Среднее и медиана стоимости билета:')
get_average_and_median(data['Fare'])
print('\n')

print('Самое популярное мужское имя на корабле', get_popular_male_name(data))
print('\n')

print('Самые популярные имена старше 15 лет')
#Самое популярное имя среди мужчин старше 15 лет
print('У мужчин - ', get_popular_name(data,'male',15))
#Самое популярное имя среди женщин старше 15 лет
print('У женщин - ', get_popular_name(data,'female',15))
#Самое популярное имя среди всех старше 15 лет
