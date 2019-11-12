"""
Favor não alterar as estruturas e de controle e estruturas de dados sem ter absoluta certeza do que está fazendo. Sempre faça um backup do core original.

"""
import dash_table_experiments
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import dash_table_experiments as dash_table
import dash
from dash.dependencies import Input, Output
import dash_table
import pandas as pd

df1 = pd.read_csv('orderlines.csv', encoding='latin-1', low_memory=False)
df1.rename(columns={"Order Type": "OrderType"}, inplace=True)
df1.rename(columns={df1.columns[40]:'ProcessFinishTime'}, inplace=True)
df1.rename(columns={df1.columns[30]:'ProcessStartTime'}, inplace=True)


# Convertendo tempos

df1.loc[(df1.ProcessFinishTime == '::'), 'ProcessFinishTime'] = 0
df1.loc[(df1.ProcessStartTime == '::'), 'ProcessStartTime'] = 0


df1['ProcessFinishTime'] = pd.to_datetime(df1['ProcessFinishTime'],errors='ignore')
df1['ProcessStartTime'] = pd.to_datetime(df1['ProcessStartTime'],errors='ignore')
df1['TimeOfProcess'] = df1['ProcessFinishTime'] - df1['ProcessStartTime']
df1['TimeOfProcess'] = pd.to_datetime(df1['TimeOfProcess'],errors='ignore')




#Teste De Processamento

df1.loc[(df1.Processed != '::'), 'Unidades Processadas'] = df1['Qty']
df1.loc[(df1.Processed == '?'), 'Unidades Processadas'] = 0
df1.loc[(df1.Processed == '::'), 'Unidades Processadas'] = 0




# Agrupamentos


df2 = df1.groupby('OrderType').sum()

df3 = df1.groupby(' Packout station Number').sum()
df4 = df1.groupby('Packout station Operator').sum()
df5 = df1.groupby('Product Category').sum()
df1.rename(columns={df1.columns[12]:'Received Time'}, inplace=True)
df6 = df1.groupby('Received Time').sum()
df7 = df1.groupby('Cut Off Time').sum()

# Convertendo tempos


df1['ProcessFinishTime'] = pd.to_datetime(df1['ProcessFinishTime'])
df1['ProcessStartTime'] = pd.to_datetime(df1['ProcessStartTime'])
df1['TimeOfProcess'] = df1['ProcessFinishTime'] - df1['ProcessStartTime']
df1['TimeOfProcess'] = pd.to_datetime(df1['TimeOfProcess'])


# Calculando unidades processadas por hora

df8 = df1.groupby('OrderType').sum()

# Resetando indices

df2.reset_index(inplace=True)
df3.reset_index(inplace=True)
df4.reset_index(inplace=True)
df5.reset_index(inplace=True)
df6.reset_index(inplace=True)
df7.reset_index(inplace=True)

#Igualando Categorias

df5['Product Category'] = df5['Product Category'].str.upper()

df2['TimeOfProcess'] = df1['TimeOfProcess']

df2['Time Proc Seg'] = 0
df2['Time Proc Seg'] = df1['ProcessFinishTime'] - df1['ProcessStartTime']
df2['Time Proc Seg'] = df2['Time Proc Seg'].dt.total_seconds().astype(int)
df2['Unidades Pendentes'] = df1['Qty'] - df1['Unidades Processadas']
df2['Horas Trabalhadas'] = (df2['Time Proc Seg'] / 3600).round(2)
df2['Unidades/ Hora'] = (df2['Unidades Processadas'] / df2['Horas Trabalhadas']).round(2)
df2['Tempo Por Unidade (H)'] = (df2['Horas Trabalhadas'] / df2['Unidades Processadas']).round(6)
df2['ETA 9(H)'] = (df2['Tempo Por Unidade (H)'] * df2['Unidades Pendentes']).round(2)

