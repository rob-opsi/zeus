from zeus.config import db
from zeus.db.mixins import RepositoryBoundMixin
from zeus.db.utils import model_repr


class RepositoryRef(RepositoryBoundMixin, db.Model):
    name = db.Column(db.String, primary_key=True)

    __tablename__ = 'repository_ref'
    __repr__ = model_repr('repository_id', 'name')
