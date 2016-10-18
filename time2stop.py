import urllib
import urllib.request as UrlReq
import urllib.parse
import random
import argparse
import sys
from string import ascii_letters as chars
from time import sleep
from time import time

msg="""Default call (without args):
    time2stop -d 3 -s -1 : script will send POST messages in 3 sec intervals
    
    When using random delay: Maximum delay > minimum delay && delay > 0
    You can always stop script by Ctrl + C"""

parser = argparse.ArgumentParser(description="Help people in village NOT die from radiation.", formatter_class=argparse.RawDescriptionHelpFormatter, epilog=msg)
parser.add_argument("-s","--signs", type=int, default=-1, help="how many signs will be sent. -1 for infinity", metavar="N")
delay_group = parser.add_mutually_exclusive_group()
delay_group.add_argument("-d","--delay", type=int, default=3, help="delay between sign sending", dest="delay", metavar="sec")
delay_group.add_argument("-r","--random", type=int, nargs=2, help="random delay in between passed 2 values", metavar="sec")

passed_args = parser.parse_args()

count = passed_args.signs
delay = passed_args.delay
if passed_args.random is not None:
    min_delay, max_delay = passed_args.random
    if max_delay <= min_delay or max_delay <= 0 or min_delay < 0:
        print("Error: When using random delay: Maximum delay > minimum delay && delay > 0")
        sys.exit()


lname_female = ["Ильина", "Гусева", "Титова", "Кузьмина", "Кудрявцева", "Баранова", "Куликова", "Алексеева", "Степанова", "Яковалева", "Сорокина", "Сергеева", "Романова", "Захарова", "Борисова", "Королева", "Герасимова", "Пономарева", "Григорьева", "Лазарева", "Медведева", "Ершова", "Никитина", "Соболева", "Рябова", "Полякова", "Цветкова", "Данилова", "Жукова", "Фролова", "Журавлева", "Николаева", "Путина", "Молчанова", "Крылова", "Максимова", "Сидорова", "Осипова", "Белоусова", "Федотова", "Дорофеева", "Егорова", "Панина", "Матвеева", "Боброва", "Дмитриева", "Калинина", "Анисимова", "Петухова", "Пугачева", "Антонова", "Тимофеева", "Никифорова", "Веселова", "Филиппова", "Романова", "Маркова", "Большакова", "Суханова", "Миронова", "Александрова", "Коновалова", "Шестакова", "Казакова", "Ефимова", "Денисова", "Громова", "Фомина", "Андреева", "Давыдова", "Мельникова", "Щербакова", "Блинова", "Колесникова", "Иванова", "Смирнова", "Кузнецова", "Попова", "Соколова", "Лебедева", "Козлова", "Новикова", "Морозова", "Петрова", "Волкова", "Соловаьева", "Васильева", "Зайцева", "Павлова", "Семенова", "Голубева", "Виноградова", "Богданова", "Воробьева", "Федорова", "Михайлова", "Беляева", "Тарасова", "Белова", "Комарова", "Орлова", "Киселева", "Макарова", "Андреева"]

fname_female = ["Милана", "София", "Есения", "Арина", "Кира", "Анастасия", "Вероника", "Алиса", "Полина", "Виктория", "Стася", "Марьяна", "Дарья", "Ксения", "Ева", "Алина", "Екатерина", "Валерия", "Мария", "Анна", "Елизавета", "Дарина", "Юлия", "Кристина", "Алёна", "Ульяна", "Милена", "Амелия", "Злата", "Диана", "Камила", "Ольга", "Софья", "Елена", "Румия", "Аделия", "Карина", "Элина", "Ирина", "Милослава", "Ангелина", "Маргарита", "Александра", "Татьяна", "Наталья", "Диляра", "Афина", "Марина", "Радмила", "Светлана", "Лина", "Олеся", "Эвелина", "Милада", "Яна", "Каролина", "Сати", "Амина", "Малика", "Евгения", "Юлиана", "Оксана", "Таисия", "Джана", "Альбина", "Мадина", "Ярослава", "Людмила", "Индира", "Юлдуз", "Гулия", "Марьям", "Дарига", "Лейла", "Анита", "Анжела", "Куралай", "Медина", "Василиса", "Аврора", "Эльвира", "Божена", "Инна", "Алла"]

