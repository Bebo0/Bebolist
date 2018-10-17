from django.http import HttpResponse
from lists.models import List, Item
from lists.forms import (DUPLICATE_ITEM_ERROR, EMPTY_ITEM_ERROR)
from rest_framework import routers, serializers, viewsets
from rest_framework.validators import UniqueTogetherValidator

# def list(request, list_id):
# 	list_ = List.objects.get(id=list_id)
# 	if request.method == 'POST':
# 		Item.objects.create(list=list_, text=request.POST['text'])
# 		return HttpResponse(status=201)		
# 	item_dicts = [
# 		{'id': item.id, 'text': item.text}
# 		for item in list_.item_set.all()
# 	]
# 	return HttpResponse(
# 		json.dumps(item_dicts),
# 		content_type='application/json'
# 		)

# ModelSerializers are DjangoRestFrameworks' way of converting
# from Django database models to JSON (or possibly other formats)
class ItemSerializer(serializers.ModelSerializer):

	text = serializers.CharField(
		allow_blank=False, error_messages={'blank': EMPTY_ITEM_ERROR})
	class Meta:
		model = Item
		fields = ('id', 'list', 'text')
		validators = [
			UniqueTogetherValidator(
				queryset=Item.objects.all(),
				fields=('list', 'text'),
				message=DUPLICATE_ITEM_ERROR
				)]


class ListSerializer(serializers.ModelSerializer):
	items = ItemSerializer(many=True, source='item_set')

	class Meta:
		model = List
		fields = ('id', 'items',)

# A ModelViewSet is DRF's way of defining all the different
# ways you can interact with the objects for a particular
# model via your API. After defining the queryset and serializer_class,
# it will automatically build views for you that will let you list,
# retrieve, update, and even delete objects.
class ListViewSet(viewsets.ModelViewSet):
	queryset = List.objects.all()
	serializer_class = ListSerializer

class ItemViewSet(viewsets.ModelViewSet):
	serializer_class = ItemSerializer
	queryset = Item.objects.all()
# A router is DRF's way of building URL configuration automatically,
# and mapping them to the functionality provided by the ViewSet.
router = routers.SimpleRouter()
router.register(r'lists', ListViewSet)
router.register(r'items', ItemViewSet)