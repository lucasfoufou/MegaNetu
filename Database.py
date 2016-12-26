#######################################################################################
########### 25/12/2016 	 			Python 2.7.X 							###########
########### Fougeras Lucas	(lucasfougeras@gmail.com)						###########
########### Connection class to be used by the MegaNetu Uploader			###########
###########           ----------------------------------------				###########
###########                                                   				###########
###########           ----------------------------------------				###########
###########                                                   				###########
########### Structure of the database:										###########
########### One table called megaToNetu										###########
########### Id 	megalink(text)	megalinkbackup(text) 	netulink(text)		###########
########### queued(boolean)													###########
###########                                                   				###########
###########           ----------------------------------------				###########
###########                                                   				###########
########### One table called megaAcc										###########
########### Id 	mail(text)	pwd(text) 	status(boolean)						###########
#######################################################################################

import pymysql.cursors

class DbManager:
	def __init__(self):
		self.user = "python_exp"
		self.server = "fougeras.me"
		self.db = "python_exp"
		self.password = "iPu9PpK3"
		self.port = 3306
		self.connection = None

	def connect(self):
		self.connection = pymysql.connect(host=self.server,
                             user=self.user,
                             password=self.password,
                             port=self.port,
                             db=self.db)

	def disconnect(self):
		try:
			self.connection.close()
		except:
			print("Cannot disconnect: the connection has never been established !")

	def select(self, query, params=None):
		cur = self.connection.cursor()
		cur.execute(query, params)
		return cur.fetchall()

	def insUp(self, query, params=None):
		cur = self.connection.cursor()
		cur.execute(query, params)
		self.connection.commit()
		return cur.lastrowid

	def edit(self, id, table, params=None):
		"""
		Usage:
		param is a list : (columnName, value)
		"""
		variables = []
		query = "UPDATE "+ table +" SET "
		for indx, param in enumerate(params):
			if param[1] is not None:
				query += param[0] + " = %s "
				variables.append(param[1])
				if indx<len(params)-1:
					query += ", "
		query +="WHERE id = %s"
		variables.append(id)
		try:
			self.insUp(query, variables)
		except:
			self.connect()
			self.insUp(query, variables)

	def editMegaToNetu(self, id, ML, MLB, NL, Q):
		"""
		Usage:
		dbm.editMegaToNetu(1, None, "MLB Value", "NL Value", True)
		"""
		if(ML is not None or MLB is not None or NL is not None or Q is not None):
			params = (("megalink", ML), ("megalinkbackup", MLB), ("netulink", NL), ("queued", Q))
			self.edit(id, "megaToNetu", params)

	def editMegaAccounts(self, id, mail, pwd, status):
		"""
		Usage:
		dbm.editMegaAccounts(1, None, None, True)
		"""
		if(mail is not None or pwd is not None or status is not None):
			params = (("mail", mail), ("pwd", pwd), ("status", status))
			self.edit(id, "megaAcc", params)

	def listQueued(self):
		try:
				ret = self.select("SELECT * FROM `megaToNetu` WHERE queued = 1", None)
		except:
				self.connect()
				ret = self.select("SELECT * FROM `megaToNetu` WHERE queued = 1", None)
		return ret

	def listMegaAccounts(self):
		try:
				ret = self.select("SELECT * FROM `megaAcc` WHERE status = 1", None)
		except:
				self.connect()
				ret = self.select("SELECT * FROM `megaAcc` WHERE status = 1", None)
		return ret