import external, checklists_final, reports

"""
    Obtiene la información contextual de cada contenedor identificado
    ids_containers: identificadores de los contenedores que componen el sistema de eSalud
    cfg: objeto que representa la información del archivo de configuracion que despliega el sistema de  eSalud

"""
def get_context_information(ids_containers, cfg):
    context_information = ''
    for source in checklists_final.SOURCES:
        if source == checklists_final.SOURCE_CFG_FILE: #local file - get context information from cfg file [NRF]
            #print(cfg['NFR'])
            if 'NFR' in cfg:
                nrfs = cfg['NFR']
                
                for nrf in nrfs:
                    if not nrf['name'].upper() in context_information:
                        context_information += f"{nrf['name']}\n".upper()
        else:
            responses = external.api_call_resolver(source, ids_containers)
            for response in responses:
                if 'running' in response['status']:
                    context_information += f"{response['description'].upper()}\n"
    return context_information

"""
    Verificar cumplimiento de un checklist
        - Consulta la información contextual de los contenedores, ya sea de los SOURCES(APIs) o de los archivos de configuración
        - Verifica los requerimientos con base en las palabras clave y la información contextual
"""
def verify_checklist(checklist, context_information):
    checks = 0
    number_requirements = 0
    number_assisted_requirements = 0

    for requirement in checklist['requirements']:
        number_requirements += 1
        if requirement['assisted']:
            number_assisted_requirements += 1
            continue
        if any((keyword in context_information or keyword == "CDN") for keyword in requirement['keywords']):
            requirement['compliance'] = True
            checks += 1
    return checklist, checks, (checks/number_requirements) * 100.0, number_requirements, number_assisted_requirements

def compliance(cfg, js, yml, output_path):
    #get containers ids
    ids_containers = [container['id'] for container in js['containers']]

    #get containers context information
    context_information = get_context_information(ids_containers, cfg)

    #compute COBIT compliance,
    COBIT, compliance, percentage, number_requirements, n_asisted_requirements = verify_checklist(checklists_final.COBIT, context_information)
    #generate report
    reports.generate_checklist_report(COBIT, compliance, percentage, number_requirements, n_asisted_requirements, output_path)
    reports.generate_checklist_graph(COBIT, percentage, output_path)
    
    #compute ISO compliance,
    ISO, compliance, percentage, number_requirements, n_asisted_requirements = verify_checklist(checklists_final.ISO, context_information)
    #generate report
    reports.generate_checklist_report(ISO, compliance, percentage, number_requirements, n_asisted_requirements, output_path)
    reports.generate_checklist_graph(ISO, percentage, output_path)

    #compute NIST compliance,
    NIST, compliance, percentage, number_requirements, n_asisted_requirements = verify_checklist(checklists_final.NIST, context_information)
    #generate report
    reports.generate_checklist_report(NIST, compliance, percentage, number_requirements, n_asisted_requirements, output_path)
    reports.generate_checklist_graph(NIST, percentage, output_path)

    #compute NOM compliance,
    MEX, compliance, percentage, number_requirements, n_asisted_requirements = verify_checklist(checklists_final.MEX, context_information)
    #generate report
    reports.generate_checklist_report(MEX, compliance, percentage, number_requirements, n_asisted_requirements, output_path)
    reports.generate_checklist_graph(MEX, percentage, output_path)

    #you can add more rules...






    
