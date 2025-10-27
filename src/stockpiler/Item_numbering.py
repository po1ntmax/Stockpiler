import csv
import os

class items(object):
	data = []
	numbers = (('CheckImages//num0.png', "0"), ('CheckImages//num1.png', "1"), ('CheckImages//num2.png', "2"),
			   ('CheckImages//num3.png', "3"), ('CheckImages//num4.png', "4"), ('CheckImages//num5.png', "5"),
			   ('CheckImages//num6.png', "6"), ('CheckImages//num7.png', "7"), ('CheckImages//num8.png', "8"),
			   ('CheckImages//num9.png', "9"), ('CheckImages//numk.png', "k+"))
	stockpilecontents = []
	sortedcontents = []
	slimcontents = []
	ThisStockpileName = ""
	FoundStockpileTypeName = ""
	UIimages = []

with open('ItemNumbering.csv', 'rt') as f_input:
	csv_input = csv.reader(f_input, delimiter=',')
	# Skips first line
	header = next(csv_input)
	# Skips reserved line
	reserved = next(csv_input)
	for rowdata in csv_input:
		items.data.append(rowdata)
		if os.path.exists("UI//" + str(rowdata[0]) + ".png"):
			items.UIimages.append((rowdata[0], "UI//" + str(rowdata[0]) + ".png"))
			
            # Load filter values into new array
with open('Filter.csv', 'rt') as f_input:
	csv_input = csv.reader(f_input, delimiter=',')
	# Skips first line
	header = next(csv_input)
	for rowdata in csv_input:
		filter.append(rowdata)

# Matches up filter value with appropriate items in items.data
# for filteritem in range(len(filter)):
for item in range(len(items.data)):
	items.data[item].append(0)

for filteritem in range(len(filter)):
	# print(filter[filteritem])
	try:
		# print(filter[filteritem])
		for item in range(len(items.data)):
			if filter[filteritem][0] == items.data[item][0]:
				items.data[item][19] = filter[filteritem][1]
				# items.data[item].extend(filter[filteritem][1])
	except Exception as e:
		print("Exception: ", e)
		print("failed to apply filters to items.data")