from dataclasses import dataclass

from jinja2 import Environment, FileSystemLoader, select_autoescape, Template

fileloader = FileSystemLoader("src/templates")
gtemplates = Environment(loader=fileloader, autoescape=select_autoescape())

@dataclass(frozen=True)
class HTMLTemplate:
    THANKYOU: Template = gtemplates.get_template("email/thankyou_contact.html")