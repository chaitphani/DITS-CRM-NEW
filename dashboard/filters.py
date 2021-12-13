import django_filters
from clientportal.models import UserDeposits
from datetime import datetime, timedelta

class UserDepositsDjangoFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(name="added_on", lookup_type=('gt'))
    end_date = django_filters.DateFilter(name='added_on', lookup_type=('lt'))

    class Meta:
        models = UserDeposits
        fields = ['added_on']

class DateRangeMaker:
    today_date_obj = datetime.now().date()
    # todate_date = datetime.now().date().strftime('%Y-%m-%d')

    def change(self, added_on_value=None):
        if int(added_on_value) == 1:
            return self.today_date_obj.strftime('%Y-%m-%d')
        elif int(added_on_value) == 2:
            d = self.today_date_obj - timedelta(1)
            return d.strftime('%Y-%m-%d')
        elif int(added_on_value) == 3:
            d = self.today_date_obj - timedelta(7)
            return d.strftime('%Y-%m-%d')
        elif int(added_on_value) == 4:
            d = self.today_date_obj - timedelta(30)
            return d.strftime('%Y-%m-%d')
        elif int(added_on_value) == 5:
            d = self.today_date_obj.replace(day=1)
            return d.strftime('%Y-%m-%d')
        elif int(added_on_value) == 6:
            d = self.today_date_obj.replace(day=1) - timedelta(1)
            return d.replace(day=1).strftime('%Y-%m-%d')

class UserDepositsDjangoFilterCustomDate(django_filters.FilterSet):
    added_on = django_filters.DateFromToRangeFilter()

    class Meta:
        models = UserDeposits
        fields = ['added_on']
