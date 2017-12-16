import pandas as pd
valid = True
csv_file = open('contacts.csv')
df = pd.read_csv(csv_file)
try:
    saved_column = df['phone']
except KeyError:
    try:
        saved_column = df['contacts']
    except KeyError:
        try:
            saved_column = df['contact']
        except KeyError:
            try:
                saved_column =df['numbers']
            except KeyError:
                try:
                    saved_column = df['number']
                except KeyError:
                    print('Error CSV')
                    valid = False

if valid:
    for contact in saved_column:
                contact = str(contact)
                if len(contact)==10:
                    contact = '91'+contact
                print(contact)
