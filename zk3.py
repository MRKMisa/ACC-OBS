def get_config():
    #načítám z config.ini
    a = "ben"
    b = "afa"
    c = "ahoj"
    d = "Larry"
    
    class Config:
        def __init__(self):
            self.a = a
            self.b = b
            self.c = c
            self.d = d
    
    return Config()
