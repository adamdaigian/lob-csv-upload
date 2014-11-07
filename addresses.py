import lob
import csv
lob.api_key = 


f = open('addresses.csv', 'rU')
csv_f = csv.reader(f)
allData = []

returnAddress = lob.Address.create(
  name = '',
  address_line1 = '',
  address_line2 = '',
  address_city = '',
  address_state = '',
  address_country = 'US',
  address_zip = ''
)

firstLine = True
for row in csv_f:
  if firstLine:
    firstLine = False
    continue
  print row[1]+' '+row[2]
  try:
    verifiedAddress = lob.Verification.create(
      address_line1=row[4],
      address_zip=row[5],
      address_country='US'
    )
    verifiedRecipientPostcard = lob.Address.create(
      name = row[1]+' '+row[2],
      address_line1 = verifiedAddress.address.address_line1,
      address_line2 = verifiedAddress.address.address_line2,
      address_city = verifiedAddress.address.address_city,
      address_state = verifiedAddress.address.address_state,
      address_country = 'US',
      address_zip = verifiedAddress.address.address_zip,
      email = row[3]
    )
    sentPostcard = lob.Postcard.create(
      name=row[0],
      to_address=verifiedRecipientPostcard,
      from_address=returnAddress,
      template=1,
      full_bleed=1,
      front='pathtofile',
      back='pathtofile'
    )
  except Exception as e: 
    print row[1]+' '+row[2]+str(e)

    data = row[1] + ' ' + row[2]
    errorMessage = str(e)
    writeRow = [data, errorMessage]
    allData.append(writeRow)

with open('errors.csv', 'wb') as w:
  writer = csv.writer(w)
  writer.writerows(allData)
