import gspread
from gspread import Cell
from pprint import pprint


GSPREAD_SERVICE_ACCOUNT = "flight-deals-382008-0b61fb416b94.json"


class DataManager:
    def __init__(self):
        self.destination_data = {}

    def get_destination_data(self):
        """Use the google API to GET all the data in that sheet and print it out."""
        # headers = {"Authorization": f"Bearer {SHEETY_TOKEN}"}
        # response = requests.get(url=SHEETY_PRICES_ENDPOINT, headers=headers)
        # response.raise_for_status()
        # data = response.json()["prices"]
        sa = gspread.service_account(GSPREAD_SERVICE_ACCOUNT)
        sh = sa.open("Flight Deals")
        wks = sh.worksheet("prices")
        data = wks.get_all_records()
        self.destination_data = data
        pprint(self.destination_data)
        return self.destination_data

    def update_destination_codes(self):
        sa = gspread.service_account(GSPREAD_SERVICE_ACCOUNT)
        sh = sa.open("Flight Deals")
        data = sh.worksheet("prices")
        iatacode_cell_list = data.range('B2:B10')
        searchprice_cell_list = data.range('C2:C10')
        for index, val in enumerate(self.destination_data):
            iatacode_cell_list[index].value = val["IATA Code"]
            searchprice_cell_list[index].value = val["Search Price"]
        data.update_cells(iatacode_cell_list)
        data.update_cells(searchprice_cell_list)
