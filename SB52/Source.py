from FilteredTwitsBuilder import FilteredTwitsBuilder
from DBPharser import DBPharser
from module1 import check
from Prediction import Prediction
from PredictionGUI import Window
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel
import sys
from PyQt5.QtGui import QPixmap
	
def main():
	#f = FilteredTwitsBuilder()

	print("starting configuration..")
	#Filtered = f.read_from_csv()
	pred = Prediction(1382, 1778)
	ans=pred.predict(pred._start, pred._end)
	print("The winner predicted to win according given quarter is " + ans)
	App = QApplication(sys.argv)
	window = Window()
	sys.exit(App.exec())
	#c = check()
	#c.func()
	

if __name__ == "__main__":
	main()
