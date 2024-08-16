from chartauditor.pdf_wrapper.utils import (generate_docx, send_progress, file_processing,
                                            cost_calculation, remove_punctuation_and_stopwords, update_chart_obj_status
                                            )
from chartauditor.pdf_wrapper.forms import ChartCheckerForm
from django.views.generic import TemplateView, ListView, View
from chartauditor.accounts.decorators import profile_completion_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from chartauditor.pdf_wrapper.models import ChartChecker
from django.http import JsonResponse
from nltk import word_tokenize


class IndexView(TemplateView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_profile:
            return redirect('chart_audit')
        else:
            return redirect('custom_login')


class CheckOutView(TemplateView):
    template_name = 'checkout.html'


@method_decorator(profile_completion_required, name='dispatch')
class ChartCheckerView(LoginRequiredMixin, TemplateView):
    template_name = 'PdfWrapper/chart_checker.html'
    form_class = ChartCheckerForm

    def get(self, request, *args, **kwargs):
        user_id = request.user.id
        form = self.form_class()
        context = {
            'form': form,
            'user_id': user_id,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        progress = '1-10'
        user_id = request.user.id
        send_progress(progress, user_id)

        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            form.save(commit=False)
            file = request.FILES.get('chart')
            combined_text, total_page_count = file_processing(file, user_id)

            progress = '71-90'
            send_progress(progress, user_id)

            extracted_text_lower = ' '.join(combined_text).lower()
            tokenize_text = word_tokenize(extracted_text_lower)
            no_stopwords_punctuation_tokens = remove_punctuation_and_stopwords(tokenize_text)

            clean_text = ' '.join(no_stopwords_punctuation_tokens)
            rounded_chart_cost = cost_calculation(clean_text)
            total_character_count = request.user.character_limit + len(clean_text)
            if total_character_count >= 175000:
                trial_status = 'False'
            else:
                trial_status = 'True'

            form.instance.clean_chart = no_stopwords_punctuation_tokens
            form.instance.user = request.user
            form.instance.total_page_count = total_page_count
            form.instance.chart_name = file.name
            form.instance.chart_price = rounded_chart_cost
            form.instance.character_count = len(clean_text)
            form.instance.save()
            form.save(commit=False)
            chart_id = form.instance.id

            progress = '91-100'
            send_progress(progress, user_id)
            progress = str(form.instance.id)
            send_progress(progress, user_id)

            return JsonResponse({
                'success': len(clean_text),
                'chart_cost': rounded_chart_cost,
                'user': request.user.email,
                'trial_status': trial_status,
                'chart_id': chart_id,
                'total_page_count': total_page_count,
            })
        print('form errors:::::', form.errors)
        return JsonResponse({
            'form-errors': form.errors,
            })


@method_decorator(profile_completion_required, name='dispatch')
class ChartUserInputView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        user = request.user
        id = request.POST.get('chartIdInput')
        chart_obj = ChartChecker.objects.get(id=id)
        update_chart_obj_status(chart_obj, user)

        return JsonResponse({'success': 'Report generated successfully'})


@method_decorator(profile_completion_required, name='dispatch')
class UserCancelChart(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        id = self.kwargs.get('pk')
        ChartChecker.objects.get(id=id).delete()
        return redirect('chart_audit')


@method_decorator(profile_completion_required, name='dispatch')
class ChartListView(LoginRequiredMixin, ListView):
    template_name = 'dashboard/reports.html'

    def get(self, request, *args, **kwargs):
        charts = ChartChecker.objects.filter(user__id=request.user.id, is_payment_done=True).order_by('-id')
        context = {
            'charts': charts,
        }
        return render(request, self.template_name, context)


@method_decorator(profile_completion_required, name='dispatch')
class DownloadsView(LoginRequiredMixin, TemplateView):
    template_name = 'PdfWrapper/chart_pdf.html'

    def get(self, request, *args, **kwargs):
        btn = request.GET.get('btn')
        id = request.GET.get('objId')
        chart = ChartChecker.objects.get(id=id)
        file_name = f'{chart.first_name}'
        # if btn == 'pdf':
        #     context = {
        #         'chart': chart.chart_response,
        #     }
        #     file = render_to_pdf_weasy(self.template_name, request, file_name, context)
        # else:
        file = generate_docx(file_name, chart.chart_response, btn)
        return file
