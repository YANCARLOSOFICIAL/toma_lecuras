from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import render,redirect
from django.http import JsonResponse
from .models import Barrio, Suscriptor, Micromedidor, SuscriptorMicromedidor, Lectura
from .forms import BarrioForm, SuscriptorForm, MicromedidorForm, SuscriptorMicromedidorForm, LecturaForm
from calendar import month_name
from datetime import datetime  
from django.utils import timezone 

def indexbarrio(request):  
    barrios=Barrio.objects.all()
    return render(request,'Barrio/indexbarrio.html',{'barrios':barrios} ) 

def crearbarrio(request):
    formulario = BarrioForm(request.POST or None,request.FILES or None)
    if formulario.is_valid():      
        formulario.save()    
        return redirect('indexbarrio')
    return render(request,'Barrio/crear.html',{'formulario':formulario})

def editarbarrio(request, id):
    barrios = get_object_or_404(Barrio, id=id) 
    formulario = BarrioForm(request.POST or None, instance=barrios)

    if formulario.is_valid():
        formulario.save()
        return redirect('indexbarrio')

    return render(request, 'Barrio/editar.html', {'formulario': formulario, 'barrio': barrios}) 

def eliminarbarrio(request, id):
    barrio = get_object_or_404(Barrio, id=id)
    
    if request.method == 'POST':
        barrio.delete()
        return redirect('indexbarrio') 

    return render(request, 'Barrio/eliminar.html', {'barrio': barrio}) 




def lista_barrios(request):
    barrios = Barrio.objects.all()
    return render(request, 'Barrio/indexbarrio.html', {'barrio': barrios})  


#####################################################################################






def indexmicromedidor(request):  
    micromedidores=Micromedidor.objects.all()
    return render(request,'Micromedidor/indexmicromedidor.html',{'micromedidores':micromedidores} ) 

def crearmicromedidor(request):
    if request.method == 'POST':
        formulario = MicromedidorForm(request.POST or None, request.FILES or None)
        if formulario.is_valid():
            # Verificar si el valor del campo 'nuid' ya existe en la base de datos
            nuid = formulario.cleaned_data.get('nuid')
            if Micromedidor.objects.filter(nuid=nuid).exists():
                # Si el 'nuid' ya existe, mostrar un mensaje de error en el formulario
                formulario.add_error('nuid', 'El NUID ya existe. Por favor ingrese un valor diferente.')
            else:
                # Guardar el formulario si es válido y el 'nuid' no existe     
                formulario.save()
                return redirect('indexmicromedidor')
    else:
        formulario = MicromedidorForm()
    return render(request, 'Micromedidor/crear.html', {'formulario': formulario}) 

def editarmicromedidor(request, id):
    micromedidor = get_object_or_404(Micromedidor, pk=id)
    formulario = MicromedidorForm(request.POST or None, instance=micromedidor)
    if request.method == 'POST':
        if formulario.is_valid():
            nuevo_nuid = formulario.cleaned_data.get('nuid')
            if Micromedidor.objects.exclude(id=id).filter(nuid=nuevo_nuid).exists():
                formulario.add_error('nuid', 'Este NUID ya está en uso. Por favor, ingrese uno diferente.')
            else:
                formulario.save()
                return redirect('indexmicromedidor')
    return render(request, 'Micromedidor/editar.html', {'formulario': formulario, 'micromedidor': micromedidor})

def eliminarmicromedidor(request, id):
    micromedidor = get_object_or_404(Micromedidor, id=id)
    
    if request.method == 'POST':
        micromedidor.delete() 
        return redirect('indexmicromedidor') 

    return render(request, 'Micromedidor/eliminar.html', {'micromedidor': micromedidor})




def lista_micromedidores(request):
    micromedidores = Micromedidor.objects.all()
    return render(request, 'Micromedidor/indexmicromedidor.html', {'micromedidores': micromedidores}) 




#######################################################################################################



def indexsuscriptor(request):  
    suscriptores=Suscriptor.objects.all()
    return render(request,'Suscriptor/indexsuscriptor.html',{'suscriptores':suscriptores} ) 

def crearsuscriptor(request):
    barrios = Barrio.objects.all()  # Define barrios fuera del bloque condicional
    if request.method == 'POST':
        form = SuscriptorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('indexsuscriptor')  # Cambia esto al nombre de tu vista de índice de Suscriptor
    else:
        form = SuscriptorForm() 
    return render(request, 'Suscriptor/crear.html', {'form': form, 'barrios': barrios})

def editarsuscriptor(request, id):
    suscriptor = get_object_or_404(Suscriptor, id=id)
    
    if request.method == 'POST':
        formulario = SuscriptorForm(request.POST, instance=suscriptor)
        if formulario.is_valid():
            formulario.save()
            return redirect('indexsuscriptor')
    else:
        formulario = SuscriptorForm(instance=suscriptor)

    # Obtener todos los barrios disponibles
    barrios = Barrio.objects.all()

    return render(request, 'Suscriptor/editar.html', {'formulario': formulario, 'barrios': barrios})

def eliminarsuscriptor(request, id):
    suscriptor = get_object_or_404(Suscriptor, id=id) 
    
    if request.method == 'POST':
        suscriptor.delete()
        return redirect('indexsuscriptor')

    return render(request, 'Suscriptor/eliminar.html', {'suscriptor': suscriptor})




def lista_suscriptor(request):
    suscriptores = Suscriptor.objects.all()
    return render(request, 'Suscriptor/indexsuscriptor.html', {'suscriptores': suscriptores}) 


#########################################################################################################



