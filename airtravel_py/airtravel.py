"""
Model foraircraft flights
"""


class Flight:

    def __init__(self, number, aircraft):
        if not number[:2].isalpha():
            raise ValueError(f"no airline code in :{number}")
        if not number[:2].isupper():
            raise ValueError(f"invalid airline code:{number}")
        if not(number[2:].isdigit() and int(number[2:]) <= 9999):
            raise ValueError(f"invalid route number:{number}")
        self._number = number
        self._aircraft = aircraft
        rows, seats = self._aircraft.seating_plan()
        self._seating = [None] + \
            [{letter: None for letter in seats} for _ in rows]

    def aircraft_model(self):
        return self._aircraft.model()

    def number(self):
        return self._number

    def airline(self):
        return self._number[:2]

    def allocate_seats(self, seat, passenger):
        row, letter = self._parse_seat(seat)
        if self._seating[row][letter] is not None:
            raise ValueError(f"seat {seat} already occupied")
        self._seating[row][letter] = passenger

    def _parse_seat(self, seat):
        rows, seat_letters = self._aircraft.seating_plan()
        letter = seat[-1]
        if letter not in seat_letters:
            raise ValueError(f"invalid seat letter {letter}")

        row_text = seat[:-1]
        try:
            row = int(row_text)
        except ValueError:
            raise ValueError(f"invalid seat row {row_text}")

        if row not in rows:
            raise ValueError(f"invalid row number {row}")
        return row, letter

    def relocate_passenger(self, from_seat, to_seat):
        from_row, from_letter = self._parse_seat(from_seat)
        if self._seating[from_row][from_letter] is None:
            raise ValueError(f"no passenger to relocate in seat {from_seat}")

        to_row, to_letter = self._parse_seat(to_seat)
        if self._seating[to_row][to_letter] is not None:
            raise ValueError(f"seat {to_seat} is already occupied")

        self._seating[to_row][to_letter] = self._seating[from_row][from_letter]
        self._seating[from_row][from_letter] = None

    def num_available_seat(self):
        return sum(sum(1 for s in row.values() if s is None)for row in self._seating if row is not None)

    def make_boarding_pass(self, card_printer):
        for passenger, seat in sorted(self._passenger_seats()):
            card_printer(passenger, seat, self.number(), self.aircraft_model())

    def _passenger_seats(self):
        row_numbers, seat_letters = self._aircraft.seating_plan()
        for row in row_numbers:
            for letter in seat_letters:
                passenger = self._seating[row][letter]
                if passenger is not None:
                    yield(passenger, f"{row}{letter}")


class Aircraft:
    def __init__(self, registration, ):
        self._registration = registration

    def registration(self):
        return self._registration

    def num_seats(self):
        rows, row_seats = self.seating_plan()
        return len(rows)*len(row_seats)


class Boeing777(Aircraft):

    def model(self):
        return "Boeing 777"

    def seating_plan(self):
        return range(1, 56), "ABCDEFGHJK"


class AirbusA319(Aircraft):

    def model(self):
        return "Airbus A319"

    def seating_plan(self):
        return range(1, 23), "ABCDEF"


def make_flights():
    f = Flight("BA758", AirbusA319("G-EUPT"))
    f.allocate_seats("12A", "Guido van Rossum")
    f.allocate_seats("15F", "bjarne stroustroup")
    f.allocate_seats("15E", "andres hejsburg")
    f.allocate_seats("21E", "yukihiro matsumoto")

    g = Flight("BA758", Boeing777("F-GSPS"))
    g.allocate_seats("12A", "Guido van Rossum")
    g.allocate_seats("15F", "bjarne stroustroup")
    g.allocate_seats("15E", "andres hejsburg")
    g.allocate_seats("21E", "yukihiro matsumoto")
    return f, g


def console_card_printer(passenger, seat, flight_number, aircraft):
    output = f"| Name: {passenger}"\
             f" Flight: {flight_number}"\
             f" Seat: {seat}"\
             f" aircraft: {aircraft}"\
             f" |"
    banner = "+"+"-"*(len(output)-2)+"+"
    border = "+"+" "*(len(output)-2)+"+"
    lines = [banner, border, output, border, banner]
    card = "\n".join(lines)
    print(card)
    print()
