from rest_framework.generics import ListCreateAPIView, DestroyAPIView, UpdateAPIView, RetrieveAPIView


class OrderListCreateView(ListCreateAPIView):
    pass
    # queryset =
    # serializer_class =
    # permission_classes = []


class OrderUpdateDeleteView(DestroyAPIView, UpdateAPIView):
    pass


class OrderCountDetailView(RetrieveAPIView):
    pass


class OrderCompleteCountView(RetrieveAPIView):
    pass
