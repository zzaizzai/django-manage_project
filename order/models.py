import csv
from datetime import datetime, timedelta, date
import os
from typing import List

from django.db import models
from django.conf import settings


class Product(models.Model):
    
    name = models.CharField(max_length=255)
    price = models.IntegerField(null=True)
    
    class Meta:
        managed = False

    def __str__(self):
        return self.name
    
    def get_orders(self) -> List['Order']:
        if self.name != "" or self.name is None:
            orders = Order.get_orders_filter_name(self.name)
            return orders
        else :
            return []
        
    def get_num_orders(self):
        return len(self.get_orders())
    
    def get_quantity(self) -> int:
        count = 0
        for order in self.get_orders():
            count += int(order.quantity)
        return count
    
class Order(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    datetime_order = models.DateTimeField()
    date_due = models.DateTimeField()

    class Meta:
        managed = False

    def __str__(self):
        return f"{self.name} - {self.quantity}"

    def show_info(self):
        return f'Order ID: {self.id},   Quantity: {self.quantity},  Due: {self.formatted_date_due()}'

    @classmethod
    def get_orders_filter_name(cls, name: str) -> List['Order']:
        orders = cls.get_all_orders()
        orders_filterd = [order for order in orders if order.name == name ]
        return orders_filterd

    @classmethod
    def get_all_orders(cls):
        path = os.path.join(settings.BASE_DIR, 'sample_data\data1.csv')
        orders = cls.get_orders_from_csv(path)
        return orders

    @classmethod
    def get_orders_from_csv(cls, csv_path) -> List['Order']:
        with open(csv_path, 'r') as csvfile:
            csvreader = csv.DictReader(csvfile)
            orders = []
            for row in csvreader:
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