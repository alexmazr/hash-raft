not_found = "404"
success = "200"

class SimpleCache:
    def __init__ (self):
        self.cache = {}
    
    def add (self, key, value = None):
        if key not in self.cache:
            self.cache [key] = value
            return success
        return not_found

    def update (self, key, value):
        if key in self.cache:
            self.cache [key] = value
            return success
        return not_found

    def get (self, key):
        if key in self.cache:
            return self.cache [key]
        return not_found

    def remove (self, key):
        if key in self.cache:
            del self.cache [key]
            return success
        return not_found
        