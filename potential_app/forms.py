from django import forms
from .models import LandAnalysis

class LandAnalysisForm(forms.ModelForm):
    class Meta:
        model = LandAnalysis
        fields = [
            'latitude', 'longitude', 'area_m2', 'area_ha', 
            'start_date', 'end_date'
        ]
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        area_m2 = cleaned_data.get('area_m2')
        area_ha = cleaned_data.get('area_ha')
        
        if not area_m2 and not area_ha:
            raise forms.ValidationError("Please provide either area in m² or hectares.")
        
        return cleaned_data

class AdvancedSettingsForm(forms.ModelForm):
    class Meta:
        model = LandAnalysis
        fields = [
            'pv_efficiency', 'pv_performance_ratio', 'pv_land_coverage', 'pv_system_efficiency',
            'wind_rated_power_kw', 'wind_rotor_diameter_m', 'wind_hub_height_m',
            'wind_cut_in_ms', 'wind_rated_ws_ms', 'wind_cut_out_ms', 'wind_alpha', 'wind_system_efficiency',
            'dc_voltage'
        ]