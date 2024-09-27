from tkinter import *
from tkinter import ttk, messagebox
from tkinter.filedialog import askopenfilename, askdirectory
import tkinter.scrolledtext as tkst
from pathlib import Path
from composer.composer import *
#import for open output directory
import subprocess
import sys
#Software version
from _version import __version__



class MainWindows:

    __selectedFilelabel=None
    __selectFileButton=None
    __selectedOutDirlabel=None
    __selectOutDirButton=None
    __selectCheckButton=None
    __selectCheckPolicyButton=None
    __selectCheckPolicyInternalContractButton=None
    __mainWin=None
    __editArea=None
    __closeButton=None
    __varF = None
    __varD = None
    __chkValue = None
    __chkPolicyValue = None

    def __init__(self):

        self.__mainWin = Tk()

        #imgPath=self.__resource_path('logo/dbanapoli.png')
        #img = PhotoImage(file=imgPath)
        #self.__mainWin.tk.call('wm', 'iconphoto', self.__mainWin._w, img)

        self.__varF = StringVar(self.__mainWin)
        self.__varD = StringVar(self.__mainWin)
        self.__chkValue = BooleanVar()
        self.__chkValue.set(False)
        #External policy index
        self.__chkPolicyValue = BooleanVar()
        self.__chkPolicyValue.set(False)
        #Internal policy Index
        self.__chkPolicyValueInternal = BooleanVar()
        self.__chkPolicyValueInternal.set(False)


        title = self.__mainWin.title("PlantUmlToJsonSchema")
        self.__mainWin.minsize(width=670, height=550)
        #self.__mainWin.maxsize(width=670, height=550)
        self.__centeronscreen(self.__mainWin)

        self.__varF.set('<unselected file>')
        self.__varD.set('<unselected dir>')
        self.__selectedFilelabel = ttk.Label(self.__mainWin, relief='groove' ,textvariable=self.__varF,foreground='red')
        self.__selectedFilelabel.grid(row=0,column=1,columnspan=2,sticky=W)
        self.__selectFileButton=ttk.Button(self.__mainWin,text='Select PlantUml File',width=24,command = self.__openfile)
        self.__selectFileButton.grid(row=0,column=0,sticky=W)

        self.__selectedOutDirlabel = ttk.Label(self.__mainWin,relief='groove' , textvariable=self.__varD,foreground='red')
        self.__selectedOutDirlabel.grid(row=2,column=1,columnspan=2,sticky=W)
        self.__selectOutDirButton=ttk.Button(self.__mainWin,text='Select Output Directory',width=24,command = self.__opendir)
        self.__selectOutDirButton.grid(row=2,column=0,sticky=W)


        self.__selectCheckPolicyButton=ttk.Checkbutton(self.__mainWin, text='Generate policy index files External Contract', var=self.__chkPolicyValue)
        self.__selectCheckPolicyInternalContractButton=ttk.Checkbutton(self.__mainWin, text='Generate policy index files Internal Contract', var=self.__chkPolicyValueInternal)
        self.__selectCheckButton=ttk.Checkbutton(self.__mainWin, text='Open output directory after parsing', var=self.__chkValue)

        self.__selectCheckPolicyButton.grid(row=3,column=0,columnspan=2,sticky=W)
        self.__selectCheckPolicyInternalContractButton.grid(row=4,column=0,columnspan=2,sticky=W)
        self.__selectCheckButton.grid(row=5,column=0,columnspan=2,sticky=W)


        self.__editArea = tkst.ScrolledText(master =self.__mainWin)
        self.__editArea.grid(row=6,column=0,columnspan=3,sticky=W)
        self.__editArea.configure(state='normal')
        self.__editArea.configure(state='disabled')

        __parserButton=ttk.Button(self.__mainWin,text='Parse',command=self.__parser)
        __parserButton.grid(row=7,column=0,sticky=E)
        __closeButton=ttk.Button(self.__mainWin,text='Close', command = lambda:self.__mainWin.destroy())
        __closeButton.grid(row=7,column=1,sticky=W)

        #Print version

        self.writeLog('PlantUmlToJSchema version {} by Massimo Iannuzzi DBA Team'.format(__version__))
        self.__mainWin.mainloop()

    #Define function for specific OS system
    if 'darwin' in sys.platform:
        def __openFolder(self,path):
            subprocess.check_call(['open', '--', path])
    elif 'linux' in sys.platform:
        def __openFolder(self,path):
            subprocess.check_call(['xdg-open', '--', path])
    elif 'win' in sys.platform:
        def __openFolder(self,path):
            subprocess.call('explorer {}'.format(path.replace('/','\\')),shell=True)

    def __resource_path(self,relative):
        if hasattr(sys, "_MEIPASS"):
            return os.path.join(sys._MEIPASS, relative)
        return os.path.join(relative)

    def __centeronscreen(self,window, w='', h=''):

        # Non so a cosa serva e l'ho commentato
        # parent = window.winfo_parent()
        # if type(parent) == types.StringType:
        #    parent = window._hull._nametowidget(parent)

        # Find size of window.
        window.update_idletasks()
        if w == '' or h == '':
            w = window.winfo_width()
            h = window.winfo_height()
            if w == 1 and h == 1:
                # If the window has not yet been displayed, its size is
                # reported as 1x1, so use requested size.
                w = window.winfo_reqwidth()
                h = window.winfo_reqheight()

        # Place in centre of screen:
        x = int((window.winfo_screenwidth() - w) / 2.0)
        y = int((window.winfo_screenheight() - h) / 2.0)
        if x < 0:
            x = 0
        if y < 0:
            y = 0
        geometry = str(w) + 'x' + str(h) + '+' + str(x) + '+' + str(y)
        window.geometry(geometry)
        return 0

    #This is where we lauch the file manager bar.
    def __openfile(self):

        home = str(Path.home())
        fileName = askopenfilename(initialdir=home,
                               filetypes =(("PlantUml file", "*.puml"),("All Files","*.*")),
                               title = "Choose a file."
                               )
        if (fileName is not None and len(fileName)>0):
            self.__varF.set(fileName)
            self.__selectedFilelabel.configure(foreground='green')

    #This is where we lauch the file manager bar.
    def __opendir(self):

        home = str(Path.home())
        dirName = askdirectory(initialdir=home,title = "Choose output directory.")

        if (dirName is not None and len(dirName)>0):
            self.__varD.set(dirName)
            self.__selectedOutDirlabel.configure(foreground='green')



    def __parser(self):


        filePath=self.getFilePath()
        dirPath=self.getDirPath()

        if 'unselected file' in filePath:
            messagebox.showinfo("Error!!", "No file selected")
            return

        if 'unselected dir' in dirPath:
            messagebox.showinfo("Error!!", "No output dir selected")
            return

        try:
            self.cleanLogArea()
            with open(filePath, 'r') as f:
                lines = f.readlines()
                composer = Composer(lines,self)
                composer.composerGenerator(dirPath);
                if (self.__chkValue.get()):
                    self.__openFolder(dirPath)
        except Exception as ex:
            self.writeLog(str(ex))
            self.writeLog('Parsing aborted!')

    def getFilePath(self):
        return self.__varF.get()

    def getDirPath(self):
        return self.__varD.get()

    def writeLog(self,textStr):

        self.__editArea.configure(state='normal')
        self.__editArea.insert(INSERT, textStr)
        self.__editArea.insert(END, "\n")
        self.__editArea.configure(state='disabled')


    def cleanLogArea(self):
        self.__editArea.configure(state='normal')
        self.__editArea.delete(1.0,END)
        self.__editArea.configure(state='disabled')

    def isPolicyIndex(self):
        return self.__chkPolicyValue.get()

    def isPolicyIndexInternal(self):
        return self.__chkPolicyValueInternal.get()

if __name__ == "__main__":

    m=MainWindows()
    print (m.getFilePath())