# Basic Info
"""
Splits language file into translated and untranslated by comparing your langpack with its base_language (base example: https://translations.telegram.org/en)
--> Requires a recently exported file of the base language for comparison
--> Supports '.xml' and '.strings' translation files
"""

# DO NOT EDIT THE CODE BELOW (unless you know Python and RegEx)

# Imports
import xml.etree.ElementTree as ET
import re
import argparse

# Command-line info and argument parsing
arg_parser = argparse.ArgumentParser(
	description='Compares your langpack with its base language, and produces 2 files for translated and untranslated strings.')
arg_parser.add_argument(
	'--lang', metavar='Langfile[.xml|.strings]', type=str, required=True,
	help="Your language's exported file (.xml or .strings)")
arg_parser.add_argument(
	'--base', metavar='Base_Language[.xml|.strings]', type=str, required=True,
	help="The base language's exported file")
arg_parser.add_argument(
	'--untranslated', action="store_true",
	help='Show untranslated strings.')
arg_parser.add_argument(
	'--translated', action="store_true",
	help='Show translated strings.')

args = arg_parser.parse_args()
lang_file = str(args.lang)
base_lang = str(args.base)
print("\n\nFiles Used:\n--lang\t"+lang_file+"\n--base\t"+base_lang)

# Variables
global tree, btree, total, skipped
total = 0
skipped = list()

# Checks if {given_file} is in XML format
def isXML(given_file):
	# (re.search(r'.*\.xml$', given_file, re.UNICODE) is not None)
	try:
		temp = ET.parse(given_file)
	except FileNotFoundError:
		print("\nError:\n\tThe file \'"+given_file+"' does not exist.\n")
		exit()
	else:
		del temp
		return True

# Checks if {given_file} is in .strings format
def isStrings (given_file):
	try:
		temp = open(given_file, 'r').read()
	except FileNotFoundError:
		print("\nError:\n\tThe file \'"+given_file+"' does not exist.\n")
		exit()
	result = (len(re.findall(r'".*"\s=\s".*";', temp)) > 0)
	del temp
	return result

# Prints summary
def printSummary():
	print('\nSummary:')
	print('\t'+str(translatedCount-1),'translated')
	print('\t'+str(untranslatedCount-1),'untranslated')
	print('\t'+str(strCount-1),'strings in total')
	print('\t'+str(len(skipped)),'skipped (did not split)')
	print("\nFiles produced:")
	print("\t"+translatedFileName)
	print("\t"+untranslatedFileName)
	print('\nImport the translated file\n')

# Algo for XML replacer
if(isXML(lang_file) & isXML(base_lang)):
	global tree, btree
	tree = ET.parse(lang_file) # also used as translated tree
	btree = ET.parse(base_lang) # also used as untranslated tree
	root = tree.getroot()
	broot = btree.getroot()
	if(args.translated):
		print('\n\nThese strings are translated:\n')
	if(args.untranslated):
		print('\n\nThese strings are untranslated:\n')
	strCount = 1
	translatedCount = 1
	untranslatedCount = 1
	for string in root.findall('string'):
		string_name = string.get('name')
		# string.text
		if(string_name == 'language_code' or string_name == "LanguageCode"):
			skipped.append(string_name)
			strCount += 1
			continue # skip
		for bstring in broot.findall('string'):
			bstring_name = bstring.get('name')
			# bstring.text
			if(string_name == bstring_name):
				if(string.text == bstring.text):
					untranslatedCount += 1
					root.remove(string)
					if(args.untranslated):
						print('\n'+str(untranslatedCount)+'. '+bstring.text+'')
				else:
					translatedCount += 1
					broot.remove(bstring)
					if(args.translated):
						print('\n'+str(translatedCount)+'. '+string.text+'')
				break
			# broot
		strCount += 1
		# root
	#end replacing strings

	# using lang_file's name
	translatedFileName = str(re.sub(r'(android_x|android)_(.*)[_.].*xml', r'\1_\2_[translated].xml', lang_file, flags=re.I))
	untranslatedFileName = str(re.sub(r'(android_x|android)_(.*)[_.].*xml', r'\1_\2_[untranslated].xml', lang_file, flags=re.I))
	#
	tree.write(translatedFileName, xml_declaration=True, encoding='Unicode')
	btree.write(untranslatedFileName, xml_declaration=True, encoding='Unicode')
	#
	print('\nSkipped:')
	for i in range(0, len(skipped)):
		print('\t<'+skipped[i]+'>')
	#
	printSummary()
	# CLEANUP MEMORY
	re.purge()
	del string, bstring, broot, root, btree, tree, ET # xml memory
	#
elif(isStrings(lang_file) & isStrings(base_lang)): # if .strings file
	global dot_strings, base_strings
	#
	dot_strings = open(lang_file, 'r').read()
	base_strings = open(base_lang, 'r').read()
	# using lang_file's name
	translatedFileName = re.sub(r'(tdesktop|macos|ios)_(.*)[_.].*strings', r'\1_\2_[translated].strings', lang_file, flags=re.I)
	untranslatedFileName = re.sub(r'(tdesktop|macos|ios)_(.*)[_.].*strings', r'\1_\2_[untranslated].strings', lang_file, flags=re.I)
	#
	translatedStringsFile = open(translatedFileName, 'w', encoding='UTF-8')
	untranslatedStringsFile = open(untranslatedFileName, 'w', encoding='UTF-8')
	#
	if(args.translated):
		print('\n\nThese strings are translated:\n')
	if(args.untranslated):
		print('\n\nThese strings are untranslated:\n')
	#
	strCount = 0
	translatedCount = 1
	untranslatedCount = 1
	for match in re.finditer(r'(?<!.)"(.*)"\s=\s"(.*)";\n', dot_strings): #no preceeding chars
		strName = match.groups()[0]
		strValue = match.groups()[1]
		for bmatch in re.finditer(r'(?<!.)"(.*)"\s=\s"(.*)";\n', base_strings): #no preceeding chars
			bStrName = bmatch.groups()[0]
			bStrValue = bmatch.groups()[1]
			if(strName == bStrName):
				if(strValue == bStrValue):
					untranslatedCount += 1
					untranslatedStringsFile.write("\""+strName+"\" = \""+strValue+"\";\n")
					if(args.untranslated):
						print('\n'+str(untranslatedCount)+'. '+strName+'')
				else:
					translatedCount += 1
					translatedStringsFile.write("\""+strName+"\" = \""+bStrValue+"\";\n")
					if(args.translated):
						print('\n'+str(translatedCount)+'. '+bStrName+'')
				break # found match
			# base_strings
		strCount += 1
		# dot_strings
	translatedStringsFile.close()
	untranslatedStringsFile.close()
	#
	printSummary()
	# CLEANUP MEMORY
	re.purge()
	del dot_strings, base_strings, isStrings
# Both files not same
elif(isXML(lang_file) or isStrings(lang_file)):
	if(isStrings(base_lang) or isXML(base_lang)):
		print("\nError: Both files need to be of same type.")
		print("Please export a translation file from your base language as well.")
		print('How to export --> https://t.me/TranslationsTalk/1759)\n') #FIXME
# Something's not right
else:
	print('\n\nwow, how did you get here?!')
	print('Please send below output to t.me/Rondevous:\n')
	print("Files Used:\n--lang\t"+lang_file+"\n--base\t"+base_lang)
	print("If you don't mind, please send the above files as well.")