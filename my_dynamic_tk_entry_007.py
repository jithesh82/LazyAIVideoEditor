from tkinter import *
from quitter import Quitter

#variables = []
fields = ['red is a good color i think what you think' for i in range(45)]

def fetch(variables, obj):
    #for var_ in variables:
    #    print(field, "==>", variables.get())
    #print([var.get() for var in variables])
    varValues = [var_.get() for var_ in variables]
    obj.choices = varValues
    print(obj.choices)

def makeform(root, fields, obj):
    """
    We are creating columns of frames N
    maxRows = 10
    len(fields) = 21
    N = 21 // 10 + 21 % 10 = 3 (no of columns)
    rowDistribution = [10, 10, 1] - no of rows in each column
    We need to find how to slice fields list in the above distribution
    [0:10] [10:20] [20:21]
    i : 0->2
    first index: i * 10
    second index [10, 20] + [21]
    10 10   10
     1  2   N-1
    2ndind = []
    [10 10]
    [1  2] => list(range(1, N))

    for i in range(2):
        2ind.append(rowDistribution[i] * indexlist[i])

    lastvalue = [(N-1)*10 + 21 % 10] = [21]
    """
    # ----------------------------------------------------
    # Figuring out the last index fields[:()] to slice
    # fields evenly in columns for large number of fields
    # ____________________________________________________
    maxRows = 25
    N = len(fields) // maxRows + (0 if (len(fields) % maxRows == 0) else 1)
    rowDistribution = [maxRows] * (len(fields) // 10) + [len(fields) % maxRows]  

    lastValue = [(len(fields) % maxRows) + (N-1) * maxRows] # [21]

    firstNminusOne = []
    multipliers = list(range(1, N))
    # first N-1 elements
    for i in range(N-1):
        firstNminusOne.append(rowDistribution[i] * multipliers[i])

    lastIndices = firstNminusOne + lastValue 
    print(lastIndices)
    #import sys; sys.exit()
    # -----------------------------------------------------
    

    form = Frame(root)
    form.pack()
    frames = []
    # N frame columns
    for i in range(N):
        frames.append(Frame(form))
    for frm in frames:
        frm.pack(side=LEFT)

    variables = []
    for i in range(N):
        r=0
        for field in fields[i*maxRows:lastIndices[i]]:
            var = StringVar()
            lab = Label(frames[i], text=field).grid(row=r, column=0, pady=(0, 2))
            ent = Entry(frames[i])
            ent.config(textvariable=var)
            var.set('0')
            variables.append(var)
            ent.grid(row=r, column=1)
            r += 1
    Button(root, text="FETCH", command=lambda  obj=obj:fetch(variables, obj)).pack(side=LEFT)
    return variables

if __name__ == '__main__':
    root = Tk()
    vars = makeform(root)
    #Button(root, text="FETCH", command=lambda vars=vars:fetch(vars)).pack(side=LEFT)
    Quitter(root).pack(side=RIGHT)
    mainloop()
    print([var.get() for var in vars])
