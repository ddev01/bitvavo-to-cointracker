import csv

# Open the input and output files
with open('history.csv', mode='r') as csv_file, open('history_transformedsss.csv', mode='w', newline='') as csv_out_file:
    csv_reader = csv.DictReader(csv_file)
    
    # Define the fieldnames for the output file
    fieldnames = ['Date', 'Received Quantity', 'Received Currency', 'Sent Quantity', 'Sent Currency', 'Fee Amount', 'Fee currency', 'Tag']
    
    # Create a DictWriter object
    csv_writer = csv.DictWriter(csv_out_file, fieldnames=fieldnames)
    
    # Write the header to the output file
    csv_writer.writeheader()
    
    for row in csv_reader:
        coinDate = row['Date'] + ' ' + row['Time'].split('.')[0]
        receivedQuantity = None
        receivedCurrency = None
        sentQuantity = None
        sentCurrency = None
        feeAmount = None
        feeCurrency = None
        try:
            if row['Type'] == 'deposit':
                receivedQuantity = abs(float(row['Amount']))
                receivedCurrency = row['Currency']
            elif row['Type'] == 'withdrawal':
                sentQuantity = abs(float(row['Amount']))
                sentCurrency = row['Currency']
                feeAmount = abs(float(row['Fee amount']))
                feeCurrency = row['Fee currency']
            elif row['Type'] == 'buy':
                receivedQuantity = abs(float(row['Amount']))
                receivedCurrency = row['Currency']
                sentQuantity = abs(float(row['EUR received / paid']))
                sentCurrency = 'EUR'
                feeAmount = abs(float(row['Fee amount']))
                feeCurrency = row['Fee currency']
            elif row['Type'] == 'sell':
                receivedQuantity = abs(float(row['EUR received / paid']))
                receivedCurrency = 'EUR'
                sentQuantity = abs(float(row['Amount']))
                sentCurrency = row['Currency']
                feeAmount = abs(float(row['Fee amount']))
                feeCurrency = row['Fee currency']
            else:
                print('Error parsing row: ' + str(row))
                continue
        except Exception as e:
            print('Error parsing row: ' + str(row) + '. Error: ' + str(e))
            exit()
        # Write the row to the output file
        csv_writer.writerow({
            'Date': coinDate,
            'Received Quantity': receivedQuantity,
            'Received Currency': receivedCurrency,
            'Sent Quantity': sentQuantity,
            'Sent Currency': sentCurrency,
            'Fee Amount': feeAmount,
            'Fee currency': feeCurrency,
            'Tag': ''
        })