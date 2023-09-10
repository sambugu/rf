'''
GUI for running pySPARSE - py Soil Plant Atmosphere Remote Sensing Evapotranspiration - Boulet et al. (2015)

-- ufu --  from 080923 ...made using pysimplegui [.exe compiled using pyinstaller]
'''

import os
import PySimpleGUI as sg
import pySPARSE as pySP
from math import floor
import webbrowser as browser

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
                  [sg.Push() , sg.Button("RUN SPARSE",s=17,button_color=('white','#008040'))] ]
        layout_r = [
                  [sg.T('Surface Energy Balance (SEB) Estimates',font='_ 14',justification='c',expand_x=True)],
                  [sg.TabGroup([[sg.Tab('Overall Fluxes [W/m²]',[[sg.T(key="OutputTot",justification='c',font='_ 12',expand_x=True)]]),
                                 sg.Tab('Partitioning [W/m²]', [[sg.T(key="OutputPart",justification='c',font='_ 12',expand_x=True)]])]],font='_ 13')] ]

                  #[sg.Push() , sg.Button("Reset") , sg.Button("run SPARSE",button_color=('white','#008040'))] ]
        layout   = [[Menu([['File', ['Timeseries',['Open CSV [wip]','Save Output [wip]'],'Exit']],['About',['SPARSE SEB', ]]],k='-CUST MENUBAR-',p=0)],              
                      [sg.Col(layout_l, p=0), sg.Col(layout_r, p=0)],
                  [sg.Text('www.runningfingers.com', font='_ 8',enable_events=True,expand_x=True,justification='c',key='rf')]]
        
        window                                  = sg.Window('pySPARSE : soil plant atmosphere remote sensing evapotranspiration',icon=resource_path('rf.ico')).Layout(layout)
        #window                                  = sg.Window('SPARSE : soil plant atmosphere remote sensing evapotranspiration',layout,use_custom_titlebar=use_custom_titlebar)

        while True:                             # Event Loop
            event, values                       = window.Read()
            if event in (None, 'Exit'):
                break
            elif event == 'RUN SPARSE':
                [LE,H,rn,G,LEv,LEs,Tv,Ts,Tsf]   = runSP(values)
                outputTot                       = f"\n LE: {LE} \n H:  {H} \n Rn: {rn} \n G:  {G}\n" ### output                          = f"LE: {LE} | H: {H} | Rn: {rn} | G: {G} \n LEv: {LEv} | LEs: {LEs}"# | Tv: {Tv} | Ts: {Ts}"
                outputPart                      = f"\n LEv: {LEv} \n LEs: {LEs}"# | Tv: {Tv} | Ts: {Ts}"
                window['OutputTot'].update(outputTot)                                         ### window['Output'].update(output)
                window['OutputPart'].update(outputPart)
            elif event == 'SPARSE SEB':
                sg.Popup('The pySPARSE model [Soil Plant Atmosphere Remote Sensing Evapotranspiration] \n\nTheory : https://doi.org/10.5194/hess-19-4653-2015 \n\n --- ufu v0.0.1 090923 ---',title='pySPARSE v0.0.1',background_color='#909090',button_color='#707070')
            elif event == 'rf':
                browser.open('https://runningfingers.com/seb.php')

        window.Close()

def _tmseries():
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
                    [sg.Button("One Instance", key="inst",expand_x=True),sg.Button("Time Series", key="cont",expand_x=True)] ]        
        layout   = [[Menu([['File', ['Input Mode',['Key in Model Inputs','Use Timeseries Dataset'],'Exit']],['About',['SPARSE SEB', ]]],k='-CUST MENUBAR-',p=0)],
                  [sg.Col(layout_l, p=0),sg.VSep(color='#666666'),sg.Col(layout_r, p=0)],
                  [sg.Text('www.runningfingers.com', font='_ 7',enable_events=True,expand_x=True,justification='c',key='rf')]]
        window                                  = sg.Window('pySPARSE : soil plant atmosphere remote sensing evapotranspiration',icon=resource_path('rf.ico')).Layout(layout)
        #window                                  = sg.Window('SPARSE : soil plant atmosphere remote sensing evapotranspiration',layout,use_custom_titlebar=use_custom_titlebar)

        while True:                             # Event Loop
            event, values                       = window.Read()
            if event in (None, 'Exit'):
                break
            elif event in ('inst','Key in Model Inputs'):
                _onetm()
            elif event in ('cont','Timeseries Input Dataset'):
                _tmseries()
            elif event == 'SPARSE SEB':
                sg.Popup('The pySPARSE model [Soil Plant Atmosphere Remote Sensing Evapotranspiration] \n\nTheory : https://doi.org/10.5194/hess-19-4653-2015 \n\n --- ufu v0.0.1 090923 ---',title='pySPARSE v0.0.1',background_color='#909090',button_color='#707070')    
            elif event == 'rf':
                browser.open('https://runningfingers.com/seb.php')        
        
        window.Close()

if __name__ == "__main__":
    _mainwin()


#--uΓu--
