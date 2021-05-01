from django.shortcuts import render, redirect, reverse, get_object_or_404
from . import forms, models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from datetime import datetime, timedelta, date
from django.conf import settings


# Create your views here.
from .forms import PatientForm, AppointmentForm
from .models import Patient, Appointment


def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request, 'hospital/index.html')



# for showing signup/login button for doctor
def doctorclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request, 'hospital/doctorclick.html')


# for showing signup/login button for patient
def patientclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request, 'hospital/patientclick.html')




def doctor_signup_view(request):
    userForm = forms.DoctorUserForm()
    doctorForm = forms.DoctorForm()
    mydict = {'userForm': userForm, 'doctorForm': doctorForm}
    if request.method == 'POST':
        userForm = forms.DoctorUserForm(request.POST)
        doctorForm = forms.DoctorForm(request.POST, request.FILES)
        if userForm.is_valid() and doctorForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            doctor = doctorForm.save(commit=False)
            doctor.user = user
            doctor.status=True
            doctor = doctor.save()
            my_doctor_group = Group.objects.get_or_create(name='DOCTOR')
            my_doctor_group[0].user_set.add(user)
        return HttpResponseRedirect('doctorlogin')
    return render(request, 'hospital/doctorsignup.html', context=mydict)


def patient_signup_view(request):
    userForm = forms.PatientUserForm()
    patientForm = forms.PatientForm()
    mydict = {'userForm': userForm, 'patientForm': patientForm}
    if request.method == 'POST':
        userForm = forms.PatientUserForm(request.POST)
        patientForm = forms.PatientForm(request.POST, request.FILES)
        if userForm.is_valid() and patientForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            patient = patientForm.save(commit=False)
            patient.user = user
            patient.assignedDoctorId = request.POST.get('assignedDoctorId')
            patient.status=True
            patient = patient.save()
            my_patient_group = Group.objects.get_or_create(name='PATIENT')
            my_patient_group[0].user_set.add(user)
        return HttpResponseRedirect('patientlogin')
    return render(request, 'hospital/patientsignup.html', context=mydict)


# -----------for checking user is doctor , patient or admin
def is_doctor(user):
    return user.groups.filter(name='DOCTOR').exists()
def is_patient(user):
    return user.groups.filter(name='PATIENT').exists()


# ---------AFTER ENTERING CREDENTIALS WE CHECK WHETHER USERNAME AND PASSWORD IS OF ADMIN,DOCTOR OR PATIENT
def afterlogin_view(request):
    if is_doctor(request.user):
        return redirect('doctor-dashboard')
    elif is_patient(request.user):
        return redirect('patient-dashboard')



# ---------------------------------------------------------------------------------
# ------------------------ DOCTOR RELATED VIEWS START ------------------------------
# ---------------------------------------------------------------------------------
@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_dashboard_view(request):
    # for three cards
    patientcount = models.Patient.objects.all().filter(status=True, assignedDoctorId=request.user.id).count()
    appointmentcount = models.Appointment.objects.all().filter(status=True, doctorId=request.user.id).count()

    # for  table in doctor dashboard
    appointments = models.Appointment.objects.all().filter(status=True, doctorId=request.user.id).order_by('-id')
    patientid = []
    for a in appointments:
        patientid.append(a.patientId)
    patients = models.Patient.objects.all().filter(status=True, user_id__in=patientid).order_by('-id')
    appointments = zip(appointments, patients)
    mydict = {
        'patientcount': patientcount,
        'appointmentcount': appointmentcount,
        'appointments': appointments,
        'doctor': models.Doctor.objects.get(user_id=request.user.id),  # for profile picture of doctor in sidebar
    }
    return render(request, 'hospital/doctor_dashboard.html', context=mydict)


@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_patient_view(request):
    mydict = {
        'doctor': models.Doctor.objects.get(user_id=request.user.id),  # for profile picture of doctor in sidebar
    }
    return render(request, 'hospital/doctor_patient.html', context=mydict)


@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_view_patient_view(request):
    patients = models.Patient.objects.all().filter(status=True, assignedDoctorId=request.user.id)
    doctor = models.Doctor.objects.get(user_id=request.user.id)  # for profile picture of doctor in sidebar
    return render(request, 'hospital/doctor_view_patient.html', {'patients': patients, 'doctor': doctor})


