#!/usr/bin/env python
# coding: utf-8

import pymatgen as mg
import pandas as pd
import tqdm
import time
import math
import random
import numpy as np
import matplotlib.pyplot as plt
from sklearn import preprocessing, metrics
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, cross_val_score, cross_val_predict, GridSearchCV, ShuffleSplit, KFold
from sklearn.metrics import mean_squared_error,mean_absolute_error
import itertools
from itertools import combinations_with_replacement
from pymatgen import Composition
from pymatgen.entries import  computed_entries
from pymatgen.analysis.phase_diagram import PhaseDiagram, CompoundPhaseDiagram, PDEntry, PDPlotter, Element
from scipy.stats import pearsonr
import warnings
warnings.simplefilter('ignore')

global_feature_cols = ['avg_Composition_Ag', 'avg_Composition_Al', 'avg_Composition_Ar',
       'avg_Composition_As', 'avg_Composition_Au', 'avg_Composition_B',
       'avg_Composition_Ba', 'avg_Composition_Be', 'avg_Composition_Bi',
       'avg_Composition_Br', 'avg_Composition_C', 'avg_Composition_Ca',
       'avg_Composition_Cd', 'avg_Composition_Ce', 'avg_Composition_Cl',
       'avg_Composition_Co', 'avg_Composition_Cr', 'avg_Composition_Cs',
       'avg_Composition_Cu', 'avg_Composition_Dy', 'avg_Composition_Er',
       'avg_Composition_Eu', 'avg_Composition_F', 'avg_Composition_Fe',
       'avg_Composition_Ga', 'avg_Composition_Gd', 'avg_Composition_Ge',
       'avg_Composition_H', 'avg_Composition_He', 'avg_Composition_Hf',
       'avg_Composition_Hg', 'avg_Composition_Ho', 'avg_Composition_I',
       'avg_Composition_In', 'avg_Composition_Ir', 'avg_Composition_K',
       'avg_Composition_Kr', 'avg_Composition_La', 'avg_Composition_Li',
       'avg_Composition_Lu', 'avg_Composition_Mg', 'avg_Composition_Mn',
       'avg_Composition_Mo', 'avg_Composition_N', 'avg_Composition_Na',
       'avg_Composition_Nb', 'avg_Composition_Nd', 'avg_Composition_Ne',
       'avg_Composition_Ni', 'avg_Composition_O', 'avg_Composition_Os',
       'avg_Composition_P', 'avg_Composition_Pb', 'avg_Composition_Pd',
       'avg_Composition_Pm', 'avg_Composition_Pr', 'avg_Composition_Pt',
       'avg_Composition_Rb', 'avg_Composition_Re', 'avg_Composition_Rh',
       'avg_Composition_Ru', 'avg_Composition_S', 'avg_Composition_Sb',
       'avg_Composition_Sc', 'avg_Composition_Se', 'avg_Composition_Si',
       'avg_Composition_Sm', 'avg_Composition_Sn', 'avg_Composition_Sr',
       'avg_Composition_Ta', 'avg_Composition_Tb', 'avg_Composition_Tc',
       'avg_Composition_Te', 'avg_Composition_Th', 'avg_Composition_Ti',
       'avg_Composition_Tl', 'avg_Composition_Tm', 'avg_Composition_U',
       'avg_Composition_V', 'avg_Composition_W', 'avg_Composition_Xe',
       'avg_Composition_Y', 'avg_Composition_Yb', 'avg_Composition_Zn',
       'avg_Composition_Zr', 'avg_ Atomic_Number', 'avg_ Atomic_Weight',
       'avg_Period', 'avg_group', 'avg_families', 'avg_Mendeleev Number',
       'avg_Atomic Radus', 'avg_ Covalent_Radius', 'avg_Zunger radii sum',
       'avg_ionic radius', 'avg_crystal radius',
       'avg_ Pauling_Electronegativity', 'avg_MB electonegativity',
       'avg_Gordy electonegativity', 'avg_Mullinke EN','avg_Allred-Rockow electronegativity', 'avg_metallic valence',
       'avg_number of valence electrons',
       'avg_gilmor number of valence electron', 'avg_valence s',
       'avg_valence p', 'avg_valence d', 'avg_outer shell electrons',
       'avg_1st ionization potential (kJ/mol)', 'avg_polarizability\n(A^3)',
       'avg_Melting point (K)', 'avg_Boiling Point (K)', 'avg_Density (g/mL)',
       'avg_specific heat (J/g K) ', 'avg_heat of fusion (kJ/mol) ',
       'avg_heat of vaporization (kJ/mol) ',
       'avg_thermal conductivity (W/(m K)) ', 'avg_heat atomization\n(kJ/mol)',
       'avg_Cohesive energy', 'avg_electron affinity (kJ/mol)',
       'diff_ Atomic_Number', 'diff_ Atomic_Weight', 'diff_Period',
       'diff_group', 'diff_families', 'diff_Mendeleev Number',
       'diff_Atomic Radus', 'diff_ Covalent_Radius', 'diff_Zunger radii sum',
       'diff_ionic radius', 'diff_crystal radius',
       'diff_ Pauling_Electronegativity', 'diff_MB electonegativity',
       'diff_Gordy electonegativity', 'diff_Mullinke EN',
       'diff_Allred-Rockow electronegativity', 'diff_metallic valence',
       'diff_number of valence electrons',
       'diff_gilmor number of valence electron', 'diff_valence s',
       'diff_valence p', 'diff_valence d', 'diff_outer shell electrons',
       'diff_1st ionization potential (kJ/mol)', 'diff_polarizability\n(A^3)',
       'diff_Melting point (K)', 'diff_Boiling Point (K)',
       'diff_Density (g/mL)', 'diff_specific heat (J/g K) ',
       'diff_heat of fusion (kJ/mol) ', 'diff_heat of vaporization (kJ/mol) ',
       'diff_thermal conductivity (W/(m K)) ',
       'diff_heat atomization\n(kJ/mol)', 'diff_Cohesive energy',
       'diff_electron affinity (kJ/mol)', 'max_ Atomic_Number',
       'max_ Atomic_Weight', 'max_Period', 'max_group', 'max_families',
       'max_Mendeleev Number', 'max_Atomic Radus', 'max_ Covalent_Radius',
       'max_Zunger radii sum', 'max_ionic radius', 'max_crystal radius',
       'max_ Pauling_Electronegativity', 'max_MB electonegativity',
       'max_Gordy electonegativity', 'max_Mullinke EN',
       'max_Allred-Rockow electronegativity', 'max_metallic valence',
       'max_number of valence electrons',
       'max_gilmor number of valence electron', 'max_valence s',
       'max_valence p', 'max_valence d', 'max_outer shell electrons',
       'max_1st ionization potential (kJ/mol)', 'max_polarizability\n(A^3)',
       'max_Melting point (K)', 'max_Boiling Point (K)', 'max_Density (g/mL)',
       'max_specific heat (J/g K) ', 'max_heat of fusion (kJ/mol) ',
       'max_heat of vaporization (kJ/mol) ',
       'max_thermal conductivity (W/(m K)) ', 'max_heat atomization\n(kJ/mol)',
       'max_Cohesive energy', 'max_electron affinity (kJ/mol)',
       'min_ Atomic_Number', 'min_ Atomic_Weight', 'min_Period', 'min_group',
       'min_families', 'min_Mendeleev Number', 'min_Atomic Radus',
       'min_ Covalent_Radius', 'min_Zunger radii sum', 'min_ionic radius','min_crystal radius', 'min_ Pauling_Electronegativity',
       'min_MB electonegativity', 'min_Gordy electonegativity',
       'min_Mullinke EN', 'min_Allred-Rockow electronegativity',
       'min_metallic valence', 'min_number of valence electrons',
       'min_gilmor number of valence electron', 'min_valence s',
       'min_valence p', 'min_valence d', 'min_outer shell electrons',
       'min_1st ionization potential (kJ/mol)', 'min_polarizability\n(A^3)',
       'min_Melting point (K)', 'min_Boiling Point (K)', 'min_Density (g/mL)',
       'min_specific heat (J/g K) ', 'min_heat of fusion (kJ/mol) ',
       'min_heat of vaporization (kJ/mol) ',
       'min_thermal conductivity (W/(m K)) ', 'min_heat atomization\n(kJ/mol)',
       'min_Cohesive energy', 'min_electron affinity (kJ/mol)']

