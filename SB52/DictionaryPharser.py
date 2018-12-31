import Dictionaries
import pprint

pp = pprint.PrettyPrinter(indent=4, width=5)


class DictionaryPharser():
	def __init__(self):
		self._EscapedUnicodeEmoticonsDic = None
		self._NegativeStopWordsList = None
		self._NickNamesList = None
		self._NRC = None 
		self._SlangDic = None
		self._StopWordsList = None 
	
	def EscapedUnicodeEmoticonsDicBuilder(self):
		EscapedUnicodeEmoticonsDic = Dictionaries.Dictionary("EscapedUnicodeEmoticonsDic")
		EscapedUnicodeEmoticonsDic.preparingTheDico(
									EscapedUnicodeEmoticonsDic.getTxt(
									EscapedUnicodeEmoticonsDic.getTxtName()))
		self._EscapedUnicodeEmoticonsDic = EscapedUnicodeEmoticonsDic.dico

		#print(EscapedUnicodeEmoticonsDic.txtName + " was created")

	
	def NegativeStopWordsListBuilder(self):
		NegativeStopWordsList = Dictionaries.listDictionary("NegativeStopWordsList")
		NegativeStopWordsList.preparingTheListDico(
									NegativeStopWordsList.getTxt(
									NegativeStopWordsList.getTxtName()))
		self._NegativeStopWordsList = NegativeStopWordsList.listDico
		#print(NegativeStopWordsList.txtName + " was created")


	def NickNamesListBuilder(self):
		NickNamesList = Dictionaries.nickNamesDictionary("NickNamesList")
		NickNamesList.preparingTheNickDico(
								NickNamesList.getTxt(
									NickNamesList.getTxtName()))
		self._NickNamesList = NickNamesList.nickDico
		#print(NickNamesList.txtName + " was created")

	
	def NRCBuilder(self):
		NRC = Dictionaries.nrcDictionary("NRC")
		NRC.preparingTheNrcDico(
				NRC.getTxt(
				NRC.getTxtName()))
		self._NRC = NRC.nrcDico
		self._NRC = NRC.Catagorise(self._NRC)
		#pp.pprint(self._NRC)
		#print(NRC.txtName + " was created")
	def SlangDicBuilder(self):
		SlangDic = Dictionaries.Dictionary("SlangDic")
		SlangDic.preparingTheDico(
				SlangDic.getTxt(
				SlangDic.getTxtName()))
		self._SlangDic = SlangDic.dico
		#print(SlangDic.txtName + " was created")


	def StopWordsListBuilder(self):
		StopWordsList = Dictionaries.listDictionary("StopWordsList")
		StopWordsList.preparingTheListDico(
				StopWordsList.getTxt(
				StopWordsList.getTxtName()))
		self._StopWordsList = StopWordsList.listDico
		#print(StopWordsList.txtName + " was created")


	def InitializeDictsBuilder(self):
		self.EscapedUnicodeEmoticonsDicBuilder()
		self.NegativeStopWordsListBuilder()
		self.NickNamesListBuilder()
		self.NRCBuilder()
		self.SlangDicBuilder()
		self.StopWordsListBuilder()