from data_manager import DataManager
from flight_search import FlightSearch
from datetime import datetime, timedelta
from notification_manager import NotificationManager

ORIGIN_CITY_IATA = "TPE"

data_manager = DataManager()
flight_search = FlightSearch()
notification_manager = NotificationManager()


sheet_data = data_manager.get_destination_data()
if sheet_data[0]["IATA Code"] == "":
	for row in sheet_data:
		row["IATA Code"] = flight_search.get_destination_code(row["City"])
	data_manager.destination_data = sheet_data
data_manager.update_destination_codes()


sheet_data = data_manager.get_destination_data()
tomorrow_datetime = datetime.now() + timedelta(days=1)
six_month_from_today_datetime = tomorrow_datetime + timedelta(days=30 * 6)
for row in sheet_data:
	flight = flight_search.check_flights(
		origin_city_code=ORIGIN_CITY_IATA,
		destination_city_code=row["IATA Code"],
		from_time=tomorrow_datetime,
		to_time=six_month_from_today_datetime
	)
	try:
		row["Search Price"] = flight.price
	except AttributeError:
		row["Search Price"] = "noFound"
	data_manager.destination_data = sheet_data

	try:
		if flight.price < row["Lowest Price"]:
			notification_manager.send_sms(
				message=f'Low price alert! Only NT${flight.price} to fly from {flight.origin_city}-{flight.origin_airport} to {flight.destination_city}-{flight.destination_airport}, from {flight.out_date} to {flight.return_date}.'
			)
	except AttributeError:
		pass

data_manager.update_destination_codes()