class Vectorize_Formula():

    def __init__(self,element_property_file = 'elementsnew_onehot.xlsx'):
        self.element_df = pd.read_excel(element_property_file) # CHECK NAME OF FILE 
        self.element_df.set_index('Symbol',inplace=True)
        self.column_names = []
        for column_name in list(self.element_df.columns.values[:85]):
            self.column_names.append('avg'+'_'+column_name)
        for string in ['avg','diff','max','min']:
            for column_name in list(self.element_df.columns.values[85:]):
                self.column_names.append(string+'_'+column_name)

    def get_features(self, formula):
        try:
            fractional_composition = mg.Composition(formula).fractional_composition.as_dict()
            element_composition = mg.Composition(formula).element_composition.as_dict()
            avg_feature = np.zeros(len(self.element_df.iloc[0]))
            for key in fractional_composition:
                try:
                    avg_feature += self.element_df.loc[key].values * fractional_composition[key]
                    diff_feature = self.element_df.loc[list(fractional_composition.keys())].max()-self.element_df.loc[list(fractional_composition.keys())].min()
                except Exception as e: 
                    print('The element:', key, 'from formula', formula,'is not currently supported in our database')
                    return np.array([np.nan]*len(self.element_df.iloc[0])*5)
            max_feature = self.element_df.loc[list(fractional_composition.keys())].max()
            min_feature = self.element_df.loc[list(fractional_composition.keys())].min()
            
            features = np.concatenate([avg_feature, diff_feature[85:], np.array(max_feature)[85:], np.array(min_feature)[85:]])
            return features.transpose()
        except:
            print(f'There was an error with the Formula: {formula}, this is a general exception with an unkown error')
            return [np.nan]*len(self.element_df.iloc[0])*5
    
