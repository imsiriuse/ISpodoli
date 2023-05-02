class Timetable:
    def __init__(self, bookings):
        self.bookings = bookings

    def gethtml(self, start, end):
        v = []
        a = v.append

        a('<h1>Timetable</h1>')

        return ''.join(v)
