from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import OWL, RDF
from rdflib.plugins.sparql import prepareQuery
#import q_main
import json
import random
import copy

ANS = Namespace("https://w3id.org/asbingowl/core#")
AONS = Namespace("https://w3id.org/asbingowl/keys/2013#")
ANSK = Namespace("https://w3id.org/asbingowl/keys#")
AOI = Namespace ("https://w3id.org/aoi#")
OPM = Namespace("https://w3id.org/opm#")
SCHEMA = Namespace("http://schema.org/")
DOT = Namespace("https://w3id.org/dot#")
INST = Namespace("https://asbingowl.org/TwinGenDemo/BW452#")
PROPS = Namespace("http://lbd.arch.rwth-aachen.de/props#")
SIBINST =Namespace("http://example.org/sibbw7936662#")

"""
def connect(database_name):
    graph = Graph()
    graph.parse(database_name, format = "turtle")
    return graph
"""

def query_tbw(sibbw_graph):
    tbw_list = []
    query_tbw = prepareQuery("""
        SELECT DISTINCT ?Teilbauwerk 
        WHERE{
            ?Teilbauwerk a asb:Teilbauwerk .
        }
        """)
    for i in sibbw_graph.query(query_tbw):
        tbw_list.append(i[0].partition('#')[-1])
    return tbw_list

def get_bauteildefinition(sibbw_graph):
    btd_list = []
    query_btd = prepareQuery("""
        SELECT DISTINCT ?Bauteildefinition
        WHERE{
            ?Bauteildefinition a asb:ASBING13_BauteilDefinition.
        }
        """, initNs={"asb":ANS})
    for i in sibbw_graph.query(query_btd):
        btd_list.append(i.Bauteildefinition)
    return btd_list

def get_asbbauteil(sibbw_graph):
    ont = Graph()
    ont.parse("https://annegoebels.github.io/asb/core//ontology.ttl")
    g = sibbw_graph + ont
    bt_list = []
    query_btd = prepareQuery("""
        SELECT DISTINCT ?Bauteil 
        WHERE{
            ?Bauteil a  ?Bauteilclass.
            ?Bauteilclass rdfs:subClassOf* asb:AbstraktesBauteil.
        }
        
        """, initNs={"asb":ANS})
    for i in g.query(query_btd):
        bt_list.append(i.Bauteil)
    return bt_list


def get_asbbauteilArt(sibbw_graph, asbBauteil):
    query_btd = prepareQuery("""
        SELECT DISTINCT ?Bauteilclass ?ArtClass ?uArt
        WHERE{
            ?Bauteil a  ?Bauteilclass.
            OPTIONAL {
            ?Bauteil asb:associatedWith ?Art.
            ?Art a ?ArtClass.
            }
            OPTIONAL {
            ?Bauteil asb:Unterbau_Art ?uArt.
            } 
        }

        """, initNs={"asb": ANS})
    for i in sibbw_graph.query(query_btd, initBindings={"Bauteil":asbBauteil}):
        return i



def get_schadenObjekte(sibbw_graph):
    sO_list = []
    query_sO= prepareQuery("""
        SELECT DISTINCT ?schadenObj
        WHERE {
            ?schadenObj a asb:SchadenObjekt.
        }
        """, initNs={"asb":ANS})
    for i in sibbw_graph.query(query_sO):
        sO_list.append(i.schadenObj)
    return sO_list

"""
    def get_schadenObjekte(sibbw_graph):
    graph = connect(sibbw_graph)
    sO_list = []
    query_sO= prepareQuery("
        prefix : <http://example.org/sibbw7936662#>
        prefix aoi: <https://w3id.org/aoi#>
       prefix asb: <https://w3id.org/asbingowl/core#>
        prefix asbkey: <https://w3id.org/asbingowl/keys#>
        prefix asbkey13: <https://w3id.org/asbingowl/keys/2013#>
        prefix xsd: <http://www.w3.org/2001/XMLSchema#>
        SELECT DISTINCT ?schadenObjekte
        WHERE{
            ?schadenObjekte a asb:SchadenObjekt.
        }
        ")
    for i in graph.query(query_sO):
        sO_list.append(i[0])
    return sO_list
 """


