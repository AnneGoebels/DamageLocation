from func import Control, q_main, Bauteil
import ifcopenshell
from ifcopenshell.util.selector import Selector
import json
from rdflib import Namespace

def createControlIfc (sibbw_graph, ifc_file, ifc_lbd_graph, bt_file) :

    selector =  Selector()
    x =selector.parse(ifc_file, ".IfcRailing")
    print(x)

    settings = ifcopenshell.geom.settings()
    settings.set(settings.USE_PYTHON_OPENCASCADE, True)

    #opens turtle files
    ANS = Namespace("https://w3id.org/asbingowl/core#")
    ### Building component location begins here:

    #model, f = Control.create_bt_file(ifc_file, bt_file)
   # model = ifcopenshell.open(ifc_file)
   # f = ifcopenshell.open(bt_file)

    bauteildefinition_list = q_main.get_bauteildefinition(sibbw_graph)
    #print(bauteildefinition_list)

    with open(r".\temp_files\map_bauteilTyp.json", "r") as file:
        map_bT = json.loads(file.read())

    unlocatedBdef = []
    locatedBauteile = []

    for bauteildefinition in bauteildefinition_list:

        asbBauteilClassList, asbBauteilInstanceList = q_main.get_ifcBridgeName(sibbw_graph, bauteildefinition)
        print(asbBauteilClassList, asbBauteilInstanceList)

        for asbBauteilInstance in asbBauteilInstanceList:

            if asbBauteilInstance in locatedBauteile:
                print("already located")
            else:
                print(bauteildefinition)
                bdef_props = q_main.query_bauteildefinition(sibbw_graph, bauteildefinition)
                #print(bdef_props)
                dictionaries = q_main.get_Ortsangabe(bdef_props)

                #print(dictionaries)
                dictionary_oa = dictionaries[0]
                dictionary_tesBauteil = dictionaries[1]
                dictionary_feld = dictionaries[2]
                dictionary_links_rechts = dictionaries[3]
                dictionary_anfang_ende =dictionaries[4]


                if len(asbBauteilClassList) > 0:
                    bT = []

                    for j in asbBauteilClassList:
                        print(str(j))
                        try:
                            res = map_bT[str(j)]
                            if "ignore" not in res and res not in bT:
                                bT.append(res)
                        except:
                            print(j)

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

                            ifc_lbd_instance = Bauteil.check_model_representation( bauteildefinition, bdef_props, ifc_file, bt_file,
                                                                             ifc_lbd_graph, ifcBridgeName, i, dictionary_tesBauteil,
                                                                             dictionary_feld, dictionary_anfang_ende)

                            print(ifc_lbd_instance)
                            if ifc_lbd_instance is not None:
                                sibbw_graph.add((asbBauteilInstance, ANS.hasModelRepresentation, ifc_lbd_instance))
                                locatedBauteile.append(asbBauteilInstance)
                            else:
                                unlocatedBdef.append(asbBauteilInstance)


                    else:
                        ifc_lbd_instance = Bauteil.check_model_representation( bauteildefinition, bdef_props, ifc_file, bt_file,
                                                                         ifc_lbd_graph, ifcBridgeName, dictionary_links_rechts,
                                                                         dictionary_tesBauteil, dictionary_feld,
                                                                         dictionary_anfang_ende)
                        print(ifc_lbd_instance)
                        if ifc_lbd_instance is not None:
                            sibbw_graph.add((asbBauteilInstance, ANS.hasModelRepresentation, ifc_lbd_instance))
                            locatedBauteile.append(asbBauteilInstance)
                        else:
                            unlocatedBdef.append(asbBauteilInstance)

                else:
                    unlocatedBdef.append(bauteildefinition)

    print(unlocatedBdef)

    return "created IfcControlFile"



