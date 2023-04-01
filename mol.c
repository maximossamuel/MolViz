/*
 * Maximos Samuel
 * 1184139
 * maximos@uoguelph.ca
 * CIS*2750 Assignment 1
 */

#include "mol.h"

/*
 * Copies the values pointed to by element, x, y and z into atom
 */
void atomset (atom *atom, char element[3], double *x, double *y, double *z)
{
    if (atom == NULL)
    {
        fprintf (stderr, "atom passed into atomset is NULL. Exiting function.\n");
        return;
    }
    
    strcpy (atom->element, element);

    atom->x = *x;
    atom->y = *y;
    atom->z = *z;
}

/*
 * Copies the values stored in atom to the locations pointed to by x, y and z
 */
void atomget (atom *atom, char element[3], double *x, double *y, double *z)
{
    if (atom == NULL)
    {
        fprintf (stderr, "atom passed into atomget is NULL. Exiting function.\n");
        return;
    }

    strcpy (element, atom->element);

    *x = atom->x;
    *y = atom->y;
    *z = atom->z;
}

/*
 * Copies the values a1, a2 and epairs into the corresponding structure attributes in bond
 */
void bondset (bond *bond, unsigned short *a1, unsigned short *a2, atom **atoms, unsigned char *epairs)
{
    if (bond == NULL)
    {
        fprintf (stderr, "bond passed into bondset is NULL. Exiting function.\n");
        return;
    }

    bond->a1 = *a1;
    bond->a2 = *a2;
    bond->epairs = *epairs;
    bond->atoms = *atoms;

    compute_coords (bond);
}

/*
 * Copies the structure attributes in bond to their corresponding arguments
 */
void bondget (bond *bond, unsigned short *a1, unsigned short *a2, atom **atoms, unsigned char *epairs)
{
    if (bond == NULL)
    {
        fprintf (stderr, "bond passed into bondset is NULL. Exiting function.\n");
        return;
    }

    *a1 = bond->a1;
    *a2 = bond->a2;
    *epairs = bond->epairs;
    *atoms = bond->atoms;
}

/*
 * Computes the z, x1, y1, x2, y2, len, dx, and dy values of the bond and sets
 * them in the appropriate structure member variables
 */
void compute_coords (bond *bond){
    if (bond == NULL || bond->atoms == NULL){
        return;
    }

    bond->x1 = bond->atoms[bond->a1].x;
    bond->y1 = bond->atoms[bond->a1].y;
    
    bond->x2 = bond->atoms[bond->a2].x;
    bond->y2 = bond->atoms[bond->a2].y;

    bond->z = (bond->atoms[bond->a1].z + bond->atoms[bond->a2].z) / 2;

    bond->len = sqrt (pow (bond->x1 - bond->x2, 2) + pow (bond->y1 - bond->y2, 2));

    bond->dx = (bond->x2 - bond->x1) / bond->len;
    bond->dy = (bond->y2 - bond->y1) / bond->len;
}

/*
 * Returns the address of a malloced area of memory, large enough to hold a molecule.
 *
 * @param atom_max This value gets copied into the atom_max variable in the structure
 * @param bond_max This value gets copied into the bond_max variable in the structure
 */
molecule *molmalloc (unsigned short atom_max, unsigned short bond_max)
{
    molecule *newMolecule = malloc (sizeof (molecule));

    if (newMolecule == NULL)
    {
        fprintf (stderr, "ERROR: malloc failed. Returning NULL.\n");
        return NULL;
    }

    newMolecule->atom_max = atom_max;
    newMolecule->bond_max = bond_max;

    newMolecule->atom_no = 0;
    newMolecule->bond_no = 0;

    if (atom_max <= 0)
    {
        newMolecule->atoms = NULL;
        newMolecule->atom_ptrs = NULL;
    }
    else
    {
        // Mallocing the arrays atoms and atom_ptrs to have enough memory to hold atom_max atoms
        // and pointers (respectively)
        newMolecule->atoms = malloc (sizeof (atom) * atom_max);
        newMolecule->atom_ptrs = malloc (sizeof (atom*) * atom_max);

        if (newMolecule->atoms == NULL || newMolecule->atom_ptrs == NULL)
        {
            fprintf (stderr, "ERROR: malloc failed. Returning NULL.\n");
            return NULL;
        }
    }

    if (bond_max <= 0)
    {
        newMolecule->bonds = NULL;
        newMolecule->bond_ptrs = NULL;
    }
    else
    {
        // Mallocing the arrays bonds and bond_ptrs to have enough memory to hold bond_max bonds
        // and pointers (respectively)
        newMolecule->bonds = malloc (sizeof (bond) * bond_max);
        newMolecule->bond_ptrs = malloc (sizeof (bond*) * bond_max);

        if (newMolecule->bonds == NULL || newMolecule->bond_ptrs == NULL)
        {
            fprintf (stderr, "ERROR: malloc failed. Returning NULL.\n");
            return NULL;
        }
    }

    return newMolecule;
}

