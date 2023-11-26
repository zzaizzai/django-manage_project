import csv
from faker import Faker
from datetime import datetime, timedelta
from itertools import cycle



def create_fake_data():
    fake = Faker()

    # CSV path
    csv_file_path = 'sample_data.csv'

    # header
    fields = ['id', 'name', 'quantity', 'datetime_order', 'date_due']

    # 가상의 주문 데이터 생성 및 CSV 파일에 저장
    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()

        # 5건씩 반복되는 name 리스트 생성
        names = [fake.uuid4()[:8].upper() for _ in range(20)]  # 20개의 고유 name 생성
        names_cycle = cycle(names)

        for idx in range(1, 101):
            product_number = next(names_cycle)
            quantity = fake.random_int(min=1, max=10)
            datetime_order = fake.date_time_between(start_date='-30d', end_date='now')
            date_due = datetime_order + timedelta(days=fake.random_int(min=7, max=14))

            writer.writerow({
                'id': idx,
                'name': product_number,
                'quantity': quantity,
                'datetime_order': datetime_order,
                'date_due': date_due,
            })
    print(f"Created {csv_file_path}")

if __name__ == "__main__":
    create_fake_data()
