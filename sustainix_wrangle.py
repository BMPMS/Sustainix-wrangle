import csv
import sys
import json
import pandas as pd
import re


pattern =["US\\$","\\\t",",","%"]


#import the excel spreadsheet
xls_file = pd.ExcelFile('sustainix_shortnames.xlsx')
print(xls_file.sheet_names)
df = xls_file.parse('numbers')


#Clean the columns with US$ or \t or % or ,
for l in list(df.columns.values):

    for x in range(0,3):
        for i,row in df.iterrows():
            row[l] = re.sub(pattern[x], "", str(row[l]))


#open a new json file
jsonfile = open('sustainix.json', 'w')

#set the starter rows for the visual
startrows =['rank16','company','market_cap']

#count the number of sectors
sectors = len(df.groupby('sector'))
sectorcount = 0

jsonfile.write('{"sustain":"all_data","children":[')
for n, group in df.groupby('sector'):
    #for each sector write the name
    sect_df = df[df['sector']==n]
    jsonfile.write('{"sector":"')
    jsonfile.write(n)
    #and then teh children
    jsonfile.write('","children":[')
    rowcount = 0
    for i,row in sect_df.iterrows():
        jsonfile.write('{"sector":"' + str(row['rank16']) + '"')
        jsonfile.write(',"size":"' + str(row['market_cap'])+ '"')
        jsonfile.write(',"company":"' + row['company'] + '"')
        for l in list(df.columns.values):
            if l not in startrows:
                jsonfile.write(',"' + l + '":"' + str(row[l]) + '"')
        jsonfile.write('}')
        rowcount = rowcount + 1
        if rowcount < len(group):
            jsonfile.write(',')
    jsonfile.write(']}')
    sectorcount = sectorcount + 1
    if sectorcount < sectors:
        jsonfile.write(',')
jsonfile.write(']}')
