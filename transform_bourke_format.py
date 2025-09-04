import sys
import scipy

def read_data(fname):
    f=open(fname)
    data=list()
    for n in f:
        data.append(n)
    f.close()
    return data
data=read_data(sys.argv[1])
n_formula=len(data[1].split())
mat=scipy.zeros([6, n_formula])
x=0
#print data
for n in data:
    
    if not(("set" in n) or ("rob" in n)):
        factors=n.split()
        #print factors
        #print len(factors)
        for i in xrange(1, len(factors)):
            mat[x, i-1]=float(factors[i])
        x+=1
for x in xrange(0, n_formula-1):
    print str(mat[0,x])+"*x+("+str(mat[1,x])+")*y+("+str(mat[4,x])+"),"+str(mat[2,x])+"*x+("+str(mat[3,x])+")*y+("+str(mat[5,x])+");"+str(1.0/float(n_formula-1))
