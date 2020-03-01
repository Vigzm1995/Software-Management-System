'''
    Script Author: Vignesh Mohan
    Python Version: 3.0
'''

'''Program for e-Commerce Solution'''

#Importing the Unittest
import unittest
import os
#Importing default dictionary from collections.
from collections import defaultdict
#Importing prettytable module.
from prettytable import PrettyTable
#File_reader import from Homework 8.
from HW08VigneshMohan_Part2_810 import file_read
#from HW09VigneshMohan810 import file_read

def file_reader(path, fields, sep='\t', header=False):
    try:
        path = open(path, 'r')

    except FileNotFoundError:
        print('File Not present in this directory:', path)                  #File reader Functionalities implemented.

    else:
        with path:
            for line_num, line in enumerate(path, 1):
                line = line.strip()
                elements = line.split(sep)

                if len(elements) == fields:
                    if header is True and line_num == 1:
                        continue
                    yield tuple(elements)
                
                else:
                    #print('valueError: has', len(elements), 'field on line', line_num, 'but expected', fields)
                    raise ValueError

class EcommerceStore:
    
    ''' Stores all the information about Stores and Customers'''

    def __init__(self, wdir, ptables = True):
        self._wdir = wdir #Directory with stores, customers, inventory, transactions and products files
        self._stores = dict() #key: cwid value: instance of class stores
        self._customers = dict() #key: cwid value: instance of class customers
        
        self._inventory = dict() #key: cwid value: instance of class inventory
        self._transactions = dict() #key: cwid value: instance of class transactions
        self._products = dict() #key: cwid value: instance of class products

        self._get_stores(os.path.join(wdir, 'stores.txt')) #Read stores file
        self._get_customers(os.path.join(wdir, 'customers.txt')) #Read customers file
        self._get_inventory(os.path.join(wdir, 'inventory.txt')) #Read inventory file
        self._get_transactions(os.path.join(wdir, 'transactions.txt')) #Read transactions file
        self._get_products(os.path.join(wdir, 'products.txt')) #Read products file

        if ptables:
            print ('\n Store Table Summary')
            self.stores_table()                                                             #Printing the Prettytable module.
                                                                        
            print ('\n Customer Table Summary')
            self.customers_table()
    
    def _get_stores(self, path):

        try:
            for store_id, store_name, in file_reader(path, 2, sep = '*', header = True):
                #store_id verification.
                if store_id in self._stores.keys():
                    print (f' Warning: store_id {store_id} already read from the file')
                else:
                    #Storing the store id as a key.
                    self._stores[store_id] = Stores(store_id, store_name)
        except ValueError as e:
            print(e)

    def _get_customers(self, path):
        
        try:
            for customer_id, customer_name in file_reader(path, 2, sep = ',', header = True):
                #Cusomer Id verification
                if customer_id in self._customers.keys():
                    print (f' Warning: customer_id {customer_id} already read from the file')
                else:
                    #Storing customer id as a key.
                    self._customers[customer_id] = Customers(customer_id, customer_name)
        except ValueError as e:
            print(e)

    
    def _get_inventory(self, path):
            
            try:
                for store_id, quantity, product_id in file_reader(path, 3, sep = '|', header = True):
                    index = int(quantity)
                    if store_id in self._stores.keys():
                        if product_id in self._stores[store_id]._items.keys():
                            print (f' Warning: product_id {product_id} already read from the file')
                        else:
                            self._stores[store_id].add_product(product_id, index)
                    else:
                        print(f"Warning: Store_id {store_id} is not in the stores file")
            
            except ValueError as e:
                print(e)

    def _get_transactions(self, path):
        
            try:
                for customer_id, quantity, product_id, store_id in file_reader(path, 4, sep = '|', header = True):
                    rest = self._stores[store_id]._items[product_id]
                    index = int(quantity)                     
                    if customer_id in self._customers.keys():
                        if rest >= index:
                            self._customers[customer_id].add_values(product_id, index)
                            self._stores[store_id].del_prod(product_id, index)
                        else:
                            self._customers[customer_id].add_values(product_id, rest)
                            self._stores[store_id].del_prod(product_id, rest)
                    else:
                        print (f' Warning: store_id {customer_id} already read from the file')
                    

                    if product_id in self._products.keys():
                        if rest > index:
                            self._products[product_id].add_product(customer_id, index)
                        else:
                            self._products[product_id].add_product(customer_id, rest)
            except ValueError as e:
                print(e)

    def _get_products(self, path):
        
            try:
                for id1, store_id, product_name in file_reader(path, 3, sep = '|', header = False):
                    if id1 in self._products.keys():
                       print (f' Warning: store_id {id1} already read from the file')
                    else:
                        self._products[id1] = Products(id1, store_id, product_name)
            except ValueError as e:
                print(e)
                
    def customers_table(self):
        pt = PrettyTable(field_names=["Customer Name", "Product", "Quantity Sold"])
        for cust in self._customers.values():
            for row in cust.pt_row():
                pt.add_row(row)

        print(pt)

    def stores_table(self):
        pt = PrettyTable(field_names=["Store Name", "Product Name ", "Customer Name", "Quantity Sold"])
        for store in self._stores.values():
            for row in store.pt_row():
                pt.add_row(row)
        print(pt)


