"""
Author: Esteban Jiménez Rodríguez
Institution: ITESO - Universidad Jesuita de Guadalajara
Date: 01/11/2017
Description: This script contains functions that make possible to use the pyomo
library directly.
"""

import numpy as np
    
def dat_write_lin(dat_name, f, A, b, Aeq, beq):
    # Dimensions of matrices
    m1 = b.shape[0]
    n = f.shape[0]
    m2 = beq.shape[0]

    # Creation and opening of the data file
    dat_file = open('default.dat', 'w')
    
    # Write the matrices in the data file
    dat_file.write('# This file is automatically generated by the linprog function\n');
    dat_file.write('param m1 := %i ;\nparam m2 := %i ;\nparam n := %i ;\nparam A := \n'%(m1, m2, n));
    for i in range(m1):
        for k in range(n):
            dat_file.write('%i %i %e\n'%(i+1, k+1, A[i, k]));
    dat_file.write(';\nparam b := \n');
    for i in range(m1):
        dat_file.write('%i %e\n'%(i+1, b[i]));
    dat_file.write(';\nparam Aeq := \n');
    for j in range(m2):
        for k in range(n):
            dat_file.write('%i %i %e\n'%(j+1, k+1, Aeq[j, k]));
    dat_file.write(';\nparam beq := \n');
    for j in range(m2):
        dat_file.write('%i %e\n'%(j+1, beq[j]));
    dat_file.write(';\nparam f := \n');
    for k in range(n):
        dat_file.write('%i %e\n'%(k+1, f[k]));
    dat_file.write(';');
    
    # Closing the data file
    dat_file.close()
    
def linprog(f, A, b, Aeq=None, beq=None):
    # Dimensions of matrices
    m1 = b.shape[0]
    n = f.shape[0]
    
    # b must be a vector
    if b.ndim != 1:
        raise ValueError('b must be a one dimensional array')
    # A must be a matrix
    if A.ndim != 2:
        raise ValueError('A must be a two dimensional array')
    
    # Dimension check for inequality constraint
    if A.shape != (m1, n):
        raise ValueError('The shape of A must be equal to (b.shape[0], f.shape[0])')
    
    # If no equality restriction
    if np.any(Aeq == None) & np.any(beq == None):
        Aeq = np.zeros((1,n))
        beq = np.zeros((1,))
        m2 = 1
    elif (np.any(Aeq != None) & np.any(beq == None)) | (np.any(Aeq == None) & np.any(beq != None)):
        raise ValueError('Please provide Aeq and beq if there is an equality constraint. If there is not, please provide none of them.')
    else:
        # Dimension of matrices
        m2 = beq.shape[0]
        
        # beq must be a vector
        if beq.ndim != 1:
            raise ValueError('b must be a one dimensional array')
        # Aeq must be a matrix
        if Aeq.ndim != 2:
            raise ValueError('A must be a two dimensional array')
        # Dimension check for equality constraint
        if Aeq.shape != (m2, n):
            raise ValueError('The shape of Aeq must be equal to (beq.shape[0], f.shape[0])')
        
    # Data file creation
    dat_write_lin('default', f, A, b, Aeq, beq)
    
    # Solution
    import linprog_model
    # Create the model instance
    instance = model.create_instance('default.dat')
    # Setup the optimizer: linear in this case
    opt = SolverFactory('glpk')    
    # Optimize
    results = opt.solve(instance)
    # Write the output
    results.write()
    
    # Optimal solution
    x = np.array([instance.x[k].value for k in instance.K])
    return x, value(instance.OBJ)
    

# Example
A = np.array([[-3,-4]])
f = np.array([2,3])
b = np.array([-1])
x, f = linprog(f, A, b)