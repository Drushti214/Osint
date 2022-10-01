#!/usr/bin/python
from googlesearch import search
from socket import timeout
import http
from bs4 import BeautifulSoup
import urllib.request
from urllib.request import URLError, HTTPError
import random
import os
import time
import sqlite3
from sqlite3 import Error
import sys
import re
from fake_useragent import UserAgent
from socket import timeout
from urllib.error import HTTPError, URLError
from datetime import datetime
import csv

imageExt = (".jpeg", ".jpg", ".exif", ".tif", ".tiff", ".gif", ".bmp", ".png", ".ppm",
			".pgm", ".pbm", ".pnm", ".webp", ".hdr", ".heif", ".bat", ".bpg", ".cgm", ".svg")
ua = UserAgent()

count_email_in_phrase = 0


def menu():
	global count_email_in_phrase
	count_email_in_phrase = 0

	try:
		clear()
		print("1 - Search only in the entered URL")
		print("2 - Search in a url (Two Levels)")
		print("3 - Search phrase in google")
		print("4 - Same as option 3 but with a list of keywords")
		print("5 - List emails")
		print("6 - Save emails in .txt file")
		print("7 - Save emails in .csv file")
		print("8 - Delete Emails from Data Base")
		print("9 - Exit")
		print("")

		option = input("Enter option : ")
		if (option == "1"):
			print("")
			print ("Example URL: http://www.google.com")
			url = str(input("Enter URL: "))
			extractOnlyUrl(url)
			input("Press enter key to continue")
			menu()

		if (option == "2"):
			print("")
			print ("Example URL: http://www.google.com")
			url = str(input("Enter URL: "))
			extractUrl(url)
			input("Press enter key to continue")
			menu()

		elif (option == "3"):
			print("")
			phrase = str(input("Enter a phrase to search: "))
			print ("***Warning: The amount of results chosen impacts the execution time***")
			cantRes = int(input("Number of Google links to explore: "))
			print ("")
			extractPhraseGoogle(phrase, cantRes)
			input("Press enter key to continue")
			menu()

		elif (option == "4"):
			print("Developing...")
			input("Press enter key to continue")
			menu()
   
		elif (option == "5"):
			print ("")
			print ("1 - Select a phrase")
			print ("2 - Insert a URL")
			print ("3 - All emails")
			opcLists = input("Enter option : ")
			
			if (opcLists == "1"):
				listsPorPhrase("Emails.db")

			elif (opcLists == "2"):
				listsPorUrl("Emails.db")

			elif (opcLists == "3"):
				listsTodo("Emails.db")

			else:
				print("Incorrect option, return to the menu...")
				time.sleep(2)
				menu()

		elif (option == "6"):
			print("")
			print("1 - Save emails from a phrase")
			print("2 - Save emails from a URL")
			print("3 - Save all emails")
			opcGuardar = input("Enter Option: ")
			
			if(opcGuardar == "1"):
				phrase = str(input("Enter phrase: "))
				guardarPhrase("Emails.db", phrase)
				
			elif(opcGuardar == "2"):
				print("Example URL: http://www.google.com")
				url = str(input("Insert URL: "))
				guardarUrl("Emails.db", url)
				
			elif(opcGuardar == "3"):
				guardarAll("Emails.db")
				
			else:
				print("Incorrect option, return to the menu...")
				time.sleep(2)
				menu()

		elif (option == "7"):
			guardarCsv("Emails.db")

		elif (option == "8"):
			print("")
			print("1 - Delete emails from a specific URL")
			print("2 - Delete emails from a specific phrase")
			print("3 - Delete all Emails")
			op = input("Enter option: ")

			if(op == "1"):
				print("Example URL: http://www.google.com")
				url = str(input("Insert URL: "))
				deleteUrl("Emails.db", url.strip())
			
			elif(op == "2"):
				phrase = str(input("Insert Phrase: "))
				deletePhrase("Emails.db", phrase.strip())

			elif(op == "3"):
				deleteAll("Emails.db")

			else:
				print("Incorrect option, return to the menu...")
				time.sleep(2)
				menu()
		
		elif (option == "9"):
			sys.exit(0)

		else:			
			print("")
			print ("Select a correct option - ")
			time.sleep(3)
			clear()
			menu()
	
	except KeyboardInterrupt:
		input("Press return to continue")
		menu()

	except Exception as e:
		print (e)
		input("Press enter to continue")
		menu()


