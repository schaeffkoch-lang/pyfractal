# To change this template, choose Tools | Templates
# and open the template in the editor.
# 25.07.2011 improved run ifs when ifs is generated
# 31.07.2011 added running variable - run lock
# 31.07.2011 fix random_run_ifs
# 31.07.2011 added stop functionality
# 31.07.2011 fixed continous run
# 31.07.2011 added version info
# 15.08.2011 added alpha for newton fractals
# 21.08.2011 added info button for julia fractals

__author__="martin"
__date__ ="$16.01.2010 13:52:34$"
from PyQt5 import QtWidgets, QtCore, QtGui
import numpy
import sys
import subprocess
import scipy
import os
import imageio



import fractal

version_info="version 2.0"
filter_rows=filter_col=3

class table_win(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super.__init__(self)
        vbox=QtWidgets.QVBoxLayout(self)
        self.filter_table=QtWidgets.QTableWidget(filter_rows, filter_col)
        self.filter_table.verticalHeader().hide()
        self.filter_table.verticalHeader().setOffset(0)
        self.filter_table.horizontalHeader().hide()
        self.filter_table.horizontalHeader().setOffset(0)
        vbox.addWidget(self.filter_table)
        self.running=1
        self.filter_table.resizeRowsToContents()
        self.filter_table.resizeColumnsToContents()
        #self.sudoku_table.resize(self.sudoku_table.sizeHint())
        #self.sudoku_table.resize(10*(self.sudoku_table.width()), 10*(self.sudoku_table.height()))
        self.filter_table.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.filter_table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        table_width=self.filter_table.columnWidth(0)*filter_col
        table_height=self.filter_table.rowHeight(0)*filter_rows
        self.filter_table.resize(table_width, table_height)
        self.filter_quit_button=QtWidgets.QPushButton("quit")
        vbox.addWidget(self.filter_quit_button)
        self.connect(self.filter_quit_button,  QtCore.SIGNAL('clicked()'), self.close)
        max_w=table_width+vbox.spacing()
        max_h=table_height+self.filter_quit_button.sizeHint().height()
        #print max_h, table_width, table_height
        #self.sudoku_table.resize(self.sudoku_table.size())      
        self.resize(max_w, max_h)
        
    def set_mat(self, mat): 
        for y in range(0, filter_rows):
            for x in range(0, filter_col):
                
                i= QtWidgets.QTableWidgetItem(QtCore.QString.number(mat[y, x] ) )
                self.filter_table.setItem(y, x, i )
        #self.filter_table.resizeRowsToContents()
        #self.filter_table.resizeColumnsToContents()  
        #print self.size()
        self.table_resize()
        
    def get_mat(self):
        m=scipy.zeros([filter_rows, filter_col])
        for y in range(0, filter_rows):
            for x in range(0, filter_col):
                #print self.filter_table.item(y,x).text()
                m[y,x]=float(self.filter_table.item(y,x).text())
        return m
        
    def resizeEvent(self, event):
        #self.resizeEvent(event)
        self.table_resize()        
        
    def table_resize(self):
        w=self.filter_table.width()
        h=self.filter_table.height()
        for x in range(0, filter_col):
            self.filter_table.setColumnWidth(x, w/filter_col)
        for y in range(0, filter_rows):
            self.filter_table.setRowHeight(y, h/filter_rows)
        self.filter_table.resize(w,h)
        

        
        

class matrix_win(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__()
        self.mat=QtGui.QImage(256, 256, 3)
        self.pic_label=QtWidgets.QLabel()
        self.setCentralWidget(self.pic_label)

        
    def load(self, filename):
        self.mat=QtGui.QImage(filename)
        self.pic_label.setPixmap(QtGui.QPixmap.fromImage(self.mat))
        self.pic_label.setScaledContents(True)

    """  def paintEvent(self, ev):
        painter=QtGui.QPainter(self)
        painter.drawImage(QtCore.QPoint(0,0), self.mat)
        self.resize(self.mat.width(), self.mat.height()  """

class gui_menue(QtWidgets.QTabWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.mat_win=matrix_win()
        self.ifs_continuous_run=0
        self.julia_continuous_run=0
        self.curlicue_continuous_run=0
        self.newton_continuous_run=0
        self.fs=""
        self.running=0        
        self.mat=numpy.zeros([200, 200])
        self.fractal_run=fractal.fractal(self)
        self.create_general_tab()
        self.create_ifs_tab()
        self.create_julia_tab()
        self.create_curlicue_tab()
        self.create_newton_tab()
        self.addTab(self.general_tab, "general")
        self.addTab(self.ifs_tab, "ifs")
        self.addTab(self.julia_tab, "julia")
        self.addTab(self.curlicue_tab, "curlicue")
        self.addTab(self.newton_tab, "newton")
        self.setMinimumHeight(400)
        self.setMinimumWidth(100)


    def create_general_tab(self):
        self.general_tab=QtWidgets.QWidget()
        vbox=QtWidgets.QVBoxLayout(self)
        version=QtWidgets.QLabel(version_info)
        vbox.addWidget(version)
        xlabel=QtWidgets.QLabel("x-resolution")
        vbox.addWidget(xlabel)
        self.x_resolution=QtWidgets.QLineEdit("400")
        vbox.addWidget(self.x_resolution)
        ylabel=QtWidgets.QLabel("y-resolution")
        vbox.addWidget(ylabel)
        self.y_resolution=QtWidgets.QLineEdit("400")
        vbox.addWidget(self.y_resolution)

        showbutton=QtWidgets.QPushButton("show matrix")
        vbox.addWidget(showbutton)
        showbutton.clicked.connect(self.show_matrix)
        savebutton=QtWidgets.QPushButton("save matrix")
        vbox.addWidget(savebutton)
        savebutton.clicked.connect(self.save_matrix)

        quitbutton=QtWidgets.QPushButton("quit")
        vbox.addWidget(quitbutton)
        quitbutton.clicked.connect(self.exit_pro )
        self.general_tab.setLayout(vbox)
    
    def exit_pro(self):
        self.stop()
        self.close()
        self.mat_win.close()
        

    def create_ifs_tab(self):
        self.ifs_tab=QtWidgets.QWidget()
        self.ifs_vbox=QtWidgets.QVBoxLayout(self)
        self.ifs_filename=""
        self.transformation_filename=""
        self.ifs_filedialog_button=QtWidgets.QPushButton("ifs file")
        self.ifs_vbox.addWidget(self.ifs_filedialog_button)
        self.ifs_filedialog_button.clicked.connect(self.get_ifs_filename)
        self.ifs_label=QtWidgets.QLabel(self.ifs_filename)
        self.ifs_vbox.addWidget(self.ifs_label)
        self.ifs_transformation_filedialog_button=QtWidgets.QPushButton("transformation function file")

        self.ifs_vbox.addWidget(self.ifs_transformation_filedialog_button)
        self.ifs_transformation_filedialog_button.clicked.connect(self.get_transformation_filename)
        self.ifs_transformation_label=QtWidgets.QLabel(self.transformation_filename)

        self.ifs_vbox.addWidget(self.ifs_transformation_label)
        self.ifs_filter_button=QtWidgets.QPushButton("filter")
        self.ifs_vbox.addWidget(self.ifs_filter_button)
        self.ifs_filter_button.clicked.connect(self.get_ifs_filter)
        self.ifs_generate_button=QtWidgets.QPushButton("generate ifs")
        self.ifs_vbox.addWidget(self.ifs_generate_button)
        self.ifs_generate_button.clicked.connect(self.generate_ifs)
        number_functions_label=QtWidgets.QLabel("number of functions:")
        self.ifs_vbox.addWidget(number_functions_label)
        self.ifs_number_of_functions=QtWidgets.QLineEdit("4")
        self.ifs_vbox.addWidget(self.ifs_number_of_functions)
        self.save_ifs_button=QtWidgets.QPushButton("save ifs")
        self.ifs_vbox.addWidget(self.save_ifs_button)
        self.save_ifs_button.clicked.connect(self.save_ifs)
        gamma_label=QtWidgets.QLabel("gamma-factor:")
        self.ifs_vbox.addWidget(gamma_label)
        self.ifs_gamma_factor=QtWidgets.QLineEdit("1.2")
        self.ifs_vbox.addWidget(self.ifs_gamma_factor)
        max_iterations_label=QtWidgets.QLabel("max. iterations")
        self.ifs_vbox.addWidget(max_iterations_label)
        self.max_ifs_iterations=QtWidgets.QLineEdit("100000")
        self.ifs_vbox.addWidget(self.max_ifs_iterations)
        rrun_label=QtWidgets.QLabel("randomize:")
        self.ifs_vbox.addWidget(rrun_label)
        self.cb_transformations=QtWidgets.QCheckBox("transformation")
        self.cb_transformations.setChecked(True)
        self.ifs_vbox.addWidget(self.cb_transformations)
        self.cb_ifs=QtWidgets.QCheckBox("ifs")
        self.cb_ifs.setChecked(QtCore.Qt.Checked)
        self.ifs_vbox.addWidget(self.cb_ifs)
        self.ifs_infobutton=QtWidgets.QPushButton("info")
        self.ifs_vbox.addWidget(self.ifs_infobutton)
        self.ifs_infobutton.clicked.connect(self.show_ifs_parameters)
        self.ifs_stopbutton=QtWidgets.QPushButton("stop")
        self.ifs_vbox.addWidget(self.ifs_stopbutton)
        self.ifs_stopbutton.clicked.connect(self.stop)
        self.ifs_runbutton=QtWidgets.QPushButton("run ifs")
        self.ifs_vbox.addWidget(self.ifs_runbutton)
        self.ifs_runbutton.clicked.connect(self.run_ifs)
        self.ifs_random_runbutton=QtWidgets.QPushButton("random run")
        self.ifs_vbox.addWidget(self.ifs_random_runbutton)
        self.ifs_random_runbutton.clicked.connect(self.random_run_ifs)
        self.ifs_ifs_continous_runbutton=QtWidgets.QPushButton("start continous run")
        self.ifs_vbox.addWidget(self.ifs_ifs_continous_runbutton)
        self.ifs_ifs_continous_runbutton.clicked.connect(self.continuous_run_ifs)
        self.ifs_tab.setLayout(self.ifs_vbox)

    def create_julia_tab(self):
        self.julia_tab=QtWidgets.QWidget()
        vbox=QtWidgets.QVBoxLayout(self)
        c_label_real=QtWidgets.QLabel("c real")
        vbox.addWidget(c_label_real)
        self.c_edit_real=QtWidgets.QLineEdit("1")
        vbox.addWidget(self.c_edit_real)
        c_label_imag=QtWidgets.QLabel("c imaginary")
        vbox.addWidget(c_label_imag)
        self.c_edit_imag=QtWidgets.QLineEdit("1")
        vbox.addWidget(self.c_edit_imag)
        max_iterations_label=QtWidgets.QLabel("max. iterations")
        vbox.addWidget(max_iterations_label)
        self.max_julia_iterations=QtWidgets.QLineEdit("100")
        vbox.addWidget(self.max_julia_iterations)
        self.julia_infobutton=QtWidgets.QPushButton("info")
        vbox.addWidget(self.julia_infobutton)
        self.julia_infobutton.clicked.connect(self.show_julia_parameters)
        self.julia_stopbutton=QtWidgets.QPushButton("stop")
        vbox.addWidget(self.julia_stopbutton)
        self.julia_stopbutton.clicked.connect(self.stop)
        runbutton=QtWidgets.QPushButton("run julia")
        vbox.addWidget(runbutton)
        random_run_button=QtWidgets.QPushButton("random run julia")
        vbox.addWidget(random_run_button)
        self.julia_continuos_runbutton=QtWidgets.QPushButton("start continous run")
        vbox.addWidget(self.julia_continuos_runbutton)
        self.julia_continuos_runbutton.clicked.connect(self.continuous_run_julia)
        random_run_button.clicked.connect(self.random_run_julia)
        runbutton.clicked.connect(self.run_julia)
        self.julia_tab.setLayout(vbox)

    def create_curlicue_tab(self):
        self.curlicue_tab=QtWidgets.QWidget()
        vbox=QtWidgets.QVBoxLayout(self)
        s_value_label=QtWidgets.QLabel("s-value")
        vbox.addWidget(s_value_label)
        self.s_value_edit=QtWidgets.QLineEdit("(1+2**0.5)/2.0")
        vbox.addWidget(self.s_value_edit)
        max_iter_label=QtWidgets.QLabel("max. iterations")
        vbox.addWidget(max_iter_label)
        self.curlicue_max_iter=QtWidgets.QLineEdit("10**6")
        vbox.addWidget(self.curlicue_max_iter)
        gamma_label=QtWidgets.QLabel("gamma")
        vbox.addWidget(gamma_label)
        self.curlicue_gamma=QtWidgets.QLineEdit("1.2")
        vbox.addWidget(self.curlicue_gamma)
        self.curlicue_infobutton=QtWidgets.QPushButton("info")
        vbox.addWidget(self.curlicue_infobutton)
        self.curlicue_infobutton.clicked.connect(self.show_curlicue_parameters)
        self.curlicue_stopbutton=QtWidgets.QPushButton("stop")
        vbox.addWidget(self.curlicue_stopbutton)
        self.curlicue_stopbutton.clicked.connect(self.stop)        
        runbutton=QtWidgets.QPushButton("run")
        vbox.addWidget(runbutton)
        random_run_button=QtWidgets.QPushButton("random run julia")
        vbox.addWidget(random_run_button)
        runbutton.clicked.connect(self.run_curlicue)
        random_run_button.clicked.connect(self.random_run_curlicue)
        self.curlicue_continuos_runbutton=QtWidgets.QPushButton("start continous run")
        vbox.addWidget(self.curlicue_continuos_runbutton)
        self.curlicue_continuos_runbutton.clicked.connect(self.continuous_run_curlicue)
        self.curlicue_tab.setLayout(vbox)


    def create_newton_tab(self):
        self.newton_tab=QtWidgets.QWidget()
        vbox=QtWidgets.QVBoxLayout(self)
        self.newton_filename=""
        self.newton_filedialog_button=QtWidgets.QPushButton("function file")
        vbox.addWidget(self.newton_filedialog_button)
        self.newton_filedialog_button.clicked.connect(self.get_newton_filename)
        self.newton_func_label=QtWidgets.QLabel(self.newton_filename)
        vbox.addWidget(self.newton_func_label)
        newton_max_iterations_label=QtWidgets.QLabel("max. iterations:")
        vbox.addWidget(newton_max_iterations_label)
        self.newton_max_iterations=QtWidgets.QLineEdit("100")
        vbox.addWidget(self.newton_max_iterations)
        newton_epsilon_label=QtWidgets.QLabel("epsilon:")
        vbox.addWidget(newton_epsilon_label)
        self.newton_epsilon=QtWidgets.QLineEdit("0.01")
        vbox.addWidget(self.newton_epsilon)
        newton_alpha_label=QtWidgets.QLabel("alpha:")
        vbox.addWidget(newton_alpha_label)
        self.newton_alpha=QtWidgets.QLineEdit("1.0")
        vbox.addWidget(self.newton_alpha)
        self.newton_infobutton=QtWidgets.QPushButton("info")
        vbox.addWidget(self.newton_infobutton)        
        self.newton_stopbutton=QtWidgets.QPushButton("stop")
        vbox.addWidget(self.newton_stopbutton)
        self.newton_stopbutton.clicked.connect(self.stop)        
        runbutton=QtWidgets.QPushButton("run")
        vbox.addWidget(runbutton)
        runbutton.clicked.connect(self.run_newton)
        random_runbutton=QtWidgets.QPushButton("random run")
        vbox.addWidget(random_runbutton)
        random_runbutton.clicked.connect(self.random_run_newton)
        continous_runbutton=QtWidgets.QPushButton("start continous run")
        vbox.addWidget(continous_runbutton)
        continous_runbutton.clicked.connect(self.continuous_run_newton)        
        self.newton_infobutton.clicked.connect(self.show_newton_parameters)
        self.newton_tab.setLayout(vbox)

    def show_matrix(self):
        if self.mat.max()!=0:
            m=self.mat*(255.0/self.mat.max())
            #m2=imageio.core.util.Array(m)
            imageio.imwrite("temp.png", m.astype(numpy.uint8))
            p=os.getcwd()
            f=p+"/temp.png"
            print(f)
            self.mat_win.load(f)
            self.mat_win.show()




        
        #subprocess.Popen(["cmd.exe", "/C","temp.png"])
        
    def save_matrix(self):
        filename=QtWidgets.QFileDialog.getSaveFileName(self, "save file", "", "*.png")
        filename=str(filename)
        if filename!="":
            #print filename
            scipy.misc.imsave(filename, self.mat)
            
    def stop(self):
        self.ifs_continuous_run=0
        self.julia_continuous_run=0
        self.curlicue_continuous_run=0
        self.newton_continuous_run=0
        self.fractal_run.stop()
        
    def show_ifs_parameters(self):
        tf=self.transformation_filename
        ifs_file=self.ifs_filename
        fs=""
        if ifs_file =="":
            for n in self.fs:
                fs+=n
        gamma=self.get_ifs_gamma()
        iterations=self.get_ifs_iterations()
        text="transformation: "+str(tf)+"\nifs: "+str(ifs_file)+"\nfunctions: \n"+str(fs)+"\ngamma: "+str(gamma)+"\niterations: "+str(iterations)
        self.info(text)
    
        
    def run_ifs(self):
        if self.running!=1:
            self.running=1
            xwidth, ywidth=self.get_resolution()
            if xwidth >0 and ywidth > 0:
                iterations=self.get_ifs_iterations()
                if iterations >0:
                    gamma_factor=self.get_ifs_gamma()
                    if self.ifs_filename!="":
                        #p=Process(target=fractal.make_ifs_pic, args=[xwidth, ywidth, iterations, self.ifs_filename, self.transformation_filename])
                        #p.start()
                        #p.join()
                        fs=self.fractal_run.load_function_system(self.ifs_filename)
                    else:
                        fs=self.fs
                    if fs!="":
                        tf=self.fractal_run.load_transformation_functions(self.transformation_filename)
                        self.mat=self.fractal_run.make_ifs_pic(xwidth, ywidth, iterations, fs, tf, gamma_factor)
                        self.show_matrix()
                        #ifs=ifs_thread()
                        #ifs.render(xwidth, ywidth, iterations, self.ifs_filename, self.transformation_filename)
                        #self.mat=ifs.mat
                    else:
                        self.info("no ifs defined!")
                        
            self.running=0

    def continuous_run_ifs(self):
        if self.ifs_continuous_run==0 and self.running==0:
            
            self.ifs_continuous_run=1
            self.random_run_ifs()
            
        else:
            #self.ifs_ifs_continous_runbutton.setText("start continous run")
            self.ifs_continuous_run=0

    def random_run_ifs(self):
        run=1

        while self.ifs_continuous_run or run:
            run=0
            if self.cb_ifs.checkState()==QtCore.Qt.Checked:
                i = numpy.random.randint(4)
                if i <= 2:
                    self.ifs_filename=self.get_random_filename(".ifs")
                else:
                    self.generate_ifs()
                    self.ifs_filename=""
            if self.cb_transformations.checkState()==QtCore.Qt.Checked:
                self.transformation_filename=self.get_random_filename(".tf")
            self.run_ifs()

    def get_random_filename(self, pattern):
        dir_list=os.listdir(".")
        filename_list=list([])
        for n in dir_list:
            if (pattern in n):
                filename_list.append(n)
        # print len(filename_list)
        i=numpy.random.randint(0, len(filename_list))
        return filename_list[i]

    def save_ifs(self):
        if self.fs != "":
            filename=QtWidgets.QFileDialog.getSaveFileName(self, "save file", "", "*.ifs")
            filename=str(filename)
            if filename!="":
                #print filename
                self.fractal_run.save_function_system(self.fs, filename)


    def show_julia_parameters(self):
        c=self.get_c_value()
        i=self.get_julia_iterations()
        text="c: "+str(c)+"\niterations: "+str(i)
        self.info(text)
        
    def run_julia(self):
        self.run_julia_pic(self.get_c_value())

    def run_julia_pic(self, c):
        if self.running!= 1:
            self.running=1
            xwidth, ywidth=self.get_resolution()
            if xwidth >0 and ywidth > 0:
               
                #print c
                if c!="invalid":
                    iterations=self.get_julia_iterations()
                    if iterations >0:
                        
                        self.mat=self.fractal_run.make_julia_pic(xwidth, ywidth, c, iterations)
                        #self.progress.close()
                        self.show_matrix()
            self.running=0
                    
    def random_run_julia(self):
        run=1
        while run or self.julia_continuous_run:
            run=0
            c=complex(numpy.random.random(), numpy.random.random())
            self.c_edit_real.setText(str(c.real))
            self.c_edit_imag.setText(str(c.imag))
            print(c)
            if c!="invalid":
                self.run_julia_pic(c)

    def continuous_run_julia(self):
        if self.julia_continuous_run==0 and self.running==0:
            #self.julia_continuos_runbutton.setText("stop continous run")
            self.julia_continuous_run=1
            self.random_run_julia()

        else:
            #self.julia_continuos_runbutton.setText("start continous run")
            self.julia_continuous_run=0
            
    def show_curlicue_parameters(self):
        s=self.s_value_edit.text()
        maxi=self.curlicue_max_iter.text()
        gamma=self.curlicue_gamma.text()
        st="s-value: "+s+"\n"+"max. iterations: "+maxi+"\ngamma: "+gamma
        self.info(st)
        
    def run_curlicue(self):
        s=float(eval(str(self.s_value_edit.text())))
        self.run_curlicue_pic(s)

    def run_curlicue_pic(self, s):
        if self.running!=1:
            self.running=1
            xwidth, ywidth=self.get_resolution()
            if xwidth >0 and ywidth > 0:
                
                #print c
                max_iter=int(eval(str(self.curlicue_max_iter.text())))
                gamma=float(eval(str(self.curlicue_gamma.text())))
                if type(s)==float:
    
                    self.mat=self.fractal_run.make_curlicue_pic(xwidth, ywidth, s, gamma, max_iter)
                    #self.progress.close()
                    self.show_matrix()
            self.running=0

    def random_run_curlicue(self):
        run=1
        while run or self.curlicue_continuous_run:
            run=0
            s=numpy.random.random()
            self.run_curlicue_pic(s)


    def continuous_run_curlicue(self):
        if self.curlicue_continuous_run==0 and self.running==0:
            #self.curlicue_continuos_runbutton.setText("stop continous run")
            self.curlicue_continuous_run=1
            self.random_run_curlicue()

        else:
            #self.curlicue_continuos_runbutton.setText("start continous run")
            self.curlicue_continuous_run=0

    def get_c_value(self):
        c="invalid"
        try:
            c=complex(float(self.c_edit_real.text()), float(self.c_edit_imag.text()))
        except:
            self.info("check c-value")
        return c

    def get_ifs_filename(self):
        self.ifs_filename=  QtWidgets.QFileDialog.getOpenFileName(self, "open file", "", "*.ifs")[0]
        self.ifs_label.setText(self.ifs_filename)

    def get_transformation_filename(self):
        self.transformation_filename=  QtWidgets.QFileDialog.getOpenFileName(self, "open file", "", "*.tf")[0]
        self.ifs_transformation_label.setText(self.transformation_filename)
        
    def get_resolution(self):
        xwidth=ywidth=0
        try:
            xwidth=int(self.x_resolution.text())
            ywidth=int(self.y_resolution.text())
        except:
            self.info("check resolution")
        return xwidth, ywidth

    def get_julia_iterations(self):
        iterations=0
        try:
            iterations=int(self.max_julia_iterations.text())
        except:
            self.info("check iterations")
        return iterations

    def get_ifs_iterations(self):
        iterations=0
        try:
            iterations=int(self.max_ifs_iterations.text())
        except:
            self.info("check iterations")
        return iterations

    def get_ifs_gamma(self):
        gamma=0
        try:
            gamma=float(self.ifs_gamma_factor.text())
        except:
            self.info("check gamma")
        return gamma

    def get_ifs_filter(self):
        #fmat=self.fractal_run.get_filter()
        t=table_win()
        m=self.fractal_run.get_filter_mat()
        t.set_mat(m)
        t.exec_()
        m=t.get_mat()
        self.fractal_run.set_filter_mat(m)
            
        
    def random_run_newton(self):
        run=1
        while run or self.newton_continuous_run:
            run=0
            fn=self.get_random_filename(".nf")
            eps=numpy.random.rand()
            self.newton_alpha.setText(str(eps))
            f, df=self.fractal_run.load_newton_function(fn)
            self.run_newton_pic(f, df)
        
    def continuous_run_newton(self):
        if self.newton_continuous_run==0 and self.running==0:
            #self.curlicue_continuos_runbutton.setText("stop continous run")
            self.newton_continuous_run=1
            self.random_run_newton()

        else:
            #self.curlicue_continuos_runbutton.setText("start continous run")
            self.newton_continuous_run=0


    def run_newton(self):
        if self.newton_filename!="":
            f, df=self.fractal_run.load_newton_function(self.newton_filename)
            self.run_newton_pic(f, df)
        else:
            self.info("File not found!")
        
    def run_newton_pic(self, f, df):
         if self.running!= 1:
            self.running=1       
            xwidth, ywidth=self.get_resolution()
            
            if f!="":
                print(f, df)
                i=self.get_newton_max_iterations()
                e=self.get_newton_eps()
                a=self.get_newton_alpha()
                self.mat=self.fractal_run.make_newton_pic(xwidth, ywidth, f, df, a, e,  i)
                self.show_matrix()
            else:
                self.info("No function defined!")
            self.running=0

    def show_newton_parameters(self):
        st="filename: "+self.newton_filename+"\n"
        i=self.get_newton_max_iterations()
        e=self.get_newton_eps()
        a=self.get_newton_alpha()
 
        st+="max. iterations: "+str(i)+"\n"
        st+="eps: "+str(e)+"\n"
        st+="alpha: "+str(a)+"\n"
        self.info(st)
        
    def info(self, text):
        msg=QtWidgets.QMessageBox()
        msg.setText(text)
        msg.exec_()

    def show_progress(self, i):
        self.progress.show()
        self.progress.setValue(i)
        QtWidgets.QApplication.processEvents()

    def generate_progress_dialog(self, text, button_text, max):
        self.progress=QtWidgets.QProgressDialog(text, button_text, 0, max )

    def close_progress_dialog(self):
        self.progress.close()

    def closeEvent(self, ev):
        self.mat_win.close()

    def generate_ifs(self):
        try:
            nof=int(self.ifs_number_of_functions.text())
            f=self.fractal_run.generate_ifs(nof)
            self.fs=f
            self.ifs_filename=""
            self.ifs_label.setText(self.ifs_filename)
        except:
            self.info("Number is not understood!")

    def get_newton_filename(self):
        self.newton_filename=  QtWidgets.QFileDialog.getOpenFileName(self, "open file", "", "*.nf");
        self.newton_func_label.setText(self.newton_filename)

    def get_newton_max_iterations(self):
        iterations=0
        try:
            iterations=int(self.newton_max_iterations.text())
        except:
            self.info("interations is not understood!")
        return iterations

    def get_newton_eps(self):
        eps=0
        try:
            eps=float(self.newton_epsilon.text())
        except:
            self.info("epsilon is not understood!")
        return eps

    def get_newton_alpha(self):
        eps=1.0
        try:
            eps=float(self.newton_alpha.text())
        except:
            self.info("alpha is not understood!")
        return eps

def main():
    app = QtWidgets.QApplication(sys.argv)
    gui=gui_menue(app)
    gui.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
    
