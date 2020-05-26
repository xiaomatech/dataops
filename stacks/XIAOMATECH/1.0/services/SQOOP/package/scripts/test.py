import os
abc = os.path.realpath(__file__).split('/services')
print(abc[0] + '/../../../stack-hooks')
