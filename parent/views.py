from parent.models import AdsMdmParent
from base.view_handler import ViewSetBase
from parent.serializers import ParentSerializer
from base.errors import NotFoundException, ParamsException
from datetime import timedelta
from django.utils import timezone
from django.db.models import Max


class ParentViewSet(ViewSetBase):

    '''家长数据接口'''

    queryset = AdsMdmParent
    serializer_class = ParentSerializer

    def get_object(self):
        pk = self.kwargs.get('pk')
        if not pk:
            raise ParamsException
        now_date = (timezone.now() + timedelta(hours=-16)).strftime('%Y%m%d')
        ads_mdm_parent = AdsMdmParent.objects.filter(ds=now_date, parent_user_id=pk).first()
        if not ads_mdm_parent:
            max_parent = AdsMdmParent.objects.aggregate(Max('ds'))
            max_date = max_parent.get('ds__max')
            ads_mdm_parent = AdsMdmParent.objects.filter(ds=max_date, parent_user_id=pk).first()
        if not ads_mdm_parent:
            raise NotFoundException
        return ads_mdm_parent