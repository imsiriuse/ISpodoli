from calendar import HTMLCalendar
import datetime
from dateutil import relativedelta


class BookingCalendar(HTMLCalendar):
    def __init__(self, year, month, day):
        super(BookingCalendar, self).__init__()
        self.year = year
        self.month = month
        self.day = day
    def formatday(self, day, weekday):
        if day == 0:
            return '<td class="noday">&nbsp;</td>'
        tag = '<td class="' + self.cssclasses[weekday] + '">'
        tag = tag + '<a href=?date=%d-%d-%d>%d</a>' % (day, self.month, self.year, day)
        return tag

    def gethtml(self):
        """
        Return a formatted month as a table.
        """
        v = []
        a = v.append

        # add previous day into calendar
        a('<div>')

        prev = datetime.date(self.year, self.month, self.day) - relativedelta.relativedelta(months=1)

        a('<div style="display: inline-block">')
        a('<a href="?date=%d-%d-%d"><</a>' % (prev.day, prev.month, prev.year))
        a('</div>')

        # add calendar
        a('<div style="display: inline-block">')
        a('<table border="0" cellpadding="0" cellspacing="0" class="%s">' % (
            self.cssclass_month))
        a('\n')
        a(self.formatmonthname(self.year, self.month, withyear=True))
        a('\n')
        a(self.formatweekheader())
        a('\n')
        for week in self.monthdays2calendar(self.year, self.month):
            a(self.formatweek(week))
            a('\n')
        a('</table>')
        a('\n')
        a('</div>')

        # add next day into calendar
        a('<div style="display: inline-block">')

        after = datetime.date(self.year, self.month, self.day) + relativedelta.relativedelta(months=1)

        a('<a href="?date=%d-%d-%d">></a>' % (after.day, after.month, after.year))
        a('</div>')

        a('</div>')
        return ''.join(v)
