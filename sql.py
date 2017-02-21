import csv

def csv_reader():
    
    with open ('malopolska.csv') as main_file:
        data_file = csv.reader(main_file, delimiter='\t')
        data = [row for row in data_file]    
    return data

data = csv_reader()
for row in data:    
    
    print("INSERT INTO Malopolskie(woj, pow, gmi, rgmi, nazwa, typ) VALUES ('{}', '{}', '{}', '{}', '{}', '{}');".format(row[0], 
                                                                            row[1], row[2], row[3], row[4], row[5])) 
