from func import q_main, AOI
import ifcopenshell

def createAOIIfc(sibbw_graph, ifc_file, lbd_ifc_graph, bt_file, aoi_file):
    settings = ifcopenshell.geom.settings()
    settings.set(settings.USE_PYTHON_OPENCASCADE, True)

    AOI.create_aoi_file(ifc_file, aoi_file)

    schadenObjekte_list = q_main.get_schadenObjekte(sibbw_graph)

    unlocatedSchaden = []

    for schadenObjekt in schadenObjekte_list:

        bdef_aoi_dict = q_main.query_schaden(sibbw_graph, schadenObjekt)
        print(bdef_aoi_dict)


        # in post process hinzufügen
        #AOI.bauteildefinition_as_aoi(bauteildefinition, sibbw_graph, schadenObjekt, 0, bauteilTyp) #??warum

        #if bdef_aoi_dict["AOI"] is not None:
            # aoi = q_main.query_aoi(sibbw_graph, str( bdef_aoi_dict["AOI"]))


        a = AOI.aoi_main(schadenObjekt, bdef_aoi_dict, sibbw_graph, ifc_file, bt_file, aoi_file,
                     lbd_ifc_graph)

        if a == None:
            unlocatedSchaden.append(schadenObjekt)


    return "AOI Ifc File created"