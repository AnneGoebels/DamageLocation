from func import Control, q_main, Bauteil
import ifcopenshell
from ifcopenshell.util.selector import Selector
import json


settings = ifcopenshell.geom.settings()
settings.set(settings.USE_PYTHON_OPENCASCADE, True)

sibbw_data_file = r"C:\GitHub\DamageLocation\input\st_2079.ttl"
ifc_file = r"C:\GitHub\DamageLocation\input\st_2079.ifc"
lbd_of_ifc_file = r'C:\GitHub\DamageLocation\input\st_2079_lbd.ttl'
bt_file = r"C:\GitHub\DamageLocation\temp_files\control.ifc"

Control.create_bt_file(ifc_file, bt_file)

bauteildefinition_list = q_main.get_bauteildefinition(sibbw_data_file)

with open(r".\temp_files\map_bauteilTyp.json", "r") as file:
    map_bT = json.loads(file.read())

for bauteildefinition in bauteildefinition_list:

    print(bauteildefinition)
    dictionaries = q_main.get_Ortsangabe(sibbw_data_file, bauteildefinition)
    print(dictionaries)

    dictionary_oa = dictionaries[0]
    dictionary_tesBauteil = dictionaries[1]
    dictionary_feld = dictionaries[2]
    dictionary_links_rechts = dictionaries[3]
    dictionary_anfang_ende = dictionaries[4]

    ifcBridgeName_list = q_main.get_ifcBridgeName(sibbw_data_file, bauteildefinition)
    if len(ifcBridgeName_list) > 0:
        bT = []
        for j in ifcBridgeName_list:
            res = map_bT[j]
            if "ignore" not in res and res not in bT:
                bT.append(res)
        if len(bT) > 0:
            ifcBridgeName = bT[0]
        else:
            ifcBridgeName = None
            print("No ifcBridgeName found")
    else:
        ifcBridgeName = None
        print("BauteilDef not connected to ASB-Bauteil")

    print(ifcBridgeName)

    if ifcBridgeName is not None:
        if len(dictionary_links_rechts) == 0:
            if ifcBridgeName == "RETAININGWALL":
                ifc_bauteil = Bauteil.locate_abutment(ifc_file,bt_file,dictionary_anfang_ende)

                # this print is never if i run the file
                print(ifc_bauteil)
