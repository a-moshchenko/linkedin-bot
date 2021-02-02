import csv

from database import Customer, get_all


customers = [i for i in get_all(Customer) if i.email is not None]


with open('employee_email.csv', mode='w') as employee_file:
    employee_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    employee_writer.writerow(['Name', 'Url', 'Email'])
    for customer in customers:
        employee_writer.writerow([customer.name, customer.url, customer.email])
