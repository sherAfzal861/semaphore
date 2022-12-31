from tkinter import *
from threading import *
from random import random
from time import *
#here we have created structure of semaphore
#we defined the class semaphore and it will be used for synchronization
class semaphor(Semaphore):
    def __init__(self , value ):
        Semaphore.__init__(self)
        self.value = value
        self.que = []
        self.el = []
    def acquire(self ,e , name ):
        self.value -= 1
        if(self.value<0):
            self.el.append(e)
            self.que.append(name)
            e.wait()
        else:
            return
    def release(self ):
        self.value +=1
        if(self.value<=0):
            self.que.pop(0)
            e = self.el.pop(0)
            e.set()
        else:
            return
#main part of programm is starting . It is class in which front end is created
#in this class also threads are created and functions are defined to create and start threads
#these threads share counting semaphore
class main():
    def __init__(self):
        self.window = Tk()      #window to whow output of programm
        self.window.geometry( "1000x1000")      #size of window (width = 1000 && height = 1000)
        self.our_label = Label(self.window , text =  "SHER AFZAL CREATION" , font = ('bold' , 30))      #heading label
        self. our_label.pack()

        self.top_frame = Frame(self.window  , width = 1000 , height=500 , bg = 'white')         #top frame to show output of CPU and WAITING LIST
        self.top_right_frame = Frame(self.top_frame , width = 500 , height=500 , bg = 'gray')  #right frame where waiting threads will be shown
        self.waitlist = Label(self.top_right_frame , text ='WAITING LIST' , bg = 'white' , fg="black" , font=('helvetica boold' , 25)) #label of witing  list
        self.waitlist.pack()
        self.top_left_frame = Frame(self.top_frame ,width=500 , height=500 , bg = 'lightgreen')#top left frame to sho critical section and processes in it
        self.cpu = Label(self.top_left_frame , text ='CPU' , bg = 'white' , fg="black" , font=('helvetica boold' , 25))     #label of CPU heading
        self.cpu.pack()

        self.top_left_frame.pack(side = "left")             #packing of top left frame
        self.top_left_frame.pack_propagate(False)     #to avoid shrinking of frame
        self.top_right_frame.pack(side =  "left")
        self.top_right_frame.pack_propagate(False)
        
        self.bottom_frame = Frame(self.window)          #bottom frame to hold entries for taking input from user and  button to start the procedure
        self.sem_label = Label(self.bottom_frame  , text = "enter number of resources" , font  = ('helvetica boold' , 15)) #label to ask user for resources
        self.sem_entry = Entry(self.bottom_frame , width = 20 , font = ('bold' , 17))                   #entry to get resources
        self.thr_label = Label(self.bottom_frame  , text = "enter number of threads" ,font  = ('helvetica boold' , 15))  #label to ask user for threads
        self.thr_entry = Entry(self.bottom_frame , width = 20  , font =('bold' , 17))                       #entry to get number of threads
        self.botton = Button(self.bottom_frame , text = "start"  , command = self.start ,fg='white',bg='black', font  = ('helvetica boold' , 25)) #start button

        self.sem_label.pack()   #packing of entries
        self.sem_entry.pack()
        self.thr_label.pack()
        self.thr_entry.pack()
        self.botton.pack()

        self.top_frame.pack()   #packing of top frame
        self.bottom_frame.pack() #packing  of bottom frame
        mainloop()                      #loop for window to be shown
    #function which will be called on click the button
    def start(self):
        self.t = int(self.thr_entry.get())      #get the number of threads entered by user and store in variable 't'
        self.s = int(self.sem_entry.get())  #get  the number of resources entered by user and  store in variable 's'
        self.semaphore = semaphor(self.s)       #initialization of semaphore
        self.beds = []                          #que to hold string variables associated with labels of cpu(top left) frame
        #loop to create labels and string variables associated with them in top left frame
        for x in range(self.s):    
            self.source = "source"+str(x)
            self.source = StringVar()
            self.bed = "bed"+str(x)
            self.bed = Label(self.top_left_frame ,text="" , textvariable = self.source , font  = ('helvetica boold' , 15) , bg='lightgreen' , fg = 'black')
            self.bed.pack()
            self.beds.append(self.source)
        self.waiting = StringVar()   #string variables associated with que_label it will hold the processes waiting for resource on waiting list
        self.que_label = Label(self.top_right_frame ,text="", textvariable = self.waiting , font  = ('helvetica boold' , 15) ,bg='gray' , fg = 'white')
        self.que_label.pack(side='top')
        #loop for creation of threads 
        for i in range(self.t):             
            thread = Thread(target = self.task , args=(i+1 , self.semaphore))
            thread.start()
            
        daemon = Thread(target =self.bgt , daemon=True , name='Monitor') #daemon thread running in background to update que label (waiting threads)
        daemon.start()
    #function which will be called by each thread
    def task(self , number , sem):      
        e = Event()
        name = current_thread().name
        sem.acquire(e , name )
        avail = self.beds.pop(0)
        avail.set(f"Thread {number} has allotted this  resource")
        sleep((20*random()))
        avail.set(f"Thread {number} is leaving  this    resource")
        sleep(5)
        avail.set("")
        self.beds.append(avail)
        sem.release()
    #function called by daemon thread for updating the list of waiting processes
    def bgt(self):
        while True:
            self.waiting.set("")
            for x in self.semaphore.que:
                self.waiting.set(self.waiting.get()+'\n'+x)
            sleep(1)
#creation of object to start the programm
myclass = main()
