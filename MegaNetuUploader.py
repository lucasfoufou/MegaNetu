#######################################################################################
########### 25/12/2016 			Python 2.7.X 								###########
########### Fougeras Lucas	(lucasfougeras@gmail.com)						###########
###########                                                   				###########
########### Projet to automatically upload a file from Mega.nz to NetuTV  	###########
########### And to make a backup from a Mega.nz account					 	###########
########### to another Mega.nz account.				 					 	###########
#######################################################################################

from Database import *
from mega import Mega
import random

def makeTheLast(dbm, mega, queue):
	email = None
	password = None
	session = None

	while True:
		"""
		Infinity loop that we end if there is no more free account or if we find one that is clean
		"""

		email = None
		password = None

		accounts = dbm.listMegaAccounts()
		if len(accounts) == 0:
			break
		#User Details - we take a random account from our mega accounts
		id = random.randint(0, (len(accounts)-1))
		email = accounts[id][1]
		print("Using the account: " + email)
		password = accounts[id][2]

		session = mega.login(email, password)
		space = session.get_storage_space()
		space = 100*space['used']/space['total']

		#We deactivate every account that uses more than 80% of the free storage
		if int(space) > 80:
			print(email + " has been deactivated since it has reached 80% of the storage")
			dbm.editMegaAccounts(accounts[id][0], None, None, False)
		else:
			break

	## Download the biggest id in the queued tasks
	link = queue[(len(queue)-1)][1]
	currentId = queue[(len(queue)-1)][0]

	print("Starting the download: ")
	try:
		filename = session.download_url(link)
		print(filename)
		print("Download is over !")

		## Upload and get the backup link
		print("Starting the upload:")
		backuplink = session.get_upload_link(session.upload(filename))
		dbm.editMegaToNetu(currentId, None, backuplink, None, False)
		return True

	except:
		dbm.editMegaToNetu(currentId, None, None, None, False)
		return False

dbm = DbManager()
mega = Mega()
queue = dbm.listQueued()

while(len(queue) != 0):
	makeTheLast(dbm, mega, queue)
	queue = dbm.listQueued()

dbm.disconnect()



