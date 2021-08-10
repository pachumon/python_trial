from airtravel import (Flight, Aircraft)


f = Flight("SN060", Aircraft("G-EUPT", "Airbus A319",
           num_rows=22, num_seats_per_row=2))
print(f.aircraft_model())
