import itertools

class Twit:
	_newid = itertools.count()

	def __init__(self, date, time, raw_text, 
			related_team, related_nick_name,
			pos, neg, plutchik, neutral):

		self._id = next(Twit._newid)
		self._date = date
		self._time = time
		self._raw_text = raw_text
		self._pos_cnt = pos
		self._neg_cnt = neg
		self._neutral_flag = neutral
		self._related_nick_name = related_nick_name
		self._related_team = related_team
		self._plutchik_emotions = plutchik 
		#self._emotion_signal = emotion_cnt

		


		
		
		

