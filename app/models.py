from . import db

def is_authenticated(self):
    return True    

def is_active(self):
    return True    

def is_anonymous(self):
    return False    

def get_id(self):
    try:
        return unicode(self.id)  # python 2 support    
    except NameError:    
        return str(self.id)  # python 3 support         