
from django.http import *
from django.contrib.auth.decorators import login_required
from django.template import Template, Context


@login_required
def welcome_page(request):
    template_file = open("/Users/kante/Documents/work/tangra/Evaluation-Portal/portal/user_studies/example_study/stages/welcome_page/template.html", "r")
    template = Template("".join(template_file.readlines()))
    context = Context({})
    return HttpResponse(template.render(context))


@login_required
def simple_task(request):
    template_file = open("/Users/kante/Documents/work/tangra/Evaluation-Portal/portal/user_studies/example_study/stages/simple_task/template.html", "r")
    template = Template("".join(template_file.readlines()))
    context = Context({})
    return HttpResponse(template.render(context))


@login_required
def bye_page(request):
    template_file = open("/Users/kante/Documents/work/tangra/Evaluation-Portal/portal/user_studies/example_study/stages/bye_page/template.html", "r")
    template = Template("".join(template_file.readlines()))
    context = Context({})
    return HttpResponse(template.render(context))

