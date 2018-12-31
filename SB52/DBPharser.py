from FilteredTwitsBuilder import FilteredTwitsBuilder
import pymysql

class DBPharser():
	def __init__(self,twits_list):
		self._twits_list_to_DB = twits_list
		self._db = None
		self._cursor = None
	
	def ConnectToDB(self):
		try:
			self._db = pymysql.connect(host = "localhost", user = "root",
								 passwd = "root", database = "twitsdb")
		except Exception:
			print("Error in MySQL connection")

		self.InsertQuery()
			

	def InsertQuery(self):
		self._cursor = self._db.cursor()
		#insert_stmt = "INSERT INTO twit(date,time,raw,team,nickname,positive,negative,anger,anticipation,disgust,fear,joy,sadness,surprise,trust,ntrl,signal) " \
		#	"VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
		insert_stmt = "INSERT INTO twit VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
		
		for twit in self._twits_list_to_DB:
			data = self.ConvertDataToTuple(twit)
			self._cursor.execute(insert_stmt, data)
		self._db.commit()

	def ConvertDataToTuple(self,twit):
		id = twit._id
		date = twit._date
		time = twit._time
		raw = " ".join(str(word) for word in twit._raw_text)
		team = twit._related_team
		nickname = twit._related_nick_name
		pos = twit._pos_cnt
		neg = twit._neg_cnt
		anger = twit._plutchik_emotions[0]
		anticipation = twit._plutchik_emotions[1]
		disgust = twit._plutchik_emotions[2]
		fear = twit._plutchik_emotions[3]
		joy = twit._plutchik_emotions[4]
		sadness = twit._plutchik_emotions[5]
		surprise = twit._plutchik_emotions[6]
		trust = twit._plutchik_emotions[7]
		ntrl = twit._neutral_flag

		data = (id, date, time, raw, team, nickname, 
				pos, neg, anger, anticipation, disgust, fear,
			    joy, sadness, surprise, trust, ntrl)

		return data


	
	