/*
 * Returns the address of a malloced area of memory, large enough to hold a molecule
 *
 * @param *src The molecule being copied to the molecule with in the address returned by
 * the function
 */
molecule *molcopy (molecule *src)
{
    // Reusing molmalloc as specified in assignment description
    molecule *newMolecule = molmalloc (src->atom_max, src->bond_max);

    if (newMolecule == NULL)
    {
        fprintf (stderr, "ERROR: molmalloc failed. Returning NULL.\n");
        return NULL;
    }

    // Appending all the atoms from src over to newMolecule
    for (int i = 0; i < src->atom_no; i++)
    {
        molappend_atom (newMolecule, &src->atoms[i]);

        if (newMolecule == NULL)
        {
            fprintf (stderr, "ERROR: molecule is NULL after appending atom. Returning NULL.\n");
            return NULL;
        }
    }

    // Appending all the bonds from src over to newMolecule
    for (int i = 0; i < src->bond_no; i++)
    {
        molappend_bond (newMolecule, &src->bonds[i]);
        
        // Getting the bonds in newMolecule to point to the new molecule's atoms
        newMolecule->bonds[i].atoms = newMolecule->atoms;

        if (newMolecule == NULL)
        {
            fprintf (stderr, "ERROR: molecule is NULL after appending bond. Returning NULL.\n");
            return NULL;
        }
    }

    return newMolecule;
}

/*
 * Frees the memory associated with the molecule pointed to by ptr
 */
void molfree (molecule *ptr)
{
    free (ptr->atoms);
    ptr->atoms = NULL;
    
    free (ptr->bonds);
    ptr->bonds = NULL;
    
    free (ptr->atom_ptrs);
    ptr->atom_ptrs = NULL;

    free (ptr->bond_ptrs);
    ptr->bond_ptrs = NULL;

    free (ptr);
    ptr = NULL;
}

/*
 * Copies data pointed to by atom_to_copy to the first "empty" atom in atoms in the molecule pointed to by molecule.
 * also sets the first "empty" pointer in atom_ptrs to the same atom in the atoms array, incrementing the value of atom_no.
 */
void molappend_atom (molecule *molecule, atom *atom_to_copy)
{
    // Allocating the molecule to hold one atom if atom_max is a non-positive number
    if (molecule->atom_max <= 0)
    {
        molecule->atom_max = 1;
        if (molecule->atoms == NULL && molecule->atom_ptrs == NULL)
        {
            molecule->atoms = realloc (NULL, sizeof (atom));
            molecule->atom_ptrs = realloc (NULL, sizeof (atom*));

            // Exit program if realloc fails
            if (molecule->atoms == NULL || molecule->atom_ptrs == NULL)
            {
                fprintf (stderr, "ERROR: realloc failed. Exiting program.\n");
                exit (0);
            }
        }
        else
        {
            molecule->atoms = realloc (molecule->atoms, sizeof (atom));
            molecule->atom_ptrs = realloc (molecule->atom_ptrs, sizeof (atom*));

            // Exit program if realloc fails
            if (molecule->atoms == NULL || molecule->atom_ptrs == NULL)
            {
                fprintf (stderr, "ERROR: realloc failed. Exiting program.\n");
                exit (0);
            }
        }

    }
    // Doubling atom_max if it is equal to atom_no
    else if (molecule->atom_max == molecule->atom_no)
    {
        molecule->atom_max = molecule->atom_max * 2;
        molecule->atoms = realloc (molecule->atoms, sizeof (atom) * molecule->atom_max);
        molecule->atom_ptrs = realloc (molecule->atom_ptrs, sizeof (atom*) * molecule->atom_max);

        // Exit program if realloc fails
        if (molecule->atoms == NULL || molecule->atom_ptrs == NULL)
        {
            fprintf (stderr, "ERROR: realloc failed. Exiting program.\n");
            exit (0);
        }

        // If a realloc occurs, the atom_ptrs array is fully reassigned to point to the new memory locations
        // of the atoms in the atoms array
        for (int i = 0; i < molecule->atom_no; i++)
        {
            molecule->atom_ptrs[i] = &molecule->atoms[i];
        }
    }

    // Appending the new atom and atom pointer   
    molecule->atoms[molecule->atom_no] = *atom_to_copy;
    molecule->atom_ptrs[molecule->atom_no] = &molecule->atoms[molecule->atom_no];

    // Incrementing the atom_no value in molecule
    molecule->atom_no++;    
}

