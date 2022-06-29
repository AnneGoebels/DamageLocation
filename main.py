import os
from scripts import Script_01, Script_02, Script_03
### Enter data file name (.ttl) ###

sibbw_data_file = r"C:\GitHub\DamageLocation\input\st_2079.ttl"

### Enter model file name (.ifc) ###

ifc_file = r"C:\GitHub\DamageLocation\input\st_2079.ifc"

### Enter model file name converted to LBD-Format (.ttl) ###

lbd_of_ifc_file = r'C:\GitHub\DamageLocation\input\st_2079_lbd.ttl'

### The next files will be created

bt_file = r"C:\GitHub\DamageLocation\temp_files\control.ifc"
aoi_file = r"C:\GitHub\DamageLocation\temp_files\damage.ifc"

### outputfiles
point_file = r"C:\GitHub\DamageLocation\output\point_representation.ifc"
bcf_file = (str(os.path.abspath(os.getcwd())) + "\\output\\bcf_representation.bcf")


first = Script_01.createControlIfc(sibbw_data_file,ifc_file,lbd_of_ifc_file,bt_file)
print(first)
second = Script_02.createAOIIfc(sibbw_data_file,ifc_file,lbd_of_ifc_file,bt_file,aoi_file)
print(second)
third = Script_03.createDamageRepresentationFiles(sibbw_data_file,ifc_file,aoi_file,point_file,bcf_file)
print(third)