def indexsuscriptormicromedidor(request): 
    suscriptoresmicromedidores = SuscriptorMicromedidor.objects.all()
    return render(request, 'SuscriptorMicromedidor/indexsuscriptorMicromedidor.html', {'suscriptormicromedidor': suscriptoresmicromedidores})

def crearsuscriptormicromedidor(request):
    suscriptores = Suscriptor.objects.all()
    micromedidores = Micromedidor.objects.all()
    
    if request.method == 'POST':
        form = SuscriptorMicromedidorForm(request.POST) 
        if form.is_valid():
            # Procesar el formulario aquí si es válido
            form.save()
            return redirect('indexsuscriptorMicromedidor')# Redirigir a la página de éxito o a donde corresponda
    else:
        form = SuscriptorMicromedidorForm()
    
    return render(request, 'SuscriptorMicromedidor/crear.html', {'form': form, 'suscriptores': suscriptores, 'micromedidores': micromedidores})

def editarsuscriptormicromedidor(request, id):
    suscriptor_micromedidor = get_object_or_404(SuscriptorMicromedidor, id=id) 
    suscriptores = Suscriptor.objects.all()
    micromedidores = Micromedidor.objects.all() 
    
    if request.method == 'POST':
        form = SuscriptorMicromedidorForm(request.POST, instance=suscriptor_micromedidor)
        if form.is_valid():
            form.save()
            # Redirigir a la página de éxito o a donde corresponda
            return redirect('indexsuscriptorMicromedidor')
    else:
        form = SuscriptorMicromedidorForm(instance=suscriptor_micromedidor)
    
    return render(request, 'SuscriptorMicromedidor/editar.html', {'form': form, 'suscriptores': suscriptores, 'micromedidores': micromedidores})

def eliminarsuscriptormicromedidor(request, id):
    suscriptor_micromedidor = get_object_or_404(SuscriptorMicromedidor, id=id)
    if request.method == 'POST':
        suscriptor_micromedidor.delete()
        return redirect('indexsuscriptorMicromedidor')
    return render(request, 'suscriptorMicromedidor/eliminar.html', {'suscriptor_micromedidor': suscriptor_micromedidor})


#############################################################################################################




def indexlectura(request):
    lecturas = Lectura.objects.all()
    return render(request, 'Lectura/indexlectura.html', {'lecturas': lecturas})

def crearlectura(request):
    if request.method == 'POST':
        form = LecturaForm(request.POST)
        if form.is_valid():
            lectura_nueva = form.save(commit=False)
            
            # Obtener la lectura anterior si existe
            suscriptor = lectura_nueva.suscriptor_micromedidor
            lectura_anterior = Lectura.objects.filter(
                suscriptor_micromedidor=suscriptor
            ).order_by('-FechaLectura').exclude(id=lectura_nueva.id).first() 

            if lectura_anterior:
                lectura_nueva.lectura_anterior = lectura_anterior.lectura_actual
                lectura_nueva.consumototal = lectura_nueva.lectura_actual - lectura_anterior.lectura_actual
            else:
                # Si no hay lectura anterior, consumototal es igual a la lectura actual
                lectura_nueva.consumototal = lectura_nueva.lectura_actual

            # Guardar la fecha y hora actual como FechaLectura (auto_now_add=True)
            lectura_nueva.save()
            return redirect('indexlectura')  
    else:
        # Si es una solicitud GET, inicializa un nuevo formulario
        form = LecturaForm()

    # Obtener suscriptores para el formulario
    suscriptores_micromedidores = SuscriptorMicromedidor.objects.all()

    

    # Renderizar la plantilla con el formulario y otros datos necesarios
    return render(request, 'Lectura/crear.html', {
        'form': form,
        'suscriptores_micromedidores': suscriptores_micromedidores,
        
    })

def editarlectura(request, id):
    lectura = get_object_or_404(Lectura, id=id)
    if request.method == 'POST':
        form = LecturaForm(request.POST, instance=lectura)
        if form.is_valid():
            lectura = form.save(commit=False)
            lectura.save()
            return redirect('indexlectura')
    else:
        form = LecturaForm(instance=lectura)
    suscriptores_micromedidores = SuscriptorMicromedidor.objects.all()
    return render(request, 'Lectura/editar.html', {'form': form, 'lectura': lectura, 'suscriptores_micromedidores': suscriptores_micromedidores})

def eliminarlectura(request, id):
    lectura = get_object_or_404(Lectura, id=id)
    if request.method == 'POST':
        lectura.delete()
        return redirect('indexlectura')
    return render(request, 'Lectura/eliminar.html', {'lectura': lectura}) 
    
def obtener_lectura_anterior_api(request, suscriptor_id):
    try:
        # Obtener la lectura anterior para el suscriptor especificado
        lectura_anterior = Lectura.objects.filter(
            suscriptor_micromedidor__id=suscriptor_id
        ).order_by('-FechaLectura').exclude(id=request.GET.get('lectura_id', 0)).first()

        if lectura_anterior:
            # Construir el JSON con los datos necesarios
            data = {
                'mes_anterior': lectura_anterior.mes_actual,
                'mes_actual': lectura_anterior.mes_actual,
                # Otros datos necesarios aquí...
            }
            return JsonResponse(data)
        else:
            # Si no se encuentra ninguna lectura anterior
            return JsonResponse({'error': 'No se encontró ninguna lectura anterior para este suscriptor'}, status=404)
    except Exception as e:
        # Manejar cualquier error y devolver una respuesta de error
        return JsonResponse({'error': str(e)}, status=500)   







