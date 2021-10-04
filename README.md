# tagspaces_getter

```python
from tagspaces_getter import Tags
from tagspaces_getter import TagDef
from pathlib import Path

tags = Tags(Path("./cocricot/test/beachparasol_yellow.json"))
skip = TagDef("skip", "#fa573cff", "white")
tags.add(skip)
print(tags.tags)
```