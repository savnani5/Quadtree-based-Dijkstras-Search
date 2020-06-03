# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 14:04:09 2020

@author: Paras

Will use quadtree decompostion in this, it requires application of Depth first search recurssive algorithm 

"""

import numpy as np 
import cv2 
from matplotlib import pyplot as plt 
from shapely import geometry
from shapely.geometry import Polygon
import sys
import time 


sys.setrecursionlimit(10**6) 

def length(i):
    return int(((i[1][1] - i[0][1])**2 + (i[1][0] - i[0][0])**2)**0.5)


def cell_checker(cell_points, obstacle_points): ## check order of cell_points ## cell points is a list of 4 points of the cell and obstacle_edges is a list of lists of corner points of obstacles
    cell_edges = [[cell_points[0], cell_points[1]],[cell_points[1], cell_points[2]],[cell_points[2], cell_points[3]],[cell_points[3], cell_points[0]]]
    
    polya = Polygon([cell_points[0], cell_points[1], cell_points[2], cell_points[3]]) 
   
    for obs in obstacle_points:
            polyb = Polygon(obs)     
            if polyb.contains(polya):
                return 'full'
            if polya.contains(polyb):
                return 'mixed'
            
            for cell_edge in cell_edges:
                for i in range(len(obs)):
                    if i == len(obs)-1:
                        line1 = geometry.LineString([obs[i], obs[0]])
                        line2 = geometry.LineString(cell_edge)
                        x = str(line1.intersection(line2))
                        if 'POINT' in x:
                            return 'mixed'
                    else:
                        line1 = geometry.LineString([obs[i], obs[i+1]])
                        line2 = geometry.LineString(cell_edge)
                        x = str(line1.intersection(line2))
                        if 'POINT' in x:
                            return 'mixed'                
    else:
        empty.append(cell_points)
        return 'empty'
 
def quadtree(cell_points):    
    
    ## points convention of cell_points
#        0 ______ 3
#         |      |
#         |      |
#         |______|
#        1        2
    
### Recurssive Method
    
    
    # if abs(cell_points[1][1] - cell_points[0][1]) < 4:  ## Maximum resolution limit
    #     return
    
    # cv2.line(image, ((cell_points[3][0]+cell_points[0][0])//2, cell_points[0][1]), ((cell_points[3][0]+cell_points[0][0])//2, cell_points[1][1]), (0,0,0), 1)   ## vertical line
    # cv2.line(image, (cell_points[0][0], (cell_points[1][1]+cell_points[0][1])//2), (cell_points[3][0], (cell_points[1][1]+cell_points[0][1])//2), (0,0,0), 1)  ## horizontal line
    
    
    # cell_0 = [cell_points[0], (cell_points[0][0], (cell_points[1][1]+cell_points[0][1])//2), ((cell_points[3][0]+cell_points[0][0])//2, (cell_points[1][1]+cell_points[0][1])//2), ((cell_points[3][0]+cell_points[0][0])//2, cell_points[0][1])]
    # cell = cell_checker(cell_0, obstacle_points)
    # if cell == 'mixed':
    #     quadtree(cell_0)
        
    # cell_1 = [(cell_points[0][0], (cell_points[1][1]+cell_points[0][1])//2), cell_points[1], ((cell_points[3][0]+cell_points[0][0])//2, cell_points[1][1]), ((cell_points[3][0]+cell_points[0][0])//2, (cell_points[1][1]+cell_points[0][1])//2)]
    # cell = cell_checker(cell_1, obstacle_points)
    # if cell == 'mixed':
    #     quadtree(cell_1)
    
    # cell_2 = [((cell_points[3][0]+cell_points[0][0])//2, (cell_points[1][1]+cell_points[0][1])//2), ((cell_points[3][0]+cell_points[0][0])//2, cell_points[1][1]), cell_points[2], (cell_points[3][0], (cell_points[1][1]+cell_points[0][1])//2)]
    # cell = cell_checker(cell_2, obstacle_points)
    # if cell == 'mixed':
    #     quadtree(cell_2)
        
    # cell_3 = [((cell_points[3][0]+cell_points[0][0])//2, cell_points[0][1]), ((cell_points[3][0]+cell_points[0][0])//2, (cell_points[1][1]+cell_points[0][1])//2), (cell_points[3][0], (cell_points[1][1]+cell_points[0][1])//2), cell_points[3]]
    # cell = cell_checker(cell_3, obstacle_points)
    # if cell == 'mixed':
    #     quadtree(cell_3)

    
## Iterative Method
    
    stack = []
    stack.append(cell_points)

    while(len(stack)):    
        cell_points = stack.pop(-1)
       
        x0, y0 = cell_points[0]
        x1, y1 = cell_points[1]
        x2, y2 = cell_points[2]
        x3, y3 = cell_points[3]
        
        
        if int(y1-y0) > 8:
            
            cv2.line(image, ((x3+x0)//2, y0), ((x3+x0)//2, y1), (0,0,0), 1)   ## vertical line
            cv2.line(image, (x0, (y1+y0)//2), (x3, (y1+y0)//2), (0,0,0), 1)  ## horizontal line
            
            cell_0 = [(x0, y0), (x0, (y1+y0)//2), ((x3+x0)//2, (y1+y0)//2), ((x3+x0)//2, y0)]
            
            cell = cell_checker(cell_0, obstacle_points)
            if cell=='mixed':
                stack.append(cell_0)
            
            cell_1 = [(x0, (y1+y0)//2), (x1, y1), ((x3+x0)//2, y1), ((x3+x0)//2, (y1+y0)//2)]
            
            cell = cell_checker(cell_1, obstacle_points)
            if cell=='mixed':
                stack.append(cell_1)
            
            cell_2 = [((x3+x0)//2, (y1+y0)//2), ((x3+x0)//2, y1), (x2,y2), (x3, (y1+y0)//2)]
        
            cell = cell_checker(cell_2, obstacle_points)
            if cell=='mixed':
                stack.append(cell_2)
            
            cell_3 = [((x3+x0)//2, y0), ((x3+x0)//2, (y1+y0)//2) ,(x3, (y1+y0)//2), (x3, y3)]
        
            cell = cell_checker(cell_3, obstacle_points)
            if cell=='mixed':
                stack.append(cell_3)
            
              
if __name__=="__main__":
    
    image = cv2.imread('obs_course1.png')
    image = cv2.resize(image, (450,450))
    image_dummy = image.copy()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    rows = image.shape[0]
    cols = image.shape[1]
    
## Ye contours wali bakchodi isliye ki hai kyuki khali good feature wale mei (x,y) random points milte hai, usse har obstacle isolate nahi ho sakta !
    
    ret,thresh = cv2.threshold(gray,150,255,cv2.THRESH_BINARY_INV)
    contours,_ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    
    # obstacle_edges = []
    obstacle_points = []

    for i in range(len(contours)):
        image1 = image_dummy.copy()
        cnt = contours[i]
        image1 = cv2.drawContours(image1, [cnt], 0, (0,0,0), -1)
        gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
        ret,thresh = cv2.threshold(gray1,20,255,cv2.THRESH_BINARY_INV)
        corners = cv2.goodFeaturesToTrack(thresh, 20, 0.4, 5) 
        corners = np.int0(corners) 
        cnt_points = []
        cnt_edges = []
        
        for e in corners: 
            x, y = e.ravel() 
            cnt_points.append((x,y))
            cv2.circle(image, (x, y), 2, 255, -1)

## Diagonal correction:
            
        if len(cnt_points) > 3:
            if length([cnt_points[0], cnt_points[1]]) > length([cnt_points[1], cnt_points[2]]):
                cnt_points[1], cnt_points[2] = cnt_points[2], cnt_points[1]
        
            if length([cnt_points[1], cnt_points[2]]) > length([cnt_points[2], cnt_points[3]]):
                cnt_points[2], cnt_points[3] = cnt_points[3], cnt_points[2]

        
        obstacle_points.append(cnt_points)
        
#################################
            
        # for a in range(0, len(cnt_points)):
        #     for b in range(a+1, len(cnt_points)):
        #         cnt_edges.append([cnt_points[a], cnt_points[b]])
        
## diagonal removal (no. of diagnals = n*(n-3)/2 )
                
        # n = len(cnt_edges)
        # d = int((n*(n-3))/2)
        
        # cnt_edges = sorted(cnt_edges, key = length)
        # cnt_edges = cnt_edges[0:(n-d+1)]
        
        # obstacle_edges.append(cnt_edges)
        
###################################       
    
    # cv2.rectangle(image, (200,150), (250, 200), (0,0,0), 1)
    # cell = cell_checker([(200,150),(200,200),(250,200),(250,200)], obstacle_points)
    # print(cell)
        
    empty = []
    quadtree([(0,0),(0,rows),(cols,rows),(cols,0)])  # 0-1-2-3
    print(empty)
    cv2.imshow('image',image)
    cv2.imwrite('grid.png',image)
    plt.imshow(image)
    plt.show()
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    


