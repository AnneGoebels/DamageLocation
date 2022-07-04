from func import q_main, Geom
import ifcopenshell
import ifcopenshell.geom
import ifcopenshell.util
import ifcopenshell.util.element
from ifcopenshell.util.selector import Selector
from ifcopenshell.util import element



def locate_caps(filename, newfile_name, dictionary_rechts_links):
    selector = Selector()
    global model
    model = ifcopenshell.open(filename)
    f = ifcopenshell.open(newfile_name)
    rechts_links = dictionary_rechts_links
    b = []
    element_list = selector.parse(model, '.IfcBeam | .IfcBuildingElementProxy | .IfcWall | .IfcColumn | .IfcSlab')
    for i in element_list:
        if "EDGEBEAM" in str(element.get_type(i)):
            b.append(i)
    #print(rechts_links)
    #print(type(rechts_links))
    if len(rechts_links) >0 :
        a = Geom.elements_in_box(rechts_links, model, f)

        intersection = list(set(a).intersection(b))
        if len(intersection) == 1:
            Kappe = intersection[0]
        else:
            dic = {}
            for i in intersection:
                dic[i] = Geom.bounding_box_center(i).Y()
            if rechts_links == "Rechts":
                a = sorted(dic.items(), key=lambda x: x[1])
                sorted_a = dict(a)
                Kappe = next(iter(sorted_a.keys()))
            elif rechts_links == "Links":
                a = sorted(dic.items(), key=lambda x: x[1], reverse=True)
                sorted_a = dict(a)
                Kappe = next(iter(sorted_a.keys()))
            else:
                Kappe = None
                print("Error")
    else:
        Kappe = None
        #sonst hier mit beiden verbinden??
    return Kappe


def locate_beam(filename, newfile_name, dictionary_bauteilsuche, dictionary_feld):
    selector = Selector()
    settings = ifcopenshell.geom.settings()
    settings.set(settings.USE_PYTHON_OPENCASCADE, True)
    global model
    model = ifcopenshell.open(filename)
    f = ifcopenshell.open(newfile_name)
    feld = list(dictionary_feld.values())[0]
    bts = list(dictionary_bauteilsuche.values())[0]
    a = Geom.elements_in_box(feld, model, f)
    # b = selector.parse(model, '.IfcBuildingElementProxy[Name *= "Traeger" ]')
    b = []
    element_list = selector.parse(model, '.IfcBeam | .IfcBuildingElementProxy | .IfcWall | .IfcColumn | .IfcSlab')
    for i in element_list:
        if "GIRDER_SEGMENT" in str(element.get_type(i)):
            b.append(i)
    intersection = list(set(a).intersection(b))
    dic_traeger = {}
    for key in intersection:
        dic_traeger[key] = (Geom.bounding_box_center(key).Y())
    if "BauteilVonLinks" in bts:
        n = int(bts[0])
        Traeger_von_rechts_nach_links = sorted(dic_traeger.items(), key=lambda x: x[1], reverse=True)
        Traeger = Traeger_von_rechts_nach_links[n - 1]
    elif "BauteilVonRechts" in bts:
        n = int(bts[0])
        Traeger_von_rechts_nach_links = sorted(dic_traeger.items(), key=lambda x: x[1], reverse=False)
        Traeger = Traeger_von_rechts_nach_links[n - 1]
    else:
        Traeger = None

    return Traeger


def locate_roadway(filename):
    selector = Selector()
    settings = ifcopenshell.geom.settings()
    settings.set(settings.USE_PYTHON_OPENCASCADE, True)
    global model
    model = ifcopenshell.open(filename)
    Fahrbahn = selector.parse(model, '.IfcSlab[Name *= "Landstrasse"]')
    # print(Fahrbahn)
    return Fahrbahn

def locate_superstructure(filename):
    selector = Selector()
    settings = ifcopenshell.geom.settings()
    settings.set(settings.USE_PYTHON_OPENCASCADE, True)
    global model
    model = ifcopenshell.open(filename)
    superstrc = selector.parse(model, '.IfcBuildingelementproxy[Name *= "Ueberbau"]')
    print(superstrc)
    return superstrc

def locate_bridge(filename):
    selector = Selector()
    settings = ifcopenshell.geom.settings()
    settings.set(settings.USE_PYTHON_OPENCASCADE, True)
    global model
    model = ifcopenshell.open(filename)
    bridge = selector.parse(model, '.IfcBuilding')
    print(bridge)
    return bridge

def locate_footing( filename):
    selector = Selector()
    settings = ifcopenshell.geom.settings()
    settings.set(settings.USE_PYTHON_OPENCASCADE, True)
    global model
    model = ifcopenshell.open(filename)
    footings = selector.parse(model, '.IfcFooting')
    #eigentlich liste, und in ttl mehrere fundamente erstellen
    return footings

