"""
    Classes and functions for generating views.py files for simple studies
"""
from study_settings import StudySettings

#url_args = [("") for s in generated_studies]
#patterns_args = map(url, *x for x in url_args)
#urlpatterns = patterns(*patterns_args)





class ViewsBuilder:
    """
        Class for creating urls.py files from StudySettings objects.
    """
    
    views_file_template = r"""
from django.http import *
from django.contrib.auth.decorators import login_required
from django.template import Template, Context

{0}
"""
    
    #@login_required
    #def stage_two(request):
    #    return render_to_response('tutorial_study/study_display.html', {'number': 2})
    stage_url_template = """
@login_required
def {1}(request):
    template_file = open("{2}", "r")
    template = Template("".join(template_file.readlines()))
    context = Context({{}})
    return HttpResponse(template.render(context))
"""
    
    def __init__(self, *settings_list):
        self.settings_list = settings_list
      
    def write_views_file(self, module_dir):
        views_file = open("{0}/{1}".format(module_dir, "views.py"), "w")
        
        fcn_list = []
        for study in self.settings_list:
            for stage in study.stages:
                template_file = "{0}/{1}/stages/{2}/template.html".format(module_dir, study.name, stage)
                fcn_list.append(ViewsBuilder.stage_url_template.format(study.name, stage, template_file))
        
        views_file.write(ViewsBuilder.views_file_template.format("\n".join(fcn_list)))