/*
 * Copies data pointed to by bond_to_copy to the first "empty" bond in bonds in the molecule pointed to by molecule.
 * Also sets the first "empty" pointer in bond_ptrs to the same bond in the bonds array, incrementing the value of bonds_no.
 */
void molappend_bond (molecule *molecule, bond *bond_to_copy)
{
    // Allocating the molecule to hold one bond if bond_max is a non-positive number
    if (molecule->bond_max <= 0)
    {
        molecule->bond_max = 1;

        if (molecule->bonds == NULL && molecule->bond_ptrs == NULL)
        {
            molecule->bonds = realloc (NULL, sizeof (bond));
            molecule->bond_ptrs = realloc (NULL, sizeof (bond*));  

            // Exit program if realloc fails
            if (molecule->bonds == NULL || molecule->bond_ptrs == NULL)
            {
                fprintf (stderr, "ERROR: realloc failed. Exiting program.\n");
                exit (0);
            } 
        }
        else
        {
            molecule->bonds = realloc (molecule->bonds, sizeof (bond) * molecule->bond_max);
            molecule->bond_ptrs = realloc (molecule->bond_ptrs, sizeof (bond*) * molecule->bond_max);

            // Exit program if realloc fails
            if (molecule->bonds == NULL || molecule->bond_ptrs == NULL)
            {
                fprintf (stderr, "ERROR: realloc failed. Exiting program.\n");
                exit (0);
            }
        }
        
    }
    // Doubling bond_max if it is equal to bond_no
    else if (molecule->bond_max == molecule->bond_no){
        molecule->bond_max = molecule->bond_max * 2;
        molecule->bonds = realloc (molecule->bonds, sizeof (bond) * molecule->bond_max);
        molecule->bond_ptrs = realloc (molecule->bond_ptrs, sizeof (bond*) * molecule->bond_max);

        // Exit program if realloc fails
        if (molecule->bonds == NULL || molecule->bond_ptrs == NULL)
        {
            fprintf (stderr, "ERROR: realloc failed. Exiting program.\n");
            exit (0); 
        }

        // If a realloc occurs, the bond_ptrs array is fully reassigned to point to the new memory locations
        // of the bonds in the bonds array
        for (int i = 0; i < molecule->bond_no; i++)
        {
            molecule->bond_ptrs[i] = &molecule->bonds[i];
        }
    }

    // Appending the new bond and bond pointer
    molecule->bonds[molecule->bond_no] = *bond_to_copy;
    molecule->bond_ptrs[molecule->bond_no] = &molecule->bonds[molecule->bond_no];
    
    // Incrementing the bond_no value in molecule
    molecule->bond_no++;
}

/*
 * Helper function to molsort. Compares the z values in both the atoms passed in
 * and returns certain values based on which atom has the larger z value
 */
int atom_compare (const void *a, const void *b)
{
    atom *atom_ptr_a, *atom_ptr_b;

    atom_ptr_a = *(atom**) a;
    atom_ptr_b = *(atom**) b;

    if (atom_ptr_a->z > atom_ptr_b->z)
    {
        return 1;
    }
    else if (atom_ptr_a->z < atom_ptr_b->z)
    {
        return -1;
    }
    else
    {
        return 0;
    }
}

/*
 * Helper function to molsort. Compares the z values in both the bonds passed in
 * and returns certain values based on which bond has the larger z value
 */
