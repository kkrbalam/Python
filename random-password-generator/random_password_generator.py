#!/usr/bin/python
#-------------------------------------------------------------------------------------
# Created by: Krishna Balam
# Date: 25-July-2015
# Purpose: Random password generator
# Change Log:
# Date               Name                  Description
#----------------------------------------------------------------------------
# 07/25/2015         Krishna Balam         Initial Creation
#
#-------------------------------------------------------------------------------------

import string
import random
import itertools

#----------------------------------------------------------------------
#-------------------Function FlagValidation----------------------------
#----------------------------------------------------------------------

# Validate flag value, and see if user enteres yes, no, y, n as choices
def FlagValidation(flagValue):
	# convert all to upper case to reduce comparison combinations
	if flagValue.upper() in ['Y', 'YES', 'N', 'NO']:
		# if flag is good return 1 else 0
		return 1
	else:
		return 0

#----------------------------------------------------------------------
#-------------------Function seedPasswordString------------------------
#----------------------------------------------------------------------

# generate password seed based on the choices selected by user
def seedPasswordString(upperCase, lowerCase, numbers):
	# convert the flags into boolean 
	flagsString = [upperCase.upper()[:1] == 'Y', lowerCase.upper()[:1] == 'Y',  numbers.upper()[:1] == 'Y' ]
	
	# use imported python string methos to get all letters and numbers
	pwdStrings = [ string.ascii_uppercase, string.ascii_lowercase, string.digits]
	passwordSeed = ''
	
	# Loop through flag boolean list and select only strings that have corresponding flag as true and concatenate that to seed string
	for i in range(len(flagsString)):
		if flagsString[i]:
			passwordSeed = passwordSeed + ''.join(pwdStrings[i])
	
	# For debugging	
	#print ("Your password seed is: %s" % passwordSeed)
	
	# return seed string
	return passwordSeed

#----------------------------------------------------------------------
#-------------------Function PasswordString----------------------------
#----------------------------------------------------------------------

# Returns random password after selecting random characters from seed string for the size required
def PasswordString (size, passwordSeed):
	# returns random password
	return ''.join(random.choice(passwordSeed) for _ in range(size))

#---------------------------------------------------------------------
# Start Main Program here
#---------------------------------------------------------------------
# Asks user for for the size, and what to include for password (uppercase, lowercase and numbers)
# and outputs random password for desired size


# Welcome the user
print ("Welcome to random password generation program")

#-------------------------------------------------------------------------------------------------------------------
#------------------------------------------- 1. Get password size from user ----------------------------------------
#-------------------------------------------------------------------------------------------------------------------

# Loop through the question until right value gets entered for size
while True:
	try:
		# since input reads the data as character string, we need to use int() methos to convert it into integer
		pwdSize = int(input("what is the size of password that is required? "))
		
		# If int() method errors out while converting value then ask user one more time to enter value
	except ValueError:
		print ("It is not an integer value !!! Please enter integer value.")
		continue
		
		# If user enters 0 or a negative number then tell him to enter positive number, else take the value as size
	else:
		if pwdSize <= 0:
			print ("It is not a positive integer value !!! Please enter integer value.")
			continue
		else:
			print("size of the password being built is %i" % pwdSize)
			break

#-------------------------------------------------------------------------------------------------------------------
#------------------------------------------- 2. Get upper case flag from user ----------------------------------------
#-------------------------------------------------------------------------------------------------------------------

# Loop through the question until right value gets entered for uppercase flag
while True:
	# Get input from user using input method
	uppercaseFlag = input("Enter 'Y' if you want uppercase letters, 'N' if you don't want? ")
	# Use the function FlagValidation to see if user entered correct flag or not
	uc_validation = FlagValidation(uppercaseFlag)
	
	# If user entered right flag then take it as flag
	if uc_validation == 1:
		print("You have said %s for including uppercase letters" % uppercaseFlag)
		break
	else:
		# If user didn't enter right flag then ask him to reenter
		print("You didn't select proper choice, please reenter choice")
		continue

#-------------------------------------------------------------------------------------------------------------------
#------------------------------------------- 3. Get lower case flag from user ----------------------------------------
#-------------------------------------------------------------------------------------------------------------------

# Loop through the question until right value gets entered for lowercase flag
while True:
	# Get input from user using input method
	lowercaseFlag = input("Enter 'Y' if you want lowercase letters, 'N' if you don't want? ")
	# Use the function FlagValidation to see if user entered correct flag or not
	lc_validation = FlagValidation(lowercaseFlag)
	
	# If user entered right flag then take it as flag
	if lc_validation == 1:
		print("You have said %s for including lowercase letters" % lowercaseFlag)
		break
	else:
		# If user didn't enter right flag then ask him to reenter
		print("You didn't select proper choice, please reenter choice")
		continue	

#-------------------------------------------------------------------------------------------------------------------
#------------------------------------------- 4. Get number flag from user ----------------------------------------
#-------------------------------------------------------------------------------------------------------------------

# Loop through the question until right value gets entered for number flag
while True:
	# Get input from user using input method
	numberFlag = input("Enter 'Y' if you want numbers in the password, 'N' if you don't want? ")
	# Use the function FlagValidation to see if user entered correct flag or not
	number_validation = FlagValidation(numberFlag)
	
	# If user entered right flag then take it as flag
	if number_validation == 1:
		print("You have said %s for including numbers" % numberFlag)
		break
	else:
		# If user didn't enter right flag then ask him to reenter
		print("You didn't select proper choice, please reenter choice")
		continue	

#-------------------------------------------------------------------------------------------------------------------
#------------------------------------------- 5. Get the seed string based on user choices---------------------------
#-------------------------------------------------------------------------------------------------------------------

# Get the seed string based on the choices made by the user using seedPasswordString function
passwordSeedString = seedPasswordString(uppercaseFlag, lowercaseFlag, numberFlag)


#-------------------------------------------------------------------------------------------------------------------
#------------------------------------------- 6. Generate random password based on user choices----------------------
#-------------------------------------------------------------------------------------------------------------------

# Generate random password based on user choices and seed string using PasswordString function
randomPassword = PasswordString(pwdSize, passwordSeedString)

#-------------------------------------------------------------------------------------------------------------------
#------------------------------------------- 7. Print password generated -------------------------------------------
#-------------------------------------------------------------------------------------------------------------------

print ("Your random password is: " + randomPassword)