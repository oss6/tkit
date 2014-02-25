from django.shortcuts import render, render_to_response, redirect
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
# from django.contrib import auth
from django.template import RequestContext
from forms import *
from models import *


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/signup-success/')
    args = {}
    args.update(csrf(request))
    args['form'] = RegistrationForm()

    return render(request, 'registration/register.html', args)


@login_required(login_url='/login/')
def disable_account(request):
    u = request.user
    u.is_active = False


@login_required(login_url='/login/')
def classes(request):
    cls = Classes.objects.all().filter(teacher=request.user)
    return render_to_response("classes.html", {"classes": cls})


@login_required(login_url='/login/')
def add_class(request):
    if request.method == "POST":
        form = AddClassForm(request.POST)
        if form.is_valid():
            # Retrieve data from request
            cl_name = form.cleaned_data["name"]
            school = form.cleaned_data["school"]
            desc = form.cleaned_data["description"]

            # Save class into db
            cl = Classes(name=cl_name, school=school, description=desc, teacher=request.user)
            cl.save()

            return redirect('/classes/')
    else:
        form = AddClassForm()

    return render_to_response('add-class.html', {"form": form}, context_instance=RequestContext(request))


@login_required(login_url='/login/')
def remove_class(request, class_name):
    c = Classes.objects.get(name=class_name)
    c.delete()

    return redirect('/classes/')


@login_required(login_url='/login/')
def students(request, class_name):
    cl = Classes.objects.all().filter(name__exact=class_name, teacher__exact=request.user)[0]
    ss = Students.objects.all().filter(s_class=cl)

    return render_to_response("students.html", {"students": ss, "class": cl, "nums": len(ss)})


@login_required(login_url='/login/')
def add_student(request, class_name):
    if request.method == "POST":
        form = AddStudentForm(request.POST)
        if form.is_valid():
            # Retrieve data from request
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            email = form.cleaned_data["email"]
            parent = form.cleaned_data["parent"]
            parent_email = form.cleaned_data["parent_email"]
            photo = form.cleaned_data["photo"]

            # Save student into db
            c = Classes.objects.get(name=class_name)
            s = Students(first_name=first_name, last_name=last_name,
                         email=email, parent=parent, parent_email=parent_email, photo=photo, s_class=c)
            s.save()

            return redirect('/classes/' + class_name + '/students/')
    else:
        form = AddStudentForm()

    return render_to_response('add-student.html', {"form": form}, context_instance=RequestContext(request))


def grade_book(request, class_name):
    cl = Classes.objects.all().filter(name__exact=class_name, teacher__exact=request.user)[0]
    ss = Students.objects.all().filter(s_class=cl)

    return render_to_response("students.html", {"students": ss, "class": cl, "nums": len(ss)})


def attendance(request, class_name):
    pass


@login_required(login_url='/login/')
def lessons(request):
    pass