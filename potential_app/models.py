from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('landowner', 'Landowner'),
        ('builder', 'PV Plant Builder'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='landowner')
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.role}"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Land(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lands')
    name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    area_m2 = models.FloatField()
    address = models.TextField(blank=True)
    proof_document = models.FileField(upload_to='land_proofs/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class LandAnalysis(models.Model):
    # Optional link to a saved Land
    land = models.ForeignKey(Land, on_delete=models.SET_NULL, null=True, blank=True, related_name='analyses')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='analyses') # For ad-hoc analysis saved to user

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

class Proposal(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    )
    builder = models.ForeignKey(User, on_delete=models.CASCADE, related_name='proposals_sent')
    land = models.ForeignKey(Land, on_delete=models.CASCADE, related_name='proposals')
    description = models.TextField()
    estimated_cost = models.FloatField(null=True, blank=True)
    estimated_duration_months = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Proposal by {self.builder.username} for {self.land.name}"

class Bond(models.Model):
    proposal = models.OneToOneField(Proposal, on_delete=models.CASCADE, related_name='bond')
    final_agreement = models.FileField(upload_to='bonds/')
    signed_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Bond for {self.proposal.land.name}"