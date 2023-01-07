
def get_coords(coordinate:str):
    def convert_to_decimal(string):
        return float(string)
    return tuple(map(convert_to_decimal,map(str.strip,coordinate.strip().split(','))))

print(get_coords("23.22, 56.77"))