def locate_column( filename):
    selector = Selector()
    settings = ifcopenshell.geom.settings()
    settings.set(settings.USE_PYTHON_OPENCASCADE, True)
    global model
    model = ifcopenshell.open(filename)
    columns = selector.parse(model, '.IfcColumn')
    #eigentlich liste, und in ttl mehrere pfeiler erstellen
    return columns

#workaroung, funktioniert nur für diese ifc-Datei mit custom ifc proxy names
def locate_bearing( filename, rechts_links):
    selector = Selector()
    settings = ifcopenshell.geom.settings()
    settings.set(settings.USE_PYTHON_OPENCASCADE, True)
    global model
    model = ifcopenshell.open(filename)
    if "10" in rechts_links:
        ifcDesc = "Lager A10-"
    if "30" in rechts_links:
        ifcDesc = "Lager A30-"
    if "Lagerreihe 1" in rechts_links:
        ifcDescF = ifcDesc+"1"
    if "Lagerreihe 2" in rechts_links:
        ifcDescF = ifcDesc+"2"
    bearing = selector.parse(model, '.IfcBuildingelementproxy[Name *= "'+ifcDescF+'"]')
    return bearing


def locate_railing(filename, newfile_name, dictionary_rechts_links):
    selector = Selector()
    global model
    model = ifcopenshell.open(filename)
    f = ifcopenshell.open(newfile_name)
    rechts_links = dictionary_rechts_links
    a = Geom.elements_in_box(rechts_links, model, f)
    b = selector.parse(model, '.IfcRailing')
    intersection = list(set(a).intersection(b))
    if len(intersection) == 1:
        railing = intersection[0]
    else:
        dic = {}
        for i in intersection:
            dic[i] = Geom.bounding_box_center(i).Y()
        if rechts_links == "Rechts":
            a = sorted(dic.items(), key=lambda x: x[1])
            sorted_a = dict(a)
            railing = next(iter(sorted_a.keys()))
        elif rechts_links == "Links":
            a = sorted(dic.items(), key=lambda x: x[1], reverse=True)
            sorted_a = dict(a)
            railing = next(iter(sorted_a.keys()))
        else:
            railing = None
            print("Error")
    return railing

def locate_guardrail(filename, newfile_name, dictionary_rechts_links):
    selector = Selector()
    global model
    model = ifcopenshell.open(filename)
    f = ifcopenshell.open(newfile_name)
    rechts_links = dictionary_rechts_links
    a = Geom.elements_in_box(rechts_links, model, f)
    b = selector.parse(model, '.IfcBuildingelementproxy[Name *= "Leitplanke"]')
    intersection = list(set(a).intersection(b))
    if len(intersection) == 1:
        guard = intersection[0]
    else:
        dic = {}
        for i in intersection:
            dic[i] = Geom.bounding_box_center(i).Y()
        if rechts_links == "Rechts":
            a = sorted(dic.items(), key=lambda x: x[1])
            sorted_a = dict(a)
            guard= next(iter(sorted_a.keys()))
        elif rechts_links == "Links":
            a = sorted(dic.items(), key=lambda x: x[1], reverse=True)
            sorted_a = dict(a)
            guard = next(iter(sorted_a.keys()))
        else:
            guard = None
            print("Error")
    return guard

def locate_abutment(filename, newfile_name, dictionary_oa):
    selector = Selector()
    global model
    model = ifcopenshell.open(filename)
    f = ifcopenshell.open(newfile_name)
    if len(dictionary_oa) != 0:
        a = Geom.elements_in_box(dictionary_oa["0"][8:], model, f)
        b = []
        element_list = selector.parse(model, '.IfcBeam | .IfcBuildingElementProxy | .IfcWall | .IfcColumn | .IfcSlab')
        for i in element_list:
            if "RETAININGWALL" in str(element.get_type(i)):
                b.append(i)
        intersection = list(set(a).intersection(b))
        Abutment = intersection[0]

    else:
        print("Error")
        Abutment= None
    return Abutment

# stair not in box "Anfang oder Ende des Bauwerks" --> ??
def locate_stair(filename, newfile_name, dictionary_oa):
    selector = Selector()
    global model
    model = ifcopenshell.open(filename)
    f = ifcopenshell.open(newfile_name)
    if len(dictionary_oa) != 0:
        a = Geom.elements_in_box(dictionary_oa["0"][8:], model, f)
        b = selector.parse(model, '.IfcStair')
        intersection = list(set(a).intersection(b))
        if len(intersection) > 0:
            Stair = intersection[0]
            print(Stair)
        else:
            Stair = None
            print("no Stair in Box in found")
    else:
        Stair = None
        print("Error")

    return Stair


