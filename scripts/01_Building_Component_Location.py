from func import Control, q_main, Bauteil
import ifcopenshell
from ifcopenshell.util.selector import Selector
import json

selector = Selector()
settings = ifcopenshell.geom.settings()
settings.set(settings.USE_PYTHON_OPENCASCADE, True)

### Enter data file name (.ttl) ###

sibbw_data_file = r'../input/st_2079.ttl'

### Enter model file name (.ifc) ###

ifc_file = r"../input/st_2079.ifc"

### Enter model file name converted to LBD-Format (.ttl) ###

lbd_of_ifc_file = r'../input/st_2079_lbd.ttl'

### The next files will be created

bt_file = r"../temp_files/control.ifc"
aoi_file = r"../temp_files/damage.ifc"

### Building component location begins here:

Control.create_bt_file(ifc_file, bt_file)
print("done")
model = ifcopenshell.open(ifc_file)
f = ifcopenshell.open(bt_file)

bauteildefinition_list = q_main.get_bauteildefinition(sibbw_data_file)

with open(r"../temp_files/map_bauteilTyp.json", "r") as file:
    map_bT = json.loads(file.read())

h = 0

for bauteildefinition in bauteildefinition_list:

    try:

        print("_____________________________________________________")
        print(bauteildefinition)

        dictionary_oa = q_main.get_Ortsangabe(sibbw_data_file, bauteildefinition)[0]
        dictionary_tesBauteil = q_main.get_Ortsangabe(sibbw_data_file, bauteildefinition)[1]
        dictionary_feld = q_main.get_Ortsangabe(sibbw_data_file, bauteildefinition)[2]
        dictionary_links_rechts = q_main.get_Ortsangabe(sibbw_data_file, bauteildefinition)[3]
        dictionary_anfang_ende = q_main.get_Ortsangabe(sibbw_data_file, bauteildefinition)[4]
        ifcBridgeName_list = q_main.get_ifcBridgeName(sibbw_data_file, bauteildefinition)
        bT = []

        for j in ifcBridgeName_list:
            res = map_bT[j]
            if "ignore" not in res and res not in bT:
                bT.append(map_bT[j])

        if len(bT) > 0:
            ifcBridgeName = bT[0]
        else:
            ifcBridgeName = "No ifcBridgeName found"

        print("Nicht klassifizierte Ortsangaben: ", end='')
        print(dictionary_oa)
        print("Ortsangaben Anfang/Ende: ", end='')
        print(dictionary_anfang_ende)
        print("Ortsangaben für Bauteilsuche: ", end='')
        print(dictionary_tesBauteil)
        print("Feld :", end='')
        print(dictionary_feld)
        print("Links/Rechts:", end='')
        print(dictionary_links_rechts)
        print("ifcBridgeName: ")
        print(ifcBridgeName)
        if len(dictionary_links_rechts) > 0:
            for counter, i in enumerate(dictionary_links_rechts.values()):
                bauteile = Bauteil.check_model_representation(bauteildefinition, sibbw_data_file, ifc_file, bt_file,
                                                              lbd_of_ifc_file, ifcBridgeName, i, dictionary_tesBauteil,
                                                              dictionary_feld, dictionary_anfang_ende)
                GlobalId = str(
                    q_main.query_bauteildefinition_hasModelRepresentation(sibbw_data_file, bauteildefinition)[counter])
                print("GlobalId: ", end='')
                print(GlobalId)
        else:
            bauteile = Bauteil.check_model_representation(bauteildefinition, sibbw_data_file, ifc_file, bt_file,
                                                          lbd_of_ifc_file, ifcBridgeName, dictionary_links_rechts,
                                                          dictionary_tesBauteil, dictionary_feld,
                                                          dictionary_anfang_ende)
            GlobalId = str(q_main.query_bauteildefinition_hasModelRepresentation(sibbw_data_file, bauteildefinition)[0])
            print("GlobalId: ", end='')
            print(GlobalId)


    except:
        h = h + 1
        print("Error")

print("Errors : " + str(h))



