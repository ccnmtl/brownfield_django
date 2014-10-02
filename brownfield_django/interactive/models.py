from django.db import models

TEST_OPTIONS = (
    ('EX', 'Excavation'),
    ('DP', 'Drilling/Push'),
    ('GR', 'GPR'),
    ('MD', 'MMD'),
    ('SG', 'SGSA'),
    ('TS', 'Topographic Survey'),
    ('ST', 'Super Test'),
)


class VisualReconnaisence(models.Model):
    '''This part of the interactive consists of simply showing the user content
    needs to be saved somewhere, if used deduct $100 from budget'''
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name


class SiteHistory(models.Model):
    '''This part of the interactive consists of showing the user content
    and deducts money based on how many questions they ask people'''
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name


class Testing(models.Model):
    '''Course'''
    interactive_type = models.CharField(max_length=2, choices=TEST_OPTIONS)

    def __unicode__(self):
        return self.name