class Stores:
    ''' Represents a store details '''
    pt_lables = ['Store Name', 'Customer', 'Product', 'Quantity Sold']

    def __init__(self, store_id, store_name):
        self.store_id = store_id
        self.store_name = store_name    

        self._items = defaultdict(int)

    def add_product(self, product_id, quantities):
        self._items[product_id] += quantities
    
    def del_prod(self, product_id, quantities):
        self._items[product_id] -= quantities
    
class Customers:
    #Labels for the class customer.
    pt_labels = ['Name', 'Quantity', 'Product']

    def __init__(self, customer_id, customer_name):
        self._customer_id = customer_id
        self._customer_name = customer_name
        self._prod = defaultdict(int)

        def add_values(self, product_id, quantity):
            self._prod[product_id] += quantity

class Products:

    pt_labels = ['Customer Name', 'Product', 'Quantity Purchased']

    def __init__(self, product_name, product_id, store_id):
        self._product_name = product_name
        self._product_id = product_id
        self._store_id = store_id    
        self._products = defaultdict(int)
    
    def add_item(self, customer_id, quantity):
        self._products[customer_id] += quantity
        
def main():
    
    #wdir = "Users\Vignesh\PycharmProjects"
    #stevens = EcommerceStore(wdir)
    EcommerceStore(r"C:\Users\Vignesh\PycharmProjects")

class EcommerceStoreTest(unittest.TestCase)
    def test_EcommerceStore(self):
        #wdir = "Users\Vignesh\PycharmProjects"
        #stevens = EcommerceStore(wdir)
        EcommerceStore(r"C:\Users\Vignesh\PycharmProjects")

        expected_store = [ Maha's Movies, Grinch movie tickets,  ['Debugging Dinesh', 'GitHub Gus','10' ],[Maha's Movies, Grinch movie tickets,['Debugging Dinesh', 'GitHub Gus'],10],[Ben's Books, Java Programming Jokes, ['Architect Armin', 'Debugging Dinesh', 'GitHub Gus'],1][Ben's Books, Python Programming Pearls, ['Architect Armin', 'Debugging Dinesh', 'GitHub Gus'], 3][Ben's Books, Job Interview Tips, ['Architect Armin', 'Debugging Dinesh', 'GitHub Gus'],2][Dariel's Donuts, Chocolate donuts, ['Architect Armin', 'GitHub Gus'],36][Dariel's Donuts, Coffee, ['Architect Armin', 'Debugging Dinesh', 'GitHub Gus'], 25]]      
        expected_customer = [Debugging Dinesh, Job Interview Tips,1][Debugging Dinesh, Grinch movie tickets,6][Debugging Dinesh, Python Programming Pearls,1       Debugging Dinesh, Coffee,11      Architect Armin, Python Programming Pearls,1       Architect Armin, Coffee,8    Architect Armin, Chocolate donuts,16     GitHub Gus, Python Programming Pearls,1      GitHub Gus, Chocolate donuts,20      GitHub Gus, Job Interview Tips,1       GitHub Gus, Bohemian Rhapsody movie tickets, 4       GitHub Gus, Coffee, 6       GitHub Gus, Grinch movie tickets, 4]  


        stores_ptable = [s.pt_row() for s in stevens._students.values()]
        customers_ptables = [row for Instructor in stevens._instructors.values() for row in Instructor.pt_row()]

        self.assertEqual(stores_ptable, expected_store)
        self.assertEqual(customer_ptable, expected_customer)

if __name__ == '__main__':
    main()
    unittest.main(exit=False, verbosity=2)



