from rest_framework.routers import DefaultRouter

from events.views import EventViewSet,CategoryViewSet,TicketViewSet,BookingViewSet

router = DefaultRouter()

router.register('events',EventViewSet, basename='events')
router.register('category', CategoryViewSet, basename='category')
router.register('tickets', TicketViewSet, basename='tickets')
router.register('booking', BookingViewSet, basename='booking')

urlpatterns = router.urls

