import scipy

x, y=1,1
while(1):
    xn=x*scipy.sin(1.57)-(y-x**2)*scipy.cos(1.57)
    yn=x*scipy.sin(1.57)+(y-x**2)*scipy.cos(1.57)
    print x, y
    x=xn
    y=yn