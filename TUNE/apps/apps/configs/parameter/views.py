import csv
import urllib.request

from django.shortcuts import render

from apps.apps.configs.parameter.models import CSVModel


def show_csv(request, pk=None):
    q_csv = CSVModel.objects.filter(id=pk)
    if not q_csv:
        context = {'data': {}, 'file': False}
        return render(request, 'html/tb_csv.html', context=context)

    response = urllib.request.urlopen(q_csv[0].file.url)
    lines = [i.decode('utf-8') for i in response.readlines()]

    reader = csv.DictReader(lines, delimiter=';')
    headers = []
    data = []
    for key in reader:
        for i, value in key.items():
            headers.append(i)
        break
    for row in reader:
        row: dict
        if row['Title'] and row['Editions'] and row['Parent UID']:
            data.append({
                'Price': row['Price'],
                'Title': row['Title'],
            })

    return render(
        request=request,
        template_name='html/tb_csv.html',
        context={
            'data': data,
            'file': True,
            'title': q_csv[0].city.name
        }
    )


def show_csv_only_amount(request, pk=None):
    q_csv = CSVModel.objects.filter(id=pk)
    if not q_csv:
        context = {'data': {}, 'file': False}
        return render(request, 'html/tb_csv.html', context=context)

    response = urllib.request.urlopen(q_csv[0].file.url)
    lines = [i.decode('utf-8') for i in response.readlines()]

    reader = csv.DictReader(lines, delimiter=';')
    headers = []
    data = []
    for key in reader:
        for i, value in key.items():
            headers.append(i)
        break
    for row in reader:
        row: dict
        if row['Title'] and row['Editions'] and row['Parent UID']:
            if int(row['Price'].replace(',', '')) != 0:
                data.append({
                    'Price': row['Price'],
                    'Title': row['Title'],
                })

    return render(
        request=request,
        template_name='html/tb_csv.html',
        context={
            'data': data,
            'file': True,
            'title': q_csv[0].city.name
        }
    )
