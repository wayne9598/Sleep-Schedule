from django import forms
from .models import PSQI

class PSQI_form(forms.ModelForm):
    class Meta:
        model = PSQI
        fields = [
            'latencyGreaterThan30', 
            'midnightAwakeEarlyMorning', 
            'useBathroom', 
            'uncomfortableBreathing', 
            'coughSnore', 
            'feelCold', 
            'feelHot', 
            'badDreams', 
            'pain', 
            'otherReason', 
            'sleepMedication', 
            'stayAwakeDuringWork', 
            'enthusiasmToDoThings', 
            'selfRatedSleepQuality', 
            'userFeedBackIntensity',
            
        ]


