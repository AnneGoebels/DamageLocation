from func import Control, q_main, Bauteil
import ifcopenshell
from ifcopenshell.util.selector import Selector
import json
from rdflib import Namespace, URIRef, Literal

def createControlIfc (sibbw_graph, ifc_file, ifc_lbd_graph, bt_file) :

    settings = ifcopenshell.geom.settings()
    settings.set(settings.USE_PYTHON_OPENCASCADE, True)

    ANS = Namespace("https://w3id.org/asbingowl/core#")

    Control.create_bt_file(ifc_file, bt_file)

    bauteildefinition_list = q_main.get_bauteildefinition(sibbw_graph)

    with open(r".\temp_files\map_bauteilTyp.json", "r") as file:
        map_bT = json.loads(file.read())

    unlocatedBdef = []
    locatedBauteile = []
    unclearBdefWithTwoBauteile = []

    unlinkedBdefs = []

    for bauteildefinition in bauteildefinition_list:

        asbBauteilClassList, asbBauteilInstanceList = q_main.get_ifcBridgeName(sibbw_graph, bauteildefinition)
        print(asbBauteilClassList, asbBauteilInstanceList)

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
            #hier noch bdefs ohne bauteile einbeziehen

        bdef_props = q_main.query_bauteildefinition(sibbw_graph, bauteildefinition)
        # print(bdef_props)
        dictionaries = q_main.get_Ortsangabe(bdef_props)

        # print(dictionaries)
        #dictionary_oa = dictionaries[0]
        dictionary_tesBauteil = dictionaries[1]
        dictionary_feld = dictionaries[2]
        dictionary_links_rechts = dictionaries[3]
        dictionary_anfang_ende = dictionaries[4]

        print(dictionary_links_rechts)
        print(dictionary_anfang_ende)

        if len(asbBauteilInstanceList) > 1:
            print(asbBauteilInstanceList)
            unclearBdefWithTwoBauteile.append(asbBauteilInstanceList)

            for asbBauteilInstance in asbBauteilInstanceList:

                if asbBauteilInstance in locatedBauteile:
                    print("already located")

                else:
                    newdicts = q_main.get_einbauort(asbBauteilInstance,sibbw_graph)
                    if len(newdicts[0]) != 0:
                        dictionary_links_rechts = newdicts[0]
                    if len(newdicts[1]) != 0:
                        dictionary_anfang_ende = newdicts[1]
                    print(dictionary_links_rechts)
                    print(dictionary_anfang_ende)

                    if ifcBridgeName is not None:

                        if len(dictionary_links_rechts) > 0:
                            for counter, i in enumerate(dictionary_links_rechts.values()):
                                print(counter, i)

                                getIfcIns = Bauteil.check_model_representation(bauteildefinition, bdef_props, ifc_file,
                                                                               bt_file,
                                                                               ifc_lbd_graph, ifcBridgeName, i,
                                                                               dictionary_tesBauteil,
                                                                               dictionary_feld, dictionary_anfang_ende)

                                if getIfcIns is not None:
                                    ifc_lbd_instance = getIfcIns[0]
                                    IfcBauteilDesc = getIfcIns[1]
                                    print(ifc_lbd_instance, IfcBauteilDesc)
                                    sibbw_graph.add(
                                        (asbBauteilInstance, ANS.hasModelRepresentation, URIRef(ifc_lbd_instance)))
                                    locatedBauteile.append(asbBauteilInstance)
                                    sibbw_graph.add((bauteildefinition, ANS.BauteilTypInIfc, Literal(IfcBauteilDesc)))
                                else:
                                    unlocatedBdef.append(asbBauteilInstance)


                        else:
                            getIfcIns = Bauteil.check_model_representation(bauteildefinition, bdef_props, ifc_file,
                                                                           bt_file,
                                                                           ifc_lbd_graph, ifcBridgeName,
                                                                           dictionary_links_rechts,
                                                                           dictionary_tesBauteil, dictionary_feld,
                                                                           dictionary_anfang_ende)

                            if getIfcIns is not None:
                                ifc_lbd_instance = getIfcIns[0]
                                IfcBauteilDesc = getIfcIns[1]
                                print(ifc_lbd_instance, IfcBauteilDesc)
                                sibbw_graph.add(
                                    (asbBauteilInstance, ANS.hasModelRepresentation, URIRef(ifc_lbd_instance)))
                                locatedBauteile.append(asbBauteilInstance)
                                sibbw_graph.add((bauteildefinition, ANS.BauteilTypInIfc, Literal(IfcBauteilDesc)))
                            else:
                                unlocatedBdef.append(asbBauteilInstance)


                    else:
                        unlocatedBdef.append(bauteildefinition)


        elif len(asbBauteilInstanceList) == 1:

            asbBauteilInstance = asbBauteilInstanceList[0]
            if asbBauteilInstance in locatedBauteile:
                print("already located")

            else:

                if ifcBridgeName is not None:

                    if len(dictionary_links_rechts) > 0:
                        for counter, i in enumerate(dictionary_links_rechts.values()):
                            print(counter,i)

                            getIfcIns = Bauteil.check_model_representation( bauteildefinition, bdef_props, ifc_file, bt_file,
                                                                             ifc_lbd_graph, ifcBridgeName, i, dictionary_tesBauteil,
                                                                             dictionary_feld, dictionary_anfang_ende)

                            if getIfcIns is not None:
                                ifc_lbd_instance = getIfcIns[0]
                                IfcBauteilDesc = getIfcIns[1]
                                print(ifc_lbd_instance, IfcBauteilDesc)
                                sibbw_graph.add((asbBauteilInstance, ANS.hasModelRepresentation, URIRef(ifc_lbd_instance)))
                                locatedBauteile.append(asbBauteilInstance)
                                sibbw_graph.add((bauteildefinition, ANS.BauteilTypInIfc, Literal(IfcBauteilDesc)))
                            else:
                                unlocatedBdef.append(asbBauteilInstance)


                    else:
                         getIfcIns = Bauteil.check_model_representation( bauteildefinition, bdef_props, ifc_file, bt_file,
                                                                         ifc_lbd_graph, ifcBridgeName, dictionary_links_rechts,
                                                                         dictionary_tesBauteil, dictionary_feld,
                                                                         dictionary_anfang_ende)

                         if getIfcIns is not None:
                             ifc_lbd_instance = getIfcIns[0]
                             IfcBauteilDesc = getIfcIns[1]
                             print(ifc_lbd_instance,IfcBauteilDesc)
                             sibbw_graph.add((asbBauteilInstance, ANS.hasModelRepresentation, URIRef(ifc_lbd_instance)))
                             locatedBauteile.append(asbBauteilInstance)
                             sibbw_graph.add((bauteildefinition, ANS.BauteilTypInIfc, Literal(IfcBauteilDesc)))
                         else:
                             unlocatedBdef.append(asbBauteilInstance)

                else:
                    unlocatedBdef.append(bauteildefinition)
        else:
            print("Bdef not Connected to asbBauteil")
            unlinkedBdefs.append(bauteildefinition)

    print(unlocatedBdef)
    #(unclearBdefWithTwoBauteile)
    print(unlinkedBdefs)

    print("created IfcControlFile")

    return sibbw_graph



