class Course:
    def __init__(self, name, section, start, end, credits, instructor, ta):
        self.name = name
        self.section = section
        self.start = start
        self.end = end
        self.credits = credits
        self.instructor = instructor
        self.ta = ta
    
    def get_name(self):
        return self.name
        
    def get_section(self):
        return self.section
        
    def get_start(self):
        return self.start
        
    def get_end(self):
        return self.end
        
    def get_credits(self):
        return self.credits
        
    def get_instructor(self):
        return self.instructor
        
    def get_ta(self):
        return self.ta