def boxplot_compare_pred(model_list,test_compounds):
    '''
    Creates a boxplot diagram intended for comparison of predicted values from a list of models for a single target composition, to test and visualize the variance between models
    
    Parameters:
    -------------------------------------
    
    test_compounds: list of strings
        list of compositions to be tested
    '''

    from matplotlib.pyplot import boxplot
    from matplotlib.pyplot import figure
    gf = Vectorize_Formula()
    for compound in test_compounds:
        figure(figsize=(12,1))
        features = gf.get_features(compound).reshape(1,225)
        predictions = []
        for model in model_list:
            predictions.append(model.predict(features)[0])
        boxplot(predictions, vert=False)
        plt.title(f'Boxplot Comparision for {compound}')
        plt.xlabel('Predicted Hf (eV/atom)')
        plt.yticks(np.zeros(len(predictions))+20,'') # needs to be at least the length of the number of samples
        plt.ylim((0.9,1.1))
        plt.xlim(min(predictions)-0.2*abs(min(predictions)),max(predictions)+0.2*abs(max(predictions)))
        plt.scatter(predictions,np.zeros(len(predictions))+1,alpha=1,color='w',edgecolors='k') # needs to be the length of the number of samples
        plt.show()
    
        
def clean_data(data_df,target_cols=None,label_col='Composition', target_range=None, remove_dupes_keep = 'none', remove_non_icsd = None,output_file = None):
    '''
    Takes in a pandas dataframe, removes null entries, data points with target values outside target range, data points with unsupported elements, and removes duplicate data points. Returns a dataframe containing the remaining data points.
    
    Parameters:
    -----------------------------------------    
    data_df: Pandas Dataframe
        columnar Dataframe with a label column and corresponding target column.
    
    label_col: string
        name of the column that contains chemical compositions
        (default = 'Composition') 
    
    target_cols: list of strings
        list of column names that contain target values
        (default = None)
    
    target_range: 2 dimensional tuple
        tuple with a lower and upper bound of acceptable target values. Values outside this range are filtered out.
        (default = None)
        
    remove_dupes_keep: select 'low','high'
        string either 'low' or 'high' that decides whether to keep only the lowest or highest value for duplicate values from label_col. If set to 'none' will not drop duplicates.
        (default = 'none')
        
    remove_non_icsd: list of strings
        list where first element is the name of the column containing ICSD reference numbers (usually 'icsd_ids') and second element is the value that will appear when that cell is empty (usually [], not in '' quotes)
        (default = None)
        
    output_file: string ending in .xlsx
        name of the file path to write the resulting file. must end in .xlsx
        (default = None)
    
   '''
    if target_cols != None:
        for target_col in target_cols:
            # remove compounds with null entries
            original_count = len(data_df)
            data_df[target_col] = data_df[target_col].replace([np.inf,-np.inf],np.nan)
            data_df = data_df[~ data_df[target_col].isnull()]
            print(f'Removed {(original_count - len(data_df))}/{original_count} null or infinite {target_col} entries')
            
            # remove data points with target values outside target range
            original_count = len(data_df)
            if target_range != None:
                data_df = data_df[data_df[target_col]>target_range[0]]
                data_df = data_df[data_df[target_col]<target_range[1]]
                print('Removed %d/%d out of range entries'%(original_count - len(data_df), original_count))
        
            # sort by target value and remove duplicate compositions
            if remove_dupes_keep == 'none':
                pass
            else:
                if remove_dupes_keep == 'low':
                    data_df.sort_values(target_col, ascending=True, inplace=True)
                if remove_dupes_keep == 'high':
                    data_df.sort_values(target_col, ascending=False, inplace=True)
                original_count = len(data_df)
                data_df.drop_duplicates(label_col, keep='first', inplace=True)
                print('Removed %d/%d duplicate entries, kept %sest value'%(original_count - len(data_df), original_count, remove_dupes_keep))        
        
    # remove unwanted elements from the data (noble gas, Tc, and Z>83 except Th, U)
    original_count = len(data_df)
    drop_index = []
    data_df=data_df.drop(data_df[data_df[label_col].isna()].index)
    for i,comp in enumerate(data_df[label_col]):
        mg_comp = mg.Composition(comp)
        if any(elem in [mg.DummySpecie('T'),mg.DummySpecie('D'),mg.Element('He'), mg.Element('Ne'), mg.Element('Ar'), mg.Element('Kr'), mg.Element('Xe'), mg.Element('Rn'), mg.Element('Tc')] for elem in mg_comp.elements):
            drop_index.append(i)
        elif any(z > 83 and z != 92 and z != 90 for z in [elem.number for elem in mg_comp.elements]):
            drop_index.append(i)
    data_df.drop(data_df.index[drop_index], inplace = True)
    data_df.reset_index(drop=True,inplace=True)
    print('Removed %d/%d bad element entries'%(original_count - len(data_df), original_count))  
    
    # remove items in the dataframe that do not have an ICSD ID
    if remove_non_icsd != None:
        original_count = len(data_df)
        target_col,target_val = remove_non_icsd[0],remove_non_icsd[1]
        data_df[target_col] = data_df[target_col].astype(str)
        data_df['column_has'] = data_df.apply(lambda row: column_has(row,target_col,target_val),axis=1)
        data_df = data_df[data_df['column_has']==False].copy()
        data_df.drop('column_has',axis=1,inplace=True)
        data_df.reset_index(drop=True)
        print('Removed %d/%d non-ICSD entries'%(original_count - len(data_df), original_count))
        
    print('Cleaned compounds remaining:',len(data_df))
        
    if output_file != None:
        print('Writing output to',output_file)
        data_df.to_excel(output_file,index=False)
    
    return data_df

