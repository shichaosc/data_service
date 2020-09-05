from student.models import AdsMdmStudent
from base.view_handler import ViewSetBase
from student.serializers import StudentSerializer
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import Max
from base.errors import NotFoundException, ParamsException
from rest_framework.decorators import action
from base.view_handler import JsonResponse
from rest_framework import status as http_status
import json
from django.conf import settings
import requests
from utils import utils
import logging
from student.student_evaluation import SUBJECT_ID_INFO, subject_id_select, calculate_socre

logger = logging.getLogger('info')

class StudentViewSet(ViewSetBase):

    '''学生数据接口'''

    # queryset = AdsMdmStudent
    serializer_class = StudentSerializer

    def get_queryset(self):
        return AdsMdmStudent.objects.all()

    def get_object(self):
        pk = self.kwargs.get('pk')
        if not pk:
            raise ParamsException
        now_date = (timezone.now() + timedelta(hours=-16)).strftime('%Y%m%d')
        ads_mdm_student = AdsMdmStudent.objects.filter(ds=now_date, student_user_id=pk).first()
        if not ads_mdm_student:
            max_student = AdsMdmStudent.objects.aggregate(Max('ds'))
            max_date = max_student.get('ds__max')
            ads_mdm_student = AdsMdmStudent.objects.filter(ds=max_date, student_user_id=pk).first()
        if not ads_mdm_student:
            raise NotFoundException
        return ads_mdm_student

    @action(methods=['get'], detail=True)
    def evaluation_result(self, request, pk):
        '''学生测评结果'''
        subject_infos = request.query_params.get('subject_infos')
        if not subject_infos:
            return JsonResponse(code=1, msg='未找到学生测评答案')
        try:
            subject_infos = subject_infos.split(',')
            subject_infos = {subject_info.split('_')[0]: subject_info.split('_')[1] for subject_info in subject_infos}
        except Exception as e:
            logger.info('evaluation_result params error, error={}, params={}'.format(e, subject_infos))
            return JsonResponse(code=1, msg='params error')
        evaluation_results = {}
        subject_ids = list(subject_infos.keys())
        evaluation_results['couese_edition'] = 1 if '17' in subject_ids else 2
        if evaluation_results['couese_edition'] == 2:  # 国际版
            evaluation_results = self.international_evaluation(subject_infos, evaluation_results)
            evaluation_ability = self.international_ability(subject_infos)
        else:  # 高级版
            evaluation_results = self.advanced_evaluation(subject_infos, evaluation_results)
            evaluation_ability = self.advanced_ability(subject_infos)
        return JsonResponse(code=0, msg='success', data={'evaluation_results': evaluation_results, 'evaluation_ability': evaluation_ability})

    def international_evaluation(self, subject_infos, evaluation_results):
        '''国际版定级'''
        right_subject = []
        for subject_id, subject_result in subject_infos.items():
            if subject_result == '1':  #  正确
                right_subject.append(subject_id)
        right_subject_len = len(right_subject)
        all_subject_len = len(subject_infos.keys())

        if evaluation_results['course_edition'] == 2:  # 国际版
            if right_subject_len/all_subject_len < 0.8:
                evaluation_results['course_level'] = 'L1'
            else:
                evaluation_results['course_level'] = 'L2'
        return evaluation_results

    def advanced_evaluation(self, subject_infos, evaluation_results):
        '''高级版定级'''
        subject_level1_true_num = 0
        subject_level1_false_num = 0
        subject_level2_true_num = 0
        subject_level2_false_num = 0
        for subject_id, subject_result in subject_infos.items():
            subject_info = SUBJECT_ID_INFO.get(subject_id, {})
            if subject_result == '1':  #  正确
                if subject_info.get('apply_level') == 1:  # level 1
                    subject_level1_true_num = subject_level1_true_num + 1
                else:
                    subject_level2_true_num = subject_level2_true_num + 1
            else:  # 错误
                if subject_info.get('apply_level') == 1:
                    subject_level1_false_num = subject_level1_false_num + 1
                else:
                    subject_level2_false_num = subject_level2_false_num + 1
        level1_percent = subject_level1_true_num/(subject_level1_false_num + subject_level1_true_num)
        level2_percent = subject_level2_true_num/(subject_level2_true_num + subject_level2_false_num)
        if level1_percent < 0.5:  # l1
            evaluation_results['course_level'] = 'L1上'
        elif level1_percent >= 0.5 and level1_percent < 0.8:
            evaluation_results['course_level'] = 'L1中'
        else:
            if level2_percent < 0.5:
                evaluation_results['course_level'] = 'L1下'
            else:
                evaluation_results['course_level'] = 'L2'
        return evaluation_results

    def international_ability(self, subject_infos):
        '''
        国际版能力
        1	听力	国际版
        2	发音	国际版
        3	词汇	国际版
        4	拼音识读	国际版
        5	表达与运用	国际版
        '''
        hear_ability = {'right': 0, 'all': 0}  # 听力
        pronunciation_ability = {'right': 0, 'all': 0}  # 发音
        word_ability = {'right': 0, 'all': 0}  # 词汇
        pinyin_read_ability = {'right': 0, 'all': 0}  # 拼音识读
        express_apply_ability = {'right': 0, 'all': 0}  # 表达与运用
        for subject_id, subject_result in subject_infos.items():
            ability_ids = SUBJECT_ID_INFO.get(subject_id, {}).get('ability_id')
            for ability_id in ability_ids:
                if ability_id == 1:
                    if subject_result == '1':
                        hear_ability['right'] = hear_ability['right'] + 1
                    hear_ability['all'] = hear_ability['all'] + 1
                elif ability_id == 2:
                    if subject_result == '1':
                        pronunciation_ability['right'] = pronunciation_ability['right'] + 1
                    pronunciation_ability['all'] = pronunciation_ability['all'] + 1
                elif ability_id == 3:
                    if subject_result == '1':
                        word_ability['right'] = word_ability['right'] + 1
                    word_ability['all'] = word_ability['all'] + 1
                elif ability_id == 4:
                    if subject_result == '1':
                        pinyin_read_ability['right'] = pinyin_read_ability['right'] + 1
                    pinyin_read_ability['all'] = pinyin_read_ability['all'] + 1
                elif ability_id == 5:
                    if subject_result == '1':
                        express_apply_ability['right'] = express_apply_ability['right'] + 1
                    express_apply_ability['all'] = express_apply_ability['all'] + 1
        return {
            'hear_ability_score': calculate_socre(hear_ability['right'], hear_ability['all']),
            'pronunciation_ability_score': calculate_socre(pronunciation_ability['right'], pronunciation_ability['all']),
            'word_ability_score': calculate_socre(word_ability['right'], word_ability['all']),
            'pinyin_read_ability': calculate_socre(pinyin_read_ability['right'], pinyin_read_ability['all']),
            'express_apply_ability': calculate_socre(express_apply_ability['right'], express_apply_ability['all'])
        }

    def advanced_ability(self, subject_infos):
        '''
        6	听力	高级版   hear_ability
        7	拼音	高级版   pinyin_ability
        8	识字	高级版   learn_word_ability
        9	语音积累	高级版  speach_ability
        10	语音运用	高级版  speach_application_ability
        '''
        hear_ability = {'right': 0, 'all': 0}  # 听力
        pinyin_ability = {'right': 0, 'all': 0}  # 发音
        learn_word_ability = {'right': 0, 'all': 0}  # 词汇
        speach_ability = {'right': 0, 'all': 0}  # 拼音识读
        speach_application_ability = {'right': 0, 'all': 0}  # 表达与运用
        for subject_id, subject_result in subject_infos.items():
            ability_ids = SUBJECT_ID_INFO.get(subject_id, {}).get('ability_id')
            for ability_id in ability_ids:
                if ability_id == 6:
                    if subject_result == '1':
                        hear_ability['right'] = hear_ability['right'] + 1
                    hear_ability['all'] = hear_ability['all'] + 1
                elif ability_id == 7:
                    if subject_result == '1':
                        pinyin_ability['right'] = pinyin_ability['right'] + 1
                    pinyin_ability['all'] = pinyin_ability['all'] + 1
                elif ability_id == 8:
                    if subject_result == '1':
                        learn_word_ability['right'] = learn_word_ability['right'] + 1
                    learn_word_ability['all'] = learn_word_ability['all'] + 1
                elif ability_id == 9:
                    if subject_result == '1':
                        speach_ability['right'] = speach_ability['right'] + 1
                    speach_ability['all'] = speach_ability['all'] + 1
                elif ability_id == 10:
                    if subject_result == '1':
                        speach_application_ability['right'] = speach_application_ability['right'] + 1
                    speach_application_ability['all'] = speach_application_ability['all'] + 1
        return {
            'hear_ability_score': calculate_socre(hear_ability['right'], hear_ability['all']),
            'pronunciation_ability_score': calculate_socre(pinyin_ability['right'], pinyin_ability['all']),
            'word_ability_score': calculate_socre(learn_word_ability['right'], learn_word_ability['all']),
            'pinyin_read_ability': calculate_socre(speach_ability['right'], speach_ability['all']),
            'express_apply_ability': calculate_socre(speach_application_ability['right'], speach_application_ability['all'])
        }

    @action(methods=['get'], detail=True)
    def next_question(self, request, pk):
        '''
            获取下一题id
            判断学生有没有答题，没有答题获取学生标签，通过标签判断接下来的做题id
            学生做过题判断
        '''
        subject_infos = request.query_params.get('subject_infos')  # 1_1,2_1,3_2
        if not subject_infos:  # 没有答过题， 获取学生标签确定是否跳过前两题
            student_tags = utils.fetch_get_api(settings.STUDENT_TAG_URL)
            if not student_tags:  # 没有返回值，按照没有标签处理
                next_question_ids = [1, 2]
                return JsonResponse(code=0, msg='success',
                                    data={'next_question_ids': next_question_ids})
            else:
                '''判断学生标签，两个都是高级版走高级版测试， 否则走国际版测试'''
                pass

        subject_infos = subject_infos.split(',')
        subject_infos = [subject_info.split('_') for subject_info in subject_infos]
        subject_infos = sorted(subject_infos, key=lambda x: x[0])
        last_subject = subject_infos[-1]
        second_last_subject = subject_infos[-2]
        next_question_ids = subject_id_select(last_subject, second_last_subject)

        return JsonResponse(code=0, msg='success',
                            data={'next_question_ids': next_question_ids})

    def get_student_tag(self, student_user_id):

        tag_url = 'https://'
        response = requests.get(tag_url)
        result = response.json()
        return result


