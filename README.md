# Brat Annotation Evaluation

In this project, we compare different annotations for protest data. Annotations are including entities: "source" , "target", "location", "material_cooperation", "verbal_cooperation", and "verbal_conflict"; relations: "srcAct" , "actTar". 

In the ```main.py``` code, you can change the "path2folder" to the folder that includes your annotation folders. Besides, you can compare the annotations partially or exactly by changing "matchingType" to "Exact" or "Partial". If you use "Partial", you can select the percent of "threshold" for partal string matching. Its defualt is 75 (percent). 
