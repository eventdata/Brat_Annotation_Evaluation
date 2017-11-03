# Brat Annotation Evaluation

In this project, we compare different annotations for protest data. Annotations are including entities: "source" , "target", "location", "material_cooperation", "verbal_cooperation", and "verbal_conflict"; relations: "srcAct" , "actTar". 

In the ```main.py``` code, you can change the "path2folder" to the folder that includes your annotation folders. Besides, you can compare the annotations partially or exactly by changing "matchingType" to "Exact" or "Partial". If you use "Partial", you can select the percent of "threshold" for partal string matching. Its defualt is 75 (percent). 


ReadAnnotations.py

```Ann2Json(fileName)```

This function reads the annotation “fileName” and stores the data in the JSON format. 
If the line starts with “T”, it means it is an entity; and if it starts with “R”, it means it is a relation, like “actTar” and “srcAct”. 

If the annotation is an entity, the line includes tag name, start index, end index and a phrase (one or more words).
For example: 
T1	source 74 108	Comunidades indígenas y campesinas

If phrase is not a consequence of words (i.e. the annotator selected words from different part of a sentence), the line includes tag name, start and end indexed of the first sequence of words; start and end indexes of second sequence of words; …  and phrase.

For example: 
T8	source 363 437;439 452	El vicepresidente de la Confederación de Nacionalidades Indígenas (CONAIE) Rafael Pandam


If the  annotation is a relation, the line includes tag name, Arg1 which is the first entity and Arg2 which is the second entity.

For example: 
R8	srcAct Arg1:T17 Arg2:T19	


```EntityExactMatching(tag, goldJson, annotatorJson)```

I compare the two JSON files with each other with exact matching method. The input of this function is tag name, gold stardard JSON file and annotation JSON file. Here tag names are entity names: “source”, “target”, “location”,  etc. 

This function compares all of the annotations for each tag name. The reference data is goldJson. If annotation in goldJson and annotatorJson are exactly same, the true positive will increase by one and that annotation will be removed from both  goldJson and annotatorJson. At the end of the process, the remaining annotations in the goldJson list are false negative (fn), which means the true annotations that annotator did not tag them. The remaining annotations in the annotatorJson list are false positive (fp), which means the false annotations that annotator tag them by mistake. Then, recall, precision and f-score can be computed by the following formulas. 
 
Recall = tp / (tp + fn)
Precision = tp / (tp + fp)
f_score = (2 * Recall * Precision) / (Recall + Precision)

In this comparison, since there may be several entity with the same name in different part of the text, I also consider their start and end indexes of the words. As an example of this case: 
T2	location 48 55	BELFAST
T3	location 37 44	BELFAST

But if the if the entity phrase name contains non-consequence words and has several start and end indexes, I just compare the phrases with the gold standard phrases to find the similar phrase. 

```EntityPartialMatching(tag, goldJson, annotatorJson, threshold)```

This function is very similar to the previous function, but it needs “ threshold” in the input. In this function if the similarity between gold standard phrase and annotator phrase is more than  threshold, then I consider them true positive (tp) and remove them from gold standard list and annotator list. Finding fp and fn is similar to the previous function. 

```RelationExactMatching(tag, goldJson, annotatorJson)```

I compare the two JSON files with each other with exact matching method. The input of this function is tag name, gold stardard JSON file and annotation JSON file. Here tag names are relation names: “srcAct” , “actTar”. 

To compare two relations, we need to compare both Arg1 and Arg2 in gold and annotator JSON together. 


```RelationPartialMatching(tag, goldJson, annotatorJson, threshold)```

This function is very similar to the previous function. However, we need to select the threshold for Arg1 and Arg2 comparison. 


```Main.py ```

This program has the main function and you need to set “Exact” or “Partial” matching, “threshold” and folderPath of the annotation folders. In every round, it will automatically select one folder as a gold standard and compare it with the other folders. Then, it will compute average of precision, recall, and f-score for each entity and relation type and overall for each gold standard annotation.
