import json
import pandas as pd

import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots

from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.views import View
from django.utils.dateparse import parse_date

from .models import SQLMODEL
from .forms import SqlModelForm


def homePage(request):
    data_rows = SQLMODEL.objects.all()
    context = {'data_rows': data_rows}
    return render(request, 'home.html', context)


def jsonModel(request):
    json_file_path = 'stock_market_data.json'

    with open(json_file_path, 'r') as file:
        json_data = file.read()
         
        payload = json.loads(json_data)
        context = {'json_data_rows':payload}
        return render (request,'json.html', context )
    

def save_json(request):
    json_file_path = 'stock_market_data.json'

    with open(json_file_path, 'r') as file:
        json_data = file.read()

    try:
        payload = json.loads(json_data)
        for item in payload:
            SQLMODEL.objects.create(
                date_column=parse_date(item.get('date', None)),
                trade_code_column=item.get('trade_code', None),
                high_column=item.get('high', None),
                low_column=item.get('low', None),
                open_column=item.get('open', None),
                close_column=item.get('close', None),
                volume_column=item.get('volume', None),
            )
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return redirect('sql')


def display_sqlModel(request):
    sql_data_rows = SQLMODEL.objects.all()
    data_count=sql_data_rows.count()
    
    if data_count == 0:
        return HttpResponse("Did you perhaps forget to import the data into the django sql model?")
    
    context = {'sql_data_rows': sql_data_rows}
    return render(request, 'sql.html', context)


'''i can work with both class based and function based views :)'''
class Update_Delete(View):
    
    template_name = 'update_delete.html'
    
    def get(self,request, pk):
        row = get_object_or_404(SQLMODEL, id=pk)
        form = SqlModelForm(instance=row)
        context = {'form':form}
        return render(request, self.template_name, context )
    
    
    def post(self,request, pk):
        row = get_object_or_404(SQLMODEL, id=pk)
        form = SqlModelForm(request.POST, instance=row)
        
        if 'edit' in request.POST and form.is_valid():
            form.save()
            return redirect('sql')
        
        if 'delete' in request.POST:
            row.delete()
            return redirect('sql')            
        
        context = {'row': row, 'form': form}
        return render(request, self.template_name, context )
    
    
    ''' This next part is for visual charts
    '''

class CombinedChartView(View):
    template_name = 'charts.html'

    def get(self, request):
        data = SQLMODEL.objects.all()
        data_count = data.count()
        if data_count == 0:
            return HttpResponse("Populate the SQL DB with the Json data first :)")

        x_line = [entry.date_column for entry in data]
        y_line = [entry.close_column for entry in data]

        x_bar = [entry.date_column for entry in data]
        y_bar = [entry.volume_column for entry in data]

        fig_line = px.line(
            x=x_line,
            y=y_line,
            title='Close/Date Chart',
            labels={'x': 'Date', 'y': 'Close'}
        )
        fig_line.update_layout(
            title={
                'font_size':22,
                'xanchor':'center',
                'x': 0.5
            }
        )

        fig_bar = px.bar(
            x=x_bar,
            y=y_bar,
            title='Volume/Date Chart',
            labels={'x': 'Date', 'y': 'Volume'}
        )
        fig_bar.update_layout(
            title={
                'font_size':22,
                'xanchor':'center',
                'x': 0.5
            }
        )

        df = pd.DataFrame({
            'Date': x_line,
            'Close': y_line,
            'Volume': y_bar,
        })

        multi_axis_fig = make_subplots(specs=[[{"secondary_y": True}]])
        
       
        multi_axis_fig.add_trace(
            go.Scatter(x=df['Date'], y=df['Close'], mode='lines', name='Close', line=dict(color='blue')),
            secondary_y=False
        )

        multi_axis_fig.add_trace(
            go.Bar(x=df['Date'], y=df['Volume'], name='Volume', marker=dict(color='orange')),
            secondary_y=True
        )
        
        multi_axis_fig.update_layout(
            
            title={
                'font_size':22,
                'xanchor':'center',
                'x': 0.5
            },
            
            xaxis=dict(title='Date'),
            yaxis=dict(title='Close', side='left', showgrid=False),
            yaxis2=dict(title='Volume', side='right', overlaying='y', showgrid=False)
        )

        line_chart = fig_line.to_html()
        bar_chart = fig_bar.to_html()
        multi_axis_chart = multi_axis_fig.to_html()

        context = {'line_chart': line_chart, 'bar_chart': bar_chart, 'multi_axis_chart': multi_axis_chart}
        return render(request, self.template_name, context)
