

import cufflinks as cf
import pandas as pd

cf.set_config_file(world_readable=True,offline=False)

cf.datagen.lines(1,200).ta_plot(study='rsi',periods=14,title='Relative Strength Index')