int bond_comp (const void *a, const void *b)
{
    bond *bond_ptr_a, *bond_ptr_b;
    double bond_a, bond_b;

    bond_ptr_a = *(bond**) a;
    bond_ptr_b = *(bond**) b;

    // Calculation of the average of each bond's z values
    bond_a = bond_ptr_a->z;
    bond_b = bond_ptr_b->z;

    if (bond_a > bond_b)
    {
        return 1;
    }
    else if (bond_a < bond_b)
    {
        return -1;
    }
    else
    {
        return 0;
    }
}

/*
 * Sorts the atom_ptrs array in order of increasing z value.
 * Also sorts the bond_ptrs array in order of increasing average of the respective bond's two z values.
 */
void molsort (molecule *molecule)
{
    qsort (molecule->atom_ptrs, molecule->atom_no, sizeof (atom*), atom_compare);
    qsort (molecule->bond_ptrs, molecule->bond_no, sizeof (bond*), bond_comp);
}

/*
 * Sets the values in xform_matrix, corresponding to a rotation of deg
 * degrees around the x-axis
 */
void xrotation (xform_matrix xform_matrix, unsigned short deg)
{
    // Conversion of deg from degrees to radians
    double rad;
    rad = deg * PI / 180;

    xform_matrix[0][0] = 1;
    xform_matrix[0][1] = 0;
    xform_matrix[0][2] = 0;

    xform_matrix[1][0] = 0;
    xform_matrix[1][1] = cos (rad);
    xform_matrix[1][2] = -(sin (rad));

    xform_matrix[2][0] = 0;
    xform_matrix[2][1] = sin (rad);
    xform_matrix[2][2] = cos (rad);
}

/*
 * Sets the values in xform_matrix, corresponding to a rotation of deg
 * degrees around the y-axis
 */
void yrotation (xform_matrix xform_matrix, unsigned short deg)
{
    // Conversion of deg from degrees to radians
    double rad;
    rad = deg * PI / 180;

    xform_matrix[0][0] = cos (rad);
    xform_matrix[0][1] = 0;
    xform_matrix[0][2] = sin (rad);

    xform_matrix[1][0] = 0;
    xform_matrix[1][1] = 1;
    xform_matrix[1][2] = 0;

    xform_matrix[2][0] = -(sin (rad));
    xform_matrix[2][1] = 0;
    xform_matrix[2][2] = cos (rad);
}

/*
 * Sets the values in xform_matrix, corresponding to a rotation of deg
 * degrees around the x-axis
 */
void zrotation (xform_matrix xform_matrix, unsigned short deg)
{
    // Conversion of deg from degrees to radians
    double rad;
    rad = deg * PI / 180;

    xform_matrix[0][0] = cos (rad);
    xform_matrix[0][1] = -(sin (rad));
    xform_matrix[0][2] = 0;

    xform_matrix[1][0] = sin (rad);
    xform_matrix[1][1] = cos (rad);
    xform_matrix[1][2] = 0;

    xform_matrix[2][0] = 0;
    xform_matrix[2][1] = 0;
    xform_matrix[2][2] = 1;
}

/*
 * Applies the transformation matrix to all the atoms of molecule by performing a vector
 * matrix multiplication on the x, y and z coordinates
 */
void mol_xform (molecule *molecule, xform_matrix matrix)
{
    // These values exist for storing the original values for each value as they get changed within the loops
    double original_x, original_y, original_z;

    for (int i = 0; i < molecule->atom_no; i++)
    {
        original_x = molecule->atoms[i].x;
        original_y = molecule->atoms[i].y;
        original_z = molecule->atoms[i].z;

        molecule->atoms[i].x = (matrix[0][0] * original_x) + (matrix[0][1] * original_y) + (matrix[0][2] *original_z);
        molecule->atoms[i].y = (matrix[1][0] * original_x) + (matrix[1][1] * original_y) + (matrix[1][2] *original_z);
        molecule->atoms[i].z = (matrix[2][0] * original_x) + (matrix[2][1] * original_y) + (matrix[2][2] *original_z);
    } 

    for (int i = 0; i < molecule->bond_no; i++){
        compute_coords (molecule->bond_ptrs[i]);
    }
}
