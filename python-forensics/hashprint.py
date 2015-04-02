# python forensics
# Simple program to generate SHA256
# one way vrypographic has of a given string

# step 1: import hashlib 
import hashlib

# print message to the user
print
print "Simple program to generate SHA-256 for a given string"
print

# define string with desired text
myString = "Python Forensics"

# create an object named hash with sha256 type
hash = hashlib.sha256()

# utilize update method of hash object to generate SHA256 hash of given string
hash.update(myString)

#obtain hex values of hash
hexSHA256 = hash.hexdigest()

# print sha256
print "SHA256 has for the string is: " + hexSHA256.upper()
print 