import numpy as np
import pandas as pd
import re
import math

NewElem = pd.read_excel('elementdata_new.xlsx')
NewElem = NewElem.replace({"^\s*|\s*$":""}, regex=True)
NewElem.columns = NewElem.columns.str.replace(' ','')
NewElem.columns = NewElem.columns.str.replace('[\n]', '')

List_A = ["Sc", "Y", "La", "Ce", "Pr", "Nd", "Sm", "Eu", "Gd", "Tb", "Dy", "Ho", "Er", "Tm", "Yb", "Lu", "Th", "U"]
List_B = ["Si", "Ga", "Ge", "In", "Sn", "Sb"]

input_file = 'compositions.xlsx'
compositions = pd.read_excel(input_file)

def compute_features(composition):
    Element1 = []
    Composition2 = []
    for s in composition:
        Composition2.append(list(map(lambda x:'1' if x=="" else x, re.findall(r"[A-Z][a-z]*\s*([-*\.\d]*)", s))))
        Element1.append(re.findall(r"[A-Z][a-z]*\s*", s))
        
    for i in range(len(Element1)):
        if Element1[i][0] not in List_A:
            Element1[i][0], Element1[i][1] = Element1[i][1], Element1[i][0]
            Composition2[i][0], Composition2[i][1] = Composition2[i][1], Composition2[i][0]
            
    df1 = pd.DataFrame(Element1, columns=['A', 'B'])
    df2 = pd.DataFrame(Composition2, columns=['Stoichiometry_A', 'Stoichiometry_B'])
    main_df = pd.concat([df1, df2], axis=1)
    
    main_df['Zunger radius sum']  = main_df['A'].map(NewElem.set_index('Symbol')['zunger radii sum']) + main_df['B'].map(NewElem.set_index('Symbol')['zunger radii sum'])
    main_df['Mean Zunger radius sum'] = (main_df['A'].map(NewElem.set_index('Symbol')['zunger radii sum']) + main_df['B'].map(NewElem.set_index('Symbol')['zunger radii sum']))/2
    main_df['Zunger radius sum ratio'] = (main_df['A'].map(NewElem.set_index('Symbol')['zunger radii sum']) / main_df['B'].map(NewElem.set_index('Symbol')['zunger radii sum'])) #red
    main_df['2 x Zunger radius sum difference'] = 2 * (main_df['A'].map(NewElem.set_index('Symbol')['zunger radii sum']) - main_df['B'].map(NewElem.set_index('Symbol')['zunger radii sum'])) #red
    main_df['Zunger radius sum difference'] = main_df['A'].map(NewElem.set_index('Symbol')['zunger radii sum']) - main_df['B'].map(NewElem.set_index('Symbol')['zunger radii sum'])
    
    main_df['Ionic radius sum'] = main_df['A'].map(NewElem.set_index('Symbol')['ionic radius']) + main_df['B'].map(NewElem.set_index('Symbol')['ionic radius'])
    main_df['Mean ionic radius'] = (main_df['A'].map(NewElem.set_index('Symbol')['ionic radius']) + main_df['B'].map(NewElem.set_index('Symbol')['ionic radius']))/2
    main_df['Ionic radius ratio'] = (main_df['A'].map(NewElem.set_index('Symbol')['ionic radius']) / main_df['B'].map(NewElem.set_index('Symbol')['ionic radius'])) #red
    main_df['2 x Ionic radius difference'] = 2 * (main_df['A'].map(NewElem.set_index('Symbol')['ionic radius']) - main_df['B'].map(NewElem.set_index('Symbol')['ionic radius'])) #red
    
    main_df['Crystal radius sum'] = main_df['A'].map(NewElem.set_index('Symbol')['crystal radius']) + main_df['B'].map(NewElem.set_index('Symbol')['crystal radius']) #blue
    main_df['Mean crystal radius'] = (main_df['A'].map(NewElem.set_index('Symbol')['crystal radius']) + main_df['B'].map(NewElem.set_index('Symbol')['crystal radius']))/2
    main_df['Crystal radius ratio'] = (main_df['A'].map(NewElem.set_index('Symbol')['crystal radius']) / main_df['B'].map(NewElem.set_index('Symbol')['crystal radius'])) #blue
    main_df['2 x Crystal radius difference'] = 2 * (main_df['A'].map(NewElem.set_index('Symbol')['crystal radius']) - main_df['B'].map(NewElem.set_index('Symbol')['crystal radius'])) #blue
    
    main_df['Period number sum'] = main_df['A'].map(NewElem.set_index('Symbol')['Period']) + main_df['B'].map(NewElem.set_index('Symbol')['Period'])
    main_df['Mean period number'] = (main_df['A'].map(NewElem.set_index('Symbol')['Period']) + main_df['B'].map(NewElem.set_index('Symbol')['Period']))/2
    main_df['Period number difference'] = main_df['A'].map(NewElem.set_index('Symbol')['Period']) - main_df['B'].map(NewElem.set_index('Symbol')['Period']) #blue
    
    main_df['Group number sum'] = main_df['A'].map(NewElem.set_index('Symbol')['group']) + main_df['B'].map(NewElem.set_index('Symbol')['group']) #red
    main_df['Mean group number'] = (main_df['A'].map(NewElem.set_index('Symbol')['group']) + main_df['B'].map(NewElem.set_index('Symbol')['group']))/2
    main_df['Group number difference'] = main_df['A'].map(NewElem.set_index('Symbol')['group']) - main_df['B'].map(NewElem.set_index('Symbol')['group']) #blue
    
    main_df['Family number sum'] = main_df['A'].map(NewElem.set_index('Symbol')['families']) + main_df['B'].map(NewElem.set_index('Symbol')['families']) #red
    main_df['Mean family number'] = (main_df['A'].map(NewElem.set_index('Symbol')['families']) + main_df['B'].map(NewElem.set_index('Symbol')['families']))/2
    main_df['Family number difference'] = main_df['A'].map(NewElem.set_index('Symbol')['families']) - main_df['B'].map(NewElem.set_index('Symbol')['families'])
    
    main_df['Quantum number (l) sum'] = main_df['A'].map(NewElem.set_index('Symbol')['l quantum number']) + main_df['B'].map(NewElem.set_index('Symbol')['l quantum number'])#blue
    main_df['Mean quantum number (l) mean'] = (main_df['A'].map(NewElem.set_index('Symbol')['l quantum number']) + main_df['B'].map(NewElem.set_index('Symbol')['l quantum number']))/2
    main_df['Quantum number (l) difference'] = main_df['A'].map(NewElem.set_index('Symbol')['l quantum number']) - main_df['B'].map(NewElem.set_index('Symbol')['l quantum number']) #blue
    
    return main_df
    
features_df = compute_features(compositions['composition'])

features_df.to_excel('AntonDescriptorsForBinary_AV.xlsx', index=False)
