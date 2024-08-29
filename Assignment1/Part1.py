from vtk import *
import numpy as np

reader = vtkXMLImageDataReader()
reader.SetFileName('Data/Isabel_2D.vti')
reader.Update()
data = reader.GetOutput()

numCells = data.GetNumberOfCells()

cell = data.GetCell(0)

C = int(input("Write contour value in range of (-1438 , 630). : "))

if(C<=-1438 or C>=630):
    print("Contour Value should be in range of (-1438 , 630).")
else:
    ans = []

    # iterating through every cell of data points
    for i in range(numCells):
        currentCell = data.GetCell(i)
        
    #     print(currentCell)
        # Calculating points ids
        pid1 = currentCell.GetPointId(0)
        pid2 = currentCell.GetPointId(1)
        pid3 = currentCell.GetPointId(3)
        pid4 = currentCell.GetPointId(2)
        
    #     print(pid1,pid2,pid3,pid4)
        
        # Calculating point coordinates
        p1 = np.array(data.GetPoint(pid1))
        p2 = np.array(data.GetPoint(pid2))
        p3 = np.array(data.GetPoint(pid3))
        p4 = np.array(data.GetPoint(pid4))
        
        dataArr = data.GetPointData().GetArray('Pressure')
        
        val1 = dataArr.GetTuple1(pid1) 
        val2 = dataArr.GetTuple1(pid2) 
        val3 = dataArr.GetTuple1(pid3)
        val4 = dataArr.GetTuple1(pid4)
        
        # print(val1,val2,val3,val4)
        
        val = [val1,val2,val3,val4]
        
        # Finding active edges in counter clockwise direction
        edges = []
        if (val[3] > C and val[0] < C) or (val[3] < C and val[0] > C):
                edges.append(4)
        
        if (val[3] > C and val[2] < C) or (val[3] < C and val[2] > C):
                edges.append(3)

        if len(edges) != 2: 
            if (val[1] > C and val[2] < C) or (val[1] < C and val[2] > C):
                edges.append(2)

        if len(edges) != 2:
            if (val[0] > C and val[1] < C) or (val[0] < C and val[1] > C):
                edges.append(1)

        if(len(edges)==2):
            x = edges[0]
            y = edges[1]
           # Doing interpolation 
            px = []
            py = []
            if(x==4):
                px = ((val1-C)/(val1-val2))*(p2-p1)+p1
                if(y==2):
                    py = ((val2-C)/(val2-val3))*(p3-p2)+p2
                elif(y==3):
                    py = ((val3-C)/(val3-val4))*(p4-p3)+p3
                else:
                    py = ((val4-C)/(val4-val1))*(p1-p4)+p4
            elif(x==2):
                px = ((val2-C)/(val2-val3))*(p3-p2)+p2
                if(y==3):
                    py = ((val3-C)/(val3-val4))*(p4-p3)+p3
                else:
                    py = ((val4-C)/(val4-val1))*(p1-p4)+p4
            else:
                px = ((val3-C)/(val3-val4))*(p4-p3)+p3
                py = ((val4-C)/(val4-val1))*(p1-p4)+p4
            ans.append(px)
            ans.append(py)
                
    points = vtkPoints()
    for i in range(len(ans)):
        points.InsertNextPoint(ans[i])
  
    # Creating lines
    polyLine = vtkPolyLine()
    polyLine.GetPointIds().SetNumberOfIds(len(ans))

    for i in range(len(ans)):
        polyLine.GetPointIds().SetId(i, i)

    cells = vtkCellArray()
    cells.InsertNextCell(polyLine)

    pdata = vtkPolyData()

    pdata.SetPoints(points)
    pdata.SetLines(cells)
    
    ### Store the polydata into a vtkpolydata file with extension .vtp
    writer = vtkXMLPolyDataWriter()
    writer.SetInputData(pdata)
    writer.SetFileName('test1.vtp')
    writer.Write()
   

