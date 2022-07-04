import os
from scripts import Script_01, Script_02, Script_03
from func import Control
from rdflib import Graph, Namespace, URIRef
import ifcopenshell
from func import Ifc, q_main

### Enter data file name (.ttl) ###
sibbw_data_file = r"C:\GitHub\DamageLocation\input\SIB7936662_2022-06-23.ttl"

### Enter model file name (.ifc) ###
ifc_file = r"C:\GitHub\DamageLocation\input\st_2079.ifc"

## Enter model file name converted to LBD-Format (.ttl) ###
lbd_of_ifc_file = r'C:\GitHub\DamageLocation\input\st_2079_lbd.ttl'

### The next files will be created
bt_file = r"C:\GitHub\DamageLocation\temp_files\control.ifc"
aoi_file = r"C:\GitHub\DamageLocation\temp_files\damage.ifc"

### outputfiles
point_file = r"C:\GitHub\DamageLocation\output\point_representation.ifc"
bcf_file = (str(os.path.abspath(os.getcwd())) + "\\output\\bcf_representation.bcf")

#creates f and opens both for ifcopenshell
#global model
#global control_icf

#model, f = Control.create_bt_file(ifc_file, bt_file)

#prepares graph handling
ANS = Namespace("https://w3id.org/asbingowl/core#")
AONS = Namespace("https://w3id.org/asbingowl/keys/2013#")
ANSK = Namespace("https://w3id.org/asbingowl/keys#")
AOI = Namespace ("https://w3id.org/aoi#")
OPM = Namespace("https://w3id.org/opm#")
SCHEMA = Namespace("http://schema.org/")
DOT = Namespace("https://w3id.org/dot#")
INST = Namespace("https://asbingowl.org/TwinGenDemo/BW452#")
PROPS = Namespace("http://lbd.arch.rwth-aachen.de/props#")


sibbw_graph = Graph()
sibbw_graph.parse(sibbw_data_file, format="ttl")


sibbw_graph.bind("asb", ANS)
sibbw_graph.bind("asbkey13", AONS)
sibbw_graph.bind("asbkey", ANSK)
sibbw_graph.bind("aoi", AOI)
#sibbw_graph.bind("opm", OPM)
#sibbw_graph.bind("schema", SCHEMA)
sibbw_graph.bind("dot", DOT)
sibbw_graph.bind("inst", INST)

ifc_lbd_graph = Graph()
ifc_lbd_graph.parse(lbd_of_ifc_file, format="ttl")

ifc_lbd_graph.bind("schema", SCHEMA)
ifc_lbd_graph.bind("props", PROPS )


graphWithIfcLinks = Script_01.createControlIfc(sibbw_graph, ifc_file, ifc_lbd_graph, bt_file)
graphWithIfcLinks.serialize("C:\GitHub\DamageLocation\output\SIBBWGraphWithIfcLinks.ttl")
#print(first)
#second = Script_02.createAOIIfc(sibbw_data_file,ifc_file,lbd_of_ifc_file,bt_file,aoi_file)
#print(second)
#third = Script_03.createDamageRepresentationFiles(sibbw_data_file,ifc_file,aoi_file,point_file,bcf_file)
#print(third)