def column_has(row,target_col,target_val):
    if row[target_col]==target_val:
        return True
    else:
        return False
   

def train_rf_model(feature_df,target_df,target_range=None,
                   mf_range=range(10,100,10),n_est=50,njobs=-1,split_fraction=0.8,rand_state=np.random.randint(100)):
#    random.seed(1234) # turn on to make reproducible

    # define X and y
    X,y = feature_df,target_df

    # filter values out of target range
    if target_range != None:
        for target in target_df.columns:
            feature_df = feature_df[feature_df[target]>target_range[0]]
            feature_df = feature_df[feature_df[target]<target_range[1]] 
        
    # train-test split
    X_train,y_train = X.sample(frac=split_fraction,random_state=rand_state),y.sample(frac=split_fraction,random_state=rand_state)
    X_test,y_test = X.drop(X_train.index),y.drop(y_train.index)
    print('Training data size:',len(X_train))
    print('Test data size:',len(X_test))
    
    grid = GridSearchCV(RandomForestRegressor(n_estimators=n_est,n_jobs=njobs,random_state=rand_state),
                        param_grid=dict(max_features=mf_range),
                        scoring='neg_mean_squared_error',
                        cv=ShuffleSplit(n_splits=1,test_size=0.1,random_state=rand_state))
    grid.fit(X_train,y_train)
    fig, (ax1,ax2) = plt.subplots(1,2,figsize=(14,6))

    # Plot the score as a function of alpha
    ax1.scatter(grid.cv_results_['param_max_features'].data,
          np.sqrt(-1 * grid.cv_results_['mean_test_score']))
    ax1.scatter([grid.best_params_['max_features']], np.sqrt([-1*grid.best_score_]), marker='o', color='r', s=40)
    ax1.set_xlabel('Max. Features')
    ax1.set_ylabel('RMSE')
    ax1.set_title('Model RMSE by MF')
    model = grid.best_estimator_
    
    # plot features by importance (top n_features)
    n_features = 10
    imp_df=pd.DataFrame(feature_df.columns,columns=['feature'])
    imp_df['importance']=model.feature_importances_
    imp_df=imp_df.sort_values(by=['importance'],ascending=False)
    ax2.bar(imp_df[0:n_features]['feature'],imp_df[0:n_features]['importance'])
    ax2.set_xlabel('Feature')
    ax2.set_xticklabels(imp_df[0:n_features]['feature'],rotation=-30,ha='left')
    ax2.set_ylabel('Importance')
    ax2.set_title(f'Most Important {n_features} Features')

    return X_train, y_train, X_test, y_test, model
    
    
def test_rf_model(X_train,y_train,X_test,y_test,model):
    cv_prediction = cross_val_predict(model, X_train, y_train, cv=KFold(10, shuffle=True))   
    for scorer in ['r2_score', 'mean_absolute_error', 'mean_squared_error']:
        score = getattr(metrics,scorer)(y_train, cv_prediction)
        print('Cross validation',scorer, round(score,4))        
    predict_y = model.predict(X_test)
    mae = mean_absolute_error(y_test, predict_y)
    rmse = np.sqrt(mean_squared_error(y_test, predict_y))
    fig, ax = plt.subplots(figsize = (7,6))
    ax.scatter(y_test, predict_y, edgecolors= (0,0,0), alpha = 0.4, color = 'grey')
    ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=4)
    ax.set_xlim([y_test.min(),y_test.max()])
    ax.set_ylim([y_test.min(),y_test.max()])
    ax.set_xlabel('Measured')
    ax.set_ylabel('Predicted')
    ax.set_title('Parity Plot')
    ax.text(0.02, .98, s = 'R2test: {0}'.format(round(model.score(X_test,y_test),4)),horizontalalignment='left',verticalalignment='top', transform=ax.transAxes)
    ax.text(0.02, .92, s = 'RMSE: {0}'.format(round(rmse,4)),horizontalalignment='left',verticalalignment='top', transform=ax.transAxes)
    ax.text(0.02, .95, s = 'MAE: {0}'.format(round(mae,4)),horizontalalignment='left',verticalalignment='top', transform=ax.transAxes)
    ax.text(0.5, .98, s = 'N_estimators = {0}, Max Features = {1}'.format(model.n_estimators,model.max_features),horizontalalignment='center',verticalalignment='top', transform=ax.transAxes)
    plt.show()

