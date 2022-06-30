from func import Control, q_main, Bauteil
import ifcopenshell
from ifcopenshell.util.selector import Selector
import json

def createControlIfc (sibbw_data_file,ifc_file,lbd_of_ifc_file,bt_file) :
    settings = ifcopenshell.geom.settings()
    settings.set(settings.USE_PYTHON_OPENCASCADE, True)

    ### Building component location begins here:

    Control.create_bt_file(ifc_file, bt_file)
   # model = ifcopenshell.open(ifc_file)
   # f = ifcopenshell.open(bt_file)

    bauteildefinition_list = q_main.get_bauteildefinition(sibbw_data_file)

    with open(r".\temp_files\map_bauteilTyp.json", "r") as file:
        map_bT = json.loads(file.read())

    unlocatedBdef = []

    for bauteildefinition in bauteildefinition_list:

        print("_____________________________________________________")
        print(bauteildefinition)

        dictionary_oa = q_main.get_Ortsangabe(sibbw_data_file, bauteildefinition)[0]
        dictionary_tesBauteil = q_main.get_Ortsangabe(sibbw_data_file, bauteildefinition)[1]
        dictionary_feld = q_main.get_Ortsangabe(sibbw_data_file, bauteildefinition)[2]
        dictionary_links_rechts = q_main.get_Ortsangabe(sibbw_data_file, bauteildefinition)[3]
        dictionary_anfang_ende = q_main.get_Ortsangabe(sibbw_data_file, bauteildefinition)[4]

        ifcBridgeName_list, asbBauteilList = q_main.get_ifcBridgeName(sibbw_data_file, bauteildefinition)

        print(asbBauteilList)

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

        if ifcBridgeName is not None:

            if len(dictionary_links_rechts) > 0:
                for counter, i in enumerate(dictionary_links_rechts.values()):
                    print(counter,i)

                    addIfctoRDF = Bauteil.check_model_representation(asbBauteilList,bauteildefinition, sibbw_data_file, ifc_file, bt_file,
                                                                  lbd_of_ifc_file, ifcBridgeName, i, dictionary_tesBauteil,
                                                                  dictionary_feld, dictionary_anfang_ende)

                    print(addIfctoRDF)
                    if addIfctoRDF is None:
                        unlocatedBdef.append(bauteildefinition)


            else:
                addIfctoRDF = Bauteil.check_model_representation(asbBauteilList, bauteildefinition, sibbw_data_file, ifc_file, bt_file,
                                                              lbd_of_ifc_file, ifcBridgeName, dictionary_links_rechts,
                                                              dictionary_tesBauteil, dictionary_feld,
                                                              dictionary_anfang_ende)

                print(addIfctoRDF)
                if addIfctoRDF is None:
                    unlocatedBdef.append(bauteildefinition)



        else:
            unlocatedBdef.append(bauteildefinition)

    print(unlocatedBdef)

    return "created IfcControlFile"



