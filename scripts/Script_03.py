from OCC.Core.BRep import BRep_Tool
import ifcopenshell.geom
import ifcopenshell.util.element
from ifcopenshell.util.selector import Selector
from OCC.Core.gp import (gp_Pnt)
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCC.Core.TopAbs import TopAbs_VERTEX
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Extend.TopologyUtils import TopologyExplorer
from func import BCF, Ifc, AOI, Geom, q_main

def createDamageRepresentationFiles(sibbw_graph, ifc_file, aoi_file, point_file, bcf_file):

    selector = Selector()
    settings = ifcopenshell.geom.settings()
    settings.set(settings.USE_PYTHON_OPENCASCADE, True)

    ### BCF representation

    damage_ifc = ifcopenshell.open(aoi_file)
    aoi_elements = selector.parse(damage_ifc, ".IfcBuildingElementProxy")
    BCF.export_bcfxml(aoi_elements, bcf_file, ifc_file,sibbw_graph)

    ### IFC representation

    AOI.create_aoi_file(ifc_file, point_file)
    point_ifc = ifcopenshell.open(point_file)


    aoi_elements = selector.parse(damage_ifc, ".IfcBuildingElementProxy")

    for i in aoi_elements:
        schadenObjekt = i.Name
        #entsprichtIfcType = i.Description
        desc = q_main.get_Schaden_Desc(sibbw_graph,schadenObjekt)
        mitte = Geom.bounding_box_center(i)
        corner1 = gp_Pnt(mitte.X()-0.15,mitte.Y()-0.15,mitte.Z()-0.15)
        corner2 = gp_Pnt(mitte.X()+0.15,mitte.Y()+0.15,mitte.Z()+0.15)
        box = BRepPrimAPI_MakeBox(corner1, corner2)
        height_box = 0.3
        top2_up_bottom = TopologyExplorer(box.Shape())
        for i, sol2 in enumerate(top2_up_bottom.solids()):
            vertex_F = TopExp_Explorer(sol2,TopAbs_VERTEX)
            x_y_F = []
            while vertex_F.More() == True:
                currentvertex = vertex_F.Current()
                point = BRep_Tool.Pnt(currentvertex)
                if[round(point.X(),2),round(point.Y(),2)] not in x_y_F:
                    x_y_F.append([round(point.X(),2),round(point.Y(),2)])
                vertex_F.Next()
            plea = Geom.sorted_point_list_extrusion_area(sol2, x_y_F)
        Ifc.place_object(point_ifc, box, plea, height_box, schadenObjekt, point_file, Description=desc)

    return "Damage Ifc and BCF created"