lname = ["Авдеев", "Агафонов", "Аксёнов", "Александров", "Алексеев", "Андреев", "Анисимов", "Антонов", "Артемьев",
         "Архипов", "Афанасьев", "Баранов", "Белов", "Белозёров", "Белоусов", "Беляев", "Беляков", "Беспалов",
         "Бирюков", "Блинов", "Блохин", "Бобров", "Бобылёв", "Богданов", "Большаков", "Борисов", "Брагин", "Буров",
         "Быков", "Васильев", "Веселов", "Виноградов", "Вишняков", "Владимиров", "Власов", "Волков", "Воробьёв",
         "Воронов", "Воронцов", "Гаврилов", "Галкин", "Герасимов", "Голубев", "Горбачёв", "Горбунов", "Гордеев",
         "Горшков", "Григорьев", "Гришин", "Громов", "Гуляев", "Гурьев", "Гусев", "Гущин", "Давыдов", "Данилов",
         "Дементьев", "Денисов", "Дмитриев", "Доронин", "Дорофеев", "Дроздов", "Дьячков", "Евдокимов", "Евсеев",
         "Егоров", "Елисеев", "Емельянов", "Ермаков", "Ершов", "Ефимов", "Ефремов", "Жданов", "Жуков", "Журавлёв",
         "Зайцев", "Захаров", "Зимин", "Зиновьев", "Зуев", "Зыков", "Иванков", "Иванов", "Игнатов", "Игнатьев",
         "Ильин", "Исаев", "Исаков", "Кабанов", "Казаков", "Калашников", "Калинин", "Капустин", "Карпов", "Кириллов",
         "Киселёв", "Князев", "Ковалёв", "Козлов", "Колесников", "Колобов", "Комаров", "Комиссаров", "Кондратьев",
         "Коновалов", "Кононов", "Константинов", "Копылов", "Корнилов", "Королёв", "Костин", "Котов", "Кошелев",
         "Красильников", "Крылов", "Крюков", "Кудрявцев", "Кудряшов", "Кузнецов", "Кузьмин", "Кулагин", "Кулаков",
         "Куликов", "Лаврентьев", "Лазарев", "Лапин", "Ларионов", "Лебедев", "Лихачёв", "Лобанов", "Логинов", "Лукин",
         "Лыткин", "Макаров", "Максимов", "Мамонтов", "Марков", "Мартынов", "Маслов", "Матвеев", "Медведев",
         "Мельников", "Меркушев", "Миронов", "Михайлов", "Михеев", "Мишин", "Моисеев", "Молчанов", "Морозов",
         "Муравьёв", "Мухин", "Мышкин", "Мясников", "Назаров", "Наумов", "Некрасов", "Нестеров", "Никитин",
         "Никифоров", "Николаев", "Никонов", "Новиков", "Носков", "Носов", "Овчинников", "Одинцов", "Орехов", "Орлов",
         "Осипов", "Павлов", "Панов", "Панфилов", "Пахомов", "Пестов", "Петров", "Петухов", "Поляков", "Пономарёв",
         "Попов", "Потапов", "Прохоров", "Рогов", "Родионов", "Рожков", "Романов", "Русаков", "Рыбаков", "Рябов",
         "Савельев", "Савин", "Сазонов", "Самойлов", "Самсонов", "Сафонов", "Селезнёв", "Селиверстов", "Семёнов",
         "Сергеев", "Сидоров", "Силин", "Симонов", "Ситников", "Соболев", "Соколов", "Соловьёв", "Сорокин", "Степанов",
         "Стрелков", "Субботин", "Суворов", "Суханов", "Сысоев", "Тарасов", "Терентьев", "Тетерин", "Тимофеев",
         "Титов", "Тихонов", "Третьяков", "Трофимов", "Туров", "Уваров", "Устинов", "Фадеев", "Фёдоров", "Федосеев",
         "Федотов", "Филатов", "Филиппов", "Фокин", "Фомин", "Фомичёв", "Фролов", "Харитонов", "Хохлов", "Цветков",
         "Чернов", "Шарапов", "Шаров", "Шашков", "Шестаков", "Шилов", "Ширяев", "Шубин", "Щербаков", "Щукин", "Юдин",
         "Яковлев", "Якушев", "Смирнов"
         ]
