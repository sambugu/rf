'''
GUI for running pySPARSE - py Soil Plant Atmosphere Remote Sensing Evapotranspiration - Boulet et al. (2015)

-- ufu --  from 080923 ...made using pysimplegui [.exe compiled using pyinstaller]
'''

import os
#import ctypes
from datetime import datetime
import PySimpleGUI as sg
import pySPARSE as pySP
import numpy as np
import pandas as pd
import webbrowser as browser
import matplotlib
import matplotlib.pyplot as plt
from math import floor
from matplotlib.ticker import NullFormatter  # useful for `logit` scale
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
matplotlib.use('TkAgg')

def resource_path(relative_path):
        try:
                base_path                       = sys._MEIPASS
        except Exception:
                base_path                       = os.path.abspath(".")

        return os.path.join(base_path, relative_path)
    
def _onetm():        
        use_custom_titlebar                     = True if sg.running_trinket() else False
        if use_custom_titlebar:
                Menu                            = sg.MenubarCustom     
        else:
                Menu                            = sg.Menu
                
        name_size                               = 32
        def name(name):
            dots                                = name_size-len(name)-2
            return sg.Text(name + ' ' + '•'*dots, size=(name_size,1),justification='r',pad=(0,0),font='consolas 10')
            
        def runSP(values):
            Tsurf                               = float(values['Tsurf'])
            vza                                 = float(values['vza'])
            rg                                  = float(values['rg'])
            Ta                                  = float(values['Ta'])
            rh                                  = float(values['rh'])
            ua                                  = float(values['ua'])
            za                                  = float(values['za'])
            lai                                 = float(values['lai'])
            glai                                = float(values['glai'])
            zf                                  = float(values['zf'])
            rstmin                              = float(values['rstmin'])
            albv                                = float(values['albv'])
            emisv                               = float(values['emisv'])
            emiss                               = float(values['emiss'])
            emissf                              = float(values['emissf'])
            albe                                = float(values['albe'])
            xg                                  = float(values['xg'])
            sigmoy                              = float(values['sigmoy'])
            albmode                             = values['albmode']
            
            [LE,H,rn,G,LEv,LEs,Hv,Hs,Tv,Ts,Tsf] = pySP.pySPARSE(Tsurf,vza,rg,Ta,rh,ua,za,lai,glai,zf,rstmin,albv,emisv,emiss,emissf,albe,xg,sigmoy,albmode)

            return [floor(LE),floor(H),floor(rn),floor(G),floor(LEv),floor(LEs),floor(Tv),floor(Ts),floor(Tsf)]

        '''keys = {
            'Surface_T':'Surface temperature',
            'rg':'Solar radiation',
        }
        defaults = {
            '297':'298',
            '293':'294',
        }
        '''

        layout_l = [
                  #[[sg.Text(text, size=10), sg.InputText(size=10, expand_x=True, key=key, default_text=default_text)] for default_text, text in defaults.items() for key, text in keys.items()],
                  [sg.T('Model Inputs',font='_ 14',justification='c',expand_x=True)],
                  [name('Surface temperature [K]') , sg.InputText(size=10,s=15,expand_x=True,key='Tsurf',default_text='297.24',justification='c')],
                  [name('View Zenith Angle [VZA [°]]') , sg.InputText(size=10,expand_x=True,key='vza',default_text='0',readonly=True,justification='c')],
                  [name('Solar radiation [W/m²]') , sg.InputText(size=10,expand_x=True,key='rg',default_text='630',justification='c')],
                  [name('Air temperature [Ta [K]]') , sg.InputText(size=10,expand_x=True,key='Ta',default_text='293.15',justification='c')],
                  [name('Relative humidity [RH [%]]') , sg.InputText(size=10,expand_x=True,key='rh',default_text='50',justification='c')],
                  [name('Wind speed [ua [m/s]]') , sg.InputText(size=10,expand_x=True,key='ua',default_text='2',justification='c')],
                  [name('Measurement height [za [m]]') , sg.InputText(size=10,expand_x=True,key='za',default_text='3',justification='c')],
                  [name('Leaf Area Index [LAI [m²/m²]]') , sg.InputText(size=10,expand_x=True,key='lai',default_text='1.5',justification='c')],
                  [name('Green LAI [GLAI [m²/m²]]') , sg.InputText(size=10,expand_x=True,key='glai',default_text='1.5',justification='c')],
                  [name('Vegetation height [m]') , sg.InputText(size=10,expand_x=True,key='zf',default_text='1',justification='c')],
                  [name('Min. stomatal resistance [s/m]') , sg.InputText(size=10,expand_x=True, key='rstmin',default_text='100',justification='c')],
                  [name('Vegetation alb. [-]') , sg.InputText(size=10,expand_x=True,key='albv',default_text='0.18',justification='c')],
                  [name('Vegetation emissivity [-]') , sg.InputText(size=10,expand_x=True,key='emisv',default_text='0.98',justification='c')],
                  [name('Soil emissivity [-]') , sg.InputText(size=10,expand_x=True, key='emiss',default_text='0.96',justification='c')],
                  [name('Surface emissivity [-]') , sg.InputText(size=10,expand_x=True, key='emissf',default_text='0.97',justification='c')],
                  [name('Surface albedo [-]]') , sg.InputText(size=10,expand_x=True, key='albe',default_text='0.3',justification='c')],
                  [name('Max. G-to-soil net radiation [-]') , sg.InputText(size=10,expand_x=True, key='xg',default_text='0.315',justification='c')],
                  [name('Leaf projection [-]') , sg.InputText(size=10,expand_x=True, key='sigmoy',default_text='0.5',justification='c')],
                  [name('Capped or Uncapped albedos') , sg.OptionMenu(['Uncapped','Capped'],s=(15,2),key='albmode')],
                  #[sg.Text("SEB estimates",size=10) , sg.Text(text_color="white", key="Output")],
                  #[name('Capped or Uncapped albedos'),sg.Radio('Uncapped', 1, key='albmode'),sg.Radio('Uncapped', 1, key='albmode')],
                  [sg.Push() , sg.Button("RUN pySPARSE",s=17,button_color=('white','#008040'))] ]
        layout_r = [
                  [sg.T('Surface Energy Balance (SEB) Estimates',font='_ 14',justification='c',expand_x=True)],
                  [sg.TabGroup([[sg.Tab('Overall Fluxes [W/m²]',[[sg.T(key="OutputTot",justification='c',font='_ 12',expand_x=True)]]),
                                 sg.Tab('Partitioning [W/m²]', [[sg.T(key="OutputPart",justification='c',font='_ 12',expand_x=True)]])]],font='_ 13')] ]

                  #[sg.Push() , sg.Button("Reset") , sg.Button("run SPARSE",button_color=('white','#008040'))] ]
        layout   = [[Menu([['File', ['Timeseries',['Open CSV [wip]','Save Output [wip]'],'Exit']],['About',['SPARSE SEB', ]]],k='-CUST MENUBAR-',p=0)],              
                      [sg.Col(layout_l, p=0), sg.Col(layout_r, p=0)],
                  [sg.Text('Surface Energy Balance | SPARSE',font='_ 8',enable_events=True,expand_x=True,justification='c',key='rf')]]
        
        window                                  = sg.Window('pySPARSE : Soil Plant Atmosphere Remote Sensing Evapotranspiration',icon=resource_path('rf.ico')).Layout(layout)
        #window                                  = sg.Window('SPARSE : soil plant atmosphere remote sensing evapotranspiration',layout,use_custom_titlebar=use_custom_titlebar)

        while True:                             # Event Loop
            event, values                       = window.Read()
            if event in (None, 'Exit'):
                break
            elif event == 'RUN pySPARSE':
                [LE,H,rn,G,LEv,LEs,Tv,Ts,Tsf]   = runSP(values)
                outputTot                       = f"\n LE: {LE} \n H:  {H} \n Rn: {rn} \n G:  {G}\n"            ### output                          = f"LE: {LE} | H: {H} | Rn: {rn} | G: {G} \n LEv: {LEv} | LEs: {LEs}"# | Tv: {Tv} | Ts: {Ts}"
                outputPart                      = f"\n LEv: {LEv} \n LEs: {LEs}"                                # | Tv: {Tv} | Ts: {Ts}"
                window['OutputTot'].update(outputTot)                                                           ### window['Output'].update(output)
                window['OutputPart'].update(outputPart)
            elif event == 'SPARSE SEB':
                sg.Popup('The pySPARSE model [Soil Plant Atmosphere Remote Sensing Evapotranspiration] \n\nTheory : https://doi.org/10.5194/hess-19-4653-2015 \n\n --- ufu v0.0.1 090923 ---',title='pySPARSE v0.0.1',background_color='#909090',button_color='#707070')
            elif event == 'rf':
                browser.open('https://runningfingers.com/seb.php')

        window.Close()

