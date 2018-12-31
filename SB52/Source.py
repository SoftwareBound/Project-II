from FilteredTwitsBuilder import FilteredTwitsBuilder
from DBPharser import DBPharser
from module1 import check
from Prediction import Prediction
	
def main():
	#f = FilteredTwitsBuilder()

	print("starting configuration..")
	#Filtered = f.read_from_csv()
	pred = Prediction(5, 30)
	ans=pred.predict(pred._start, pred._end)
	print("The winner predicted to win according given quarter is " + ans)
	#c = check()
	#c.func()
	

if __name__ == "__main__":
	main()
