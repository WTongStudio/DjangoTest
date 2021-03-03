from django.db import models
from django.forms import model_to_dict
from base.time import date2timestamp


class BaseModel(models.Model):
    APP_ID = [(1, 'LiveMe'), (2, 'Fluxr'), (3, 'DSP'), ]

    app_id = models.IntegerField(verbose_name=u'应用id）', choices=APP_ID, default=1)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间', db_index=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name=u'更新时间', db_index=True)
    is_delete = models.BooleanField(verbose_name=u'是否被删除', default=False, db_index=True)

    class Meta:
        abstract = True

    @property
    def create_at(self):
        return int(date2timestamp(self.created_at))

    @property
    def update_at(self):
        return int(date2timestamp(self.updated_at))

    @classmethod
    def model_key(cls):
        opts = cls._meta
        return "%s:%s" % (opts.app_label, opts.db_table)

    @classmethod
    def filter_objects(cls, params, offset=0, limit=50):
        try:
            instances = cls.objects.filter(**params)[offset: offset + limit]
        except:
            return []
        return instances

    @classmethod
    def filter_objects_with_total_count(cls, params, offset=0, limit=50):
        try:
            queryset = cls.objects.filter(**params)
            return queryset.count(), queryset[offset: offset + limit]
        except:
            return 0, []

    @classmethod
    def filter_details(cls, params, offset=0, limit=50):
        instances = cls.filter_objects(params, offset, limit)
        if not instances:
            return []
        return [ins.to_dict() for ins in instances]

    @classmethod
    def filter_details_with_total_count(cls, params, offset=0, limit=50):
        """
        :param params:
        :param offset:
        :param limit:
        :return: total count, detail list
        """
        total_count, instances = cls.filter_objects_with_total_count(params, offset, limit)
        if not instances:
            return total_count, []
        return total_count, [ins.to_dict() for ins in instances]
