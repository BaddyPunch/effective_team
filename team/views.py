from django.shortcuts import render, get_object_or_404
from .models import Creator, Team, Member
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from django.http import HttpResponseBadRequest, HttpResponseForbidden
from .forms import TeamForm, CreatorForm, MemberForm, TeamRequest, ProcessTeamRequestsForm, TeamRequestForm

MAX_REQUESTS = 5


def creator_list(request):
    creators = Creator.objects.all()
    return render(request, 'team/creator_list.html', {'creators': creators})


def team_list(request):
    teams = Team.objects.all()
    return render(request, 'team/team_list.html', {'teams': teams})


def member_list(request):
    members = Member.objects.all()
    return render(request, 'team/member_list.html', {'members': members})


@csrf_exempt
def create_creator(request):
    if request.method == 'POST':
        form = CreatorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('creator_list')
        else:
            return render(request, 'team/create_creator.html', {'form': form})
    else:
        form = CreatorForm()

    return render(request, 'team/create_creator.html', {'form': form})


def transfer_money(request):
    if request.method == 'POST':
        sender_id = request.POST.get('sender_id')
        recipient_id = request.POST.get('recipient_id')
        try:
            amount = float(request.POST.get('amount'))
        except (TypeError, ValueError):
            return HttpResponseBadRequest("Некорректная сумма перевода")

        sender = get_object_or_404(Creator, name=sender_id)
        recipient = get_object_or_404(Creator, name=recipient_id)

        try:
            sender.translation(recipient, amount)
            context = {"success": True, "message": "Перевод выполнен успешно"}
        except ValueError as e:
            context = {"success": False, "message": str(e)}

        return render(request, "team/transfer_money.html", context)
    else:
        return render(request, "team/transfer_money.html", {"success": False, "message": "Только POST-запросы поддерживаются"})


def create_team(request):
    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('team_list')
    else:
        form = TeamForm()
    return render(request, 'team/team_creator.html', {'form': form})


@csrf_exempt
def delete_creator(request, pk):
    creator = get_object_or_404(Creator, pk=pk)
    if request.method == 'POST':
        creator.delete()
        return redirect('creator_list')
    return render(request, 'team/delete_creator.html', {'creator': creator})


@csrf_exempt
def delete_team(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    if request.method == "POST":
        team.delete()
        return redirect('team_list')
    return render(request, 'team/delete_team.html', {'team': team})


def edit_team(request, team_id):
    team = get_object_or_404(Team, id=team_id)

    if request.method == 'POST':
        name = request.POST.get('name')  # Получаем новое имя из данных POST-запроса
        if name:  # Проверяем, что имя передано
            team.name = name  # Обновляем поле name
            team.save()  # Сохраняем изменения
            return redirect('team_list')
        else:
            error = "Название команды не может быть пустым."
            return render(request, 'edit_team.html', {'team': team, 'error': error})

    return render(request, 'team/team_edit.html', {'team': team})


def edit_creator(request, pk):
    creator = get_object_or_404(Creator, pk=pk)

    if request.method == 'POST':
        name = request.POST.get('name')  # Получаем новое имя из данных POST-запроса
        if name:  # Проверяем, что имя передано
            creator.name = name  # Обновляем поле name
            creator.save()  # Сохраняем изменения
            return redirect('creator_list')
        else:

            return render(request, 'creator_edit.html', {'creator': creator})

    return render(request, 'team/creator_edit.html', {'creator': creator})


def create_member(request):
    if request.method == 'POST':
        form = MemberForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('member_list')
    else:
        form = MemberForm()
    return render(request, 'team/create_member.html', {'form': form})


def create_team_request(request):
    if request.method == 'POST':
        form = TeamRequestForm(request.POST)
        if form.is_valid():
            team_request = form.save(commit=False)
            try:
                team_request.save()
                return redirect('success_page')
            except TeamRequest.WeakRequestError as e:
                form.add_error(None, str(e))
    else:
        form = TeamRequestForm()

    return render(request, 'team/team_requests.html', {'form': form})