def plot_pd(data_pd,data_df,e_above_max = 50,plot_elements=['heatmap','known','above hull','on hull','facets'],alternate_heatmap_data_pd=pd.DataFrame(),export_image_name = None,point_scale=500):
    if alternate_heatmap_data_pd.empty == False:
        data_pd_heatmap = alternate_heatmap_data_pd
    else:
        data_pd_heatmap = data_pd
    e_above_max = e_above_max/(10e5)
    elem_list = data_pd['System'][0]
    known_df = find_known_phases(data_pd,data_df)
    if len(elem_list)==2:
        e1,e2 = elem_list[0],elem_list[1]
        from scipy.spatial import ConvexHull
        hull = ConvexHull(data_pd[[elem_list[1],'Value']])
        hull_verts = []
        hull.vertices.sort()
        hull_verts.append(hull.points[0])
        for vertex in hull.vertices:
            if hull.points[vertex][1] <= 0:
                hull_verts.append(hull.points[vertex])
        hull_verts.append(hull.points[-1])
        hull_verts = np.stack(hull_verts)
        
        import matplotlib.pyplot as plt

        fig,ax = plt.subplots(figsize=(12,9))
        
        for xc in known_df[e2]:
            ax.axvline(x=xc*100,linewidth=1,color='black',alpha=0.3)

        ax.plot(hull_verts[:,0], hull_verts[:,1], 'r--', lw=2,zorder = 0)
        ax.scatter(hull_verts[:,0],hull_verts[:,1],edgecolors = 'red',linewidths = 4)
        ax.fill_between(data_pd[elem_list[1]],data_pd['Value']+data_pd['StDev'],data_pd['Value']-data_pd['StDev'],alpha = 0.3,color = 'grey')
        ax.scatter(data_pd[elem_list[1]],data_pd['Value'],color = 'blue')
        ax.set_title('{0}-{1} Predicted Phase Diagram'.format(elem_list[0],elem_list[1]))
        plt.text(0.5, 0.98, s = 'One S.D. shown',horizontalalignment = 'center', verticalalignment = 'top', transform = ax.transAxes)
        plt.xlabel('{} percent'.format(e2))
        plt.ylabel('Predicted Formation Energy (eV/atom)')
        plt.show()
        
        # write file to png
        if export_image_name != None:
            import os
            if not os.path.exists("images"):
                os.mkdir("images")
            fig.savefig("images/{0}".format(export_image_name))
        
    if len(elem_list)==3:
        import plotly.graph_objects as go
        import matplotlib.pyplot as plt
        import plotly.figure_factory as ff
        import plotly.colors as clrs
        fig = go.Figure()
        
        # Define custom reverse rainbow color map
        clrs.PLOTLY_SCALES['Rainbow_r'] = [[0, 'rgb(255,0,0)'],[0.125, 'rgb(255,111,0)'], [0.25, 'rgb(255,234,0)'],[0.375, 'rgb(151,255,0)'],[0.5, 'rgb(44,255,150)'],[0.625, 'rgb(0,152,255)'],[0.75, 'rgb(0,25,255)'],[0.875, 'rgb(0,0,200)'],[1, 'rgb(150,0,90)']]
        e1_per = data_pd_heatmap[elem_list[0]].values
        e2_per = data_pd_heatmap[elem_list[1]].values
        e3_per = data_pd_heatmap[elem_list[2]].values
        y_predict = data_pd_heatmap['Value'].values

        # when we imported the pycalphad.plot.triangular module, it made the 'triangular' projection available for us to use.
        fig = ff.create_ternary_contour(np.stack([e1_per,e2_per,e3_per]),
                                        y_predict,
                                        pole_labels = elem_list,
                                        interp_mode='cartesian',
                                        ncontours = 20,
                                        colorscale= 'Rainbow_r',
                                        showscale = True,
                                        showmarkers = False,
                                        coloring = None,
                                        title = {
                                            'text':'{0}-{1}-{2} system ({3} meV above hull shown)'.format(elem_list[0],elem_list[1],elem_list[2],e_above_max*1000000),
                                            'x':0.5,
                                            'y':0.9,
                                            'xanchor':'center',
                                            'yanchor':'top'
                                        },
                                        width = 800,
                                        height = 800)   
        if 'facets' in plot_elements:
            # START PLOTTING FACETS
            comps = data_pd['Composition']
            Ef=data_pd['Value']
            mg_comp=[None]*len(comps)
            for i in range(len(comps)):
                mg_comp[i]=Composition(comps[i])
            entries3=[None]*len(mg_comp)
            for i in range(len(mg_comp)):
                entries3[i]=PDEntry(composition=mg_comp[i], energy=Ef[i])
            pd3 = PhaseDiagram(entries3)
            pd3_stable = [None]*len(pd3.stable_entries)
            simps = []
            for phase in pd3.stable_entries:
                chempots = pd3.get_all_chempots(phase.composition)
                for keys, values in chempots.items():
                    simps.append(keys)
            # remove duplicates
            simps = list(set(simps))
            for i,simplex in enumerate(simps):
                simps[i] = simplex.split('-')
                simps[i].append(simps[i][0])
            import re
            for i,simp in enumerate(simps):
                for n,vert in enumerate(simp):
                    simps[i][n] = re.findall('[A-Z]+[a-z]*[0-9]*.[0-9]*',mg.Composition(vert).formula)
                    for element in elem_list:
                        if list(filter(re.compile(rf'{element}.*').match,simps[i][n])) ==[]:
                            simps[i][n].append(element+'0')
                    simps[i][n].sort()
                    for p,element in enumerate(elem_list):
                        simps[i][n][p] = simps[i][n][p].replace(element,'')

            for simp in simps:
                a,b,c = [],[],[]
                for n_elem,elem in enumerate([a,b,c]):
                    for n_vert,vert in enumerate(simp):
                        elem.append(vert[n_elem])
                fig.add_trace(go.Scatterternary({
                        'mode': 'lines',
                        'a': a,
                        'b': b,
                        'c': c,
            #    'text': df_pcd['Composition'].values,
                        'line':{
                            'width':1,
                            'color':'black'
                        }
                            }))
            ### END PLOTTING FACETS
       
        std_scaler = point_scale
        
        if 'above hull' in plot_elements:
            df_abovehull = data_pd[data_pd['Ehull'].between(0.000000000000001,e_above_max)] # <-- dataframe of points above the hull

            # plot above convex hull points
            fig.add_trace(go.Scatterternary({
               'mode': 'markers',
                'a': df_abovehull[elem_list[0]].values,
                'b': df_abovehull[elem_list[1]].values,
                'c': df_abovehull[elem_list[2]].values,
                'text': df_abovehull['Composition'].values,
                'name': 'ML Above Hull',
                'hoverinfo': 'text+name',
                'marker': {
                    'symbol': 0,
                    'color': 'grey',
                    'opacity': 0.5,
                    'size': df_abovehull['StDev']*std_scaler,
                    'line': { 'width': 2,
                            'color': 'black'}
                }
            }))

        if 'on hull' in plot_elements:
            df_hull = data_pd[data_pd['Ehull'].between(-100,0)] # <-- dataframe of just points on the hull
            # plot convex hull points
            fig.add_trace(go.Scatterternary({
               'mode': 'markers',
                'a': df_hull[elem_list[0]].values,
                'b': df_hull[elem_list[1]].values,
                'c': df_hull[elem_list[2]].values,
                'text': df_hull['Composition'].values,
                'name': 'ML Convex Hull',
                'hoverinfo': 'text+name',
                'marker': {
                    'symbol': 0,
                    'color': 'red',
                    'opacity': 1.0,
                    'size': df_hull['StDev']*std_scaler,
                    'line': { 'width': 2,
                            'color': 'black'}
                }
            }))

        if 'known' in plot_elements:
            ### plot known phases
            known_df = find_known_phases(data_pd,data_df) 
            # define the scatterplot of known phases
            fig.add_trace(go.Scatterternary({
                'mode': 'markers',
                'a': known_df[elem_list[0]].values,
                'b': known_df[elem_list[1]].values,
                'c': known_df[elem_list[2]].values,
                'text': known_df['Composition'].values,
                'hoverinfo':'text+name',
                'name': 'Known',
                'marker': {
                    'symbol': 4,
                    'color': 'white',
                    'size': 12,
                    'line': { 'width': 1,
                            'color' : 'black'}
                }
            }))

        # retitle and rename some features of the plot
        fig.update_layout({
            'ternary':
                {
                'sum':1,
                'bgcolor':'white',
                'aaxis':{'title': elem_list[0], 'min': 0, 'linewidth':1, 'ticks':'outside', 'linecolor':'black' },
                'baxis':{'title': elem_list[1], 'min': 0, 'linewidth':1, 'ticks':'outside', 'linecolor':'black' },
                'caxis':{'title': elem_list[2], 'min': 0, 'linewidth':1, 'ticks':'outside', 'linecolor':'black' }
            }
        })
        fig.show()
        
        # write file to png
        if export_image_name != None:
            import os
            if not os.path.exists("images"):
                os.mkdir("images")
            fig.write_image("images/{0}".format(export_image_name))
            
    if len(elem_list)>3:
        print('Only binary and ternary phase diagram plotting currently supported, sorry!')
        
    return

