import csv
from datetime import datetime, timedelta, date

from django.db import models



class Order(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=10)
    quantity = models.PositiveIntegerField()
    datetime_order = models.DateTimeField()
    date_due = models.DateTimeField()

    class Meta:
        managed = False

    def __str__(self):
        return f"{self.name} - {self.quantity}"
    
    @classmethod
    def get_orders_from_csv(cls, csv_path) -> list['Order']:
        with open(csv_path, 'r') as csvfile:
            csvreader = csv.DictReader(csvfile)
            orders = []
            for row in csvreader:
                print(row)
                order = cls(
                    id=row['id'],
                    name=row['name'],
                    quantity=row['quantity'],
                    datetime_order= datetime.strptime(row['datetime_order'],  "%Y-%m-%d %H:%M:%S"),
                    date_due=datetime.strptime(row['date_due'],  "%Y-%m-%d %H:%M:%S").date()
                )
                orders.append(order)
            
        return orders

    def formatted_datetime_orderd(self) -> str:
        return self.datetime_order.strftime("%Y-%m-%d %H:%M") or "Time Error"
    
    def formatted_date_due(self) -> str:
        return self.date_due.strftime("%Y-%m-%d") or "Time Error"
    
    def get_d_days(self) -> int:
        difference  = self.date_due - date.today()
        return difference.days
    
    def show_d_days(self) -> str:
        return str(self.get_d_days())