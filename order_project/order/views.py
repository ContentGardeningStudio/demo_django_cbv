from django.views.generic import ListView
from django.http import JsonResponse, HttpResponse
from .models import Order
import csv


class OrderListView(ListView):
    model = Order
    context_object_name = "orders"
    template_name = "orders.html"

    def get(self, request, *args, **kwargs):
        # format demandé : html (par défaut), json ou csv
        self.format = request.GET.get("format", "html")
        return super().get(request, *args, **kwargs)

    def render_to_response(self, context):
        orders = context["object_list"]

        if self.format == "json":
            return JsonResponse(
                list(orders.values("name", "total")),
                safe=False
            )

        if self.format == "csv":
            response = HttpResponse(content_type="text/csv")
            response["Content-Disposition"] = "attachment; filename=orders.csv"

            writer = csv.writer(response)
            writer.writerow(["name", "total"])

            for order in orders:
                writer.writerow([order.name, order.total])

            return response

        # HTML par défaut
        return super().render_to_response(context)
