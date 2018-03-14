import django_tables2 as tables
import itertools

class SimpleTable(tables.Table):
	class Meta:
		attrs = {'class': 'mytable'}