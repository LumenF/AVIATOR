from django.db import models, transaction, router
from django.db.models.signals import post_save, pre_save

from service.image.zip import zip_image
from src.abstractions.models import AbstractModel
from src.abstractions.service import get_amount_point
from src.product.product_base.models import BaseProduct


class NewProductParametersModel(AbstractModel):
    """Параметры для новых устройств ы"""

    class Meta:
        verbose_name = 'Параметры названия'
        verbose_name_plural = 'Параметры названия'

    product = models.ForeignKey(
        verbose_name='Товар',
        to='product_base.BaseProduct',
        on_delete=models.CASCADE,
    )
    parameter = models.ForeignKey(
        verbose_name='Параметр',
        to='region.WordsModel',
        on_delete=models.SET_NULL,
        null=True,
    )
    author = None

    def __str__(self):
        return self.product.name

    def save(
            self,
            force_insert=False,
            force_update=False,
            using=None,
            update_fields=None
    ):
        self.save_base(
            using=using,
            force_insert=force_insert,
            force_update=force_update,
            update_fields=update_fields,
        )
        #
        # NewProductModel.objects.get(
        #     id=self.product.id
        # ).save(update_name=True)
    #
    # def delete(self, using=None, keep_parents=False):
    #     if self.pk is None:
    #         raise ValueError(
    #             "%s object can't be deleted because its %s attribute is set "
    #             "to None." % (self._meta.object_name, self._meta.pk.attname)
    #         )
    #     using = using or router.db_for_write(self.__class__, instance=self)
    #     collector = Collector(using=using, origin=self)
    #     collector.collect([self], keep_parents=keep_parents)
    #     collector.delete()
    #
    #     NewProductModel.objects.get(
    #         id=self.product.id
    #     ).save(update_name=True)


class NewProductModel(BaseProduct):
    """Новые товары"""

    class Meta:
        verbose_name = 'Новый товар'
        verbose_name_plural = 'Новые товары'
        ordering = ('id',)

    series = models.ForeignKey(
        to='params.SeriesModel',
        verbose_name='Серия',
        on_delete=models.CASCADE,
    )
    text_post = models.TextField(
        verbose_name='Описание',
    )
    is_moderation = None

    def __str__(self):
        return self.name

    def save(
            self,
            force_insert=False,
            force_update=False,
            using=None,
            update_fields=None,
            update_name=None,
    ):
        self.save_base(
            using=using,
            force_insert=force_insert,
            force_update=force_update,
            update_fields=update_fields,
        )
        params = NewProductParametersModel.objects.filter(
            product=self
        )
        product_name = str(self.series) + ' ' \
                       + "".join([str(i.parameter.name) + ' ' for i in params]) \
                       + get_amount_point(int(self.amount)) + '₽'
        self.name = product_name

        self.save_base(
            using=using,
            force_insert=force_insert,
            force_update=force_update,
            update_fields=update_fields,
        )


def path_new_image(instance,
                   filename):
    return 'new/{0}/{1}/{2}'.format(
        instance.product.series.device.group.name.replace(' ', '_'),
        instance.product.series.name.replace(' ', '_'),
        filename
    )


class ImageNewProductModel(AbstractModel):
    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'

    product = models.ForeignKey(
        to='product_new.NewProductModel',
        on_delete=models.CASCADE,
        verbose_name='Новый товар',
    )
    image = models.ImageField(
        upload_to=path_new_image,
        verbose_name='Изображение',
    )
    author = None

    def __str__(self):
        return self.product.name

    def save_base(
            self,
            raw=False,
            force_insert=False,
            force_update=False,
            using=None,
            update_fields=None,
    ):

        using = using or router.db_for_write(self.__class__, instance=self)
        assert not (force_insert and (force_update or update_fields))
        assert update_fields is None or update_fields
        cls = origin = self.__class__
        # Skip proxies, but keep the origin as the proxy model.
        if cls._meta.proxy:
            cls = cls._meta.concrete_model
        meta = cls._meta
        if not meta.auto_created:
            pre_save.send(
                sender=origin,
                instance=self,
                raw=raw,
                using=using,
                update_fields=update_fields,
            )
        # A transaction isn't needed if one query is issued.
        if meta.parents:
            context_manager = transaction.atomic(using=using, savepoint=False)
        else:
            context_manager = transaction.mark_for_rollback_on_error(using=using)
        with context_manager:
            parent_inserted = False
            if not raw:
                parent_inserted = self._save_parents(cls, using, update_fields)
            updated = self._save_table(
                raw,
                cls,
                force_insert or parent_inserted,
                force_update,
                using,
                update_fields,
            )
        # Store the database on which the object was saved
        self._state.db = using
        # Once saved, this is no longer a to-be-added instance.
        self._state.adding = False

        # Signal that the save is complete
        if not meta.auto_created:
            post_save.send(
                sender=origin,
                instance=self,
                created=(not updated),
                update_fields=update_fields,
                raw=raw,
                using=using,
            )
        zip_image(input_image_path='media/' + str(self.image),
                  output_image_path='media/' + str(self.image),
                  size=(800, 800))