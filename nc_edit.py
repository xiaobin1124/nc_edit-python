#!/HOME/pp292/VIPSPACE/tools/anaconda2/bin/python

'''
 a netcdf file editing tool for duplicating , modifying and deleting data and attributes.
 rationale: enumerate feature in netCDF4 python, data manipulation in the memory.
 xiaobin
'''

from netCDF4 import Dataset,MFDataset,MFTime,num2date
import datetime
import numpy as np
from collections import OrderedDict

class nc_edit:
  def __init__(self,file_in_name):
    self.file_in_name=file_in_name
    self.fin=Dataset(self.file_in_name,'r')
    self.edit_var_name=[]
    self.edit_var_data=[]
    self.edit_var_dtype=[]
    self.edit_var_scale=[]
    self.edit_var_offset=[]
    self.edit_var_missing=[]
##################
#not yet finished
    self.add_var_name  = []
    self.add_var_dim   = []
    self.add_var_data  = []
    self.add_var_dtype = []
    self.add_var_scale = []
    self.add_var_offset= []
    self.add_dim_name  = []
    self.add_dim_size  = []
##################
    self.del_var_name=[]
    self.del_dim_name=[]

  def edit_variables(self,var_name,var_data=None,var_dtype=None,var_dim=None,\
                     scale=None,add_offset=None,fill_value=None,zlib=None):
    assert isinstance(var_name,list)
    self.edit_var_name=var_name
    if var_data is not None:
      assert isinstance(var_data,list) and len(var_name)==len(var_data)
      self.edit_var_data=var_data
    else:
      self.edit_var_data=[self.fin.variables[i] for i in self.edit_var_name]

    if var_dtype is not None:
      assert isinstance(var_dtype,list) and len(var_name)==len(var_dtype)
      self.edit_var_dtype=var_dtype
    else:
      self.edit_var_dtype=[self.fin.variables[i].datatype for i in self.edit_var_name]

    if var_dim is not None:
      assert isinstance(var_dim,list) and len(var_name)==len(var_dim)
      self.edit_var_dim=var_dim
    else:
      self.edit_var_dim=[self.fin.variables[i].dimensions for i in self.edit_var_name]

    if zlib is not None:
      assert isinstance(zlib,list) and len(var_name)==len(zlib)
      self.edit_var_zlib=zlib
    else:
      self.edit_var_zlib=[False for i in self.edit_var_name]

    if fill_value is not None:
      assert isinstance(fill_value,list) and len(var_name)==len(fill_value)
      self.edit_var_missing=fill_value
    else:
      self.edit_var_missing=[None for i in self.edit_var_name]

    self.edit_var_scale=scale
    self.edit_var_offset=add_offset
  '''
  def add_variables(self,var_name,var_dim,var_data=None,var_dtype=None,scale=None,add_offset=None):
  def delete_variables:
  def add_dimension
  def delete_dimension
  '''
  def output(self,file_name=None,in_place=False,format='NETCDF4_CLASSIC'):
    fname_out=file_name
    if file_name is not None:
      fname_out=file_name
    elif in_place:
      fname_out=self.file_in_name
    else:
      postfix='.nc'
      fname_out=self.file_in_name+postfix
    #print "ok"
    with Dataset(fname_out,'w',format=format) as fout:
        vin=self.fin.variables
        dimin=self.fin.dimensions
        #iterate all the global attr of srcfile and clone them in the outfile
        for i in self.fin.ncattrs():      # copy global attribute
           fout.setncattr(i,self.fin.getncattr(i))
        #iterate all the dimensions of srcfile and clone them in the outfile
        #note the exception for time
        for i in dimin.iterkeys():   # copy dimension
           if i not in self.del_dim_name:
             print i
             if i.lower()=='time': #this line should be changed, time axis should be determained through axis attr not its name
               fout.createDimension(i,None)
             else:
               fout.createDimension(i,len(dimin[i]))
        for i in self.add_dim_name: # add dimension
             if i.lower()=='time':
               fout.createDimension(i,None)
             else:
               fout.createDimension(i,self.add_dim_size[self.add_dim_name.index(i)])
        #iterate all the variables of srcfile and clone them in the outfile
        #perform the modification for specific var
        for i in vin.iterkeys():
           if (i not in self.del_var_name) and (i not in self.del_dim_name):
             invar=vin[i]
             if i in self.edit_var_name:
                print 'edit var '+i
                indx=self.edit_var_name.index(i)
                tmp=fout.createVariable(i,self.edit_var_dtype[indx],self.edit_var_dim[indx],zlib=self.edit_var_zlib[indx],fill_value=self.edit_var_missing[indx])
                for iattr in invar.ncattrs():
                   print 'xiao 1.2 '+iattr
                   if not iattr == '_FillValue':
                     #print 'xiao 0 '+iattr
                     #print invar
                     #print 'xiao 1 '+iattr
                     #print invar.getncattr(iattr)
                     #print tmp.ncattrs()
                     #if iattr == '_FillValue':
                     #  print 'xiao 1.1 '+iattr
                     #  #import pdb;pdb.set_trace()
                     #  tmp.setncattr('_FillValue',1.0)
                     #else:
                     tmp.setncattr(iattr,invar.getncattr(iattr))
                     #if iattr == '_FillValue':
                     #  tmp.setncattr('_FillValue',1)
                     #print 'xiao 2 '+iattr
                if self.edit_var_missing[indx] is not None:
                  tmp.setncattr('missing_value',self.edit_var_missing[indx])
                if self.edit_var_scale is not None :
                  tmp.setncattr('scale_factor',self.edit_var_scale[indx])
                if self.edit_var_offset is not None:
                  tmp.setncattr('add_offset',self.edit_var_offset[indx])
                tmp[:]=self.edit_var_data[self.edit_var_name.index(i)][:]
             else:
                tmp=fout.createVariable(i,invar.dtype,invar.dimensions)
                for iattr in invar.ncattrs():
                   tmp.setncattr(iattr,invar.getncattr(iattr))
                tmp[:]=invar[:]
        for ni,i in enumerate(self.add_var_name):
           print('add var',i)
           tmp=fout.createVariable(i,self.add_var_dtype[ni],self.add_var_dim[ni])
           tmp[:]=self.add_var_data[ni][:]

if __name__ == '__main__':
  nced=nc_edit('/VIP/pp292/dataout/2018122712/tco.rz.2018122712.ocean_u_2019_01_01.nc')
  #nced.edit_variables(var_name=['U'],var_dtype=['i2'],scale=[0.001,],zlib=[True,])
  nced.edit_variables(var_name=['U'],var_dtype=['i2'],scale=[0.00025,],fill_value=[-32768,],zlib=[True,])
  nced.output('/VIP/pp292/dataout/2018122712/tco.rz.2018122712.ocean_u_2019_01_01.nc.nc')

