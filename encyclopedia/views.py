from django.shortcuts import render

from . import util
from markdown2 import Markdown


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
      "title": title.capitalize()
    })
  else:
    return render(request, "encyclopedia/not_found.html", {
      "page": "wiki"
    })

def create_new_wiki(request):
  return render(request, "encyclopedia/create_new.html")
  
  

def not_found(request, exception):
  return render(request, "encyclopedia/not_found.html", status=404)