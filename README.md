# json_repository
A simple json repository

# Install

[https://pypi.org/project/json-repository/](Pypi) 

pip install json-repository

# Examples

## Creating custom repository 

```python
class FoobarRepository(BaseJsonRepository):
  def __init__(self):
    super(FoobarRepository, self).__init__("foo")
```

## using created repository

```python
  with FoobarRepository() as repo:
    for entity in repo.get_all():
      repo.delete(entity)
    repo.context.commit()
```