dftable1 = df2
dftable1.drop(['Order No', 'Line','Order No','PickNO','TimeOfProcess','Etch Line','Time Proc Seg'], axis=1, inplace=True)

app = dash.Dash()
app.layout = html.Div([
    html.H1(children = "Dashboard Para Gestão De Produção",
    style = {'textAlign' : 'center',}),
        html.Div(children = "_______________________________",
                 style = {'textAlign' : 'center',}),

    
html.Div([
    
dash_table.DataTable(
    id='table',
    columns=[{"name": i, "id": i} for i in df2.columns],
     data=dftable1.to_dict('records'),
    #table_style={'padding-left': '10%','padding-right': '10%'},
     style_as_list_view=False,
    style_cell={'padding': '5px','fontSize': 20},
    style_header={
        'backgroundColor': 'white',
        'fontWeight': 'bold',
        'fontSize': 20},
     
     
),
    
    ],style={'textAlign': 'center',
             'align-items': 'center',
             'fontSize': 15,
             'width': '100%',
             'display': 'flex',
             'align-items': 'center',
             'justify-content': 'center'}),
    
    
    dcc.Graph(
        id = 'lines-chart',
        figure = {
            'data' : [
        {'x': df2['OrderType'], 'y': df2['Qty'],                'type': 'bar', 'name': 'Dropado'},
        {'x': df2['OrderType'], 'y': df2['Unidades Processadas'], 'type': 'bar', 'name': 'Realizado'}
        
            
            ],
            'layout' : {
                'title': 'Grafico'
            }
        }
    ),
    
   
    
    
    
    dcc.Graph(
        id = 'linehart',
        figure = {
            'data' : [
        {'x': df3[' Packout station Number'], 'y': df3['Unidades Processadas'], 'type': 'bar', 'name': 'Unidades / Hora'},
        #{'x': ['DCO13','DCO14','DCO15'], 'y': [37,78,43], 'type': 'line', 'name': 'DNs / Hora'}
        
            ],
            'layout' : {
                'title': 'Qty Processada Por Estação'
            }
        }
    ),
    
        dcc.Graph(
        id = 'linehaaaaart',
        figure = {
            'data' : [
        {'x': df4['Packout station Operator'], 'y': df4['Unidades Processadas'], 'type': 'bar', 'name': 'Unidades / Hora'},
        #{'x': ['DCO13','DCO14','DCO15'], 'y': [37,78,43], 'type': 'line', 'name': 'DNs / Hora'}
        
            ],
            'layout' : {
                'title': 'Qty Processada Por Operador'
            }
        }
    ),
    
    dcc.Graph(
        id = 'linehaaaaartz',
        figure = {
            'data' : [
        {'x': df5['Product Category'], 'y': df5['Qty'], 'type': 'bar', 'name': 'Dropado'},
        {'x': df5['Product Category'], 'y': df5['Unidades Processadas'],'type': 'bar', 'name': 'Realizado'}
        
            ],
            'layout' : {
                'title': 'Unidades Por Categoria'
            }
        }
    ),
    
    dcc.Graph(
        id = 'dropchart',
        figure = {
            'data' : [
        {'x': df6['Received Time'], 'y': df6['Qty'], 'type': 'line', 'name': 'Dropado'},
        {'x': df6['Received Time'], 'y': df6['Unidades Processadas'],'type': 'line', 'name': 'Realizado'}
        
            ],
            'layout' : {
                'title': 'Drops'
            }
        }
    ),
    
    dcc.Graph(
        id = 'cutofpogress',
        figure = {
            'data' : [
        {'x': df7['Cut Off Time'], 'y': df7['Qty'], 'type': 'bar', 'name': 'Dropado'},
        {'x': df7['Cut Off Time'], 'y': df7['Unidades Processadas'],'type': 'bar', 'name': 'Realizado'}
        
            ],
            'layout' : {
                'title': 'CutOff Progress'
            }
        }
    ),
    
   
    
])

if __name__ == '__main__':
    app.run_server(port =4050)