@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_appointment_view(request):
    doctor = models.Doctor.objects.get(user_id=request.user.id)  # for profile picture of doctor in sidebar
    return render(request, 'hospital/doctor_appointment.html', {'doctor': doctor})


@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_view_appointment_view(request):
    doctor = models.Doctor.objects.get(user_id=request.user.id)  # for profile picture of doctor in sidebar
    appointments = models.Appointment.objects.all().filter(status=True, doctorId=request.user.id)
    patientid = []
    for a in appointments:
        patientid.append(a.patientId)
    patients = models.Patient.objects.all().filter(status=True, user_id__in=patientid)
    appointments = zip(appointments, patients)
    return render(request, 'hospital/doctor_view_appointment.html', {'appointments': appointments, 'doctor': doctor})


#
#
@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_delete_appointment_view(request):
    doctor = models.Doctor.objects.get(user_id=request.user.id)  # for profile picture of doctor in sidebar
    appointments = models.Appointment.objects.all().filter(status=True, doctorId=request.user.id)
    patientid = []
    for a in appointments:
        patientid.append(a.patientId)
    patients = models.Patient.objects.all().filter(status=True, user_id__in=patientid)
    appointments = zip(appointments, patients)
    return render(request, 'hospital/doctor_delete_appointment.html', {'appointments': appointments, 'doctor': doctor})


@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def delete_appointment_view(request, pk):
    appointment = models.Appointment.objects.get(id=pk)
    appointment.delete()
    doctor = models.Doctor.objects.get(user_id=request.user.id)  # for profile picture of doctor in sidebar
    appointments = models.Appointment.objects.all().filter(status=True, doctorId=request.user.id)
    patientid = []
    for a in appointments:
        patientid.append(a.patientId)
    patients = models.Patient.objects.all().filter(status=True, user_id__in=patientid)
    appointments = zip(appointments, patients)
    return render(request, 'hospital/doctor_delete_appointment.html', {'appointments': appointments, 'doctor': doctor})

@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_prescription(request):
    if request.method=='POST':
        form=AppointmentForm(request.POST)
        if form.is_valid():
            # app=Appointment.objects.get(patientName=)
            patient=form.save(commit=True)
        return HttpResponseRedirect('doctor-dashboard')
    else:
        form = AppointmentForm()
        return render(request,'hospital/doctor-patient-details.html',{'form':form})


@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def Detailview(request,PatientID):
    patient=get_object_or_404(Patient,id=PatientID)
    details_list = Patient.objects.filter(id=PatientID)
    appointments = get_object_or_404(Appointment,patientName=patient.user)
    print("appointsments details name-{} ID-{} descripton-{} prescription-{}".format(appointments.patientName,appointments.patientId,appointments.description,appointments.prescription))
    form = AppointmentForm()
    return render(request,'hospital/doctor-patient-details.html',{'form':form,'appointments':appointments,'patient':patient,'doctor': models.Doctor.objects.get(user_id=request.user.id)})
    # if request.method=='POST':
    #     print("appointsments details {}".format(appointments.patientName))
    #     form = AppointmentForm(request.POST)
    #     form.save()
    #     prescription='test value'
    #     print("prescription: {}".format(prescription))
    #     appointments.prescription=prescription
    #     appointments.save()
    #     patient.save()
    #     return HttpResponseRedirect('hospital/doctor_dashboard.html')
    # else:
    #     form=AppointmentForm()
    #     return render(request,'hospital/doctor-patient-details.html',{'form':form,'appointments':appointments,'patient':patient,'doctor': models.Doctor.objects.get(user_id=request.user.id)})

# ---------------------------------------------------------------------------------
# ------------------------ DOCTOR RELATED VIEWS END ------------------------------
# ---------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------
# ------------------------ PATIENT RELATED VIEWS START ------------------------------
# ---------------------------------------------------------------------------------
@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_dashboard_view(request):
    patient = models.Patient.objects.get(user_id=request.user.id)
    doctor = models.Doctor.objects.get(user_id=patient.assignedDoctorId)
    mydict = {
        'patient': patient,
        'doctorName': doctor.get_name,
        'doctorMobile': doctor.mobile,
        'doctorAddress': doctor.address,
        'symptoms': patient.symptoms,
        'doctorDepartment': doctor.department,
        'admitDate': patient.admitDate,
    }
    return render(request, 'hospital/patient_dashboard.html', context=mydict)


