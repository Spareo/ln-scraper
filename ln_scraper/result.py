class Result:
    def __init__(self, results_dict):
        self.results_dict = results_dict

    @property
    def address(self):
        address = self.results_dict.get("Address", None)
        return address

    @property
    def image_url(self):
        image_url = self.results_dict.get("ImageURL", None)
        return image_url

    @property
    def property_url(self):
        property_url = self.results_dict.get("PropertyURL", None)
        return property_url

    @property
    def price(self):
        price = self.results_dict.get("Price", None)
        return price
    
    @property   
    def num_units(self):
        num_units = self.results_dict.get("No. Units", None)
        return num_units

    @property
    def property_type(self):
        property_type = self.results_dict.get("Property Type", None)
        return property_type

    @property
    def sub_property_type(self):
        sub_property_type = self.results_dict.get("Property Sub-type", None)
        return sub_property_type

    @property
    def building_class(self):
        building_class = self.results_dict.get("Building Class", None)
        return building_class

    @property
    def cap_rate(self):
        cap_rate = self.results_dict.get("Cap Rate", None)
        return cap_rate

    @property
    def num_stories(self):
        num_stories = self.results_dict.get("No. Stories", None)
        return num_stories

    @property
    def year_built(self):
        year_built = self.results_dict.get("Year Built", None)
        return year_built

    @property
    def avg_occupancy(self):
        avg_occupancy = self.results_dict.get("Average Occupancy", None)
        return avg_occupancy
    
    @property
    def avg_rent(self):
        avg_rent = self.results_dict.get("MIX_INFO_Avg. Rent/Mo", None)
        return avg_rent

    @property
    def avg_unit_size(self):
        avg_unit_size = self.results_dict.get("MIX_INFO_Sq. Ft.", None)
        return avg_unit_size