def find_known_phases(data_pd,data_df):
#    pcd_data = pd.read_excel('PCD2019_comp.xlsx')
    elem_list = data_pd['System'][0]
    
    phases = []
    for comp in data_df['Composition']:
        if(all(str(x) in elem_list for x in mg.Composition(comp).elements)):
            phases.append(comp)
    known_df = pd.DataFrame(phases,columns=['Composition'])
    for elem in elem_list:
        known_df[elem]=0
    for n,comp in enumerate(known_df['Composition']):
        for elem in elem_list:
            known_df.loc[[n],[elem]]=(mg.Composition(comp).get_atomic_fraction(mg.Element(elem)))
    
    return known_df

def pretrain_nn_models(data_df,feature_df,element_property_file = 'elementsnew_onehot.xlsx',energy_cutoff = None,n_samples=10,split_fraction=0.8,epochs=50):
    feature_cols = feature_df.columns[1:]
    
    print('Building models...')
    time.sleep(0.3)
    # initialize lists and read in descriptor file for targets
    model_stats,val_stats = [],[]
    feature_cols = feature_df.columns[1:]
    
    # define X and y
    X,y = feature_df[feature_cols],feature_df['Value']

    # filter out data above 1 eV/atom
    if energy_cutoff != None:
        X,y = feature_df[feature_df['Value']<energy_cutoff][feature_cols], feature_df[feature_df['Value']<energy_cutoff]['Value']
        
    model_list=[]
    for i in tqdm.tqdm(range(n_samples)):
        X_train, y_train, X_test, y_test, model = mlf.train_nn_model(feature_df,epochs=epochs,split_fraction=split_fraction)
        model_list.append(model)
        
        # calculate the MSE and RMSE of the holdout data and store in 'stats'
        mae = mean_absolute_error(y_test, predict_y)
        
    return model_list

