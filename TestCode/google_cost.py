

def calc(minutes):
    return (minutes*60)*(0.006/15)

while True:
    minutes = input('How many minutes would you like to trascribe?: ')
    while type(minutes) != int:
        minutes = input('Type an int/float value. How many minutes would you like to trascribe?: ')
    minutes
    print('TOTAL COST FOR {} MINUTES: '.format(minutes), calc(minutes))
