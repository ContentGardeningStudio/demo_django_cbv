from django.views.generic import ListView
from django.http import JsonResponse, HttpResponse
from .models import Order
from django.db.models import Q
import csv


class ExportMixin:
    """
    Reusable export logic for any ListView.
    """
    export_formats = ("json", "csv")

    def get_export_format(self):
        return self.request.GET.get("format")

    def render_export(self, queryset):
        export_format = self.get_export_format()

        if export_format == "json":
            return JsonResponse(
                list(queryset.values("name", "total")),
                safe=False
            )

        if export_format == "csv":
            response = HttpResponse(content_type="text/csv")
            response["Content-Disposition"] = "attachment; filename=orders.csv"

            writer = csv.writer(response)
            writer.writerow(["name", "total"])

            for obj in queryset:
                writer.writerow([obj.name, obj.total])

            return response

        return None


class OrderListView(ExportMixin, ListView):
    model = Order
    context_object_name = "orders"
    template_name = "orders.html"
    paginate_by = 10  # CBV superpower

    def get_queryset(self):
        """
        Filtering logic belongs here — very CBV-ish.
        """
        qs = super().get_queryset()

        search = self.request.GET.get("search")
        if search:
            qs = qs.filter(
                Q(name__icontains=search)
            )

        return qs

    def render_to_response(self, context, **response_kwargs):
        """
        Single override point for all formats.
        """
        export_response = self.render_export(context["object_list"])
        if export_response:
            return export_response

        return super().render_to_response(context, **response_kwargs)
