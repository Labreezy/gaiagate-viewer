import os

from django.core import serializers
from django.forms.models import model_to_dict
from django.views.generic.base import TemplateView
from django.views.generic import ListView, DetailView
from .models import *
from glob import glob
from django.conf import settings
import os.path as osp
from os import listdir
from glob import glob


class StageListView(ListView):
    model = Stage
    template_name = "viewer/stagelist.html"


class StageDetailView(DetailView):
    model = Stage
    template_name = "viewer/viewer.html"

    def get_context_data(self, **kwargs):
        context = super(StageDetailView, self).get_context_data(**kwargs)
        stg_object = self.get_object()
        filenames = stg_object.get_obj_filepaths()
        filenames = [fn.replace("\\","/") for fn in filenames]
        context.update({"files": filenames})
        triggers = SetItem.objects.filter(stage_id=stg_object.id,headerinfo="10058002")
        context.update({"triggers": list(map(lambda t: t.trigger_as_object(), triggers))})
        return context

class ViewerView(TemplateView):
    template_name = "viewer/viewer.html"

    def get_context_data(self, **kwargs):
        context = super(ViewerView, self).get_context_data(**kwargs)
        flist = []
        print(context.get('stageid'))
        target_path = osp.join(settings.STATIC_ROOT, "obj", context['stageid'])
        obj_dict = dict(cam_files=[], death_files=[], hit_files=[])
        if osp.exists(target_path):
            areapath = osp.join(target_path, "area" + context['area'])
            safe_area_parts = areapath.split(os.sep)
            static_idx = safe_area_parts.index('obj')
            safe_area_parts = safe_area_parts[static_idx:]
            areapath_safe = osp.join(*safe_area_parts)
            if osp.exists(osp.join(areapath, "camera")):
                obj_dict.update({"camera_files": os.listdir(osp.join(areapath, "camera"))})
            if osp.exists(osp.join(areapath, "death")):         
                obj_dict.update({"death_files": os.listdir(osp.join(areapath, "death"))})
            if osp.exists(osp.join(areapath, "hit")):
                obj_dict.update({"hit_files": os.listdir(osp.join(areapath, "hit"))})
            for k in obj_dict.keys():
                basename_list = obj_dict[k]
                obj_dict[k] = list(map(lambda fn: osp.join(areapath_safe, k.split("_")[0], fn).replace("\\",'/'), basename_list))

            context.update({"objfiles": obj_dict})


        return context
