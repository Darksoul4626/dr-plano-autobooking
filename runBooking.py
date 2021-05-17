from src.businesslogic.booking import Booking


def __init__():
    booking = Booking()

    booking.initBrowser()
    booking.openPage()
    booking.startBooking()
    booking.endBooking()


__init__()
