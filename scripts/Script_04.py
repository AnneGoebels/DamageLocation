from rdflib import Graph, Namespace, URIRef
from func import q_main

def CreateDamageAreasLinks(sibbw_graph):
    ANS = Namespace("https://w3id.org/asbingowl/core#")

    LbdOfDamageAreaIfc = r"C:\GitHub\DamageLocation\temp_files\damage_LBD.ttl"
    damageAreaGraph= Graph()
    damageAreaGraph.parse(LbdOfDamageAreaIfc, format="ttl")

    LbdofDamagePointIfc = r"C:\GitHub\DamageLocation\output\point_representation_LBD.ttl"
    damagePointGraph = Graph()
    damagePointGraph.parse(LbdofDamagePointIfc, format="ttl")

    SchadenObjekte = q_main.get_schadenObjekte(sibbw_graph)
    for schadenObj in SchadenObjekte:
        aoi = q_main.query_schaden(sibbw_graph,schadenObj)["AOI"]

        name = schadenObj.split("#")[1][:21]
        instlistArea = q_main.get_aoi_ifc_lbd_box(damageAreaGraph, name)
        if len(instlistArea) != 0:
            for i in instlistArea:
                print(i)
                if aoi is not None:
                    sibbw_graph.add((aoi, ANS.hasModelRepresentation, URIRef(i)))
                else:
                    sibbw_graph.add((schadenObj, ANS.hasModelRepresentation, URIRef(i)))

        instlistPoint = q_main.get_aoi_ifc_lbd_box(damagePointGraph, name)
        if len(instlistPoint) != 0:
            for ip in instlistPoint:
                print(ip)
                sibbw_graph.add((schadenObj, ANS.hasModelRepresentation, URIRef(ip)))

    return sibbw_graph