def query_schaden(sibbw_graph,schadenObjekt):
    schaden_dic = {}
    bauteildefinition_query = prepareQuery("""
    SELECT DISTINCT ?bauteildefinition ?aoiInst ?bauteiltyp 
    WHERE{
         ?schadObj a asb:SchadenObjekt;
                   asb:hatBauteilDefinition ?bauteildefinition.
         OPTIONAL{
         ?aoiInst aoi:locatesDamage ?schadObj.
         }
         OPTIONAL{
         ?bauteildefinition  asb:BauteilTypInIfc ?bauteiltyp
         }
    }
    """, initNs={"asb":ANS, "aoi":AOI})
    for i in sibbw_graph.query(bauteildefinition_query, initBindings={"schadObj":schadenObjekt}):
        schaden_dic["Bauteildefinition"] = i.bauteildefinition
        schaden_dic["AOI"] = i.aoiInst
        schaden_dic["Bauteiltyp"] = i.bauteiltyp

    return schaden_dic

"""
def query_schaden_btd(sibbw_graph,schadenObjekt):
    bauteildefinition_query = prepareQuery("
    SELECT ?bauteildefinition
    WHERE{
        ?schadObj a asb:SchadenObjekt ;
                  asb:hatBauteilDefinition ?bauteildefinition.

    }
    ", initNs={"asb":ANS})
    for i in sibbw_graph.query(bauteildefinition_query, initBindings={"schadObj":schadenObjekt}):
        return i.bauteildefinition
"""

def query_schaden_aoi(data_filename,schadenObjekt):
    graph = connect(data_filename)
    aoi_dic = {}
    aoi_query = prepareQuery("""
    prefix : <http://example.org/sibbw7936662#> 
    prefix aoi: <https://w3id.org/aoi#> 
    prefix asb: <https://w3id.org/asbingowl/core#> 
    prefix asbkey: <https://w3id.org/asbingowl/keys#> 
    prefix asbkey13: <https://w3id.org/asbingowl/keys/2013#> 
    prefix xsd: <http://www.w3.org/2001/XMLSchema#> 
    SELECT DISTINCT ?aoi
    WHERE{

        ?aoi aoi:locatesDamage <""" + str(schadenObjekt) + """>
    }
    """)
    for i in graph.query(aoi_query):
        aoi_dic["AOI"] = i[0]

    return aoi_dic

