from chartauditor.accounts.utils import email_confirmation, create_stripe_customer
from django.contrib.auth import update_session_auth_hash
from allauth.socialaccount.models import SocialAccount
from chartauditor.accounts.models import User, CompanyInformation
from django.contrib.auth import authenticate, login
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from chartauditor.accounts.forms import CompanyInfoForm, ChangePasswordForm
from django.contrib import messages
from django.conf import settings


class CustomLoginView(TemplateView):
    template_name = 'registration/login.html'

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None and user.is_profile == False:
            return redirect('profile')
        if user is not None and user.is_profile:
            login(request, user)
            return redirect('chart_audit')
        messages.error(request, 'Incorrect Email or Password')
        return redirect('custom_login')


class SignUpView(TemplateView):
    template_name = 'registration/signup.html'

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        password = request.POST.get('password')
        if email and password:
            is_obj_exists = User.objects.filter(email=email).exists()
            if is_obj_exists:
                messages.error(request, 'User with this email already exists')
                return render(request, self.template_name)
            else:
                user = User.objects.create(email=email)
                user.set_password(password)
                user.save()
                user = authenticate(email=email, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('profile')
                else:
                    messages.error(request, "Invalid credentials.")
        messages.error(request, "Email and password both are required.")
        return render(request, self.template_name)


class CompanyInfoView(TemplateView):
    template_name = 'registration/profile.html'
    form_class = CompanyInfoForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        context = {
            'form': form,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        user = User.objects.get(id=request.user.id)
        form = self.form_class(request.POST)
        social_account = SocialAccount.objects.filter(user_id=user.id)

        if form.is_valid():
            if social_account:
                form.instance.user = user
                form.instance.user.first_name = request.POST.get('first_name')
                form.instance.user.is_profile = True
                form.instance.user.save()
                form.save()
                return redirect('chart_audit')
            else:
                obj, created = CompanyInformation.objects.get_or_create(user=user)
                if created:
                    obj.user = user
                    obj.user.first_name = request.POST.get('first_name')
                    obj.facility_name = request.POST.get('facility_name')
                    obj.state_licence = request.POST.get('state_licence')
                    obj.accreditation = request.POST.get('accreditation')
                    obj.accept_insurance = request.POST.get('accept_insurance')
                    facility_types = request.POST.getlist('facility_type')
                    # Clear existing facility types
                    obj.facility_type.clear()
                    # Add new facility types
                    for facility_type in facility_types:
                        obj.facility_type.add(facility_type)

                    obj.user.save()
                    obj.save()

                email = user.email
                uuid = user.uuid
                host = settings.BASE_HOST
                email_confirmation(email, uuid, host)
                messages.success(request, 'A Verification email sent to your email address, confirm your email to '
                                          'complete the registration!.')
                return redirect('index')
        return render(request, self.template_name, {'form': form})


class ActivateUser(TemplateView):
    template_name = 'activate_user.html'

    def get(self, request, *args, **kwargs):
        uuid = kwargs.get('uuid')
        user = User.objects.get(uuid=uuid)
        user.is_profile = True
        user.save()
        create_stripe_customer(user)
        return render(request, self.template_name)


class UpdateCompanyInfoView(TemplateView):
    template_name = 'registration/update_profile.html'
    pass_form_class = ChangePasswordForm
    profile_form_class = CompanyInfoForm

    def get(self, request, *args, **kwargs):
        obj = CompanyInformation.objects.get(user=request.user)
        password_form = self.pass_form_class(request.user)
        form = self.profile_form_class(instance=obj)
        context = {
            'password_form': password_form,
            'form': form,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        obj = CompanyInformation.objects.get(user=request.user)
        form = self.profile_form_class(request.POST, instance=obj)
        if form.is_valid():
            form.save(commit=True)
            return redirect('update_profile')
        print('update form error::::', form.errors)
        return render(request, self.template_name, {"errors": form})


class ChangePasswordView(TemplateView):
    template_name = 'registration/update_profile.html'
    form_class = ChangePasswordForm

    def post(self, request, *args, **kwargs):
        password_form = self.form_class(request.user, data=request.POST)
        if password_form.is_valid():
            password_form.save()
            update_session_auth_hash(request, password_form.user)
            messages.success(request, 'Password changed successfully')
            return redirect('update_profile')
        return render(request, self.template_name, {'password_form': password_form})

