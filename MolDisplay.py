import molecule

header = """<svg version="1.1" width="1000" height="1000" 
            xmlns="http://www.w3.org/2000/svg">"""

footer = """</svg>"""

offsetx = 500
offsety = 500

# Wrapper class for the atom struct/class written in C. Mainly used for getting the SVG formatting of an atom
class Atom():

    # Initializes object elements to be same as that of the passed-in atom
    def __init__(self, c_atom):
        self.x = c_atom.x
        self.y = c_atom.y
        self.z = c_atom.z
        self.element = c_atom.element

    # Returns the "string-form" of the object, displaying all the elements of the atom. For debugging purposes
    def __str__(self):
        return f'ATOM INFO\nELEMENT: {self.element}\nx: {self.x}\ny: {self.y}\nz: {self.z}\n'

    # Returns a string with the SVG formatting of the atom
    def svg(self):
        cx = f'{"{:.2f}".format((self.x * 100.0) + offsetx)}'
        cy = f'{"{:.2f}".format((self.y * 100.0) + offsety)}'
        r = f'{radius.get(self.element)}'
        fill = f'{element_name.get(self.element)}'

        return f'  <circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#{fill})"/>\n'

# Wrapper class for the bond struct/class written in C. Mainly used for getting the SVG formatting of a bond
class Bond():

    # Initializes object elements to be same as that of the passed-in bond
    def __init__(self, c_bond):
        self.a1 = c_bond.a1
        self.a2 = c_bond.a2
        self.epairs = c_bond.epairs
        self.atoms = c_bond.atoms
        self.x1 = c_bond.x1
        self.x2 = c_bond.x2
        self.y1 = c_bond.y1
        self.y2 = c_bond.y2
        self.z = c_bond.z
        self.len = c_bond.len
        self.dx = c_bond.dx
        self.dy = c_bond.dy

    # Returns the "string-form" of the object, displaying all the elements of the bond. For debugging purposes
    def __str__(self):
        base_bond_info = f'a1: {self.a1}\na2: {self.a2}\nepairs: {self.epairs}\n'
        computed_bond_info = f'x1: {self.x1}\nx2: {self.x2}\ny1: {self.y1}\ny2: {self.y2}\nz: {self.z}\ndx: {self.dy}\ndy: {self.dy}\nlen: {self.len}\n'

        return f'BOND INFO\n{base_bond_info}{computed_bond_info}'

    # Returns a string with the SVG formatting of the bond
    def svg(self):
        point1 = f'{"{:.2f}".format((self.x1 * 100.0) + offsetx + (self.dy * 10))},{"{:.2f}".format((self.y1 * 100.0) + offsety - (self.dx * 10))}'
        point2 = f'{"{:.2f}".format((self.x1 * 100.0) + offsetx - (self.dy * 10))},{"{:.2f}".format((self.y1 * 100.0) + offsety + (self.dx * 10))}'
        point3 = f'{"{:.2f}".format((self.x2 * 100.0) + offsetx - (self.dy * 10))},{"{:.2f}".format((self.y2 * 100.0) + offsety + (self.dx * 10))}'
        point4 = f'{"{:.2f}".format((self.x2 * 100.0) + offsetx + (self.dy * 10))},{"{:.2f}".format((self.y2 * 100.0) + offsety - (self.dx * 10))}'

        return f'  <polygon points="{point1} {point2} {point3} {point4}" fill="green"/>\n'

# Subclass of the molecule class from molecule.py
class Molecule(molecule.molecule):

    # Returns the "string-form" of the object, displaying all the atoms and bonds within the molecule and their elements.
    # For debugging purposes
    def __str__(self):
        return_string = f'MOLECULE INFO:\n{self.atom_no} ATOMS and {self.bond_no} BONDS\n\n'

        # Adding all the atoms' info to return_string
        for i in range(0, self.atom_no):
            return_string += f'ATOM INDEX {i}:\n' + f'{Atom(self.get_atom(i))}\n'
        
        # Adding all the bonds' info to return_string
        for i in range(0, self.bond_no):
            return_string += f'BOND INDEX {i}:\n' + f'{Bond(self.get_bond(i))}\n'

        return return_string

    # Using the svg() methods in the Bond and Atom classes, assembles and returns the SVG formatting of the molecule
    def svg(self):
        return_string = header

        # current_atom_index and current_bond_index are the variables used to iterate through all the
        # molecule's atoms and bonds 
        current_atom_index = 0
        current_bond_index = 0

        # While loop goes through each atom and bond in the molecule and appends each one to return_string by
        # increasing z-value
        while current_atom_index < self.atom_no or current_bond_index < self.bond_no:
            if current_atom_index < self.atom_no:
                current_atom = Atom(self.get_atom(current_atom_index))
                
                # current_atom_z is a temporary variable that stores the z-value of the current
                # atom. This is to avoid modifying the atom in the else statement where the variable is
                # set to negative infinity when all atoms have been iterated through. Which was done to avoid
                # avoid a possible infinite loop where the last atom is endlessly appended into return_string
                current_atom_z = current_atom.z
            else:
                current_atom_z = float('-inf')
                        
            if current_bond_index < self.bond_no:
                current_bond = Bond(self.get_bond(current_bond_index))
                
                # current_bond_z is a temporary variable that stores the z-value of the current
                # bond. This is to avoid modifying the bond in the else statement where the variable is
                # set to infinity when all bonds have been iterated through. Which was done to avoid
                # avoid a possible infinite loop where the last bond is endlessly appended into return_string
                current_bond_z = current_bond.z
            else:
                current_bond_z = float('inf')

            # Main "sorting algorithm." Appends all the SVG formatting for each atom and bond in the molecule
            # in order of increasing z-value
            if current_atom_z < current_bond_z:
                return_string += current_atom.svg()
                current_atom_index = current_atom_index + 1            
            else:
                return_string += current_bond.svg()
                current_bond_index = current_bond_index + 1

        return_string += footer
        return return_string

    # Takes in an opened SDF file and reads its data into the Molecule object
    def parse(self, file):
        file_data = file.readlines()

        # started_reading is a boolean that sets to true when the start of the molecule information in an
        # SDF is reached. This is to prevent garbage data from being accidentally read in
        started_reading = False
        
        # Main operation involves reading the file line-by-line and parsing different data
        # depending on how many individual elements are on each line (e.g. a line with atom data)
        # has 16 elements after the line's string has been split at every space)
        for line in file_data:
            if 'M  END' in line:
                # Stops reading the file if the line with 'M  END' is reached, which is the last line
                # of relevant info in an SDF file
                break
            elif 'V2000' in line and '999' in line:
                # Set the started_reading boolean to true after the "starting line" in the SDF file
                # so that the lines can start being read
                started_reading = True
                continue

            line_elements = line.split()

            if started_reading:
                # Atom parsing 
                if len(line_elements) == 16:
                    element = line_elements[3]
                    x = float(line_elements[0])
                    y = float(line_elements[1])
                    z = float(line_elements[2])
                    self.append_atom(element, x, y, z)  
                # Bond parsing. 
                elif len(line_elements) == 7:
                    a1 = int(line_elements[0]) - 1
                    a2 = int(line_elements[1]) - 1
                    epairs = int(line_elements[2])
                    self.append_bond(a1, a2, epairs)
