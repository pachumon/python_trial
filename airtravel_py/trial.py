from airtravel import (Flight,Aircraft)


f=Flight("SN060")
print(f.number())

a=Aircraft("G-EUPT","Airbus A319",num_rows=22,num_seats_per_row=4 )

print(a.registration())
print(a.model())
print(a.seating_plan())

