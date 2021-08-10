from airtravel import *
from pprint import pprint as pp

f, g = make_flights()

a = AirbusA319("G-EZBT")
b = Boeing777("N1717AN")

pp(a.num_seats())
pp(b.num_seats())

pp(f.aircraft_model())
pp(g.aircraft_model())
pp(f.num_available_seat())
pp(g .num_available_seat())
