import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

doc =  DocumentManager.Instance.CurrentDBDocument

clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)

clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import *
#--------------------------------------------------------------#
results = []

#The inputs to this node will be stored as a list in the IN variables.
dataEnteringNode = IN
x = IN[0]
y = IN[1]

#If the Bool input is True at IN[1] then remove Materials
if x:
	theMaterials = (
		FilteredElementCollector(doc)
		.OfCategory(BuiltInCategory.OST_Materials)
		.ToElementIds()
		)
	results.Add('Deleted ' + str(theMaterials.Count) + ' Materials')
	if theMaterials.Count > 0:
		try:
			TransactionManager.Instance.EnsureInTransaction(doc)
			doc.Delete(theMaterials)
			TransactionManager.Instance.TransactionTaskDone()
		except Exception as e:
			results.Add(e.message)
			pass
else:
	results.Add('Materials Not Selected')	
	
#If the Bool input is True at IN[2] then remove Appearance Assets
if y:
	theAppearanceAssets = (
		FilteredElementCollector(doc)
		.OfClass(AppearanceAssetElement)
		.ToElementIds()
		)
	results.Add('Deleted ' + str(theAppearanceAssets.Count) + ' Appearance Assets')
	if theAppearanceAssets.Count > 0:
		try:
			TransactionManager.Instance.EnsureInTransaction(doc)
			doc.Delete(theAppearanceAssets)
			TransactionManager.Instance.TransactionTaskDone()
		except Exception as e:
			results.Add(e.message)
			pass
else:
	results.Add('AppearanceAssets Not Selected')
#Assign your output to the OUT variable.
OUT = results