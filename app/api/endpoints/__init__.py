# from .guest import router as guest_router  # noqa
# from .car import router as car_router  # noqa
# from .point import router as point_router  # noqa
# from .user import router as user_router  # noqa
# from .payments import router as payment_router  # noqa

from .guest.guest import router as guest_router  # noqa
from .payments.payment import router as payment_router  # noqa
from .point.point import router as point_router  # noqa
from .reports.reports import router as reports_router  # noqa
from .sending_ads.sending_ads import router as sending_ads_router  # noqa
from .user.user import router as user_router  # noqa

