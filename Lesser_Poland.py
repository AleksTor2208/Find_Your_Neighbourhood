
class Area:
    
    def __init__ (self, name, the_type):
        self.name = name
        self.the_type = the_type

class Province(Area):
    def __init__ (self, name, the_type):
        super().__init__ (name, the_type)
        
        self.counties = []

    def add_county(self, county):        
        self.counties.append(county)

class County(Area):
    def __init__ (self, name, the_type):
        super().__init__(name, the_type)

        self.communities = []

    def add_community(self, community):        
        self.communities.append(community)

class Municipality(Area):
    def __init__ (self, name, the_type):
        super().__init__(name, the_type)

        self.cities = []
    
class Rural_commune(Area):
    def __init__ (self, name, the_type):
        super().__init__(name, the_type)

        self.rural_areas = []

class Urban_rural_commune(Area):
    def __init__ (self, name, the_type):
        super().__init__(name, the_type)

        self.urban_areas = []

class Rural_area(Area):
    def __init__ (self, name, the_type):
        super().__init__(name, the_type)

class City(Area):
    def __init__ (self, name, the_type):
        super().__init__(name, the_type)

class Town_wth_district_rights(Area):
    def __init__ (self, name, the_type):
        super().__init__ (name, the_type)

class Delegacy(Area):
    def __init__ (self, name, the_type):
        super().__init__ (name, the_type)