def query_bauteildefinition(sibbw_graph, bauteildefinition):

    dictionary = {}
    list_bauteil = []
    list_bauteilgruppe = []
    list_konstruktionsteil = []
    list_teilbauwerk = []
    list_ortsangabe = []
    list_abst_anz = []
    q1 = prepareQuery("""
    SELECT  ?Teilbauwerk ?Bauteil ?Bauteilgruppe ?Konstruktionsteil 
    WHERE {
        ?bdef a asb:ASBING13_BauteilDefinition;
                asb:associatedWith ?Teilbauwerk .
        OPTIONAL{?bdef
                    asb:ASBING13_Bauteil ?Bauteil. }
        OPTIONAL{?bdef       
                    asb:ASBING13_Bauteilgruppe ?Bauteilgruppe. }
        OPTIONAL{?bdef
                    asb:ASBING13_Konstruktionsteil ?Konstruktionsteil. }
    }
    """, initNs={"asb":ANS})
    for i in sibbw_graph.query(q1, initBindings={"bdef":bauteildefinition}):
        list_bauteil.append(i.Bauteil)
        list_bauteilgruppe.append(i.Bauteilgruppe)
        list_konstruktionsteil.append(i.Konstruktionsteil)
        list_teilbauwerk.append(i.Teilbauwerk)

    q5 = prepareQuery(""" 
    SELECT  ?Ortsangabe 
    WHERE {
        ?bdef a asb:ASBING13_BauteilDefinition;
               asb:Schaden_Ortsangabe [asb:Ortsangabe_Ortsangabe ?Ortsangabe].
    }
    """, initNs={"asb":ANS})
    for i in sibbw_graph.query(q5, initBindings={"bdef":bauteildefinition}):
        list_ortsangabe.append(str(i[0]))     
    q6 = prepareQuery("""
    SELECT  ?Abstand_Anzahl
    WHERE {
        ?bdef a asb:ASBING13_BauteilDefinition;
             asb:Schaden_Ortsangabe [asb:Ortsangabe_GroesseOrtsangabe [asb:AbstandAnzahl_Anzahl ?Abstand_Anzahl]] .
    }
    """, initNs={"asb":ANS})
    for i in sibbw_graph.query(q6, initBindings={"bdef":bauteildefinition}):
        list_abst_anz.append(str(i[0]))    
    j= 0
    while True:       
        if j == len(list_bauteil):
                break
        for i in list_bauteil:
            dictionary["Bauteil_0"] = list_bauteil[0]
            if list_bauteil[j]==list_bauteil[j-1]:
                continue
            else:
                dictionary["Bauteil_"+str(j)] = i
        j = j + 1
    j = 0
    while True:       
        if j == len(list_bauteilgruppe):
                break
        for i in list_bauteilgruppe:
            dictionary["Bauteilgruppe_0"] = list_bauteilgruppe[0]
            if list_bauteilgruppe[j]==list_bauteilgruppe[j-1]:
                continue
            else:
                dictionary["Bauteilgruppe_"+str(j)] = i
        j = j + 1
    j = 0
    while True:       
        if j == len(list_konstruktionsteil):
                break
        for i in list_konstruktionsteil:
            dictionary["Konstruktionsteil_0"] = list_konstruktionsteil[0]
            if list_konstruktionsteil[j]==list_konstruktionsteil[j-1]:
                continue
            else:
                dictionary["Konstruktionsteil_"+str(j)] = i
        j = j + 1
    j = 0
    while True:       
        if j == len(list_teilbauwerk):
                break
        for i in list_teilbauwerk:
            dictionary["Teilbauwerk_0"] = list_teilbauwerk[0]
            if list_teilbauwerk[j]==list_teilbauwerk[j-1]:
                continue
            else:
                dictionary["Teilbauwerk_"+str(j)] = i
        j = j + 1
    j = 0
    while True:       
        if j == len(list_ortsangabe):
                break
        for i in list_ortsangabe:
            dictionary["Ortsangabe_"+str(j)] = i
            j = j+1  
    j = 0
    while True:       
        if j == len(list_abst_anz):
                break
        for i in list_abst_anz:
            dictionary["Abstand_Anzahl_0"] = list_abst_anz[0]
            if list_abst_anz[j]==list_abst_anz[j-1]:
                continue
            else:
                dictionary["Abstand_Anzahl_"+str(j)] = i
        j = j + 1

    return dictionary

def query_bauteildefinition_hasModelRepresentation(sibbw_graph,bauteildefinition):

    list_inst = []
    inst_query = prepareQuery("""
        SELECT DISTINCT  ?lbd_inst
        WHERE{
             ?bauteildefinition  asb:hasModelRepresentation | asb:beschreibtBauteil/asb:hasModelRepresentation ?lbd_inst.
        }
        """, initNs={"asb": ANS})
    for i in sibbw_graph.query(inst_query, initBindings={"bauteildefinition": bauteildefinition}):
        list_inst.append(i.lbd_inst)

    return list_inst

def query_bauteildefinition_bauteilTyp(sibbw_graph,bauteildefinition):
    BauteilTyp = "Proxy"
    q1 = prepareQuery("""
    SELECT ?BT_Typ
    WHERE{
         a asb:ASBING13_BauteilDefinition .
         asb:BauteilTypInIfc ?BT_Typ.
    }
    """)
    for i in graph.query(q1):
        BauteilTyp = i[0]    
    return BauteilTyp


def query_aoi_Classes(sibbw_graph,aoi_inst):
    aoi_Class_list = []
    query_aoi = prepareQuery("""
    SELECT DISTINCT ?aoiClass
    WHERE{
       ?aoiInst a ?aoiClass .
    }
    """)
    for i in sibbw_graph.query(query_aoi, initBindings={"aoiInst":aoi_inst}):
        aoi_Class_list.append(i.aoiClass)

    return aoi_Class_list

