from django.contrib import admin
from ots_app.models import Candidate
from ots_app.models import Question
from ots_app.models import Result
# from ots_app.models import UserAnswer



@admin.register(Candidate)
class CandidateName(admin.ModelAdmin):
    list_display=('username','password','email','name','test_attempt','point')

@admin.register(Question)
class Questions(admin.ModelAdmin):
    list_display=('Qid','title','Question','option_a','option_b','option_c','option_d','answer','explanation')

@admin.register(Result)
class Results(admin.ModelAdmin):
    list_display=('resultid','username','date','time','title','right','wrong','points','user_answer_option')



