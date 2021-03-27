from datetime import datetime, timedelta
from calendar import HTMLCalendar
from .models import ViewProgram


class Calendar(HTMLCalendar):
    
    def __init__(self, year=None, month=None, profile_pk=None):
        self.year = year
        self.month = month
        self.profile_pk = profile_pk
        super(Calendar, self).__init__()


    def formatday(self, day, viewProgram):
        viewProgram_per_day = viewProgram.filter(date__day=day)
        d = ''
        for view in viewProgram_per_day:
            # d += f"<li class='calendar_list'> {view.get_html_url} </li>"
            if view.profile.user.id == self.profile_pk: 
                d += f"<li class='calendar_list'> {view.get_html_url} </li>"
            
        if day != 0:
            return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
        
        return '<td></td>'


    def formatweek(self, theweek, viewProgram):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, viewProgram)

        return f'<tr> {week} </tr>'


    def formatmonth(self, withyear=True):
        viewProgram = ViewProgram.objects.filter(date__year=self.year, date__month=self.month)
        cal = f'<table border="0" cellpadding="0" cellspacing="0"     class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, viewProgram)}\n'
        cal += f'</table>'
        
        return cal