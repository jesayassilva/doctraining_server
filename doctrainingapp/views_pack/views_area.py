from doctrainingapp.views import *
#DECORATORS
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required



@login_required(login_url='')
@staff_member_required
def area_list(request, template_name='area-list.html'):
    areas = Area.objects.all()

    return render(request, template_name, {'areas': areas})

@login_required(login_url='')
@staff_member_required
def area_add(request, template_name='area-add.html'):
    form = AreaForm(request.POST or None)
    if form.is_valid():
        try:
            area_aux = Area.objects.get(versao=request.POST['nome'])

            if area_aux:
                messages.error(request, 'Erro! Area ja existe.')
                # return redirect('/areas')
                return redirect(reverse_lazy("doctrainingapp:areas_list"))
        except:
            form.save()
            # return redirect('/areas')
            return redirect(reverse_lazy("doctrainingapp:areas_list"))
    return render(request, template_name, {'form': form})


@login_required(login_url='')
@staff_member_required
def area_edit(request, pk, template_name='area-edit.html'):
    area= get_object_or_404(Area, pk=pk)
    form = AreaForm(request.POST or None, instance=area)
    if form.is_valid():
        form.save()
        # return redirect('/areas')
        return redirect(reverse_lazy("doctrainingapp:areas_list"))
    return render(request, template_name, {'form':form})


@login_required(login_url='')
@staff_member_required
def area_delete(request, pk, template_name='area-delete.html'):
    area = get_object_or_404(Area, pk=pk)
    try:
        salas = Sala.objects.filter(area=area)
        if salas:
            messages.error(request, 'Erro! Area você não pode deletar essa Area pois existe salas contidas nela...')
            # return redirect('/areas')
            return redirect(reverse_lazy("doctrainingapp:areas_list"))
    except:
        area.delete()
        # return redirect('/areas')
        return redirect(reverse_lazy("doctrainingapp:areas_list"))
    return render(request, template_name, {'object': area})
