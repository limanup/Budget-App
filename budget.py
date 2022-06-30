class Category:

    # create a new class object with name 'self', giving it ledger list, balance, item
    def __init__(self, name):
        self.name = name
        self.ledger = list()
        self.balance = 0
        self.item = dict()

    # create a 'deposit' method 
    def deposit(self, amount, desc=''):
        self.item = {'amount': amount, 'description': desc}
        self.balance = self.balance + float(amount)
        self.ledger.append(self.item)
        # print(self.item, self.balance, self.ledger)

    # create a 'withdraw' method, only withdraw when balance is more than amount
    def withdraw(self, amount, desc=''):
        blncheck = self.check_funds(amount)
        if blncheck:
            self.item = {'amount': -amount, 'description': desc}
            self.balance = self.balance - float(amount)
            self.ledger.append(self.item)
        return blncheck

    # create a get_balance method that returns the current balance
    def get_balance(self):
        return self.balance

    # create a transfer method which transfers amount from 1 category to another
    # only transfer if balance is more than transfer amount
    def transfer(self, amount, transfer_to):
        blncheck = self.check_funds(amount)
        if blncheck:
            self.withdraw(amount, 'Transfer to ' + transfer_to.name)
            transfer_to.deposit(amount, 'Transfer from ' + self.name)
        return blncheck

    # create a check_funds method that checks input amount vs balance
    # it returns false if amount is > balance, true if amount <= balance
    # amount has to be positive
    # https://www.geeksforgeeks.org/print-objects-of-a-class-in-python/
    def check_funds(self, amount):
        if amount >= 0 and amount <= self.balance:
            return True
        else:
            return False

    # print out the output in a table format
    # __repr__ is used if we need a detailed information for debugging while 
    # __str__ is used to print a string version for the users.
    def __str__(self):
        # header
        header = self.name.center(30, '*') + '\n'

        # item list & amount
        body = str() 
        for entry in self.ledger:
            # figure out length of word, space, amount
            word = entry['description']
            # take only up to 23 characters
            word = word[:min(len(word), 23)]
            num = str(f"{entry['amount']:.2f}")

            # concatenate each line
            body += word.ljust(23) + num.rjust(7) + '\n'

        # Total amount
        total = 'Total: ' + str(f"{self.get_balance():.2f}") 

        # combine header, body and total line
        result = header + body + total
        return result



def create_spend_chart(categories):
    # assign total expenses to each category
    dctexpense = dict()
    dctpctexpense = dict()

    # each cat (category) is an object of class
    for cat in categories:
        # start total expenses at 0
        expenses = 0
        # loop through all dictionaries (entry) in the ledger list (list of dictionaries)
        for entry in cat.ledger:
            # do not include if its a deposit (i.e. amount > 0)
            if entry['amount'] > 0 : continue
            # adds up all expenses (minus becuz all negative number)
            expenses = expenses - entry['amount']
        dctexpense[cat.name] = expenses
    
    # sum up total expenses across all categories
    total_expense = sum(dctexpense.values())

    # start constructing final result strchart
    strchart = 'Percentage spent by category'
    # loop through % vertical axis
    # percentage number in desc order, 100 -> 90 -> 80 
    for i in range(100, -10, -10):
        # concatenate to strchart, right justify % number
        strchart += '\n' + str(i).rjust(3) + '| '
        # loop through categories on horizontal axis
        for cat in dctexpense.keys():
            # calculate percentage for each category
            dctpctexpense[cat] = (dctexpense[cat] / total_expense) * 10 // 1 * 10
            if dctpctexpense[cat] >= i:
                # add 'o' to chart if the category % is more than chart %, also add 2 spaces
                strchart += 'o  '
            else:
                # add 3 spaces if not 
                strchart += ' ' * 3
    # end of 2 for loops, end of bar chart

    
    # find total number of dashes
    total_dash = 1 + len(categories) * 3
    # add 4 spaces before dashes
    strchart += '\n' + ' ' * 4 + '-' * total_dash

    # construct horizontal axis labels 
    # loop through from 0 to longest string length (vertical loop)
    for i in range(max( [ len(key) for key in dctexpense.keys() ] ) ):
        # start the line with 5 spaces
        strchart = strchart + '\n' + ' ' * 5
        # loop through each category (horizontal loop)
        for cat in dctexpense.keys():
            # the category name is all shown, add 3 spaces 
            if i > len(cat) - 1:
                strchart += ' ' * 3
            else:
                strchart += cat[i] + ' ' * 2
    
    return strchart


        

# # test cases
# food = Category("Food")
# food.deposit(1000, "initial deposit")
# food.withdraw(10.15, "groceries")
# food.withdraw(15.89, "restaurant and more food for dessert")
# print(food.get_balance())
# clothing = Category("Clothing")
# food.transfer(50, clothing)
# clothing.withdraw(25.55)
# clothing.withdraw(100)
# auto = Category("Auto")
# auto.deposit(1000, "initial deposit")
# auto.withdraw(15)

# print(food)
# print(clothing)
# print(auto)

# print(create_spend_chart([food, clothing, auto]))

# print(food.ledger)
# print(clothing.ledger)