def insertEmail(db_file, email, phrase, url):
	try:
		conn = sqlite3.connect(db_file)
		c = conn.cursor()
		c.execute("INSERT INTO emails (phrase, email, url) VALUES (?,?,?)", (phrase, email, url))
		conn.commit()
		conn.close()

	except Error as e:
		print(e)
		input("Press enter to continue")
		menu()

	finally:
		conn.close()


def searchEmail(db_file, email, phrase):
	try:
		conn = sqlite3.connect(db_file)
		c = conn.cursor()
		sql = 'SELECT COUNT(*) FROM emails where email LIKE "%' + str(email) + '%" AND phrase LIKE "%' + str(phrase) + '%"'
		result = c.execute(sql).fetchone()
		conn.close()

		return (result[0])

	except Error as e:
		print(e)
		input("Press enter to continue")
		menu()

	finally:
		conn.close()

def crearTabla(db_file, delete = False):
	try:
		conn = sqlite3.connect(db_file)
		c = conn.cursor()
		
		if(delete == True):
			c.execute('drop table if exists emails')			

		sql = '''create table if not exists emails 
				(ID INTEGER PRIMARY KEY AUTOINCREMENT,
				 phrase varchar(500) NOT NULL,
				 email varchar(200) NOT NULL,
				 url varchar(500) NOT NULL)'''

		c.execute(sql)
		conn.close()

	except Error as e:
		print(e)
		input("Press enter to continue")
		menu()

	finally:
		conn.close()

def guardarUrl(db_file, url):
	try:
		conn = sqlite3.connect(db_file)
		c = conn.cursor()
		sql = 'SELECT COUNT(*) FROM emails WHERE url = "' + url.strip() + '"'
		result = c.execute(sql).fetchone()

		if(result[0] == 0):
			print("There are no emails to erase")
			input("Press enter to continue")
			menu()
			
		else:
			nameFile = str(input("Name of the file: "))
			print("")
			print("Save file, please wait...")
			
			f = open(nameFile.strip() + ".txt", "w")
		
			c.execute('SELECT * FROM emails WHERE url = "' + url.strip() + '"')
			
			count = 0
			
			for i in c:
				count += 1
				f.write("")
				f.write("Number: " + str(count) + '\n')
				f.write("Phrase: " + str(i[1]) + '\n')
				f.write("Email: " + str(i[2]) + '\n')
				f.write("Url: " + str(i[3]) + '\n')
				f.write("-------------------------------------------------------------------------------" + '\n')
				
			f.close()
			
		conn.close()
		input("Press enter to continue")
		menu()
		
	except Error as e:
		print(e)
		input("Press enter to continue")
		menu()
		
	except Exception as o:
		print(o)
		input("Press enter to continue")
		menu()
		
	finally:
		conn.close()


def guardarPhrase(db_file, phrase):
	try:
		conn = sqlite3.connect(db_file)
		c = conn.cursor()
		sql = 'SELECT COUNT(*) FROM emails WHERE phrase = "' + phrase.strip() + '"'
		result = c.execute(sql).fetchone()

		if(result[0] == 0):
			print("There are no emails to erase")
			input("Press enter to continue")
			menu()
			
		else:
			nameFile = str(input("Name of the file: "))
			print("")
			print("Save file, please wait...")
			
			f = open(nameFile.strip() + ".txt", "w")
		
			c.execute('SELECT * FROM emails WHERE phrase = "' + phrase.strip() + '"')
			
			count = 0
			
			for i in c:
				count += 1
				f.write("")
				f.write("Number: " + str(count) + '\n')
				f.write("Phrase: " + str(i[1]) + '\n')
				f.write("Email: " + str(i[2]) + '\n')
				f.write("Url: " + str(i[3]) + '\n')
				f.write("-------------------------------------------------------------------------------" + '\n')
				
			f.close()
			
		conn.close()
		input("Press enter to continue")
		menu()
			
	except Error as e:
		print(e)
		input("Press enter to continue")
		menu()
		
	except Exception as o:
		print(o)
		input("Press enter to continue")
		menu()
		
	finally:
		conn.close()


