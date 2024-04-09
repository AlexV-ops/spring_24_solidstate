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
    
    main_df['Electronegativity difference (Pauling scale)'] = main_df['A'].map(NewElem.set_index('Symbol')['Pauling_Electronegativity']) - main_df['B'].map(NewElem.set_index('Symbol')['Pauling_Electronegativity']) #blue
    main_df['Electronegativity difference (Martynov-Batsanov scale)'] = main_df['A'].map(NewElem.set_index('Symbol')['MBelectonegativity']) - main_df['B'].map(NewElem.set_index('Symbol')['MBelectonegativity']) #red
    main_df['Electronegativity difference (Gordy scale)'] = main_df['A'].map(NewElem.set_index('Symbol')['Gordyelectonegativity']) - main_df['B'].map(NewElem.set_index('Symbol')['Gordyelectonegativity']) #blue
    main_df['Electronegativity difference (Mulliken scale)'] = main_df['A'].map(NewElem.set_index('Symbol')['MullinkeEN']) - main_df['B'].map(NewElem.set_index('Symbol')['MullinkeEN']) #blue
    main_df['Electronegativity difference (Allred-Rochow scale)'] = main_df['A'].map(NewElem.set_index('Symbol')['AllenEN']) - main_df['B'].map(NewElem.set_index('Symbol')['AllenEN']) #red

    main_df['Mean electronegativity (Pauling scale)'] = (main_df['A'].map(NewElem.set_index('Symbol')['MullinkeEN']) + main_df['B'].map(NewElem.set_index('Symbol')['MullinkeEN']))/2 #blue
    main_df['Mean electronegativity (Martynov-Batsanov scale)'] = (main_df['A'].map(NewElem.set_index('Symbol')['MBelectonegativity']) + main_df['B'].map(NewElem.set_index('Symbol')['MBelectonegativity']))/2 #red
    main_df['Mean electronegativity (Gordy scale)'] = (main_df['A'].map(NewElem.set_index('Symbol')['Gordyelectonegativity']) + main_df['B'].map(NewElem.set_index('Symbol')['Gordyelectonegativity']))/2 #red
    main_df['Mean electronegativity (Mulliken scale)'] = (main_df['A'].map(NewElem.set_index('Symbol')['MullinkeEN']) + main_df['B'].map(NewElem.set_index('Symbol')['MullinkeEN']))/2 #red
    main_df['Mean electronegativity (Allred-Rochow scale)'] = (main_df['A'].map(NewElem.set_index('Symbol')['AllenEN']) + main_df['B'].map(NewElem.set_index('Symbol')['AllenEN']))/2 #red

    main_df['Ionic character (Martynov-Batsanov scale)'] = (1 - np.exp(-0.25 * (main_df['A'].map(NewElem.set_index('Symbol')['MBelectonegativity']) - main_df['B'].map(NewElem.set_index('Symbol')['MBelectonegativity'])) ** 2)) #red
    
    main_df['Sum of valence electrons'] = main_df['A'].map(NewElem.set_index('Symbol')['numberofvalenceelectrons']) + main_df['B'].map(NewElem.set_index('Symbol')['numberofvalenceelectrons']) #blue

    main_df['Atomic number sum'] = main_df['A'].map(NewElem.set_index('Symbol')['Atomic_Number']) + main_df['B'].map(NewElem.set_index('Symbol')['Atomic_Number']) #blue
        
    main_df['Atomic radius ratio'] = (main_df['A'].map(NewElem.set_index('Symbol')['AtomicRadus']) / main_df['B'].map(NewElem.set_index('Symbol')['AtomicRadus'])) #red

    main_df['Covalent radius sum'] = main_df['A'].map(NewElem.set_index('Symbol')['Covalent_Radius']) + main_df['B'].map(NewElem.set_index('Symbol')['Covalent_Radius']) #blue
    
    main_df['Covalent radius ratio'] = (main_df['A'].map(NewElem.set_index('Symbol')['Covalent_Radius']) / main_df['B'].map(NewElem.set_index('Symbol')['Covalent_Radius'])) #blue
    main_df['2 x covalent radius difference'] = 2 * (main_df['A'].map(NewElem.set_index('Symbol')['Covalent_Radius']) + main_df['B'].map(NewElem.set_index('Symbol')['Covalent_Radius'])) #blue

    main_df['Atomic weight sum'] = main_df['A'].map(NewElem.set_index('Symbol')['Atomic_Weight']) + main_df['B'].map(NewElem.set_index('Symbol')['Atomic_Weight']) #blue

    main_df['Zunger radius sum ratio'] = (main_df['A'].map(NewElem.set_index('Symbol')['zungerradiisum']) / main_df['B'].map(NewElem.set_index('Symbol')['zungerradiisum'])) #red
    main_df['2 x Zunger radius sum difference'] = 2 * (main_df['A'].map(NewElem.set_index('Symbol')['zungerradiisum']) - main_df['B'].map(NewElem.set_index('Symbol')['zungerradiisum'])) #red
    main_df['Ionic radius ratio'] = (main_df['A'].map(NewElem.set_index('Symbol')['ionicradius']) / main_df['B'].map(NewElem.set_index('Symbol')['ionicradius'])) #red
    main_df['2 x Ionic radius difference'] = 2 * (main_df['A'].map(NewElem.set_index('Symbol')['ionicradius']) - main_df['B'].map(NewElem.set_index('Symbol')['ionicradius'])) #red

    main_df['Crystal radius sum'] = main_df['A'].map(NewElem.set_index('Symbol')['crystalradius']) + main_df['B'].map(NewElem.set_index('Symbol')['crystalradius']) #blue
    main_df['Crystal radius ratio'] = (main_df['A'].map(NewElem.set_index('Symbol')['crystalradius']) / main_df['B'].map(NewElem.set_index('Symbol')['crystalradius'])) #blue
    main_df['2 x Crystal radius difference'] = 2 * (main_df['A'].map(NewElem.set_index('Symbol')['crystalradius']) - main_df['B'].map(NewElem.set_index('Symbol')['crystalradius'])) #blue

    main_df['Period number difference'] = main_df['A'].map(NewElem.set_index('Symbol')['Period']) - main_df['B'].map(NewElem.set_index('Symbol')['Period']) #blue

    main_df['Group number sum'] = main_df['A'].map(NewElem.set_index('Symbol')['group']) + main_df['B'].map(NewElem.set_index('Symbol')['group']) #red
    main_df['Group number difference'] = main_df['A'].map(NewElem.set_index('Symbol')['group']) - main_df['B'].map(NewElem.set_index('Symbol')['group']) #blue

    main_df['Family number sum'] = main_df['A'].map(NewElem.set_index('Symbol')['families']) + main_df['B'].map(NewElem.set_index('Symbol')['families']) #red

    main_df['Quantum number (l) sum'] = main_df['A'].map(NewElem.set_index('Symbol')['lquantumnumber']) + main_df['B'].map(NewElem.set_index('Symbol')['lquantumnumber'])#blue
    main_df['Quantum number (l) difference'] = main_df['A'].map(NewElem.set_index('Symbol')['lquantumnumber']) - main_df['B'].map(NewElem.set_index('Symbol')['lquantumnumber']) #blue

    return main_df
    
features_df = compute_features(compositions['composition'])

features_df.to_excel('AntonDescriptorsForBinary_redblue.xlsx', index=False)