def add_hasModelRepresentation(data_filename,bauteilId,bauteildefinition):
    g = Graph()
    g.parse(data_filename)
    asb =Namespace("https://w3id.org/asbingowl/core#")
    inst =Namespace("https://asbingowl.org/TwinGenDemo/BW452#")
    g.bind("inst",inst)
    g.bind("asb",asb)
    bauteildefinition_ref  = URIRef(bauteildefinition)
    g.add((bauteildefinition_ref,asb.hasModelRepresentation,(URIRef(bauteilId))))
    g.serialize(destination=data_filename)

def add_BauteilTyp(data_filename,bauteilTyp,bauteildefinition):
    g = Graph()
    g.parse(data_filename)
    asb =Namespace("https://w3id.org/asbingowl/core#")
    g.bind("asb",asb)
    bauteildefinition_ref  = URIRef(bauteildefinition)
    g.add((bauteildefinition_ref,asb.BauteilTyp,Literal(bauteilTyp)))
    g.serialize(destination=data_filename)

def get_Ortsangabe(qbtd):
    with open(r".\temp_files\map_damage_location.json", "r") as file:
        map_damage_location = json.loads(file.read())
    dictionary_oa = {}
    dictionary_tesBauteil = {}
    dictionary_Feld = {}
    dictionary_links_rechts = {}
    dictionary_anfang_ende = {}
    count = 0
    if "Abstand_Anzahl" in str(qbtd.keys()):
        for i in qbtd.keys():   
            if "Abstand_Anzahl" in i:
                count = count + 1
        i = 0
        while True:   
            dictionary_oa[str(i)] = qbtd["Abstand_Anzahl_"+str(i)]  
            OA = qbtd["Ortsangabe_"+str(i)]
            OA_map = map_damage_location[OA]
            dictionary_oa[str(i)] = str(dictionary_oa[str(i)])+ str(OA_map) 
            del qbtd["Abstand_Anzahl_"+str(i)]
            del qbtd["Ortsangabe_"+str(i)]
            i = i + 1
            if i == count:
                break
    if "Ortsangabe" and not "Abstand_Anzahl" in str(qbtd.keys()):    
        count_2 = count
        for i in qbtd.keys():
            if "Ortsangabe" in i:
                OA = qbtd["Ortsangabe_"+str(count_2)]
                OA_map = map_damage_location[OA]
                dictionary_oa[str(count_2)] = str(OA_map) 
                count_2 = count_2 + 1            
    j = 0
    for i in list(dictionary_oa):
        if "BauteilVon" in dictionary_oa[i]:
            dictionary_tesBauteil[j] = dictionary_oa[i]
            dictionary_oa.pop(i)
    for i in list(dictionary_oa):
        if "Feld" in dictionary_oa[i]:
            dictionary_Feld[j] = dictionary_oa[i]
            dictionary_oa.pop(i)
    for i in list(dictionary_oa):
        if "Control_EndeDesBauwerks" in dictionary_oa[i]  or  "Control_AnfangDesBauwerks" in dictionary_oa[i] or "Control_beideWiderlager" in dictionary_oa[i]:
            dictionary_anfang_ende[str(j)] = dictionary_oa[i]
            dictionary_oa.pop(i)
    j = 0
    for i in list(dictionary_oa):
        if "Rechts"in dictionary_oa[i]  or "Links" in dictionary_oa[i] or "Control_rundl" in dictionary_oa[i]:
            dictionary_links_rechts[j] = dictionary_oa[i]
            dictionary_oa.pop(i)
            j = j + 1


    return dictionary_oa, dictionary_tesBauteil, dictionary_Feld, dictionary_links_rechts, dictionary_anfang_ende

def create_AOI(data_filename,schadenObjekt):
    g = Graph()
    g.parse(data_filename)

    INS = Namespace("http://example.org/sibbw7936662#")
    AOI = Namespace("https://w3id.org/aoi#")

    g.bind("", INS)
    g.bind("aoi",  AOI)   

    aoi_ref  = str(random.randint(1000000,9999999))+"_AOI"
    print("New AOI: "+str(aoi_ref))
    g.add((URIRef(INS + aoi_ref),AOI.locatesDamage,URIRef(schadenObjekt)))
    g.serialize(destination=data_filename)

