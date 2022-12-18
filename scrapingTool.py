import requests
from pygame import mixer
from datetime import datetime, timedelta
import time

age = int(input("Please Enter your Age:"))
pincodes=[input("Please Enter the Pin Code of the Area You want to check:")]

# print(len(pincodes))

for length in pincodes:
    # print(len(length))
    if len(length)>6 or len(length)<6:
        print("wrong input/ invalid pincode")
    else:


        # pincodes = ["413003","413004"]
        num_days = 2

        print_flag = 'Y'

        print("Starting search for Covid vaccine slots!")

        # Get today's date
        actual = datetime.today()
        # Run a loop to convert it into list format.
        # We will make use of timedelta method to convert it into list format
        list_format = [actual + timedelta(days=i) for i in range(num_days)]
        # We will again run a loop to fetch the dates from the list and
        # we will make use of strftime method to do so.
        # Note that we are storing date in date-month-year format.
        actual_dates = [i.strftime("%d-%m-%Y") for i in list_format]

        # Let's introduce two more loops here:
        # 1. to fetch details for each pin-code.
        # 2. to fetch details for each date in the given pin-code.


        while True:
            counter = 0

            for pincode in pincodes:
                for given_date in actual_dates:

                    # Now in order to get requests, let's define the URL.
                    # I have added parameters in the URL itself using string formatting.
                    # We are passing in two parameters here, pincode and date.
                    # Every time the inner loop runs, this URL will be called and
                    # the respective date and pin-code will be passed as arguments for each case.
                    URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={}&date={}".format(
                        pincode, given_date)
                    # In order to get the request, let's define the header.
                    header = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}

                    result = requests.get(URL, headers=header)

                    # This data is not structured. So, we will make use of json here.
                    # Let's cast the data into json file.
                    if result.ok:
                        response_json = result.json()
                        if response_json["centers"]:
                            if (print_flag.lower() == 'y'):
                                for center in response_json["centers"]:
                                    # let's display and verify our data for each center
                                    # print(center)
                                    # Finally, we can retrieve the information for each session.
                                    # We will apply the check parameters as the arguments we saved earlier.
                                    for session in center["sessions"]:
                                        if (session["min_age_limit"] <= age and session["available_capacity"] > 0):
                                            # If it stratifies our conditions, let's display the result
                                            print('Pincode: ' + pincode)
                                            print("Available on: {}".format(given_date))
                                            print("\t", center["name"])
                                            print("\t", center["block_name"])
                                            print("\t Price: ", center["fee_type"])
                                            print("\t Availablity : ", session["available_capacity"])

                                            if (session["vaccine"] != ''):
                                                print("\t Vaccine type: ", session["vaccine"])
                                            print("\n")
                                            # At the end, let's increase the counter by one
                                            counter = counter + 1
                    else:
                        print("No Response!")

            # Let's cover the edge case
            if (counter == 0):
                print("No Vaccination slot available!")
            else:
                # mixer.init()
                # mixer.music.load('sound/chime.mp3')
                # mixer.music.play()
                print("Search Completed!")

            # Lastly, let's sync the data in real-time
            dt = datetime.now() + timedelta(minutes=3)

            while datetime.now() < dt:
                time.sleep(1)