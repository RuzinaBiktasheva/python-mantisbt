from models.project import Project
import random
import string

def random_name(prefix, maxlen):
    symbols = string.ascii_letters
    return prefix + ''.join([random.choice(symbols) for i in range(random.randrange(maxlen))])

testdata = [
    Project(name=random_name('Project_name: ', 10), status = 'development', view_status = 'public', description = 'Description - 1')
]