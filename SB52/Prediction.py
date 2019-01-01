from DBPharser import DBPharser


#will be in the gui controller




class Prediction():
	def __init__(self, start, end):
		self._start = int(start)
		self._end = int(end)


	def predict(self, start, end):
		eagles_count = 0
		patriots_count = 0
		statement = "SELECT * FROM twit WHERE id>=%s AND id<=%s"
		db = DBPharser()
		db.ConnectToDB()
		data = db.SelectQuery(statement, (int(start),int(end)))
		for twit in data:
			if twit[4] == "eagles":
				if twit[6]>=1:
					eagles_count += twit[6]
			elif twit[6] >=1:
				patriots_count += twit[6]
		if eagles_count > patriots_count:
			return 'eagles'
		else: return 'patriots'
		




