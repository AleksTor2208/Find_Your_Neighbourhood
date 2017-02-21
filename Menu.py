import csv
from Lesser_Poland import *
import sqlite3
import time
import os
import sys


class Menu: 
    
    @staticmethod
    def data_reader(file_path):
        with open (file_path) as cities_file:
            reader = csv.reader(cities_file, delimiter='\t')
            data = [row for row in reader]
        return data 

    
    @staticmethod
    def get_input(parameter):

        choose = input(parameter)
        if int(choose) > 5:
            raise ValueError ("Value needs to be more then 0 and less then 5")
        return choose


    @staticmethod
    def main():

        while True:
        
            interface = ''' What would you like to do:
                (1) List statistics
                (2) Display 3 cities with longest names
                (3) Display county's name with the largest number of communities 
                (4) Display locations, that belong to more than one category
                (5) Advanced search
                (0) Exit program
                '''
            print(interface, '\n')
            option = Menu.get_input('choose the number: ')

            if option == '1':
                os.system('clear')
                Menu.statistic_method()                
            elif option == '2':
                os.system('clear')
                print('\nCities with longest names: {}.'.format(Menu.longest_names('malopolska.csv')))
                time.sleep(2)
            elif option == '3':
                os.system('clear')
                county = Menu.largest_county('malopolska.csv')
                print('{} is the largest county including {} communities.'.format(county[0], county[1]))
                time.sleep(2)
            elif option == '4':
                os.system('clear')
                data = Menu.load_db('malopolskie.db')
                Menu.moreone_category(data)
                time.sleep(5)
            elif option == '5':
                os.system('clear')
                Menu.advanced_search('malopolska.csv')
                time.sleep(4)
            elif option == '0':
                sys.exit()

    @staticmethod
    def statistic_method():        
        print('''
╔════════════════════╗    
║ (1) Try SQL        ║
║ (2) Try CSV reader ║
╚════════════════════╝   ''')

        choose = input("Type the number: ")
        
        if choose == '1':
            data = Menu.load_db('malopolskie.db')
            Menu.try_sql_data(data)  # result is a list of lists.
            
        elif choose == '2':        
            Menu.list_statistics('malopolska.csv')
        else:
            print('Invalid value.')
            return
        time.sleep(4)


    @staticmethod
    def load_db(filepath):
        load_data = sqlite3.connect(filepath)
        return load_data


    @staticmethod
    def try_sql_data(data):
        """
        Prepares the table of cumulative amount of different types in Lesser Poland district
        """
        time_cur = time.time()
        result = data.execute(
            '''SELECT Count(*), typ FROM Malopolskie GROUP BY typ;''')   
        
        new_table = [[0, 'województwo'], [0, 'powiat'],
                [0, 'gmina miejska'], [0, 'gmina wiejska'],
                [0, 'gmina miejsko-wiejska'], [0, 'miasto'],
                [0, 'obszar wiejski'], [0, 'miasto na prawach powiatu'],
                [0, 'delegatura']]
        for row in result:
            for area in new_table:
                if area[1] == 'powiat':                    
                    if row[1] == 'miasto na prawach powiatu':
                        area[0] += int(row[0])
                if row[1] == area[1]:
                    area[0] += int(row[0])
        for row in new_table:
            for item in row:
                if type(item) == int:
                    item = str(item)

        
        print(Menu.get_table(['Malopolskie'], new_table))       
        print('Time:', time.time()-time_cur)

    @staticmethod
    def advanced_search(filepath):
        """
        Prepares the table wich shows the advanced search of the locations.
        """
        Lesspol = Menu.data_reader(filepath)
        choose = input('Searching for: ')
        if choose == '':
            print("User input is empty.")
            return
        table = []
        for row in Lesspol:
            word = row[4][:len(choose)]
            if  word.lower() == choose.lower():                
                table.append([row[4], row[5]])
        sorted_table = sorted(table)   
        print(Menu.get_table(['LOCATION', 'TYPE'], sorted_table))


    @classmethod
    def moreone_category(cls, data):
        """
        Prints the table with locations, which belong to more then one category. 
        """
        result = data.execute(
            
            '''SELECT DISTINCT nazwa FROM Malopolskie GROUP BY nazwa HAVING COUNT(*) > 1;''')
        table = []
        for row in result:
            table.append(list(row))
        print('Locations, which belong \nto more then one category:')
        print(Menu.get_table('', table))

        
    
    @classmethod
    def list_statistics(cls, filepath):
        """
        Prepares the table of cumulative amount of different types in Lesser Poland district
        """
        time_cur = time.time()
        Lesspol = Menu.data_reader(filepath)
        Lesspol = Lesspol[1:]
        dict_stat = {'województwo': 0, 'powiaty': 0, 'gmina miejska': 0, 'gmina wiejska': 0, 
        'gmina miejsko-wiejska': 0, 'obszar wiejski': 0, 'miasto': 0, 'miasto na prawach powiatu': 0, 'delegatura': 0}
       
     
        for row in Lesspol:
            if row[5] == 'województwo':                
                dict_stat['województwo'] += 1
            elif row[5] == 'powiat' or row[5] == 'miasto na prawach powiatu':                               
                dict_stat['powiaty'] += 1
            elif row[5] == 'gmina miejska':                 
                dict_stat['gmina miejska'] += 1
            elif row[5] == 'gmina wiejska':
                dict_stat['gmina wiejska'] += 1
            elif row[5] == 'gmina miejsko-wiejska':
                dict_stat['gmina miejsko-wiejska'] += 1
            elif row[5] == 'miasto':
                dict_stat['miasto'] += 1
            elif row[5] == 'obszar wiejski':
                dict_stat['obszar wiejski'] += 1
            elif row[5] == 'miasto na prawach powiatu':
                dict_stat['miasto na prawach powiatu'] += 1
            elif row[5] == 'delegatura':
                dict_stat['delegatura'] += 1

        table = [['', 'województwo'], ['', 'powiaty'],
                ['', 'gmina miejska'], ['', 'gmina wiejska'],
                ['', 'gmina miejsko-wiejska'], ['', 'miasto'],
                ['', 'obszar wiejski'], ['', 'miasto na prawach powiatu'],
                ['', 'delegatura']]

        for key, value in dict_stat.items():
            for index in table:
                if key == index[1]:
                    index[0] = str(value)     
        
        print(Menu.get_table(['MAłOPOLSKIE'], table))
        print('Time:', time.time()-time_cur)

    @classmethod
    def largest_county(cls, filepath):
         
        Lesspol = Menu.data_reader(filepath)
        for row in Lesspol[1:]:
            if row[5] == 'województwo':
                malopolska = Province(row[4], row[5])  # object of a province is created
            if row[5] == 'powiat':
                county = County(row[4], row[5])
                malopolska.add_county(county) 
            if row[5][:5] == 'gmina':  # check if the row represents the community
               
                if row[5] == 'gmina miejska': 
                    municipality = Municipality(row[4], row[5])
                    county.add_community(municipality)
                
                elif row[5] == 'gmina wiejska':
                    rural = Rural_commune(row[4], row[5])
                    county.add_community(rural)
                elif row[5] == 'gmina miejsko-wiejska':
                    urban_rural = Urban_rural_commune(row[4], row[5])
                    county.add_community(urban_rural)
        largest_county = ['', 0]
        for county in malopolska.counties:
            
            if len(county.communities) > largest_county[1]:
                largest_county = [county.name, len(county.communities)]
        return largest_county
            

    @classmethod
    def longest_names(cls, filepath):
        
        Lesspol = Menu.data_reader(filepath)
        cities = []
        for row in Lesspol:
            if row[5] == 'miasto':
                city = City(row[4], row[5])    #create an object of the City regarding the external data
                cities.append(city.name)  
        longest_names = []
        biggest_city = ''
        for city in cities:            
            if len(biggest_city) < len(city):
                biggest_city = city
                longest_names.insert(0, biggest_city)
                cities.remove(city)
        return ', '.join(longest_names)   


    @classmethod
    def get_table(cls, title_list, table):
        """
        Return the table
        """
        cell_size = []
        new_table = ''
        # checking largest cells
        cell_size = list()

        for i, title in enumerate(title_list):
            cell_size.append(len(title))
        
        for items in table:
            for i, item in enumerate(items):
                try:
                    if cell_size[i] < len(str(item)):
                        cell_size[i] = len(str(item))
                except:
                    cell_size.append(len(item))
     

        # how big table
        table_size = 1
        for dash in cell_size:
            table_size += (dash + 3)

        # printing table
        
        if len(title_list) == 1:         
            new_table +=    '/' + '-' * (table_size-2) + '\ ' + '\n'
            new_table += "|" + ' ' * (table_size-(len(title_list[0]))*3) + title_list[0] + ' ' * 20 + '|\n'
            new_table += '-' * table_size + '\n'
            for items in table:  # items - pojedyncza lista z calej list
                for i, item in enumerate(items):  # item - oddzielny element z listy items
                    if i == 0:
                        new_table += '|'
                    new_table += ' {:{width}} |'.format(str(item), width=cell_size[i])
        
                new_table += '\n'

            new_table += '-' * table_size + '\n'
        else:
            
            # printing table
            new_table += '-' * table_size + '\n'

            for i, title in enumerate(title_list):
                if i == 0:
                    new_table += '|'
                new_table += ' {:{width}} |'.format(title, width=cell_size[i])

            new_table += '\n' + '-' * table_size + '\n'

            for items in table:
                for i, item in enumerate(items):
                    if i == 0:
                        new_table += '|'
                    new_table += ' {:{width}} |'.format(str(item), width=cell_size[i])
                new_table += '\n'

            new_table += '-' * table_size

            return new_table

        return new_table




if __name__ == '__main__':
    Menu.main()