def pretrain_rf_models(data_df,feature_df,target_cols = None,element_property_file = 'elementsnew_onehot.xlsx',energy_cutoff = None):
    feature_cols = feature_df.columns[1:]
    
    # set number of trials to be averaged, number of trees in each forest, max features, and elements
    n_samples = int(input('Number of independent RFs (default 10): ') or 10)
    ne = int(input('Number of estimators per RF (default 50): ') or 50)
    mf = int(input('Max number of features (default 48): ') or 48)
    
    print('Building models...')
    time.sleep(0.3)
    # initialize lists and read in descriptor file for targets
    model_stats,val_stats = [],[]

    # define X and y
    X,y = feature_df.drop(target_cols,axis=1),feature_df[target_cols]

    # filter out data above energy_cutoff
    if energy_cutoff != None:
        X,y = feature_df[feature_df['Value']<energy_cutoff][feature_cols], feature_df[feature_df['Value']<energy_cutoff]['Value']
    
    model_list = []

    for i in tqdm.tqdm(range(n_samples)):
        rand_state = np.random.randint(100)
        # train-test split
        X_train,y_train = X.sample(frac=0.8,random_state=rand_state),y.sample(frac=0.8,random_state=rand_state)
        X_test,y_test = X.drop(X_train.index),y.drop(y_train.index)
    
        # train the RF model on the training data
        model = RandomForestRegressor(n_jobs = -1, n_estimators = ne, max_features = mf)
        model.fit(X_train, y_train)
        predict_y = model.predict(X_test)
        model_list.append(model)
    
        # calculate the MSE and RMSE of the holdout data and store in 'stats'
        mae = mean_absolute_error(y_test, predict_y)
        model_stats.append([model.score(X_test,y_test),mae])
    model_stats=np.stack(model_stats)
    stats_rmse = np.average(model_stats[:,0])
    stats_mae = np.average(model_stats[:,1])
    print('Average model RMSE:',stats_rmse,'\n','Average model MAE:',stats_mae)
    
    return model_list

def predict_pd(model_list,elem_list = None,step_size = None, comp_ranges = None,element_property_file = 'elementsnew_onehot.xlsx',energy_cutoff = None,extra_feature_dict=None,static_elem_dict=None,write_data=True):
    feature_cols = global_feature_cols
    
    if elem_list == None:
        elem, elem_list = 'value',[]
        elements = ['','H','He','Li','Be','B','C','N','O','F','Ne','Na','Mg','Al','Si','P','S','Cl','Ar','K','Ca','Sc','Ti','V','Cr','Mn','Fe','Co','Ni','Cu','Zn','Ga','Ge','As','Se','Br','Kr','Rb','Sr','Y','Zr','Nb','Mo','Tc','Ru','Rh','Pd','Ag','Cd','In','Sn','Sb','Te','I','Xe','Cs','Ba','La','Ce','Pr','Nd','Pm','Sm','Eu','Gd','Tb','Dy','Ho','Er','Tm','Yb','Lu','Hf','Ta','W','Re','Os','Ir','Pt','Au','Hg','Tl','Pb','Bi','Po','At','Rn','Fr','Ra','Ac','Th','Pa','U','Np','Pu','Am','Cm','Bk','Cf','Es','Fm','Md','No','Lr','Rf','Db','Sg','Bh','Hs','Mt','Ds','Rg','Cn','Nh','Fl','Mc','Lv','Ts','Og']
        while elem != '':
            elem = input('Enter element (blank if done): ')
            if elem in elements:
                elem_list.append(elem)
            else:
                print('Element not found!')

        # alphabetize element list
        elem_list.remove('')
    elem_list.sort()
    system = ''
    for elem in elem_list:
        system += elem
        
    if comp_ranges == None:
        if step_size == None:
            step = float(input('Step size % (default 5%): ') or 5)
        else:
            step = float(step_size)
        n_steps = int((100)/step + 1)
        steps = np.linspace(0,100,n_steps)
        
        phases = []
        for phase in itertools.product(steps, repeat=len(elem_list)):
            if sum(map(round, phase)) == 100:
                phases.append(phase)                
             
        
    if comp_ranges != None:
        steps = comp_ranges
        phases = []
        for phase in itertools.product(*steps):
            if sum(map(round,phase)) == 100:
                phases.append(phase)  
        for i in range(len(elem_list)):
            endpoint = list(np.zeros(len(elem_list)))
            endpoint[i] = 100
            phases.append(tuple(endpoint))
        
    
    print('Generating composition grid and features...')
    time.sleep(0.3)
    comps = []
    for phase in phases:
        comp = ''
        comp_list = [elem+str(phase[n]) for n,elem in enumerate(elem_list)]
        for item in comp_list:
            comp += item
        if static_elem_dict != None:
            for key,value in static_elem_dict.items():
                comp += key+str(value)
        comps.append((comp))
    
    elemental_stoich_df = pd.DataFrame(phases,columns = elem_list)
    comps_df = pd.DataFrame({'Composition':comps,'Value':np.zeros(len(comps))})
    data_pd = pd.concat([elemental_stoich_df,comps_df],axis=1)
            
    feature_pd = write_features(data_pd)
    
    # add any extra feature columns as manually defined, will use same value for all targets
    if extra_feature_dict != None:
        for key,value in extra_feature_dict.items():
            feature_pd[key]=value
    
    print('Generating predictions...')
    time.sleep(0.3)
    # initialize lists and read in descriptor file for targets
    values,val_stats = [],[]
    targets_X = feature_pd.values

    for model in tqdm.tqdm(model_list):
        values.append(model.predict(targets_X))

    # create 'val_stats' list of mean and stdev for all targets
    values = np.stack(values)
    for i in range(len(values[0])):
        val_stats.append([np.average(values[:,i]),np.std(values[:,i])])
    val_stats = np.stack(val_stats) 

    # read in and store x values in 'x_vals' list
    # (percent of alphabetically second element)
    data_pd['Value'],data_pd['StDev'] = val_stats[:,0],val_stats[:,1]
    
    if static_elem_dict != None:
        data_pd = find_pseudo_hull(data_pd,elem_list)
    else:
        data_pd = find_hull(data_pd,elem_list)
    
    if write_data == True:
        data_pd.to_excel('%s_predict.xlsx' % (system), index = False )
        feature_pd.to_excel('{0}_descriptors.xlsx'.format(system),index=False)
        time.sleep(0.1)
        print('Done! Wrote {0}_predict.xlsx and {0}_descriptors.xlsx'.format(system),end='',flush=True)

    return data_pd

