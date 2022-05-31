import os

from django.db import models
from django.conf import settings
import os.path as osp
from os import listdir
import json

class Stage(models.Model):

    class LevelRegion(models.IntegerChoices):
        APOTOS = 1
        HOLOSKA = 2
        SPAGONIA = 3
        CHUN_NAN = 4
        SHAMAR = 5
        ADABAT = 6
        EGGMANLAND = 7

    class StageTime(models.IntegerChoices):
        DAY = 0
        NIGHT = 1

    class StageType(models.IntegerChoices):
        MAIN = 1
        MISSION = 2
        BOSS_MAYBE = 5
        UNKNOWN = 6

    AREA_CHOICES = list(enumerate("ABCDEFGH"))
    stage_subarea = models.IntegerField(choices=AREA_CHOICES,default=0)
    level_day_night = models.IntegerField(choices=StageTime.choices,default=0)
    region = models.IntegerField(choices=LevelRegion.choices,default=1)
    stage_kind = models.IntegerField(choices=StageType.choices,default=1)

    def get_obj_filepaths(self):
        stage_folder_name = "stage" + str(self.level_day_night) + str(self.region) + str(self.stage_kind)
        area_folder_name = "area" + self.get_stage_subarea_display()
        target_path = osp.join("static", "obj", stage_folder_name, area_folder_name)
        if not osp.exists(target_path):
            return []
        else:
            basenames = os.listdir(target_path)
            print(basenames)
            return [osp.join("obj", stage_folder_name, area_folder_name, objfn) for objfn in basenames]

    @property
    def stage_id(self):
        return str(self.level_day_night) + str(self.region) + str(self.stage_kind)


    def __str__(self):
        reg = self.get_region_display()
        dn = self.get_level_day_night_display()
        kind = self.get_stage_kind_display()
        area =  self.get_stage_subarea_display()
        return f"{reg} {dn} ({kind}, Area {area})"

def get_stage_by_stage_id(id_str,area='A'):
    level_day_night, region, stage_kind = list(map(int, id_str))
    stg_area = 'ABCDEFGH'.index(area)
    stg_obj = Stage.objects.filter(level_day_night=level_day_night,region=region,stage_kind=stage_kind,stage_subarea=stg_area).first()
    return stg_obj






class Vec3(models.Model):
    x = models.FloatField(default=0.0)
    y = models.FloatField(default=0.0)
    z = models.FloatField(default=0.0)

    def __str__(self):
        return f'({self.x},{self.y},{self.z})'

class Quaternion(models.Model):
    x = models.FloatField(default=0.0)
    y = models.FloatField(default=0.0)
    z = models.FloatField(default=0.0)
    w = models.FloatField(default=1.0)

    def __str__(self):
        return f'({self.x},{self.y},{self.z},{self.w})'

class SetItem(models.Model):
    stage = models.ForeignKey(Stage,on_delete=models.CASCADE)
    position = models.ForeignKey(Vec3,on_delete=models.CASCADE,related_name="position")
    rotation = models.ForeignKey(Quaternion,on_delete=models.CASCADE)
    scale = models.ForeignKey(Vec3,on_delete=models.CASCADE,blank=True,null=True,related_name="scale")
    headerinfo = models.CharField(max_length=8,default="00000000")
    params = models.CharField(max_length=200)

    def set_params(self, x):
        self.params = json.dumps(x)

    def get_params(self):
        return json.loads(self.params)

    def __str__(self):
        return "Set item for " + str(self.stage) + f" Header Info: {self.headerinfo}"

    def trigger_as_object(self):
        return {
            "headerinfo": self.headerinfo,
            "position": [
                self.position.x,
                self.position.y,
                self.position.z
            ],
            "rotation": [
                    self.rotation.x,
                    self.rotation.y,
                    self.rotation.z,
                    self.rotation.w
            ],
            "params": self.get_params()
        }




