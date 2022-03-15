#!/usr/bin/env python3

from tcalendar_old import Tcalendar as tc

def main():
	"""Testing the tclaendar module."""

	def full_year():
		while True:
			try:
				year = int(input("Year:  "))
			except ValueError:
				print("Please make sure you typed right!\n")
			else:
				print()
				for i in range(1,13):
					a = tc.calendar(year, i)
					print(a)
				break
	
	def single_month():
		while True:
			try:
				year = int(input("Year:  "))
			except ValueError:
				print("Please make sure you typed right!\n")
				continue
			while True:
				month = input("Month: ")
				try:
					month = int(month)
				except ValueError:
					pass
				if type(month) == int:
					if month < 0 or month > 12:
						print("Hey there, the month you typed is not valid.\n")
						continue
				break
			print()
			a = tc.calendar(year, month)
			print(a)
			break

	# ask_user:
	while True:
		print("1. Entire Year")
		print("2. Single Month")
		try:
			response = int(input("Enter Choice (1/2): "))
		except ValueError:
			print("Make sure you typed right!\n")
		else:
			if response < 3 and response > 0:
				if response == 1:
					print()
					full_year()
					break
				elif response == 2:
					print()
					single_month()
					break
			else:
				print("The option you selected doesn't exist.\n")

if __name__ == '__main__':
	main()
