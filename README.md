# bigdata6
宿題のやーつー

# reader.py usage

2008.txt ~ 2016.txt と同じディレクトリに置きます

```
from reader import reader
r = reader()
next(r) #記事一つ分取り出す
[next(r) for _ in range(3)] # 3個取り出す
d = list(r) #全部取り出す, 一度全部パースするとcache.binが生成されてデータがキャッシュされます

import pandas as pd
df = pd.DataFrame(d) #pandasのデータフレームにする
```
