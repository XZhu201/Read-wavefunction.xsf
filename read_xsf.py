# -*- coding: utf-8 -*-
"""
Created on Mon Dec  3 22:57:25 2018

@author: Xiaosong Zhu
"""

import sys
sys.path.append('/bigwork/nhbbzhux/Tools/mypip/lib/python3.5/site-packages')

import numpy as np
import linecache
import matplotlib.pyplot as plt


##### input #####
filename = input("Input the file name to read. No need to type .xsf: ")
filename = filename+'.xsf'

##### prepare to read data #####

# number of atom 
natom = input('Input the number of atoms (Directly press Enter for 1): ')
if natom=='':
	natom='1'
natom = int(natom)

begin_gridinfo = 5+natom       # the grid information begins from this line  (Line number starts from 1!)
begin_data = 10+natom    # the data begins from this line (Line number starts from 0!)

##### Read the spatial grid  #####
with open(filename, "r") as f:
	print('Open',filename)
	
	# number of grids, like  "101    121     81"
	head0 = linecache.getline(filename,begin_gridinfo)  
	head0 = head0.split()
	Lx = int(head0[0])
	Ly = int(head0[1])
	Lz = int(head0[2])
	print('\nLx, Ly, Lz = \n',Lx,Ly,Lz)
	
	# xmax
	head2 = linecache.getline(filename,begin_gridinfo+2) 
	head2 = head2.split()
	Rx = float(head2[0])/2          # don't forget /2
	
	# ymax
	head3 = linecache.getline(filename,begin_gridinfo+3) 
	head3 = head3.split()
	Ry = float(head3[1])/2
	
	# zmax
	head4 = linecache.getline(filename,begin_gridinfo+4) 
	head4 = head4.split()
	Rz = float(head4[2])/2

	print('Rx, Ry, Rz = \n',Rx,Ry,Rz)
	
	dx = 2*Rx/(Lx-1)
	dy = 2*Ry/(Ly-1)
	dz = 2*Rz/(Lz-1)
    
	print('dx, dy, dz = \n',dx,dy,dz,'\n')    

    
##### Read the data  #####
vec = np.loadtxt(filename,skiprows=begin_data-1,dtype=bytes)  # ??!!
vec = vec[:-2].astype(float)    # remove the last two non-data lines

norm = np.sum( np.abs(vec) * np.abs(vec) )*dx*dy*dz
print('The norm of the inital state is',norm,'\n')

assert len(vec)==Lx*Ly*Lz

##### 1D --> 3D for matlab  #####

# The data of .xsf is organized as:
# C-syntax:
#  for (k=0; k<nz; k++)
#  for (j=0; j<ny; j++)
#  for (i=0; i<nx; i++)
#  printf("%f",value[i][j][k]);

# So it change x value first, then y, then z.
# Note that, in matlab, the m-th row corresponds to y=m, the n-th column corresponse to x=n
# I would like to make the matrxi like that in Matlab

# Because of the above, use np.reshape in the 'C' mode. e.g.
# if A = array([ 1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12])
# np.reshape(A,(2,2,3),'C') is:

#array([[[ 1,  2,  3],
#        [ 4,  5,  6]],
#
#       [[ 7,  8,  9],
#        [10, 11, 12]]])
# which changes the column (x) first, then the row (y), finally the column
# but different from matlab, in value([i][j][k]):
# i <-> layer <-> z
# j <-> row <-> y
# k <-> column <-> x

wfn = np.reshape(vec,(Lz,Ly,Lx),'C')

# --- Above are the nots with reshape ---
# To arrange the date suitable for matlab, I can also use the loops.
# This is also OK:

#count = 0
#
#wfn = np.zeros((Ly,Lx,Lz))
#for n3 in range(Lz):
#    for n2 in range(Ly):
#        for n1 in range(Lx):
#            wfn[n3,n2,n1]=vec[count]
#            count = count+1

##### plot the 3D isosurface figure of the orbital  #####
fig, axs = plt.subplots(nrows=2,ncols=2)
plt.subplots_adjust(hspace=0.3, wspace=0.3)  # set the space between panels
            
x = np.linspace(-Rx,Rx,Lx)
y = np.linspace(-Ry,Ry,Ly)
z = np.linspace(-Rz,Rz,Lz)



# slice x-y
wfn_slice = wfn[int(np.round(Lz/2)),:,:]
axs[1,0].pcolor(x,y,wfn_slice)
# axs[1,0].set_title('slice x-y')
axs[1,0].axis([ -5, 5, -5, 5 ])
axs[1,0].set_xlabel('x')
axs[1,0].set_ylabel('y')

# slice y-z
wfn_slice = wfn[:,:,int(np.round(Lx/2))]
axs[0,1].pcolor(y,z,wfn_slice)
# axs[0,1].set_title('slice y-z')
axs[0,1].axis([ -5, 5, -5, 5 ])
axs[0,1].set_xlabel('y')
axs[0,1].set_ylabel('z')

# slice x-z
wfn_slice = wfn[:,int(np.round(Ly/2)),:]
axs[0,0].pcolor(x,z,wfn_slice)
# axs[0,0].set_title('slice x-z')
axs[0,0].axis([ -5, 5, -5, 5 ])
axs[0,0].set_xlabel('x')
axs[0,0].set_ylabel('z')

# isosurface ??
axs[1,1].text(0.1,0.3,'I don not know how to \n plot a 3D isosurface \n \
  with matplotlib... \n Can anyone help me? \n\n Thanks very much!')
# zxs.201@gmail.com. Thanks very much for help!

plt.savefig(filename+'.png')
# plt.show()
plt.close()