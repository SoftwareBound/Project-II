import csv
import operator
import itertools
import DictionaryPharser
from Twit import Twit

character_replacements = [
    ('\\u2018', "'"),   # LEFT SINGLE QUOTATION MARK
    ('\\u2019', "'"),   # RIGHT SINGLE QUOTATION MARK
    ('\\u201c', '"'),   # LEFT DOUBLE QUOTATION MARK
    ('\\u201d', '"'),   # RIGHT DOUBLE QUOTATION MARK
    ('\\u201e', '"'),   # DOUBLE LOW-9 QUOTATION MARK
    ('\\u2013', '-'),   # EN DASH
    ('\\u2026', '...'), # HORIZONTAL ELLIPSIS
]

eagles_ref = ["doug pederson", "zach ertz","corey clement", "jake elliott", "legarrette blount" ,"nick foles", "fletcher cox", "jason peter", "malcolm jenkins", "rodney mcleod"]
patriots_ref = ["bill belichick", "tom brady", "chris hogan","james white","stephen gostkowski" ,"stephon gilmore", "devin mccourty", "rob gronkowski", "dont'a hightower" ]

class FilteredTwitsBuilder:
	def __init__(self):
		self._filtered_twit_list = []
		self._filtered_twit_list_csv = []
		self._dict_builder = DictionaryPharser.DictionaryPharser()
		self._dict_builder.InitializeDictsBuilder()
		print("Dictionaries built seccessfully..")

	
	def read_from_csv(self):
		with open(r"C:\Users\itaia\Desktop\Data.csv", encoding='utf-8') as csv_file:
			START_POINT = 56590
			END_POINT = 71250
			#START_POINT = 56590
			#END_POINT = 59000
			data = csv.reader(csv_file)
			for row in itertools.islice(data,START_POINT,END_POINT):
				del row[-1]
				del row[2]
				words = row[2].replace('\\n', ' ').split()
				words = self.noiseRemoval(words) #removing noise
				#words = self.upperToLower(words) #change all text to lowercase 
				words = self.EmoticonsReplacement(words)
				temp_nicknames_list = self.nickNamesPharser(words)
				if (temp_nicknames_list != None):
					words = self.EmoticonsPharser(words)
					words = self.SlangPharser(words)
					words = self.StopWordsPharser(words)
					words = self.NegativeStopWordsPharser(words)
					emotions_list = self.NRCPharser(words)
					plutchik_flag = 0
					for element in emotions_list[2]:
						if (element == 0):
							continue
						else:
							plutchik_flag = 1
							break
					if ((emotions_list[0] == emotions_list[1]) and (plutchik_flag ==1)):
						if (len(self._filtered_twit_list) == 66):
							print("h")
						self._filtered_twit_list.append(Twit(row[0], row[1], words, 
														temp_nicknames_list[0], temp_nicknames_list[1], 
														emotions_list[0], emotions_list[1],emotions_list[2],1))
						tuple_twit = (row[0], row[1], words, 
									temp_nicknames_list[0], temp_nicknames_list[1],
									emotions_list[0], emotions_list[1], emotions_list[2],1, emotions_list[3])
						#print(tuple_twit)
						self._filtered_twit_list_csv.append(tuple_twit)
						tuple_twit = ()
					elif (emotions_list[0] != emotions_list[1]):
						self._filtered_twit_list.append(Twit(row[0], row[1], words, 
														temp_nicknames_list[0], temp_nicknames_list[1], 
														emotions_list[0], emotions_list[1], emotions_list[2],0))
						tuple_twit = (row[0], row[1], words, 
									temp_nicknames_list[0], temp_nicknames_list[1],
									emotions_list[0], emotions_list[1],emotions_list[2],0, emotions_list[3])
						#print(tuple_twit)
						self._filtered_twit_list_csv.append(tuple_twit)
						tuple_twit = ()
					else: 
						continue						
				else:
					continue
			return self._filtered_twit_list

	def noiseRemoval(self, word_list):
		new_list = []
		for word in word_list:
			if((word.find("http") != -1) or (word.find("&") != -1)):
				word_list.remove(word)
				continue
			if(word.find("\\u") != -1):
				word = self.CheckCharecterReplacement(word, character_replacements)
			letter_list = list(word)
			i = 0
			while i < len(letter_list):
				if ((letter_list[i] == '#') 
					or (letter_list[i] == '@')
				    or (letter_list[i] == '!') 
					or (letter_list[i] == '?') 
					or (letter_list[i] == '.')
					or (letter_list[i] == '-')):
					letter_list.remove(letter_list[i])
					i -= 1
				i += 1
			word = "".join(letter_list)
			word = word.lower()
			new_list.append(word)
		
		return new_list
	

	def upperToLower(self, word_list):
		word_list = [element.lower() for element in word_list]
		return word_list

	def CheckCharecterReplacement(self, word, list):
		for tuple in list:
			if(word.find(tuple[0]) != -1):
				if(word.find("\\u2026") != -1):
					return word.replace(tuple[0], "")
				return word.replace(tuple[0], tuple[1])
		return word


	def nickNamesPharser(self,text_list):
		dict = self._dict_builder._NickNamesList
		pat_cnt = 0
		eag_cnt = 0
		nick_names = []
		team_nick_names = []
		nick_names_eag = {"jake elliott" : 0, "legarrette blount" : 0, "zach ertz" : 0, "corey clement" : 0, "doug pederson" : 0, "nick foles" : 0, "fletcher cox" : 0, "jason peter" : 0, "malcolm jenkins" : 0, "rodney mcleod" : 0}
		nick_names_pat = {"chris hogan" : 0,"james white" : 0,"stephen gostkowski" : 0,"bill belichick" : 0, "tom brady" : 0, "stephon gilmore" : 0, "devin mccourty" : 0, "rob gronkowski" : 0, "dont'a hightower" : 0} 
		
		for word in text_list:
			for key in dict.keys():
				try:
					dict.get(key).index(word)
					if ((key == "eagles") or (key == "patriots")):
						team_nick_names.append(key)
					else:
						nick_names.append(key)
				except ValueError:
					continue

		for team in team_nick_names:
			if(team == "patriots"):
				pat_cnt += 1
			elif(team == "eagles"):
				eag_cnt += 1
		
		if not nick_names :
			if(eag_cnt > pat_cnt):
				return ["eagles","eagles"]
			elif(eag_cnt < pat_cnt):
				return ["patriots", "patriots"]
			else:
				return None
		else:
			for name in nick_names:
				try:
					eagles_ref.index(name)
					nick_names_eag[name]+=1

				except ValueError:
					try:
						patriots_ref.index(name)
						nick_names_pat[name]+=1
					except ValueError:
						continue
			max_key_eagles = max(nick_names_eag, key = nick_names_eag.get)
			max_key_patriots = max(nick_names_pat, key = nick_names_pat.get)
			if(nick_names_pat[max_key_patriots] > nick_names_eag[max_key_eagles]):
				return ["patriots", max_key_patriots]
			elif(nick_names_pat[max_key_patriots] < nick_names_eag[max_key_eagles]):
				return ["eagles", max_key_eagles]
			else:
				return None


	def EmoticonsReplacement(self, word_list):
		temp_list = []
		for word in word_list:
			if(word.find("\\u") != -1):
				parts = word.split("\\u")
				i = 0
				while i < len(parts):
					if (parts[i] == ""):
						del parts[i]
						continue
					if((len(parts[i]) == 4) and ( "d83" in parts[i])):
						p = "\\u" + parts[i] + "\\u" + parts[i+1][0:4]
						temp_list.append(p)
						i += 2
						continue
					temp_list.append(parts[i])
					i += 1
			else:
				temp_list.append(word)
		return temp_list


	def EmoticonsPharser(self,text_list):
		dict = self._dict_builder._EscapedUnicodeEmoticonsDic
		new_list = []
		for word in text_list:
			flag = 0
			for key in dict.keys():
				if(key == word):
					new_list.append(dict.get(key))
					flag = 1
					break
			if(flag == 0):
				new_list.append(word)
		
		return new_list
				
					
	def StopWordsPharser(self,text_list):
		stop_words_list = self._dict_builder._StopWordsList
		new_list = []
		for word in text_list:
			flag = 0
			for key in stop_words_list:
				if(key == word):
					flag = 1
					break
			if(flag == 0):
				new_list.append(word)

		return new_list


	def NegativeStopWordsPharser(self,text_list):
		negative_stop_words_list = self._dict_builder._NegativeStopWordsList
		new_list = []
		for word in text_list:
			for key in negative_stop_words_list:
				if(key == word):
					word = "negative_word"
					break
			new_list.append(word)
		return new_list

	

	def SlangPharser(self,text_list):
		dict = self._dict_builder._SlangDic
		new_list = []
		for word in text_list:
			flag = 0
			for key in dict.keys():
				if(key == word):
					val = dict.get(key)
					if(val.find(" ") != -1):
						parts = val.split()
						for part in parts:
							new_list.append(part)
					else:
						new_list.append(val)
					flag = 1
					break
			if(flag == 0):
				new_list.append(word)
		
		return new_list


	def NRCPharser(self,text_list):
		nrc_dict = self._dict_builder._NRC
		pos = 0
		neg = 0
		emotion_words_cnt = 0
		#anger[0], anticipation[1], disgust[2], fear[3], joy[4], sadness[5], surprise[6], trust[7]
		emotions_list = [0] * 8
		answer_list = []
		word_dict = {}

		for word in text_list:
			check_list = []
			for letter_id,info_letters_dict in nrc_dict.items():
				if (word == ""):
					break
				if(word[0] == letter_id):
					check_list = self.CheckNRCDictMatch(word, info_letters_dict, emotion_words_cnt)
					break
			if(check_list):
				pos += check_list[0]
				neg += check_list[1]
				emotion_words_cnt += check_list[4]
				i = 0
				emoition_check = check_list[2]
				while i < len(emoition_check):
					if (emoition_check[i] == 1):
						emotions_list[i] += 1
					i += 1

				word_dict.update({word : check_list[3]})
				check_negative = self.ConvertNegativeEmotions(word_dict, pos, neg, emotions_list)
				pos = check_negative[0]
				neg = check_negative[1]
				emotions_list = check_negative[2]
			else:
				word_dict.update({word : []})
			
		answer_list.append(pos)
		answer_list.append(neg)
		answer_list.append(emotions_list)
		answer_list.append(emotion_words_cnt)
		
		return answer_list	

	
	def ConvertNegativeEmotions(self, text_dict, pos_cnt, neg_cnt, plutchik):
		i = 0
		words_list = list(text_dict.keys())
		while (i < (len(words_list) - 1)):
			if (words_list[i] == "negative_word"):
				key = words_list[i+1]
				value = text_dict.get(key) 
				if not value:
					i +=1
					continue
				else:
					answer_list = self.EmotionsChanger(value,pos_cnt,neg_cnt,plutchik)
					pos_cnt = answer_list[0]
					neg_cnt = answer_list[1]
					plutchik = answer_list[2]
					i += 1
			else:
				i += 1

		return [pos_cnt, neg_cnt, plutchik] 


	def EmotionsChanger(self, emotions_list, pos, neg, plutchik):
		for emotion in emotions_list:
			if (emotion == "positive"):
				pos -= 1
				if (pos < 0):
					pos = 0
				neg += 1
				continue
			if (emotion == "negative"):
				pos += 1
				neg -= 1
				if (neg < 0):
					neg = 0
				continue
			if (emotion == "anger"):
				plutchik[0] -= 1
				if (plutchik[0] < 0):
					plutchik[0] = 0
				plutchik[3] += 1
				continue
			if (emotion == "anticipation"):
				plutchik[1] -= 1
				if (plutchik[1] < 0):
					plutchik[1] = 0
				plutchik[6] += 1
				continue
			if (emotion == "disgust"):
				plutchik[2] -= 1
				if (plutchik[2] < 0):
					plutchik[2] = 0
				plutchik[7] += 1
				continue
			if (emotion == "fear"):
				plutchik[3] -= 1
				if (plutchik[3] < 0):
					plutchik[3] = 0
				plutchik[0] += 1
				continue
			if (emotion == "joy"):
				plutchik[4] -= 1
				if (plutchik[4] < 0):
					plutchik[4] = 0
				plutchik[5] += 1
				continue
			if (emotion == "sadness"):
				plutchik[5] -= 1
				if (plutchik[5] < 0):
					plutchik[5] = 0
				plutchik[4] += 1
				continue
			if (emotion == "surprise"):
				plutchik[6] -= 1
				if (plutchik[6] < 0):
					plutchik[6] = 0
				plutchik[1] += 1
				continue
			if (emotion == "trust"):
				plutchik[7] -= 1
				if (plutchik[7] < 0):
					plutchik[7] = 0
				plutchik[2] += 1
				continue
		if(pos < 0):
			pos = 0
		if(neg < 0):
			neg = 0
		for element in plutchik:
			if (element < 0):
				element = 0
		
		return [pos, neg, plutchik]


	def CheckNRCDictMatch(self, word, list_of_dicts, emotions_cnt):
		for part in list_of_dicts:			
			check = list(part.keys())
			check_word = check[0]
			if(word == check_word):
				check_list = self.CreateWordsDict(word, part.get(check_word), emotions_cnt)
				return check_list
		
		
	def CreateWordsDict(self, word, dict, emotions_cnt):
		returned_list = []
		pos_cnt = 0
		neg_cnt = 0
		emotions_list = [0] * 8
		emotions_list_str = []
		emotion_flag = 0

		l = []
		for key in dict:
			if((key == "positive") and (dict.get(key) == '1')):
				pos_cnt += 1
				emotions_list_str.append(key)
				continue
			elif((key == "negative") and (dict.get(key) == '1')):
				neg_cnt += 1
				emotions_list_str.append(key)
				continue
			if((key == "anger") and (dict.get(key) == '1')):
				emotions_list[0] += 1
				emotions_list_str.append(key)
				continue
			if((key == "anticipation") and (dict.get(key) == '1')):
				emotions_list[1] += 1
				emotions_list_str.append(key)
				continue
			if((key == "disgust") and (dict.get(key) == '1')):
				emotions_list[2] += 1
				emotions_list_str.append(key)
				continue
			if((key == "fear") and (dict.get(key) == '1')):
				emotions_list[3] += 1
				emotions_list_str.append(key)
				continue
			if((key == "joy") and (dict.get(key) == '1')):
				emotions_list[4] += 1
				emotions_list_str.append(key)
				continue
			if((key == "sadness") and (dict.get(key) == '1')):
				emotions_list[5] += 1
				emotions_list_str.append(key)
				continue
			if((key == "surprise") and (dict.get(key) == '1')):
				emotions_list[6] += 1
				emotions_list_str.append(key)
				continue
			if((key == "trust") and (dict.get(key) == '1')):
				emotions_list[7] += 1
				emotions_list_str.append(key)
				continue
		for element in emotions_list:
			if (element == 0):
				continue
			else:
				emotion_flag = 1
				break 
		if(pos_cnt < 0):
			pos_cnt = 0
		if(neg_cnt < 0):
			neg_cnt = 0
		for emo in emotions_list:
			if (emo < 0):
				emo = 0
		if ((neg_cnt) or (pos_cnt) or (emotion_flag)):
			emotions_cnt += 1
		returned_list.append(pos_cnt)
		returned_list.append(neg_cnt)
		returned_list.append(emotions_list)
		returned_list.append(emotions_list_str)
		returned_list.append(emotions_cnt)
			
		return returned_list
		
		

			
	

	