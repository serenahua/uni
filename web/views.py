from datetime import datetime, timedelta, time
from itertools import chain

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages import get_messages
from django.db.models import Q, Sum
from django.db.models.functions import TruncDate
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views.generic import TemplateView

from .models import ExpenseItem, Expense, Income, Setting


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'web/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        color = Setting.objects.get(name="color")
        context['page'] = "home"
        context['color'] = color.value
        now = timezone.now()

        chicken_incomes = Income.objects.filter(date__year=now.year, date__month=now.month, chicken=True)
        hotpot_incomes = Income.objects.filter(date__year=now.year, date__month=now.month, hot_pot=True)
        chicken_expenses = Expense.objects.filter(date__year=now.year, date__month=now.month,  item__chicken=True)
        hotpot_expenses = Expense.objects.filter(date__year=now.year, date__month=now.month,  item__hot_pot=True)
        home_expenses = Expense.objects.filter(date__year=now.year, date__month=now.month,  item__home=True)

        volume = sum([x.volume for x in chicken_incomes])
        chicken = sum([x.value for x in chicken_incomes]) - sum([x.value for x in chicken_expenses])
        hotpot = sum([x.value for x in hotpot_incomes]) - sum([x.value for x in hotpot_expenses])
        expense = sum([x.value for x in home_expenses])
        total = chicken + hotpot - expense

        context['total'] = total
        context['chicken'] = chicken
        context['hotpot'] = hotpot
        context['expense'] = expense
        context['volume'] = volume

        return context


class ChickenView(LoginRequiredMixin, TemplateView):
    template_name = 'web/chicken.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = "chicken"

        color = Setting.objects.get(name="color")
        context['color'] = color.value

        if (item_id := self.request.GET.get('n')) is not None:
            type = self.request.GET.get('t')
            if type == 'income':
                item = Income.objects.get(id=item_id)
            elif type == 'expense':
                item = Expense.objects.get(id=item_id)
            context['type'] = type
            context['item'] = item

        context['categories'] = ExpenseItem.objects.filter(chicken=True).order_by('name')
        context['today'] = timezone.now()

        return context

    def post(self, request, **kwargs):
        method = request.POST['method']
        item_id = request.POST['id'] if method == 'edit' else None
        type = request.POST['type']
        date = request.POST['date']
        value = request.POST['value']
        chicken = request.POST['chicken']
        category = request.POST['category']
        remark = request.POST['remark']

        if item_id and type == 'income':
            item = Income.objects.get(id=item_id)
        elif type == 'income':
            item = Income()
        elif item_id and type == 'expense':
            item = Expense.objects.get(id=item_id)
        elif type == 'expense':
            item = Expense()

        item.date = date
        item.value = value
        item.remark = remark

        if type == 'income':
            item.volume = chicken
            item.chicken = True
        elif type == 'expense':
            item.item_id = category

        item.save()

        return JsonResponse({
            'status': True
        })


class HotPotView(LoginRequiredMixin, TemplateView):
    template_name = 'web/hotpot.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = "hotpot"

        color = Setting.objects.get(name="color")
        context['color'] = color.value

        if (item_id := self.request.GET.get('n')) is not None:
            type = self.request.GET.get('t')
            if type == 'income':
                item = Income.objects.get(id=item_id)
            elif type == 'expense':
                item = Expense.objects.get(id=item_id)
            context['type'] = type
            context['item'] = item

        context['categories'] = ExpenseItem.objects.filter(hot_pot=True).order_by('name')
        context['today'] = timezone.now()

        return context

    def post(self, request, **kwargs):
        method = request.POST['method']
        item_id = request.POST['id'] if method == 'edit' else None
        type = request.POST.get('type')
        date = request.POST['date']
        value = request.POST['value']
        category = request.POST['category']
        remark = request.POST['remark']

        if item_id and type == 'income':
            item = Income.objects.get(id=item_id)
        elif type == 'income':
            item = Income()
        elif item_id and type == 'expense':
            item = Expense.objects.get(id=item_id)
        elif type == 'expense':
            item = Expense()

        item.date = date
        item.value = value
        item.remark = remark

        if type == 'expense':
            item.item_id = category
        else:
            item.hot_pot = True

        item.save()

        return JsonResponse({
            'status': True
        })