def guardarAll(db_file):
	try:
		conn = sqlite3.connect(db_file)
		c = conn.cursor()
		sql = 'SELECT COUNT(*) FROM emails'
		result = c.execute(sql).fetchone()

		if(result[0] == 0):
			print("There are no emails to save")
			input("Press enter to continue")
			menu()
			
		else:
			nameFile = str(input("Name of the file: "))
			print("")
			print("Save file, please wait...")
			
			f = open(nameFile + ".txt", "w")
		
			c.execute('SELECT * FROM emails')
			
			count = 0
			
			for i in c:
				count += 1
				f.write("")
				f.write("Number: " + str(count) + '\n')
				f.write("Phrase: " + str(i[1]) + '\n')
				f.write("Email: " + str(i[2]) + '\n')
				f.write("Url: " + str(i[3]) + '\n')
				f.write("-------------------------------------------------------------------------------" + '\n')
				
			f.close()
			
		conn.close()
		
		input("Press enter to continue")
		menu()
		
	except Error as e:
		print(e)
		input("Press enter to continue")
		menu()
		
	except Exception as o:
		print(o)
		input("Press enter to continue")
		menu()
		
	finally:
		conn.close()

def deleteUrl(db_file, url):
	try:
		conn = sqlite3.connect(db_file)
		c = conn.cursor()
		sql = 'SELECT COUNT(*) FROM emails WHERE url = ' + '"' + url + '"'
		result = c.execute(sql).fetchone()
		
		if(result[0] == 0):
			print("There are no emails to erase")
			input("Press enter to continue")
			menu()
			
		else:
			option = str(input("Are you sure you want to delete " + str(result[0]) + " emails? Y/N :"))
			
			if(option == "Y" or option == "y"):
				c.execute("DELETE FROM emails WHERE url = " + '"' + url + '"')
				conn.commit()

				print("Emails deleted")
				input("Press enter to continue")
				menu()
				
			elif(option == "N" or option == "n"):
				print("Canceled operation, return to the menu ...")
				time.sleep(2)
				menu()
				
			else:
				print("Select a correct option")
				time.sleep(2)
				deleteUrl(db_file, url)
				
		conn.close()
		
	except Error as e:
		print(e)
		input("Press enter to continue")
		menu()
		
	finally:
		conn.close()


def deletePhrase(db_file, phrase):
	try:
		conn = sqlite3.connect(db_file)
		c = conn.cursor()
		sql = 'SELECT COUNT(*) FROM emails WHERE phrase = ' + '"' + phrase + '"'
		result = c.execute(sql).fetchone()
		
		if(result[0] == 0):
			print("There are no emails to erase")
			input("Press enter to continue")
			menu()
			
		else:
			option = str(input("Are you sure you want to delete " + str(result[0]) + " emails? Y/N :"))
			
			if(option == "Y" or option == "y"):
				c.execute("DELETE FROM emails WHERE phrase = " + '"' + phrase + '"')
				conn.commit()

				print("Emails deleted")
				input("Press enter to continue")
				menu()
				
			elif(option == "N" or option == "n"):
				print("Canceled operation, return to the menu ...")
				time.sleep(2)
				menu()
				
			else:
				print("Select a correct option")
				time.sleep(2)
				deleteUrl(db_file, phrase)
				
		conn.close()
				
	except Error as e:
		print(e)
		input("Press enter to continue")
		menu()
		
	finally:
		conn.close()

