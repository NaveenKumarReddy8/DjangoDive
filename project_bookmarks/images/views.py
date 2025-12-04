from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from images.forms import ImageCreateForm
from images.models import Image

# Create your views here.


@login_required
def image_create(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_image: Image = form.save(commit=False)
            new_image.user = request.user
            new_image.save()
            messages.success(request, "Image added successfully")
            return redirect(new_image.get_absolute_url())
    else:
        form = ImageCreateForm(data=request.GET)
    return render(
        request=request,
        template_name="images/image/create.html",
        context={
            "section": "images",
            "form": form,
        },
    )
