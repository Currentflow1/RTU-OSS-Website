import random

from django.shortcuts import render


ROUNDS = 5
CHOICES = {"25", "50", "75"}


def generate_sequence(length=5):
  return [random.choice(["H", "T"]) for _ in range(length)]


def game(request):
  if request.method == "POST":
      choice = request.POST.get("choice")

      if choice not in CHOICES:
          return render(
              request,
              "easter/game.html",
              {"error": "Please select a probability."},
          )

      sequence = generate_sequence()
      next_flip = random.choice(["H", "T"])

      correct = choice == "50"

      return render(request, "easter/game.html", {
        "sequence": sequence,
        "next_flip": next_flip,
        "choice": choice,
        "correct": correct,
        "show_result": True,
      })

  return render(request, "easter/game.html", {
    "sequence": generate_sequence(),
    "show_result": False,
  })