from flask import request
from flask_restful import Resource

from core.web.api.api import render


class CrudApi(Resource):

    def delete(self, id):
        obj = self.objectmanager.objects.get(id=id)
        obj.delete()
        return render({"status": "ok"})

    def get(self, id=None, template=None):
        if id:
            data = self.objectmanager.objects.get(id=id).info()
        else:
            data = [d.info() for d in self.objectmanager.objects.all()]

        if not template:  # template has not been overridden in URL
            if not id:  # determine if we're listing or displaying a single object
                template = self.template
            else:
                template = self.template_single

        return render(data, template=template)

    def post(self, id=None):
        if not id:
            return render(self.objectmanager(**request.json).save().info())
        else:
            self.objectmanager.update(id, request.json)

        return render({"status": "ok"})
