import requests
from bs4 import BeautifulSoup
import sqlite3
import httplib2


def update_db():
    con = sqlite3.connect("players.db")
    cursor = con.cursor()
    try:
        cursor.execute("""DROP TABLE players""")
    except Exception:
        pass
    cursor.execute("""CREATE TABLE players (surname TEXT, name TEXT, otchestvo TEXT, link TEXT)""")
    for i in range(1, 172):
        req = requests.get(f"https://www.mossambo.ru/players?page={i}")
        src = req.text
        soup = BeautifulSoup(src, "lxml")
        names = soup.find_all(class_="name")
        links = soup.find(class_="catalog-list flex-row justify-space").find_all("a")
        for i in range(len(names)):
            fio = []
            fio = names[i].text.strip().lower().split()
            surname = fio[0]
            name = fio[1]
            otchestvo = " ".join(fio[2:])
            cursor.execute(f"""INSERT INTO players VALUES ('{surname}', '{name}', '{otchestvo}', '{links[i].get("href")}')""")
            con.commit()
    con.close()


def get_info(fio: str):
    con = sqlite3.connect("players.db")
    cursor = con.cursor()
    fio = fio.lower().split()
    if len(fio) == 3:
        surname = fio[0]
        name = fio[1]
        otchestvo = " ".join(fio[2:])
    elif len(fio) == 2:
        surname = fio[0]
        name = fio[1]
        otchestvo = ""
    else:
        surname = fio[0]
        name = ""
        otchestvo = ""
    image_link = None
    if (not (name) and not (otchestvo)):
        res = cursor.execute(f"SELECT link FROM players WHERE surname = '{surname}'")
        try:
            link, = res.fetchone()
            text, image_link = parse_info(link)
        except Exception:
            text = "Неизвестный спортсмен"
    elif (not (otchestvo)):
        res = cursor.execute(f"SELECT link FROM players WHERE surname = '{surname}' AND name = '{name}'")
        try:
            link, = res.fetchone()
            text, image_link = parse_info(link)
        except Exception:
            text = "Неизвестный спортсмен"
    else:
        res = cursor.execute(f"SELECT link FROM players WHERE surname = '{surname}' AND name = '{name}' AND otchestvo = '{otchestvo}'")
        try:
            link, = res.fetchone()
            text, image_link = parse_info(link)
        except Exception:
            text = "Неизвестный спортсмен"
    con.close()
    return text, image_link


def remove_duplicates(data: list):
    for i in range(len(data)):
        if "Тренер(ы): " in data[i]:
            if (data[i][11:]).strip() == (data[i + 1][:len(data[i]) - 11]).strip():
                data[i] = "Тренер(ы): "
            else:
                pass
    return data


def parse_info(link: str):
    req = requests.get(f"{link}")
    src = req.text
    soup = BeautifulSoup(src, "lxml")
    name = soup.find(class_="name").text
    data = soup.find(class_="characteristics-list").find_all(class_="val")
    if (soup.find(class_="photo").find("img") != None):
        image_link = soup.find(class_="photo").find("img").get("src")
    else:
        image_link = None
    res = []
    res.append(f"{name.replace("\n\n", "\n").strip()}\n")
    for i in data:
        res.append(f"{i.find_previous().text} {i.text.replace("\n\n", "\n").strip()}\n")
    res = remove_duplicates(res)
    res = "".join(res)
    res = res.strip()
    res = make_bold(res)
    return res, image_link


def insert_string(original, insert, index):
    return original[:index] + insert + original[index:]


# От \n и несколько символов
def make_bold(data: str):
    idn = [i for i in range(len(data)) if data[i] == "\n"]
    data = insert_string(data, '*', 0)
    data = insert_string(data, '*', idn[0] + 1)
    data = insert_string(data, '*', idn[0] + 3)
    data = insert_string(data, '*', idn[0] + 18)
    data = insert_string(data, '*', idn[1] + 5)
    data = insert_string(data, '*', idn[1] + 11)
    data = insert_string(data, '*', idn[2] + 7)
    data = insert_string(data, '*', idn[2] + 26)
    data = insert_string(data, '*', idn[3] + 9)
    data = insert_string(data, '*', idn[3] + 20)
    data = insert_string(data, '*', idn[4] + 11)
    data = insert_string(data, '*', idn[4] + 30)
    return data


# print(get_info("Гусаров Андрей Андреевич")[0], get_info("Гусаров Андрей Андреевич")[1])
# print("#" * 20)
# print(get_info("Клецков"))
# print("#" * 20)
# print(get_info("Инякин Роман"))
# print("#" * 20)
# print(get_info("Гусаров"))

# make_bold('Клецков Никита Валерьевич\nДата рождения: 26 November 1986 года (37 лет)\nКлуб: ГБОУ «ЦСиО  «Самбо-70» (отд. "Виноградова") Москомспорта\nВесовая категория: 71 кг\nТренер(ы): Павлов Денис  Фунтиков Павел\nСпортивное звание: Заслуженный мастер спорта России')