# Borra todos los correos
def deleteAll(db_file):
	try:
		conn = sqlite3.connect(db_file)
		c = conn.cursor()
		sql = 'SELECT COUNT(*) FROM emails'
		result = c.execute(sql).fetchone()

		if(result[0] == 0):
			print("There are no emails to erase")
			input("Press enter to continue")
			menu()
		
		
		else:			
			option = str(input("Are you sure you want to delete " + str(result[0]) + " emails? Y/N :"))
			
			if(option == "Y" or option == "y"):
				c.execute("DELETE FROM emails")
				conn.commit()
				crearTabla("Emails.db", True)
				print("All emails were deleted")
				input("Press enter to continue")
				menu()

			elif(option == "N" or option == "n"):
				print("Canceled operation, return to the menu ...")
				time.sleep(2)
				menu()

			else:
				print("Select a correct option")
				time.sleep(2)
				deleteAll(db_file)
				
		conn.close()

	except Error as e:
		print(e)
		input("Press enter to continue")
		menu()

	finally:
		conn.close()

def listsPorPhrase(db_file):
	try:
		phrase = str(input("Inserter phrase: "))
		conn = sqlite3.connect(db_file)
		c = conn.cursor()
		
		sql = 'SELECT COUNT(*) FROM emails WHERE phrase LIKE "%' + phrase.strip() + '%"'
		result = c.execute(sql).fetchone()

		if(result[0] == 0):
				print("No results for the specified url")
				input("Press enter to continue")
				menu()
				
		else:
			c.execute('SELECT * FROM emails WHERE phrase LIKE "%' + phrase.strip() + '%"')

			for i in c:

				print ("")
				print ("Number: " + str(i[0]))
				print ("Phrase: " + str(i[1]))
				print ("Email: " + str(i[2]))
				print ("Url: " + str(i[3]))
				print ("-------------------------------------------------------------------------------")

		conn.close()
		
		print ("")
		input("Press enter key to continue")
		menu()
		
	except Error as e:
		print(e)
		input("Press enter to continue")
		menu()
	
	finally:
		conn.close()

def listsPorUrl(db_file):
	try:
		print("Example URL: http://www.google.com ")
		url = str(input("Insert a Url: "))
		conn = sqlite3.connect(db_file)
		c = conn.cursor()

		sql = 'SELECT COUNT(*) FROM emails WHERE url LIKE "%' + url.strip() + '%"'
		result = c.execute(sql).fetchone()

		if(result[0] == 0):
				print("No results for the specified url")
				input("Press enter to continue")
				menu()

		else:
			c.execute('SELECT * FROM emails WHERE url LIKE "%' + url.strip() + '%"')

			for i in c:

				print ("")
				print ("Number: " + str(i[0]))
				print ("Phrase: " + str(i[1]))
				print ("Email: " + str(i[2]))
				print ("Url: " + str(i[3]))
				print ("-------------------------------------------------------------------------------")

		conn.close()
		print ("")
		input("Press enter key to continue")
		menu()

	except Error as e:
		print(e)
		input("Press enter to continue")
		menu()

	finally:
		conn.close()

def listsTodo(db_file):
	try:
		conn = sqlite3.connect(db_file)
		c = conn.cursor()

		sql = 'SELECT COUNT(*) FROM emails'
		result = c.execute(sql).fetchone()

		if(result[0] == 0):
			print("The data base is Empty")
			input("Press enter to continue")
			menu()

		c.execute("SELECT * FROM emails")

		for i in c:

			print ("")
			print ("Number: " + str(i[0]))
			print ("Phrase: " + str(i[1]))
			print ("Email: " + str(i[2]))
			print ("Url: " + str(i[3]))
			print ("-------------------------------------------------------------------------------")

		conn.close()

		print ("")
		input("Press enter key to continue")
		menu()

	except Error as e:
		print(e)
		input("Press enter to continue")
		menu()

	finally:
		conn.close()

