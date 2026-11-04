import numpy as np
from scipy.special import gammaln
LN2=np.log(2)
def closed(b):  # normalized avg of (1+cos x)^b
    return np.exp(b*LN2+gammaln(b+.5)-0.5*np.log(np.pi)-gammaln(b+1))
def Phi(p,Delta,avgfun=closed):
    return 1+p*Delta+(1+p)*np.log2(avgfun(1/(1+p)))
def trig(coef,x):
    # coef: (deg,2) array a_k cos kx + b_k sin kx
    s=np.zeros_like(x)
    for k,(a,b) in enumerate(coef,1): s+=a*np.cos(k*x)+b*np.sin(k*x)
    return s
def quantities(lf,lg,kappa,N=None):
    """lf, lg: natural log of (unnormalized) densities on grid x_j=2pi j/N. Returns u,v,Q,Qstar arrays (direct definitions)."""
    N=len(lf)
    lf=lf-np.log(np.mean(np.exp(lf-lf.max())))-lf.max()   # normalize so mean f=1
    lg=lg-np.log(np.mean(np.exp(lg-lg.max())))-lg.max()
    lfs=kappa*lf; lfs=lfs-np.log(np.mean(np.exp(lfs-lfs.max())))-lfs.max()
    lgs=kappa*lg; lgs=lgs-np.log(np.mean(np.exp(lgs-lgs.max())))-lgs.max()
    idx=(np.arange(N)[:,None]+np.arange(N)[None,:])%N   # [x,w] -> x+w
    LFw=lf[idx]; LT=LFw+lg[None,:]          # log f(x+w)g(w)
    m=LT.max(1,keepdims=True); W=np.exp(LT-m); Qn=W.mean(1,keepdims=True)
    lQ=(np.log(Qn)+m)[:,0]
    K=W/Qn                                   # K_x(w), avg over w = 1
    lK=LT-lQ[:,None]
    D=np.mean(K*lK,1)/LN2
    A=np.mean(K*lfs[idx],1)/LN2
    E=np.mean(K*lgs[None,:],1)/LN2
    u=A+E-D; v=2*D-A-E
    LTs=lfs[idx]+lgs[None,:]; ms=LTs.max(1,keepdims=True)
    lQs=(np.log(np.mean(np.exp(LTs-ms),1,keepdims=True))+ms)[:,0]
    return u,v,lQ/LN2,lQs/LN2
def log2M1(u,Delta,p,x):
    e=p*(Delta-u)*LN2+np.log(2+2*np.cos(x)+1e-300)
    mx=e.max(); return (mx+np.log(np.mean(np.exp(e-mx))))/LN2
