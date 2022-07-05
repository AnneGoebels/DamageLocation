from func import Control, q_main, Bauteil
import ifcopenshell
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

    with open(r".\temp_files\map_bauteilTyp2.json", "r") as file:
        map_bT2 = json.loads(file.read())

    unlocatedBdef = []
    locatedBauteile = []


    for bauteildefinition in bauteildefinition_list:

        asbBauteilClassList, asbBauteilInstanceList = q_main.get_ifcBridgeName(sibbw_graph, bauteildefinition)
      #print(asbBauteilClassList, asbBauteilInstanceList)

        if len(asbBauteilClassList) > 0:
            bT = []

            for j in asbBauteilClassList:
              #print(str(j))
                try:
                    res = map_bT[str(j)]
                    if "ignore" not in res and res not in bT:
                        bT.append(res)
                except:
                  print(j)

            if len(bT) > 0:
                ifcBridgeName = bT[0]
            else:
                for j in asbBauteilClassList:
                    try:
                        res = map_bT2[str(j)]
                        if res not in bT:
                            bT.append(res)
                    except:
                      print(j)

                if len(bT) > 0:
                  #print(bT)
                    ifcBridgeName = bT[0]
                else:
                    ifcBridgeName = None
                  #print("No ifcBridgeName found")
        else:
            ifcBridgeName = None
          #print("BauteilDef not connected to ASB-Bauteil")
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

        if len(asbBauteilInstanceList) > 1:

            for asbBauteilInstance in asbBauteilInstanceList:

                if asbBauteilInstance in locatedBauteile:
                  print("already located")

                else:
                    newdicts = q_main.get_einbauort(asbBauteilInstance,sibbw_graph)
                    if len(newdicts[0]) != 0:
                        dictionary_links_rechts = newdicts[0]
                    if len(newdicts[1]) != 0:
                        dictionary_anfang_ende = newdicts[1]
                  #print(dictionary_links_rechts)
                  #print(dictionary_anfang_ende)

                    if ifcBridgeName is not None:

                        if len(dictionary_links_rechts) > 0:
                            for counter, i in enumerate(dictionary_links_rechts.values()):
                              #print(counter, i)

                                getIfcIns = Bauteil.check_model_representation(bauteildefinition, bdef_props, ifc_file,
                                                                               bt_file,
                                                                               ifc_lbd_graph, ifcBridgeName, i,
                                                                               dictionary_tesBauteil,
                                                                               dictionary_feld, dictionary_anfang_ende)

                                if getIfcIns is not None:
                                    ifc_lbd_instance_list = getIfcIns[0]
                                    IfcBauteilDesc = getIfcIns[1]
                                    for ifc_inst in ifc_lbd_instance_list:
                                        sibbw_graph.add((asbBauteilInstance, ANS.hasModelRepresentation, URIRef(ifc_inst)))
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
                                ifc_lbd_instance_list = getIfcIns[0]
                                IfcBauteilDesc = getIfcIns[1]
                                for ifc_inst in ifc_lbd_instance_list:
                                    sibbw_graph.add((asbBauteilInstance, ANS.hasModelRepresentation, URIRef(ifc_inst)))
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
                          #print(counter,i)

                            getIfcIns = Bauteil.check_model_representation( bauteildefinition, bdef_props, ifc_file, bt_file,
                                                                             ifc_lbd_graph, ifcBridgeName, i, dictionary_tesBauteil,
                                                                             dictionary_feld, dictionary_anfang_ende)

                            if getIfcIns is not None:
                                ifc_lbd_instance_list = getIfcIns[0]
                                IfcBauteilDesc = getIfcIns[1]
                              #print(ifc_lbd_instance_list, IfcBauteilDesc)
                                for ifc_inst in ifc_lbd_instance_list:
                                    sibbw_graph.add((asbBauteilInstance, ANS.hasModelRepresentation, URIRef(ifc_inst)))
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
                             ifc_lbd_instance_list = getIfcIns[0]
                             IfcBauteilDesc = getIfcIns[1]
                             for ifc_inst in ifc_lbd_instance_list:
                                 sibbw_graph.add((asbBauteilInstance, ANS.hasModelRepresentation, URIRef(ifc_inst)))
                                 locatedBauteile.append(asbBauteilInstance)
                             sibbw_graph.add((bauteildefinition, ANS.BauteilTypInIfc, Literal(IfcBauteilDesc)))
                         else:
                             unlocatedBdef.append(asbBauteilInstance)

                else:
                    unlocatedBdef.append(bauteildefinition)

        elif len(asbBauteilInstanceList) == 0 and ifcBridgeName is not None:
          #print("Bdef not Connected to asbBauteil")

            getIfcIns = Bauteil.check_model_representation(bauteildefinition, bdef_props, ifc_file, bt_file,
                                                           ifc_lbd_graph, ifcBridgeName, dictionary_links_rechts,
                                                           dictionary_tesBauteil, dictionary_feld,
                                                           dictionary_anfang_ende)

            if getIfcIns is not None:
                ifc_lbd_instance_list = getIfcIns[0]
                IfcBauteilDesc = getIfcIns[1]
                for ifc_inst in ifc_lbd_instance_list:
                    sibbw_graph.add((bauteildefinition, ANS.hasModelRepresentation, URIRef(ifc_inst)))
                    locatedBauteile.append(bauteildefinition)
                sibbw_graph.add((bauteildefinition, ANS.BauteilTypInIfc, Literal(IfcBauteilDesc)))
            else:
                unlocatedBdef.append(bauteildefinition)

    #check Bauteile without damage

    allAsbBauteile = q_main.get_asbbauteil(sibbw_graph)

    for asbBauteil in allAsbBauteile:
        if asbBauteil not in locatedBauteile:

            artOrClass = q_main.get_asbbauteilArt(sibbw_graph, asbBauteil)
            bT = []
            for j in artOrClass:
              #print(j)

                try:
                    res = map_bT[str(j)]
                    if "ignore" not in res and res not in bT:
                        bT.append(res)
                except:
                  print(j)

            if len(bT) > 0:
                ifcBridgeName = bT[0]

                newdicts = q_main.get_einbauort(asbBauteil, sibbw_graph)

                dictionary_links_rechts = newdicts[0]


                getIfcIns = Bauteil.check_model_representation(asbBauteil, {}, ifc_file, bt_file,
                                                               ifc_lbd_graph, ifcBridgeName,
                                                               dictionary_links_rechts,
                                                               {}, {},
                                                               {})

                if getIfcIns is not None:
                    ifc_lbd_instance_list = getIfcIns[0]
                    IfcBauteilDesc = getIfcIns[1]
                  #print(ifc_lbd_instance_list, IfcBauteilDesc)
                    for ifc_inst in ifc_lbd_instance_list:
                        sibbw_graph.add((asbBauteil, ANS.hasModelRepresentation, URIRef(ifc_inst)))
                        locatedBauteile.append(asbBauteil)
                    sibbw_graph.add((asbBauteil, ANS.BauteilTypInIfc, Literal(IfcBauteilDesc)))
                else:
                    unlocatedBdef.append(asbBauteil)

    print("created IfcControlFile")

    return sibbw_graph