def extractOnlyUrl(url):
	try:
		print ("Searching emails... please wait")

		count = 0
		listUrl = []

		req = urllib.request.Request(
    			url,
    			data=None,
    			headers={
        		'User-Agent': ua.random
    		})

		try:
			conn = urllib.request.urlopen(req, timeout=10)

		except timeout:
			raise ValueError('Timeout ERROR')

		except (HTTPError, URLError):
			raise ValueError('Bad Url...')

		status = conn.getcode()
		contentType = conn.info().get_content_type()

		if(status != 200 or contentType == "audio/mpeg"):
			raise ValueError('Bad Url...')

		html = conn.read().decode(conn.headers.get_content_charset())

		emails = re.findall(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}', html)

		for email in emails:
			if (email not in listUrl and not email.endswith(imageExt)):
				count += 1
				print(str(count) + " - " + email)
				listUrl.append(email)
				if(searchEmail("Emails.db", email, "specific Search") == 0):
					insertEmail("Emails.db", email, "specific Search", url)

		print("")
		print("***********************")
		print(str(count) + " emails were found")
		print("***********************")

	except KeyboardInterrupt:
		input("Press return to continue")
		menu()

	except Exception as e:
		print (e)
		input("Press enter to continue")
		menu()
def extractUrl(url):
	print ("Searching emails... please wait")
	print ("This operation may take several minutes")
	try:
		count = 0
		listUrl = []
		req = urllib.request.Request(
    			url,
    			data=None,
    			headers={
        		'User-Agent': ua.random
    		})

		try:
			conn = urllib.request.urlopen(req, timeout=10)

		except timeout:
			raise ValueError('Timeout ERROR')

		except (HTTPError, URLError):
			raise ValueError('Bad Url...')

		status = conn.getcode()
		contentType = conn.info().get_content_type()

		if(status != 200 or contentType == "audio/mpeg"):
			raise ValueError('Bad Url...')

		html = conn.read().decode(conn.headers.get_content_charset())
		
		emails = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}", html)
		print ("Searching in " + url)
		
		for email in emails:
			if (email not in listUrl and not email.endswith(imageExt)):
					count += 1
					print(str(count) + " - " + email)
					listUrl.append(email)
					if(searchEmail("Emails.db", email, "specific Search") == 0):
						insertEmail("Emails.db", email, "specific Search", url)

		soup = BeautifulSoup(html, "lxml")
		links = soup.find_all('a')

		print("They will be analyzed " + str(len(links) + 1) + " Urls..." )
		time.sleep(2)

		for tag in links:
			link = tag.get('href', None)
			if link is not None:
				try:
					print ("Searching in " + link)
					if(link[0:4] == 'http'):
						req = urllib.request.Request(
							link, 
							data=None, 
							headers={
							'User-Agent': ua.random
							})

						try:
							f = urllib.request.urlopen(req, timeout=10)

						except timeout:
							print("Bad Url..")
							time.sleep(2)
							pass

						except (HTTPError, URLError):
							print("Bad Url..")
							time.sleep(2)
							pass

						status = f.getcode()
						contentType = f.info().get_content_type()

						if(status != 200 or contentType == "audio/mpeg"):
							print("Bad Url..")
							time.sleep(2)
							pass

						s = f.read().decode('utf-8')

						emails = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}", s)

						for email in emails:
							if (email not in listUrl and not email.endswith(imageExt)):
								count += 1
								print(str(count) + " - " + email)
								listUrl.append(email)
								if(searchEmail("Emails.db", email, "specific Search") == 0):
									insertEmail("Emails.db", email, "specific Search", url)

				except Exception:
					pass
		print("")
		print("***********************")
		print("Finish: " + str(count) + " emails were found")
		print("***********************")
		input("Press return to continue")
		menu()

	except KeyboardInterrupt:
		input("Press return to continue")
		menu()

	except Exception as e:
		print(e)
		input("Press enter to continue")
		menu()


