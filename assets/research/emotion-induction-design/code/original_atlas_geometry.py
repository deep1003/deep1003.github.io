"""Fixed equal-area geometry helpers; no experiment execution."""
import numpy as np
def clip(poly,n,b):
    if len(poly)==0:return np.empty((0,2))
    result=[]
    for a,z in zip(poly,np.roll(poly,-1,axis=0)):
        da, dz=np.dot(a,n)-b,np.dot(z,n)-b
        ina,inz=da<=1e-12,dz<=1e-12
        if ina:result.append(a)
        if ina!=inz:result.append(a+(z-a)*da/(da-dz))
    return np.array(result).reshape(-1,2)

def area(poly):
    if len(poly)<3:return 0.
    return abs(np.sum(poly[:,0]*np.roll(poly[:,1],-1)-poly[:,1]*np.roll(poly[:,0],-1)))/2

def center(poly):
    cross=poly[:,0]*np.roll(poly[:,1],-1)-np.roll(poly[:,0],-1)*poly[:,1]
    return np.sum((poly+np.roll(poly,-1,axis=0))*cross[:,None],axis=0)/(3*cross.sum())

def partition(poly,n):
    """Equal-area recursive cuts. Geometry never uses measured activation values."""
    if n==1:return [poly]
    axis=int(np.argmax(np.ptp(poly,axis=0)));normal=np.eye(2)[axis]
    a,z=poly[:,axis].min(),poly[:,axis].max();left=n//2;target=area(poly)*left/n
    for _ in range(40):
        mid=(a+z)/2
        if area(clip(poly,normal,mid))<target:a=mid
        else:z=mid
    mid=(a+z)/2
    return partition(clip(poly,normal,mid),left)+partition(clip(poly,-normal,-mid),n-left)

