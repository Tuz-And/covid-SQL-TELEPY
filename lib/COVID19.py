import mysql.connector
import requests
if __name__ == "__main__":
    pass


class GetCOVID19:
    def __init__(self, HOSTNAME, USERNAME, PASSWORD, COVID19API):
        self.__COVID19API = COVID19API
        self.__db = mysql.connector.connect(
            host=HOSTNAME,
            user=USERNAME,
            password=PASSWORD
        )
        self.__cursor = self.__db.cursor()
        self.__cursor.execute("CREATE DATABASE IF NOT EXISTS telepy")
        self.__cursor.execute('USE telepy')
        self.__cursor.execute('CREATE TABLE IF NOT EXISTS Countries (id INT AUTO_INCREMENT PRIMARY KEY, Country VARCHAR(64), CountryCode VARCHAR(4), Slug VARCHAR(124),NewConfirmed INT, TotalConfirmed INT, NewDeaths INT, TotalDeaths INT, NewRecovered INT, TotalRecovered INT, Date VARCHAR(128))')
        self.__get_covid19_info()

    def __get_covid19_info(self):
        responce = requests.get(self.__COVID19API)
        self.__covid_data = responce.json()
        # print('API => ', covid_data)
        self.__cursor.execute("TRUNCATE Countries")
        for item in self.__covid_data['Countries']:
            # print(item['Country'])
            sql = "INSERT INTO Countries (Country, CountryCode, Slug, NewConfirmed, TotalConfirmed, NewDeaths, TotalDeaths, NewRecovered, TotalRecovered, Date) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (item['Country'], item['CountryCode'], item['Slug'], item['NewConfirmed'], item['TotalConfirmed'],
                   item['NewDeaths'], item['TotalDeaths'], item['NewRecovered'], item['TotalRecovered'], item['Date'])
            self.__cursor.execute(sql, val)
        self.__db.commit()
    def menu(self):
        exit = False
        while not exit:
            choice = int(input(
                "1. sort_by_total_confirmed\n2. sort_by_new_confirmed\n3. sort_by_country_name\n0 Exit\n ===>> "))
            if choice == 1:
                self.sort_by_total_confirmed()
            elif choice == 2:
                self.sort_by_new_confirmed()
            elif choice == 3:
                self.sort_by_country_name()
            elif choice == 0:
                break
            else:
                print("Wrong choice.")


    def sort_by_total_confirmed(self):
        self.__cursor.execute("SELECT Country, TotalConfirmed FROM Countries ORDER BY TotalConfirmed ")
        for item in self.__cursor.fetchall():
            print(item)

    def sort_by_new_confirmed(self):
        self.__cursor.execute("SELECT Country, NewConfirmed FROM Countries ORDER BY NewConfirmed ")
        for item in self.__cursor.fetchall():
            print(item)

    def sort_by_country_name(self):
        self.__cursor.execute("SELECT Country, CountryCode, Slug, NewConfirmed, TotalConfirmed, NewDeaths, TotalDeaths, NewRecovered, TotalRecovered FROM Countries ORDER BY Country ")
        for item in self.__cursor.fetchall():
            print(item)
