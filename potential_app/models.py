from django.db import models

class LandAnalysis(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    area_m2 = models.FloatField(null=True, blank=True)
    area_ha = models.FloatField(null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    
    # PV Configuration
    pv_efficiency = models.FloatField(default=0.20)
    pv_performance_ratio = models.FloatField(default=0.80)
    pv_land_coverage = models.FloatField(default=0.60)
    pv_system_efficiency = models.FloatField(default=0.95)
    
    # Wind Configuration
    wind_rated_power_kw = models.FloatField(default=5.0)
    wind_rotor_diameter_m = models.FloatField(default=7.0)
    wind_hub_height_m = models.FloatField(default=20.0)
    wind_cut_in_ms = models.FloatField(default=3.0)
    wind_rated_ws_ms = models.FloatField(default=12.0)
    wind_cut_out_ms = models.FloatField(default=25.0)
    wind_alpha = models.FloatField(default=0.14)
    wind_system_efficiency = models.FloatField(default=0.90)
    
    # Electrical
    dc_voltage = models.FloatField(default=48.0)
    
    # Results
    soil_data = models.JSONField(null=True, blank=True)
    crop_recommendations = models.JSONField(null=True, blank=True)
    energy_results = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Land Analysis at ({self.latitude}, {self.longitude})"