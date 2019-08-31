#!/HOME/pp292/VIPSPACE/tools/anaconda2/bin/python

'''
 a netcdf file editing tool for duplicating , modifying and deleting data and attributes.
 rationale: enumerate feature in netCDF4 python, data manipulation in the memory.
 xiaobin, 20181229
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
    self.edit_dim_name=[]
    self.edit_dim_data=[]

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

  def add_variables(self,var_name,var_dim,var_data=None,var_dtype=None,\
                     scale=None,add_offset=None,fill_value=None,zlib=None):
    assert isinstance(var_name,list)
    self.add_var_name=var_name
    if var_data is not None:
      assert isinstance(var_data,list) and len(var_name)==len(var_data)
      self.add_var_data=var_data
    else:
      self.add_var_data=[self.fin.variables[i] for i in self.add_var_name]

    if var_dtype is not None:
      assert isinstance(var_dtype,list) and len(var_name)==len(var_dtype)
      self.add_var_dtype=var_dtype
    else:
      self.add_var_dtype=['f4' for i in self.add_var_name]

    assert isinstance(var_dim,list) and len(var_name)==len(var_dim)
    self.add_var_dim=var_dim

    if zlib is not None:
      assert isinstance(zlib,list) and len(var_name)==len(zlib)
      self.add_var_zlib=zlib
    else:
      self.add_var_zlib=[False for i in self.add_var_name]

    if fill_value is not None:
      assert isinstance(fill_value,list) and len(var_name)==len(fill_value)
      self.add_var_missing=fill_value
    else:
      self.add_var_missing=[None for i in self.add_var_name]

    self.add_var_scale=scale
    self.add_var_offset=add_offset
  '''
  def add_variables(self,var_name,var_dim,var_data=None,var_dtype=None,scale=None,add_offset=None):
  def add_dimension
  '''
  '''
  '''
  def edit_dimensions(self,dim_name,dim_data):
    '''
    we assume all the dimensions are also defined with corresponding variables.
    '''
    assert isinstance(dim_data,list) and len(dim_name)==len(dim_data)
    self.edit_dim_name=dim_name
    self.edit_dim_data=dim_data
    #self.edit_var_name.append(dim_name)
    #self.edit_var_data.append(dim_data)

  def delete_variables(self,var_name):
    assert isinstance(var_name,list)
    self.del_var_name=var_name
  def delete_dimensions(self,dim_name):
    assert isinstance(dim_name,list)
    self.del_dim_name=dim_name

  def output(self,file_name=None,in_place=False,format='NETCDF4_CLASSIC'):
    fname_out=file_name
    if file_name is not None:
      fname_out=file_name
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
             if i in self.edit_dim_name:
               indx=self.edit_dim_name.index(i)
               fout.createDimension(i,len(self.edit_dim_data[indx]))
             else:
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
           tmp=fout.createVariable(i,self.add_var_dtype[ni],self.add_var_dim[ni],zlib=self.add_var_zlib[ni],fill_value=self.add_var_missing[ni])
           if self.add_var_missing[ni] is not None:
             tmp.setncattr('missing_value',self.add_var_missing[ni])
           if self.add_var_scale is not None :
             tmp.setncattr('scale_factor',self.add_var_scale[ni])
           if self.add_var_offset is not None:
             tmp.setncattr('add_offset',self.add_var_offset[ni])
           tmp[:]=self.add_var_data[ni][:]
    if in_place:
      os.rename(fname_out,self.file_in_name)

if __name__ == '__main__':
  nced=nc_edit('/VIP/pp292/dataout/2019012712/tco.rz.2019012712.ocean_u_2019_01_28.nc')
  nced.edit_variables(var_name=['U'],var_dtype=['i2'],scale=[0.00025,],fill_value=[-32768,],zlib=[True,])
  nced.delete_variables(var_name=['U'])
  nced.output('/VIP/pp292/dataout/2019012712/tco.rz.2019012712.ocean_u_2019_01_28.nc.nc')
  import numpy as np
  from netCDF4 import Dataset
  #from nc_edit import nc_edit

  fin=Dataset('/VIP/pp292/xiaob/MOM/MOM5/work/p25BT_Gebco_bedmap2/INPUT/Bedmap2_thick_p25grd.nc','r')
  ice_thick=fin.variables['thick'][:]
  fin=Dataset('/VIP/pp292/xiaob/MOM/MOM5/work/p25BT_Gebco_bedmap2/INPUT/grid_spec.nc','r')
  depth=fin.variables['depth_t'][:]
  ice_mask=np.zeros(shape=depth.shape)
  ice_mask[(depth>0.) & (ice_thick>2.)]=1

  nced=nc_edit('/VIP/pp292/xiaob/MOM/MOM5/work/p25BT_Gebco_bedmap2//INPUT/Bedmap2_thick_p25grd.nc')
  nced.delete_variables(var_name=['thick',])
  nced.add_variables(var_name=['iceshelf_mask',],var_data=[ice_mask,],var_dim=[('y','x'),])
  nced.output('/VIP/pp292/xiaob/MOM/MOM5/work/p25BT_Gebco_bedmap2/make_iceshelf_mask/iceshelf_mask.nc')

  #20190218
  fin=Dataset('/VIP/pp292/xiaob/MOM/MOM5/work/p1_WTC/INPUT/grid_spec.nc','r')
  new_depth=fin.variables['zt'][:]
  ne=nc_edit('/VIP/pp292/xiaob/EN4/EN.4.2.1.f.analysis.g10.201811.nc')
  ne.edit_dimensions(dim_name=['depth'],dim_data=[new_depth,])
  ne.output('/VIP/pp292/xiaob/EN4/EN.4.2.1.f.analysis.g10.201811-rz.nc')

