def LatticeSolutions(L, a, U0, cutoff): # L: Total length | a: Lattice parameter | U0: Perturbation strenght | Spread: Perturbation width | cutoff: Energy cut-off
    
    print('Diagonalizing the perturbed Hamiltonian...')
    
    import numpy
    import pylab
    from math import sqrt, sin, cos, exp, pi
    from numBraKet import numBraKet as BraKet
    
    s = 10*L  # Sampling grain for integrals
    
    ## Imperturbed eigenproblem ##
    A = sqrt(2/L)
    def psi0_n(x): return A*sin(pi/L * n * x)
    def psi0_m(x): return A*sin(pi/L * m * x)
    def eigenE0(n): return (pi**2 * n**2)/(2 * L**2)    

    n = 1

    while eigenE0(n) <= cutoff:
        
        n += 1
    
    basisDIM = n # We've established the basis dimension from the energy cut-off
    print('Basis dimension: ', basisDIM)
    
    ## Periodic potential definition ##
    
    def U(x): 
    
        return U0*cos(2*pi/a * x)


    """x = numpy.linspace(0,L,s)
    f = numpy.vectorize(U, otypes=[numpy.float])
    y = f(x)
    pylab.fill_between(x,y, facecolor='gray', edgecolor='black', alpha=0.3)"""
    
    ## Now we proceed constructing the hamiltionian matrix H_{nm} ##
    
    H = [[0 for i in range(basisDIM)] for j in range(basisDIM)]
    
    def Ket_m(x): return U(x)*psi0_m(x)
    
    Bra_n = numpy.vectorize(psi0_n, otypes=[numpy.float])
    Ket_m = numpy.vectorize(Ket_m, otypes=[numpy.float])
    
    for i in range(basisDIM):
    
        for j in range(basisDIM):
        
            n, m = i+1, j+1 # Dumb python indexing...

            ## Kinetic (diagonal) part ##
            
            if i==j: H[i][i] += eigenE0(n)
            
            ## Periodic potential part ##
            
            x = numpy.linspace(0,L,s)
            H[i][j] += BraKet(Bra_n(x), Ket_m(x), 0, L, x)    
            #if (m+n)**2==1: H[i][j] += U0/(4*pi) * (L*(m+n)*sin(pi*(m+n)))/(pi*((m+n)**2-1))
            #if (m-n)**2==1: H[i][j] += U0/(4*pi) * (L*(n-m)*sin(pi*(m-n)))/(pi*((m-n)**2-1))
            
    ## Perturbed solutions ##
    eigenvalues, eigenvectors = numpy.linalg.eigh(H)
    
    return eigenvalues, eigenvectors
 
