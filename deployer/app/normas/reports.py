from texttable import Texttable #pip install texttable
import plotly.graph_objects as go #pip install plotly==5.3.1    pip install -U kaleido

"""
    Genera el reporte de cumplimiento del checklist dado:
        - Reporte en formato .txt del cumplimiento de las normas y porcentajes
"""
def generate_checklist_report(checklist, compliance, percentage, number_requirements, n_asisted_requirements, output_path):
    tabl = Texttable()
    tabl.add_row(['Rule', checklist['name']])
    tabl.add_row(['', ''])
    tabl.add_row(['Concept', 'Comply'])
    requirements = checklist["requirements"]
    for r in requirements:
        if r['assisted']:
            tabl.add_row([r['concept'], 'Assisted'])
        else:
            tabl.add_row([r['concept'], ("True" if r['compliance'] else "X") ])
            
    tabl.add_row(['', ''])
    tabl.add_row(['Compliance', str(percentage) + "%"])
    tabl.add_row(['If you comply assisted requirements', str(( (compliance+n_asisted_requirements) / (number_requirements) * 100.0)) + "%"])
    #print(tabl.draw().encode('utf-8'))
    #output report.txt
    f = open(f'{output_path}/{checklist["name"].strip()}_report.txt', 'w')
    f.write( str(tabl.draw().encode('utf-8')))
    f.close()

"""
     Genera Gráfico similar a un tacómetro donde se visualiza el porcentaje de cumplimiento del checklist
"""
def generate_checklist_graph(checklist, percentage, output_path):
    #output graph
    fig = go.Figure(go.Indicator(
    domain = {'x': [0, 1], 'y': [0, 1]},
    value = percentage,
    mode = "gauge+number",
    title = {'text': checklist['name'] + ' compliance %'},
    gauge = {
        'axis': {'range': [0.0, 100.0], 'tickwidth': 1, 'tickcolor': "black"},
        'bar': {'color': "black"},
        'bgcolor': "white",
        'borderwidth': 2,
        'bordercolor': "gray",
        'steps': [
            {'range': [0.0, 25.0], 'color': 'red'},
            {'range': [25.0, 50.0], 'color': 'orange'},
            {'range': [50.0, 75.0], 'color': 'yellow'},
            {'range': [75.0, 100.0], 'color': 'green'}]
        }
    ))
    fig.write_image(f'{output_path}/{checklist["name"].strip()}_compliance_graph.png')