def add_AOI(data_filename,aoi_ref,key,new_aoi):
    g = Graph()
    g.parse(data_filename)

    INS = Namespace("http://example.org/sibbw7936662#")
    ANS = Namespace("https://w3id.org/asbingowl/core#")
    AONS = Namespace("https://w3id.org/asbingowl/keys/2013#")
    ANSK = Namespace("https://w3id.org/asbingowl/keys#")
    AOI = Namespace("https://w3id.org/aoi#")

    map = {"INS":INS,"ANSK": ANSK,"AONS":AONS,"ANS":ANS,"AOI":AOI }

    g.bind("", INS)
    g.bind("owl", OWL)
    g.bind("asb", ANS)
    g.bind("asbkey13",  AONS)
    g.bind("asbkey",  ANSK)
    g.bind("aoi",  AOI)   

    g.add((URIRef(INS + aoi_ref),RDF.type,URIRef(map[key] + new_aoi)))
    g.serialize(destination=data_filename)

def query_instance(lbd_ifc_graph,GlobalId):
    q1 = prepareQuery("""
    SELECT ?inst
    WHERE {
        ?inst props:globalIdIfcRoot ?globalIdIfcRoot.
        ?globalIdIfcRoot schema:value ?GlobalId .        
    }
    """, initNs={"props":PROPS, "schema":SCHEMA})
    for i in lbd_ifc_graph.query(q1, initBindings={"GlobalId":Literal(GlobalId)}):
        ifc_lbd_inst = i.inst

    return  ifc_lbd_inst


def get_beschreibtBauteil(sibbw_graph,bauteildefinition):
    list_bauteil = []
    list_bauteilarten = []
    # hier auch bauteilgruppe von bdef querien
    q1 = prepareQuery("""
    SELECT DISTINCT ?konTeil ?btgrp ?asbBauteil ?asbBauteilClass ?asbBauteilart ?asbBauteilartClass ?FrzR_Art ?Unterbau_Art ?einfacheArt
    WHERE{
        ?bdef a asb:ASBING13_BauteilDefinition.
        
        OPTIONAL{
         ?bdef asb:ASBING13_Konstruktionsteil ?konTeil.}
         
        OPTIONAL{
        ?bdef asb:ASBING13_Bauteilgruppe ?btgrp. }
        
        OPTIONAL{
        ?bdef asb:beschreibtBauteil ?asbBauteil.
        ?asbBauteil a ?asbBauteilClass.
        
        OPTIONAL{
        ?asbBauteil asb:Unterbau_Art ?Unterbau_Art .
        }
        
        OPTIONAL{
        ?asbBauteil asb:associatedWith ?asbBauteilart.
        ?asbBauteilart a ?asbBauteilartClass. 
        
        OPTIONAL{
        ?asbBauteilart asb:FahrzeugRueckhaltesystem_Art [ asb:ArtFahrzeugRueckhaltesystem_Systembezeichnung [ asb:Systembezeichnung_Bezeichnung  ?FrzR_Art] ] 
        }
        OPTIONAL{
        ?asbBauteilart asb:EinfacheBauteilart_Art  ?einfacheArt.
        }
        }  
        } 
    }
    """, initNs={"asb":ANS})
    for i in sibbw_graph.query(q1, initBindings={"bdef":bauteildefinition}):
        #print(len(i))
        count = 0
        for a in i:
            #print(a)
            count += 1
            if a is not None:
                if a == i.asbBauteil:
                    list_bauteil.append(a)
                else:
                    list_bauteilarten.append(a)

            if count == len(i):
                break
    #print(list_bauteil)
    #print(list_bauteilarten)
    cleanBauteilList = list(dict.fromkeys(list_bauteil))
    cleanBauteilartlist = list(dict.fromkeys(list_bauteilarten))
    #print(cleanBauteilList)
    #print(cleanBauteilartlist)

    return cleanBauteilList, cleanBauteilartlist

