class MD5:
    def __init__(self, hasher):
        self.hasher = hasher

    def execute(self, text):
        return self.hasher(text.encode('utf8')).hexdigest()
