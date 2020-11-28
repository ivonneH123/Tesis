import json
import xlsxwriter
def traducir_ruta(lista, pacientes):
    trad_ruta=[]
    for punto in lista:
        if isinstance(punto, int):
            trad_ruta.append(pacientes[str(punto)])
        else:
            trad_ruta.append(punto)
    return trad_ruta   


ruta_excels='D:/Ivonne/Documents/github/tesis/Tesis/solucion/excels'
ruta_json='D:/Ivonne/Documents/github/tesis/Tesis/solucion'

carpetas_json={'area_1_2':{'capacidad_20':'sol_area_1_2_3amb__cap20','capacidad_50':'sol_area_1_2_3amb__cap50','capacidad_70':'sol_area_1_2_3amb__cap70'},
               'area_3':{'capacidad_20':'sol_area_3_3amb__cap20','capacidad_50':'sol_area_3_3amb__cap50','capacidad_70':'sol_area_3_5amb__cap70'},
               'area_4':{'capacidad_20':'sol_area_4_2amb__cap20','capacidad_50':'sol_area_4_4amb__cap50','capacidad_70':'sol_area_4_6amb__cap70'},
               'area_5a_5b_5c_5d':{'capacidad_20':'sol_area_5a_5b_5c_5d_2amb__cap20','capacidad_50':'sol_area_5a_5b_5c_5d_6amb__cap50','capacidad_70':'sol_area_5a_5b_5c_5d_8amb__cap70'},
               'area_6a_6b':{'capacidad_20':'sol_area_6a_6b_2amb__cap20','capacidad_50':'sol_area_6a_6b_5amb__cap50','capacidad_70':'sol_area_6a_6b_6amb__cap70'}}
areas=['area_1_2','area_3','area_4','area_5a_5b_5c_5d','area_6a_6b']
capacidades=['capacidad_20','capacidad_50','capacidad_70']


for area in range(len(areas)):
    for cap in range(len(capacidades)):
        file_json=ruta_json+'/'+areas[area]+'/'+capacidades[cap]+'/'+carpetas_json[areas[area]][capacidades[cap]]+'.txt'

        with open(file_json) as json_file:
            data = json.load(json_file)
        #traducir rutas
        pacientes={num_pac:data['pacientes'][num_pac]['pma'] for num_pac in list(data['pacientes'].keys())}

        ambulancias_rutas={num_amb:data['ambulancias'][num_amb]['ruta'] for num_amb in list(data['ambulancias'].keys())}

        rutas_traducidas={}
        for amb in ambulancias_rutas.keys():
            trad_ruta=traducir_ruta(ambulancias_rutas[amb],pacientes)
            rutas_traducidas[amb]=trad_ruta


        # escribir todo en excel
        book = xlsxwriter.Workbook(ruta_excels+'/'+areas[area]+'/'+carpetas_json[areas[area]][capacidades[cap]]+'.xlsx')     
        workSheet = book.add_worksheet()
        row=1
        column=1

        #escribir capacidad y tiempo de ejecución
        workSheet.write(row,column,"Capacidad")
        workSheet.write(row,column+1,data['capacidad'])

        row+=1 # un espacio
        workSheet.write(row+1,column,"Tiempo de ejecución")
        workSheet.write(row+1,column+1,data["tiempo_ejecucion"])

        row+=1# un espacio
        #datos de la curva
        workSheet.write(row,column,'i')
        workSheet.write(row,column+1,'f(s)')

        for i in range(len(data['g']['i'])):
            row+=1
            workSheet.write(row,column,int(data['g']['i'][i]))
            workSheet.write(row,column+1,int(data['g']['f(s)'][i]))
        row+=1 # un espacio
        column_1=column
        # datos de los hospitales
        workSheet.write(row+1,column,'HOSPITALES')
        row+=2
        for h in list(data['hospitales'].keys()):
            workSheet.write(row,column_1,h)
            workSheet.write(row+1,column_1,data['hospitales'][h])
            column_1+=1

        row+=1 #un espacio
        workSheet.write(row+1,column,'AMBULANCIAS')
        workSheet.write(row+1,column+1,'hosp')
        workSheet.write(row+1,column+2,'tiempo_final')
        row+=1
        for amb in data['ambulancias'].keys():
            row+=1
            workSheet.write(row,column,amb)
            workSheet.write(row,column+1,str(rutas_traducidas[amb]))
            workSheet.write(row,column+2,data['ambulancias'][amb]['hosp'])
            workSheet.write(row,column+3,data['ambulancias'][amb]['tiempo_final'])
        #pacientes
        row+=1 # un espacio
        workSheet.write(row+1,column,'PACIENTES')
        workSheet.write(row+1,column+1,'pma')
        workSheet.write(row+1,column+2,'hosp')
        workSheet.write(row+1,column+3,'atendido')
        workSheet.write(row+1,column+4,'ambulancia')
        workSheet.write(row+1,column+5,'w')
        row+=1

        for pac in data['pacientes'].keys():
            row+=1
            workSheet.write(row,column,pac)
            workSheet.write(row,column+1,data['pacientes'][pac]['pma'])
            workSheet.write(row,column+2,data['pacientes'][pac]['hosp'])
            workSheet.write(row,column+3,data['pacientes'][pac]['atendido'])
            workSheet.write(row,column+4,data['pacientes'][pac]['ambulancia'])
            workSheet.write(row,column+5,data['pacientes'][pac]['w'])

        book.close()





