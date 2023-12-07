import json
import plotly.express as px
from django.shortcuts import render, redirect, get_object_or_404
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
    context = {'sql_data_rows': sql_data_rows}
    return render(request, 'sql.html', context)


#I can work with both Function and Class based views 
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
        
        if 'edit' in request.POST:
           if form.is_valid():
               form.save()
               return redirect('sql')
        
        if 'delete' in request.POST:
            row.delete()
            return redirect('sql')            
        
        context = {'row': row, 'form': form}
        return render(request, self.template_name, context )
    
    
    ''' This next part is for visual charts
    '''
def line_chart(request):
    data= SQLMODEL.objects.all()
        
    fig=px.line(
        x=[c.date_column for c in data],
        y=[c.close_column for c in data],
        title='Close over Time Chart',
        labels ={'x':'Date', 'y':'Close'}
        )
    
        
    chart =fig.to_html()
        
    context ={'chart': chart}
    return render(request, 'charts.html', context)