""" ps3_tests.py

Contains tests of the implementations:
- krr
- cv

(c) Daniel Bartz, TU Berlin, 2013
"""
import numpy as np
import scipy.linalg as la
import pylab as pl

import ps3_implementation as imp
imp = reload(imp)

def squared_error_loss(y_true, y_pred):
    ''' returns the squared error loss
    '''
    loss = np.mean( (y_true - y_pred)**2 )
    return loss


def noisysincfunction(N, noise):
    ''' noisysincfunction - generate data from the "noisy sinc function"
        % usage
        %     [X, Y] = noisysincfunction(N, noise)
        %
        % input
        %     N: number of data points
        %     noise: standard variation of the noise
        %
        % output
        %     X: (1, N)-matrix uniformly sampled in -2pi, pi
        %     Y: (1, N)-matrix equal to sinc(X) + noise
        %
        % description
        %     Generates N points from the noisy sinc function
        %
        %        X ~ uniformly in [-2pi, pi]
        %        Y = sinc(X) + eps, eps ~ Normal(0, noise.^2)
        %
        % author
        %     Mikio Braun
    '''
    X = np.sort(2 * np.pi * np.random.rand(1, N) ) - np.pi
    Y = np.sinc(X) + noise * np.random.randn(1, N)
    return X, Y
    
def krr_test():
    '''
        tests the class krr
    '''
    Xtr, Ytr = noisysincfunction(100, 0.1)
    Xte = np.arange( -np.pi, np.pi, 0.01 )[np.newaxis,:] 

    pl.figure()
    kernels = ['gaussian','polynomial','linear']
    titles = ['gaussian','polynomial','linear']
    params = [0.5,4,0]
    regularizations = [ 0.01,0.01,0.01]
    for i in range(3):
        for j in range(2): 
            pl.subplot(2,3,1+i+3*j)    
            krr = imp.krr()
            if j==0:
                krr.fit(Xtr,Ytr,kernel=kernels[i],
                        kernelparameter=params[i],
                        regularization=regularizations[i])
            if j==1:
                krr.fit(Xtr,Ytr,kernel=kernels[i],
                        kernelparameter=params[i],
                        regularization=0)
                print krr.regularization
            krr.predict(Xte)
            pl.plot(Xtr.T,Ytr.T)
            pl.plot(Xte.T,krr.ypred.T)
            if j==0 and i == 0:
                pl.ylabel('fixed regularization')
            if j==1 and i == 0:
                pl.ylabel('reg. by efficent cv')
            pl.title( titles[i] )

         
def cv_test():
    '''
        tests the cross validation. needs working krr class!
    '''
    Xtr, Ytr = noisysincfunction(100, 0.1)
    Xte = np.arange( -np.pi, np.pi, 0.01 )[np.newaxis,:] 

    krr = imp.krr()    
    
    pl.figure()
    pl.subplot(1,2,1)
    params = [ 'kernel',['gaussian'], 'kernelparam', np.logspace(-2,2,10),
                  'regularization', np.logspace(-2,2,10) ]
    cvkrr = imp.cv(Xtr, Ytr, krr, params, loss_function=squared_error_loss, nrepetitions=2)
    cvkrr.predict(Xte)

    pl.plot(Xtr.T,Ytr.T)
    pl.plot(Xte.T,cvkrr.ypred.T)

    pl.subplot(1,2,2)
    params = [ 'kernel',['gaussian'], 'kernelparam', np.logspace(-2,2,10),
                  'regularization', [0]  ]
    cvkrr = imp.cv(Xtr, Ytr, krr, params, loss_function=squared_error_loss,nrepetitions=2)
    cvkrr.predict(Xte)
    
    pl.plot(Xtr.T,Ytr.T)
    pl.plot(Xte.T,cvkrr.ypred.T)
        
if __name__ == '__main__':
    krr_test();
    cv_test();
    pl.show();
