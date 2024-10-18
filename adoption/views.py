from django.http import HttpResponse
from django.shortcuts import redirect, render
from . forms import InterestForm
from adoption.models import Interest, Pet

# Create your views here.
def index(request):
    pets = Pet.objects.all()
    context = {"pets" : pets}
    return render(request, 'adoption/index.html', context)

def pet_details(request, pet_id):
    pet = Pet.objects.get(id=pet_id)
    if request.method == "POST":
        form = InterestForm(request.POST)
        if form.is_valid():
            Interest.objects.create(pet=pet, email=form.cleaned_data["email"], text=form.cleaned_data.get('text', ''))
            # return redirect("adoption:pet_list")
            form = InterestForm()
            message = "Thanks for your interest! The owner will get in touch with you shortly!"
    else:
        form = InterestForm()
        message = None

    context = {"pet": pet, 'form': form, 'message': message}
    return render(request, 'adoption/pet_details.html', context)