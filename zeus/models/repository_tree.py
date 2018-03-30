from typing import List

from zeus.config import db
from zeus.db.mixins import RepositoryBoundMixin
from zeus.db.types import GUID
from zeus.db.utils import model_repr
from zeus.exceptions import MissingRevision


class RepositoryTree(RepositoryBoundMixin, db.Model):
    """
    A tree is a fast-access flat mapping for a given ref.

    It, for example, lets you answer ``git log master``, where you identify
    master by name in the ``RepositoryRef`` model.

    The tree is updated on push, and will automatically rewrite relevant entries
    upon a force push, removing invalid references.
    """
    ref_id = db.Column(GUID, db.ForeignKey(
        'author.id'), primary_key=True)
    order = db.Column(db.Integer, primary_key=True)
    revision_sha = db.Column(db.String(40), db.ForeignKey(
        'revision.sha'))

    revision = db.relationship('Revision', foreign_keys=[revision_sha])
    ref = db.relationship('RepositoryRef', foreign_keys=[ref_id])

    __tablename__ = 'repository_tree'
    __table_args__ = (db.UniqueConstraint(
        'ref_id',
        'revision_sha',
        name='unq_tree_revision',
    ), )
    __repr__ = model_repr('repository_id', 'order', 'revision_sha')

    @classmethod
    def update_tree(cls, ref_id: GUID, parent_sha: str, new_revisions: List[str]):
        """
        Update a the cached tree for ``ref_id`` beginning at ``parent_sha``.

        ``new_revisions`` should be passed in commit order, with the oldest being
        first. Thus, given the following tree:

        A -> B -> C -> D

        If you are passing ``parent_sha=B``, ``new_revisions`` should be ``[C, D]``.

        If the ``parent_sha`` does not exist, a ``MissingRevision`` exception will be
        raised.
        """
        tree_base = cls.query.filter(
            cls.ref_id == ref_id,
            cls.revision_sha == parent_sha,
        ).first()
        if not tree_base:
            raise MissingRevision('Revision {} not found in tree'.format(
                parent_sha,
            ))

        with db.session.begin_nested():
            cls.query.filter(
                cls.ref_id == ref_id,
                cls.order > tree_base.order,
            ).delete()
            cur_parent_sha = parent_sha
            for revision_sha in new_revisions:
                db.session.add(cls(
                    ref_id=ref_id,
                    parent_sha=cur_parent_sha,
                    revision_sha=revision_sha,
                ))
                cur_parent_sha = revision_sha
