from queries import q1
import os

import pyarrow.parquet as pq
import polars as pl
import dask.dataframe as dd
import pandas as pd

pd.options.mode.copy_on_write = True
pd.options.future.infer_string = True

lineitem = os.path.join('data', 'lineitem.parquet')

IO_FUNCS = {
    'pandas': lambda x: pd.read_parquet(x, engine='pyarrow'),
    'pandas[pyarrow]': lambda x: pd.read_parquet(x, engine='pyarrow', dtype_backend='pyarrow'),
    'polars[eager]': lambda x: pl.read_parquet(x),
    'polars[lazy]': lambda x: pl.scan_parquet(x),
    'pyarrow': lambda x: pq.read_table(x),
    'dask': lambda x: dd.read_parquet(x, engine='pyarrow', dtype_backend='pyarrow'),
}

print(q1.query(IO_FUNCS['pandas[pyarrow]'](lineitem)))
print(q1.query(IO_FUNCS['polars[lazy]'](lineitem)).collect())
print(q1.query(IO_FUNCS['pyarrow'](lineitem)))
print(q1.query(IO_FUNCS['dask'](lineitem)).compute())

