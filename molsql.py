import MolDisplay
import sqlite3
import os

# Handles visualizing molecules using an SQLite3 Database
class Database:

    # Creates/opens a database connection to a file in the local directory called
    # "molecules.db" and stores it as a class attribute. If the reset parameter is
    # set to True, it will delete the file "molecules.db" so a fresh database
    # is created upon connection
    def __init__(self, reset):

        # Resetting the molecules databse if it has been found in local directory
        if reset == True and os.path.exists("molecules.db"):
            os.remove("molecules.db")
        
        self.conn = sqlite3.connect("molecules.db")
        self.conn.cursor()

    # Creates tables as per the assignment description. If any of the tables already
    # exist, the method leaves them alone and doesn't re-create them.
    def create_tables(self):

        # Create Elements table
        self.conn.execute("""CREATE TABLE IF NOT EXISTS Elements (
                                ELEMENT_NO      INTEGER     NOT NULL,
                                ELEMENT_CODE    VARCHAR(3)  NOT NULL,
                                ELEMENT_NAME    VARCHAR(32) NOT NULL,
                                COLOUR1         CHAR(6)     NOT NULL,
                                COLOUR2         CHAR(6)     NOT NULL,
                                COLOUR3         CHAR(6)     NOT NULL,
                                RADIUS          DECIMAL(3)  NOT NULL,
                                PRIMARY KEY (ELEMENT_CODE));""")
        
        # Create Atoms table
        self.conn.execute("""CREATE TABLE IF NOT EXISTS Atoms (
                                ATOM_ID         INTEGER         NOT NULL    PRIMARY KEY AUTOINCREMENT,
                                ELEMENT_CODE    VARCHAR(3)      NOT NULL,
                                X               DECIMAL(7, 4)   NOT NULL,
                                Y               DECIMAL(7, 4)   NOT NULL,
                                Z               DECIMAL(7, 4)   NOT NULL,
                                FOREIGN KEY (ELEMENT_CODE) REFERENCES Elements(ELEMENT_CODE));""")    

        # Create Bonds table
        self.conn.execute("""CREATE TABLE IF NOT EXISTS Bonds (
                                BOND_ID     INTEGER     NOT NULL        PRIMARY KEY AUTOINCREMENT,
                                A1          INTEGER     NOT NULL,
                                A2          INTEGER     NOT NULL,
                                EPAIRS      INTEGER     NOT NULL);"""
                          )

        # Create Molecules table
        self.conn.execute("""CREATE TABLE IF NOT EXISTS Molecules (
                                MOLECULE_ID     INTEGER     NOT NULL    PRIMARY KEY AUTOINCREMENT,
                                NAME            TEXT    NOT NULL    UNIQUE);"""
                          )
        
        # Create MoleculeAtom table
        self.conn.execute("""CREATE TABLE IF NOT EXISTS MoleculeAtom (
                                MOLECULE_ID     INTEGER     NOT NULL,
                                ATOM_ID         INTEGER     NOT NULL,
                                PRIMARY KEY (MOLECULE_ID, ATOM_ID),
                                FOREIGN KEY (MOLECULE_ID) REFERENCES Molecules(MOLECULE_ID),
                                FOREIGN KEY (ATOM_ID) REFERENCES Atoms(ATOM_ID));"""
                          )
        
        # Create MoleculeBond table
        self.conn.execute("""CREATE TABLE IF NOT EXISTS MoleculeBond (
                                MOLECULE_ID     INTEGER     NOT NULL,
                                BOND_ID         INTEGER     NOT NULL,
                                PRIMARY KEY (MOLECULE_ID, BOND_ID),
                                FOREIGN KEY (MOLECULE_ID) REFERENCES Molecules(MOLECULE_ID),
                                FOREIGN KEY (BOND_ID) REFERENCES Bonds(BOND_ID));"""
                          )
        
        self.conn.commit()
        
    # Uses indexing to set the values in the table named table based on the
    # whatever is in the values tuple
    def __setitem__(self, table, values):
        self.conn.execute(f'''INSERT OR IGNORE
                                INTO        {table}
                                VALUES      {values};'''
                          )

        self.conn.commit()

    # Adds the attributes of the atom object to the Atoms table, then adds an entry into
    # the MoleculeBond table that links the named molecule to the atom entry in the Atoms
    # table
    def add_atom(self, molname, atom):
        cursor = self.conn.cursor()

        # Inserting attributes of the Atom object into the Atoms table
        cursor.execute(f'''INSERT
                                INTO    Atoms   (ELEMENT_CODE,      X,          Y,          Z)
                                VALUES          ('{atom.element}',  {atom.x},   {atom.y},   {atom.z});'''
                       )
        
        atom_id = cursor.lastrowid

        # Getting the molecule ID for the Molecule named the same as molname
        cursor.execute(f'''SELECT * FROM Molecules WHERE NAME = '{molname}';''')
        mol = cursor.fetchall()
        mol_id = mol[0][0]

        # Adding the linking entry into the MoleculeAtom table
        self.conn.execute(f'''INSERT OR IGNORE
                                INTO MoleculeAtom   (MOLECULE_ID,   ATOM_ID)
                                VALUES              ({mol_id},      {atom_id});'''
                          )

        self.conn.commit()

    # Adds the attributes of the bond object to the Bonds table, then adds an entry into
    # the MoleculeBond table that links the named molecule to the bond entry in the Bonds
    # table
    def add_bond(self, molname, bond):
        cursor = self.conn.cursor()

        # Inserting attributes of the Bond object into the Bonds table
        cursor.execute(f'''INSERT
                            INTO    Bonds   (A1,        A2,         EPAIRS)
                            VALUES          ({bond.a1}, {bond.a2},  {bond.epairs});'''
                       )

        bond_id = cursor.lastrowid

        # Getting the molecule ID for the Molecule named the same as molname
        cursor.execute(f'''SELECT * FROM Molecules WHERE NAME = '{molname}';''')
        mol = cursor.fetchall()
        mol_id = mol[0][0]

        # Adding the linking entry into the MoleculeBond table
        self.conn.execute(f'''INSERT OR IGNORE
                                INTO MoleculeBond   (MOLECULE_ID,   BOND_ID)
                                VALUES              ({mol_id},      {bond_id});'''
                          )

        self.conn.commit()

    # Creates a MolDisplay.Molecule object, call its parse method on the fp parameter, adds
    # an entry to the Molecules table and adds all its bonds and atoms on the database.
    def add_molecule (self, name, fp):
        molecule = MolDisplay.Molecule()

        molecule.parse(fp)

        # Inserting the new molecule into Molecules
        self.conn.execute(f'''INSERT
                                INTO Molecules  (NAME)
                                VALUES          ('{name}');'''
                          )
        
        self.conn.commit()

        # Adding every atom and bond of the passed Molecule into their appropriate tables
        for i in range (0, molecule.atom_no):
            self.add_atom(name, MolDisplay.Atom(molecule.get_atom(i))) 

        for i in range (0, molecule.bond_no):
            self.add_bond(name, MolDisplay.Bond(molecule.get_bond(i)))

    # Returns a MolDisplay.Molecule object initialized based on the molecule named in the name parameter
    def load_mol(self, name):
        return_molecule = MolDisplay.Molecule()

        cursor = self.conn.cursor()

        # Getting all Atoms in the named molecule
        cursor.execute(f'''SELECT * FROM Atoms
                        INNER JOIN MoleculeAtom ON Atoms.ATOM_ID=MoleculeAtom.ATOM_ID
                        INNER JOIN Molecules ON MoleculeAtom.MOLECULE_ID=Molecules.MOLECULE_ID 
                        WHERE NAME='{name}';'''
                       )
        atoms = cursor.fetchall()
        atoms.sort(key = lambda x: x[0])

        # Adding all Atoms to the MolDisplay.Molecule object
        for i in atoms:
            return_molecule.append_atom(i[1], i[2], i[3], i[4])

        # Getting all Bonds in the named molecule
        cursor.execute(f'''SELECT * FROM Bonds
                        INNER JOIN MoleculeBond ON Bonds.BOND_ID=MoleculeBond.BOND_ID
                        INNER JOIN Molecules ON MoleculeBond.MOLECULE_ID=Molecules.MOLECULE_ID 
                        WHERE NAME='{name}';'''
                       )
        bonds = cursor.fetchall()
        bonds.sort(key = lambda x: x[0])

        # Adding all bonds to the MolDisplay.Molecule object
        for i in bonds:
            return_molecule.append_bond(i[1], i[2], i[3])        

        return return_molecule

    # Returns a dictionary mapping ELEMENT_CODE values to RADIUS values based
    # on the Elements table
    def radius(self):
        radius_dictionary = {}

        # Getting all elements
        cursor = self.conn.cursor()
        cursor.execute(f'''SELECT * FROM ELEMENTS;''')
        elements = cursor.fetchall()

        # Adding all elements and their radiuses into the dictionary
        for i in elements:
            radius_dictionary[i[1]] = i[6]

        return radius_dictionary

    # Returns a dictionary mapping ELEMENT_CODE values to ELEMENT_NAME
    # values based on the Elements table
    def element_name(self):
        name_dictionary = {}

        # Getting all elements
        cursor = self.conn.cursor()
        cursor.execute(f'''SELECT * FROM ELEMENTS;''')
        elements = cursor.fetchall()

        # Adding all elements and their names into the dictionary
        for i in elements:
            name_dictionary[i[1]] = i[2]

        return name_dictionary

    # Returns a string consisting of multiple concatenations of the colour codes for all elements
    # in the database
    def radial_gradients(self):
        radial_gradient_svg = f'''<radialGradient id="default" cx="-50%" cy="-50%" r="220%" fx="20%" fy="20%">
                    <stop offset="0%" stop-color="#808080"/>
                    <stop offset="50%" stop-color="#000000"/>
                    <stop offset="100%" stop-color="#FF0000"/>
                </radialGradient>'''

        # Getting all elements
        cursor = self.conn.cursor()
        cursor.execute(f'''SELECT * FROM ELEMENTS;''')
        elements = cursor.fetchall()

        # Adding all elements to the string
        for i in elements:
            radial_gradient_svg += f'''<radialGradient id="{i[2]}" cx="-50%" cy="-50%" r="220%" fx="20%" fy="20%">
                    <stop offset="0%" stop-color="#{i[3]}"/>
                    <stop offset="50%" stop-color="#{i[4]}"/>
                    <stop offset="100%" stop-color="#{i[5]}"/>
                </radialGradient>'''
            
        return radial_gradient_svg
    