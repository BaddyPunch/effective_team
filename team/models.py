from django.db import models


class Creator(models.Model):
    name = models.CharField(max_length=100)
    money = models.FloatField(default=0)

    def translation(self, recipient, amount):
        if amount <= 0:
            raise ValueError('Сумма должна быть больше 0')
        if self.money < amount:
            raise ValueError('Недостаточно средств')
        self.money -= amount
        recipient.money += amount
        self.save()
        recipient.save()

    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=100)
    creator = models.ForeignKey(Creator, on_delete=models.CASCADE, related_name='teams')

    def __str__(self):
        return self.name


class Member(models.Model):
    name = models.CharField(max_length=100)
    stamina = models.IntegerField(default=0)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, related_name='members')

    def __str__(self):
        return self.name


# class TeamRequest(models.Model):
#     member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='requests')
#     team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='requests')
#
#     def __str__(self):
#         return f"Request from {self.member} to {self.team}"


class TeamRequest(models.Model):
    member = models.ForeignKey('Member', on_delete=models.CASCADE, related_name='requests')
    team = models.ForeignKey('Team', on_delete=models.CASCADE, related_name='requests')

    MAX_REQUESTS_PER_TEAM = 3  # Задайте лимит на количество заявок в команду

    class WeakRequestError(Exception):
        pass

    def save(self, *args, **kwargs):
        existing_requests = TeamRequest.objects.filter(team=self.team).order_by('-member__stamina')

        if existing_requests.count() >= self.MAX_REQUESTS_PER_TEAM:
            lowest_stamina_request = existing_requests.last()
            if lowest_stamina_request.member.stamina < self.member.stamina:
                lowest_stamina_request.delete()
            else:
                raise TeamRequest.WeakRequestError("Your stamina is too low to join this team.")

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Request from {self.member.name} to {self.team.name}"