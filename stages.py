import pypyodbc


class Lookup:
    def __init__(self, items):
        self.items = items

    def __iter__(self):
        for item in self.items:
            yield (item)


conn = pypyodbc.connect(
    "Driver={SQL Server};"
    "Server=LAPTOP-8DPA66RQ;"
    "Database=db1;"
    "Trusted_Connection=yes;"
)
cursor = conn.cursor()
select1 = ("SELECT name,name "
           "FROM UserDash2 ")
cursor.execute(select1)
result1 = cursor.fetchall()
print(result1)
result2 = [('Round1', 'Round 1'),
           ('Round2', 'Round 2'),
           ('Round3', 'Round 3'),
           ('Round4', 'Round 4'),
           ('HR', 'HR'),
           ('Offer', 'Offer'),
           ('Joined', 'Joined')]

result3 = [('Scheduled', 'Scheduled'),
           ('Selected', 'Selected'),
           ('Rejected', 'Rejected'),
           ('On Hold', 'On Hold'),
           ('Offer Rolled out', 'Offer Rolled out'),
           ('Offer Accepted', 'Offer Accepted'),
           ('Offer Declined', 'Offer Declined')]
result4 = [
           ('1001', '1001'),
           ('1002', '1002'),
           ('1003', '1003'),
           ('1004', '1004'),
           ('1005', '1005'),
           ('1006', '1006')]
choices = [('Skills', 'Skills'),
           ('Job ID', 'Job ID'),
           ('Notice Period', 'Notice Period'),
           ('Status', 'Status')]