def _tmseries():
        use_custom_titlebar                     = True if sg.running_trinket() else False
        if use_custom_titlebar:
                Menu                            = sg.MenubarCustom     
        else:
                Menu                            = sg.Menu

        name_size                               = 32
        def name(name):
            dots                                = name_size-len(name)-2
            return sg.Text(name + ' ' + '•'*dots, size=(name_size,1),justification='r',pad=(0,0))#,font='consolas 10')
        
        def draw_figure(canvas, figure):
            figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
            figure_canvas_agg.draw()
            figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)

            return figure_canvas_agg
              
        def delete_figure_agg(figure_agg):
            figure_agg.get_tk_widget().forget()
            plt.close('all')            
            
        def runSPtm(meteoNrad):#,progress_bar):
            
            Tsurf                               = np.array(meteoNrad['tsobs']) + 273.15                         # tsobs loaded in [C]
            vza                                 = np.array(meteoNrad['vza'])                                    # np.array(meteoNrad['vza'])
            rg                                  = np.array(meteoNrad['rg'])
            Ta                                  = np.array(meteoNrad['ta']) + 273.15                            # ta loaded in [C]
            rh                                  = np.array(meteoNrad['rh'])
            ua                                  = np.array(meteoNrad['ua'])
            za                                  = np.array(meteoNrad['za'])                                     # ideally, the measurement height need not change over time. added to reduce the number of files to be loaded by user
            #lai                                 = 1.5; glai = 1.5  
            lai                                 = np.array(meteoNrad['lai']); glai = np.array(meteoNrad['glai'])# temporally varying surface leaf areas                                               # np.array(biophysical['lai'])
            zf                                  = np.array(meteoNrad['zf'])                                     # temporally varying vegetation height
            rstmin                              = np.array(meteoNrad['rstmin'])
            albv                                = np.array(meteoNrad['albv'])
            emisv                               = 0.98; emiss = 0.96; emissf = 0.97
            albe                                = np.array(meteoNrad['albedo'])                                 # np.array(meteoNrad['albe'])
            xg                                  = np.array(meteoNrad['xG'])                                     # G/soil net radiation fraction
            sigmoy                              = 0.5
            #albmode                             = 'UnCapped'
            albmode                             = values['albmode']
            doy                                 = np.array(meteoNrad['doy'])

            xx                                  = {'le':[]}; xx['h'] = []; xx['rn'] = []; xx['g'] = []; xx['lev'] = []; xx['les'] = []; xx['hv'] = []; xx['hs'] = []; xx['tv'] = []; xx['ts'] = []; xx['tsf'] = []; xx['doy'] = []
            #le              = []; h = []; rn =[]; g = []; lev = []; les = []; hv = []; hs = []; tv = []; ts = []; tsf = []
            for i in range(len(Tsurf)):
                [LE,H,Rn,G,LEv,LEs,Hv,Hs,Tv,Ts,Tsf] = pySP.pySPARSE(Tsurf[i],vza[i],rg[i],Ta[i],rh[i],ua[i],za[i],lai[i],glai[i],zf[i],rstmin[i],albv[i],emisv,emiss,emissf,albe[i],xg[i],sigmoy,albmode) ###= _fxn_.pySPARSE(Tsurf[i],vza[i],rg[i],Ta[i],rh[i],ua[i],za,lai[i],glai[i],zf[i],rstmin,albv,emisv,emiss,emissf,albe[i],xg,sigmoy,albmode)

                '''
                le[len(le):] = [LE]; h[len(h):] = [H]; rn[len(rn):] =[Rn]; g[len(g):] = [G];
                lev[len(lev):] = [LEv]; les[len(les):] = [LEs]; hv[len(hv):] = [Hv]; hs[len(hs):] = [Hs];
                tv[len(tv):] = [Tv]; ts[len(ts):] = [Ts]; tsf[len(tsf):] = [Tsf]
                '''
                    
                xx['le'][len(xx['le']):]        = [LE]; xx['h'][len(xx['h']):] = [H]; xx['rn'][len(xx['rn']):] = [Rn]; xx['g'][len(xx['g']):] = [G];
                xx['lev'][len(xx['lev']):]      = [LEv]; xx['les'][len(xx['les']):] = [LEs]; xx['hv'][len(xx['hv']):] = [Hv]; xx['hs'][len(xx['hs']):] = [Hs];
                xx['tv'][len(xx['tv']):]        = [Tv]; xx['ts'][len(xx['ts']):] = [Ts]; xx['tsf'][len(xx['tsf']):] = [Tsf]; xx['doy'][len(xx['doy']):] = [doy[i]]

                if i/10 == floor(i/10) or i == (len(Tsurf)-1):
                        curr_ = (i/len(Tsurf)*100) if i != (len(Tsurf)-1) else 100                        
                        progress_bar.UpdateBar(curr_,100) 
                        #window.write_event_value('next_sp', curr_)
                        #window.refresh()
                        if i == (len(Tsurf)-1): run_pySP.update(disabled=False)
                
            output                              = xx

            return [output]
        
        layout_l  = [[sg.Text("Input File: ")], [sg.Input(key='csv_loc',expand_x=True), sg.FileBrowse()],
                     [sg.T(key="inputname",justification='c',font='_ 12',expand_x=True),sg.Button('Load Input Data [.csv]')],
                     [sg.Canvas(key='indat_canvas', background_color=sg.theme_button_color()[1], size=(305,200),expand_x=True)],
                     [name('Capped or Uncapped albedos ?') , sg.Push() , sg.OptionMenu(['Uncapped','Capped'],s=(15,2),key='albmode')],
                     [],
                     [] ]
        layout_r  = [[sg.Canvas(key='rnsp_canvas', background_color=sg.theme_button_color()[1], size=(125,120),expand_x=True),
                      sg.Canvas(key='lesp_canvas', background_color=sg.theme_button_color()[1], size=(125,120),expand_x=True)],
                     [sg.Canvas(key='outdat_canvas', background_color=sg.theme_button_color()[1], size=(420,200),expand_x=True)],                     
                     [],
                     [sg.ProgressBar(1, orientation='h', size=(20, 20), key='progress_sp'),
                      sg.Push() , sg.Button("RUN pySPARSE",s=17,button_color=('white','#008040'),disabled=True)],
                     [sg.Text("Output Path: ")], [sg.Input(key='csv_outloc',expand_x=True),sg.FolderBrowse()],
                     [sg.Push() , sg.Button("Save Results",s=10,button_color=('white','#008040'),disabled=True)] ]
        layout    = [[Menu([['File', ['Timeseries',['Open CSV [wip]','Save Output [wip]'],'Key In Data','Exit']],['About',['SPARSE SEB', ]]],k='-CUST MENUBAR-',p=0)],      
                      [sg.Col(layout_l, p=0),sg.VSep(color='#666666'),sg.Col(layout_r, p=0)],
                  [sg.Text('Surface Energy Balance | SPARSE',font='_ 7',enable_events=True,expand_x=True,justification='c',key='rf')]]

        window                                  = sg.Window('pySPARSE : Soil Plant Atmosphere Remote Sensing Evapotranspiration',icon=resource_path('rf.ico')).Layout(layout)
        progress_bar                            = window['progress_sp']
        run_pySP                                = window['RUN pySPARSE']
        Save_SP                                 = window['Save Results']
        
        while True:                             # Event Loop
            event, values                       = window.Read()
            if event in (None, 'Exit'):
                break
            elif event in ('inst','Key In Data'):
                window.close()    
                _onetm()
            elif event == 'Load Input Data [.csv]':  
                #window['inputname'].update(values['csv_loc'])
                    
                ###load_csv()
                meteoNrad                       = pd.read_csv(values['csv_loc'])                                # meteoNrad.head()
                rg                              = np.array(meteoNrad['rg'])
                ta                              = np.array(meteoNrad['ta']) + 273.15                            # ta loaded in [C]
                rh                              = np.array(meteoNrad['rh'])
                doy                             = np.array(meteoNrad['doy'])
                
                #inputs               
                if 'figrg' in locals():                 #if 'figrg' in locals(): del figrg, figrh, fig
                        delete_figure_agg(figure_rg)
                        delete_figure_agg(figure_rh)
                        delete_figure_agg(figure_ta)
                figrg                           = matplotlib.figure.Figure(figsize=(4,0.8),dpi=100, facecolor="#677787")
                #figrg.patch.set_alpha(0.0)
                figrg.add_subplot(111, facecolor="#677787").plot(doy[-2000:-1000],rg[-2000:-1000],'w');figrg.suptitle('Rg [W.m$^{-2}$]',color='white',fontsize=9)#;figrg.supylabel('rg')
                figrh                           = matplotlib.figure.Figure(figsize=(4,0.8),dpi=100, facecolor="#677787")
                figrh.add_subplot(111, facecolor="#677787").plot(doy[-2000:-1000],rh[-2000:-1000],'w');figrh.suptitle('RH [%]',color='white',fontsize=9)#;figrh.supylabel('rh')
                fig                             = matplotlib.figure.Figure(figsize=(4,0.8),dpi=100, facecolor="#677787")
                fig.add_subplot(111, facecolor="#677787").plot(doy[-2000:-1000],ta[-2000:-1000],'w');fig.suptitle('Tair [K]',color='white',fontsize=9)#;fig.supylabel('ta')
                
                figure_rg                       = draw_figure(window['indat_canvas'].TKCanvas,figrg)
                figure_rh                       = draw_figure(window['indat_canvas'].TKCanvas,figrh)
                figure_ta                       = draw_figure(window['indat_canvas'].TKCanvas,fig)

                run_pySP.update(disabled=False)
            elif event == 'RUN pySPARSE':
                #window['inputname'].update('xxxxx')
                ### run pySPARSE
                run_pySP.update(disabled=True)
                Save_SP.update(disabled=True)
                [seboutput]                     = runSPtm(meteoNrad)#,progress_bar)
                Save_SP.update(disabled=False)
                
                #outputs
                if 'figle' in locals():                 #if 'figle' in locals(): del figle, figh, figg, figrn, figrnsp, figlesp
                        delete_figure_agg(figure_le)
                        delete_figure_agg(figure_h)
                        delete_figure_agg(figure_g)
                        delete_figure_agg(figure_rn)
                        delete_figure_agg(figure_lesp)
                        delete_figure_agg(figure_rnsp)
                        
                figle                           = matplotlib.figure.Figure(figsize=(4,0.55),dpi=100, facecolor="#677787")
                figle.add_subplot(111, facecolor="#677787").plot(doy[-2000:-1000],seboutput['le'][-2000:-1000],'w');figle.supylabel('$\lambda$E',fontsize=9)
                figh                            = matplotlib.figure.Figure(figsize=(4,0.55),dpi=100, facecolor="#677787")
                figh.add_subplot(111, facecolor="#677787").plot(doy[-2000:-1000],seboutput['h'][-2000:-1000],'w');figh.supylabel('H',fontsize=9)
                figg                            = matplotlib.figure.Figure(figsize=(4,0.55),dpi=100, facecolor="#677787")
                figg.add_subplot(111, facecolor="#677787").plot(doy[-2000:-1000],seboutput['g'][-2000:-1000],'w');figg.supylabel('G',fontsize=9)
                figrn                           = matplotlib.figure.Figure(figsize=(4,0.55),dpi=100, facecolor="#677787")
                figrn.add_subplot(111, facecolor="#677787").plot(doy[-2000:-1000],seboutput['rn'][-2000:-1000],'w');figrn.supylabel('Rn',fontsize=9)
                figrnsp                         = matplotlib.figure.Figure(figsize=(1.8,1.8),dpi=100, facecolor="#677787")
                figrnsp.add_subplot(111, facecolor="#677787").plot([-200,800],[-200,800],'k-',np.array(meteoNrad['rnobs'])[-2000:-1000],seboutput['rn'][-2000:-1000],'w.');figrnsp.suptitle('Est. vs Obs. Rn [W.m$^{-2}$]',color='white',fontsize=8)#;figrn.supylabel('rn')
                figlesp                         = matplotlib.figure.Figure(figsize=(1.8,1.8),dpi=100, facecolor="#677787")
                figlesp.add_subplot(111, facecolor="#677787").plot([-200,800],[-200,800],'k-',np.array(meteoNrad['leobs'])[-2000:-1000],seboutput['le'][-2000:-1000],'w.');figlesp.suptitle('Est. vs Obs. $\lambda$E [W.m$^{-2}$]',color='white',fontsize=8)#;figrn.supylabel('rn')

                figure_le                       = draw_figure(window['outdat_canvas'].TKCanvas,figle)
                figure_h                        = draw_figure(window['outdat_canvas'].TKCanvas,figh)
                figure_g                        = draw_figure(window['outdat_canvas'].TKCanvas,figg)
                figure_rn                       = draw_figure(window['outdat_canvas'].TKCanvas,figrn)
                figure_lesp                     = draw_figure(window['lesp_canvas'].TKCanvas,figlesp)
                figure_rnsp                     = draw_figure(window['rnsp_canvas'].TKCanvas,figrnsp)
                '''
                elif event == 'next_sp':
                count                           = values[event]
                progress_bar.UpdateBar(count,100)
                window.refresh()
                '''
            elif event == 'Save Results':
                dttime=datetime.now()
                #try:
                file_nm = values['csv_outloc'] + '/SPARSE_SEB_' + str(dttime.year*100000000 + dttime.month*1000000 + dttime.day*10000 + dttime.hour*100 + dttime.minute) + '.csv'                
                np.savetxt(file_nm,np.transpose(np.asarray([meteoNrad['doy'],meteoNrad['rnobs'],meteoNrad['leobs'],meteoNrad['hobs'],meteoNrad['gobs']
                                                            ,seboutput['rn'],seboutput['le'],seboutput['lev'],seboutput['les'],seboutput['h'],seboutput['hv'],seboutput['hs'],seboutput['g']]))
                           ,delimiter=",",header="doy,rnobs,leobs,hobs,gobs,rnest_SPARSE,leest_SPARSE,levest_SPARSE,lesest_SPARSE,hest_SPARSE,hvest_SPARSE,hsest_SPARSE,gest_SPARSE",comments="")
                #except:
                #        ctypes.windll.user32.MessageBoxW(0, "Please select a valid saving directory !", "Saving ERROR", 1)
                        
        
            elif event == 'SPARSE SEB':
                sg.Popup('The pySPARSE model [Soil Plant Atmosphere Remote Sensing Evapotranspiration] \n\nTheory : https://doi.org/10.5194/hess-19-4653-2015 \n\n --- ufu v0.0.1 090923 ---',title='pySPARSE v0.0.1',background_color='#909090',button_color='#707070')    
            elif event == 'rf':
                browser.open('https://runningfingers.com/seb.php')    
                
        
        window.Close()

