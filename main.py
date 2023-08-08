import ezdxf

def linefilter(e):
    if e.dxftype() == "TEXT":
        if e.dxf.layer == "FLOOR":
            text=e.dxf.text
            a=e.dxf.text.find("x")
            if a != -1:
                # q=text[1:a]
                # w="x"
                # r=text[a+1:-1]
                # final="("+r+w+q+")"
                # e.dxf.text=final
                e.dxf.layer = "S042_"
                e.dxf.style = "2mm"
                e.dxf.height =175
                e.dxf.color=4
        if e.dxf.layer == "TITLE":
            text = e.dxf.text
            a = e.dxf.text.find("B")
            if a != -1:
                e.dxf.height = 250
                e.dxf.layer = "S041_"
                e.dxf.style = "2mm"
        if e.dxf.layer == "DIM-TEXT":
            text = e.dxf.text
            a = e.dxf.text.find("EF")
            if a != -1:
                e.dxf.height = 125
                e.dxf.layer = "S048__"
                e.dxf.style = "2mm"
            else:
                e.dxf.height = 125
                e.dxf.layer = "S048__"
                e.dxf.style = "2mm"
        if e.dxf.layer == "SUPPORT":
            e.dxf.height = 175
            e.dxf.layer = "S042_1-100"
            e.dxf.style = "2mm"
    if e.dxf.layer == "MAINBAR":
        e.dxf.layer = "S291_9"
    if e.dxf.layer == "STIRRUP":
        e.dxf.layer = "S291_9"
        e.dxf.color=3
    if e.dxf.layer == "LAYOUT":
        e.dxf.layer = "S282_B"
    if e.dxftype() == "DIMENSION":
        print(e)



def patch(e):
    if e.dxftype() == "TEXT":
        if e.dxf.layer == "TITLE":
            text=e.dxf.text
            a=e.dxf.text.find("U")
            if a == -1:
                text = "%%U" + text
                e.dxf.text=text
                e.dxf.height = 175
                e.dxf.layer = "S041__"
                e.dxf.style = "5mm"
    if e.dxftype() == "TEXT":
        if e.dxf.layer == "S041_":
            text=e.dxf.text
            a=e.dxf.text.find("U")
            if a == -1:
                text = "%%U" + text
                e.dxf.text=text
def distancefinder(a,b):

    temptext="a"
    for i in range(len(a)):
        min = 100000
        tempmin = 100000
        for j in range(len(b)):
            tempmin= ((a[i][0]-b[j][0])**2+(a[i][1]-b[j][1])**2)**0.5
            if tempmin<min:
                min=tempmin
                temptext=b[j][2]
        a[i].append(temptext)

def dimensionfilter(e, b,c):
    if e.dxftype() == "DIMENSION":
        if e.dxf.layer == "DIM-TEXT":
            if len(e.dxf.text) == 1:
                if abs(e.dxf.defpoint[0]-e.dxf.defpoint2[0])>500:
                    a = []
                    a.append((e.dxf.defpoint[0]+e.dxf.defpoint2[0])/2)
                    a.append((e.dxf.defpoint[1]+e.dxf.defpoint2[1])/2)
                    a.append(e)
                    a.append(e.dxf.text)
                    b.append(a)
                    print(e.dxf.text)
    if e.dxftype() == "TEXT":
        if e.dxf.layer == "DIM-TEXT":
            existence = e.dxf.text.find("-")
            if existence != -1:
                s = []
                s.append(e.dxf.insert[0])
                s.append(e.dxf.insert[1])
                s.append(e.dxf.text)
                c.append(s)
                print(e)

def dimtextadd(e,dimensionlist):
    if e.dxftype() == "DIMENSION":
        if e.dxf.layer == "DIM-TEXT":
            for i in range(len(dimensionlist)):
                if e == dimensionlist[i][2]:

                    pos=int((dimensionlist[i][4]).find("-"))
                    spacing= int(dimensionlist[i][4][pos+1:pos+4])
                    print('dimension:',e.dxf.actual_measurement, ' spacing:', spacing)
                    no=e.dxf.actual_measurement/spacing
                    if no-int(no)>0.5:
                        no=int(no)+2
                    else:
                        no=int(round(no,0))
                    e.dxf.text = str(no)+dimensionlist[i][4]
                    # print(e.dxf.text)


# if e.dxftype() == "LEADER":
    #     leader=e

# for x in range(10,32):
doc = ezdxf.readfile("B1P2B012.dxf")
msp = doc.modelspace()
dimensionlist=[]
dimtextlist=[]
for e in msp:
    dimensionfilter(e,dimensionlist,dimtextlist)
# print(len(dimensionlist))
# print((dimtextlist))
distancefinder(dimensionlist,dimtextlist)
# print(dimensionlist)
for e in msp:
    dimtextadd(e,dimensionlist)
    linefilter(e)

doc.saveas('newB1P2B012.dxf')
