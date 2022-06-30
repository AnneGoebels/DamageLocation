from func import q_main, AOI
import ifcopenshell
from ifcopenshell.util.selector import Selector

def createAOIIfc(sibbw_data_file,ifc_file,lbd_of_ifc_file,bt_file,aoi_file):
    #selector = Selector()
    settings = ifcopenshell.geom.settings()
    settings.set(settings.USE_PYTHON_OPENCASCADE, True)

    ### Enter data file name (.ttl) ###

    #sibbw_data_file = 'st_2079.ttl'

    ### Enter model file name (.ifc) ###

    #ifc_file = "st_2079.ifc"

    ### Enter model file name converted to LBD-Format (.ttl) ###

    #lbd_of_ifc_file = 'st_2079_lbd.ttl'

    ### The next files will be created

    #bt_file = "control.ifc"
    #aoi_file = "damage.ifc"

    ### Damage location starts here:

    AOI.create_aoi_file(sibbw_data_file, ifc_file, aoi_file)

   # model = ifcopenshell.open(ifc_file)
   # f = ifcopenshell.open(bt_file)
   # g = ifcopenshell.open(aoi_file)

    schadenObjekte_list = q_main.get_schadenObjekte(sibbw_data_file)

    i = 0

    for schadenObjekt in schadenObjekte_list:
        try:

            print(
                "__________________________________________________________________________________________________________")
            schadenquery = q_main.query_schaden_btd(sibbw_data_file, schadenObjekt)
            print(schadenquery)
            for bauteildefinition in schadenquery:
                print("Schaden: ", end='')
                print(schadenObjekt)
                print("Bauteildefinition: ", end='')
                print(bauteildefinition)
                bauteilTyp = q_main.query_bauteildefinition_bauteilTyp(sibbw_data_file, bauteildefinition)
                print("Bauteil Typ: ", end='')
                print(bauteilTyp)

                AOI.bauteildefinition_as_aoi(bauteildefinition, sibbw_data_file, schadenObjekt, 0, bauteilTyp) #??warum
                #if "AOI" in schadenquery:
                #    aoi = q_main.query_aoi(sibbw_data_file, str(schadenquery["AOI"]))
                #    print("AOI: ", end='')
                #    print(aoi)

                AOI.aoi_main(schadenObjekt, bauteildefinition, sibbw_data_file, ifc_file, bt_file, aoi_file,
                             lbd_of_ifc_file)

        except:
            print("Error")
            i = i + 1

    print("number of errors : " + str(i))

    return "AOI Ifc File created"