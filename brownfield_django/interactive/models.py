from django.db import models


INTERACTIVE_TYPE = (
    ('TS', 'Testing'),
    ('SH', 'Site History'),
    ('VR', 'Visual Reconassence'),
)

TEST_OPTIONS = (
    ('EX', 'Excavation'),
    ('DP', 'Drilling/Push'),
    ('GR', 'GPR'),
    ('MD', 'MMD'),
    ('SG', 'SGSA'),
    ('TS', 'Topographic Survey'),
    ('ST', 'Super Test'),                               
)

# SITE_HISTORY_OPTIONS = (
#     ('EX', 'Excavation'),
#     ('DP', 'Drilling/Push'),
#     ('GR', 'GPR'),
#     ('MD', 'MMD'),
#     ('SG', 'SGSA'),
#     ('TS', 'Topographic Survey'),
#     ('ST', 'Super Test'), 
#     Commercial
#         BTEX Gas Satation
#         Firn Freeze
#         Kilroy's Bar
#         Plucker's Scrap Metal
#         Roche Mountonee Vineyard
#         Self-Lume Factory
#         Tillie's All-Night Diner
#         Wedging Nursery
# 
#     Government
#         Municipal Government
#         Town Well
#         Water Tower
# 
#     Residential
#         Eolian Acres
#         Fallow Home
#         Four Homes of Erratic
#         Kame Kondos
# )

# Create your models here.
class Interactive(models.Model):
    '''Course'''
    interactive_type = models.CharField(max_length=2, choices=INTERACTIVE_TYPE)


    def __unicode__(self):
        return self.name