class HomeExpenseView(LoginRequiredMixin, TemplateView):
    template_name = 'web/expense.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = "home_expense"

        color = Setting.objects.get(name="color")
        context['color'] = color.value

        if (item_id := self.request.GET.get('n')) is not None:
            item = Expense.objects.get(id=item_id)
            context['item'] = item

        context['categories'] = ExpenseItem.objects.filter(home=True).order_by('name')
        context['today'] = timezone.now()

        return context

    def post(self, request, **kwargs):
        method = request.POST['method']
        item_id = request.POST['id'] if method == 'edit' else None
        date = request.POST['date']
        value = request.POST['value']
        category = request.POST['category']
        remark = request.POST['remark']

        if item_id:
            item = Expense.objects.get(id=item_id)
        else:
            item = Expense()

        item.date = date
        item.value = value
        item.item_id = category
        item.remark = remark
        item.save()

        return JsonResponse({
            'status': True
        })


class ReportView(LoginRequiredMixin, TemplateView):
    template_name = 'web/report.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        color = Setting.objects.get(name="color")
        context['page'] = "report"
        context['color'] = color.value

        return context

    def get(self, request, **kwargs):

        context = self.get_context_data(**kwargs)
        now = timezone.now()

        type = request.GET.get('t', 'm')
        year = int(request.GET.get('y', now.year))
        month = int(request.GET.get('m', now.month))
        day = int(request.GET.get('d', now.day))
        action = int(request.GET.get('a', 0))

        year, month, day = self.get_valid_date(year, month, day, action)

        if type == 'm':
            incomes = Income.objects.filter(date__year=year, date__month=month)
            expenses = Expense.objects.filter(date__year=year, date__month=month, item__isnull=False)

            # monthly data
            monthly_volume = sum([x.volume for x in incomes])
            monthly_income = sum([x.value for x in incomes])
            monthly_expense = sum([x.value for x in expenses])
            monthly_total = monthly_income - monthly_expense

            context['total'] = monthly_total
            context['income'] = monthly_income
            context['expense'] = monthly_expense
            context['volume'] = monthly_volume

            # daily data
            daily_incomes = Income.objects.filter(date__year=year, date__month=month).\
                            values(d=TruncDate('date')).\
                            annotate(income=Sum('value'), chicken=Sum('volume'))
            daily_expenses = Expense.objects.filter(date__year=year, date__month=month, item__isnull=False).\
                            values(d=TruncDate('date')).\
                            annotate(expense=Sum('value'))
            lists = sorted(list(chain(daily_incomes, daily_expenses)), key=lambda item: item['d'], reverse=True)
            daily_list = lists.copy()

            for i in range(len(lists)):
                if i >= len(daily_list)-1:
                    continue
                elif daily_list[i]['d'] == daily_list[i+1]['d']:
                    daily_list[i].update(daily_list[i+1])
                    daily_list.pop(i+1)

            for item in daily_list:
                inc = item.get('income', 0)
                exp = item.get('expense', 0)
                item['total'] = inc - exp

            context['daily_items'] = daily_list
        elif type == 'd':
            date_string = "%s-%s-%s" % (year, month, day)
            current_date = datetime.strptime(date_string, "%Y-%m-%d")
            next_date = current_date + timedelta(1)
            incomes = Income.objects.filter(date__gte=current_date, date__lt=next_date)
            expenses = Expense.objects.filter(date__gte=current_date, date__lt=next_date,item__isnull=False)
            items = sorted(list(chain(incomes, expenses)), key=lambda i: i.creation, reverse=True)

            context['items'] = items

            daily_volume = sum([x.volume for x in incomes])
            daily_income = sum([x.value for x in incomes])
            daily_expense = sum([x.value for x in expenses])
            daily_total = daily_income - daily_expense

            context['total'] = daily_total
            context['income'] = daily_income
            context['expense'] = daily_expense
            context['volume'] = daily_volume

        context['type'] = type
        context['year'] = year
        context['month'] = month
        context['day'] = day


        return self.render_to_response(context)

    def post(self, request, **kwargs):
        method = request.POST['method']
        type = 0

        if method == 'delete_item':
            item_id = request.POST['id']
            type = request.POST['type']
            if type == 'income':
                Income.objects.get(id=item_id).delete()
            elif type == 'expense':
                Expense.objects.get(id=item_id).delete()

        return JsonResponse({
            'status': True,
            'type': type
        })

    def get_valid_date(self, year, month, day, action):

        if action == 0:
            pass
        elif action == -1 or action == 1:
            date_string = "%s-%s-%s" % (year, month, day)
            _d = datetime.strptime(date_string, "%Y-%m-%d")
            _d += timedelta(action)
            year, month, day = _d.year, _d.month, _d.day
        elif action == -30 or action == 30:
            if month == 1 and action < 0:
                year -= 1
                month = 12
            elif month == 12 and action > 0:
                year += 1
                month = 1
            else:
                add = 1 if action > 0 else -1
                month += add

        return (year, month, day)


