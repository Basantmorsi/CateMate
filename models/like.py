from sqlmodel import Field, SQLModel, UniqueConstraint


class Like(SQLModel, table=True):
    # A like is one owner marking one cat as a favourite.
    __table_args__ = (UniqueConstraint("owner_id", "cat_id", name="uq_owner_cat_like"),)

    id: int | None = Field(default=None, primary_key=True)
    owner_id: int = Field(foreign_key="owner.id")
    cat_id: int = Field(foreign_key="cat.id")
