from tutor.models import AdsMdmTutor
from tutor.serializers import TutorSerializer
from student.models import AdsMdmStudent
from base.view_handler import ViewSetBase
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import Max
from base.errors import NotFoundException, ParamsException


class TutorViewSet(ViewSetBase):

    '''教师数据接口'''

    queryset = AdsMdmTutor
    serializer_class = TutorSerializer

    def get_object(self):
        pk = self.kwargs.get('pk')
        if not pk:
            raise ParamsException
        now_date = (timezone.now() + timedelta(hours=-16)).strftime('%Y%m%d')
        ads_mdm_tutor = AdsMdmTutor.objects.filter(ds=now_date, tutor_user_id=pk).first()
        if not ads_mdm_tutor:
            max_tutor = AdsMdmTutor.objects.aggregate(Max('ds'))
            max_date = max_tutor.get('ds__max')
            ads_mdm_tutor = AdsMdmTutor.objects.filter(ds=max_date, tutor_user_id=pk).first()
        if not ads_mdm_tutor:
            raise NotFoundException
        return ads_mdm_tutor