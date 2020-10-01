from doctrainingapp.views import *
#DECORATORS
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required



@login_required(login_url='')
def area_list(request, template_name='area-fase-list.html'):
    areas = AreaFase.objects.all()

    return render(request, template_name, {'areas': areas})

@login_required(login_url='')
def area_add(request, template_name='area-fase-add.html'):
    form = AreaFaseForm(request.POST or None)
    if form.is_valid():
        try:
            area_aux = AreaFase.objects.get(nome=request.POST['nome'])

            if area_aux:
                messages.error(request, 'Erro! Area ja existe.')
                # return redirect('/areas')
                return redirect(reverse_lazy("doctrainingapp:areas_fase_list"))
        except:
            form.save()
            # return redirect('/areas')
            return redirect(reverse_lazy("doctrainingapp:areas_fase_list"))
    return render(request, template_name, {'form': form})


@login_required(login_url='')
def area_edit(request, pk, template_name='area-fase-edit.html'):
    area= get_object_or_404(AreaFase, pk=pk)
    form = AreaFaseForm(request.POST or None, instance=area)
    if form.is_valid():
        form.save()
        # return redirect('/areas')
        return redirect(reverse_lazy("doctrainingapp:areas_fase_list"))
    return render(request, template_name, {'form':form})


@login_required(login_url='')
def area_delete(request, pk, template_name='area-fase-delete.html'):
    area = get_object_or_404(AreaFase, pk=pk)
    fases = Fase.objects.filter(area=area)
    if fases:
        messages.error(request, 'Erro! Area você não pode deletar essa Area pois existe fases contidas nela...')
        # return redirect('/areas')
        return redirect(reverse_lazy("doctrainingapp:areas_fase_list"))
    elif request.method == 'POST':
        area.delete()
        # return redirect('/areas')
        return redirect(reverse_lazy("doctrainingapp:areas_fase_list"))
    return render(request, template_name, {'object': area})
