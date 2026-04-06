from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from maat.models import Review, CategoryEnum

class ReviewRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, title: str, category: CategoryEnum, score: int, text: Optional[str] = None) -> Review:
        review = Review(
            title=title,
            category=category,
            score=score,
            text=text
        )
        self.session.add(review)
        self.session.commit()
        return review

    def get_all(self) -> List[Review]:
        stmt = select(Review).order_by(Review.created_at.desc())
        return list(self.session.execute(stmt).scalars().all())

    def delete(self, review_id: int) -> None:
        review = self.session.get(Review, review_id)
        if review:
            self.session.delete(review)
            self.session.commit()

    def get_by_category(self, category: CategoryEnum) -> List[Review]:
        stmt = select(Review).where(Review.category == category).order_by(Review.created_at.desc())
        return list(self.session.execute(stmt).scalars().all())