def find_hull(data_pd, elem_list):
    # For plotting the convex hull points
    Ef = data_pd['Value']
    mg_comp = [Composition(comp) for comp in data_pd['Composition']]
    
    entries3=[None]*len(mg_comp)
    for i in range(len(mg_comp)):
        entries3[i]=PDEntry(composition=mg_comp[i], energy=Ef[i])

    pd3 = PhaseDiagram(entries3)
    
    # calculate convex hull points
    data_pd['Ehull'] = [pd3.get_e_above_hull(e) for e in entries3]
    data_pd['System'] = None
    data_pd['System'][0] = elem_list
    
    return data_pd

    
def find_pseudo_hull(data_pd,elem_list):
    # For plotting the convex hull points
    Ef = data_pd['Value']
    mg_comp = [Composition(comp) for comp in data_pd['Composition']]
    
    entries3=[None]*len(mg_comp)
    for i in range(len(mg_comp)):
        entries3[i]=PDEntry(composition=mg_comp[i], energy=Ef[i])

    pd3 = CompoundPhaseDiagram(entries3,[entries3[0].composition,entries3[-1].composition])
    pd3 = pd3.transform_entries(entries3,[entries3[0].composition,entries3[-1].composition])
    
    # calculate convex hull points
#    data_pd['Ehull'] = [pd3.get_e_above_hull(e) for e in entries3]
    data_pd['System'] = None
    data_pd['System'][0] = elem_list
    return data_pd 

def write_features(data_df,
                   target_col = None,
                   label_col='Composition',
                   element_property_file='elementsnew_onehot.xlsx',
                   scale_properties=False,
                   output_file = None
                  ):
    gf=Vectorize_Formula()
    
    '''
    Takes in a pandas dataframe and outputs a dataframe of elemental and compositional properties.
    
    Parameters:
    -----------------------------------------    
    data_df: Pandas Dataframe
        columnar Dataframe with a label column and corresponding target column.
    
    label_col: string
        name of the column that contains chemical compositions
        (default = 'Composition') 
    
    target_col: string
        name of the column that contains target values
        (default = None)
        
    element_property_file: string
        path to xlsx spreadsheet with reference data for elemental properties
        (default = 'elementsnew_onehot.xlsx')
        
    scale_properties: Bool
        whether to apply a standard scaler to only the property based descriptors.
        ***WARNING***: if set to True, descriptors for predicted compounds must also be scaled by the SAME STANDARD SCALER or nothing will make sense. Leave as False unless you are sure you can scale these properly.
        (default = False)
        
    output_file: string ending in .xlsx
        file name to save the resulting spreadsheet to, will not save unless this tag is set
        (default = None)
    
   '''

    # empty lists for storage of features and targets
    features= []    

    # add values to list using for loop
    for formula in tqdm.tqdm(data_df[label_col],total=len(data_df)):
        features.append(gf.get_features(formula))
        
    # feature vectors as X
    X = pd.DataFrame(features, columns = gf.column_names)
    pd.set_option('display.max_columns', None)

    # drop elements that aren't included in the elemental properties list. 
    # These will be returned as feature rows completely full of NaN values. 
    X.dropna(inplace=True, how='all')

    # reset dataframe indices to simplify code later.
    X.reset_index(drop=True, inplace=True)

    # collect column names and find median values, fill missing values with mean
    cols = X.columns.values
    median_values = X[cols].median()
    X[cols]=X[cols].fillna(median_values.iloc[0])
    print('Data Shape:',X.shape)

    # add formation energy targets to first column
    X_cols = X.columns.tolist()
    feature_df = X[X_cols]
    
    if scale_properties == True:
        feature_df_1hot = feature_df[feature_df.columns[:86]]
        feature_df_prop = feature_df[feature_df.columns[86:]]
        
        pipeline = Pipeline([
            ('imputer',SimpleImputer(strategy='median')),
            ('std_scaler',StandardScaler())
        ])
        feature_df_prop = pd.DataFrame(pipeline.fit_transform(feature_df_prop),columns=feature_df_prop.columns)
        feature_df = pd.concat([feature_df_1hot,feature_df_prop],axis=1)     
        
    if output_file != None:
        print('Writing output to',output_file)
        feature_df.to_excel(output_file,index=False)
    
    return feature_df