def check_model_representation(bauteildefinition, bdef_props, ifc_file, bt_filename, lbd_graph, ifcBridgeName, oa,
                               dictionary_bauteilsuche, dictionary_feld, dictionary_anfang_ende):
    dictionary_bauteil = find_model_representation(bauteildefinition, bdef_props, ifc_file, bt_filename,
                                                   ifcBridgeName, oa, dictionary_bauteilsuche, dictionary_feld,
                                                   dictionary_anfang_ende)
    ifc_bauteil = dictionary_bauteil[bauteildefinition]

    lbd_inst_list = []
    if ifc_bauteil is not None:
        if type(ifc_bauteil) == list:
            for ifcB in ifc_bauteil:
                globalIfcID = ifcB[0]
                print(globalIfcID)
                lbd_inst = q_main.query_instance(lbd_graph, globalIfcID)
                print(lbd_inst)
                if lbd_inst:
                    lbd_inst_list.append(lbd_inst)
        else:
            globalIfcID = ifc_bauteil[0]
            lbd_inst = q_main.query_instance(lbd_graph, globalIfcID)
            if lbd_inst:
                lbd_inst_list.append(lbd_inst)

        return lbd_inst_list, dictionary_bauteil["Bauteil"]

    else:
        print("no ifc ele found")
        return None


def find_model_representation(bauteildefinition, bdef_props, filename, bt_filename, ifcBridgeName, oa,
                              dictionary_bauteilsuche, dictionary_feld, dictionary_anfang_ende):
    bauteile = {}
    if "EDGEBEAM" in ifcBridgeName:
        bauteile[bauteildefinition] = locate_caps(filename, bt_filename, oa)
        bauteile["Bauteil"] = "EDGEBEAM"
    elif "GIRDER_SEGMENT" in ifcBridgeName:
        if len(dictionary_bauteilsuche) > 0 and len(dictionary_feld) > 0:
            bauteile[bauteildefinition] = locate_beam(filename, bt_filename, dictionary_bauteilsuche, dictionary_feld)[0]
            bauteile["Bauteil"] = "GIRDER_SEGMENT"
        else:
            bauteile[bauteildefinition] = None
    elif "SLAB" in ifcBridgeName:
        bauteile[bauteildefinition] = locate_roadway(filename)[0]
        bauteile["Bauteil"] = "SLAB"
    elif "RAILING" in ifcBridgeName:
        bauteile[bauteildefinition] = locate_railing(filename, bt_filename, oa)
        bauteile["Bauteil"] = "RAILING"
    elif "GUARDRAIL" in ifcBridgeName:
        bauteile[bauteildefinition] = locate_guardrail(filename, bt_filename, oa)
        bauteile["Bauteil"] = "RAILING"
    elif "RETAININGWALL" in ifcBridgeName and "WiderlagerHinten" in str(bdef_props.values()):
        bauteile[bauteildefinition] = locate_abutment(filename, bt_filename, dictionary_anfang_ende)
        bauteile["Bauteil"] = "Widerlager_Wand_Hinten"
    elif "RETAININGWALL" in ifcBridgeName and "WiderlagerVorn" in str(bdef_props.values()):
        bauteile[bauteildefinition] = locate_abutment(filename, bt_filename, dictionary_anfang_ende)
        bauteile["Bauteil"] = "Widerlager_Wand_Vorne"
    elif "RETAININGWALL" in ifcBridgeName and "Fluegel" in str(bdef_props.values()) and "Hinten" in str(bdef_props.values()):
        bauteile[bauteildefinition] = locate_abutment(filename, bt_filename, dictionary_anfang_ende)
        bauteile["Bauteil"] = "Fluegel_Wand_Hinten"
    elif "RETAININGWALL" in ifcBridgeName and "Fluegel" in str(bdef_props.values()) and "Vorn" in str(bdef_props.values()):
        bauteile[bauteildefinition] = locate_abutment(filename, bt_filename, dictionary_anfang_ende)
        bauteile["Bauteil"] = "Fluegel_Wand_Vorne"
    elif "STAIR" in ifcBridgeName and "beideWid" in str(bdef_props.values()):
        bauteile[bauteildefinition] = locate_stair(filename, bt_filename, dictionary_anfang_ende)
        bauteile["Bauteil"] = "Widerlager_Wand_Vorne"
    elif "SUPERSTRUCTURE" in ifcBridgeName:
        bauteile[bauteildefinition] = locate_superstructure(filename)
        bauteile["Bauteil"] = "SUPERSTRUCTURE"
    elif "BRIDGE" in ifcBridgeName:
        bauteile[bauteildefinition] = locate_bridge(filename)
        bauteile["Bauteil"] = "BRIDGE"
    elif "FOOTING" in ifcBridgeName:
        bauteile[bauteildefinition] = locate_footing(filename)
        bauteile["Bauteil"] = "FOOTING"
    elif "COLUMN" in ifcBridgeName:
        bauteile[bauteildefinition] = locate_column(filename)
        bauteile["Bauteil"] = "COLUMN"
    elif "BEARING" in ifcBridgeName:
        bauteile[bauteildefinition] = locate_bearing(filename, oa)
        bauteile["Bauteil"] = "BEARING"
    else:
        bauteile[bauteildefinition] = None
        print("No Bauteil found for Bauteildefinition")

    return bauteile




