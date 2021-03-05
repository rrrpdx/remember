#!/usr/bin/python3
import pygsheets
import sys
from datetime import datetime
import re

SECRET_FILE='credentials.json'
SECRET_DIRECTORY='/home/rrrao/.google'
GOOGLE_SHEETS_FILE='daily_log'
def usage():
	print("Usage: remember <line_of_text>")
	print("          - This command will store the date, day of week, tags, line_of_text and parameters in a google sheet")
	print("          - <line_of_text> should likely be in double quotes")
	print("          - Hastags (#) in line of text will be converted to tags")
	print("          - Any urls beginning with http will add a #link to tags")
	print("          - Characters between brackets [] will be parameters and added in consecutive columns") 
	print("          - #P1 tag will cause line to be bold")
	print("          - ~ID will cause line with that ID number to stricken")

def add_tags(row_values,input_string):
	addl_format=[]
	tags=re.findall(r'#\w+',input_string)
	http_tags=re.findall(r'http',input_string)
	if http_tags:
		tags.append("#link")
	row_values.append(" ".join(tags))
	bold=re.findall(r'#P1',input_string)
	if bold:
		addl_format.append('bold')
	return(addl_format)

def add_params(row_values,input_string):
	params=re.findall(r'\[(.*?)\]',input_string)
	row_values.extend(params)

def update_row_color(worksheet):
	colors=["#447c69", "#e9d78e", "#f19670", "#e16552", "#7c9fb0", "#5698c4", "#9abf88"]
	scaled_colors=[]

	for c in colors:
		h=c.lstrip('#')
		scaled_colors.append(tuple(int(h[i:i+2], 16)/255.0 for i in (0, 2, 4)))

	color_index=int(datetime.now().strftime("%w"))
	worksheet.get_row(2,returnas="range").apply_format(pygsheets.Cell('A2'),fields = "userEnteredFormat.backgroundColor",
		cell_json={"userEnteredFormat":{"backgroundColor":{"red":scaled_colors[color_index][0],
		"green":scaled_colors[color_index][1],"blue":scaled_colors[color_index][2]}}})

def update_addl_format(worksheet,addl_format):
	set_bold=False
	for fmt in addl_format:
		if fmt=='bold':
				set_bold=True
				worksheet.get_row(2,returnas="range").apply_format(pygsheets.Cell('A1'),fields = "userEnteredFormat.textFormat.bold",
					cell_json={"userEnteredFormat":{"textFormat":{"bold":True}}})

def update_strikethrough_row(worksheet,input_string):
	row=re.findall(r'~(\d+)',input_string)
	if row:
		cell=worksheet.find(row[0],cols=(1,1),matchEntireCell=True)
		if cell:
			worksheet.get_row(cell[0].row,returnas="range").apply_format(pygsheets.Cell('A1'),fields = "userEnteredFormat.textFormat.strikethrough",
				cell_json={"userEnteredFormat":{"textFormat":{"strikethrough":True}}})

if len(sys.argv)==1:
	usage()
	sys.exit()

gc=pygsheets.authorize(client_secret=SECRET_FILE, credentials_directory=SECRET_DIRECTORY)
sheet=gc.open(GOOGLE_SHEETS_FILE)
worksheet=sheet.sheet1

output_row=[]
output_row.append(str(int(worksheet.get_value('A2'))+1))
output_row.append(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
output_row.append(datetime.now().strftime("%a"))

addl_fmt=add_tags(output_row,sys.argv[1])
output_row.append(sys.argv[1])
add_params(output_row,sys.argv[1])
worksheet.insert_rows(row=1,number=1,values=output_row)
worksheet.get_row(2,returnas="range").clear(fields = "userEnteredFormat.textFormat")

update_row_color(worksheet)
update_addl_format(worksheet,addl_fmt)
update_strikethrough_row(worksheet,sys.argv[1])
print(output_row)
