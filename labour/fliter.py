import django_filters
from .models import Attendance

class AttendanceFilter(django_filters.FilterSet):
    date = django_filters.DateFilter(field_name="date")
    month = django_filters.NumberFilter(method='filter_by_month')

    class Meta:
        model = Attendance
        fields = ['date', 'month']

    def filter_by_month(self, queryset, name, value):
        return queryset.filter(date__month=value)
