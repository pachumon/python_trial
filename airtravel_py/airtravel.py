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


class Aircraft:

    def __init__(self, registration, model, num_rows, num_seats_per_row):
        self._registration = registration
        self._model = model
        self._num_rows = num_rows
        self._num_seats_per_row = num_seats_per_row

    def registration(self):
        return self._registration

    def model(self):
        return self._model

    def seating_plan(self):
        return(range(1, self._num_rows+1), "ABCDEFGHJK"[:self._num_seats_per_row])


def make_flight():
    f = Flight("SN060", Aircraft("G-EUPT", "Airbus A319",
                                 num_rows=22, num_seats_per_row=6))
    f.allocate_seats("12A", "Guido van Rossum")
    f.allocate_seats("15F", "bjarne stroustroup")
    f.allocate_seats("15E", "andres hejsburg")
    f.allocate_seats("21E", "yukihiro matsumoto")
    return f
