## Requirements
* Installing selenium (pip install selenium)
* Download the related webdriver version for your preferred browser on https://selenium-python.readthedocs.io/installation.html#drivers 
    * edit the DRIVERPATH in the '.env'-file to the preferred webdriver.exe

### Create env file
1. Create an '.env'-file or rename the '.env.sample'-file and fill out the missing fields 
2. Edit the URL in the '.env'-file to the website where [Dr. Plano's BookingSystem](https://www.dr-plano.com/de/) is active.

### Running tests
* Installing pytest (pip install pytest)
* Execute tests by entering ```pytest ./tests/test_dynochromBooking.py``` on your prefered commandline

# Execute automatic booking
1. Run ```py runBooking.py``` to start the booking until the payment page is visible.
2. Enter your payment info. 
3. You just finished your booking ! :) 



## Installing chrome driver 
https://sites.google.com/a/chromium.org/chromedriver/downloads 



