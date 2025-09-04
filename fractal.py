# 25.07.2011 improved load_transmation_function - when file is not found return identity
# 31.07.2011 added stop functionality
# 15.08.2011 added alpha to newton iteration
# todo
# parent in class fractal once
__author__="martin"
__date__ ="$18.12.2009 19:05:18$"

import scipy
import numpy
import scipy.ndimage
import pylab
from PyQt5 import QtGui, QtCore
import sys
#import parser



allowedCharsMath=["+","-","*","/", "%", " ",".","1","2","3","4","5","6","7","8","9","0","scipy","(",")","sign","sin","cos","tan", "log", "exp", "abs", "int", "psi_", "phi", "pi", "omega", "arc", "x","y", "z","r"]

class fractal:
    xmax=10
    ymax=10
    def __init__(self, parent=None):
        self.run=1
        self.parent=parent
        self.fmat=numpy.zeros([3,3])
        self.fmat[0:3:2, 0:3:2]=0.5
        self.fmat[1,:]=1.0
        self.fmat[:,1]=1.0
        self.fmat[1,1]*=4
        ssf=sum(sum(self.fmat))
        self.fmat*=1.0/ssf
    
    def get_filter_mat(self):
        return self.fmat
    
    def set_filter_mat(self, mat):
        if type(mat)==type(numpy.zeros(1)):
            if mat.shape==(3,3):
                self.fmat=mat.copy()
    
    def stop(self):
        self.run=0
        
    def filter(self, mat, f):
        xsize, ysize= mat.shape
        xrange=range(1, xsize-1)
        yrange=range(1, ysize-1)
        max_n=xsize*ysize
        mat2=numpy.zeros([xsize, ysize])
        mat3=numpy.zeros([3, 3])
        n=0
        if self.parent != None:
            self.parent.generate_progress_dialog("filtering...", "cancel", max_n)
        for x in xrange:
            for y in yrange:
                n+=1
                if self.parent != None:
                    self.parent.show_progress(n)
                mat3=mat[x-1:x+2, y-1:y+2]
                mat3=mat3*f
                mat2[x ,y]=sum(sum(mat3))
        if self.parent != None:
            self.parent.close_progress_dialog()
        return mat2
    
    def create_matrix_from_point_list(self, point_list, xwidth, ywidth):
        mat=numpy.zeros([ywidth, xwidth])
        p_array=numpy.array(point_list)
        #print p_array[:, 0]
        x_min=p_array[:,0].min()
        x_max=p_array[:,0].max()
        y_min=p_array[:,1].min()
        y_max=p_array[:,1].max()
    
        dx=float(abs(x_max-x_min))
        if dx==0.0:
            dx=1.0
        dy=float(abs(y_max-y_min))
        if dy==0.0:
            dy=1.0
        print(dx, x_min, x_max)
        print (dy, y_min, y_max)
        p_range=range(0, len(p_array))
        #if self.parent != None:
        #    self.parent.generate_progress_dialog("working...", "cancel", len(p_array))
        #progress=QtGui.QProgressDialog("Working...", "cancel", 0, len(p_array) )
        for n in p_range:
            #progress.setValue(n)
            #if self.parent != None:
            #    self.parent.show_progress(n)
            xh=float((p_array[n,0]-x_min)/dx*xwidth)
            yh=float((p_array[n,1]-y_min)/dy*ywidth)
            if not(numpy.isnan(xh) or numpy.isnan(yh)):
                x=int(xh)
                y=ywidth-int(yh)
                #print x, y
                if 0<=x<xwidth and 0<=y<ywidth:
                    mat[y,x]+=1

        #if self.parent != None:
        #    self.parent.close_progress_dialog()
        return mat
    
    
        
    def generate_ifs(self, number_of_functions):
        fs=list()
    
        for n in range(0, number_of_functions):
            p=scipy.random.randint(0,100)/100.0
            a=scipy.random.randint(-100,100)/100.0
            b=scipy.random.randint(-100,100)/100.0
            c=scipy.random.randint(-100,100)/100.0
            d=scipy.random.randint(-100,100)/100.0
            e=scipy.random.randint(-100,100)/100.0
            f=scipy.random.randint(-100,100)/100.0
            st="x*"+str(a)+"+y*"+str(b)+"+("+str(c)+"), x*"+str(d)+"+y*"+str(e)+"+("+str(f)+");"+str(p)
            print (st)
            fs.append(st)
        return fs
    
    def load_transformation_functions(self, transformation_functions_filename):
        f=list()
        try:
            file=open(transformation_functions_filename)
        except:
            print( "no transformation or file not found!")
            f=list(["x, y"])
            return f
        for line in file:
            f.append(line.strip())
        file.close()
        return f
    
    def save_function_system(self,fs, filename):
        try:
            f=open(filename, "w")
            for line in fs:
                f.write(line+"\n")
            f.close()
        except:
            print ("error file write")
    
    def load_function_system(self,function_system_filename):
        f=list([])
        try:
            file=open(function_system_filename)
        except:
            print ("file not found!")
            return f
        for line in file:
            data=line.strip()
            f.append(data)
        file.close()
        return f
    
    def make_ifs_pic(self, xwidth=800, ywidth=600, max_iterations=10**6, function_system="", transform_function="", gamma=1.2):
    
        def iterate( x, y, f):
    
    
            
            #print x, y
            #print j
            try:
                (nx, ny)=eval(f)
            except:
                (nx, ny)=(x, y)
            #print x, y
            return (nx, ny)
    
        def get_rand_func(p):
            j=numpy.random.uniform()
            n=0
            nr=0
            ps=0.0
            for i in p:
                ps+=float(i)
            p_acc=0.0
            #print j
            while p_acc < j*ps:
                p_acc+=float(p[n])
                if n < len(p)-1:
                    n+=1
                else:
                    n=0
            return n
        
        def get_probabilities(f):
            p=list()
            for line in f:
                data=line.split(";")
                if len(data) >= 2:
                    p.append(data[1])
            return p
        
        def get_func_list(f):
            fsys=list()    
            for line in f:
                data=line.split(";")
                if len(data) >= 2:
                    fsys.append(data[0])
            return fsys      
          
        def expand_functions(fsys):
            f=list();
            for line in fsys:
                data=line.split(";")
                for n in range(0, int(100*eval(data[1]))):
                    f.append(data[0])
            return f
    
        def transform(x, y, function_list):
            if y!= 0:
                phi=numpy.arctan(x/float(y))
            else:
                phi=numpy.sign(x)*numpy.pi/2
            if x!= 0:
                omega=numpy.arctan(y/float(x))
            else:
                omega=numpy.sign(y)*numpy.pi/2
            #print x, y
            try:
                r=(x**2+y**2)**0.5
            except:
                r=1
            psi_1=numpy.random.random()
            psi_2=numpy.random.random()
            #print w
            x_t=0.0
            y_t=0.0
            x_f=0
            y_f=0
            #print function_list
            for f in function_list:
                try:
                    x_f, y_f=eval(f)
                except:
                    x_f, y_f= x, y
                if (numpy.isfinite(x_f)):
                    x_t+=x_f
                if (numpy.isfinite(y_f)):
                    y_t+=y_f
            return x_t, y_t
    
    
    
    
        x=0.1
        y=0.1
        #max_iterations=10**6
        i=0
        old_pc=0
        self.run=1
        p_list=list([])
        prob_f=get_probabilities(function_system)
        print( prob_f)
        function_system=get_func_list(function_system)
        if self.parent != None:
            self.parent.generate_progress_dialog("working...", "cancel", max_iterations)
        # progress=QtGui.QProgressDialog("Working...", "cancel", 0, max_iterations )
        print (function_system)
        mat=numpy.zeros((ywidth,xwidth))
        ok=1
        for n in function_system:
            fx,fy=n.split(",")
            if not(self.check_math_function(fx, allowedCharsMath)):
                ok=0
            if not(self.check_math_function(fy, allowedCharsMath)):
                ok=0
        for n in transform_function:
            fx,fy=n.split(",")
            if not(self.check_math_function(fx, allowedCharsMath)):
                ok=0
            if not(self.check_math_function(fy, allowedCharsMath)):
                ok=0         
        if ok:        
            #scipy.random.seed(0)
            parsedFunctionSys=list()
            parsedTransformFunc=list()
            for n in function_system:
                parsedFunctionSys.append(n)#parser.compilest(parser.expr(n)))
            for n in transform_function:
                parsedTransformFunc.append(n)#parser.compilest(parser.expr(n)))
            while i <= max_iterations and self.run:
                    i+=1
                    if self.parent != None:
                        self.parent.show_progress(i)
                    #progress.setValue(i)
                    c=get_rand_func(prob_f)
                    #print c, function_system
                    x, y=iterate(x, y, parsedFunctionSys[c])
    
                    x, y=transform(x, y, parsedTransformFunc)
                    if x==numpy.inf or y==numpy.inf or numpy.isnan(x) or numpy.isnan(y):
                        x=numpy.random.rand()
                        y=numpy.random.rand()
                    xt, yt=x, y
                    p_list.append([xt, yt, c])
          
            if self.parent != None:
                self.parent.close_progress_dialog()
            mat=self.create_matrix_from_point_list(p_list, xwidth, ywidth)
            #f=numpy.zeros([3,3])
            #f[0:2, 0:2]=1
            
            #f[1,1]=3
            
            #mat=filter(mat, f, parent)
            #mat=scipy.ndimage.convolve(mat, f) 
              
            
            mat=numpy.log2(mat+1)
            #print mat.min() 
            #mat=self.normalize_mat(mat) 
            #mat=scipy.sqrt(mat)
            #print mat.min() 
            #mat=mat**gamma 
            #print mat.min() 
    
            #f[1,0:3]=2
            #f[1,1]=4
            
            #mat=filter(mat, f, parent)
      
    
            
            mat=scipy.ndimage.convolve(mat, self.fmat)
            #mat=scipy.log10(mat+1)
            mat=mat**gamma     
            #print mat
    
            mat=self.normalize_mat(mat)
    
    
        #mat=mat/float(mat.max())
        return mat
    
    def check_math_function(self,f, tokenlist):
        f1=f.strip()
        ok=1
        for n in tokenlist:
            f1=f1.replace(n,"")

        if (len(f1)>0):
            print( f1)
            ok=0
        return ok
    
    def make_julia_pic(self, xwidth=800, ywidth=600, c=-1, max_iterations=10):
    
        def iterate(number_of_iterations, value, x0, y0, c=0):
            z=complex(x0, y0)
            n=0
    
            while (n < number_of_iterations) and (abs(z) <= value):
                z=z**2+c
                n+=1
            return n
        self.run=1
        mat=numpy.zeros([ywidth, xwidth])
        xrange=range(0, xwidth)
        yrange=range(0, ywidth)
        max_points=xwidth*ywidth
        i=0
        if self.parent != None:
            self.parent.generate_progress_dialog("working...", "cancel", max_points)
        for x in xrange:
            #print x
            if self.run==0:
                break            
            for y in yrange:
                i+=1
                if self.parent != None:
                    self.parent.show_progress(i)
                if self.run==0:
                    break
                mat[y, x]=iterate(max_iterations, 2, (x-xwidth/2)/float(xwidth)*4, (y-ywidth/2)/float(ywidth)*4, c)
    
        if self.parent != None:
            self.parent.close_progress_dialog()
        return mat
    
    def make_curlicue_pic(self, xwidth=800, ywidth=600, s=(1+5**0.5)/2.0, gamma=1.2, max_iterations=10**6):
        self.run=1
        mat=numpy.zeros([ywidth, xwidth])
        i=0
        omega=0
        phi=0
        x, y=0, 0
        old_pc=0
        e=numpy.e
        pi=numpy.pi
        p_list=list()
        max_value=0
        if self.parent != None:
            self.parent.generate_progress_dialog("working...", "cancel", max_iterations)
        while i <= max_iterations and self.run:
            i+=1
            if i*100/max_iterations > old_pc:
                old_pc=i*100/max_iterations
                if self.parent != None:
                    self.parent.show_progress(i)
    
            omega=(omega+2*pi*s)%(2*pi)
            phi=(phi+omega)%(2*pi)
            x, y=x+numpy.cos(phi), y+numpy.sin(phi)
            p_list.append([x, y,0])
    
        mat=self.create_matrix_from_point_list(p_list, xwidth, ywidth)
    
        mat=numpy.log(1+mat)/numpy.log(2)
        mat=mat**gamma
        if self.parent != None:
            self.parent.close_progress_dialog()
        return mat
    
    
    def load_newton_function(self,filename):
        f=""
        df=""
        try:
            file=open(filename)
        except:
            print ("file not found!")
            return f, df
        for line in file:
            data=line.strip().split(",")
        if len(data)>1:
            f=data[0]
            df=data[1]
        else:
            print ("error fileformat")
        file.close()
        return f, df
    
    
    def make_newton_pic(self,xwidth=800, ywidth=600, f="0", df="1", alpha=1.0, epsilon=0.01, max_iterations=100):
    
        def iterate(z0, f, df, alpha):
            z=z0
            z_old=0
            n=0
            self.run=1
            #epsilon=10**(-2)
            #print z, n
            while (abs(z-z_old) > epsilon ) and (n <max_iterations):
                n+=1
                z_old=z
                nz=eval(df)
                #print nz
                if nz != 0:
                    try:
                        z=z-alpha*eval(f)/(nz)
                    except:
                        z=z-1
                else:
                    z=0
    
            return z
    
        mat=numpy.zeros([ywidth, xwidth])
        xrange=range(0, xwidth)
        yrange=range(0, ywidth)
        imax=xwidth*ywidth
        i=0
        ok=1
        for n in f:
            if not (self.check_math_function(n, allowedCharsMath)):
                ok=0
        for n in df:
            if not (self.check_math_function(n, allowedCharsMath)):
                ok=0
        if ok:
            #f=parser.compilest(parser.expr(f.strip()))
            #df=parser.compilest(parser.expr(df.strip()))
            self.run=1
            if self.parent != None:
                self.parent.generate_progress_dialog("working...", "cancel", imax)
            for x in xrange:
                if self.run==0:
                    break            
                #print x
                for y in yrange:
                    if self.parent != None:
                        self.parent.show_progress(i)
                    if self.run==0:
                        break
                    z=complex((x-xwidth/2.0)*3/float(xwidth), (y-ywidth/2.0)*3/float(ywidth))
                    i_z=iterate(z, f, df, alpha)
                    mat[y, x]=(i_z.real+i_z.imag)
                    i+=1
        
        
            mat-=mat.min()
            #mat=scipy.log(mat)
            mat/=mat.max()
        if self.parent != None:
            self.parent.close_progress_dialog()
        return mat
    
    def normalize_mat(self, mat):
        r=mat.copy()
        mat_min=mat.min()
        if mat_min < 0:
            r-=mat_min
        mat_max=r.max()
        if mat_max==0.0:
            mat_max=1.0
        r/=float(mat_max)
        return r

if __name__ == "__main__":
    crange=pylab.linspace(-1, 1, 100)
    app=QtGui.QGuiApplication(sys.argv)

    f=fractal(None)
    fmat=numpy.zeros([3,3])
    fmat[1,1]=1
    #fmat[1,:]=scipy.arange(1,4)
    fmat/=sum(sum(fmat))
    print (fmat)
    f.set_filter_mat(fmat)
    fsys=f.load_function_system("farn2.ifs")
    tsys=f.load_transformation_functions("")
    mat=f.make_ifs_pic(400, 400, 10**5, fsys, tsys, 1.2)
    #mat=mat-mat.min()
    #mat=scipy.log(1+mat)/scipy.log(2)
    #mat=mat/float(mat.max())
    #print mat.mean()
    pylab.matshow(mat)
    pylab.gray()
    pylab.show()
    sys.exit(app.exec_())

    
