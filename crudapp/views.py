from django.shortcuts import get_object_or_404, redirect, render

from .models import Student


def index(request):
    students = Student.objects.all().order_by('id')
    return render(request, 'crudapp/index.html', {'students': students})


def add_student(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        if name and email:
            Student.objects.create(name=name, email=email)
            return redirect('crudapp:index')

    return render(request, 'crudapp/add.html')


def edit_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.name = request.POST.get('name', '').strip()
        student.email = request.POST.get('email', '').strip()
        student.save()
        return redirect('crudapp:index')

    return render(request, 'crudapp/edit.html', {'student': student})


def delete_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    student.delete()
    return redirect('crudapp:index')
