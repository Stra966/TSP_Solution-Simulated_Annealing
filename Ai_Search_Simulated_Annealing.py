#This will be the start of my program
import numpy as np
import random as rn
import copy
import math
# for 12 the best value is 56. Try to find it
def r_n_p(filename): #Read and parse
    y1 = list(range(10))
    for i in range(len(y1)):
        y1[i] = str(y1[i])
    y1.append(",") # Creates an array of digits and commas
    x2 = []
    file = open(filename+".txt","r")
    x = file.read()
    x = x.replace("\n","")
    x = x.replace(" ","")
    x1 = list(x)
    x1 = [i for i in x1 if i in y1] #List comprehension >:(   
    x1 = ''.join(x1)
    x1 = x1.split(',')
    x1.pop(0)
    for i in x1:
        x2.append(int(i))
        
   # x = x2.pop(0)
    return x2 #Returns an array of ints, where the first one is size


def arrayify(input_array): #implement numpy stuff
    maxim = input_array.pop(0)
    arr = np.full([maxim,maxim],-1,int)
    x = 0
    y = 0
    while(x<maxim):
        if(x == y):
            arr[x][y] = 0
        elif(arr[y][x] != -1):
            arr[x][y] = arr[y][x]
        else:
            arr[x][y] = input_array.pop(0)
            arr[y][x] = arr[x][y]
        #implement counters
        if(y < maxim-1): #-1 because arrays start at 0
            y+=1
        else:
            x+=1
            y = x
            
    return (arr,maxim) #returns array and the number of nodes

    
# tour_eval is a function that returns the value of a given tour based on a value matrix
def tour_eval(arr,tour): #Value array and value of given tour. Tested and works!
    v = 0 #Value of the tour
    mx = len(tour)
##    print(arr)
    x = 0 #used in the while loop
    t = 0 # t and t1 are used as the values tour[x] 
    t1 = 0 # and t1[x], because of an error that would occur otherwise
    while( x < mx):
        if(x == mx-1): #important to take tour[x] rather then x
            t = tour[x] #Due to the fact that arrays start at 0
            t1 = tour[0] #We have to subtract 1 so that it aligns with arr
            v = v + arr[t][t1]
            x+=1
        else:
            t = tour[x]
            t1 = tour[x+1]
            v =  v + arr[t][t1]
            x+=1
                    
    return v


def outpt_worth (t): # This function is used to output the tours in the form they are ment to be seen in. I.e 1,n and not 0,n-1
    t1 = copy.deepcopy(t)
    for i in range(len(t)):
        t1[i] = t1[i] + 1
    return t1

# Create another method for switching the tours. Goiing from random switch to 2 opt

def two_opt (old_t): #Tour make, I.e make new tour from old one. Works
    t1 = copy.deepcopy(old_t) # Initially give the new tour the value of the first
    mx = len(t1) 
    x = rn.randint(0,mx-1)    #Getting the two indexes of cities
    y = rn.randint(0,mx-1)    #to switch using 2opt approach
    while( y == x):             #and making sure that they 
        y = rn.randint(0,mx-1)
    if(x > y): #make sure that y is greater than x. That way the following code will always work
        x,y=y,x
    t_temp = t1[x:y] #give temp the value between x and y
    t_temp = t_temp[::-1] # Out of place reversing of iterable
    t1[x:y] = t_temp #put back into the original list
    
    
    return t1

def n_swap (t_old): #naive_swap, this functions takes the original list, and returns a new list with 2 cities swapped
        mx = len(t_old)
        t1 = copy.deepcopy(t_old) # Initially give the new tour the value of the first
        x = rn.randint(0,mx-1)    #Getting the two indexes of cities
        y = rn.randint(0,mx-1)    #to switch using 2opt approach
        while( y == x):             #and making sure that they 
            y = rn.randint(0,mx-1)#aren't the same city. 
        
        t1[x],t1[y] = t1[y],t1[x] #Switch the two cities.
        return t1
    
def sim_anne(arr): #With the current settings I'm expecting 88 cycles
    mx = arr[1] # This bit is just unpacking the tuple
    arr = arr[0]# which contains mx and the array 
    temp = 1000 #initial temperature
    dt = 0.98 # Change in temperature
##    t = t_prov #This line was used only for the experiment, the one below is used for normal functioning
    
    t = np.random.permutation([i for i in range(mx)]) #A random permutation of a tour of lenth mx
    while(temp > 0.00000001): # -d(fy-fx)/temp , this is the probability of acceptance
        
        t1 = two_opt(t)
##        t1 = n_swap(t)
        t_val = tour_eval(arr,t) #Get value of initial tour
        t1_val = tour_eval(arr,t1) #Get value of new tour

        if(t1_val < t_val): #If the new tour is better, always keep
            t = copy.deepcopy(t1)#Important to make sure it's a deepcopy otherwise it refers to the same object
        elif (math.exp((t_val-t1_val)/temp) > np.random.sample(1)): #If it's worse keep with chance
            t = copy.deepcopy(t1)
        temp*= dt
        print("These are the values for t and t1:")
        print(t)
        print(t1)
        print("These are the values for the tours:")
        print(t_val)
        print(t1_val)
    return (t,t_val) #Return the tour, as well as the value         
    

# [31, 55, 16, 21, 42, 23,  6, 46, 25, 49, 11, 13, 44, 27, 56, 37,  7,
##       41,  3, 29,  4,  9, 20, 36, 28, 10,  5, 45, 14, 26, 40, 30, 51, 22,
##       33, 35, 19, 54, 57,  0,  8, 12, 32,  2, 39, 15, 47, 50, 43, 52, 34,
##       48, 53,  1, 24, 38, 18, 17]), 37574
# 56 [3,5,8,11,10,0,1,6,4,9,7,2] - remember to add 1 to all of them using t[0:len(t)] + 1

def f (arr,t):
    t1 = np.random.permutation([i for i in range(len(arr))])
    if( tour_eval(arr,t1) < tour_eval(arr,t)):
        t = copy.deepcopy(t1)
    return t

def inpt (t):
    for i in range(len(t)):
        t[i] = t[i] - 1
    return t    
        
##x = r_n_p("NEWAISearchfile535")
##y = arrayify(x)
##z = sim_anne(y)
##t = outpt_worth(z[0])





























    