def extractPhraseGoogle(phrase, cantRes):
	print ("Searching emails... please wait")
	print ("This operation may take several minutes")
	try:
		listUrl = []
		listEmails = []

		for url in search(phrase, stop=cantRes):
			listUrl.append(url)

		for i in listUrl:
			try:
				req = urllib.request.Request(
							i,
							data=None,
							headers={
							'User-Agent': ua.random
							})
				try:
					conn = urllib.request.urlopen(req)
				except timeout:
					print("Bad Url..")
					time.sleep(2)
					pass
				except(HTTPError, URLError):
					print("Bad Url..")
					time.sleep(2)
					pass

				status = conn.getcode()
				contentType = conn.info().get_content_type()

				if(status != 200 or contentType == "audio/mpeg"):
					print("Bad Url..")
					time.sleep(2)
					pass

				html = conn.read()

				soup = BeautifulSoup(html, "lxml")
				links = soup.find_all('a')

				print("They will be analyzed " + str(len(links) + 1) + " Urls..." )
				time.sleep(2)

				for tag in links:
					link = tag.get('href', None)
					if link is not None:
						searchSpecificLink(link, listEmails, phrase)

			except urllib.error.URLError as e:
				print("Problems with the url:" + i)
				print(e)
				pass
			except (http.client.IncompleteRead) as e:
				print(e)
				pass
			except Exception as e:
				print(e)
				pass

		print("")
		print("*******")
		print("Finish")
		print("*******")
		input("Press return to continue")
		menu()

	except KeyboardInterrupt:
		input("Press return to continue")
		menu()

	except Exception as e:
		print(e)
		input("Press enter to continue")
		menu()

def extractKeywordsList(txtFile):
	f = open(txtFile, 'r')
	text = f.read()
	keywordList = text.split(sep='\n')
	for key in keywordList:
    		print(key)


def clear():
	try:
		if os.name == "posix":
			os.system("clear")
		elif os.name == "ce" or os.name == "nt" or os.name == "dos":
			os.system("cls")
	except Exception as e:
		print(e)
		input("Press enter to continue")
		menu()

def searchSpecificLink(link, listEmails, phrase):
	try:

		global count_email_in_phrase

		print("Searching in " + link)
		if(link[0:4] == 'http'):
			f = urllib.request.urlopen(link, timeout=10)
			s = f.read().decode('utf-8')
			emails = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}", s)
			for email in emails:
				if (email not in listEmails and not email.endswith(imageExt)):
					count_email_in_phrase += 1
					listEmails.append(email)
					print(str(count_email_in_phrase) + " - " + email)
					if (searchEmail("Emails.db", email, phrase) == 0):
						insertEmail("Emails.db", email, phrase, link)

	except (HTTPError, URLError) as e:
		print(e)
		pass
	except timeout:
		print('socket timed out - URL %s', link)
		pass
	except (http.client.IncompleteRead) as e:
		print(e)
		pass
	except Exception as e:
		print(e)
		pass

def guardarCsv(db_file):
	try:
		conn = sqlite3.connect(db_file)
		c = conn.cursor()

		nameFile = datetime.now().strftime('csvemails_%Y_%m_%d_%H_%M_%S.csv')
		print("")
		print("Creating csv, please wait...")

		f = open(nameFile, "w", newline="")
		writer = csv.writer(f)

		header = ['Phrase', 'Email', 'Url']
		writer.writerow(header)

		c.execute('SELECT * FROM emails')

		for i in c:
			row = [str(i[1]), str(i[2]), str(i[3])]
			writer.writerow(row)

		f.close()

		conn.close()
		input("Press enter to continue")
		menu()
	except Error as e:
		print(e)
		input("Press enter to continue")
		menu()

	except Exception as o:
		print(o)
		input("Press enter to continue")
		menu()

	finally:
		conn.close()


def web():
    Main()

def Main():
	clear()
	crearTabla("Emails.db", False)
	menu()
