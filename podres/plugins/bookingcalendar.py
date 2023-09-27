from calendar import HTMLCalendar
from datetime import datetime, date
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

        if self.day == day:
            return '<td class="' + self.cssclasses[weekday] + ' cal-today">' + '<a href=?date=%d-%d-%d>%d</a>' % (day, self.month, self.year, day)

        return '<td class="' + self.cssclasses[weekday] + '">' + '<a href=?date=%d-%d-%d>%d</a>' % (day, self.month, self.year, day)

    def gethtml(self):
        prev = date(self.year, self.month, self.day) - relativedelta.relativedelta(months=1)
        after = date(self.year, self.month, self.day) + relativedelta.relativedelta(months=1)
        month_name = self.formatmonthname(self.year, self.month, withyear=False)


        v = []
        a = v.append

        a('<div class="cal">')

        a('<div class="cal-month">')
        a('<ul>')

        a('<li class="cal-prev">')
        a('<a class="cal-prev" href="?date=%d-%d-%d">&#10094;</a>' % (prev.day, prev.month, prev.year))
        a('</li>')

        a('<li class="cal-next">')
        a('<a class="cal-next" href="?date=%d-%d-%d">&#10095;</a>' % (after.day, after.month, after.year))
        a('</li>')

        a('<li>%s<br><span>%d</span></li>' % (month_name, self.year))

        a('</ul>')
        a('</div>')

        a('<table class="cal-days">')
        a('<thead><tr>')
        a('<th>Mo</th>')
        a('<th>Tu</th>')
        a('<th>We</th>')
        a('<th>Th</th>')
        a('<th>Fr</th>')
        a('<th>Sa</th>')
        a('<th>Su</th>')
        a('</thead></tr>')

        for week in self.monthdays2calendar(self.year, self.month):
            a(self.formatweek(week))
            a('\n')

        a('</table>')

        a('</div>')

        return ''.join(v)