def get_einbauort (asbBauteil, sibbw_graph):
    rechts_links = {}
    anfang_ende = {}
    q1 = prepareQuery("""
       SELECT ?einbauort
       WHERE {
       ?asbBauteil asb:AbstraktesBauteil_Einbauort ?einbauort.
       }
    """, initNs={"asb":ANS})
    for ort in sibbw_graph.query(q1, initBindings={"asbBauteil":asbBauteil}):
        print(ort.einbauort)
        ortsangabe = ort.einbauort
        if "West" in ortsangabe:
            rechts_links["0"]= "Rechts"
        if "Ost" in ortsangabe:
            rechts_links["0"] = "Links"
        if "10" in ortsangabe:
            anfang_ende["0"]= "Control_AnfangDesBauwerks"
        if "30" in ortsangabe:
            anfang_ende["0"]= "Control_EndeDesBauwerks"
        if "Linke" in ortsangabe:
            rechts_links["0"] = "Links"
        if "Rechte" in ortsangabe:
            rechts_links["0"]= "Rechts"
        if "Lagerreihe" in ortsangabe:
            rechts_links = ortsangabe
        #else:
        #    print("no interpretable location description found")

    return rechts_links, anfang_ende




def get_ifcBridgeName(sibbw_graph, bauteildefinition):
    bauteil_list, bauteilarten_list = get_beschreibtBauteil(sibbw_graph, bauteildefinition)
    #print(bauteil_list, bauteilarten_list)

    bauteilTyp_list = []

    for j in bauteilarten_list:
        if "Bruecke" in str(j) or "Teilbauwerk" in str(j) or "Fahrzeug" in str(j) or "[]" in str(j):
            pass
        elif j not in bauteilTyp_list:
            bauteilTyp_list.append(j)

    return bauteilTyp_list, bauteil_list

def get_GlobalId(lbd_graph,inst):

    q1 = prepareQuery("""
    SELECT ?globalId
    WHERE{
        ?inst props:globalIdIfcRoot ?globalIdIfcRoot.
        ?globalIdIfcRoot schema:value ?globalId.
    }
    """, initNs={"props":PROPS, "schema":SCHEMA})
    for i in lbd_graph.query(q1, initBindings={"inst":inst}):
        globalId =i.globalId

        return globalId

def get_Schaden_Desc (sibbwgraph, SchadenObjektName):
    test = []
    SchadenObjekt = URIRef(SIBINST + SchadenObjektName[:21] )
    #print(SchadenObjekt)
    q1 = prepareQuery("""
    SELECT DISTINCT  ?schadenArt ?size 
    WHERE {
    ?schadenobj asb:hatPruefDokumentation ?schaden.
    ?schaden dot:coveredInInspection ?pruf. 
    ?pruf asb:PruefungUeberwachung_Status asbkey:StatusPruefung_abgeschlossen . 
    ?schaden asb:Schaden_Schaden ?schadenArt;
             asb:Schaden_AllgemeineMengenangabe ?size. 
    }
    """,initNs={"asb":ANS, "dot":DOT, "asbkey":ANSK})

    q2 = prepareQuery("""
    SELECT DISTINCT  ?schadenArt ?size 
    WHERE {
    ?schadenobj asb:hatPruefDokumentation ?schaden.
    ?schaden asb:Schaden_Schaden ?schadenArt;
             asb:Schaden_AllgemeineMengenangabe ?size. 
    }
    LIMIT 1
    """, initNs={"asb": ANS, "dot": DOT, "asbkey": ANSK})


    for res in sibbwgraph.query(q1, initBindings={"schadenobj":SchadenObjekt}):
        art = str(res.schadenArt)
        grs = str(res.size)
        Desc = "Damage Type: "+ art +"\n"+"Damage Size: "+grs
        #print(Desc)
        test.append(res)
        return Desc

    if len(test) == 0:
        for res2 in sibbwgraph.query(q2, initBindings={"schadenobj": SchadenObjekt}):
            #print(res2)
            art = str(res2.schadenArt)
            grs = str(res2.size)
            Desc2 = "Damage Type: " + art + "\n" + "Damage Size: " + grs
            #print(Desc2)
            return Desc2