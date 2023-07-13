from ninja import ModelSchema
from . import models

class CourseSchema(ModelSchema):
    class Config:
        model = models.Course
        model_fields = "__all__"