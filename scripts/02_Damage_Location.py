from func import q_main, AOI
import ifcopenshell
from ifcopenshell.util.selector import Selector

selector = Selector()
settings = ifcopenshell.geom.settings()
settings.set(settings.USE_PYTHON_OPENCASCADE, True)

### Enter data file name (.ttl) ###

data_filename = 'st_2079.ttl'

### Enter model file name (.ifc) ###

filename = "st_2079.ifc"

### Enter model file name converted to LBD-Format (.ttl) ###

lbd_filename = 'st_2079_lbd.ttl'

### The next files will be created

bt_filename = "control.ifc"
aoi_filename = "damage.ifc"

### Damage location starts here:

AOI.create_aoi_file(data_filename, filename, aoi_filename)

model = ifcopenshell.open(filename)
f = ifcopenshell.open(bt_filename)
g = ifcopenshell.open(aoi_filename)

schadenObjekte_list = q_main.get_schadenObjekte(data_filename)

i = 0

for schadenObjekt in schadenObjekte_list:
    try:

        print(
            "__________________________________________________________________________________________________________")
        schadenquery = q_main.query_schaden_btd(data_filename, schadenObjekt)
        for bauteildefinition in schadenquery:
            print("Schaden: ", end='')
            print(schadenObjekt)
            print("Bauteildefinition: ", end='')
            print(bauteildefinition)
            bauteilTyp = q_main.query_bauteildefinition_bauteilTyp(data_filename, bauteildefinition)
            print("Bauteil Typ: ", end='')
            print(bauteilTyp)

            AOI.bauteildefinition_as_aoi(bauteildefinition, data_filename, schadenObjekt, 0, bauteilTyp)
            if "AOI" in schadenquery:
                aoi = q_main.query_aoi(data_filename, str(schadenquery["AOI"]))
                print("AOI: ", end='')
                print(aoi)

            AOI.aoi_main(schadenObjekt, bauteildefinition, data_filename, filename, bt_filename, aoi_filename,
                         lbd_filename)

    except:
        print("Error")
        i = i + 1

print("number of errors : " + str(i))