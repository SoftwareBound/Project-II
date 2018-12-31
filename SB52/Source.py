from FilteredTwitsBuilder import FilteredTwitsBuilder
from DBPharser import DBPharser
from module1 import check
	
def main():
	#f = FilteredTwitsBuilder()
	print("starting configuration..")
	#Filtered = f.read_from_csv()
	#DB = DBPharser(Filtered)
	#DB.ConnectToDB()
	c = check()
	c.func()
	

if __name__ == "__main__":
	main()
