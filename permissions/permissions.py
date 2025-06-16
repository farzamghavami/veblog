from rest_framework.permissions import BasePermission
from rest_framework import permissions
from django.contrib.auth import get_user_model


User = get_user_model()




class IsOwnerOrAdmin(BasePermission):
    """
    اجازه فقط برای ادمین یا صاحب آبجکت.
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff or request.user.is_superuser:
            return True

        user = self._extract_user(obj)
        return user == request.user

    def _extract_user(self, obj):
        """
        استخراج کاربر از آبجکت یا آبجکت‌های مرتبط.
        """
        # اگر خود obj از جنس User باشه
        if isinstance(obj, User):
            return obj

        # حالت مستقیم
        for attr in ["user", "owner","author"]:
            if hasattr(obj, attr):
                return getattr(obj, attr)

        # حالت غیرمستقیم
        for relation in ["order", "shop", "product",]:
            related_obj = getattr(obj, relation, None)
            if related_obj:
                for attr in ["user", "owner","author"]:
                    if hasattr(related_obj, attr):
                        return getattr(related_obj, attr)

        return None