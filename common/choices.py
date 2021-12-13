class ObjectStatusChoices(object):
    ACTIVE = 0
    DELETED = 1
    CHOICES = (
        (ACTIVE, 'Active'),
        (DELETED, 'Deleted'),
    )

class CustomDateFilter(object):
    CHOICES = (
        (1, 'Today', 'date_1'),
        (2, 'Yesterday', 'date_2'),
        (3, 'Last 7 days', 'date_3'),
        (4, 'Last 30 days', 'date_4'),
        (5, 'This Month', 'date_5'),
        (6, 'Last Month', 'date_6'),
        (7, 'Custom date', 'date_7'),
    )
