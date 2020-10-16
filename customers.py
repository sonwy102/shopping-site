"""Customers at Hackbright."""


class Customer(object):
    """Ubermelon customer."""

    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
    

    def __repr__(self):
        """Convenience method to show information about customer in console."""

        return "<Customer: {}, {}, {}>".format(self.first_name, 
                                               self.last_name,
                                               self.email)


def read_customer_from_file(filepath):

    customers = open(filepath)
    customers_data = {}

    for line in customers:

        (first_name, 
        last_name, 
        email, 
        password) = line.strip().split('|')
        
        customers_data[email] = Customer(first_name, 
                                         last_name,
                                         email,
                                         password)
    
    return customers_data
        
def get_by_email(email):
    
    return customers_data[email]

customers_data = read_customer_from_file('customers.txt')

