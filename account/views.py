from itertools import chain

from django.contrib.messages import get_messages
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.utils import timezone
from django.views.generic import TemplateView

from .models import ExpenseItem, ChickenIncome, ChickenExpense, HotPotIncome, HotPotExpense, HomeExpense


class IndexView(TemplateView):
    template_name = 'account/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        start_of_month = timezone.now().replace(day=1)

        chicken_items = ChickenIncome.objects.filter(date__gte=start_of_month)
        hotpot_items = HotPotIncome.objects.filter(date__gte=start_of_month)
        income_items = chain(chicken_items, hotpot_items)

        expense_items = chain(ChickenExpense.objects.filter(date__gte=start_of_month), HotPotExpense.objects.filter(date__gte=start_of_month), HomeExpense.objects.filter(date__gte=start_of_month))

        expense = sum([x.value for x in expense_items])
        chicken = sum([x.value for x in chicken_items])
        hotpot = sum([x.value for x in hotpot_items])
        total = sum([x.value for x in income_items]) - expense

        context['total'] = f"{(total):,}"
        context['chicken'] = f"{chicken:,}"
        context['hotpot'] = f"{(hotpot):,}"
        context['expense'] = f"{(expense):,}"

        return context


class ChickenView(TemplateView):
    template_name = 'account/chicken.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if (item_id := self.request.GET.get('n')) is not None:
            type = self.request.GET.get('t')
            if type == 'income':
                item = ChickenIncome.objects.get(id=item_id)
            elif type == 'expense':
                item = ChickenExpense.objects.get(id=item_id)
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
            item = ChickenIncome.objects.get(id=item_id)
        elif type == 'income':
            item = ChickenIncome()
        elif item_id and type == 'expense':
            item = ChickenExpense.objects.get(id=item_id)
        elif type == 'expense':
            item = ChickenExpense()

        item.date = date
        item.value = value
        item.remark = remark

        if type == 'income':
            item.volume = chicken
        elif type == 'expense':
            item.item_id = category

        item.save()

        return JsonResponse({
            'status': True
        })


class HotPotView(TemplateView):
    template_name = 'account/hotpot.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if (item_id := self.request.GET.get('n')) is not None:
            type = self.request.GET.get('t')
            if type == 'income':
                item = HotPotIncome.objects.get(id=item_id)
            elif type == 'expense':
                item = HotPotExpense.objects.get(id=item_id)
            context['type'] = type
            context['item'] = item

        context['categories'] = ExpenseItem.objects.filter(hot_pot=True).order_by('name')
        context['today'] = timezone.now()

        return context

    def post(self, request, **kwargs):
        method = request.POST['method']
        item_id = request.POST['id'] if method == 'edit' else None
        type = request.POST['type']
        date = request.POST['date']
        value = request.POST['value']
        category = request.POST['category']
        remark = request.POST['remark']

        if item_id and type == 'income':
            item = HotPotIncome.objects.get(id=item_id)
        elif type == 'income':
            item = HotPotIncome()
        elif item_id and type == 'expense':
            item = HotPotExpense.objects.get(id=item_id)
        elif type == 'expense':
            item = HotPotExpense()

        item.date = date
        item.value = value
        item.remark = remark

        if type == 'expense':
            item.item_id = category

        item.save()

        return JsonResponse({
            'status': True
        })


class HomeExpenseView(TemplateView):
    template_name = 'account/expense.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if (item_id := self.request.GET.get('n')) is not None:
            item = HomeExpense.objects.get(id=item_id)
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
            item = HomeExpense.objects.get(id=item_id)
        else:
            item = HomeExpense()

        item.date = date
        item.value = value
        item.item_id = category
        item.remark = remark
        item.save()

        return JsonResponse({
            'status': True
        })


class ReportView(TemplateView):
    template_name = 'account/report.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class SystemManagementView(TemplateView):
    template_name = 'account/system.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        cat = self.request.GET.get('cat', '1')

        if cat == '1':
            items = ExpenseItem.objects.filter(chicken=True).order_by('name')
        elif cat == '2':
            items = ExpenseItem.objects.filter(hot_pot=True).order_by('name')
        elif cat == '3':
            items = ExpenseItem.objects.filter(home=True).order_by('name')

        context['items'] = items
        context['cat'] = cat

        return context

