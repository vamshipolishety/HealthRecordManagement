from django.contrib import admin, auth
from django.contrib.auth.models import User

from .models import Doctor,Patient,Appointment#PatientDischargeDetails,
# Register your models here.
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')
    pass
admin.site.register(Doctor, DoctorAdmin)

class PatientAdmin(admin.ModelAdmin):
    list_display =('id', 'user')
    pass
admin.site.register(Patient, PatientAdmin)

class AppointmentAdmin(admin.ModelAdmin):
    pass
admin.site.register(Appointment, AppointmentAdmin)

# class UserAdmin(auth.UserAdmin):
#     list_display = ('id','user')
#     pass
# admin.site.register(User, UserAdmin,)

# class PatientDischargeDetailsAdmin(admin.ModelAdmin):
#     pass
# admin.site.register(PatientDischargeDetails, PatientDischargeDetailsAdmin)
