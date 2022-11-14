# Conversion of implicit textual damage locations of bridge inspection data in geometrical representations using Linked Data
In this project, an approach was created to automatically convert textual damage information into geometrical representations using Linked Data. The project bases on the definitions of the ASB-ING (basis for collecting and managing bridge inspection data in Germany) and  works with data which has been entered in the database application "SIB-Bauwerke".

## Requirements:
- Damage inspection information converted into Turtle file (.ttl)
- IFC model of bridge (.ifc)
- IFC model of bridge converted into LBD format (.ttl)

## Procedure:
Run file "main"

ouput:
   - BCF file with damages in form of issues 
   - IFC file with point representation of damages
   - create links between inspection and ifc files
     (on element, damage area, and damage representation level)