fname = ["Азамат", "Азат", "Александр", "Альберт", "Антон", "Артём", "Артур", "Богдан", "Борис", "Валентин", "Вадим",
         "Владимир", "Владислав", "Виктор", "Вячеслав", "Глеб", "Герман", "Давид", "Даниил", "Денис", "Егор", "Захар",
         "Иван", "Ильдар", "Кирилл", "Константин", "Леонид", "Марат", "Марк", "Максим", "Михаил", "Назар", "Никита",
         "Олег", "Петр", "Рашид", "Ринат", "Роберт", "Роман", "Руслан", "Рустам", "Святослав", "Станислав", "Степан",
         "Семён", "Тарас", "Филипп", "Фёдор", "Эрик", "Эльдар", "Эмиль", "Эдуард", "Ярослав", "Яков"]

city = ["Азов", "Батайск", "Белая Калитва", "Волгодонск", "Донецк", "Новочеркасск", "Новошахтинск", "Ростов",
        "Ростов-на-Дону", "Сальск", "Таганрог", "Шахты"]

domain = ["yandex.ru", "mail.ru", "bk.ru", "rambler.ru", "gmail.com"]

headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
           "Accept-Encoding": "gzip, deflate",
           "Accept-Language": "en-US,en;q=0.8,ru;q=0.6",
           "Cache-Control": "max-age=0",
           "Connection": "keep-alive",
           "Content-Type": "application/x-www-form-urlencoded",
           "Host": "www.derevensk.ru",
           "Origin": "http://www.derevensk.ru",
           "Referer": "http://www.derevensk.ru/sborgolosov/izlucheniu_net.php",
           "Upgrade-Insecure-Requests": "1"
           }

second_url = "http://www.derevensk.ru/sborgolosov/ok.php"
second_headers = {"Host": "www.derevensk.ru",
          "Connection": "keep-alive",
          "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
          "Upgrade-Insecure-Requests": "1",
          "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36",
          "Referer": "http://www.derevensk.ru/sborgolosov/izlucheniu_net.php",
          "Accept-Encoding": "gzip, deflate, sdch",
          "Accept-Language": "en-US,en;q=0.8,ru;q=0.6"}

# to get random name/city/domain
random_ = lambda values_list: values_list[random.randint(0, len(values_list) - 1)]
random_age = lambda: random.randint(19, 60)
# to get random username for email address
# username is the only thing that generates entirely random
# because email is the ONLY field that checks in form
random_username = lambda: "".join([random.choice(chars) for _ in range(random.randint(6, 10))])

# total signs in session
total_signs = 0

# file with all worked signs
logfile = open("stopping_the_polution.txt", "a", encoding="utf8")

print("STOPPING THE POLLUTION begins now")
print("Every dot shown another active citizen")
if count > 0:
    print("There will be {0} active citizens".format(count))

try:
    while count != 0:
        try:
            # generate random data (gender, name, city, mail)
            data = {
                "golospost": 1,
                "fname": random_(fname),
                "lname": random_(lname),
                "otch": random_(fname) + "ович",  # hotfix
                "email": random_username() + "@" + random_(domain),
                "ages": random_age(),
                "city": random_(city)
            } if random.randint(0,1) else {
                "golospost": 1,
                "fname": random_(fname_female),
                "lname": random_(lname_female),
                "otch": random_(fname) + "овна",  # hotfix
                "email": random_username() + "@" + random_(domain),
                "ages": random_age(),
                "city": random_(city)
            }

            # encoding data to send
            values = urllib.parse.urlencode(data, encoding="cp1251")
            binary_values = values.encode(encoding="cp1251")
            req = UrlReq.Request(url="http://www.derevensk.ru/sborgolosov/izlucheniu_net.php", data=binary_values, headers=headers)
            req.add_header("Content-Length", str(len(binary_values)))
            
            # send the POST
            response = urllib.request.urlopen(req)

            # request to derevensk OK
            # req = UrlReq.Request(url=second_url, headers=second_headers, method='GET')

            # response = urllib.request.urlopen(req)

            if response.code == 200:
                logfile.write("{lname} {fname} {otch},{ages} из {city} - {email} signed the petition\n".format(**data))
                logfile.flush()
                print(".", end="", flush=True)
                total_signs += 1
        except Exception as e:
            print("something went wrong")
            print(e)
        count -= 1
        if delay == 0:
            sleep(random.randint(min_delay, max_delay))
        else:
            sleep(delay)
except KeyboardInterrupt as err:
    print("\nYou've interrupted the revolution.")
finally:
    print("Total of {0} signs today.\nGood job, comrade.".format(total_signs))
    print("\nRevolution end.")
    logfile.close()