class SystemManagementView(TemplateView):
    template_name = 'web/system.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = "setting"

        color = Setting.objects.get(name="color")
        context['color'] = color.value

        cat = self.request.GET.get('cat', '1')

        if cat == '1':
            items = ExpenseItem.objects.filter(chicken=True).order_by('name')
        elif cat == '2':
            items = ExpenseItem.objects.filter(hot_pot=True).order_by('name')
        elif cat == '3':
            items = ExpenseItem.objects.filter(home=True).order_by('name')
        elif cat == '4':
            items = Setting.objects.all()

        context['items'] = items
        context['cat'] = cat

        return context


class SystemDataView(TemplateView):
    template_name = 'web/data.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = "setting"

        color = Setting.objects.get(name="color")
        context['color'] = color.value

        cat = self.request.GET.get('cat', '1')
        if (item_id := self.request.GET.get('n')) is not None:
            if cat == '4':
                item = Setting.objects.get(id=item_id)
            else:
                item = ExpenseItem.objects.get(id=item_id)
            context['item'] = item

        context['cat'] = cat

        return context

    def post(self, request, **kwargs):
        method = request.POST['method']
        type = 0

        if method == 'delete_item':
            item_id = request.POST['id']
            ExpenseItem.objects.get(id=item_id).delete()
        elif method == 'create_item':
            type = request.POST['type']
            name = request.POST['name']
            item = ExpenseItem()

            item.name = name
            item.chicken = (type == 'chicken')
            item.hot_pot = (type == 'hotpot')
            item.home = (type == 'home')
            item.save()

            type = 1 if type == 'chicken' else 2 if type == 'hotpot' else 3
        elif method == 'edit_item':
            name = request.POST['name']
            item_id = request.POST['id']
            item = ExpenseItem.objects.get(id=item_id)

            item.name = name
            item.save()
            type = 1 if item.chicken else 2 if item.hot_pot else 3
        elif method == 'edit_setting':
            item_id = request.POST['id']
            value = request.POST['name']
            item = Setting.objects.get(id=item_id)
            type = 4

            item.value = value
            item.save()
        elif method == 'edit_color':
            item_id = request.POST['id']
            value = str(request.POST['_color'])
            item = Setting.objects.get(id=item_id)
            type = 4

            item.value = value
            item.save()

        return JsonResponse({
            'status': True,
            'type': type
        })


class LoginView(TemplateView):
    template_name = 'web/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        name = Setting.objects.get(name='name')
        color = Setting.objects.get(name="color")
        context['name'] = name
        context['color'] = color.value

        return context

    def get(self, request, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('web:index'))

        context = self.get_context_data(**kwargs)
        context['next'] = request.GET.get('next', '/')
        return self.render_to_response(context)

    def post(self, request, **kwargs):

        username = request.POST['account']
        password = request.POST['password']
        _next = request.POST['next']

        if not username or not password:
            return JsonResponse({
                'status': False,
                'error': -1,
                'msg': 'account/password not provided'
            })

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
        else:
            return JsonResponse({
                'status': False,
                'error': -2,
                'msg': 'account/password not provided'
            })

        return JsonResponse({
            'status': True,
            'next': _next,
        })