@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_appointment_view(request):
    patient = models.Patient.objects.get(user_id=request.user.id)  # for profile picture of patient in sidebar
    return render(request, 'hospital/patient_appointment.html', {'patient': patient})


@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_book_appointment_view(request):
    appointmentForm = forms.PatientAppointmentForm()
    patient = models.Patient.objects.get(user_id=request.user.id)  # for profile picture of patient in sidebar
    message = None
    mydict = {'appointmentForm': appointmentForm, 'patient': patient, 'message': message}
    if request.method == 'POST':
        appointmentForm = forms.PatientAppointmentForm(request.POST)
        if appointmentForm.is_valid():
            print(request.POST.get('doctorId'))
            desc = request.POST.get('description')

            doctor = models.Doctor.objects.get(user_id=request.POST.get('doctorId'))

            if doctor.department == 'Cardiologist':
                if 'heart' in desc:
                    pass
                else:
                    print('else')
                    message = "Please Choose Doctor According To Disease"
                    return render(request, 'hospital/patient_book_appointment.html',
                                  {'appointmentForm': appointmentForm, 'patient': patient, 'message': message})

            if doctor.department == 'Dermatologists':
                if 'skin' in desc:
                    pass
                else:
                    print('else')
                    message = "Please Choose Doctor According To Disease"
                    return render(request, 'hospital/patient_book_appointment.html',
                                  {'appointmentForm': appointmentForm, 'patient': patient, 'message': message})

            if doctor.department == 'Emergency Medicine Specialists':
                if 'fever' in desc:
                    pass
                else:
                    print('else')
                    message = "Please Choose Doctor According To Disease"
                    return render(request, 'hospital/patient_book_appointment.html',
                                  {'appointmentForm': appointmentForm, 'patient': patient, 'message': message})

            if doctor.department == 'Allergists/Immunologists':
                if 'allergy' in desc:
                    pass
                else:
                    print('else')
                    message = "Please Choose Doctor According To Disease"
                    return render(request, 'hospital/patient_book_appointment.html',
                                  {'appointmentForm': appointmentForm, 'patient': patient, 'message': message})

            if doctor.department == 'Anesthesiologists':
                if 'surgery' in desc:
                    pass
                else:
                    print('else')
                    message = "Please Choose Doctor According To Disease"
                    return render(request, 'hospital/patient_book_appointment.html',
                                  {'appointmentForm': appointmentForm, 'patient': patient, 'message': message})

            if doctor.department == 'Colon and Rectal Surgeons':
                if 'cancer' in desc:
                    pass
                else:
                    print('else')
                    message = "Please Choose Doctor According To Disease"
                    return render(request, 'hospital/patient_book_appointment.html',
                                  {'appointmentForm': appointmentForm, 'patient': patient, 'message': message})

            appointment = appointmentForm.save(commit=False)
            appointment.doctorId = request.POST.get('doctorId')
            appointment.patientId = request.user.id  # ----user can choose any patient but only their info will be stored
            appointment.doctorName = models.User.objects.get(id=request.POST.get('doctorId')).first_name
            appointment.patientName = request.user.first_name  # ----user can choose any patient but only their info will be stored
            appointment.status = True
            appointment.save()
        return HttpResponseRedirect('patient-view-appointment')
    return render(request, 'hospital/patient_book_appointment.html', context=mydict)


@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_view_appointment_view(request):
    patient = models.Patient.objects.get(user_id=request.user.id)  # for profile picture of patient in sidebar
    appointments = models.Appointment.objects.all().filter(patientId=request.user.id)
    return render(request, 'hospital/patient_view_appointment.html', {'appointments': appointments, 'patient': patient})

#----------------------------------------------------------------------------------
# ------------------------ PATIENT RELATED VIEWS END ------------------------------
# ---------------------------------------------------------------------------------
