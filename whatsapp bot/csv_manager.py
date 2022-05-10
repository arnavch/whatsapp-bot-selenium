import csv

def put_data(userData: dict):
    table_header=[]
    with open('C:/Users/mihir/Desktop/whatsapp bot/csv storage/table.csv', 'r', newline='') as f_object:
        dictwriter_object = csv.reader(f_object)
        if dictwriter_object==None:
            print('here')
            table_header=[]
        else:
            table_header=list(dictwriter_object)[0]
        f_object.close()
    
    with open('C:/Users/mihir/Desktop/whatsapp bot/csv storage/data.csv', 'a+', newline='') as f_object:
        data=[]
        for i in table_header:
            val=''
            if userData.get(i)!=None:
                val=userData.get(i)
                del userData[i]
            data.append(val)
            
        if len(userData.keys())>0:
            for i in userData.keys():
                table_header.append(i)
                data.append(userData[i])

        dictwriter_object = csv.writer(f_object)
    
        dictwriter_object.writerow(data)
    
        f_object.close()

    with open('C:/Users/mihir/Desktop/whatsapp bot/csv storage/table.csv', 'w+', newline='') as f_object:
        dictwriter_object = csv.writer(f_object)
        dictwriter_object.writerow(table_header)
        f_object.close()


def get_contact():
    with open('C:/Users/mihir/Desktop/whatsapp bot/csv storage/contact.csv', 'r', newline='') as f_object:
        reader=csv.reader(f_object)
        return list(reader)[0]

def set_contact(contact):
    with open('C:/Users/mihir/Desktop/whatsapp bot/csv storage/contact.csv', 'w+', newline='') as f_object:
        dictwriter_object = csv.writer(f_object)
        dictwriter_object.writerow(contact)
        f_object.close()
        return True

