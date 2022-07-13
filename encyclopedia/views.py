from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from random import randrange
from . import util
from markdown2 import Markdown

class NewWikiForm(forms.Form):
  title = forms.CharField(label="Wiki Title")
  content = forms.CharField(widget=forms.Textarea())

class EditWikiForm(forms.Form):
  title = forms.CharField(label="Wiki Title")
  content = forms.CharField(widget=forms.Textarea())

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wiki(request, title):
  print(f"get_entry: {util.get_entry(title)}")
  markDownPage = util.get_entry(title)
  markdowner = Markdown()
  if markDownPage:
    return render(request, "encyclopedia/wiki.html", {
      "content": markdowner.convert(markDownPage),
      "title": title.upper()
    })
  else:
    return render(request, "encyclopedia/not_found.html", {
      "page": "wiki"
    })

def create_new_wiki(request):
  if request.method == "POST":
    form = NewWikiForm(request.POST)
    if form.is_valid():
      title = form.cleaned_data["title"]
      if util.get_entry(title) != None:
        return render(request, "encyclopedia/create_new.html", {
          "form": form,
          "error": "There's a wiki with the same title, please choose a different title"
        })
      content = form.cleaned_data["content"]
      util.save_entry(title, content)
      return HttpResponseRedirect(f"/wiki/{title}")
    else:
      return render(request, "encyclopedia/create_new.html", {
        "form": form
      })
  return render(request, "encyclopedia/create_new.html", {
    "form": NewWikiForm()
  })

def edit_wiki(request, title):
  if request.method == "POST":
    form = EditWikiForm(request.POST)
    print(form)
    if form.is_valid():
      title = form.cleaned_data["title"]
      content = form.cleaned_data["content"]
      util.save_entry(title, content)
      return HttpResponseRedirect(f"/wiki/{title}")
    else:
      return render(request, "encyclopedia/edit-wiki.html", {
        "form": form
      })
  else:
    entry = util.get_entry(title)
    return render(request, "encyclopedia/edit-wiki.html", {
      "form": EditWikiForm({
        "title": title,
        "content": entry
      }),
      "title": title
    })

def random_page(request):
  entryList = util.list_entries()
  number = randrange(len(entryList))
  print(entryList)
  print(number)
  markDownPage = util.get_entry(entryList[number])
  markdowner = Markdown()
  
  return HttpResponseRedirect(f"/wiki/{entryList[number]}", {
      "content": markdowner.convert(markDownPage),
      "title": entryList[number].upper()
  })

def not_found(request, exception):
  return render(request, "encyclopedia/not_found.html", status=404)

def search_page(request):
  if request.method == "POST":
    searchWord = request.POST["q"]
    if util.get_entry(searchWord) != None:
      markDownPage = util.get_entry(searchWord)
      markdowner = Markdown()
      if markDownPage:
        return HttpResponseRedirect(f"wiki/{searchWord}", {
          "content": markdowner.convert(markDownPage),
          "title": searchWord.upper()
        })
    searchResults = []
    print(searchWord)
    entryList = util.list_entries()
    print(entryList)
    for entry in entryList:
      print(searchWord in entry)
      if searchWord.lower() in entry.lower():
        searchResults.append(entry)
    print(searchResults)
    return render(request, "encyclopedia/search_page.html", {
      "entries": searchResults
    })