def _mainwin():
        use_custom_titlebar                     = True if sg.running_trinket() else False
        if use_custom_titlebar:
                Menu                            = sg.MenubarCustom     
        else:
                Menu                            = sg.Menu
        
        layout_l = [[sg.Image(filename=resource_path('RB_EBsm.png'))] ]
        layout_r = [[sg.T('pySPARSE',font='_ 14',justification='c',expand_x=True)],
                    [sg.Text('Instantaneous or continuous inputs ?')],
                    [sg.Button("One Instance", key="inst",expand_x=True),sg.Button("Time Series", key="cont",expand_x=True)],
                    [sg.Text(key='locktext', font='_ 8')] ]        
        layout   = [[Menu([['File', ['Input Mode',['Key in Model Inputs','Use Timeseries Dataset'],'Exit']],['About',['SPARSE SEB', ]]],k='-CUST MENUBAR-',p=0)],
                  [sg.Col(layout_l, p=0),sg.VSep(color='#666666'),sg.Col(layout_r, p=0)],
                  [sg.Text('Surface Energy Balance | SPARSE', font='_ 7',enable_events=True,expand_x=True,justification='c',key='rf')]]
        window                                  = sg.Window('pySPARSE v0.0.1',icon=resource_path('rf.ico')).Layout(layout)
        #window                                  = sg.Window('SPARSE : soil plant atmosphere remote sensing evapotranspiration',layout,use_custom_titlebar=use_custom_titlebar)

        while True:                             # Event Loop
            event, values                       = window.Read()
            if event in (None, 'Exit'):
                break
            elif event in ('inst','Key in Model Inputs'):
                #window.close()                window['locktext'].update('... close other window to continue !')
                _onetm()
            elif event in ('cont','Use Timeseries Dataset'):
                #window.close()                window['locktext'].update('... close other nwindow to continue !')
                _tmseries()
            elif event == 'SPARSE SEB':
                sg.Popup('The pySPARSE model [Soil Plant Atmosphere Remote Sensing Evapotranspiration] \n\nTheory : https://doi.org/10.5194/hess-19-4653-2015 \n\nContact : gilles.boulet@ird.fr \n\n --- ufu v0.0.1 090923 ---',title='pySPARSE v0.0.1',background_color='#909090',button_color='#707070')    
            elif event == 'rf':
                browser.open('https://doi.org/10.5194/hess-19-4653-2015')        
        
        window.Close()

if __name__ == "__main__":
    _mainwin()


#--uΓu--
